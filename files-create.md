# 文件创建清单 (Files Created by Command)

> 本文件记录每个 Command/Agent 创建的所有文件，供依赖检查用。
> 格式：`Command | 文件名 | 完整路径 | 模板 | 被依赖阶段`
> **重要**：每个文件的"被依赖阶段"说明该文件是哪些后续阶段的必要输入。

---

## 阶段0 (/mf-upgrade:00-init)

### PM-Stage0

| 文件名 | 完整路径 | 模板 | 被依赖阶段 |
|--------|----------|------|-----------|
| session-status.md | `.claude/iterations/session-status.md` | `.claude/templates/session-status-template.md` | 01-requirements (§2), 03-plan (§2.1), 04-implement (§2.1), 06-retrospect (§2), 下一 iteration 的 00-init |
| project.md | `.claude/context/project.md` | `.claude/templates/project-template.md` | 所有阶段（项目上下文） |
| tech-stack-profile.md | `.claude/context/tech-stack-profile.md` | `.claude/templates/tech-stack-profile-template.md` | 01-requirements (§2), 02-arch-qa (§2.2), 03-plan (§2.3), BA-Stage1 |

### Architect-Stage0

| 文件名 | 完整路径 | 模板 | 被依赖阶段 |
|--------|----------|------|-----------|
| consistency-baseline.md | `.claude/context/consistency-baseline.md` | `.claude/templates/consistency-baseline-template.md` | 01-requirements (§2), 02-arch-qa (§2.2), 04-implement (§2), BA-Stage1 |
| dependencies-overview.md | `.claude/context/dependencies-overview.md` | `.claude/templates/dependencies-overview-template.md` | 02-arch-qa (§2.2) |

### Analyst-Stage0

| 文件名 | 完整路径 | 模板 | 被依赖阶段 |
|--------|----------|------|-----------|
| feature.md | `.claude/iterations/sprint-latest/feature.md` | `.claude/templates/feature-template.md` | 01-requirements (§4.2), BA-Stage1, PM-Stage1 |

---

## 阶段1 (/mf-upgrade:01-requirements)

### BA-Stage1

| 文件名 | 完整路径 | 模板 | 被依赖阶段 |
|--------|----------|------|-----------|
| requirements.md | `.claude/iterations/sprint-latest/requirements.md` | `.claude/templates/requirements-template.md` | 02-arch-qa (§2.1), Architect-Stage2, QA-Stage2, PM-Stage1 |
| similarity-analysis-temp.md | `.claude/iterations/sprint-latest/similarity-analysis-temp.md` | - | 内部临时文件 |
| reuse-analysis-temp.md | `.claude/iterations/sprint-latest/reuse-analysis-temp.md` | - | 内部临时文件 |

### PM-Stage1

| 文件名 | 完整路径 | 模板 | 被依赖阶段 |
|--------|----------|------|-----------|
| .review-count | `.claude/iterations/sprint-latest/.review-count` | - | 审查次数追踪 |
| .notifications.log | `.claude/iterations/sprint-latest/.notifications.log` | - | Architect 通知记录 |

---

## 阶段2 (/mf-upgrade:02-arch-qa)

### Architect-Stage2

| 文件名 | 完整路径 | 模板 | 被依赖阶段 |
|--------|----------|------|-----------|
| ADR.md | `.claude/iterations/sprint-latest/ADR.md` | `.claude/templates/adr-template.md` | 03-plan (§2.2), Analyst-Stage3, PM-Stage3, 04-implement (§2), Dev-Stage4 |
| pseudocode/T{NNN}.md | `.claude/iterations/sprint-latest/pseudocode/T{NNN}.md` | - | Dev-Stage4（Task 实现参考）, Analyst-Stage3（Task 详情提取） |

### PM-Audit-Stage2

| 文件名 | 完整路径 | 模板 | 被依赖阶段 |
|--------|----------|------|-----------|
| adr-review.md | `.claude/iterations/sprint-latest/reviews/adr-review.md` | `.claude/templates/adr-review-template.md` | Architecture-Fix-ADR, Architect-Stage2 |
| review-log.md | `.claude/iterations/sprint-latest/reviews/review-log.md` | `.claude/templates/review-log-template.md` | 所有 Agent（问题追踪） |
| .adr-review-round | `.claude/iterations/sprint-latest/reviews/.adr-review-round` | - | 审核轮次计数 |

### Architecture-Fix-ADR

| 文件名 | 完整路径 | 模板 | 被依赖阶段 |
|--------|----------|------|-----------|
| ADR.md（修复后） | `.claude/iterations/sprint-latest/ADR.md` | - | PM-Audit-Stage2（再次审核） |

### QA-Stage2

