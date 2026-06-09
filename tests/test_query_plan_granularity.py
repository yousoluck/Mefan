"""Tests for query_plan.md / results.json N-rows invariants (2026-06-06 refactor).

The N-rows refactor (2026-06-06) changed query_plan.md from "1 row per section" to
"N rows per question" (1 row = 1 atomic question). The matching results.json
schema wraps each section in an item with a `data.questions: QuestionItem[]`
array (per-question granularity).

These tests guard against regressions in the 4 critical invariants:

1. **Every row must have a `parent_section_id`** (N-rows 重构 adds 2 columns:
   `parent_section_id` + `question_index` to the 8-column legacy schema).
2. **results.json questions count must match query_plan row count** (per
   `parent_section_id`). E.g., if `cb_1_1` has 4 rows in query_plan.md, then
   `items.cb_1_1.data.questions.length == 4`.
3. **No legacy chapter-level data** (顶层 `fields` / `chapters` / `elements`
   must NOT exist outside `data.questions[]`). The legacy schema had these as
   the primary storage; the new schema demotes them to optional aggregations.
4. **feature_elements_section 保持 1 FE = 1 row** (no N×M explosion). The
   `feature_elements_section` type is special-cased to 1 question per row,
   even though `data.elements[]` may contain many FE records (it's the FE
   metadata aggregation, not a question decomposition).

Each test uses pytest's tmp_path fixture to build an isolated filesystem.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import pytest

# Reuse the existing backtick-aware parser from extract-snippets.py.
# This keeps test parsing logic identical to production parsing.
SCRIPT = Path(__file__).resolve().parent.parent / ".claude/agents/scripts/extract-snippets.py"

# 10-column schema header (matches query-plan-template.md §1/§2/§3).
CB_HEADER = "| 目标 ID | 章节 | 调查项 | Graphify Query | Bash Fallback | Code Target | 期望结果 | 优先级 | 父章节 ID | 问题序号 |"
SKILL_HEADER = "| 目标 ID | FE 来源 | 模板选择 | Graphify Query | Bash Fallback | Code Target | 期望结果 | 优先级 | 父章节 ID | 问题序号 |"
DOC_HEADER = "| 目标 ID | 章节 | 调查项 | Graphify Query | Bash Fallback | 期望结果 | 优先级 | doc_type | 父章节 ID | 问题序号 |"


def _load_extract_snippets_module() -> Any:
    """Import extract-snippets.py (hyphenated filename) via importlib.

    The script file is `extract-snippets.py` (hyphen), which cannot be imported
    by Python's normal `import` statement. Use importlib to load it as
    `extract_snippets` module dynamically. This keeps the test parsing logic
    identical to production parsing.
    """
    import importlib.util

    spec = importlib.util.spec_from_file_location("extract_snippets", SCRIPT)
    assert spec is not None and spec.loader is not None, (
        f"Could not create import spec for {SCRIPT}"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _parse_query_plan_rows(md: str, header: str) -> list[dict[str, str]]:
    """Parse all data rows of a query_plan.md table.

    Returns a list of {col_name: value} dicts. Reuses extract-snippets.py's
    backtick-aware parser to match production behavior.
    """
    snippets_mod = _load_extract_snippets_module()
    parse_table_row = snippets_mod.parse_table_row
    SKILL_COLUMNS = snippets_mod.SKILL_COLUMNS

    rows: list[dict[str, str]] = []
    for line in md.splitlines():
        cells = parse_table_row(line)
        if cells is None or len(cells) != len(SKILL_COLUMNS):
            continue
        row = dict(zip(SKILL_COLUMNS, cells))
        # The 3 tables in the template use slightly different headers but
        # share the 10-column physical schema; SKILL_COLUMNS is a superset.
        # We accept any of the 3 types by matching on first cell pattern.
        target_id = row["target_id"].strip()
        if not (
            target_id.startswith("cb_")
            or target_id.startswith("skill_")
            or target_id.startswith("doc_")
        ):
            continue
        rows.append(row)
    return rows


# ─── Test 1: Every row must have parent_section_id ────────────────────────


def test_query_plan_rows_have_parent_section_id(tmp_path: Path) -> None:
    """Every data row in query_plan.md must declare a `parent_section_id`.

    N-rows 重构（2026-06-06）新增的强制列。缺失该列 = 行无法路由到正确的
    results.json item，下游 AI 组装时会找不到对应 question 数组。

    Test fixture: 4 cb rows (cb_1_1 × 4 questions) + 2 skill rows (1 FE each)
    + 2 doc rows (doc_project_s_1_1 × 2 questions).
    """
    md = f"""# Query Plan
> SCHEMA_VERSION: 2.1.0

## 1. CB 调查项

