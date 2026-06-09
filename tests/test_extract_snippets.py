"""Tests for extract-snippets.py (architect-stage0 §2.5.5).

The script reads $ROOT/.claude/context/query_plan.md (markdown table, skill_* rows)
and writes real source snippets to $ROOT/.claude/context/results.json.

N-rows 重构 2026-06-06 关键变更：
- query_plan.md schema 从 8 列扩到 10 列（新增 父章节 ID + 问题序号）
- target_id 必带 _qN 后缀（如 `skill_db_q1`）
- results.json snippets 从顶层 `items[*].snippets` 移到 `items[*].data.questions[0].snippets`
  （per-question 粒度；1 FE = 1 question，question_index=1）
- 脚本按 `parent_section_id` + `question_index` 路由到正确的 question

The critical regression we guard against: bash fallback column often contains
shell pipes like `| head` or `| grep "x"`. A naive `IFS='|'` split misaligns
the Code Target field, silently breaking snippet extraction. The fix is a
backtick-aware row parser.

Each test uses pytest's tmp_path fixture to build an isolated filesystem.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / ".claude/agents/scripts/extract-snippets.py"


# 10 列 schema（与 query-plan-template.md §2 skill_* 表格一致）
# 注意：cb_* 行也走通用 parser 路径（脚本会 skip），但 fixture 里包含 cb_*
# 用来验证 N-rows 不变量 + 非 skill 行的处理
QUERY_PLAN = """# Query Plan
> Test fixture (N-rows 重构 2026-06-06, SCHEMA_VERSION 2.1.0)

## 1. CB 调查项（4 个 question 拆 4 行）

| 目标 ID | 章节 | 调查项 | Graphify Query | Bash Fallback | Code Target | 期望结果 | 优先级 | 父章节 ID | 问题序号 |
|---------|------|--------|---------------|---------------|-------------|---------|--------|------------|----------|
| cb_1_1_q1 | §1.1 | 项目名称 | `graphify query "name"` | `grep "name" pyproject.toml` | n/a | name | P0 | cb_1_1 | 1 |
| cb_1_1_q2 | §1.1 | 项目版本 | `graphify query "version"` | `grep "version" pyproject.toml` | n/a | version | P0 | cb_1_1 | 2 |
| cb_1_1_q3 | §1.1 | 前端框架 | `graphify query "react"` | `grep "react" package.json` | n/a | framework | P0 | cb_1_1 | 3 |
| cb_1_1_q4 | §1.1 | 后端框架 | `graphify query "fastapi"` | `grep "fastapi" pyproject.toml` | n/a | framework | P0 | cb_1_1 | 4 |

## 2. Skill 调查项（1 FE = 1 行，target_id 带 _q1 后缀）

