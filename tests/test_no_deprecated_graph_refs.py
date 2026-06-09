"""Regression test: no operational use of deprecated graphify patterns.

Prevents regression of three issues fixed on 2026-06-08:
1. `knowledge.grap` typo / `.claude/context/knowledge.grap` path
   - Real location: `graphify-out/graph.json`
2. Non-existent `graphify similar` / `graphify dependents` commands
   - Real commands: `graphify query` / `graphify path` / `graphify explain`
3. Non-existent `graphify scan` command
   - Real command: `graphify .` (or `graphify . --update`)

The framework has been refactored to use the real graphify CLI and the real
graph.json file. This test ensures no future change reintroduces the dead
references IN AN OPERATIONAL CONTEXT.

**Exception**: Lines that LEGITIMATELY mention the deprecated patterns in
a deprecation-notice / migration-note context (e.g., "原 `knowledge.grap`
已重构废弃", "不是真实命令") are excluded from the assertion. These notes
are intentional and serve as migration aids for readers.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Directories to scan
SCAN_DIRS = [
    PROJECT_ROOT / ".claude" / "agents",
    PROJECT_ROOT / ".claude" / "commands",
    PROJECT_ROOT / ".claude" / "templates",
    PROJECT_ROOT / ".claude" / "skills",
    PROJECT_ROOT / ".claude" / "rules",
    PROJECT_ROOT / ".claude" / "docs",
]

# Patterns that should NOT appear in OPERATIONAL context.
# A line is "operational" if it doesn't look like a deprecation notice.
DEPRECATED_PATH_PATTERNS = [
    re.compile(r"\.claude/context/knowledge\.grap"),
    re.compile(r"\bknowledge\.grap\b"),
]

DEPRECATED_COMMAND_PATTERNS = [
    re.compile(r"\bgraphify\s+similar\b"),
    re.compile(r"\bgraphify\s+dependents\b"),
    re.compile(r"\bgraphify\s+scan\b"),
]

# Markers that indicate a line is a deprecation notice / migration note
# (NOT operational use). Any line containing one of these substrings is
# considered a "deprecation notice" and is excluded from the assertion.
DEPRECATION_NOTICE_MARKERS = [
    "已重构",
    "已废弃",
    "已弃用",
    "已删除",
    "不是真实命令",
    "已删除的命令",
    "不存在的命令",
    "注意：",  # explicit warning prefix
    "**注**：",  # deprecation footnote
    "(**注**",
    "(已废弃)",
    "（已废弃）",
    "(已弃用)",
    "（已弃用）",
    "deprecated",
    "Deprecated",
    "DEPRECATED",
    "已修正",
    "命令名修正",
]

# Files that are HISTORICAL audit reports or the canonical migration guide
# — exempt entirely (they document past state and reference deprecated
# patterns on purpose as part of the migration narrative)
HISTORICAL_REPORT_FILES = {
    "framework-audit-stage0.md",
    "framework-audit-2026-06-08.md",
    "framework-comparison.md",
    "to-improvement.md",
    # graphify-query-cheatsheet.md is the canonical migration guide —
    # it documents the old → new command mapping for readers.
    "graphify-query-cheatsheet.md",
}


def _is_deprecation_notice(line: str) -> bool:
    return any(marker in line for marker in DEPRECATION_NOTICE_MARKERS)


def _iter_framework_files() -> list[Path]:
    files: list[Path] = []
    for d in SCAN_DIRS:
        if not d.exists():
            continue
        files.extend(d.rglob("*.md"))
    return sorted(files)


def _scan_for_pattern(pattern: re.Pattern[str]) -> list[str]:
    """Return operational (non-deprecation-notice) matches of pattern."""
    offenders: list[str] = []
    for f in _iter_framework_files():
        if f.name in HISTORICAL_REPORT_FILES:
            continue
        text = f.read_text(encoding="utf-8")
        for i, line in enumerate(text.splitlines(), start=1):
            if pattern.search(line) and not _is_deprecation_notice(line):
                offenders.append(f"{f.relative_to(PROJECT_ROOT)}:{i}: {line.strip()}")
    return offenders


@pytest.mark.parametrize("pattern", DEPRECATED_PATH_PATTERNS)
def test_no_operational_knowledge_grap_path(pattern: re.Pattern[str]):
    """No file under .claude/ should OPERATE on the dead `knowledge.grap` path.

    Deprecation notices / migration notes are allowed.
    """
    offenders = _scan_for_pattern(pattern)
    assert not offenders, (
        f"Found {len(offenders)} operational reference(s) to deprecated `knowledge.grap`:\n"
        + "\n".join(f"  {o}" for o in offenders[:10])
        + ("\n  ..." if len(offenders) > 10 else "")
    )


@pytest.mark.parametrize("pattern", DEPRECATED_COMMAND_PATTERNS)
def test_no_operational_deprecated_graphify_command(pattern: re.Pattern[str]):
    """No file under .claude/ should OPERATE the non-existent graphify commands.

    Deprecation notices are allowed.
    """
    offenders = _scan_for_pattern(pattern)
    assert not offenders, (
        f"Found {len(offenders)} operational reference(s) to deprecated graphify command:\n"
        + "\n".join(f"  {o}" for o in offenders[:10])
        + ("\n  ..." if len(offenders) > 10 else "")
    )


def test_real_graphify_commands_documented():
    """The real graphify commands must be documented in the cheatsheet."""
    cheatsheet = (
        PROJECT_ROOT / ".claude" / "skills" / "graphify-query-cheatsheet.md"
    )
    if not cheatsheet.exists():
        pytest.skip("graphify cheatsheet not found")
    text = cheatsheet.read_text(encoding="utf-8")
    for cmd in ("query", "path", "explain"):
        assert f"graphify {cmd}" in text or f"`{cmd}`" in text, (
            f"graphify command `{cmd}` should be documented in cheatsheet"
        )


def test_real_graph_file_path_used_operationally():
    """The real graph file path `graphify-out/graph.json` must be used in
    operational contexts (NOT in a deprecation-notice context)."""
    real_path = "graphify-out/graph.json"
    files_with_real_path: list[str] = []
    for f in _iter_framework_files():
        if f.name in HISTORICAL_REPORT_FILES:
            continue
        text = f.read_text(encoding="utf-8")
        for i, line in enumerate(text.splitlines(), start=1):
            if real_path in line and not _is_deprecation_notice(line):
                files_with_real_path.append(f"{f.relative_to(PROJECT_ROOT)}")
                break
    # The real path should be used in at least the analyst-stage0 and ba-stage1
    # agents (these are the primary consumers of the knowledge graph)
    assert files_with_real_path, (
        f"No operational use of `{real_path}` found in framework files. "
        f"Refactor complete?"
    )
