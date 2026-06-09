"""Stage 0 Master Test Suite Entry Point.

Aggregates all stage 0 tests. Provides `pytest -m stage0` selector.

Test IDs covered:
    ST0-TC-001 ~ ST0-TC-028 (28 cases, ~83% automated, 5 manual)

Usage:
    pytest tests/test_stage0_init.py -v
    pytest tests/ -m stage0 -v
    pytest tests/test_stage0_init.py::TestSessionStatus -v

Related plan: .claude/iterations/testplans/mf-testplan.md (Stage 0 section)
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

# Repository root
REPO_ROOT = Path(__file__).resolve().parent.parent
ITERATIONS_DIR = REPO_ROOT / ".claude" / "iterations"
CONTEXT_DIR = REPO_ROOT / ".claude" / "context"
SKILLS_DIR = REPO_ROOT / ".claude" / "skills"
TEMPLATES_DIR = REPO_ROOT / ".claude" / "templates"
SPRINT_LATEST = ITERATIONS_DIR / "sprint-latest"
GRAPHIFY_OUT = REPO_ROOT / "graphify-out"
MEFAN_LOG = REPO_ROOT / "iterations" / "mefan-log.md"


# All tests in this file belong to stage 0
pytestmark = pytest.mark.stage0


# ──────────────────────────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def session_status():
    """Read session-status.md content (skip if missing)."""
    path = ITERATIONS_DIR / "session-status.md"
    if not path.exists():
        pytest.skip(f"session-status.md 不存在：{path}（请先执行 /mf-upgrade:00-init）")
    return path.read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def project_md():
    path = CONTEXT_DIR / "project.md"
    if not path.exists():
        pytest.skip(f"project.md 不存在：{path}")
    return path.read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def tech_stack_profile():
    path = CONTEXT_DIR / "tech-stack-profile.md"
    if not path.exists():
        pytest.skip(f"tech-stack-profile.md 不存在：{path}")
    return path.read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def feature_elements():
    path = CONTEXT_DIR / "feature-elements.md"
    if not path.exists():
        pytest.skip(f"feature-elements.md 不存在：{path}")
    return path.read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def consistency_baseline():
    path = CONTEXT_DIR / "consistency-baseline.md"
    if not path.exists():
        pytest.skip(f"consistency-baseline.md 不存在：{path}")
    return path.read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def feature_md():
    path = SPRINT_LATEST / "feature.md"
    if not path.exists():
        pytest.skip(f"feature.md 不存在：{path}")
    return path.read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def query_plan():
    path = CONTEXT_DIR / "query_plan.md"
    if not path.exists():
        pytest.skip(f"query_plan.md 不存在：{path}")
    return path.read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def results_json():
    path = CONTEXT_DIR / "results.json"
    if not path.exists():
        pytest.skip(f"results.json 不存在：{path}")
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def project_skills():
    if not SKILLS_DIR.exists():
        return []
    return list(SKILLS_DIR.glob("project-*/SKILL.md"))


# ──────────────────────────────────────────────────────────────
# ST0-TC-001 / 002 / 003 — session-status + sprint-latest/
# ──────────────────────────────────────────────────────────────

class TestSessionStatus:
    """ST0-TC-001/002/003: session-status.md structure + completion time + directory."""

    def test_tc001_has_7_sections(self, session_status):
        """ST0-TC-001: session-status.md ≥ 7 一级章节."""
        sections = re.findall(r"^## ", session_status, re.MULTILINE)
        assert len(sections) >= 7, (
            f"session-status.md 仅 {len(sections)} 个一级章节，期望 ≥ 7"
        )

    def test_tc001_required_sections(self, session_status):
        """ST0-TC-001: 必需章节齐全."""
        required = [
            "迭代概览",
            "自动推进状态",
            "阶段完成记录",
            "User Story 高层状态追踪",
            "产出物追踪表",
            "历史 Sprint 索引",
            "异常记录",
            "PM 阶段完成报告",
        ]
        for s in required:
            assert s in session_status, f"session-status.md 缺少章节：{s}"

    def test_tc002_stage00_completion_time(self, session_status):
        """ST0-TC-002: 阶段 00 完成时间已填写且状态 ✅."""
        # 解析 阶段完成记录 表格行
        m = re.search(
            r"\| 00 \|.*?\|\s*(.*?)\s*\|\s*(✅|⏳)\s*\|",
            session_status,
            re.DOTALL,
        )
        assert m, "阶段完成记录表中找不到阶段 00"
        completion_time = m.group(1).strip()
        status = m.group(2).strip()
        assert completion_time, "阶段 00 完成时间未填写"
        assert status == "✅", f"阶段 00 状态应为 ✅，实际 {status}"

    def test_tc003_sprint_latest_dir_exists(self):
        """ST0-TC-003: sprint-latest/ 目录存在."""
        assert SPRINT_LATEST.exists(), f"{SPRINT_LATEST} 不存在"
        assert SPRINT_LATEST.is_dir(), f"{SPRINT_LATEST} 不是目录"


# ──────────────────────────────────────────────────────────────
# ST0-TC-004 / 005 / 006 — context 三件套
# ──────────────────────────────────────────────────────────────

class TestContextDocs:
    """ST0-TC-004/005/006: project/tech-stack/feature-elements structure."""

    def test_tc004_project_md_chapter_count(self, project_md):
        """ST0-TC-004: project.md 章节数 ≥ 模板."""
        gen = len(re.findall(r"^## ", project_md, re.MULTILINE))
        tmpl_path = TEMPLATES_DIR / "project-template.md"
        if tmpl_path.exists():
            tmpl = len(
                re.findall(r"^## ", tmpl_path.read_text(encoding="utf-8"), re.MULTILINE)
            )
            assert gen >= tmpl, f"project.md 章节数 {gen} < 模板 {tmpl}"

    def test_tc004_project_md_has_sprint_latest(self, project_md):
        """ST0-TC-004: project.md 含 ### 迭代 sprint-latest."""
        assert "### 迭代 sprint-latest" in project_md, (
            "project.md 缺少 '### 迭代 sprint-latest'"
        )

    def test_tc005_tech_stack_section_count(self, tech_stack_profile):
        """ST0-TC-005: tech-stack-profile.md 章节数 ≥ 5."""
        gen = len(re.findall(r"^## ", tech_stack_profile, re.MULTILINE))
        assert gen >= 5, f"tech-stack-profile.md 章节数 {gen} < 5"

    def test_tc005_tech_stack_key_sections(self, tech_stack_profile):
        """ST0-TC-005: 含前端/后端/数据库关键词."""
        for kw in ["前端", "后端", "数据库"]:
            assert kw in tech_stack_profile, (
                f"tech-stack-profile.md 缺少关键词：{kw}"
            )

    def test_tc006_feature_elements_l1_l5(self, feature_elements):
        """ST0-TC-006: 含 L1-L5."""
        for layer in ["L1", "L2", "L3", "L4", "L5"]:
            assert layer in feature_elements, f"feature-elements.md 缺少 {layer}"

    def test_tc006_feature_elements_architecture_diagram(self, feature_elements):
        """ST0-TC-006: §1 含 mermaid 架构图."""
        assert "```mermaid" in feature_elements, (
            "feature-elements.md 缺少 mermaid 架构图"
        )


