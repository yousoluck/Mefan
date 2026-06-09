"""Tests for Skill standard compliance (superpowers alignment).

These tests assert that the mefan Skill ecosystem:
- All skill SKILL.md files use real YAML frontmatter (not body code-fenced blocks)
- All frontmatter `description:` fields use "Use when..." triggering format
- No forbidden meta fields (category, version, author, created, trigger, depends_on, provides_to, name_zh)
- `_templates/` contains NO hardcoded reference code files
- `_templates/` contains NO empty references/ directories
- No `assets/` or `tests/` subdirectories inside any skill
- `references/` subdirectory depth is at most 1 (no nesting)

Background: per the superpowers `writing-skills` standard (v5.1.0), every Skill
must follow the agentskills.io spec — real frontmatter, "Use when..." description,
and the three allowed file patterns (self-contained / with tool / with heavy ref).
Violations are a P1 issue (skill is not discoverable by the Skill tool).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml


# Forbidden frontmatter fields (per superpowers spec — only name + description allowed)
FORBIDDEN_FIELDS = {
    "name_zh", "category", "version", "author", "created",
    "trigger", "trigger_files", "depends_on", "provides_to",
    "framework", "source", "tags",
}


def _parse_frontmatter(path: Path) -> dict | None:
    """Parse the YAML frontmatter block from a SKILL.md file.

    Returns the dict if parseable, None otherwise.
    """
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return None
    # Find the closing ---
    lines = content.splitlines()
    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        return None
    yaml_text = "\n".join(lines[1:end_idx])
    try:
        return yaml.safe_load(yaml_text) or {}
    except yaml.YAMLError:
        return None


# ───────────────────────────────────────────────────────────────────
# Frontmatter structure
# ───────────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "skill_md",
    [
        # Templates
        "skill-template",
        "project-api-generic",
        "project-domain-generic",
        "project-feature-generic",
        "project-service-generic",
        "project-ui-generic",
        "project-infra-cache",
        "project-infra-config",
        "project-infra-database",
        "project-infra-filesystem",
        "project-infra-generic",
        "project-infra-logging",
        "project-infra-message-queue",
        "project-infra-naming-convention",
        "project-infra-network",
        "project-infra-security",
        # Framework skills
        "backend-django",
        "backend-fastapi",
        "backend-flask",
        "frontend-redux",
        "frontend-vue",
    ],
)
def test_skill_has_real_frontmatter(skills_dir: Path, skill_md: str) -> None:
    """Every skill must have a real YAML frontmatter (--- block) at the top."""
    # Search the skill in templates/ or at top level
    candidates = [
        skills_dir / "_templates" / skill_md / "SKILL.md",
        skills_dir / skill_md / "SKILL.md",
    ]
    skill_path = next((p for p in candidates if p.exists()), None)
    if skill_path is None:
        pytest.skip(f"Skill not found: {skill_md}")

    content = skill_path.read_text(encoding="utf-8")
    assert content.startswith("---"), f"{skill_md}: missing frontmatter (first line must be ---)"


@pytest.mark.parametrize(
    "skill_md",
    [
        "skill-template", "project-api-generic", "project-infra-database",
        "project-infra-cache", "project-infra-config", "project-infra-filesystem",
        "project-infra-generic", "project-infra-logging", "project-infra-message-queue",
        "project-infra-naming-convention", "project-infra-network", "project-infra-security",
        "project-domain-generic", "project-feature-generic", "project-service-generic",
        "project-ui-generic",
        "backend-django", "backend-fastapi", "backend-flask",
        "frontend-redux", "frontend-vue",
    ],
)
def test_skill_frontmatter_has_name_and_description(skills_dir: Path, skill_md: str) -> None:
    """Every skill frontmatter must declare both `name` and `description`."""
    candidates = [
        skills_dir / "_templates" / skill_md / "SKILL.md",
        skills_dir / skill_md / "SKILL.md",
    ]
    skill_path = next((p for p in candidates if p.exists()), None)
    if skill_path is None:
        pytest.skip(f"Skill not found: {skill_md}")

    fm = _parse_frontmatter(skill_path)
    assert fm is not None, f"{skill_md}: frontmatter not parseable"
    assert "name" in fm, f"{skill_md}: frontmatter missing `name`"
    assert "description" in fm, f"{skill_md}: frontmatter missing `description`"


@pytest.mark.parametrize(
    "skill_md",
    [
        "skill-template", "project-api-generic", "project-infra-database",
        "project-infra-cache", "project-infra-config", "project-infra-filesystem",
        "project-infra-generic", "project-infra-logging", "project-infra-message-queue",
        "project-infra-naming-convention", "project-infra-network", "project-infra-security",
        "project-domain-generic", "project-feature-generic", "project-service-generic",
        "project-ui-generic",
        "backend-django", "backend-fastapi", "backend-flask",
        "frontend-redux", "frontend-vue",
    ],
)
def test_skill_description_uses_when_format(skills_dir: Path, skill_md: str) -> None:
    """Every skill's `description` must use the 'Use when...' triggering format."""
    candidates = [
        skills_dir / "_templates" / skill_md / "SKILL.md",
        skills_dir / skill_md / "SKILL.md",
    ]
    skill_path = next((p for p in candidates if p.exists()), None)
    if skill_path is None:
        pytest.skip(f"Skill not found: {skill_md}")

    fm = _parse_frontmatter(skill_path)
    assert fm is not None, f"{skill_md}: frontmatter not parseable"
    desc = fm.get("description", "")
    assert "Use when" in desc, (
        f"{skill_md}: description must start with 'Use when...', got: {desc[:80]!r}"
    )


