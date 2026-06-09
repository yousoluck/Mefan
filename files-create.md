# 文件创建清单 (Files Created by Command)

> 本文件记录每个 Command/Agent 创建的所有文件，供依赖检查用。
> **更新于 2026-06-08**：增加"如何生成"和"数据来源"维度，补充遗漏文件
> **完整审计报告**：见 `docs/product/framework-audit-2026-06-08.md`

---

## 格式说明

| 列名 | 取值范围 | 说明 |
|------|---------|------|
| **文件名** | 文件名（含扩展名） | |
| **完整路径** | 相对 `$ROOT` 的完整路径 | `$ROOT` 从 `.claude/project.conf` 加载 |
| **模板** | 模板文件名（含路径）或 `-` | |
| **生成方式** | `动态-A` / `复制-B` / `混合-C` / `硬编码-D` / `手动-E` | 新增维度 |
| **数据来源** | `graph.json` / `源码扫描` / `上游文档` / `graphify query + bash fallback` / `人工补充` / `-` | 新增维度 |
| **被依赖阶段** | 引用该文件的阶段 ID 列表 | |
| **问题备注** | `需重构` / `已废弃` / `路径不一致` / `-` | 可选 |

### 生成方式分类标准

| 模式 | 描述 | 典型实现 |
|------|------|---------|
| **动态-A** | AI 分析上游数据 + Write 工具按模板格式填充真实内容 | `query_plan.md → results.json → AI Write` |
| **复制-B** | `cp $ROOT/.claude/templates/xxx.md` 直接复制 + `sed` 替换少量占位符 | ⚠️ 模板字段多为空 |
| **混合-C** | 部分字段动态生成 + 部分 heredoc 模板占位 | `cat << EOF` + sed |
| **硬编码-D** | heredoc 写死整个文件，无项目数据 | `cat << 'EOF'` |
| **手动-E** | 人工/PM 维护，通过 Edit 工具更新 | 增量追加 |

### 数据来源分类

| 标识 | 说明 |
|------|------|
| `graph.json` | `graphify-out/graph.json`（已重构，**原 `knowledge.grap` 已废弃**） |
| `源码扫描` | grep/find 扫描项目源码 |
| `上游文档` | ADR/requirements/sprint-status 等前序阶段产出 |
| `graphify query + bash fallback` | 三级降级查询 |
| `人工补充` | 字段缺失时由 AI/PM 人工填入 |

---

## 阶段0 (/mf-upgrade:00-init)

### PM-Stage0

| 文件名 | 完整路径 | 模板 | 生成方式 | 数据来源 | 被依赖阶段 | 问题备注 |
|--------|----------|------|---------|---------|----------|---------|
| session-status.md | `.claude/iterations/session-status.md` | - | 混合-C | heredoc 模板 + sed 占位符 | 01-requirements (§2), 03-plan (§2.1), 04-implement (§2.1), 06-retrospect (§2), 下一 iteration 的 00-init | - |
| project.md | `.claude/context/project.md` | - | 动态-A ✅ | graph.json + results.json | 所有阶段（项目上下文） | 模式 C 重构版（2026-06-06） |
| tech-stack-profile.md | `.claude/context/tech-stack-profile.md` | - | 动态-A ✅ | graph.json + results.json | 01-requirements (§2), 02-arch-qa (§2.2), 03-plan (§2.3), BA-Stage1 | 模式 C 重构版（2026-06-06） |
| feature-elements.md | `.claude/context/feature-elements.md` | - | 动态-A ✅ | graph.json + results.json | 02-arch-qa (§2.2), BA-Stage1, 04-implement (§2) | 模式 C 重构版（2026-06-06） |
| **query_plan.md** 🆕 | `.claude/context/query_plan.md` | `query-plan-template.md` | 动态-A ✅ | 模板解析 + 词表 + AI 设计 query | pm-stage0 §0.3, arch-stage0 §2.4 | N-rows 重构后约 110-130 行 |
| **results.json** 🆕 | `.claude/context/results.json` | `results-json-schema.md` | 动态-A ✅ | graphify query + bash fallback | pm-stage0 §0.4, arch-stage0 §2.5 | SCHEMA_VERSION 2.1.0 |

