r"""Skill 闭环验证：ADR §7.3 per-Task skill 列表 ↔ mefan-log.md 中 dev 的 log 条目。

闭合路径：
  1. Stage 2 在 pseudocode/T-NNN.md 的 `## Skill 依赖` 表声明 required skills
  2. Stage 4 dev-stage4 在操作 3.2 用 Read + log-event.sh 显式加载并记录
  3. 本测试断言：对每个 T-NNN，required skills ⊆ loaded skills
     不在 loaded 集合中的 required skill = 闭环断裂

Schema 约束（adr-template.md §7.3）：
  - `## Skill 依赖` 表**至少 1 行**（空表 = 违规）
  - `Skill 文件` 列**必须**符合 `^project-[a-z0-9-]+\.md$`（精确文件名）
  - **不得**使用通配符（如 `project-tech-*.md`）

Log 格式（log-event.sh 6 字段）：
  `| 时间戳 | 阶段 | Agent | 事件类型 | 描述 | 关联 | 结果 |`
  事件类型 = `加载Skill`；关联 = `{MG_ID}:T-{NNN}`；描述 = `{Skill 文件}`

设计依据：plan `/home/amdin/.claude/plans/tingly-launching-seahorse.md`
模式参考：tests/test_declared_vs_invoked.py
"""
from __future__ import annotations

import re
import textwrap
from pathlib import Path

import pytest


# ── 正则（与 schema / log-event.sh 格式严格对齐） ─────────────────────────

# ADR §7.3 §18.1：Skill 文件列必须符合精确文件名（不允许通配符）
SKILL_FILE_RE = re.compile(r"^project-[a-z0-9-]+\.md$")

# log-event.sh 第 3 字段 = 事件类型 `加载Skill`
# 第 4 字段 = 描述（skill 文件名）
# 第 5 字段 = 关联（MG_ID:T-NNN）
LOG_LOAD_RE = re.compile(
    r"加载Skill\s*\|\s*([\w.\-]+\.md)\s*\|\s*([\w\-]+):T-(\d+)"
)


# ── 解析器 ───────────────────────────────────────────────────────────────


def _parse_required_skills(pseudo_text: str) -> list[str]:
    """从 `## Skill 依赖` 表中提取 `Skill 文件` 列。

    跳过非法行（如 `project-tech-*.md` 通配符、空单元格）。
    """
    m = re.search(r"##\s*Skill\s*依赖\s*\n(.*?)(?=\n##|\Z)", pseudo_text, re.DOTALL)
    if not m:
        return []
    skills: list[str] = []
    for line in m.group(1).splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip().strip("`") for c in line.split("|")[1:-1]]
        if not cells:
            continue
        if SKILL_FILE_RE.match(cells[0]):
            skills.append(cells[0])
    return skills


def _parse_loaded_skills(log_text: str, task_num: str) -> set[str]:
    """从 mefan-log.md 提取某 T-NNN 加载过的 skill 集合。"""
    loaded: set[str] = set()
    for m in LOG_LOAD_RE.finditer(log_text):
        skill_file, _mg, log_task = m.group(1), m.group(2), m.group(3)
        if log_task == task_num:
            loaded.add(skill_file)
    return loaded


def _task_id_from_filename(stem: str) -> tuple[str, str]:
    """`T-001-entity` → `('T-001', '001')`."""
    head = stem.split("-", 2)[:2]  # ["T", "001"]
    return f"{head[0]}-{head[1]}", head[1]


# ── 测试 ─────────────────────────────────────────────────────────────────