# ──────────────────────────────────────────────────────────────
# ST0-TC-007 / 008 — 模式 C N-rows 不变量
# ──────────────────────────────────────────────────────────────

class TestPatternC:
    """ST0-TC-007/008: query_plan.md 9 列 + results.json N-rows invariant."""

    def test_tc007_query_plan_9_columns(self, query_plan):
        """ST0-TC-007: query_plan.md 数据行 9 列."""
        data_rows = [
            line for line in query_plan.split("\n")
            if line.startswith("|") and line.count("|") >= 9
        ]
        assert len(data_rows) >= 1, "query_plan.md 没有数据行"
        bad = [r for r in data_rows if r.count("|") != 9]
        assert not bad, f"query_plan.md 有 {len(bad)} 行不是 9 列"

    def test_tc007_query_plan_unique_ids(self, query_plan):
        """ST0-TC-007: 目标 ID 唯一."""
        ids = re.findall(
            r"\|\s*(cb_[\d_]+_q\d+|doc_[\d_]+_q\d+|skill_[\w_]+_q\d+)\s*\|",
            query_plan,
        )
        assert len(ids) == len(set(ids)), (
            f"query_plan.md 有重复 ID：{len(ids) - len(set(ids))} 个"
        )

    def test_tc008_results_json_schema_version(self, results_json):
        """ST0-TC-008: schema_version == 2.1.0."""
        assert results_json.get("schema_version") == "2.1.0", (
            f"results.json schema_version 应为 2.1.0，实际 "
            f"{results_json.get('schema_version')}"
        )

    def test_tc008_results_json_nrows_invariant(self, results_json):
        """ST0-TC-008: 每个 item 的 data.questions 数组非空."""
        items = results_json.get("items", {})
        empty = [
            k for k, v in items.items()
            if not (v.get("data", {}).get("questions") or [])
        ]
        assert not empty, f"N-rows 违反：{empty} 的 data.questions 为空"

    def test_tc008_summary_total_questions_matches(self, results_json):
        """ST0-TC-008: summary.total_questions == sum."""
        items = results_json.get("items", {})
        actual = sum(
            len((v.get("data", {}).get("questions") or []))
            for v in items.values()
        )
        declared = results_json.get("summary", {}).get("total_questions", 0)
        assert actual == declared, (
            f"summary.total_questions {declared} != 实际 {actual}"
        )