### Architect-Stage0

| 文件名 | 完整路径 | 模板 | 生成方式 | 数据来源 | 被依赖阶段 | 问题备注 |
|--------|----------|------|---------|---------|----------|---------|
| consistency-baseline.md | `.claude/context/consistency-baseline.md` | `consistency-baseline-template.md` | 动态-A ✅ | graph.json + results.json | 01-requirements (§2), 02-arch-qa (§2.2), 04-implement (§2), BA-Stage1 | 17 章节 + evidence 引用 |
| Skills（L1-L5 全层） | `.claude/skills/project-*/` | - | 动态-A ✅ | graph.json + 模板解析 | 04-implement (§2), 02-arch-qa | superpowers:writing-skills 套用 |

### Analyst-Stage0

| 文件名 | 完整路径 | 模板 | 生成方式 | 数据来源 | 被依赖阶段 | 问题备注 |
|--------|----------|------|---------|---------|----------|---------|
| feature.md | `.claude/iterations/sprint-latest/feature.md` | `feature-template.md` | 混合-C/A | graphify query + 澄清对话 | 01-requirements (§4.2), BA-Stage1, PM-Stage1 | 应统一为动态-A |

---

## 阶段1 (/mf-upgrade:01-requirements)

### BA-Stage1

| 文件名 | 完整路径 | 模板 | 生成方式 | 数据来源 | 被依赖阶段 | 问题备注 |
|--------|----------|------|---------|---------|----------|---------|
| requirements.md | `.claude/iterations/sprint-latest/requirements.md` | `requirements-template.md` | 硬编码-D ⚠️ | heredoc + 部分 graphify | 02-arch-qa (§2.1), Architect-Stage2, QA-Stage2, PM-Stage1 | **建议重构为动态-A**（参考 pm-stage0 模式 C） |
| similarity-analysis-temp.md | `.claude/iterations/sprint-latest/similarity-analysis-temp.md` | - | 硬编码-D | heredoc 写死 | 内部临时文件 | 可接受 |
| reuse-analysis-temp.md | `.claude/iterations/sprint-latest/reuse-analysis-temp.md` | - | 硬编码-D | heredoc 写死 | 内部临时文件 | 可接受 |

### PM-Stage1

| 文件名 | 完整路径 | 模板 | 生成方式 | 数据来源 | 被依赖阶段 | 问题备注 |
|--------|----------|------|---------|---------|----------|---------|
| .review-count | `.claude/iterations/sprint-latest/.review-count` | - | 手动-E | sed/echo | 审查次数追踪 | - |
| .notifications.log | `.claude/iterations/sprint-latest/.notifications.log` | - | 手动-E | echo 追加 | Architect 通知记录 | - |

---

## 阶段2 (/mf-upgrade:02-arch-qa)

### Architect-Stage2

| 文件名 | 完整路径 | 模板 | 生成方式 | 数据来源 | 被依赖阶段 | 问题备注 |
|--------|----------|------|---------|---------|----------|---------|
| ADR.md | `.claude/iterations/sprint-latest/ADR.md` | `adr-template.md` | 动态-A ✅ | graph.json + requirements.md | 03-plan (§2.2), Analyst-Stage3, PM-Stage3, 04-implement (§2), Dev-Stage4 | 17 章节设计要素 |
| pseudocode/T{NNN}.md | `.claude/iterations/sprint-latest/pseudocode/T{NNN}.md` | - | 混合-C/D | 部分 heredoc，部分 AI 写 | Dev-Stage4, Analyst-Stage3 | - |

### PM-Audit-Stage2

| 文件名 | 完整路径 | 模板 | 生成方式 | 数据来源 | 被依赖阶段 | 问题备注 |
|--------|----------|------|---------|---------|----------|---------|
| adr-review.md | `.claude/iterations/sprint-latest/reviews/adr-review.md` | `adr-review-template.md` | **复制-B** ❌ | **仅 sed 替换** | Architecture-Fix-ADR, Architect-Stage2 | **需重构为动态-A** |
| review-log.md | `.claude/iterations/sprint-latest/reviews/review-log.md` | `review-log-template.md` | **复制-B** ❌ | **仅 sed 追加** | 所有 Agent | **需重构为动态-A** |
| .adr-review-round | `.claude/iterations/sprint-latest/reviews/.adr-review-round` | - | 手动-E | echo 数字 | 审核轮次计数 | - |