def test_required_skills_were_loaded(tmp_path: Path) -> None:
    """T-NNN.md 声明的 skill 必须全部在 mefan-log.md 出现 `加载Skill` 条目。

    Fixture: 2 个 task, T-001 声明 2 个 skill, T-002 声明 1 个,
    log 全部加载 → 通过。
    """
    sprint = tmp_path / "sprint-latest"
    pseudo_dir = sprint / "pseudocode"
    pseudo_dir.mkdir(parents=True)
    log = sprint / "mefan-log.md"
    log.write_text(
        textwrap.dedent(
            """\
            | 时间戳 | 阶段 | Agent | 事件类型 | 描述 | 关联 | 结果 |
            |---|---|---|---|---|---|---|
            """
        ),
        encoding="utf-8",
    )

    (pseudo_dir / "T-001-entity.md").write_text(
        textwrap.dedent(
            """\
            # T-001 实体创建

            ## Skill 依赖

            | Skill 文件 | 来源 | 体现 |
            |-----------|------|------|
            | project-tech-lombok.md | cb 5.3 | @Getter |
            | project-middleware-database.md | cb 5.5 | Page<> |
            """
        ),
        encoding="utf-8",
    )
    (pseudo_dir / "T-002-repo.md").write_text(
        textwrap.dedent(
            """\
            # T-002 Repository

            ## Skill 依赖

            | Skill 文件 | 来源 | 体现 |
            |-----------|------|------|
            | project-mybatis-pattern.md | cb 5.4 | ORM |
            """
        ),
        encoding="utf-8",
    )
    log.write_text(
        textwrap.dedent(
            """\
            | 时间戳 | 阶段 | Agent | 事件类型 | 描述 | 关联 | 结果 |
            |---|---|---|---|---|---|---|
            | 2026-06-06 10:00:00 | 04 | Dev | 加载Skill | project-tech-lombok.md | MG-001:T-001 | 成功 |
            | 2026-06-06 10:00:01 | 04 | Dev | 加载Skill | project-middleware-database.md | MG-001:T-001 | 成功 |
            | 2026-06-06 10:00:02 | 04 | Dev | 加载Skill | project-mybatis-pattern.md | MG-001:T-002 | 成功 |
            """
        ),
        encoding="utf-8",
    )

    failures: list[tuple[str, list[str]]] = []
    for f in sorted(pseudo_dir.glob("T-*.md")):
        task_id, task_num = _task_id_from_filename(f.stem)
        required = _parse_required_skills(f.read_text(encoding="utf-8"))
        loaded = _parse_loaded_skills(log.read_text(encoding="utf-8"), task_num)
        missing = sorted(set(required) - loaded)
        if missing:
            failures.append((task_id, missing))

    assert not failures, (
        "Skill 闭环断裂：\n"
        + "\n".join(f"  {tid}: 未加载 {m}" for tid, m in failures)
    )


def test_detects_missing_skill(tmp_path: Path) -> None:
    """required skill 缺失时,test_detects_missing_skill 应能精确报告缺失项。

    本测试不调用 assert 失败路径,而是**直接计算缺失集**来验证检测逻辑。
    """
    sprint = tmp_path / "sprint-latest"
    (sprint / "pseudocode").mkdir(parents=True)
    (sprint / "pseudocode" / "T-001-test.md").write_text(
        textwrap.dedent(
            """\
            ## Skill 依赖

            | Skill 文件 | 来源 | 体现 |
            |-----------|------|------|
            | project-tech-lombok.md | cb | @Getter |
            | project-tech-jpa.md | cb | @Entity |
            """
        ),
        encoding="utf-8",
    )
    (sprint / "mefan-log.md").write_text(
        textwrap.dedent(
            """\
            | 时间戳 | 阶段 | Agent | 事件类型 | 描述 | 关联 | 结果 |
            |---|---|---|---|---|---|---|
            | t | 04 | Dev | 加载Skill | project-tech-lombok.md | MG-001:T-001 | 成功 |
            """
        ),
        encoding="utf-8",
    )
    log_text = (sprint / "mefan-log.md").read_text(encoding="utf-8")
    required = _parse_required_skills(
        (sprint / "pseudocode" / "T-001-test.md").read_text(encoding="utf-8")
    )
    loaded = _parse_loaded_skills(log_text, "001")
    missing = set(required) - loaded
    assert missing == {"project-tech-jpa.md"}, (
        f"应仅检测到 project-tech-jpa.md 缺失,实际: {missing}"
    )


def test_wildcard_skill_name_rejected() -> None:
    """`project-tech-*.md` 通配符**不应**被解析为合法 required skill。

    Schema 约束（adr-template.md §7.3）：`Skill 文件` 必须精确文件名,不允许通配。
    """
    text = textwrap.dedent(
        """\
        ## Skill 依赖

        | Skill 文件 | 来源 | 体现 |
        |-----------|------|------|
        | project-tech-*.md | cb | 全套 |
        """
    )
    assert _parse_required_skills(text) == [], (
        "通配符应被 schema 拒绝,不应进入 required skills 集合"
    )


def test_log_load_re_matches_realistic_log_line() -> None:
    """log-event.sh 实际产生的行格式应能被正则解析。

    行格式:`| {ts} | 04 | Dev | 加载Skill | xxx.md | MG-001:T-001 | 成功 |`
    """
    line = "| 2026-06-06 10:00:00 | 04 | Dev | 加载Skill | project-tech-lombok.md | MG-001:T-001 | 成功 |"
    m = LOG_LOAD_RE.search(line)
    assert m is not None, f"正则未匹配: {line!r}"
    assert m.group(1) == "project-tech-lombok.md"
    assert m.group(2) == "MG-001"
    assert m.group(3) == "001"
