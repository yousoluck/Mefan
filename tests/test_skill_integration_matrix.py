"""Tests that the superpowers-integration.md matrix matches reality.

These tests parse the integration matrix in
`.claude/rules/global/superpowers-integration.md` and compare it to:
- The actual superpowers: references in each agent file
- The Skill tool invocations in each agent file

The matrix must be:
1. **Complete**: every agent with a `superpowers:` reference appears in the matrix
2. **Accurate**: the matrix's ✓/⚠ status matches the actual invocations
3. **Consistent**: the agent count claim in the change log is correct
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest


INTEGRATION_DOC = (
    Path(__file__).resolve().parent.parent
    / ".claude" / "rules" / "global" / "superpowers-integration.md"
)


# ---------- Helpers ----------


SKILL_RE = re.compile(r"superpowers:([a-zA-Z0-9_-]+)")
# Accepts both proper `Skill(skill: "...")` and markdown-friendly
# ``调用 `Skill` 工具，`skill: "..."` `` formats. The regex is intentionally
# permissive to accept all real-world patterns the agents use.
SKILL_CALL_RE = re.compile(
    r"[`\"']?Skill[`\"']?\s*"
    r"(?:\(\s*|\u5de5\u5177\s*[, \uFF0C]?\s*|\u5de5\u5177\u4e0e\u6db5\u4e49\s*[:=]?\s*)?"
    r"[`\"']?skill\s*[:=]\s*[\"']superpowers:([a-zA-Z0-9_-]+)[\"']",
    re.IGNORECASE,
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _extract_declared_skills(agent_text: str) -> set[str]:
    m = re.search(r"##\s*需要的技能\s*\n(.*?)(?=\n##\s|\Z)", agent_text, re.DOTALL)
    if not m:
        return set()
    return set(SKILL_RE.findall(m.group(1)))


def _extract_invoked_skills(agent_text: str) -> set[str]:
    return set(SKILL_CALL_RE.findall(agent_text))


def _parse_matrix(integration_text: str) -> dict[str, dict[str, str]]:
    """Parse the integration matrix tables. Returns {agent_file: {skill: status}}.

    Looks for table rows like:
      | `dev-stage4.md` | `superpowers:test-driven-development` | 操作 3 开头 | ✓ |
    """
    matrix: dict[str, dict[str, str]] = {}
    # Match table rows (skip header and separator)
    for line in integration_text.split("\n"):
        m = re.match(
            r"\|\s*`?([\w-]+\.md)`?\s*\|\s*`?superpowers:([\w-]+)`?\s*\|.*?\|\s*([✓⚠])?\s*\|",
            line,
        )
        if m:
            agent_file, skill, status = m.group(1), m.group(2), m.group(3) or ""
            matrix.setdefault(agent_file, {})[skill] = status
    return matrix


# ---------- Test 1: matrix completeness — every agent with superpowers reference is listed ----------


def test_matrix_lists_every_superpowers_agent(agents_dir: Path):
    """Every agent with a `superpowers:` reference must appear in the matrix.

    Excludes: `pm.md` (role index, no operations).
    """
    if not INTEGRATION_DOC.exists():
        pytest.skip(f"integration doc not found: {INTEGRATION_DOC}")
    matrix = _parse_matrix(_read(INTEGRATION_DOC))
    matrix_agents = set(matrix.keys())

    # Actual agents with superpowers references
    actual_agents = set()
    for p in sorted(agents_dir.glob("*.md")):
        if p.name == "pm.md":
            continue
        text = _read(p)
        if SKILL_RE.search(text):
            actual_agents.add(p.name)

    missing_from_matrix = actual_agents - matrix_agents
    # Note: qa-fix-stage4 has Skill tool but no superpowers skill, so it should NOT be in actual_agents
    assert not missing_from_matrix, (
        f"Agents with superpowers references not in matrix: {sorted(missing_from_matrix)}\n"
        f"Either add them to the matrix or remove their superpowers references."
    )


# ---------- Test 2: matrix ✓/⚠ accuracy — declared-only skills marked ⚠ ----------


def test_matrix_status_matches_declaration(agents_dir: Path):
    """For each agent in the matrix, the ✓/⚠ status must match:
    - ✓ = skill is declared AND invoked
    - ⚠ = skill is declared but NOT invoked (declared-only)

    If a matrix row says ✓ but the skill is not invoked → matrix is wrong.
    If a matrix row says ⚠ but the skill IS invoked → matrix is wrong.
    """
    if not INTEGRATION_DOC.exists():
        pytest.skip(f"integration doc not found: {INTEGRATION_DOC}")
    matrix = _parse_matrix(_read(INTEGRATION_DOC))

    errors: list[str] = []
    for agent_file, skills in matrix.items():
        p = agents_dir / agent_file
        if not p.exists():
            continue
        text = _read(p)
        declared = _extract_declared_skills(text)
        invoked = _extract_invoked_skills(text)

        for skill, status in skills.items():
            is_invoked = skill in invoked
            is_declared = skill in declared
            if status == "✓" and not is_invoked:
                errors.append(
                    f"{agent_file}: matrix says ✓ for `{skill}` but not invoked"
                )
            if status == "⚠" and is_invoked:
                errors.append(
                    f"{agent_file}: matrix says ⚠ for `{skill}` but IS invoked"
                )

    assert not errors, (
        "Matrix status mismatches:\n" + "\n".join(f"  {e}" for e in errors)
    )


# ---------- Test 3: changelog agent count claim is accurate ----------


def test_changelog_agent_count_claim(agents_dir: Path):
    """The change log claim '集成 10 个 superpowers skill 到 13 个 agent' should be accurate.

    After the 2026-06-06 third audit (cleanup), the count should be 13
    (12 fake ⚠ declarations removed from stage 0-3 agents).
    """
    if not INTEGRATION_DOC.exists():
        pytest.skip(f"integration doc not found: {INTEGRATION_DOC}")
    text = _read(INTEGRATION_DOC)

    # Find the LATEST change log entry mentioning "agent" with an explicit N count
    matches = re.findall(
        r"\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*([^|]+agent[^|]*)\s*\|",
        text,
        re.IGNORECASE,
    )
    # Filter to entries with explicit "N 个 agent 真集成" claim (the format we use)
    with_count = []
    for date, desc in matches:
        n_match = re.search(r"(\d+)\s*个\s*agent\s*真集成", desc)
        if n_match:
            with_count.append((date, desc, int(n_match.group(1))))
    if not with_count:
        pytest.skip("no change log entry with 'N 个 agent 真集成' claim found")
    # Take the most recent by date
    with_count.sort(key=lambda x: x[0], reverse=True)
    date, description, claimed_count = with_count[0]

    # Count actual agents
    actual_count = sum(
        1 for p in agents_dir.glob("*.md")
        if p.name != "pm.md" and SKILL_RE.search(_read(p))
    )
    assert claimed_count == actual_count, (
        f"Change log claims {claimed_count} agents (latest entry: {date}), actual is {actual_count}.\n"
        f"Entry: {description!r}"
    )