| 文件名 | 完整路径 | 模板 | 被依赖阶段 |
|--------|----------|------|-----------|
| test-plan.md | `.claude/iterations/sprint-latest/test-plan.md` | `.claude/templates/test-plan-template.md` | 03-plan (§2.3), Analyst-Stage3, QA-Stage4 |
| sprintN-testplan.md | `.claude/testplans/sprintN-testplan.md` | - | 历史存档 |

### PM-Audit-TP-Stage2

| 文件名 | 完整路径 | 模板 | 被依赖阶段 |
|--------|----------|------|-----------|
| testplan-review.md | `.claude/iterations/sprint-latest/reviews/testplan-review.md` | `.claude/templates/test-plan-review-template.md` | QA-Fix-Testplan, QA-Stage2 |
| .testplan-review-round | `.claude/iterations/sprint-latest/reviews/.testplan-review-round` | - | 审核轮次计数 |

### QA-Fix-Testplan

| 文件名 | 完整路径 | 模板 | 被依赖阶段 |
|--------|----------|------|-----------|
| test-plan.md（修复后） | `.claude/iterations/sprint-latest/test-plan.md` | - | PM-Audit-TP-Stage2（再次审核） |

---

## 阶段3 (/mf-upgrade:03-plan)

### Analyst-Stage3

| 文件名 | 完整路径 | 模板 | 被依赖阶段 |
|--------|----------|------|-----------|
| sprint-status.md（草案） | `.claude/iterations/sprint-latest/sprint-status.md` | `.claude/templates/sprint-status-template.md` | PM-Stage3（审核定稿）, Dev-Stage4（领任务） |

### PM-Stage3

| 文件名 | 完整路径 | 模板 | 被依赖阶段 |
|--------|----------|------|-----------|
| sprint-status.md（定稿） | `.claude/iterations/sprint-latest/sprint-status.md` | `.claude/templates/sprint-status-template.md` | 04-implement (§2.1), Dev-Stage4, QA-Stage4 |

---

## 阶段4 (/mf-upgrade:04-implement)

### PM-Stage4

| 文件名 | 完整路径 | 模板 | 被依赖阶段 |
|--------|----------|------|-----------|
| test-report.md | `.claude/iterations/sprint-latest/test-report.md` | `.claude/templates/quality-report-template.md` | 06-retrospect |

### Dev-Stage4（每个 MG）

| 文件名 | 完整路径 | 模板 | 被依赖阶段 |
|--------|----------|------|-----------|
| 源代码 | 按项目结构 | - | Architect-Stage4（Code Review）, QA-Stage4（测试） |
| task-summary/T{NNN}.md | `.claude/iterations/sprint-latest/task-summary/T{NNN}.md` | `.claude/templates/task-summary-template.md` | Architect-Stage4, QA-Stage4, 06-retrospect |
| bugs.md | `.claude/iterations/sprint-latest/bugs.md` | `.claude/templates/bugs-template.md` | Dev-Fix-Stage4, PM-Stage4, 06-retrospect |

### Architect-Stage4（每个 MG 的 Code Review 循环）

| 文件名 | 完整路径 | 模板 | 被依赖阶段 |
|--------|----------|------|-----------|
| code-review-{MG-ID}.md | `.claude/iterations/sprint-latest/reviews/code-review-{MG-ID}.md` | `.claude/templates/code-review-template.md` | Dev-Fix-Stage4, PM-Stage4 |
| test-code-review-{MG-ID}.md | `.claude/iterations/sprint-latest/reviews/test-code-review-{MG-ID}.md` | `.claude/templates/test-code-review-template.md` | QA-Fix-Stage4, PM-Stage4 |
| review-log.md（更新） | `.claude/iterations/sprint-latest/reviews/review-log.md` | `.claude/templates/review-log-template.md` | 所有 Agent |

### QA-Stage4