{CB_HEADER}
|---------|------|--------|---------------|---------------|-------------|---------|--------|------------|----------|
| cb_1_1_q1 | §1.1 | name | `q` | `grep` | n/a | name | P0 | cb_1_1 | 1 |
| cb_1_1_q2 | §1.1 | version | `q` | `grep` | n/a | version | P0 | cb_1_1 | 2 |
| cb_1_1_q3 | §1.1 | frontend | `q` | `grep` | n/a | framework | P0 | cb_1_1 | 3 |
| cb_1_1_q4 | §1.1 | backend | `q` | `grep` | n/a | framework | P0 | cb_1_1 | 4 |

## 2. Skill 调查项

{SKILL_HEADER}
|---------|---------|---------|---------------|---------------|-------------|---------|--------|------------|----------|
| skill_infra_database_q1 | FE-I-001 | L1 | `q` | `grep` | src/db.py:1-5 | 配置 | P0 | skill_infra_database | 1 |
| skill_infra_cache_q1 | FE-I-002 | L1 | `q` | `grep` | *(空)* | 缓存 | P0 | skill_infra_cache | 1 |

## 3. PM context 调查项

{DOC_HEADER}
|---------|------|--------|---------------|---------------|---------|--------|----------|------------|----------|
| doc_project_s_1_1_q1 | §1.1 | name | `q` | `grep` | name | P0 | project | doc_project_s_1_1 | 1 |
| doc_project_s_1_1_q2 | §1.1 | type | `q` | `grep` | type | P0 | project | doc_project_s_1_1 | 2 |
"""
    (tmp_path / "query_plan.md").write_text(md, encoding="utf-8")

    rows = _parse_query_plan_rows(md, CB_HEADER)
    assert len(rows) == 8, f"Expected 8 data rows, parsed {len(rows)}"

    # **核心断言**：每行 parent_section_id 必须非空
    for r in rows:
        assert r["parent_section_id"].strip(), (
            f"Row {r['target_id']!r} is missing parent_section_id; "
            f"this row cannot be routed to results.json"
        )

    # question_index 必须能从 1 解析为正整数
    for r in rows:
        qidx = r["question_index"].strip()
        assert qidx.isdigit() and int(qidx) >= 1, (
            f"Row {r['target_id']!r} has invalid question_index={qidx!r}"
        )


# ─── Test 2: results.json questions count must match plan ─────────────────


def test_results_json_questions_count_matches_plan(tmp_path: Path) -> None:
    """**N-rows 不变量**：items[*].data.questions.length == query_plan.md
    中 parent_section_id 等于该 item key 的行数。

    Fixture: query_plan.md has 3 sections with different question counts:
    - cb_1_1: 4 rows
    - skill_infra_database: 1 row
    - doc_project_s_1_1: 2 rows

    results.json must have items.cb_1_1.data.questions.length == 4,
    items.skill_infra_database.data.questions.length == 1, etc.
    """
    md = f"""# Query Plan
> SCHEMA_VERSION: 2.1.0

{CB_HEADER}
|---------|------|--------|---------------|---------------|-------------|---------|--------|------------|----------|
| cb_1_1_q1 | §1.1 | name | `q` | `grep` | n/a | name | P0 | cb_1_1 | 1 |
| cb_1_1_q2 | §1.1 | version | `q` | `grep` | n/a | version | P0 | cb_1_1 | 2 |
| cb_1_1_q3 | §1.1 | frontend | `q` | `grep` | n/a | framework | P0 | cb_1_1 | 3 |
| cb_1_1_q4 | §1.1 | backend | `q` | `grep` | n/a | framework | P0 | cb_1_1 | 4 |

{SKILL_HEADER}
|---------|---------|---------|---------------|---------------|-------------|---------|--------|------------|----------|
| skill_infra_database_q1 | FE-I-001 | L1 | `q` | `grep` | src/db.py:1-5 | 配置 | P0 | skill_infra_database | 1 |

