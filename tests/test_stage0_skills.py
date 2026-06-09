"""Stage 0 Skills 独立测试.

可独立运行：`pytest tests/test_stage0_skills.py -v`
覆盖 ST0-TC-011/012/013 的 Skill 相关部分。

Related plan: .claude/iterations/testplans/mf-testplan.md (Stage 0 / Skills)
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / ".claude" / "skills"
TEMPLATES_DIR = REPO_ROOT / ".claude" / "templates"
FE_PATH = REPO_ROOT / ".claude" / "context" / "feature-elements.md"

pytestmark = pytest.mark.stage0


def test_skill_count_matches_fe():
    """ST0-TC-011: Skill 数 ≥ FE 数."""
    if not FE_PATH.exists():
        pytest.skip("feature-elements.md 不存在")
    fe_count = len(re.findall(r"\bFE-[IDAF]-\d+\b", FE_PATH.read_text(encoding="utf-8")))
    skill_count = len(list(SKILLS_DIR.glob("project-*/SKILL.md")))
    assert skill_count >= fe_count, f"Skill {skill_count} < FE {fe_count}"


@pytest.mark.parametrize("skill_path", list(SKILLS_DIR.glob("project-*/SKILL.md")))
def test_skill_frontmatter(skill_path):
    """ST0-TC-012: 每个 SKILL.md 含规范 frontmatter（superpowers:writing-skills 规范）."""
    text = skill_path.read_text(encoding="utf-8")
    assert text.startswith("---"), f"{skill_path} 缺 frontmatter"
    end = text.find("---", 3)
    assert end > 0, f"{skill_path} frontmatter 未闭合"
    fm = text[3:end]
    assert "name:" in fm, f"{skill_path} frontmatter 缺 name"
    assert "description:" in fm, f"{skill_path} frontmatter 缺 description"
    assert re.search(r"Use when", fm, re.IGNORECASE), (
        f"{skill_path} description 缺 'Use when'"
    )


def test_no_nested_references():
    """ST0-TC-013: 不允许嵌套 references/ 目录（与 superpowers 一致）."""
    for path in SKILLS_DIR.glob("project-*/references"):
        assert not path.exists(), f"Skill 不应嵌套 references/：{path}"


def test_no_assets_or_tests_dirs():
    """ST0-TC-013: 不允许 assets/、tests/ 目录（与 superpowers 一致）."""
    for skill_dir in SKILLS_DIR.glob("project-*"):
        for sub in ["assets", "tests"]:
            assert not (skill_dir / sub).exists(), (
                f"Skill 不应包含 {sub}/：{skill_dir / sub}"
            )


def test_examples_md_top_level():
    """ST0-TC-013: examples.md 顶层（深度=1）."""
    for examples in SKILLS_DIR.glob("project-*/examples.md"):
        assert examples.parent.parent == SKILLS_DIR, (
            f"examples.md 嵌套过深：{examples}"
        )


def test_examples_md_cites_path_line():
    """ST0-TC-013: examples.md 的 fenced code block 前必须有 path:line-line 引用."""
    for examples in SKILLS_DIR.glob("project-*/examples.md"):
        content = examples.read_text(encoding="utf-8")
        code_blocks = re.findall(r"```\w+", content)
        cite_headers = re.findall(r"### `[^`]+\.\w+:\d+(-\d+)?`", content)
        if len(code_blocks) > 0:
            ratio = len(cite_headers) / len(code_blocks)
            assert ratio >= 0.8, (
                f"{examples} 引用率 {ratio:.0%} < 80%"
            )


def test_skill_no_meta_fields():
    """不允许 meta 字段（category/version/author/created/trigger 等）."""
    # 来自 architect-stage0.md 操作 2.6.2 步骤 5
    forbidden = ["category:", "version:", "author:", "created:",
                 "trigger:", "depends_on:", "provides_to:"]
    for skill_path in SKILLS_DIR.glob("project-*/SKILL.md"):
        text = skill_path.read_text(encoding="utf-8")
        end = text.find("---", 3)
        if end < 0:
            continue
        fm = text[3:end].lower()
        for field in forbidden:
            assert field not in fm, (
                f"{skill_path} frontmatter 含禁止字段：{field}"
            )