| 文件名 | 完整路径 | 模板 | 被依赖阶段 |
|--------|----------|------|-----------|
| 自动化测试代码 | `tests/{US-ID}/*.test.js` 等 | - | Test Code Review, 06-retrospect |
| manual-test/*.md | `.claude/iterations/sprint-latest/manual-test/` | `.claude/templates/manual-test-guide-template.md` | Human Test |

### Dev-Fix-Stage4 / QA-Fix-Stage4

| 文件名 | 完整路径 | 模板 | 被依赖阶段 |
|--------|----------|------|-----------|
| 修复后代码 | 按项目结构 | - | 重新提交检查 |
| review-log.md（更新） | `.claude/iterations/sprint-latest/reviews/review-log.md` | `.claude/templates/review-log-template.md` | 问题追踪 |

---

## 阶段5 (/mf-upgrade:05-quality)

### QA-Stage5

| 文件名 | 完整路径 | 模板 | 被依赖阶段 |
|--------|----------|------|-----------|
| quality-report.md | `.claude/iterations/sprint-latest/quality-report.md` | `.claude/templates/quality-report-template.md` | 06-retrospect |
| bug-log/auto-YYYY-MM-DD.md | `.claude/iterations/sprint-latest/bug-log/auto-YYYY-MM-DD.md` | ❌ 缺失（需创建 bug-log-template.md） | Dev-Stage5, PM-Stage5 |
| bug-log/manual-YYYY-MM-DD.md | `.claude/iterations/sprint-latest/bug-log/manual-YYYY-MM-DD.md` | ❌ 缺失（需创建 bug-log-template.md） | Dev-Stage5, PM-Stage5 |
| test-results/regression-YYYY-MM-DD.log | `.claude/iterations/sprint-latest/test-results/regression-YYYY-MM-DD.log` | - | 06-retrospect |
| test-results/manual-test-guide.md | `.claude/iterations/sprint-latest/test-results/manual-test-guide.md` | `.claude/templates/manual-test-guide-template.md` | Human Test |

### PM-Stage5

| 文件名 | 完整路径 | 模板 | 被依赖阶段 |
|--------|----------|------|-----------|
| 缺陷决策记录 | `.claude/iterations/sprint-latest/sprint-status.md`（更新） | `.claude/templates/sprint-status-template.md` | Dev-Stage5, QA-Stage5 |

### Dev-Stage5

| 文件名 | 完整路径 | 模板 | 被依赖阶段 |
|--------|----------|------|-----------|
| 修复后代码 | 按项目结构 | - | QA-Stage5（重新测试） |
| bug-log（更新） | `.claude/iterations/sprint-latest/bugs.md` | `.claude/templates/bugs-template.md` | QA-Stage5 |

---

## 阶段6 (/mf-upgrade:06-retrospect)

### Coach-Stage6

| 文件名 | 完整路径 | 模板 | 被依赖阶段 |
|--------|----------|------|-----------|
| iteration-retrospective.md | `.claude/iterations/sprint-latest/iteration-retrospective.md` | `.claude/templates/iteration-retrospective-template.md` | 下一 iteration 的 00-init（输入上下文） |
| evolution-proposal.md | `.claude/evolution-proposals/upgrade-YYYY-MM-DD-title.md` | `.claude/templates/evolution-proposal-template.md` | PM-Stage6（审批） |

### Guardian-Stage6

| 文件名 | 完整路径 | 模板 | 被依赖阶段 |
|--------|----------|------|-----------|
| 验证报告 | `.claude/iterations/sprint-latest/验证报告.md` | - | PM-Stage6（决策） |

### PM-Stage6

| 文件名 | 完整路径 | 模板 | 被依赖阶段 |
|--------|----------|------|-----------|
| CHANGELOG.md | `CHANGELOG.md`（更新） | - | 全局可读 |
| HARNESS_VERSION.md | `.claude/HARNESS_VERSION.md`（更新） | - | 所有阶段（版本参考） |
| reports/PROJECT_STATUS.md | `.claude/reports/PROJECT_STATUS.md` | `.claude/templates/project-status-template.md` | 全局可读，下一 iteration 参考 |

---

## 全局文件（不隶属于特定 iteration）

| 文件名 | 完整路径 | 说明 | 被依赖阶段 |
|--------|----------|------|-----------|
| mefan-log.md | `.claude/iterations/mefan-log.md` | 全局框架运行日志 | 所有阶段（日志追加） |
| violations.json | `.claude/iterations/sprint-latest/violations.json` | Hook 拦截记录 | 06-retrospect |
| graphify-out/ | `graphify-out/` | 代码图谱 | 阶段0-6（分析查询） |

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
| 测试计划存档 | `.claude/testplans/` |
| 单次迭代 | `.claude/iterations/sprint-latest/` |
| 迭代内 reviews | `.claude/iterations/sprint-latest/reviews/` |
| 迭代内 task-summary | `.claude/iterations/sprint-latest/task-summary/` |
| 迭代内 pseudocode | `.claude/iterations/sprint-latest/pseudocode/` |
| 迭代内 manual-test | `.claude/iterations/sprint-latest/manual-test/` |

---

## 模板文件使用情况汇总（按首字母排序）

| 模板文件 | 是否被使用 | 使用者 |
|---------|-----------|--------|
| adr-review-template.md | ✅ | pm-audit-stage2.md |
| adr-template.md | ✅ | architect-stage2.md |
| bugs-template.md | ✅ | qa-stage4.md (bugs.md), dev-stage5.md (更新 bugs.md) |
| bug-log-template.md | ❌ | **缺失** - qa-stage5.md 引用但文件不存在 |
| code-review-template.md | ✅ | architect-stage4.md |
| consistency-baseline-template.md | ✅ | architect-stage0.md |
| dependencies-overview-template.md | ✅ | architect-stage0.md |
| evolution-proposal-template.md | ✅ | coach-stage6.md |
| feature-template.md | ✅ | analyst-stage0.md |
| human-gate-report-template.md | ❌ | 未被使用 |
| iteration-retrospective-template.md | ✅ | coach-stage6.md |
| log-entry-template.md | ❌ | 未被使用（使用 hooks/log-event.sh 替代） |
| manual-test-guide-template.md | ✅ | qa-stage4.md |
| project-template.md | ✅ | pm-stage0.md |
| project-status-template.md | ✅ | pm-stage6.md |
| quality-report-template.md | ✅ | pm-stage4.md (生成 test-report.md) |
| requirements-template.md | ✅ | ba-stage1.md |
| review-log-template.md | ✅ | pm-audit-stage2.md, architect-stage4.md |
| session-status-template.md | ✅ | pm-stage0.md |
| sprint-status-template.md | ✅ | analyst-stage3.md |
| sub-feature-template.md | ❌ | 未被使用（内容已内联到 requirements-template.md） |
| task-summary-template.md | ✅ | dev-stage4.md |
| tech-stack-profile-template.md | ✅ | pm-stage0.md |
| test-code-review-template.md | ✅ | architect-stage4.md |
| test-plan-review-template.md | ✅ | pm-audit-testplan-stage2.md |
| test-plan-template.md | ✅ | qa-stage2.md |
| user-story-template.md | ❌ | 未被使用（内容已内联到 requirements-template.md） |

---

## 项目配置文件

| 文件 | 路径 | 说明 |
|------|------|------|
| project.conf | `.claude/project.conf` | 定义 ROOT 等环境变量，供 shell 脚本 source 引用 |

---

## 自动生成的 Skill 文件

> 以下 Skill 文件由 Architect-Stage0 在生成 consistency-baseline.md 时调用 `code-pattern-extractor.sh` 自动生成
> **生成时机**：阶段 0，Architect Agent 执行一致性基线提取时
> **调用方式**：`bash .claude/skills/code-pattern-extractor.sh --all`

| Skill 文件 | 生成方式 | 用途 |
|-----------|---------|------|
| project-tech-naming.md | Architect 调用时生成 | 变量/函数/类命名规范 |
| project-tech-frontend.md | Architect 调用时生成 | 前端框架模式（React/Redux/Ant Design/Router） |
| project-tech-backend.md | Architect 调用时生成 | 后端框架模式（Express/FastAPI/Spring） |
| project-middleware.md | Architect 调用时生成 | 中间件配置和注册顺序 |
| architecture-pattern.md | Architect 调用时生成 | 项目分层结构和依赖规则 |
| directory-structure.md | Architect 调用时生成 | 目录组织规范 |
| project-domain.md | Architect 调用时生成（需人工补充） | 业务领域 Skill |

**使用方式**：
```bash
# 在 Architect-Stage0 执行时调用
bash .claude/skills/code-pattern-extractor.sh --all

# 或按类型单独提取
bash .claude/skills/code-pattern-extractor.sh --type tech-frontend
bash .claude/skills/code-pattern-extractor.sh --type tech-backend
```

---

## 断链检测报告

### 依赖断链

1. **ADR → test-plan**: Architect-Stage2 的 ADR.md 中应包含对 test-plan.md 的引用，但当前 ADR 模板中没有明确标注 test-plan 关联
2. **sprint-status.md → task-summary**: analyst-stage3.md 生成 sprint-status.md 时，应明确关联 task-summary/ 目录下的文件，但路径未在模板中标注
3. **pseudocode/ 目录**: architect-stage2.md 提到生成 pseudocode/T-{NNN}.md 文件，但没有 pseudocode-template.md
4. **testplans/ 目录**: qa-stage2.md 保存历史到 `.claude/testplans/`，但该目录创建未在 command 中体现

### 模板断链

| 模板 | 状态 |
|-----|------|
| sub-feature-template.md | 内容已内联到 requirements-template.md，不需单独使用 |
| user-story-template.md | 内容已内联到 requirements-template.md，不需单独使用 |
| human-gate-report-template.md | 阶段4 Human Gate 触发时使用，但生成逻辑分散 |
| log-entry-template.md | 使用 hooks/log-event.sh 替代，无需单独生成文件 |
| bug-log-template.md | ❌ **缺失** - qa-stage5.md、mf-upgrade:05-quality.md 引用此模板，但该文件不存在。实际应使用 `bugs-template.md` 或需新建 bug-log-template.md |