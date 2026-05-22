# 文件创建清单 (Files Created by Command)

> 本文件记录每个 Command 阶段创建/更新的所有文件，供依赖检查用。
> 格式：`Command | 文件名 | 完整路径 | 模板 | 被依赖阶段`
> **重要**：每个文件的"被依赖阶段"说明该文件是哪些后续阶段的必要输入。

---

## 00-init (会话初始化与上下文建立)

| 文件名 | 完整路径 | 模板 | 被依赖阶段 |
|--------|----------|------|-----------|
| tech-stack-profile.md | `.claude/context/tech-stack-profile.md` | `.claude/templates/tech-stack-profile-template.md` | 01-requirements (§2), 02-arch-qa (§2) |
| consistency-baseline.md | `.claude/context/consistency-baseline.md` | `.claude/templates/consistency-baseline-template.md` | 01-requirements (§2), 02-arch-qa (§2), 04-implement (§2) |
| session-status.md | `.claude/iterations/session-status.md` | `.claude/templates/session-status-template.md` | 01-requirements (§2), 03-plan (§2), 04-implement (§2), 06-retrospect (§2), 下一 iteration 的 00-init (§2.2/§2.4 记录加载的实验规则/技能) |

---

## 01-requirements (需求澄清与现有系统分析)

| 文件名 | 完整路径 | 模板 | 被依赖阶段 |
|--------|----------|------|-----------|
| requirements/*.md | `.claude/iterations/sprint-latest/requirements/upgrade-YYYY-MM-DD-title.md` | `.claude/templates/requirements-template.md` | 02-arch-qa (§2), 03-plan (§2), 05-quality (§4.2) |

---

## 02-arch-qa (架构设计与测试策略)

| 文件名 | 完整路径 | 模板 | 被依赖阶段 |
|--------|----------|------|-----------|
| adr/*.md | `.claude/iterations/sprint-latest/adr/upgrade-YYYY-MM-DD-title.md` | `.claude/templates/adr-template.md` | 03-plan (§2), 04-implement (§2) |
| test-plan/*.md | `.claude/iterations/sprint-latest/test-plan/upgrade-YYYY-MM-DD-title.md` | `.claude/templates/test-plan-template.md` | 03-plan (§2), 05-quality (§2) |

---

## 03-plan (迭代计划与任务排期)

| 文件名 | 完整路径 | 模板 | 被依赖阶段 |
|--------|----------|------|-----------|
| iteration-plan.md | `.claude/iterations/sprint-latest/iteration-plan.md` | `.claude/templates/iteration-plan-template.md` | 04-implement (§2), 05-quality (§2) |
| sprint-status.md | `.claude/iterations/sprint-latest/sprint-status.md` | `.claude/templates/sprint-status-template.md` | 04-implement (§2), 05-quality (§2), 06-retrospect (§2) |

---

## 04-implement (迭代实现)

| 文件名 | 完整路径 | 模板 | 被依赖阶段 |
|--------|----------|------|-----------|
| task-summary/T{NNN}.md | `.claude/iterations/sprint-latest/task-summary/T{NNN}.md` | `.claude/templates/task-summary-template.md` | 05-quality (§2), 06-retrospect (§2) |
| test-results/unit-T{NNN}.log | `.claude/iterations/sprint-latest/test-results/unit-T{NNN}.log` | - | 05-quality (§4.1), 06-retrospect (§4.1) |
| interception-analysis.md | `.claude/iterations/sprint-latest/task-summary/interception-analysis.md` | - | 06-retrospect（分析Hook拦截模式） |

---

## 05-quality (质量测试与门禁)

| 文件名 | 完整路径 | 模板 | 被依赖阶段 |
|--------|----------|------|-----------|
| test-results/regression-YYYY-MM-DD.log | `.claude/iterations/sprint-latest/test-results/regression-YYYY-MM-DD.log` | - | 06-retrospect (§4.1) |
| test-results/manual-test-guide.md | `.claude/iterations/sprint-latest/test-results/manual-test-guide.md` | `.claude/templates/manual-test-guide-template.md` | 人机交接用 |
| test-results/quality-report.md | `.claude/iterations/sprint-latest/test-results/quality-report.md` | `.claude/templates/quality-report-template.md` | 06-retrospect (§4.1) |
| bug-log/auto-YYYY-MM-DD.md | `.claude/iterations/sprint-latest/bug-log/auto-YYYY-MM-DD.md` | `.claude/templates/bug-log-template.md` | 06-retrospect (§4.3) |
| bug-log/manual-YYYY-MM-DD.md | `.claude/iterations/sprint-latest/bug-log/manual-YYYY-MM-DD.md` | `.claude/templates/bug-log-template.md` | 06-retrospect (§4.3) |

---

## 06-retrospect (迭代总结与进化)

| 文件名 | 完整路径 | 模板 | 被依赖阶段 |
|--------|----------|------|-----------|
| iteration-retrospective.md | `.claude/iterations/sprint-latest/iteration-retrospective.md` | `.claude/templates/iteration-retrospective-template.md` | 下一 iteration 的 00-init（输入上下文）、06-retrospect §4.4（进化分析参考） |
| evolution-proposal.md | `.claude/evolution-proposals/upgrade-YYYY-MM-DD-title.md` | `.claude/templates/evolution-proposal-template.md` | 06-retrospect §4.4 采纳后写入 rules-proposed/ 或 skills-proposed/ → 下一 iteration 的 00-init §2.2/§2.4 加载 |
| rules-proposed/*.md | `.claude/rules-proposed/` | - | 下一 iteration 的 00-init §2.2 加载为实验规则 |
| skills-proposed/*.md | `.claude/skills-proposed/` | - | 下一 iteration 的 00-init §2.4 加载为实验技能 |
| reports/PROJECT_STATUS.md | `.claude/reports/PROJECT_STATUS.md` | `.claude/templates/project-status-template.md` | 全局可读，下一 iteration 参考 |
| CHANGELOG.md | `CHANGELOG.md`（更新） | - | 全局可读 |
| HARNESS_VERSION.md | `.claude/HARNESS_VERSION.md`（更新） | - | 所有阶段（版本参考） |

---

## 全局文件（不隶属于特定 iteration）

| 文件名 | 完整路径 | 说明 | 被依赖阶段 |
|--------|----------|------|-----------|
| mefan-log.md | `.claude/iterations/mefan-log.md` | 全局框架运行日志 | 所有阶段（日志追加） |
| violations.json | `.claude/iterations/sprint-latest/violations.json` | Hook拦截记录 | 06-retrospect (§2) |

---

## 依赖闭环检查规则

1. **阶段 N 的前置输入**必须是阶段 < N 的产出物。
2. **阶段 N 不可读取**阶段 > N 的产出物（未来产出不存在）。
3. **阶段 0 是唯一例外**：无前置输入，但必须确保所需目录存在，不存在则报错退出。
4. **跨 iteration 依赖**：全局文件（mefan-log.md、CHANGELOG.md、HARNESS_VERSION.md）可被后续 iteration 读取。

---

## 文件路径规范（供检查）

| 文件类型 | 规范路径 |
|----------|----------|
| 全局上下文 | `.claude/context/` |
| 全局规则 | `.claude/rules/` |
| 全局技能 | `.claude/skills/` |
| 全局模板 | `.claude/templates/` |
| 全局报告 | `.claude/reports/` |
| 进化提案 | `.claude/evolution-proposals/` |
| 单次迭代 | `.claude/iterations/sprint-YYYY-MM-DD/` |
| 迭代内产出物 | `.claude/iterations/sprint-latest/requirements/` |
| | `.claude/iterations/sprint-latest/adr/` |
| | `.claude/iterations/sprint-latest/test-plan/` |
| | `.claude/iterations/sprint-latest/task-summary/` |
| | `.claude/iterations/sprint-latest/test-results/` |
| | `.claude/iterations/sprint-latest/bug-log/` |