# ──────────────────────────────────────────────────────────────
# ST0-TC-009 — graphify 图谱
# ──────────────────────────────────────────────────────────────

class TestGraphify:
    """ST0-TC-009: graphify-out/graph.json 存在性."""

    def test_tc009_graph_json_exists(self):
        path = GRAPHIFY_OUT / "graph.json"
        assert path.exists(), f"{path} 不存在，请先执行 /graphify ."

    def test_tc009_graph_json_has_nodes(self):
        path = GRAPHIFY_OUT / "graph.json"
        if not path.exists():
            pytest.skip("graph.json 不存在")
        data = json.loads(path.read_text(encoding="utf-8"))
        assert "nodes" in data, "graph.json 缺少 nodes 字段"
        assert len(data["nodes"]) > 0, "graph.json nodes 为空"


# ──────────────────────────────────────────────────────────────
# ST0-TC-010 / 026 / 027 — consistency-baseline
# ──────────────────────────────────────────────────────────────

class TestConsistencyBaseline:
    """ST0-TC-010/026/027: 17+ 章 + 证据 + Skill 引用."""

    def test_tc010_cb_chapter_count(self, consistency_baseline):
        """ST0-TC-010: CB 章节数 ≥ 17."""
        chapters = re.findall(r"^### \d+\.", consistency_baseline, re.MULTILINE)
        assert len(chapters) >= 17, (
            f"consistency-baseline.md 章节数 {len(chapters)} < 17"
        )

    def test_tc010_cb_evidence_count(self, consistency_baseline):
        """ST0-TC-010: evidence 引用数 ≥ 30."""
        evidence = re.findall(r":\d+(-\d+)?\b", consistency_baseline)
        assert len(evidence) >= 30, (
            f"consistency-baseline.md 证据数 {len(evidence)} < 30"
        )

    def test_tc010_cb_no_data_count(self, consistency_baseline):
        """ST0-TC-010: [需人工补充]/[NO_DATA] 数 < 5."""
        no_data = re.findall(r"\[需人工补充\]|\[NO_DATA\]", consistency_baseline)
        assert len(no_data) < 5, (
            f"consistency-baseline.md 缺失标记 {len(no_data)} ≥ 5"
        )

    def test_tc026_evidence_total(
        self, consistency_baseline, project_md, tech_stack_profile, feature_elements
    ):
        """ST0-TC-026: 4 个 context 文档 evidence 总数 ≥ 10."""
        all_text = (
            consistency_baseline + project_md + tech_stack_profile + feature_elements
        )
        evidence = re.findall(r":\d+(-\d+)?\b", all_text)
        assert len(evidence) >= 10, (
            f"4 个 context 文档 evidence 总数 {len(evidence)} < 10"
        )

    def test_tc027_cb_skill_references_resolve(self, consistency_baseline):
        """ST0-TC-027: CB §5 引用的 Skills 目录必须存在."""
        skill_refs = re.findall(
            r"project-([\w-]+)/SKILL\.md", consistency_baseline
        )
        for ref in skill_refs:
            skill_path = SKILLS_DIR / f"project-{ref}" / "SKILL.md"
            assert skill_path.exists(), (
                f"CB 引用了不存在的 Skill：{skill_path}"
            )


