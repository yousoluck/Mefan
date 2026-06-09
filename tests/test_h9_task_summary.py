"""Tests for H9 closure: dev-stage4 writes task-summary/T-NNN.md (production side).

H9 was identified as a broken link during the 2026-06-06 audit:
- Consumption side (pm-stage6 操作 1 §1.2) reads `task-summary/` — already fixed
- Production side (dev-stage4) had NO `task-summary` mention — now fixed via 操作 3.7

These tests verify:
1. dev-stage4.md has 操作 3.7 with the correct structure
2. The task-summary template contains the 6 required sections
3. The file path uses the standard `.claude/iterations/sprint-latest/task-summary/T-{TASK_ID}.md`
4. The doc is wired up (superpowers-integration.md §J shows H9 as ✅)

If any of these fail, the H9 link is broken and pm-stage6 will silently skip
the data aggregation step (per `if [ -d "$TASK_SUMMARY_DIR" ]` guard).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest


# ---------- Helpers ----------


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _has_section(text: str, section_heading: str) -> bool:
    """Check if `text` contains a markdown section heading like `## {section_heading}`.

    Accepts both top-level headings (`## X`) and indented headings inside code blocks
    (`   ## X`), since the task-summary template is embedded in a markdown code block
    in dev-stage4.md 操作 3.7.
    """
    return bool(
        re.search(
            rf"^\s*##\s+{re.escape(section_heading)}\s*$",
            text,
            re.MULTILINE,
        )
    )


def _has_substring(text: str, needle: str) -> bool:
    """Check if `text` contains the literal substring `needle`."""
    return needle in text


# ---------- Test 1: dev-stage4 has 操作 3.7 with task-summary write ----------


def test_dev_stage4_has_operation_3_7(agents_dir: Path):
    """dev-stage4.md must contain 操作 3.7 (task-summary writer) per H9 fix.

    The operation must:
    - Be numbered `### 操作 3.7`
    - Reference `task-summary` directory
    - Reference `Write` tool
    - Include the Task ID pattern `T-{TASK_ID}` or `T-{NNN}`
    """
    p = agents_dir / "dev-stage4.md"
    assert p.exists()
    text = _read(p)

    # Find the 操作 3.7 section
    m = re.search(
        r"^### 操作 3\.7[：:]\s*(.+?)$",
        text,
        re.MULTILINE,
    )
    assert m, (
        f"dev-stage4.md missing '### 操作 3.7' section. "
        f"H9 fix requires a new operation that writes task-summary/T-NNN.md."
    )

    # Extract the section body
    section_start = m.end()
    next_section = re.search(r"^### 操作 \d", text[section_start:], re.MULTILINE)
    section_end = section_start + next_section.start() if next_section else len(text)
    section = text[section_start:section_end]

    # Must reference task-summary
    assert "task-summary" in section, (
        f"操作 3.7 must reference `task-summary` directory. Got:\n{section[:200]}"
    )

    # Must reference Write tool
    assert re.search(r"\bWrite\b", section), (
        f"操作 3.7 must reference `Write` tool. Got:\n{section[:200]}"
    )

    # Must include Task ID placeholder
    assert re.search(r"T-\{TASK_ID\}|T-\{NNN\}", section), (
        f"操作 3.7 must include a Task ID placeholder (T-{{TASK_ID}} or T-{{NNN}}). "
        f"Got:\n{section[:200]}"
    )


# ---------- Test 2: task-summary template has the 6 required sections ----------


REQUIRED_TEMPLATE_SECTIONS = [
    "基本信息",     # 任务 ID, 所属 US/MG, 完成时间, 开发者
    "实现要点",     # API 签名, 关键算法/决策
    "测试覆盖",     # 单元测试, 集成测试, 未覆盖场景
    "技术债务",     # 债务项列表
    "关联 ADR",     # ADR § 章节引用
    "状态",         # Code Review, 已合并
]


def test_task_summary_template_has_all_sections(agents_dir: Path):
    """dev-stage4.md 操作 3.7's task-summary template must contain all 6 sections.

    These sections are what pm-stage6 操作 1 §1.2 grep-parses for tech debt aggregation.
    Missing any section → silent data loss in stage 6.
    """
    p = agents_dir / "dev-stage4.md"
    text = _read(p)

    missing = [s for s in REQUIRED_TEMPLATE_SECTIONS if not _has_section(text, s)]
    assert not missing, (
        f"task-summary template in dev-stage4.md 操作 3.7 is missing sections: {missing}\n"
        f"pm-stage6 grep-parses these for tech debt aggregation."
    )


# ---------- Test 3: file path matches the consumption contract ----------


def test_task_summary_path_matches_consumption(agents_dir: Path):
    """dev-stage4's write path must match pm-stage6's read path.

    - Producer (dev-stage4): `.claude/iterations/sprint-latest/task-summary/T-{TASK_ID}.md`
    - Consumer (pm-stage6):  `.claude/iterations/sprint-latest/task-summary/`
    """
    producer = _read(agents_dir / "dev-stage4.md")
    consumer = _read(agents_dir / "pm-stage6.md")

    # Both must use the same path
    path = ".claude/iterations/sprint-latest/task-summary"

    assert path in producer, (
        f"dev-stage4.md must write to `{path}/T-{{TASK_ID}}.md`"
    )
    assert path in consumer, (
        f"pm-stage6.md must read from `{path}/` (already verified by test_loop_closure)"
    )


# ---------- Test 4: superpowers-integration.md §J shows H9 as fixed ----------


def test_superpowers_integration_marks_h9_fixed(repo_root: Path):
    """The framework doc must reflect the H9 fix in §J (verification table) + changelog.

    Guards against doc drift: if the fix is reverted but the doc is not updated,
    this test fails.
    """
    p = repo_root / ".claude" / "rules" / "global" / "superpowers-integration.md"
    assert p.exists()
    text = _read(p)

    # §J table row for H9 must show ✅
    m = re.search(
        r"\|\s*H9\s*\|\s*task-summary/T-NNN\.md\s*\|\s*([^|]+?)\s*\|",
        text,
    )
    assert m, (
        f"superpowers-integration.md §J table missing H9 row, or row format changed."
    )
    status = m.group(1).strip()
    assert "已修" in status or "✅" in status, (
        f"H9 row in §J table should show ✅ 已修, got: {status!r}\n"
        f"Update the table after fixing H9."
    )

    # Changelog must have a H9 entry
    assert "H9 修复" in text or "H9修复" in text, (
        f"superpowers-integration.md changelog missing H9 fix entry."
    )


# ---------- Test 5: H9 is removed from K.2 pending list ----------


def test_h9_removed_from_k2_pending_list(repo_root: Path):
    """K.2 待办清单 should no longer list H9 as P1 pending.

    After the fix, H9 should be marked ✅ 已修 in the pending list.
    """
    p = repo_root / ".claude" / "rules" / "global" / "superpowers-integration.md"
    text = _read(p)

    # Find the K.2 table area
    m = re.search(
        r"### K\.2[^\n]*\n(.*?)(?=\n###|\Z)",
        text,
        re.DOTALL,
    )
    assert m, "superpowers-integration.md missing K.2 section"

    k2_text = m.group(1)

    # H9 must appear as ✅ 已修, not as P1
    h9_row = re.search(r"\|\s*H9[^|]*\|[^\n]*", k2_text)
    if h9_row:
        assert "已修" in h9_row.group(0) or "✅" in h9_row.group(0), (
            f"K.2 待办清单 H9 row should show ✅ 已修, got: {h9_row.group(0)!r}"
        )
