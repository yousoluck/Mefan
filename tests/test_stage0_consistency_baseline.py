"""Stage 0 Consistency Baseline 独立测试.

可独立运行：`pytest tests/test_stage0_consistency_baseline.py -v`
覆盖 ST0-TC-010/026/027 的 CB 相关部分。

Related plan: .claude/iterations/testplans/mf-testplan.md (Stage 0 / Consistency Baseline)
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
CB_PATH = REPO_ROOT / ".claude" / "context" / "consistency-baseline.md"
TEMPLATE_PATH = REPO_ROOT / ".claude" / "templates" / "consistency-baseline-template.md"
SKILLS_DIR = REPO_ROOT / ".claude" / "skills"

pytestmark = pytest.mark.stage0


def test_cb_exists():
    """CB 文件存在."""
    assert CB_PATH.exists(), f"{CB_PATH} 不存在"


def test_cb_chapter_count_17():
    """ST0-TC-010: CB 章节数 ≥ 17."""
    if not CB_PATH.exists():
        pytest.skip("consistency-baseline.md 不存在")
    text = CB_PATH.read_text(encoding="utf-8")
    chapters = re.findall(r"^### \d+\.", text, re.MULTILINE)
    assert len(chapters) >= 17, f"章节数 {len(chapters)} < 17"


def test_cb_evidence_count_30():
    """ST0-TC-010: CB 证据数 ≥ 30."""
    if not CB_PATH.exists():
        pytest.skip("consistency-baseline.md 不存在")
    text = CB_PATH.read_text(encoding="utf-8")
    evidence = re.findall(r":\d+(-\d+)?\b", text)
    assert len(evidence) >= 30, f"证据数 {len(evidence)} < 30"


def test_cb_no_data_count():
    """ST0-TC-010: [需人工补充] 标记 < 5."""
    if not CB_PATH.exists():
        pytest.skip("consistency-baseline.md 不存在")
    text = CB_PATH.read_text(encoding="utf-8")
    no_data = re.findall(r"\[需人工补充\]|\[NO_DATA\]", text)
    assert len(no_data) < 5, f"缺失标记 {len(no_data)} ≥ 5"


def test_cb_skill_references_resolve():
    """ST0-TC-027: CB 引用的 Skills 目录必须存在."""
    if not CB_PATH.exists():
        pytest.skip("consistency-baseline.md 不存在")
    text = CB_PATH.read_text(encoding="utf-8")
    refs = re.findall(r"project-([\w-]+)/SKILL\.md", text)
    assert len(refs) >= 1, "CB 未引用任何 Skill"
    for ref in refs:
        path = SKILLS_DIR / f"project-{ref}" / "SKILL.md"
        assert path.exists(), f"CB 引用了不存在的 Skill：{path}"


def test_cb_template_chapter_parity():
    """CB 章节数与模板对齐（不遗漏）."""
    if not CB_PATH.exists() or not TEMPLATE_PATH.exists():
        pytest.skip("CB 或 template 缺失")
    cb_chapters = set(re.findall(r"^### \d+\.\s*(.+)$",
                                 CB_PATH.read_text(encoding="utf-8"),
                                 re.MULTILINE))
    tmpl_chapters = set(re.findall(r"^### \d+\.\s*(.+)$",
                                   TEMPLATE_PATH.read_text(encoding="utf-8"),
                                   re.MULTILINE))
    missing = tmpl_chapters - cb_chapters
    assert not missing, f"CB 缺失模板章节：{missing}"


def test_cb_has_reference_module_section():
    """CB 含"参考模块"章节（rule: reference-module.md）."""
    if not CB_PATH.exists():
        pytest.skip("consistency-baseline.md 不存在")
    text = CB_PATH.read_text(encoding="utf-8")
    assert "参考模块" in text, "CB 缺少 '参考模块' 章节（违反 reference-module.md）"