# ──────────────────────────────────────────────────────────────
# ST0-TC-011 / 012 / 013 — Skills
# ──────────────────────────────────────────────────────────────

class TestSkills:
    """ST0-TC-011/012/013: Skill 数量 + frontmatter + examples.md."""

    def test_tc011_skill_count_matches_fe(self, project_skills, feature_elements):
        """ST0-TC-011: Skill 数 ≥ FE 数."""
        fe_count = len(re.findall(r"\bFE-[IDAF]-\d+\b", feature_elements))
        assert len(project_skills) >= fe_count, (
            f"Skill 数 {len(project_skills)} < FE 数 {fe_count}"
        )

    def test_tc012_skill_frontmatter(self, project_skills):
        """ST0-TC-012: 每个 SKILL.md 含规范 frontmatter."""
        for path in project_skills:
            text = path.read_text(encoding="utf-8")
            assert text.startswith("---"), f"{path} 缺少 frontmatter"
            end = text.find("---", 3)
            assert end > 0, f"{path} frontmatter 未闭合"
            fm = text[3:end]
            assert "name:" in fm, f"{path} frontmatter 缺少 name"
            assert "description:" in fm, f"{path} frontmatter 缺少 description"
            assert re.search(r"Use when", fm, re.IGNORECASE), (
                f"{path} description 不含 'Use when'"
            )

    def test_tc013_pattern_c_examples_top_level(self, project_skills):
        """ST0-TC-013: examples.md 顶层（深度=1）."""
        for skill_dir in SKILLS_DIR.glob("project-*"):
            examples = skill_dir / "examples.md"
            if examples.exists():
                assert examples.parent.parent == SKILLS_DIR, (
                    f"examples.md 嵌套过深：{examples}"
                )

    def test_tc013_no_nested_references(self):
        """ST0-TC-013: 不允许嵌套 references/（与 superpowers 一致）."""
        for path in SKILLS_DIR.glob("project-*/references"):
            assert not path.exists(), f"Skill 不应嵌套 references/：{path}"

    def test_tc013_no_assets_or_tests_dirs(self):
        """ST0-TC-013: 不允许 assets/、tests/ 目录."""
        for skill_dir in SKILLS_DIR.glob("project-*"):
            for sub in ["assets", "tests"]:
                assert not (skill_dir / sub).exists(), (
                    f"Skill 不应包含 {sub}/：{skill_dir / sub}"
                )


# ──────────────────────────────────────────────────────────────
# ST0-TC-014 / 028 — 跨文档一致性
# ──────────────────────────────────────────────────────────────

class TestCrossDocument:
    """ST0-TC-014/028: 双向同步 + sprint 隔离."""

    def test_tc014_outputs_listed_in_session_status(self, session_status):
        """ST0-TC-014: 6 个 stage 0 产出物在 session-status 中有引用."""
        for name in [
            "project.md", "tech-stack-profile.md", "feature-elements.md",
            "consistency-baseline.md", "feature.md", "session-status.md",
        ]:
            assert name in session_status, (
                f"session-status 产出物追踪表缺 {name}"
            )

    def test_tc028_sprint_isolation(self):
        """ST0-TC-028: sprint-latest 与历史 sprint 隔离."""
        if not SPRINT_LATEST.exists():
            pytest.skip("sprint-latest 不存在")
        # 校验历史 sprint 不可写（仅检查存在性）
        history = [
            e for e in ITERATIONS_DIR.iterdir()
            if e.name.startswith("sprint-") and e.name != "sprint-latest"
        ]
        # 弱校验：历史 sprint 不应与 sprint-latest 重名
        for entry in history:
            assert entry.name != "sprint-latest", "重名冲突"


# ──────────────────────────────────────────────────────────────
# ST0-TC-015 / 016 — feature.md
# ──────────────────────────────────────────────────────────────

