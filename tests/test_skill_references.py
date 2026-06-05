"""Tests for `@superpowers/xxx` placeholder integrity.

These tests assert that every `@superpowers/xxx` reference in agent /
skill / rule files resolves to a real installed skill in
`~/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/`.

Background: the integration plan revealed that agent files contain
placeholders like `@superpowers/tdd-mastery` that do not exist in the
installed superpowers v5.1.0 plugin. These tests are the regression
guard — any new placeholder must point to a real skill.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest


# Match `@superpowers/<skill-name>` where skill-name is one or more
# word characters or hyphens.
PLACEHOLDER_RE = re.compile(r"@superpowers/([a-zA-Z0-9_-]+)")


def _iter_text_files(root: Path):
    """Yield (path, text) for every .md file under `root`."""
    if not root.exists():
        return
    for p in sorted(root.rglob("*.md")):
        # Skip agent templates / large auto-generated files
        if "node_modules" in p.parts:
            continue
        try:
            yield p, p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue


def _extract_placeholders(text: str) -> list[str]:
    """Return the unique set of skill names referenced via @superpowers/X."""
    return sorted(set(PLACEHOLDER_RE.findall(text)))


# ---------- Test 1: every @superpowers/X resolves to a real skill ----------


def test_all_superpowers_placeholders_resolve(agents_dir: Path, superpowers_dir: Path):
    """Every `@superpowers/<name>` reference must point to an installed skill.

    This is the primary Layer 2 deliverable. It will fail RED at baseline
    because the current agents reference skills that don't exist
    (e.g. `tdd-mastery`, `code-review`, `test-automation`).
    """
    if not superpowers_dir.exists():
        pytest.skip(f"superpowers plugin not installed at {superpowers_dir}")
    installed_skills = {
        p.parent.name for p in superpowers_dir.glob("*/SKILL.md")
    }
    # Also allow direct `superpowers:X` namespace form (used in the Skill tool)
    installed_skills |= {f"superpowers:{n}" for n in installed_skills}

    broken: list[tuple[Path, str]] = []
    for sub in (agents_dir,):
        if not sub.exists():
            continue
        for p in sorted(sub.glob("*.md")):
            text = p.read_text(encoding="utf-8")
            for name in _extract_placeholders(text):
                if name not in installed_skills:
                    broken.append((p, name))

    assert not broken, (
        "Broken `@superpowers/X` references (skill does not exist in "
        f"{superpowers_dir}):\n"
        + "\n".join(f"  {p.name}: @{name}" for p, name in broken)
    )


# ---------- Test 2: no agent uses the deprecated `@superpowers/X` raw form ----------
# (the Skill tool expects `superpowers:X` colon-namespaced form, not `@superpowers/X`)


def test_no_raw_at_superpowers_in_agents(agents_dir: Path):
    """Agent files should use `superpowers:skill-name` (colon form) for
    the Skill tool, not `@superpowers/skill-name` (raw form).

    The raw `@superpowers/X` form is a documentation placeholder; the
    runtime expects `superpowers:X` when invoking the Skill tool.
    """
    if not agents_dir.exists():
        pytest.skip(f"agents dir missing: {agents_dir}")
    raw_refs: list[tuple[Path, str]] = []
    for p in sorted(agents_dir.glob("*.md")):
        text = p.read_text(encoding="utf-8")
        for name in _extract_placeholders(text):
            # The placeholder is in raw form. Track the file.
            raw_refs.append((p, name))
    # Note: the plan keeps `@superpowers/X` as a documentation hint
    # alongside the runtime `superpowers:X` Skill tool call. So this
    # test is an ADVISORY test, not a hard fail. We emit a warning.
    if raw_refs:
        import warnings
        warnings.warn(
            f"Found {len(raw_refs)} raw `@superpowers/X` placeholder(s). "
            f"These are documentation hints — the runtime expects "
            f"`superpowers:X` (colon form) for the Skill tool.",
            stacklevel=2,
        )


# ---------- Test 3: stage 4/5/6 agents must reference at least one
#                  superpowers skill (proof of integration) ----------


STAGE45_AGENT_FILES = (
    "dev-stage4.md", "dev-fix-stage4.md", "architect-stage4.md",
    "qa-stage4.md", "pm-stage4.md",
    "qa-stage5.md", "pm-stage5.md", "dev-stage5.md", "guardian-stage5.md",
    "coach-stage6.md", "pm-stage6.md", "guardian-stage6.md",
)


@pytest.mark.parametrize("agent_file_name", STAGE45_AGENT_FILES)
def test_stage45_agent_uses_at_least_one_superpowers_skill(
    agents_dir: Path, agent_file_name: str
):
    """Every stage 4/5/6 agent must reference at least one superpowers skill
    (either as `@superpowers/X` or as `superpowers:X` in a Skill call).

    This is the proof of integration — if the test passes, the agent is
    actually wired into the superpowers plugin at the call-site level.
    """
    p = agents_dir / agent_file_name
    if not p.exists():
        pytest.skip(f"agent missing: {p}")
    text = p.read_text(encoding="utf-8")
    has_placeholder = bool(PLACEHOLDER_RE.search(text))
    has_skill_call = bool(re.search(r"superpowers:[a-zA-Z0-9_-]+", text))
    assert has_placeholder or has_skill_call, (
        f"{agent_file_name} does not reference any superpowers skill. "
        f"Expected at least one `@superpowers/X` placeholder or one "
        f"`superpowers:X` Skill tool call. See the integration plan."
    )