### Architecture-Fix-ADR

| 文件名 | 完整路径 | 模板 | 生成方式 | 数据来源 | 被依赖阶段 | 问题备注 |
|--------|----------|------|---------|---------|----------|---------|
| ADR.md（修复后） | `.claude/iterations/sprint-latest/ADR.md` | - | 动态-A ✅ | AI Edit/Write（基于审核反馈） | PM-Audit-Stage2 | - |

### QA-Stage2

| 文件名 | 完整路径 | 模板 | 生成方式 | 数据来源 | 被依赖阶段 | 问题备注 |
|--------|----------|------|---------|---------|----------|---------|
| test-plan.md | `.claude/iterations/sprint-latest/test-plan.md` | `test-plan-template.md` | 动态-A ✅ | graph.json + ADR + requirements | 03-plan (§2.3), Analyst-Stage3, QA-Stage4 | - |
| sprintN-testplan.md | `.claude/testplans/sprintN-testplan.md` | - | 手动-E | cp test-plan.md | 历史存档 | - |

### PM-Audit-TP-Stage2

| 文件名 | 完整路径 | 模板 | 生成方式 | 数据来源 | 被依赖阶段 | 问题备注 |
|--------|----------|------|---------|---------|----------|---------|
| testplan-review.md | `.claude/iterations/sprint-latest/reviews/testplan-review.md` | `test-plan-review-template.md` | **复制-B** ❌ | **仅 sed 替换** | QA-Fix-Testplan, QA-Stage2 | **需重构为动态-A** |
| .testplan-review-round | `.claude/iterations/sprint-latest/reviews/.testplan-review-round` | - | 手动-E | echo 数字 | 审核轮次计数 | - |

### QA-Fix-Testplan

| 文件名 | 完整路径 | 模板 | 生成方式 | 数据来源 | 被依赖阶段 | 问题备注 |
|--------|----------|------|---------|---------|----------|---------|
| test-plan.md（修复后） | `.claude/iterations/sprint-latest/test-plan.md` | - | 动态-A ✅ | AI Edit/Write | PM-Audit-TP-Stage2 | - |

---

## 阶段3 (/mf-upgrade:03-plan)

### Analyst-Stage3

| 文件名 | 完整路径 | 模板 | 生成方式 | 数据来源 | 被依赖阶段 | 问题备注 |
|--------|----------|------|---------|---------|----------|---------|
| sprint-status.md（草案） | `.claude/iterations/sprint-latest/sprint-status.md` | `sprint-status-template.md` | **复制-B** ❌ | **cp 模板 + sed** | PM-Stage3, Dev-Stage4 | **需重构为动态-A** |

### PM-Stage3

| 文件名 | 完整路径 | 模板 | 生成方式 | 数据来源 | 被依赖阶段 | 问题备注 |
|--------|----------|------|---------|---------|----------|---------|
| sprint-status.md（定稿） | `.claude/iterations/sprint-latest/sprint-status.md` | - | 混合-C | Read 草案 + 调整 | 04-implement (§2.1), Dev-Stage4, QA-Stage4 | - |

---

## 阶段4 (/mf-upgrade:04-implement)

### PM-Stage4

| 文件名 | 完整路径 | 模板 | 生成方式 | 数据来源 | 被依赖阶段 | 问题备注 |
|--------|----------|------|---------|---------|----------|---------|
| test-report.md | `.claude/iterations/sprint-latest/test-report.md` | `quality-report-template.md` | 动态-A ✅ | 测试结果 + 模板 | 06-retrospect | - |

### Dev-Stage4（每个 MG）

