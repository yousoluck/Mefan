"""Tests for skill declaration vs invocation consistency.

These tests parse each agent file's:
1. `## 需要的技能` section → list of declared skills
2. Operation steps → list of `Skill(skill="...")` invocations

Then assert the 3 known declared-only skills have been wired in
their planned locations (per superpowers-integration.md §H):
- pm-stage4.requesting-code-review → 下沉到 reviewer subagent (mf-upgrade:04-implement.md)
- qa-stage5.systematic-debugging → qa-stage5.md 自身接线
- pm-stage6.writing-skills → pm-stage6.md 自身接线

Stage 0-3 声明但未调用的 skill 保持 ⚠ 状态（不强制接线，见集成文档）。
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest


# Match `superpowers:<skill-name>` (the Skill tool namespace form)
SKILL_RE = re.compile(r"superpowers:([a-zA-Z0-9_-]+)")

# Match explicit Skill tool invocations. Accepts both forms used in the
# codebase today:
#   1. Proper: `Skill(skill: "superpowers:xxx")` or `Skill(skill="superpowers:xxx")`
#   2. Markdown-friendly: `` 调用 `Skill` 工具，`skill: "superpowers:xxx"` ``
#   3. Playbook-style: `> **Skill tool invocation**: \`skill="superpowers:xxx"\``
# The regex is intentionally permissive to accept all real-world patterns.
SKILL_CALL_RE = re.compile(
    r"[`\"']?Skill[`\"']?\s*"
    r"(?:\(\s*|\u5de5\u5177\s*[, \uFF0C]?\s*|\u5de5\u5177\u4e0e\u6db5\u4e49\s*[:=]?\s*)?"
    r"[`\"']?skill\s*[:=]\s*[\"']superpowers:([a-zA-Z0-9_-]+)[\"']",
    re.IGNORECASE,
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _extract_declared_skills(agent_text: str) -> set[str]:
    """Extract superpowers skill names declared in `## 需要的技能` section.

    Parses lines like:
      - `superpowers:brainstorming`  # 外部技能（...）
      - `superpowers:test-driven-development`
    """
    # Find the `## 需要的技能` section
    m = re.search(
        r"##\s*需要的技能\s*\n(.*?)(?=\n##\s|\Z)",
        agent_text,
        re.DOTALL,
    )
    if not m:
        return set()
    section = m.group(1)
    # Each line like `- `superpowers:foo`  # comment`
    return set(SKILL_RE.findall(section))


def _extract_invoked_skills(agent_text: str) -> set[str]:
    """Extract superpowers skill names actually invoked via Skill tool."""
    return set(SKILL_CALL_RE.findall(agent_text))


# ---------- Test 1: 3 known declared-only skills are now wired ----------


# Each entry: (agent_file, skill_name, expected_in_path)
WIRED_SKILLS = [
    # P3: pm-stage4.requesting-code-review → 下沉到 reviewer subagent playbook
    (
        "mf-upgrade:04-implement.md",
        "requesting-code-review",
        Path(__file__).resolve().parent.parent
        / ".claude" / "commands" / "mf-upgrade:04-implement.md",
    ),
    # Q1: qa-stage5.systematic-debugging → qa-stage5 自身接线
    (
        "qa-stage5.md",
        "systematic-debugging",
        Path(__file__).resolve().parent.parent
        / ".claude" / "agents" / "qa-stage5.md",
    ),
    # W1: pm-stage6.writing-skills → pm-stage6 自身接线
    (
        "pm-stage6.md",
        "writing-skills",
        Path(__file__).resolve().parent.parent
        / ".claude" / "agents" / "pm-stage6.md",
    ),
]


@pytest.mark.parametrize(
    "label,skill_name,expected_path",
    [(label, skill, path) for label, skill, path in WIRED_SKILLS],
    ids=[label for label, _, _ in WIRED_SKILLS],
)
def test_wired_skill_is_actually_invoked(
    label: str, skill_name: str, expected_path: Path
):
    """Each known declared-only skill must be invoked via Skill tool in its planned location.

    Per superpowers-integration.md §H wiring plan:
    - P3: pm-stage4.requesting-code-review → mf-upgrade:04-implement.md (reviewer subagent)
    - Q1: qa-stage5.systematic-debugging → qa-stage5.md (门禁裁定前)
    - W1: pm-stage6.writing-skills → pm-stage6.md (合并进化提案时)
    """
    assert expected_path.exists(), f"{label}: file not found: {expected_path}"
    text = _read(expected_path)
    invoked = _extract_invoked_skills(text)
    assert skill_name in invoked, (
        f"{label}: skill `{skill_name}` is declared in plan but NOT invoked in "
        f"{expected_path.name}. Expected to see `Skill(skill: \"superpowers:{skill_name}\")` "
        f"or `Skill tool invocation: skill=\"superpowers:{skill_name}\"`."
    )


# ---------- Test 2: the 2 wired agents (per plan Q1/W1) have no declared-only skills ----------


# Per superpowers-integration.md §H 接线方案：
# - P3: pm-stage4.requesting-code-review → 下沉到 mf-upgrade:04-implement.md
#       （不在 pm-stage4.md 自身接线，矩阵也不列；见 §H 注）
# - Q1: qa-stage5.systematic-debugging → qa-stage5.md 自身接线
# - W1: pm-stage6.writing-skills → pm-stage6.md 自身接线
# 注：阶段 4-6 的其他 declared-only skill 不在本次接线范围内
#     （共 20+ 项 declared-only），留待 Stage 6 重构时统一处理
#     （见 .claude/plans.md Stage 6 重构入口）
WIRED_AGENTS = ["qa-stage5.md", "pm-stage6.md"]


def test_wired_agents_have_no_declared_only_skills(agents_dir: Path):
    """The 2 wired agents (per plan Q1/W1) should have no declared-only superpowers skills.

    Note: P3 (pm-stage4.requesting-code-review) is wired in mf-upgrade:04-implement.md
    (the playbook, not pm-stage4.md itself), so pm-stage4.md is intentionally
    excluded from this check.

    For the OTHER stage 4-6 agents, declared-only is acceptable (per integration doc §H).
    They will be rewired during Stage 6 refactor.
    """
    offenders: list[tuple[str, str]] = []
    for fname in WIRED_AGENTS:
        p = agents_dir / fname
        if not p.exists():
            continue
        text = _read(p)
        declared = _extract_declared_skills(text)
        invoked = _extract_invoked_skills(text)
        declared_only = declared - invoked
        for s in sorted(declared_only):
            offenders.append((fname, s))

    assert not offenders, (
        f"The 2 wired agents ({', '.join(WIRED_AGENTS)}) have superpowers: skills "
        f"declared but NOT invoked:\n"
        + "\n".join(f"  {f}: superpowers:{s}" for f, s in offenders)
        + "\n\nFix: add a `Skill(skill: \"superpowers:<name>\")` invocation "
        "in the planned operation step."
    )