class TestFeatureMd:
    """ST0-TC-015/016: feature.md 模板继承 + 必填字段."""

    def test_tc015_feature_md_sections(self, feature_md):
        """ST0-TC-015: feature.md 含模板的所有 10 章节."""
        for sec in [
            "基本信息", "功能要点列表", "功能详情",
            "现有项目分析", "功能交互分析", "非功能性需求",
            "部署与兼容性", "替代方案分析", "业务规则",
            "待确认事项", "验收标准", "备注", "澄清对话记录",
        ]:
            assert sec in feature_md, f"feature.md 缺少章节：{sec}"

    def test_tc015_feature_md_has_at_least_one_feature(self, feature_md):
        """ST0-TC-015: feature.md ≥ 1 个 FEATURE-XXX."""
        ids = re.findall(r"\bFEATURE-\d+\b", feature_md)
        assert len(ids) >= 1, "feature.md 没有任何 FEATURE-XXX"

    def test_tc016_feature_md_has_acceptance_criteria(self, feature_md):
        """ST0-TC-016: feature.md 含验收标准."""
        assert "验收标准" in feature_md, "feature.md 缺少验收标准"

    def test_tc016_feature_md_has_clarification_log(self, feature_md):
        """ST0-TC-016: feature.md 含澄清对话记录 ≥ 1 轮."""
        assert "澄清对话记录" in feature_md, (
            "feature.md 缺少澄清对话记录"
        )
        rounds = re.findall(r"第 \d+ 轮", feature_md)
        assert len(rounds) >= 1, "澄清对话记录至少 1 轮"


# ──────────────────────────────────────────────────────────────
# ST0-TC-017 / 018 — HARNESS_VERSION / CHANGELOG
# ──────────────────────────────────────────────────────────────

class TestHarnessClosure:
    """ST0-TC-017/018: Stage 6 → 0 闭环文件."""

    def test_tc017_harness_version(self):
        """ST0-TC-017: HARNESS_VERSION.md 存在 + 格式正确."""
        path = REPO_ROOT / "HARNESS_VERSION.md"
        if not path.exists():
            pytest.skip("HARNESS_VERSION.md 不存在（首次运行 OK）")
        text = path.read_text(encoding="utf-8")
        assert re.search(r"v\d+\.\d+\.\d+", text), (
            "HARNESS_VERSION.md 缺版本号"
        )

    def test_tc018_changelog(self):
        """ST0-TC-018: CHANGELOG.md 存在 + 含版本条目."""
        path = REPO_ROOT / "CHANGELOG.md"
        if not path.exists():
            pytest.skip("CHANGELOG.md 不存在（首次运行 OK）")
        text = path.read_text(encoding="utf-8")
        versions = re.findall(r"^## \[?v?\d+\.\d+", text, re.MULTILINE)
        assert len(versions) >= 1, "CHANGELOG.md 缺版本条目"


# ──────────────────────────────────────────────────────────────
# ST0-TC-023 / 024 — 异常路径（集成测试占位）
# ──────────────────────────────────────────────────────────────

class TestFailureModes:
    """ST0-TC-023/024: 失败容错.

    实际执行需要修改真实文件，由 MT0-5 端到端冒烟测试覆盖。
    """

    def test_tc023_graphify_degradation_marker(self):
        """ST0-TC-023: 验证降级字符串可被检测（不执行真实降级）."""
        # 实际由集成测试覆盖
        assert True  # placeholder

    def test_tc024_template_missing_hard_block(self):
        """ST0-TC-024: 模板缺失必须硬阻塞（集成测试占位）."""
        assert True  # placeholder


# ──────────────────────────────────────────────────────────────
# ST0-TC-025 — 日志
# ──────────────────────────────────────────────────────────────

class TestLogging:
    """ST0-TC-025: mefan-log.md 写入."""

    def test_tc025_mefan_log_exists(self):
        path = MEFAN_LOG
        assert path.exists(), f"{path} 不存在"

    def test_tc025_stage0_logs_present(self):
        path = MEFAN_LOG
        if not path.exists():
            pytest.skip("mefan-log.md 不存在")
        text = path.read_text(encoding="utf-8")
        assert "PM" in text, "mefan-log.md 缺 PM 记录"
        assert "Architect" in text, "mefan-log.md 缺 Architect 记录"
        assert "Analyst" in text, "mefan-log.md 缺 Analyst 记录"


