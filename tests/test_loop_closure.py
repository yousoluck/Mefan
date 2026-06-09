"""Tests for Stage 6 → Stage 0 main loop closure.

These tests verify that:
1. pm-stage0 操作 0.7 reads evolution-proposals, iteration-retrospective, PROJECT_STATUS, sprint-N 归档
2. architect-stage0 操作 0.1a reads CHANGELOG + HARNESS_VERSION
3. pm-stage6 操作 1 reads task-summary + bug-log (Stage 4 debt + Stage 5 defects)

The closures form the main iteration loop:
  Stage 0 → 1 → 2 → 3 → 4 → 5 → 6 → 下一迭代 Stage 0
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest


# ---------- Helpers ----------


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _has_read_mention(text: str, pattern: str) -> bool:
    """Check if `text` mentions a Read of the given file pattern.

    Accepts both `Read` tool calls and inline comments mentioning the path.
    """
    # Match `Read` followed by the pattern (allowing both `Read` tool and `Read 工具`)
    return bool(
        re.search(rf"Read\s+(?:工具\s+)?[`'\"]?[^`'\"]*{re.escape(pattern)}", text)
    )


# ---------- Test 1: pm-stage0 closes the Stage 6 loop (4 reads) ----------


PM_STAGE0_READS = [
    "evolution-proposals",      # B1: coach-stage6 进化提案
    "iteration-retrospective",  # B2: pm-stage6 复盘
    "PROJECT_STATUS",           # B3: pm-stage6 步骤 4 全局状态
    "sprint-",                  # B8: sprint-N 归档（最近一次）
]


def test_pm_stage0_closes_stage6_loop(agents_dir: Path):
    """pm-stage0 操作 0.7 must read 4 stage 6 output files.

    Per plan §四 B1-B4 + B8.
    """
    p = agents_dir / "pm-stage0.md"
    assert p.exists()
    text = _read(p)

    missing = [r for r in PM_STAGE0_READS if not _has_read_mention(text, r)]
    assert not missing, (
        f"pm-stage0.md 操作 0.7 missing Read for: {missing}\n"
        f"Stage 6→Stage 0 main loop not closed."
    )


# ---------- Test 2: architect-stage0 reads framework changelog ----------


ARCH_STAGE0_READS = [
    "CHANGELOG",         # B4: 变更日志
    "HARNESS_VERSION",   # B4: 版本号
]


def test_architect_stage0_reads_framework_changelog(agents_dir: Path):
    """architect-stage0 操作 0.1a must read CHANGELOG + HARNESS_VERSION.

    Per plan §四 B4.
    """
    p = agents_dir / "architect-stage0.md"
    assert p.exists()
    text = _read(p)

    missing = [r for r in ARCH_STAGE0_READS if not _has_read_mention(text, r)]
    assert not missing, (
        f"architect-stage0.md 操作 0.1a missing Read for: {missing}\n"
        f"Framework changelog awareness not wired."
    )


# ---------- Test 3: pm-stage6 reads Stage 4 debt + Stage 5 bugs ----------


PM_STAGE6_READS = [
    "task-summary",  # B7: Stage 4 任务级技术债务
    "bug-log",       # B7: Stage 5 缺陷趋势
]


def test_pm_stage6_reads_stage4_debt_and_stage5_bugs(agents_dir: Path):
    """pm-stage6 操作 1 must read task-summary (Stage 4 debt) + bug-log (Stage 5 defects).

    Per plan §四 B7.
    """
    p = agents_dir / "pm-stage6.md"
    assert p.exists()
    text = _read(p)

    missing = [r for r in PM_STAGE6_READS if not _has_read_mention(text, r)]
    assert not missing, (
        f"pm-stage6.md 操作 1 missing Read for: {missing}\n"
        f"Stage 4→6 debt/defect feedback not wired."
    )


# ---------- Test 4: iteration-planning.md no longer references stale iteration-plan.md ----------


def test_iteration_planning_rule_no_stale_ref(agents_dir: Path, repo_root: Path):
    """iteration-planning.md should not contain `iteration-plan.md` document requirement.

    Per plan §四 B6. pm-stage3 already merged it into sprint-status.md.
    """
    p = repo_root / ".claude" / "rules" / "global" / "iteration-planning.md"
    assert p.exists()
    text = _read(p)
    assert "iteration-plan.md" not in text, (
        f"{p.name} still references stale `iteration-plan.md`. "
        f"pm-stage3 already merged this into sprint-status.md — clean up the rule."
    )
