"""Tests for agent YAML frontmatter integrity.

These tests assert that the mefan agent files:
- Have a valid YAML frontmatter block
- Declare a known list of tools
- For stage 4/5/6 agents, MUST include the `Skill` tool (so that they can
  invoke superpowers skills at runtime).

Background: per the superpowers integration plan, every stage 4/5/6 agent
needs the `Skill` tool so that the Claude Code plugin runtime can dispatch
to installed skills like `superpowers:test-driven-development`.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml


# Tools that we know are valid. Any other tool name in frontmatter is
# a typo (or an attempt to use a forbidden tool) and must fail the test.
KNOWN_TOOLS = {
    "Read", "Write", "Edit", "Bash", "Grep", "Glob",
    "TaskCreate", "TaskUpdate", "TaskList", "TaskGet",
    "WebFetch", "WebSearch", "Skill", "NotebookEdit",
    "Task", "TodoWrite", "TaskOutput", "AskUserQuestion", "EnterPlanMode",
    "ExitPlanMode", "EnterWorktree", "ExitWorktree",
    "CronCreate", "CronDelete", "CronList",
    "BashOutput", "KillShell",
    "mcp__context7__resolve-library-id", "mcp__context7__query-docs",
    "mcp__memory__create_entities", "mcp__memory__create_relations",
    "mcp__memory__add_observations", "mcp__memory__delete_entities",
    "mcp__memory__delete_observations", "mcp__memory__delete_relations",
    "mcp__memory__read_graph", "mcp__memory__search_nodes", "mcp__memory__open_nodes",
    "mcp__playwright__browser_close", "mcp__playwright__browser_resize",
    "mcp__playwright__browser_console_messages", "mcp__playwright__browser_handle_dialog",
    "mcp__playwright__browser_evaluate", "mcp__playwright__browser_file_upload",
    "mcp__playwright__browser_drop", "mcp__playwright__browser_fill_form",
    "mcp__playwright__browser_press_key", "mcp__playwright__browser_type",
    "mcp__playwright__browser_navigate", "mcp__playwright__browser_navigate_back",
    "mcp__playwright__browser_network_requests", "mcp__playwright__browser_network_request",
    "mcp__playwright__browser_run_code_unsafe", "mcp__playwright__browser_take_screenshot",
    "mcp__playwright__browser_snapshot", "mcp__playwright__browser_click",
    "mcp__playwright__browser_drag", "mcp__playwright__browser_hover",
    "mcp__playwright__browser_select_option", "mcp__playwright__browser_tabs",
    "mcp__playwright__browser_wait_for",
}

# Agents that, per the integration plan, MUST have `Skill` in their tools.
# (Stage 4/5/6 = the "execution" stages of the framework.)
STAGE45_AGENTS_REQUIRING_SKILL = {
    # Stage 4 — implementation
    "dev-stage4",
    "dev-fix-stage4",
    "architect-stage4",
    "qa-stage4",
    "qa-fix-stage4",
    "pm-stage4",
    # Stage 5 — quality gate
    "qa-stage5",
    "pm-stage5",
    "dev-stage5",
    "guardian-stage5",
    # Stage 6 — retrospective & evolution
    "coach-stage6",
    "pm-stage6",
    "guardian-stage6",
}

# Stage 0/1/2/3 agents: Skill is recommended but not strictly required
# (the plan lists them as P2 priority).
STAGE0123_AGENTS_RECOMMENDING_SKILL = {
    "pm-stage0", "analyst-stage0", "architect-stage0",
    "ba-stage1", "pm-stage1",
    "architect-stage2", "qa-stage2", "pm-audit-stage2",
    "analyst-stage3", "pm-stage3",
}


FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def _parse_frontmatter(path: Path) -> dict:
    """Parse the YAML frontmatter at the top of a markdown file.

    Returns an empty dict if no frontmatter is present.
    """
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    return yaml.safe_load(m.group(1)) or {}


def _iter_agent_files(agents_dir: Path):
    """Yield (path, name) for every .md agent file."""
    if not agents_dir.exists():
        return
    for p in sorted(agents_dir.glob("*.md")):
        yield p, p.stem


# ---------- Basic structural tests (must always pass) ----------


@pytest.mark.parametrize("agent_file,agent_name", list(_iter_agent_files(Path(__file__).resolve().parent.parent / ".claude" / "agents")))
def test_agent_has_valid_yaml_frontmatter(agent_file: Path, agent_name: str):
    """Every agent file must have a valid YAML frontmatter block."""
    if not agent_file.exists():
        pytest.skip(f"agents dir missing: {agent_file}")
    fm = _parse_frontmatter(agent_file)
    # `name` is the canonical identifier
    assert "name" in fm, f"{agent_file.name} has no `name` in frontmatter"
    # `description` is required for agent discovery
    assert "description" in fm, f"{agent_file.name} has no `description` in frontmatter"


@pytest.mark.parametrize("agent_file,agent_name", list(_iter_agent_files(Path(__file__).resolve().parent.parent / ".claude" / "agents")))
def test_agent_tools_are_known(agent_file: Path, agent_name: str):
    """Every tool declared in frontmatter must be a known tool name.

    Catches typos and unknown tools that would silently disable an agent.
    """
    if not agent_file.exists():
        pytest.skip(f"agents dir missing: {agent_file}")
    fm = _parse_frontmatter(agent_file)
    tools = fm.get("tools", [])
    if isinstance(tools, str):
        tools = [t.strip() for t in tools.split(",") if t.strip()]
    assert isinstance(tools, list), f"{agent_file.name}: tools must be a list"
    unknown = set(tools) - KNOWN_TOOLS
    assert not unknown, (
        f"{agent_file.name}: unknown tool(s) {sorted(unknown)}. "
        f"Add them to KNOWN_TOOLS if intentional."
    )


# ---------- Stage 4/5/6 integration tests (RED → GREEN) ----------


@pytest.mark.parametrize("agent_name", sorted(STAGE45_AGENTS_REQUIRING_SKILL))
def test_stage45_agent_has_skill_tool(agents_dir: Path, agent_name: str):
    """Stage 4/5/6 agents MUST have `Skill` in their `tools` list.

    This is the primary Layer 1 deliverable: the `Skill` tool must be
    present so that the agent can dispatch to superpowers skills at
    runtime. Without it, `@superpowers:xxx` references in agent bodies
    are inert comments.
    """
    agent_file = agents_dir / f"{agent_name}.md"
    if not agent_file.exists():
        pytest.skip(f"agent file missing: {agent_file}")
    fm = _parse_frontmatter(agent_file)
    tools = fm.get("tools", [])
    if isinstance(tools, str):
        tools = [t.strip() for t in tools.split(",") if t.strip()]
    assert "Skill" in tools, (
        f"{agent_name}.md frontmatter is missing `Skill` in tools. "
        f"Required: [..., 'Skill']. Current: {tools}"
    )


# ---------- Stage 0-3 advisory tests ----------


@pytest.mark.parametrize("agent_name", sorted(STAGE0123_AGENTS_RECOMMENDING_SKILL))
def test_stage0123_agent_has_skill_tool_recommended(agents_dir: Path, agent_name: str):
    """Stage 0-3 agents are RECOMMENDED (P2) to have `Skill` in tools.

    This is a soft test: it produces a warning via `pytest.warns` rather
    than a hard fail. It exists to make P2 missing-Skill agents visible
    during code review.
    """
    agent_file = agents_dir / f"{agent_name}.md"
    if not agent_file.exists():
        pytest.skip(f"agent file missing: {agent_file}")
    fm = _parse_frontmatter(agent_file)
    tools = fm.get("tools", [])
    if isinstance(tools, str):
        tools = [t.strip() for t in tools.split(",") if t.strip()]
    if "Skill" not in tools:
        import warnings
        warnings.warn(
            f"{agent_name}.md is missing `Skill` in tools (P2 priority).",
            stacklevel=2,
        )