| 目标 ID | FE 来源 | 模板选择 | Graphify Query | Bash Fallback | Code Target | 期望结果 | 优先级 | 父章节 ID | 问题序号 |
|---------|---------|---------|---------------|---------------|-------------|---------|--------|------------|----------|
| skill_db_q1 | FE-I-001 | L1 | `graphify query "db"` | `grep -rn "engine" src/ | head -10` | src/db/config.py:1-3 | 配置 | P0 | skill_db | 1 |
| skill_api_q1 | FE-F-001 | L2 | `graphify query "api"` | `grep -rn "router" | grep "v1" | head` | src/api/users.py:1-2 | 端点 | P1 | skill_api | 1 |
| skill_empty_q1 | FE-I-002 | L1 | `graphify query "x"` | `grep "x" src/ | head` | *(空)* | - | P2 | skill_empty | 1 |
| skill_missing_q1 | FE-I-003 | L1 | `graphify query "y"` | `grep "y" src/ | head` | nonexistent.py:1-5 | y | P0 | skill_missing | 1 |
"""


def _setup_fixture(root: Path) -> None:
    """Create a minimal project tree with src files + query_plan + results.

    results.json 预填充 data.questions[] 结构（N-rows 重构后）。
    """
    db_dir = root / "src" / "db"
    db_dir.mkdir(parents=True)
    (db_dir / "config.py").write_text(
        "engine = create_engine(\n    DATABASE_URL,\n    pool_size=10\n)\n",
        encoding="utf-8",
    )
    api_dir = root / "src" / "api"
    api_dir.mkdir(parents=True)
    (api_dir / "users.py").write_text(
        "@router.get('/users')\nasync def list_users():\n    return []\n",
        encoding="utf-8",
    )
    context_dir = root / ".claude" / "context"
    context_dir.mkdir(parents=True)
    (context_dir / "query_plan.md").write_text(QUERY_PLAN, encoding="utf-8")
    # **N-rows 重构**：results.json 预填充 data.questions[] 结构
    (context_dir / "results.json").write_text(
        json.dumps(
            {
                "schema_version": "2.1.0",
                "items": {
                    "cb_1_1": {
                        "type": "cb_section",
                        "status": "success",
                        "data": {
                            "section_id": "1.1",
                            "questions": [
                                {"key": "cb_1_1_q1", "status": "success", "data": {"name": "Mefan"}},
                                {"key": "cb_1_1_q2", "status": "success", "data": {"version": "0.1.0"}},
                                {"key": "cb_1_1_q3", "status": "fallback", "data": {"frontend": "react"}},
                                {"key": "cb_1_1_q4", "status": "success", "data": {"backend": "fastapi"}},
                            ],
                        },
                    },
                    "skill_db": {
                        "type": "skill",
                        "status": "success",
                        "data": {
                            "fe_id": "FE-I-001",
                            "questions": [
                                {
                                    "key": "skill_db_q1",
                                    "status": "success",
                                    "data": {"engine": "SQLAlchemy"},
                                },
                            ],
                        },
                    },
                    "skill_api": {
                        "type": "skill",
                        "status": "success",
                        "data": {
                            "fe_id": "FE-F-001",
                            "questions": [
                                {"key": "skill_api_q1", "status": "success", "data": {}},
                            ],
                        },
                    },
                    "skill_empty": {
                        "type": "skill",
                        "status": "success",
                        "data": {"questions": [{"key": "skill_empty_q1", "status": "success", "data": {}}]},
                    },
                    "skill_missing": {
                        "type": "skill",
                        "status": "success",
                        "data": {"questions": [{"key": "skill_missing_q1", "status": "success", "data": {}}]},
                    },
                },
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def _read_db_snippets(results: dict) -> dict:
    """**N-rows 重构 helper**：从 items.skill_db.data.questions[0].snippets 取 snippets map。"""
    return results["items"]["skill_db"]["data"]["questions"][0]["snippets"]


def _read_api_snippets(results: dict) -> dict:
    return results["items"]["skill_api"]["data"]["questions"][0]["snippets"]


def test_extracts_snippet_when_bash_fallback_has_pipes(tmp_path: Path) -> None:
    """skill_db_q1 has bash fallback `... | head -10`; Code Target must still parse.

    N-rows 重构后：snippets 写入 `data.questions[0].snippets`（per-question 粒度）。
    """
    _setup_fixture(tmp_path)
    r = subprocess.run(
        [sys.executable, str(SCRIPT), str(tmp_path)],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, f"Script failed: {r.stderr}"
    results = json.loads((tmp_path / ".claude" / "context" / "results.json").read_text())
    db_snippets = _read_db_snippets(results)
    assert "src/db/config.py:1-3" in db_snippets, (
        f"Code Target not parsed correctly when bash fallback has | chars: {db_snippets}"
    )
    assert "create_engine" in db_snippets["src/db/config.py:1-3"]


def test_extracts_snippet_with_multiple_pipes_in_bash_fallback(tmp_path: Path) -> None:
    """skill_api_q1 bash fallback has 2 pipes: `... | grep "v1" | head`."""
    _setup_fixture(tmp_path)
    r = subprocess.run(
        [sys.executable, str(SCRIPT), str(tmp_path)],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, f"Script failed: {r.stderr}"
    results = json.loads((tmp_path / ".claude" / "context" / "results.json").read_text())
    api_snippets = _read_api_snippets(results)
    assert "src/api/users.py:1-2" in api_snippets, (
        f"Multiple | chars in bash fallback broke parsing: {api_snippets}"
    )
    assert "@router.get" in api_snippets["src/api/users.py:1-2"]


def test_skips_rows_with_empty_code_target(tmp_path: Path) -> None:
    """skill_empty_q1 has Code Target = `*(空)*`; no snippet should be written."""
    _setup_fixture(tmp_path)
    r = subprocess.run(
        [sys.executable, str(SCRIPT), str(tmp_path)],
        capture_output=True, text=True,
    )
    assert r.returncode == 0
    results = json.loads((tmp_path / ".claude" / "context" / "results.json").read_text())
    skill_empty_q = results["items"]["skill_empty"]["data"]["questions"][0]
    assert skill_empty_q.get("snippets", {}) == {}, (
        f"Expected no snippets for empty Code Target, got: {skill_empty_q.get('snippets')}"
    )


def test_soft_failure_when_file_missing(tmp_path: Path) -> None:
    """skill_missing_q1 cites nonexistent.py; should write soft-failure marker."""
    _setup_fixture(tmp_path)
    r = subprocess.run(
        [sys.executable, str(SCRIPT), str(tmp_path)],
        capture_output=True, text=True,
    )
    assert r.returncode == 0
    results = json.loads((tmp_path / ".claude" / "context" / "results.json").read_text())
    miss_q = results["items"]["skill_missing"]["data"]["questions"][0]
    miss_snippets = miss_q["snippets"]
    assert "nonexistent.py:1-5" in miss_snippets
    assert "SNIPPET_FETCH_FAILED" in miss_snippets["nonexistent.py:1-5"]
    assert "file not found" in miss_snippets["nonexistent.py:1-5"]


def test_only_skill_rows_processed(tmp_path: Path) -> None:
    """cb_1_1 是 CB 行（4 个 question，无 snippets 处理）; cb 行的 questions 数组应保持原状。"""
    _setup_fixture(tmp_path)
    r = subprocess.run(
        [sys.executable, str(SCRIPT), str(tmp_path)],
        capture_output=True, text=True,
    )
    assert r.returncode == 0
    results = json.loads((tmp_path / ".claude" / "context" / "results.json").read_text())
    # cb_* 行不应有顶层 snippets 字段
    assert "snippets" not in results["items"]["cb_1_1"]
    # cb_* 行的 questions 应保持 4 个 question，**无 snippets 子字段**
    cb_questions = results["items"]["cb_1_1"]["data"]["questions"]
    assert len(cb_questions) == 4, f"cb_1_1 应有 4 个 question，实际 {len(cb_questions)}"
    for q in cb_questions:
        assert "snippets" not in q, f"cb question 不应有 snippets: {q}"


def test_summary_counters_updated(tmp_path: Path) -> None:
    """Summary should reflect: 2 extracted, 1 failed, 0 truncated.

    N-rows 后 fixture 包含 4 个 skill_* 行：
    - skill_db_q1: extracted (1 行)
    - skill_api_q1: extracted (1 行)
    - skill_empty_q1: skipped (空 Code Target)
    - skill_missing_q1: failed (1 行)
    """
    _setup_fixture(tmp_path)
    r = subprocess.run(
        [sys.executable, str(SCRIPT), str(tmp_path)],
        capture_output=True, text=True,
    )
    assert r.returncode == 0
    results = json.loads((tmp_path / ".claude" / "context" / "results.json").read_text())
    summary = results["summary"]
    assert summary["snippets_extracted"] == 2, summary
    assert summary["snippets_failed"] == 1, summary
    assert summary["snippets_truncated"] == 0, summary


def test_truncates_oversized_snippet(tmp_path: Path) -> None:
    """If cited range > 100 lines, snippet is truncated with marker.

    N-rows 后：snippet 写入 data.questions[0].snippets。
    """
    big_file = tmp_path / "big.py"
    big_file.parent.mkdir(parents=True, exist_ok=True)
    big_file.write_text("\n".join(f"line_{i} = {i}" for i in range(1, 201)) + "\n")
    (tmp_path / ".claude" / "context").mkdir(parents=True)
    (tmp_path / ".claude" / "context" / "query_plan.md").write_text(
        "# Query Plan\n\n"
        "| 目标 ID | FE 来源 | 模板选择 | Graphify Query | Bash Fallback | Code Target | 期望结果 | 优先级 | 父章节 ID | 问题序号 |\n"
        "|---------|---------|---------|---------------|---------------|-------------|---------|--------|------------|----------|\n"
        "| skill_big_q1 | FE-X | L1 | `q` | `cat big.py` | big.py:1-200 | y | P0 | skill_big | 1 |\n",
        encoding="utf-8",
    )
    (tmp_path / ".claude" / "context" / "results.json").write_text(
        json.dumps(
            {
                "schema_version": "2.1.0",
                "items": {
                    "skill_big": {
                        "type": "skill",
                        "status": "success",
                        "data": {
                            "questions": [{"key": "skill_big_q1", "status": "success", "data": {}}]
                        },
                    }
                },
            }
        ),
        encoding="utf-8",
    )
    r = subprocess.run(
        [sys.executable, str(SCRIPT), str(tmp_path)],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stderr
    results = json.loads((tmp_path / ".claude" / "context" / "results.json").read_text())
    snippet = results["items"]["skill_big"]["data"]["questions"][0]["snippets"]["big.py:1-200"]
    assert "[TRUNCATED" in snippet
    assert "original had 200 lines" in snippet
    assert "line_1" in snippet
    assert "line_100" in snippet
    assert "line_101" not in snippet


def test_strip_question_suffix_helper() -> None:
    """N-rows helper: `skill_db_q1` → `skill_db`（去 _qN 后缀找 item key）。"""
    # 文件名 `extract-snippets.py` 含连字符，不能用 `import` 语句；
    # 用 importlib 按文件路径加载，模块名以 `extract_snippets` 别名注册。
    import importlib.util

    spec = importlib.util.spec_from_file_location("extract_snippets", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    strip_question_suffix = module.strip_question_suffix
    parse_question_index = module.parse_question_index
    assert strip_question_suffix("skill_db_q1") == "skill_db"
    assert strip_question_suffix("skill_db_q12") == "skill_db"
    assert strip_question_suffix("cb_1_1") == "cb_1_1"  # 无 _qN 后缀保持原样
    assert strip_question_suffix("cb_1_1_q3") == "cb_1_1"
    assert parse_question_index("skill_db_q1") == 1
    assert parse_question_index("skill_db_q42") == 42
    assert parse_question_index("cb_1_1") == 1  # 无 _qN → 1
    assert parse_question_index("cb_1_1_q3") == 3


def test_snippet_writes_to_correct_question_index(tmp_path: Path) -> None:
    """**N-rows 重构关键不变量**：target_id `_qN` 的 N 决定写入 data.questions[N-1].snippets。

    1 个 skill 多个 question 的场景：query_plan 里 2 行（_q1 + _q2）→ results.json
    data.questions 长度 = 2，_q1 写 q[0].snippets，_q2 写 q[1].snippets。
    """
    # 构造 1 个 skill 2 个 question 的 fixture
    (tmp_path / "src").mkdir(parents=True)
    (tmp_path / "src" / "a.py").write_text("a_line_1\na_line_2\n")
    (tmp_path / "src" / "b.py").write_text("b_line_1\nb_line_2\n")
    (tmp_path / ".claude" / "context").mkdir(parents=True)
    (tmp_path / ".claude" / "context" / "query_plan.md").write_text(
        "# Query Plan\n\n"
        "| 目标 ID | FE 来源 | 模板选择 | Graphify Query | Bash Fallback | Code Target | 期望结果 | 优先级 | 父章节 ID | 问题序号 |\n"
        "|---------|---------|---------|---------------|---------------|-------------|---------|--------|------------|----------|\n"
        "| skill_multi_q1 | FE-X | L1 | `q` | `cat` | src/a.py:1-2 | a | P0 | skill_multi | 1 |\n"
        "| skill_multi_q2 | FE-X | L1 | `q` | `cat` | src/b.py:1-2 | b | P1 | skill_multi | 2 |\n",
        encoding="utf-8",
    )
    (tmp_path / ".claude" / "context" / "results.json").write_text(
        json.dumps(
            {
                "schema_version": "2.1.0",
                "items": {
                    "skill_multi": {
                        "type": "skill",
                        "status": "success",
                        "data": {
                            "questions": [
                                {"key": "skill_multi_q1", "status": "success", "data": {}},
                                {"key": "skill_multi_q2", "status": "success", "data": {}},
                            ]
                        },
                    }
                },
            }
        ),
        encoding="utf-8",
    )
    r = subprocess.run(
        [sys.executable, str(SCRIPT), str(tmp_path)],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stderr
    results = json.loads((tmp_path / ".claude" / "context" / "results.json").read_text())
    questions = results["items"]["skill_multi"]["data"]["questions"]
    # **关键不变量**：q[0] 写 src/a.py，q[1] 写 src/b.py
    assert "src/a.py:1-2" in questions[0]["snippets"]
    assert "a_line_1" in questions[0]["snippets"]["src/a.py:1-2"]
    assert "src/b.py:1-2" in questions[1]["snippets"]
    assert "b_line_1" in questions[1]["snippets"]["src/b.py:1-2"]
    # 互不污染
    assert "src/a.py" not in questions[1].get("snippets", {})
    assert "src/b.py" not in questions[0].get("snippets", {})