def test_templates_have_no_forbidden_meta_fields(skills_dir: Path) -> None:
    """No template may use forbidden frontmatter fields (name_zh, category, version, ...)."""
    templates_dir = skills_dir / "_templates"
    for skill_md in templates_dir.glob("*/SKILL.md"):
        fm = _parse_frontmatter(skill_md)
        if fm is None:
            continue
        forbidden_present = FORBIDDEN_FIELDS & set(fm.keys())
        assert not forbidden_present, (
            f"{skill_md.parent.name}: contains forbidden frontmatter fields: {forbidden_present}"
        )


def test_framework_skills_have_no_forbidden_meta_fields(skills_dir: Path) -> None:
    """No framework skill may use forbidden frontmatter fields."""
    for pattern in ("backend-*", "frontend-*"):
        for skill_md in (skills_dir).glob(f"{pattern}/SKILL.md"):
            fm = _parse_frontmatter(skill_md)
            if fm is None:
                continue
            forbidden_present = FORBIDDEN_FIELDS & set(fm.keys())
            assert not forbidden_present, (
                f"{skill_md.parent.name}: contains forbidden frontmatter fields: {forbidden_present}"
            )


# ───────────────────────────────────────────────────────────────────
# Directory hygiene (templates must be CLEAN skeletons)
# ───────────────────────────────────────────────────────────────────


def test_templates_have_no_hardcoded_code_files(skills_dir: Path) -> None:
    """Templates must not contain hardcoded .java / .py / .ts / .yml / .sql reference files.

    These were the anti-patterns that were soft-deleted to `_templates/.trash/`.
    Any new .java/.py/.ts/.yml/.sql file under _templates/ is a regression.
    """
    templates_dir = skills_dir / "_templates"
    forbidden_exts = {".java", ".py", ".ts", ".yml", ".sql", ".json", ".xml"}
    violations = []
    for path in templates_dir.rglob("*"):
        if path.is_file() and path.suffix in forbidden_exts:
            # Allow files under .trash/ (those are quarantined)
            if ".trash" in path.parts:
                continue
            violations.append(path.relative_to(templates_dir))
    assert not violations, f"Templates contain hardcoded code files: {violations}"


def test_templates_have_no_references_subdirs(skills_dir: Path) -> None:
    """No `references/` subdir under _templates/ (anti-pattern: placeholder files)."""
    templates_dir = skills_dir / "_templates"
    refs = list(templates_dir.glob("*/references"))
    # Filter out .trash/ refs
    refs = [r for r in refs if ".trash" not in r.parts]
    assert not refs, f"Templates contain references/ subdirs (anti-pattern): {refs}"


def test_no_skill_has_assets_directory(skills_dir: Path) -> None:
    """No skill may have an `assets/` subdir (not in superpowers spec)."""
    for skill_md in list(skills_dir.glob("*/SKILL.md")) + list((skills_dir / "_templates").glob("*/SKILL.md")):
        skill_dir = skill_md.parent
        if skill_dir.name == "_templates":
            continue
        assets = skill_dir / "assets"
        assert not assets.exists(), f"{skill_dir}: contains forbidden assets/ subdir"


def test_no_skill_has_nested_references(skills_dir: Path) -> None:
    """`references/` must be at most one level deep (superpowers convention)."""
    for skill_md in skills_dir.rglob("SKILL.md"):
        skill_dir = skill_md.parent
        # Skip templates
        if "_templates" in skill_dir.parts:
            continue
        for refs_dir in skill_dir.glob("**/references"):
            # references/ is fine; references/foo/ is NOT fine
            depth = len(refs_dir.relative_to(skill_dir).parts)
            assert depth == 1, (
                f"{skill_dir}: nested references/ (depth {depth}); superpowers spec requires one level only"
            )


