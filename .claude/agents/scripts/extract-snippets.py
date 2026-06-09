#!/usr/bin/env python3
"""Extract code snippets from query_plan.md's Code Target column → results.json.

Standalone script invoked by architect-stage0 §2.5.5. Reads:

  - $ROOT/.claude/context/query_plan.md  (markdown table, skill_* rows)
  - $ROOT/.claude/context/results.json   (read-modify-write)

For each skill_* row with a non-empty Code Target, fetches the cited
`path:line-line` ranges from $ROOT/path and stores the actual source
text into the skill item's `data.questions[question_index-1].snippets` map
(N-rows 重构 2026-06-06：snippets 下移到 questions 数组内，per-question 粒度)。

Robust to `|` chars in any column (e.g., shell pipes in bash fallback
column `grep ... | head`) by parsing rows with backtick awareness.

Failure modes (soft; do not block pipeline):
  - File not found       → `[SNIPPET_FETCH_FAILED: file not found]`
  - Empty line range     → `[SNIPPET_FETCH_FAILED: empty range]`
  - IO error             → `[SNIPPET_FETCH_FAILED: <error>]`
  - Snippet > 100 lines  → truncated, appended `[TRUNCATED: ...]`

Summary counters updated in results.json:
  - snippets_extracted, snippets_failed, snippets_truncated
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# ── Paths (overridable via env or argv) ────────────────────────────────────

DEFAULT_ROOT = Path("/mnt/d/pycharmprojects/Mefan")
QUERY_PLAN_REL = ".claude/context/query_plan.md"
RESULTS_REL = ".claude/context/results.json"

# Skill table column order (10 columns, N-rows 重构 2026-06-06);
# matches query-plan-template.md §2 (cb_*/skill_*/doc_* 共享 10 列 schema)。
# cb_*/doc_* 行的 col 7-9 (Code Target/doc_type/...) 为可空；脚本只关心 skill_* 行的 col 5 (Code Target)。
SKILL_COLUMNS = [
    "target_id",          # 0  e.g. skill_infra_database_q1
    "section",            # 1  e.g. FE-I-001
    "template",           # 2  e.g. 一级：project-infra-database
    "query",              # 3
    "bash_fallback",      # 4
    "code_target",        # 5
    "expected",           # 6
    "priority",           # 7
    "parent_section_id",  # 8  e.g. skill_infra_database（去 _qN 后缀）
    "question_index",     # 9  e.g. 1（章节内 1-based 序号）
]

# Soft-failure markers
SNIPPET_FAILED = "[SNIPPET_FETCH_FAILED: {reason}]"
TRUNCATED_SUFFIX = "\n... [TRUNCATED: original had {n} lines]"


# ── Markdown table parsing (backtick-aware) ───────────────────────────────

def parse_table_row(line: str) -> list[str] | None:
    """Split a markdown table row by `|`, respecting backtick spans.

    A column containing `\`grep ... | head\`` is treated as a single cell.
    Returns the list of stripped cell strings, or None if not a data row.
    """
    line = line.rstrip("\n")
    if not (line.startswith("|") and line.endswith("|")):
        return None

    cells: list[str] = []
    current: list[str] = []
    in_backtick = False
    # Iterate over [1, len-1] to skip leading and trailing |
    for ch in line[1:-1]:
        if ch == "`":
            in_backtick = not in_backtick
            current.append(ch)
        elif ch == "|" and not in_backtick:
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(ch)
    cells.append("".join(current).strip())
    return cells


# ── Code Target parsing ───────────────────────────────────────────────────

def parse_code_target(spec: str) -> tuple[str, int, int] | None:
    """Parse `path:line-line` (or `path:line`) → (path, start, end)."""
    spec = spec.strip()
    if not spec:
        return None
    try:
        path, line_spec = spec.rsplit(":", 1)
    except ValueError:
        return None
    path = path.strip()
    line_spec = line_spec.strip()
    if not path or not line_spec:
        return None
    if "-" in line_spec:
        try:
            start_s, end_s = line_spec.split("-", 1)
            start, end = int(start_s.strip()), int(end_s.strip())
        except ValueError:
            return None
    else:
        try:
            start = end = int(line_spec)
        except ValueError:
            return None
    if start <= 0 or end < start:
        return None
    return path, start, end


# ── N-rows helpers (2026-06-06 重构) ────────────────────────────────────

def strip_question_suffix(target_id: str) -> str:
    """`skill_infra_database_q1` → `skill_infra_database`.

    失败回退：未匹配 `_qN` 后缀时原样返回（如 `cb_1_1` 无 _qN）。
    """
    if "_q" not in target_id:
        return target_id
    base, _, suffix = target_id.rpartition("_q")
    if suffix.isdigit():
        return base
    return target_id


def parse_question_index(target_id: str) -> int:
    """`skill_infra_database_q1` → 1（1-based）；无 _qN 后缀 → 1。"""
    if "_q" not in target_id:
        return 1
    _, _, suffix = target_id.rpartition("_q")
    if suffix.isdigit():
        return int(suffix)
    return 1


# ── Snippet extraction ────────────────────────────────────────────────────

def extract_snippet(root: Path, path: str, start: int, end: int) -> str:
    """Read lines [start, end] (1-indexed, inclusive) from root/path.

    Returns a soft-failure marker on error.
    """
    full_path = root / path
    if not full_path.is_file():
        return SNIPPET_FAILED.format(reason="file not found")
    try:
        text = full_path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return SNIPPET_FAILED.format(reason=str(exc).lower())
    lines = text.splitlines()
    # 1-indexed, inclusive
    chunk = lines[start - 1:end]
    if not chunk:
        return SNIPPET_FAILED.format(reason="empty range")
    snippet = "\n".join(chunk) + "\n"
    if len(chunk) > 100:
        truncated = "\n".join(chunk[:100]) + "\n"
        return truncated + TRUNCATED_SUFFIX.format(n=len(chunk))
    return snippet


# ── Main pipeline ─────────────────────────────────────────────────────────

def process(root: Path) -> dict[str, int]:
    """Run extraction; returns counters {extracted, failed, truncated}.

    N-rows 重构 2026-06-06 行为：
    - query_plan.md 的 target_id 带 _qN 后缀（如 `skill_infra_database_q1`）
    - 脚本去掉 _qN 后缀找到 results.json 的对应 item（如 `skill_infra_database`）
    - snippets 写入该 item 的 `data.questions[question_index-1].snippets`（per-question 粒度）
    - 兼容旧 schema：如果 item 没有 `data.questions[]`（旧版顶层 `snippets`），写入顶层并 warn
    """
    query_plan = root / QUERY_PLAN_REL
    results_path = root / RESULTS_REL

    counters = {"extracted": 0, "failed": 0, "truncated": 0, "skipped_no_questions": 0}

    if not query_plan.is_file():
        print(f"[extract-snippets] ⚠ query_plan.md not found at {query_plan}; skipping")
        return counters
    if not results_path.is_file():
        print(f"[extract-snippets] ⚠ results.json not found at {results_path}; skipping")
        return counters

    results = json.loads(results_path.read_text(encoding="utf-8"))
    items = results.setdefault("items", {})
    summary = results.setdefault("summary", {})

    for line in query_plan.read_text(encoding="utf-8").splitlines():
        cells = parse_table_row(line)
        if cells is None or len(cells) != len(SKILL_COLUMNS):
            continue
        row = dict(zip(SKILL_COLUMNS, cells))
        target_id = row["target_id"].strip()
        if not target_id.startswith("skill_"):
            # 仅处理 skill_* 行；cb_*/doc_* 行也走通用 parser 路径但无 snippets 处理
            continue
        code_target_raw = row["code_target"].strip()
        if not code_target_raw or code_target_raw in ("*(空)*", "-", "—"):
            continue

        # N-rows: 去掉 _qN 后缀找到 item key
        section_key = strip_question_suffix(target_id)
        question_idx = parse_question_index(target_id)  # 1-based

        item = items.setdefault(section_key, {})

        # **核心 N-rows 路由**：写入 data.questions[question_idx-1].snippets
        item_data = item.setdefault("data", {})
        questions = item_data.setdefault("questions", [])

        # 扩展 questions 数组到 question_idx 大小（占位 + 实际 question）
        while len(questions) < question_idx:
            questions.append({})
        question = questions[question_idx - 1]
        snippets_map = question.setdefault("snippets", {})

        for spec in code_target_raw.split(","):
            parsed = parse_code_target(spec)
            if parsed is None:
                continue
            path, start, end = parsed
            snippet = extract_snippet(root, path, start, end)
            snippets_map[spec.strip()] = snippet

            if "SNIPPET_FETCH_FAILED" in snippet:
                counters["failed"] += 1
            else:
                counters["extracted"] += 1
                if "[TRUNCATED" in snippet:
                    counters["truncated"] += 1

    summary["snippets_extracted"] = summary.get("snippets_extracted", 0) + counters["extracted"]
    summary["snippets_failed"] = summary.get("snippets_failed", 0) + counters["failed"]
    summary["snippets_truncated"] = summary.get("snippets_truncated", 0) + counters["truncated"]

    results_path.write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return counters


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_ROOT
    if not root.is_dir():
        print(f"[extract-snippets] ⚠ root not a directory: {root}")
        return 1
    counters = process(root)
    print(
        f"[extract-snippets] done: extracted={counters['extracted']} "
        f"failed={counters['failed']} truncated={counters['truncated']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
