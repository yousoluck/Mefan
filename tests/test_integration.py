"""Stage 4 integration tests for the mefan framework.

These tests verify the end-to-end 7-state machine flow
(Dev → Self-Check → Code Review → QA-Test-Coding → Test Code Review →
Testing → Close) by simulating a sprint with mock ADR / sprint-status.

**These are STAGE 4 tests** (per the plan: stage 4 is where the heavy
work happens — 7 state machine + hooks + verification all live here).

**Dependencies**:
- `mock_adr` — minimal ADR.md fixture (§2.4 MG table, §5 API, §7 pseudocode)
- `mock_sprint_status` — minimal sprint-status.md fixture
- `tmp_sprint` — tmp_path simulating `.claude/iterations/sprint-latest/`

See tests/TEST-MEFAN.md for the test flow documentation.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest


pytestmark = pytest.mark.stage4


# 7-state lifecycle, in order
SEVEN_STATES = (
    "Dev",
    "SelfCheck",
    "CodeReview",
    "QATestCoding",
    "TestCodeReview",
    "Testing",
    "Close",
)


def _write_sprint_status(sprint_dir: Path, mg_id: str, state: str) -> None:
    """Write a minimal sprint-status.md with the given MG in the given state."""
    content = (
        "# Sprint Status\n\n"
        "## 2. 状态机\n\n"
        f"| {mg_id} | {state} |\n"
    )
    (sprint_dir / "sprint-status.md").write_text(content, encoding="utf-8")


@pytest.fixture
def state_machine_hook(hooks_dir: Path) -> Path:
    """Path to the state machine hook script."""
    sm = hooks_dir / "check-state-machine.sh"
    if not sm.exists():
        pytest.skip(f"check-state-machine.sh missing from {hooks_dir}")
    return sm


@pytest.mark.parametrize("state", SEVEN_STATES)
def test_state_machine_accepts_each_of_7_states(
    state_machine_hook: Path, tmp_sprint: Path, state: str
):
    """The state machine must accept every one of the 7 valid states.

    Writes a minimal sprint-status.md with the MG in the given state,
    then calls check-state-machine.sh with the expected state, and
    asserts the hook returns exit 0.
    """
    mg_id = "MG-001"
    _write_sprint_status(tmp_sprint, mg_id, state)

    # Run from a directory such that $ROOT resolves to the tmp_sprint's
    # parent of .claude/iterations/sprint-latest/. We symlink the
    # needed structure to make the hook see sprint-status.md.
    import os
    fake_root = tmp_sprint.parent
    claude_dir = fake_root / ".claude"
    claude_dir.mkdir(exist_ok=True)
    iterations_dir = claude_dir / "iterations"
    iterations_dir.mkdir(exist_ok=True)
    # Move our tmp_sprint (which IS tmp_path) under iterations/sprint-latest
    target = iterations_dir / "sprint-latest"
    if target.exists():
        import shutil
        shutil.rmtree(target)
    # tmp_sprint is a fresh empty dir with reviews/, task-summary/ subdirs
    # we just need it to BE at iterations/sprint-latest
    tmp_sprint.rename(target)
    sprint = target
    # write the status file (it was created in tmp_sprint before rename)
    (sprint / "sprint-status.md").write_text(
        f"# Sprint Status\n\n## 2. 状态机\n\n| {mg_id} | {state} |\n",
        encoding="utf-8",
    )

    # The script hardcodes ROOT=/mnt/d/pycharmprojects/Mefan. We can't
    # easily override that without modifying the script. Instead, we
    # use a different approach: skip this e2e test if ROOT doesn't match.
    # See test_state_machine_static_check below for the static equivalent.
    script_text = state_machine_hook.read_text(encoding="utf-8")
    if 'ROOT="/mnt/d/pycharmprojects/Mefan"' not in script_text:
        pytest.skip("state machine hook does not use the expected ROOT hardcode")

    # To make this test work without modifying the script, we create a
    # symbolic link: /mnt/d/pycharmprojects/Mefan/.claude/iterations/sprint-latest
    # pointing to our tmp_path.
    real_root = Path("/mnt/d/pycharmprojects/Mefan")
    real_iter = real_root / ".claude" / "iterations" / "sprint-latest"
    backup = None
    if real_iter.exists() and not real_iter.is_symlink():
        backup = real_root / ".claude" / "iterations" / "sprint-latest.backup-test"
        if backup.exists():
            import shutil
            shutil.rmtree(backup)
        real_iter.rename(backup)
    elif real_iter.is_symlink():
        real_iter.unlink()
    try:
        real_iter.symlink_to(sprint, target_is_directory=True)
        result = subprocess.run(
            ["bash", str(state_machine_hook), mg_id, state],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0, (
            f"State machine rejected valid state {state}.\n"
            f"  rc={result.returncode}\n"
            f"  stdout: {result.stdout}\n"
            f"  stderr: {result.stderr}"
        )
    finally:
        if real_iter.is_symlink() or real_iter.exists():
            if real_iter.is_symlink():
                real_iter.unlink()
        if backup is not None and backup.exists():
            backup.rename(real_iter)


def test_state_machine_static_check(state_machine_hook: Path):
    """Static check: the state machine script must declare the 7 valid states.

    This is a fallback for environments where the e2e test cannot run
    (e.g. CI without write access to the mefan root).
    """
    text = state_machine_hook.read_text(encoding="utf-8")
    for state in SEVEN_STATES:
        # The script defines VALID_TRANSITIONS map; states appear as keys/values.
        assert state in text, (
            f"check-state-machine.sh does not mention state {state!r} "
            f"in its VALID_TRANSITIONS map. State machine is incomplete."
        )


def test_state_machine_rejects_invalid_state(state_machine_hook: Path, tmp_sprint: Path):
    """The state machine must reject a state not in the 7-state set."""
    mg_id = "MG-001"
    fake_root = tmp_sprint.parent
    real_root = Path("/mnt/d/pycharmprojects/Mefan")
    real_iter = real_root / ".claude" / "iterations" / "sprint-latest"
    backup = None
    if real_iter.exists() and not real_iter.is_symlink():
        backup = real_root / ".claude" / "iterations" / "sprint-latest.backup-test"
        if backup.exists():
            import shutil
            shutil.rmtree(backup)
        real_iter.rename(backup)
    elif real_iter.is_symlink():
        real_iter.unlink()
    try:
        # Set MG to a real state
        sprint = real_root / ".claude" / "iterations" / "sprint-latest"
        sprint.mkdir(parents=True, exist_ok=True)
        sprint.joinpath("sprint-status.md").write_text(
            f"# Sprint Status\n\n## 2. 状态机\n\n| {mg_id} | Dev |\n",
            encoding="utf-8",
        )
        # Ask for an invalid state
        result = subprocess.run(
            ["bash", str(state_machine_hook), mg_id, "TotallyNotAState"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode != 0, (
            f"State machine should reject 'TotallyNotAState' but returned rc=0.\n"
            f"  stdout: {result.stdout}\n"
            f"  stderr: {result.stderr}"
        )
    finally:
        if backup is not None and backup.exists():
            if real_iter.exists():
                import shutil
                shutil.rmtree(real_iter)
            backup.rename(real_iter)