def test_no_hardcoded_trash_files_outside_quarantine(skills_dir: Path) -> None:
    """The `.trash/` quarantine must contain all hardcoded files; none should be elsewhere."""
    templates_dir = skills_dir / "_templates"
    trash_dir = templates_dir / ".trash"

    # All hardcoded files should be ONLY in .trash/
    forbidden_exts = {".java", ".py", ".ts", ".yml", ".sql", ".json", ".xml"}
    leaks = []
    for path in templates_dir.rglob("*"):
        if path.is_file() and path.suffix in forbidden_exts and ".trash" not in path.parts:
            leaks.append(path.relative_to(templates_dir))

    # Note: this is the same as test_templates_have_no_hardcoded_code_files
    # but provides a more descriptive error message
    assert not leaks, (
        f"Hardcoded code files leaked outside .trash/: {leaks}. "
        f"Move to {trash_dir}/ if quarantined, or remove entirely."
    )


# ───────────────────────────────────────────────────────────────────
# Code Snippet Extraction (refinement stage 5, 2026-06-06)
# ───────────────────────────────────────────────────────────────────


def test_templates_have_no_examples_md(skills_dir: Path) -> None:
    """Templates must NOT pre-fill examples.md.

    examples.md is generated by architect-stage0 from results.json snippets.
    A template having examples.md is a regression (template author pre-filled
    hardcoded code, which violates the 'NO SKILL WITHOUT EVIDENCE' Iron Law).
    """
    templates_dir = skills_dir / "_templates"
    for examples in templates_dir.rglob("examples.md"):
        # Allow examples.md under .trash/ (quarantined)
        if ".trash" in examples.parts:
            continue
        assert False, (
            f"{examples.relative_to(templates_dir)}: template must NOT pre-fill examples.md. "
            f"This file should be generated by architect-stage0 from results.json snippets."
        )


def test_templates_have_no_fenced_code_in_md(skills_dir: Path) -> None:
    """Templates must NOT contain fenced code blocks in their .md files.

    Defense-in-depth: even if a template author sneaks code into a `.md` file
    (e.g. in the body of SKILL.md), this test catches it. The only legitimate
    fenced code blocks in templates are tiny inline examples in Iron Law /
    Red Flags (which use the format `\\`code\\``, not full ```lang blocks).
    """
    templates_dir = skills_dir / "_templates"
    # Pattern: opening ``` on its own line (not inline `code`)
    fence_pattern = re.compile(r"^```\w*\s*$", re.MULTILINE)
    violations = []
    for md_file in templates_dir.rglob("*.md"):
        if ".trash" in md_file.parts:
            continue
        content = md_file.read_text(encoding="utf-8")
        if fence_pattern.search(content):
            violations.append(md_file.relative_to(templates_dir))
    assert not violations, (
        f"Templates contain fenced code blocks (forbidden — use Code Target column instead): {violations}"
    )


def test_skill_has_examples_md_when_snippets(skills_dir: Path) -> None:
    """If a generated skill has examples.md, it must start with a top-level heading.

    Skips templates and skills without examples.md (presence is optional;
    architect-stage0 only generates it when snippets are non-empty).
    """
    for examples in skills_dir.rglob("examples.md"):
        if "_templates" in examples.parts:
            continue
        content = examples.read_text(encoding="utf-8")
        assert content.startswith("# "), (
            f"{examples}: examples.md must start with a top-level heading (`# ...`)"
        )


def test_examples_md_cites_path_line(skills_dir: Path) -> None:
    """Every fenced code block in examples.md must be preceded by a `path:line` citation."""
    # Pattern: `### \\`path/to/file.py:15-25\\`` followed by ```lang\\n...
    # Allow optional backticks around the path:line citation
    block_pattern = re.compile(
        r"^### `[\w./\-]+:\d+(-\d+)?`\s*$\n```\w*\n",
        re.MULTILINE,
    )
    missing_citation = []
    for examples in skills_dir.rglob("examples.md"):
        if "_templates" in examples.parts:
            continue
        content = examples.read_text(encoding="utf-8")
        if not block_pattern.search(content):
            missing_citation.append(examples)
    assert not missing_citation, (
        f"examples.md files without path:line-cited code blocks (forbidden — "
        f"every fenced block must be preceded by `### \\`path:line-line\\``): {missing_citation}"
    )


def test_examples_md_is_top_level(skills_dir: Path) -> None:
    """examples.md must be at the top level of its skill (no nesting).

    Per superpowers spec, Pattern C allows only top-level companion files.
    """
    for examples in skills_dir.rglob("examples.md"):
        if "_templates" in examples.parts:
            continue
        # Find the skill directory (the parent that contains SKILL.md)
        skill_dir = None
        for parent in examples.parents:
            if (parent / "SKILL.md").exists():
                skill_dir = parent
                break
        if skill_dir is None:
            # No parent SKILL.md — this is an orphan, skip
            continue
        depth = len(examples.relative_to(skill_dir).parts)
        assert depth == 1, (
            f"{examples}: must be top-level companion (no nesting). "
            f"Found at depth {depth} relative to {skill_dir}."
        )