{DOC_HEADER}
|---------|------|--------|---------------|---------------|---------|--------|----------|------------|----------|
| doc_project_s_1_1_q1 | §1.1 | name | `q` | `grep` | name | P0 | project | doc_project_s_1_1 | 1 |
| doc_project_s_1_1_q2 | §1.1 | type | `q` | `grep` | type | P0 | project | doc_project_s_1_1 | 2 |
"""
    (tmp_path / "query_plan.md").write_text(md, encoding="utf-8")

    # Step 1: 从 query_plan.md 聚合出每个 parent_section_id 的行数
    rows = _parse_query_plan_rows(md, CB_HEADER)
    expected_counts: dict[str, int] = {}
    for r in rows:
        psid = r["parent_section_id"].strip()
        expected_counts[psid] = expected_counts.get(psid, 0) + 1

    assert expected_counts == {
        "cb_1_1": 4,
        "skill_infra_database": 1,
        "doc_project_s_1_1": 2,
    }, f"Plan row counts: {expected_counts}"

    # Step 2: 构造完全匹配 plan 的 results.json（每 item.data.questions 长度 == 行数）
    results = {
        "schema_version": "2.1.0",
        "items": {
            "cb_1_1": {
                "type": "cb_section",
                "status": "success",
                "data": {
                    "questions": [
                        {"key": f"cb_1_1_q{i}", "status": "success", "data": {}}
                        for i in range(1, 5)
                    ]
                },
            },
            "skill_infra_database": {
                "type": "skill",
                "status": "success",
                "data": {
                    "questions": [
                        {"key": "skill_infra_database_q1", "status": "success", "data": {}}
                    ]
                },
            },
            "doc_project_s_1_1": {
                "type": "project_section",
                "status": "success",
                "data": {
                    "questions": [
                        {"key": f"doc_project_s_1_1_q{i}", "status": "success", "data": {}}
                        for i in range(1, 3)
                    ]
                },
            },
        },
    }
    (tmp_path / "results.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8"
    )

    # Step 3: **核心断言** — 加载 results.json 并逐 item 验证
    loaded = json.loads((tmp_path / "results.json").read_text())
    for psid, expected in expected_counts.items():
        actual = len(loaded["items"][psid]["data"]["questions"])
        assert actual == expected, (
            f"items.{psid}.data.questions.length mismatch: "
            f"expected {expected} (from query_plan.md), got {actual}"
        )


# ─── Test 3: No legacy chapter-level data ────────────────────────────────


def _detect_legacy_chapter_data(results: dict[str, Any]) -> list[str]:
    """Detect legacy top-level `fields` / `chapters` / `elements` on items.

    N-rows 重构 (2026-06-06) requires these fields to live **only inside**
    `data.questions[*].data` (as aggregation views). Their presence at the
    item's top level indicates an incomplete migration.

    Returns a list of violation strings (empty = no violations).
    """
    violations: list[str] = []
    for item_key, item in results.get("items", {}).items():
        for legacy_field in ("fields", "chapters", "elements"):
            if legacy_field in item:
                violations.append(
                    f"items.{item_key} has legacy top-level `{legacy_field}` field; "
                    f"must live inside `data.questions[*].data`"
                )
    return violations


def test_no_legacy_chapter_level_data(tmp_path: Path) -> None:
    """**Migration completeness invariant**：results.json items 不应有顶层
    (data 之外的) `fields` / `chapters` / `elements`。

    旧版 schema 把这些字段作为 item 顶层字段（如 `item.fields` / `item.chapters`）。
    N-rows 重构后，它们**只能**作为 `data.questions[*].data` 内部的便捷聚合形式
    （或 `data.fields` / `data.chapters` 聚合视图），**不能**出现在 item 顶层。

    Test scenarios:
    1. **Bad fixture** (item 顶层有 `fields`): validator should report violation
    2. **Good fixture** (item 顶层无 legacy, 但 data.questions[].data 内可有
       聚合视图): validator should report no violations
    """
    # ── Scenario 1: bad fixture (legacy `fields` at item top level) ─────
    bad_results = {
        "schema_version": "2.1.0",
        "items": {
            "cb_1_1": {
                "type": "cb_section",
                "status": "success",
                "fields": {  # ❌ legacy field at item top level
                    "project_name": "Mefan",
                    "project_version": "0.1.0",
                },
                "data": {
                    "questions": [
                        {
                            "key": "cb_1_1_q1",
                            "status": "success",
                            "data": {"name": "Mefan"},
                        }
                    ]
                },
            }
        },
    }
    (tmp_path / "bad_results.json").write_text(
        json.dumps(bad_results, indent=2), encoding="utf-8"
    )
    bad_violations = _detect_legacy_chapter_data(
        json.loads((tmp_path / "bad_results.json").read_text())
    )
    assert any("cb_1_1" in v and "fields" in v for v in bad_violations), (
        f"Validator should flag top-level `fields` on cb_1_1; got: {bad_violations}"
    )

    # ── Scenario 2: good fixture (item 顶层无 legacy, 聚合视图在 data 内) ──
    good_results = {
        "schema_version": "2.1.0",
        "items": {
            "skill_infra_database": {
                "type": "skill",
                "status": "success",
                "data": {
                    "questions": [
                        {
                            "key": "skill_infra_database_q1",
                            "status": "success",
                            "data": {
                                "fields": {  # ✅ 聚合视图（在 data.questions[].data 内）
                                    "engine": "SQLAlchemy",
                                },
                                "chapters": {  # ✅ 聚合视图
                                    "数据源配置": "...",
                                },
                            },
                        }
                    ]
                },
            }
        },
    }
    (tmp_path / "good_results.json").write_text(
        json.dumps(good_results, indent=2), encoding="utf-8"
    )
    good_violations = _detect_legacy_chapter_data(
        json.loads((tmp_path / "good_results.json").read_text())
    )
    assert good_violations == [], (
        f"Good fixture should have no violations; got: {good_violations}"
    )
    # 还要验证聚合视图本身可以正常访问
    skill_item = good_results["items"]["skill_infra_database"]
    q_data = skill_item["data"]["questions"][0]["data"]
    assert q_data["fields"]["engine"] == "SQLAlchemy"
    assert "数据源配置" in q_data["chapters"]


# ─── Test 4: feature_elements_section 保持 1 FE = 1 row ──────────────────


def test_feature_elements_one_row_per_fe(tmp_path: Path) -> None:
    """**防 N×M 爆炸回潮**：`feature_elements_section` 章节的 query_plan.md
    行数 = FE 数（即 1:1），**不是** = FE 数 × 字段数。

    例：feature-elements.md §3.1 L1 基础设施有 8 个 FE（FE-I-001~008），
    query_plan.md 中 `doc_feature_s_3_1` 章节下应该**恰好 8 行**
    （1 FE = 1 row），**不是** 64 行（8 FE × 8 字段）。

    FE 元数据通过 1 个 graphify query 整体拿，data.elements[] 数组承载
    聚合形式（不是 question 分解）。
    """
    # 模拟 feature-elements.md L1 基础设施有 5 个 FE
    fe_list = ["FE-I-001", "FE-I-002", "FE-I-005", "FE-I-007", "FE-I-008"]
    n_fes = len(fe_list)

    # 构造 query_plan.md：1 FE = 1 row（保持 1:1）
    fe_rows = "\n".join(
        f"| doc_feature_s_3_1_q{i + 1} | §3.1 L1 基础设施 | {fe} 元数据 | `q` | `grep` | 元数据聚合 | P0 | feature_elements | doc_feature_s_3_1 | {i + 1} |"
        for i, fe in enumerate(fe_list)
    )

    md = f"""# Query Plan