| 文件名 | 完整路径 | 模板 | 生成方式 | 数据来源 | 被依赖阶段 | 问题备注 |
|--------|----------|------|---------|---------|----------|---------|
| 源代码 | 按项目结构 | - | 动态-A ✅ | ADR 伪代码 + TDD | Architect-Stage4, QA-Stage4 | - |
| task-summary/T{NNN}.md | `.claude/iterations/sprint-latest/task-summary/T{NNN}.md` | `task-summary-template.md` | 动态-A ✅ | AI Write 工具（操作 3.7） | Architect-Stage4, QA-Stage4, 06-retrospect | H9 修复后落地（2026-06-06） |
| bugs.md | `.claude/iterations/sprint-latest/bugs.md` | `bugs-template.md` | 动态-A ✅ | sed 追加 + 模板 | Dev-Fix-Stage4, PM-Stage4, 06-retrospect | - |

### Architect-Stage4（每个 MG 的 Code Review 循环）

| 文件名 | 完整路径 | 模板 | 生成方式 | 数据来源 | 被依赖阶段 | 问题备注 |
|--------|----------|------|---------|---------|----------|---------|
| code-review-{MG-ID}.md | `.claude/iterations/sprint-latest/reviews/code-review-{MG-ID}.md` | `code-review-template.md` | 动态-A ✅ | git diff + ADR + subagent | Dev-Fix-Stage4, PM-Stage4 | - |
| test-code-review-{MG-ID}.md | `.claude/iterations/sprint-latest/reviews/test-code-review-{MG-ID}.md` | `test-code-review-template.md` | 动态-A ✅ | git diff + ADR + subagent | QA-Fix-Stage4, PM-Stage4 | - |
| review-log.md（更新） | `.claude/iterations/sprint-latest/reviews/review-log.md` | - | 手动-E | sed 追加 | 所有 Agent | - |

### QA-Stage4