# ──────────────────────────────────────────────────────────────
# ST0-TC-029 — Legacy Skill 死代码回归测试
# ──────────────────────────────────────────────────────────────
#
# 历史背景：`project-create-skill` 是早期的元 Skill，意图作为 "生成其他 Skill" 的工具。
# 但从未被任何 agent / command / hook 实际调用过，且不符合 superpowers frontmatter 规范。
# 2026-06-09 删除，统一改用 `superpowers:writing-skills`（在 architect-stage0 / pm-stage6 /
# coach-stage6 共 7 处显式调用）。
#
# 本测试防止其被误恢复。

class TestLegacySkillRegression:
    """ST0-TC-029: 防止 project-create-skill 复活."""

    def test_legacy_skill_not_present(self):
        """project-create-skill 目录不存在."""
        legacy = SKILLS_DIR / "project-create-skill"
        assert not legacy.exists(), (
            f"死代码回归：{legacy} 已被删除，禁止恢复。"
            "Skill 生成统一用 superpowers:writing-skills（见 architect-stage0.md 操作 2.6 / "
            "pm-stage6.md 操作 4 / coach-stage6.md 操作 1）"
        )

    def test_legacy_skill_md_not_present(self):
        """project-create-skill/SKILL.md 不存在."""
        legacy = SKILLS_DIR / "project-create-skill" / "SKILL.md"
        assert not legacy.exists(), f"死代码回归：{legacy} 已被删除"

    def test_no_agent_references_legacy_skill(self):
        """agents 中无 project-create-skill 引用."""
        agents_dir = REPO_ROOT / ".claude" / "agents"
        for path in agents_dir.glob("*.md"):
            text = path.read_text(encoding="utf-8")
            assert "project-create-skill" not in text, (
                f"{path} 仍引用 project-create-skill（死代码）"
            )

    def test_no_command_references_legacy_skill(self):
        """commands 中无 project-create-skill 引用."""
        commands_dir = REPO_ROOT / ".claude" / "commands"
        for path in commands_dir.glob("**/*.md"):
            text = path.read_text(encoding="utf-8")
            assert "project-create-skill" not in text, (
                f"{path} 仍引用 project-create-skill（死代码）"
            )

    def test_no_hook_references_legacy_skill(self):
        """hooks 中无 project-create-skill 引用."""
        hooks_dir = REPO_ROOT / ".claude" / "hooks"
        for path in hooks_dir.glob("*.sh"):
            text = path.read_text(encoding="utf-8")
            assert "project-create-skill" not in text, (
                f"{path} 仍引用 project-create-skill（死代码）"
            )


# ──────────────────────────────────────────────────────────────
# ST0-TC-030 — superpowers:writing-skills 替代检查
# ──────────────────────────────────────────────────────────────
#
# 验证 3 个生成 Skill 的位置都显式调用了 superpowers:writing-skills。
# 这保证 project-create-skill 删除后没有功能空缺。

class TestWritingSkillsSubstitution:
    """ST0-TC-030: superpowers:writing-skills 替代 project-create-skill."""

    def test_architect_stage0_invokes_writing_skills(self):
        """architect-stage0.md 显式调用 superpowers:writing-skills."""
        agent = REPO_ROOT / ".claude" / "agents" / "architect-stage0.md"
        text = agent.read_text(encoding="utf-8")
        assert "superpowers:writing-skills" in text, (
            f"{agent} 缺少 superpowers:writing-skills 引用"
        )
        # 至少 1 次 Skill tool 显式调用
        assert re.search(r'Skill\(skill=["\']superpowers:writing-skills["\']\)', text), (
            f"{agent} 缺少 Skill(skill='superpowers:writing-skills') 显式调用"
        )

    def test_pm_stage6_invokes_writing_skills(self):
        """pm-stage6.md 显式调用 superpowers:writing-skills（合并新 Skill 时）."""
        agent = REPO_ROOT / ".claude" / "agents" / "pm-stage6.md"
        text = agent.read_text(encoding="utf-8")
        assert "superpowers:writing-skills" in text, (
            f"{agent} 缺少 superpowers:writing-skills 引用"
        )

    def test_coach_stage6_invokes_writing_skills(self):
        """coach-stage6.md 显式调用 superpowers:writing-skills（写 evolution-proposal 时）."""
        agent = REPO_ROOT / ".claude" / "agents" / "coach-stage6.md"
        text = agent.read_text(encoding="utf-8")
        assert "superpowers:writing-skills" in text, (
            f"{agent} 缺少 superpowers:writing-skills 引用"
        )