> SCHEMA_VERSION: 2.1.0

{DOC_HEADER}
|---------|------|--------|---------------|---------------|---------|--------|----------|------------|----------|
{fe_rows}
"""
    (tmp_path / "query_plan.md").write_text(md, encoding="utf-8")

    rows = _parse_query_plan_rows(md, DOC_HEADER)
    rows_for_3_1 = [r for r in rows if r["parent_section_id"].strip() == "doc_feature_s_3_1"]

    # **核心断言**：doc_feature_s_3_1 的行数 == FE 数（1:1）
    assert len(rows_for_3_1) == n_fes, (
        f"feature_elements_section N×M explosion detected: "
        f"expected {n_fes} rows (1 FE = 1 row), got {len(rows_for_3_1)}"
    )

    # question_index 应该是 1..N 连续
    for i, r in enumerate(rows_for_3_1, start=1):
        assert int(r["question_index"].strip()) == i, (
            f"question_index not continuous: row {i} has "
            f"question_index={r['question_index']!r}"
        )

    # 构造 results.json：1 question 包含 5 个 FE 的元数据（聚合在 data.elements[]）
    results = {
        "schema_version": "2.1.0",
        "items": {
            "doc_feature_s_3_1": {
                "type": "feature_elements_section",
                "status": "success",
                "data": {
                    "questions": [
                        {
                            "key": "doc_feature_s_3_1_q1",
                            "question": "L1 基础设施元数据（DB/Cache/MQ 等 FE）",
                            "status": "success",
                            "data": {
                                "elements": [
                                    {"id": fe, "name_zh": f"FE {fe}"} for fe in fe_list
                                ]
                            },
                        }
                    ]
                },
            }
        },
    }
    (tmp_path / "results.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8"
    )

    loaded = json.loads((tmp_path / "results.json").read_text())
    questions = loaded["items"]["doc_feature_s_3_1"]["data"]["questions"]

    # 1 FE = 1 row → 1 question（聚合所有 FE 元数据在 data.elements[]）
    assert len(questions) == 1, (
        f"feature_elements_section should have 1 question (FE metadata aggregation), "
        f"got {len(questions)}"
    )
    elements = questions[0]["data"]["elements"]
    assert len(elements) == n_fes, (
        f"Expected {n_fes} FE elements in data.questions[0].data.elements, "
        f"got {len(elements)}"
    )
    assert [e["id"] for e in elements] == fe_list
