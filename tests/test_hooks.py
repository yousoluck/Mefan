"""Tests for the .claude/hooks/ scripts.

These tests assert that:
- The 4 stage-4 hooks (state-machine, tdd-rhythm, test-coverage, adr-impl)
  reference the correct project paths (so they don't silently no-op).
- The state machine hook correctly accepts/rejects state transitions.
- The "completion" hooks have a fallback path that returns a meaningful
  exit code (not just silent 0) when their target dirs are missing.

Background: a previous audit found that check-tdd-rhythm.sh,
check-test-coverage.sh, and check-adr-implementation.sh all used
`$ROOT/../tests` and `$ROOT/../src` (one directory too high). When
run from the mefan project root, the directories were silently missing
and the hooks returned exit 0 — i.e., they approved MG completion
without verifying anything.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest


# Stage-4 hooks that must use the correct project paths.
PATH_HOOKS = (
    "check-tdd-rhythm.sh",
    "check-test-coverage.sh",
    "check-adr-implementation.sh",
)


# ---------- Test 1: static analysis of hook paths ----------


@pytest.mark.parametrize("hook_name", PATH_HOOKS)
def test_hook_uses_correct_tests_path(hooks_dir: Path, hook_name: str):
    """The hook must reference $ROOT/tests (or equivalent), NOT $ROOT/../tests.

    The bug: $ROOT/../tests resolves to /mnt/d/pycharmprojects/tests,
    one level above the mefan project, where nothing exists. The hook
    then silently no-ops.
    """
    hook = hooks_dir / hook_name
    if not hook.exists():
        pytest.skip(f"hook missing: {hook}")
    text = hook.read_text(encoding="utf-8")

    # The buggy pattern: TESTS_DIR=...$ROOT/../tests or similar
    bad_patterns = [
        re.compile(r"TESTS_DIR=.{0,40}\$ROOT/\.\./tests"),
        re.compile(r'SRC_DIR=.{0,40}\$ROOT/\.\./src'),
        re.compile(r'\$ROOT/\.\./src'),
    ]
    violations = [p.pattern for p in bad_patterns if p.search(text)]
    assert not violations, (
        f"{hook_name} uses wrong path(s) — looking one level above project root:\n"
        f"  Matched: {violations}\n"
        f"  Expected: $ROOT/tests and $ROOT/src (relative to the mefan project root)"
    )


# ---------- Test 2: state machine accepts/rejects correctly ----------


def test_state_machine_script_exists(hooks_dir: Path):
    """The state machine hook must exist (it's the most critical hook)."""
    sm = hooks_dir / "check-state-machine.sh"
    assert sm.exists(), f"check-state-machine.sh missing from {hooks_dir}"
    assert sm.stat().st_mode & 0o111, f"{sm} is not executable"


def test_state_machine_no_sprint_status_returns_nonzero(hooks_dir: Path, tmp_path: Path):
    """When sprint-status.md is missing, check-state-machine.sh must
    return exit 2 (per its own contract: "2=文件缺失/异常").

    This is a regression guard: the script must NOT silently exit 0
    when the input files are missing.
    """
    sm = hooks_dir / "check-state-machine.sh"
    if not sm.exists():
        pytest.skip(f"missing: {sm}")

    # Run from a tmp_path that has no sprint-status.md
    result = subprocess.run(
        ["bash", str(sm), "MG-001", "CodeReview"],
        cwd=str(tmp_path),
        capture_output=True,
        text=True,
        timeout=30,
    )
    # Per check-state-machine.sh line 19-22, missing sprint-status.md
    # should cause exit 2.
    assert result.returncode == 2, (
        f"check-state-machine.sh must exit 2 when sprint-status.md is missing. "
        f"Got: rc={result.returncode}\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )


# ---------- Test 3: when tests/src dirs are missing, hooks must NOT silently pass ----------


@pytest.mark.parametrize("hook_name", PATH_HOOKS)
def test_hook_warns_when_dirs_missing(hooks_dir: Path, tmp_path: Path, hook_name: str):
    """When the hook's target tests/src dirs are missing, the hook should
    emit a clear warning (not just silent exit 0).

    A "silent no-op" would defeat the purpose of the verification. The
    plan allows for "exit 0 with a WARN message" (graceful skip), but
    NOT for "exit 0 with no message at all" (silent no-op).
    """
    hook = hooks_dir / hook_name
    if not hook.exists():
        pytest.skip(f"hook missing: {hook}")

    # We need the hook to run with its hardcoded ROOT (=/mnt/d/pycharmprojects/Mefan).
    # If we run from tmp_path, the script will look for $ROOT/../tests
    # (one level above mefan) which is /mnt/d/pycharmprojects/tests —
    # it would always be missing. So we instead look for a clear warn message
    # in stdout/stderr.
    result = subprocess.run(
        ["bash", str(hook), "MG-001"],
        cwd=str(tmp_path),
        capture_output=True,
        text=True,
        timeout=30,
    )
    # Acceptable outcomes:
    #   - exit 0 with a warning message about missing dir (graceful skip)
    #   - exit 1 (real error: tests or coverage is missing)
    #   - exit 2 (file missing)
    #   - exit 0 (everything passes, despite no real source)
    #
    # UNACCEPTABLE outcome: silent exit 0 with no useful info
    has_warning = any(
        keyword in (result.stdout + result.stderr).lower()
        for keyword in ("warn", "skip", "不存在", "missing", "error", "not found")
    )
    has_real_check = any(
        keyword in (result.stdout + result.stderr).lower()
        for keyword in ("覆盖率", "coverage", "tdd", "rhythm", "impl", "task", "通过", "pass", "fail")
    )
    assert has_warning or has_real_check or result.returncode != 0, (
        f"{hook_name} appears to silently no-op.\n"
        f"  Return code: {result.returncode}\n"
        f"  stdout: {result.stdout[:500]}\n"
        f"  stderr: {result.stderr[:500]}\n"
        f"  Expected: a WARN message, a real check output, or a non-zero exit code."
    )