| 文件名 | 完整路径 | 模板 | 生成方式 | 数据来源 | 被依赖阶段 | 问题备注 |
|--------|----------|------|---------|---------|----------|---------|
| 自动化测试代码 | `tests/{US-ID}/*.test.js` 等 | - | 动态-A ✅ | ADR + TDD | Test Code Review, 06-retrospect | - |
| manual-test/*.md | `.claude/iterations/sprint-latest/manual-test/` | `manual-test-guide-template.md` | 混合-C | 部分 AI Write + 模板 | Human Test | - |

### Dev-Fix-Stage4 / QA-Fix-Stage4

| 文件名 | 完整路径 | 模板 | 生成方式 | 数据来源 | 被依赖阶段 | 问题备注 |
|--------|----------|------|---------|---------|----------|---------|
| 修复后代码 | 按项目结构 | - | 动态-A ✅ | Edit 工具 | 重新提交检查 | - |
| review-log.md（更新） | `.claude/iterations/sprint-latest/reviews/review-log.md` | - | 手动-E | sed 追加 | 问题追踪 | - |

### **mg-state.json** 🆕

| 文件名 | 完整路径 | 模板 | 生成方式 | 数据来源 | 被依赖阶段 | 问题备注 |
|--------|----------|------|---------|---------|----------|---------|
| mg-state.json | `.claude/iterations/sprint-latest/mg-state.json` | - | 手动-E | `hooks/check-state-machine.sh` 写入 | 04-implement (7 状态流转) | **遗漏，应补充** |

---

## 阶段5 (/mf-upgrade:05-quality)

### QA-Stage5

| 文件名 | 完整路径 | 模板 | 生成方式 | 数据来源 | 被依赖阶段 | 问题备注 |
|--------|----------|------|---------|---------|----------|---------|
| quality-report.md | `.claude/iterations/sprint-latest/quality-report.md` | `quality-report-template.md` | 动态-A ✅ | 7 门禁 + 测试结果 | 06-retrospect | - |
| bug-log/auto-YYYY-MM-DD.md | `.claude/iterations/sprint-latest/bug-log/auto-YYYY-MM-DD.md` | - | 动态-A ✅ | 测试结果 + 模板 | Dev-Stage5, PM-Stage5 | ⚠️ bug-log-template.md 缺失（见下） |
| bug-log/manual-YYYY-MM-DD.md | `.claude/iterations/sprint-latest/bug-log/manual-YYYY-MM-DD.md` | - | 动态-A ✅ | 人工测试结果 + 模板 | Dev-Stage5, PM-Stage5 | ⚠️ bug-log-template.md 缺失 |
| test-results/regression-YYYY-MM-DD.log | `.claude/iterations/sprint-latest/test-results/regression-YYYY-MM-DD.log` | - | 手动-E | 测试命令输出 | 06-retrospect | - |
| test-results/manual-test-guide.md | `.claude/iterations/sprint-latest/test-results/manual-test-guide.md` | `manual-test-guide-template.md` | 动态-A ✅ | 实现清单 + 受影响模块 | Human Test | - |

### PM-Stage5

| 文件名 | 完整路径 | 模板 | 生成方式 | 数据来源 | 被依赖阶段 | 问题备注 |
|--------|----------|------|---------|---------|----------|---------|
| sprint-status.md（更新） | `.claude/iterations/sprint-latest/sprint-status.md` | - | 动态-A ✅ | Read + Edit | Dev-Stage5, QA-Stage5 | - |

### Dev-Stage5

| 文件名 | 完整路径 | 模板 | 生成方式 | 数据来源 | 被依赖阶段 | 问题备注 |
|--------|----------|------|---------|---------|----------|---------|
| 修复后代码 | 按项目结构 | - | 动态-A ✅ | Edit 工具 | QA-Stage5 | - |
| bugs.md（更新） | `.claude/iterations/sprint-latest/bugs.md` | - | 动态-A ✅ | Edit 工具 | QA-Stage5 | - |

---

## 阶段6 (/mf-upgrade:06-retrospect)

### Coach-Stage6

| 文件名 | 完整路径 | 模板 | 生成方式 | 数据来源 | 被依赖阶段 | 问题备注 |
|--------|----------|------|---------|---------|----------|---------|
| iteration-retrospective.md | `.claude/iterations/sprint-latest/iteration-retrospective.md` | `iteration-retrospective-template.md` | 动态-A ✅ | grep mefan-log.md + AI Write | 下一 iteration 的 00-init | - |
| evolution-proposal.md | `.claude/evolution-proposals/upgrade-YYYY-MM-DD-title.md` | `evolution-proposal-template.md` | 动态-A ✅ | 模式识别 + superpowers:writing-skills | PM-Stage6 | - |

### Guardian-Stage6

| 文件名 | 完整路径 | 模板 | 生成方式 | 数据来源 | 被依赖阶段 | 问题备注 |
|--------|----------|------|---------|---------|----------|---------|
| 验证报告 | `.claude/iterations/sprint-latest/验证报告.md` | - | 动态-A ✅ | 报告 + AI Write | PM-Stage6 | - |

### PM-Stage6

| 文件名 | 完整路径 | 模板 | 生成方式 | 数据来源 | 被依赖阶段 | 问题备注 |
|--------|----------|------|---------|---------|----------|---------|
| CHANGELOG.md | `CHANGELOG.md`（根目录） ⚠️ | - | 动态-A ✅ | Edit 工具 | 全局可读 | **路径不一致**（部分引用 .claude/CHANGELOG.md） |
| HARNESS_VERSION.md | `.claude/HARNESS_VERSION.md` ⚠️ | - | 动态-A ✅ | Edit 工具 | 所有阶段 | **路径不一致**（arch-stage0 引用 $ROOT/HARNESS_VERSION.md） |
| reports/PROJECT_STATUS.md | `reports/PROJECT_STATUS.md`（根目录） | `project-status-template.md` | 动态-A ✅ | Edit 工具 | 全局可读，下一 iteration 参考 | - |

---

## 全局文件（不隶属于特定 iteration）

| 文件名 | 完整路径 | 模板 | 生成方式 | 数据来源 | 被依赖阶段 | 问题备注 |
|--------|----------|------|---------|---------|----------|---------|
| mefan-log.md | `.claude/iterations/mefan-log.md` | - | 手动-E | hooks/log-event.sh 追加 | 所有阶段（日志追加） | - |
| conversation-log.md 🆕 | `logs/conversation-log.md`（根目录） | - | 手动-E | hooks/conversation-log.sh 追加 | 跨 session 对话记录 | **遗漏，应补充** |
| ~~violations.json~~ | `.claude/iterations/sprint-latest/violations.json` | - | - | - | - | **已废弃**：6 个 hook 全部 stdout + mefan-log.md，无 violations.json（详见 hook-vs-guardian.md） |
| graphify-out/ | `graphify-out/` | - | 动态-A | graphify 工具生成 | 阶段0-6（分析查询） | - |
| HARNESS_VERSION.md ⚠️ | `HARNESS_VERSION.md`（根目录）或 `.claude/HARNESS_VERSION.md` | - | 动态-A | Edit 工具 | 所有阶段 | **路径不一致需统一** |

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
| 迭代内 bug-log | `.claude/iterations/sprint-latest/bug-log/` |
| 迭代内 test-results | `.claude/iterations/sprint-latest/test-results/` |
| 迭代内 mg-state | `.claude/iterations/sprint-latest/mg-state.json` |
| 迭代内 query-plan | `.claude/context/query_plan.md` |
| 迭代内 results | `.claude/context/results.json` |

---

## 模板文件使用情况汇总（按首字母排序）

| 模板文件 | 是否被使用 | 使用者 | 生成方式 |
|---------|-----------|--------|---------|
| adr-review-template.md | ✅ | pm-audit-stage2.md | 复制-B ⚠️ |
| adr-template.md | ✅ | architect-stage2.md | 动态-A |
| bugs-template.md | ✅ | qa-stage4.md (bugs.md), dev-stage5.md (更新 bugs.md) | 动态-A |
| **bug-log-template.md** | ❌ | **缺失** - qa-stage5.md 引用但文件不存在 | - |
| code-review-template.md | ✅ | architect-stage4.md | 动态-A |
| consistency-baseline-template.md | ✅ | architect-stage0.md | 动态-A |
| dependencies-overview-template.md | ❌ | 已废弃（graphify 可直接查询依赖，无须独立文档） | - |
| evolution-proposal-template.md | ✅ | coach-stage6.md | 动态-A |
| feature-elements-template.md | ✅ | pm-stage0.md | 动态-A |
| feature-template.md | ✅ | analyst-stage0.md | 混合-C/A |
| human-gate-report-template.md | ❌ | 未被使用 | - |
| iteration-retrospective-template.md | ✅ | coach-stage6.md | 动态-A |
| log-entry-template.md | ❌ | 未被使用（使用 hooks/log-event.sh 替代） | - |
| manual-test-guide-template.md | ✅ | qa-stage4.md, qa-stage5.md | 动态-A |
| project-status-template.md | ✅ | pm-stage6.md | 动态-A |
| project-template.md | ✅ | pm-stage0.md | 动态-A |
| quality-report-template.md | ✅ | pm-stage4.md (生成 test-report.md), qa-stage5.md (生成 quality-report.md) | 动态-A |
| query-dsl-cheatsheet.md ✅ | ✅ | arch-stage0.md, pm-stage0.md | 参考文档 |
| query-plan-template.md ✅ | ✅ | arch-stage0.md, pm-stage0.md | 动态-A |
| requirements-template.md | ✅ | ba-stage1.md | 硬编码-D ⚠️ |
| results-json-schema.md ✅ | ✅ | arch-stage0.md, pm-stage0.md | Schema 参考 |
| review-log-template.md | ✅ | pm-audit-stage2.md, architect-stage4.md | 复制-B ⚠️ |
| session-status-template.md | ✅ | pm-stage0.md | 混合-C |
| sprint-status-template.md | ✅ | analyst-stage3.md | 复制-B ⚠️ |
| sub-feature-template.md | ❌ | 未被使用（内容已内联到 requirements-template.md） | - |
| task-summary-template.md | ✅ | dev-stage4.md | 动态-A |
| tech-stack-profile-template.md | ✅ | pm-stage0.md | 动态-A |
| test-code-review-template.md | ✅ | architect-stage4.md | 动态-A |
| test-plan-review-template.md | ✅ | pm-audit-testplan-stage2.md | 复制-B ⚠️ |
| test-plan-template.md | ✅ | qa-stage2.md | 动态-A |
| user-story-template.md | ❌ | 未被使用（内容已内联到 requirements-template.md） | - |

> ✅ = 2026-06-08 新增/确认条目

---

## 项目配置文件

| 文件 | 路径 | 说明 |
|------|------|------|
| project.conf | `.claude/project.conf` | 定义 ROOT / GRAPHIFY_OUT / SKILLS_DIR / TEMPLATE_DIR，供 shell 脚本 source 引用 |

**当前 project.conf 变量清单**：
```bash
export ROOT=/mnt/d/pycharmprojects/Mefan
export GRAPHIFY_OUT="$ROOT/graphify-out"
export SKILLS_DIR="$ROOT/.claude/skills"
export TEMPLATE_DIR="$ROOT/.claude/templates"
```

**建议扩充变量**（重构 1 计划）：
```bash
export SCENARIO="upgrade"              # 当前硬编码于多个 agent
export SPRINT_LATEST_DIR="$ROOT/.claude/iterations/sprint-latest"
export MGFAN_LOG_DIR="$ROOT/.claude/iterations"
export REVIEWS_DIR="$ROOT/.claude/iterations/sprint-latest/reviews"
export TASK_SUMMARY_DIR="$ROOT/.claude/iterations/sprint-latest/task-summary"
```

---

## 模式 B（复制模板）agent 重构优先级

| 优先级 | Agent | 输出文件 | 引用位置 | 重构方案 |
|--------|-------|---------|---------|---------|
| **P0** | `pm-audit-stage2.md` | adr-review.md | L86 | 仿 arch-stage0 模式 C：query_plan.md → results.json → AI Write |
| **P0** | `pm-audit-stage2.md` | review-log.md | L384 | 同上 |
| **P0** | `pm-audit-testplan-stage2.md` | testplan-review.md | L86 | 同上 |
| **P0** | `pm-audit-testplan-stage2.md` | review-log.md | L353 | 同上 |
| **P0** | `analyst-stage3.md` | sprint-status.md | L166 | 仿 arch-stage0 模式 C |

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
| **bug-log-template.md** | ❌ **缺失** - qa-stage5.md、mf-upgrade:05-quality.md 引用此模板，但该文件不存在。实际应使用 `bugs-template.md` 或需新建 bug-log-template.md |

### 路径断链 🆕

| 路径 | 状态 |
|------|------|
| HARNESS_VERSION.md | ❌ **路径不一致** - pm-stage6 引用 `.claude/HARNESS_VERSION.md`，arch-stage0 L138 引用 `$ROOT/HARNESS_VERSION.md`（根目录） |
| CHANGELOG.md | ⚠️ **路径不一致** - 大部分引用根目录，files-create.md 标注"根目录"，但 `.claude/docs/` 中可能有副本 |
| violations.json | ❌ **已废弃** - 6 个 hook 全部 stdout + mefan-log.md，无 violations.json 文件 |
| knowledge.grap | ❌ **已废弃** - 60+ 处引用待重构，详见 `framework-audit-2026-06-08.md` §2 |

---

## 2026-06-08 审计更新摘要

1. **新增维度**：`生成方式`（5 分类）+ `数据来源`（5 分类）+ `问题备注`
2. **补充文件** 🆕：
   - `query_plan.md`（pm-stage0 §0.3 + arch-stage0 §2.4）
   - `results.json`（pm-stage0 §0.4 + arch-stage0 §2.5）
   - `mg-state.json`（check-state-machine.sh 维护）
   - `conversation-log.md`（hooks/conversation-log.sh 维护）
3. **标记问题** ⚠️：
   - 5 个 agent 模式 B（复制模板）：pm-audit-stage2 × 2、pm-audit-testplan-stage2 × 2、analyst-stage3 × 1
   - 1 个 agent 模式 D（硬编码）：ba-stage1
   - 路径不一致：HARNESS_VERSION.md, CHANGELOG.md
   - 已废弃：violations.json, knowledge.grap（53+ 处）
4. **完整审计报告**：`docs/product/framework-audit-2026-06-08.md`

---

*最后更新：2026-06-08（增加"如何生成"维度 + 补充遗漏文件 + 路径一致性审计）*
