# Superpowers Integration Contract
- type: guideline
- severity: info

## Purpose

文档化 mefan 框架与 `superpowers` 插件（v5.1.0）的集成合约，包括：

1. Skill 加载机制（agent frontmatter `Skill` tool）
2. 调用点（哪个 agent 调哪个 skill）
3. 边界（不集成哪些 skill 及原因）
4. Code Review context isolation 方案（**方案 B**）
5. 失败回退（Skill tool 不可用时）

## 加载机制

### Agent 加载 superpowers skill 的方式

**唯一合法方式**：在 agent frontmatter 的 `tools:` 数组中声明 `Skill` 工具，然后在 agent 操作步骤中通过 `Skill` tool 显式调用。

```yaml
---
name: dev-stage4
tools: [Read, Write, Bash, Grep, Glob, Edit, TaskCreate, TaskUpdate, TaskList, TaskGet, Skill]
---
```

```markdown
## 操作 3：实现代码

调用 superpowers TDD 流程：
> **Skill tool invocation**: `skill="superpowers:test-driven-development"`
```

**禁止**：
- 复制 superpowers skill 内容到 `.claude/skills/` 目录（避免双源真相）
- 在 agent frontmatter 的 `## 需要的技能` 章节把 superpowers skill 写成 markdown 路径（路径应只指向 mefan 自有 skill）
- 用 `@superpowers/xxx` 占位符代替真实 skill 名（已被 `test_skill_references.py` 拦截）

### Skill 名称规范

**严格使用 v5.1.0 真实存在的名字**（区分大小写、连字符）：

| 真实 skill 名 | 不存在（占位符，已弃用） |
|---|---|
| `superpowers:test-driven-development` | ~~`@superpowers/tdd-mastery`~~ |
| `superpowers:requesting-code-review` | ~~`@superpowers/code-review`~~ |
| `superpowers:verification-before-completion` | ~~`@superpowers/test-execution`~~ |
| `superpowers:systematic-debugging` | （无对应占位符，新增） |
| `superpowers:finishing-a-development-branch` | （无对应占位符，新增） |

引用路径：`superpowers:<skill-name>`，冒号是 Claude Code 解析 plugin skill 的官方语法。

## 全 7 阶段集成矩阵

> **图例**：✓ = 显式 `Skill(skill="...")` 调用 | ⚠ = 仅在 agent 的 `## 需要的技能` 章节以 markdown bullets 声明，**未在操作步骤中显式调用**

### 阶段 0（Init / Tech Stack Analysis / Knowledge Graph）

| Agent | 调用 Skill | 调用点 | 状态 |
|---|---|---|---|
| `architect-stage0.md` | `superpowers:writing-skills` | 操作 2.6 / 3 / 4：生成 L1-L5 项目 Skill 时 | ✓ |

> **注**：阶段 0 早期列出的 3 条 ⚠（`pm-stage0.brainstorming` / `analyst-stage0.brainstorming` / `architect-stage0.dispatching-parallel-agents`）已于 2026-06-06 第三次审计中**从 agent `## 需要的技能` 章节删除**（详见 §I 评估结果 + §K 后续工作）。

### 阶段 1（Requirements / User Story）

**无 superpowers skill 集成**。3 条 ⚠ 已于 2026-06-06 第三次审计中**从 agent `## 需要的技能` 章节删除**：
- `ba-stage1.brainstorming`（澄清时序错位，详见 §I #4）
- `ba-stage1.writing-plans`（requirements.md 不是 dev tasks，详见 §I #5）
- `pm-stage1.verification-before-completion`（6 维度清单已强制，详见 §I #6）

### 阶段 2（Architecture / ADR / Test Plan）

**无 superpowers skill 集成**。3 条 ⚠ 已于 2026-06-06 第三次审计中**从 agent `## 需要的技能` 章节删除**：
- `architect-stage2.writing-plans`（v3.x DEFER，详见 §I #7 + §K）
- `architect-stage2.dispatching-parallel-agents`（MG 划分是全局推理，详见 §I #8）
- `qa-stage2.writing-plans`（错误分类，详见 §I #9）

> **注**：`pm-audit-stage2.md` 的 `## 需要的技能` 仅引用了项目自有 skill `.claude/skills/graphify-query-cheatsheet.md`，**未集成 superpowers skill**。该 agent 的 frontmatter `tools:` 数组也不含 `Skill` 工具（与 `test_agent_frontmatter.py` 注释"P2 警告：pm-audit-stage2.md 显式 defer 到 v2.5.0+"一致）。**v2.5.0+ 待补线**。

### 阶段 3（Iteration Planning / Sprint Board）

**无 superpowers skill 集成**。3 条 ⚠ 已于 2026-06-06 第三次审计中**从 agent `## 需要的技能` 章节删除**：
- `analyst-stage3.writing-plans`（机械提取不是 plan 创作，详见 §I #10）
- `pm-stage3.dispatching-parallel-agents`（与单 dev 串行冲突，详见 §I #11）
- `pm-stage3.verification-before-completion`（8 项自检已强制，详见 §I #12）

### 阶段 4（Implementation / 7 状态）

| Agent | 调用 Skill | 调用点 | 状态 |
|---|---|---|---|
| `dev-stage4.md` | `superpowers:test-driven-development` | 操作 3 开头：写第一行代码前 | ✓ |
| `dev-stage4.md` | `superpowers:verification-before-completion` | 操作 3 末尾：声明"实现完成"前 | ✓ |
| `dev-stage4.md` | `superpowers:systematic-debugging` | 操作 5：Self-Check 失败时 | ✓ |
| `dev-fix-stage4.md` | `superpowers:receiving-code-review` | 操作 1 开头：接收 review 反馈 | ✓ |
| `dev-fix-stage4.md` | `superpowers:systematic-debugging` | 修复 Bug 时 | ✓ |
| `dev-fix-stage4.md` | `superpowers:verification-before-completion` | 修复完成前 | ✓ |
| `architect-stage4.md` | `superpowers:requesting-code-review` | 操作 2.1：Code Review 准备 | ✓ |
| `architect-stage4.md` | `superpowers:verification-before-completion` | 操作 4：出报告前 | ✓ |
| `qa-stage4.md` | `superpowers:test-driven-development` | 操作 2：QA-Test-Coding | ✓ |
| `qa-stage4.md` | `superpowers:verification-before-completion` | 操作 4 末尾 | ✓ |
| `qa-stage4.md` | `superpowers:systematic-debugging` | 操作 5：发现 Bug 时 | ✓ |
| `pm-stage4.md` | `superpowers:finishing-a-development-branch` | 操作 4：Close 验收开头 | ✓ |
| `pm-stage4.md` | `superpowers:verification-before-completion` | 操作 4 中段：merge 前后验证 | ✓ |

### 阶段 5（Quality Gate）

| Agent | 调用 Skill | 调用点 | 状态 |
|---|---|---|---|
| `qa-stage5.md` | `superpowers:verification-before-completion` | 门禁裁定前 | ✓ |
| `qa-stage5.md` | `superpowers:systematic-debugging` | **Q1：qa-stage5 自身接线**（操作 7：发现新 P0/P1 bug 走 4 阶段） | ✓ |
| `pm-stage5.md` | `superpowers:verification-before-completion` | P0/P1 决策时 | ✓ |
| `dev-stage5.md` | `superpowers:test-driven-development` | 修复 P0 缺陷时 | ✓ |
| `dev-stage5.md` | `superpowers:systematic-debugging` | 修复前走 4 阶段调查根因 | ✓ |
| `dev-stage5.md` | `superpowers:verification-before-completion` | 修复完成前 | ✓ |
| `guardian-stage5.md` | `superpowers:verification-before-completion` | 终审前 | ✓ |

### 阶段 6（Retrospective / Evolution）

| Agent | 调用 Skill | 调用点 | 状态 |
|---|---|---|---|
| `coach-stage6.md` | `superpowers:writing-skills` | 写 evolution-proposal.md 时 | ✓ |
| `pm-stage6.md` | `superpowers:verification-before-completion` | 批准 evolution proposal 前 | ✓ |
| `pm-stage6.md` | `superpowers:writing-skills` | **W1：pm-stage6 自身接线**（操作 4：合并新 Skill 套用写作规范） | ✓ |
| `guardian-stage6.md` | `superpowers:verification-before-completion` | 验证 evolution proposal 通过前 | ✓ |

### `qa-fix-stage4.md` 补充说明

`qa-fix-stage4.md` 存在 frontmatter `tools:` 含 `Skill` 工具，但**未声明任何 superpowers skill**。本矩阵未将其列入"集成清单"，但在 `## 需要的技能` 章节声明了 3 个 mefan 自有 skill（`.claude/skills/write-unit-test.md`、`write-manual-test-guide.md`、`test-plan-reading.md`）。

---

## H. 声明≠调用（Declared-only Skills）追踪

**已完成接线的 3 个 declared-only skills**（2026-06-06 审计更新）：

| 接线方 | Skill | 实际接线位置 | 接线方案 |
|---|---|---|---|
| `qa-stage5.md` | `superpowers:systematic-debugging` | 操作 7 步骤 5：`Skill(skill: "superpowers:systematic-debugging")` | **Q1：qa-stage5 自身真正接线**（门禁裁定前，发现新 P0/P1 bug → 调 systematic-debugging 走 4 阶段调查） |
| `mf-upgrade:04-implement.md`（playbook） | `superpowers:requesting-code-review` | §步骤 2.3 reviewer subagent prompt：`Skill(skill: "superpowers:requesting-code-review")` | **P3：下沉到 reviewer subagent**（与 superpowers 哲学一致：context isolation；不在 `pm-stage4.md` 矩阵列出，详见 §H 注） |
| `pm-stage6.md` | `superpowers:writing-skills` | 操作 4 步骤 4：`Skill(skill: "superpowers:writing-skills")` | **W1：pm-stage6 自身调**（合并新 Skill 套用 writing-skills 规范） |

> **§H 注（P3 特殊处理）**：`pm-stage4.md` 仍**在 `## 需要的技能` 章节声明** `superpowers:requesting-code-review`（作为该 agent 编排的"应有能力"），但**实际调用点**在 `mf-upgrade:04-implement.md` §步骤 2.3 派发的 reviewer subagent 内部。因此本矩阵**不在 `pm-stage4.md` 阶段 4 表格列出此条目**，避免读者误以为 pm-stage4 自身显式调用了它。

**待补线的 declared-only skills**（历史）：早期矩阵列出的 12 条 ⚠（阶段 0-3 agent）已于 **2026-06-06 第三次审计中从 agent `## 需要的技能` 章节全部删除**（详见 §I 评估结果）。当前阶段 0-3 仅剩 1 条真集成（`architect-stage0.writing-skills` ✓）。DEFER 项目（2 条）记录在 §K 后续工作中。

**2026-06-06 第二次审计更新**：上述 10 条 ⚠ 已逐条评估，详见 §I。结果：**0 条需要升级为显式 Skill tool 调用**（mefan 模板化程度高，方法论已被自有 skill 覆盖）。

---

## I. 阶段 0-3 ⚠ Skill 评估（2026-06-06 第二次审计）

逐条评估阶段 0-3 的 12 条 declared-only（⚠）是否需要升级为显式 `Skill(skill: "superpowers:xxx")` 调用。

### 评估方法

每条 ⚠ 评估 3 维度：
1. **mefan 覆盖度**：mefan 自有 skill / 模板 / 规则是否已覆盖该方法论？
2. **场景适用性**：该 skill 是否真的适合 mefan 的工作流？
3. **风险评估**：如果不调用，会出现什么问题？

### 评估结论一览

| 决策 | 数量 | 涉及条目 |
|------|------|---------|
| **NOT-FIX**（删除声明，方法论已覆盖） | 9 | #1, #3, #4, #5, #6, #8, #9, #10, #11 |
| **NOT-FIX**（删除声明 + 是错误分类） | 2 | #9, #10（声明与 skill 方法论不对应） |
| **DEFER**（保留 ⚠，v3.x 评估） | 2 | #2, #7 |
| **FIX**（升级为 ✓） | **0** | — |

**核心结论**：12 条 ⚠ 中 **0 条值得升级**。mefan 模板化程度极高（template + 自有 skill + rule），所有方法论已被 mefan 自身机制覆盖。显式调用会**重复双源**且**消耗 context**。

### 12 条逐条评估

#### 1. `pm-stage0.brainstorming`（操作 0.5 需求澄清对话前）

- **NOT-FIX** | 角色错位
- pm-stage0 核心是"环境初始化 + 上下文建立"，**不做需求澄清**（澄清是 analyst-stage0 职责）
- 套用 brainstorming 是角色错位
- **改动**：从 `pm-stage0.md` 的 `## 需要的技能` 删除该声明

#### 2. `analyst-stage0.brainstorming`（功能需求澄清对话）

- **DEFER** | v3.x 评估
- analyst-stage0 操作 0.3 的 **12 项检查清单**（"1. 新需求是什么"/"2. 现有项目是否已实现"/"5. 与现有功能的关系"/"7. 非功能性需求"/"8. 大文件处理"/"12. 设计复杂度" 等）已强制覆盖 brainstorming 关键的"未明确问题探测"
- 显式调用的边际收益主要是给 AI 提供"如何发散"的更细指引，但每次澄清会消耗 context
- 当前 mefan 单 dev 串行 + WIP ≤ 2，context 是稀缺资源
- **决策**：保留 ⚠ 状态，v3.x 多 agent 并行模式 + 增强 context 隔离时再升级

#### 3. `architect-stage0.dispatching-parallel-agents`（graphify 大规模查询时）

- **NOT-FIX** | 场景不适用
- arch-stage0 操作 2.5 graphify query 是**图数据库查询命令**，不是 subagent 推理任务
- 每条 query 独立可串行执行（伪代码 for each row），30-40 条 ~1-2 分钟
- "并行 subagent" 会引入 context 隔离开销（每个 subagent 都要加载 vocabulary + 模板规则）
- **改动**：从 `architect-stage0.md` 删除该声明（保留 `superpowers:writing-skills`）

#### 4. `ba-stage1.brainstorming`（需求澄清时）

- **NOT-FIX** | 时序错位
- 澄清**已由 analyst-stage0 完成**，ba-stage1 接收的是"已澄清的功能要点"
- ba-stage1 的工作是"如何拆"（结构化拆解），不是"需要问什么"（澄清）
- user-story-splitting.md（INVEST 7 步）+ sub-feature-splitting.md（最小化粒度 8 步）已强制
- **改动**：从 `ba-stage1.md` 删除该声明

#### 5. `ba-stage1.writing-plans`（写 requirements.md 前）

- **NOT-FIX** | 文档类型不匹配
- writing-plans 关心的是"待执行任务"（细粒度 code change），有 verify step
- requirements.md 是"用户需求"（高层次 user story），没有 verify step
- INVEST 原则在 US 层不直接对应
- requirements-template.md + user-story-splitting.md 已强制 US/SF 结构 + Gherkin AC 4 类
- **改动**：从 `ba-stage1.md` 删除该声明

#### 6. `pm-stage1.verification-before-completion`（PM 审查通过前）

- **NOT-FIX** | 方法论已内化
- pm-stage1 已自包含**完整 6 维度审查清单**（拓扑完整性、Gherkin AC、受影响范围、非功能需求、AC 完整性 4 类、需求一致性 vs feature.md）+ 打回计数规则（≥ 3 次提交 Human Gate）
- verification-before-completion 的核心方法（"在声称完成前，逐项核对标准"）已完全内化
- skill 调用会**重复双源**
- **改动**：从 `pm-stage1.md` 删除该声明

#### 7. `architect-stage2.writing-plans`（生成 ADR §7 任务拆解 + pseudocode）

- **DEFER** | v3.x 评估
- architect-stage2 操作 2.3.6.1 明确 Task 拆分原则（时间粒度 2-4h、依赖标注、优先级排序、关联 US/MG）
- 操作 2.3.6.3 强制 pseudocode 注释块（按 P1-P9 顺序）
- pseudocode 文件独立化（每个 Task 一个文件）已实现 writing-plans 的"exact files/paths"纪律
- 边际收益主要是"每个 task 都有 verify step"，mefan 已通过 pseudocode/ 独立文件 + Skill 引用实现同等纪律
- **决策**：保留 ⚠ 状态，v3.x 评估

#### 8. `architect-stage2.dispatching-parallel-agents`（§2.4 MG 划分时）

- **NOT-FIX** | 全局推理不能用并行 subagent
- MG 划分是单 agent 全局推理任务，依赖所有 US + API 关系 + 复用约束的**全局视图**
- 每个 subagent 看到的是**局部信息**，会产生**冲突的 MG 边界**，破坏 §2.6 集成分析的全局一致性
- superpowers-integration.md §"不集成的 superpowers skill" 已明确 `subagent-driven-development` 只在"独立 reviewer subagent"模式借鉴，**不适用 MG 划分**
- **改动**：从 `architect-stage2.md` 删除该声明

#### 9. `qa-stage2.writing-skills`（写 test-plan.md 时）

- **NOT-FIX** | **错误分类**
- writing-skills 是 superpowers 的 **meta-skill**，专门用于撰写新的 SKILL.md（frontmatter、Use when...、Token 高效）
- test-plan.md **不是 skill**，不应套用此 skill 的写作规范
- 强行套用会引入"Use when..."等不适用的字段
- 正确的对位应是 `.claude/skills/write-manual-test-guide.md` 或 `write-unit-test.md`（mefan 已有）
- **改动**：从 `qa-stage2.md` 删除 `superpowers:writing-skills`，补充 mefan 自有 skill（如有缺失）

#### 10. `analyst-stage3.writing-plans`（从 ADR 提取 Task）

- **NOT-FIX** | **方法论不对应**
- analyst-stage3 操作 2-3 明确"**直接从 ADR 提取，不要重写**"——是机械任务，不是 plan 创作
- writing-plans 方法论（"bite-sized tasks with verification"）适用于 plan 创作者（architect-stage2），不适用于 plan 提取者（analyst-stage3）
- 6 类信息（关联 Test Plan、引用 Skills、可复用代码、风险说明、预计工时、输入输出）从 ADR 对应章节直接读取
- **改动**：从 `analyst-stage3.md` 删除该声明

#### 11. `pm-stage3.dispatching-parallel-agents`（WIP 估算/冲突识别）

- **NOT-FIX** | 与单 dev 串行模式冲突
- WIP 估算和冲突识别是**单 agent 推理任务**（依赖全局 sprint 视图），不适合并行 subagent
- conflict-resolution.md 规则 + pm-stage3 操作 2-5 冲突裁决决策树已实现
- 适用场景是 multi-agent code review 之类（参考 architect-stage4 的 P3 模式），不适用 sprint planning
- **改动**：从 `pm-stage3.md` 删除该声明

#### 12. `pm-stage3.verification-before-completion`（sprint-status.md 发布前）

- **NOT-FIX** | 方法论已内化
- pm-stage3 操作 7 自检清单 **8 项**（Modular Group 完整、US 依赖矩阵、原子化、Task 关联 US/MG、核心冲突、WIP、警戒线、里程碑、生命周期状态）已强制
- verification-before-completion 的核心方法已完全内化
- **改动**：从 `pm-stage3.md` 删除该声明

### 实施结果（2026-06-06 第三次审计）

**所有 12 条 declared-only 已从 agent 文件中物理删除**：

| # | Agent | 删除的 bullet | 状态 |
|---|-------|--------------|------|
| #1 | `pm-stage0.md` | `superpowers:brainstorming` | ✅ 已删 |
| #2 | `analyst-stage0.md` | `superpowers:brainstorming` | ✅ 已删（DEFER→§K） |
| #3 | `architect-stage0.md` | `superpowers:dispatching-parallel-agents` | ✅ 已删 |
| #4 | `ba-stage1.md` | `superpowers:brainstorming` | ✅ 已删 |
| #5 | `ba-stage1.md` | `superpowers:writing-plans` | ✅ 已删 |
| #6 | `pm-stage1.md` | `superpowers:verification-before-completion` | ✅ 已删 |
| #7 | `architect-stage2.md` | `superpowers:writing-plans` | ✅ 已删（DEFER→§K） |
| #8 | `architect-stage2.md` | `superpowers:dispatching-parallel-agents` | ✅ 已删 |
| #9 | `qa-stage2.md` | `superpowers:writing-plans` | ✅ 已删 |
| #10 | `analyst-stage3.md` | `superpowers:writing-plans` | ✅ 已删 |
| #11 | `pm-stage3.md` | `superpowers:dispatching-parallel-agents` | ✅ 已删 |
| #12 | `pm-stage3.md` | `superpowers:verification-before-completion` | ✅ 已删 |

**最终状态**：阶段 0-3 仅剩 1 条 superpowers 集成（`architect-stage0.writing-skills` ✓，**真集成**）。其余 9 个 stage 0-3 agent 的 `## 需要的技能` 章节**不再包含任何 superpowers 引用**。

**实施后总览**：
- 阶段 0-3：1 个 agent 真集成（architect-stage0）
- 阶段 4-6：13 个 agent 真集成（22+ 处显式 `Skill(...)` 调用）
- **总计**：13 个 agent 真集成，0 条假集成

---

## J. 中间文件断链清单（2026-06-06 第二次审计）

逐条验证 2026-06-06 第一次审计识别的 10 个断链点（H1-H10），状态如下。

### 验证结论一览

| # | 断链点 | 验证结果 | 影响 | 修复决策 |
|---|--------|---------|------|---------|
| H1 | evolution-proposals/*.md | ✅ **已修**（pm-stage0 操作 0.7.1） | 低 | NOT-FIX |
| H2 | iteration-retrospective.md | ⚠ 部分修（analyst 未修） | 中 | DEFER |
| H3 | reports/PROJECT_STATUS.md | ✅ **已修**（pm-stage0 操作 0.7.3） | 低 | NOT-FIX |
| H4 | CHANGELOG.md + HARNESS_VERSION.md | ✅ **已修**（architect-stage0 操作 0.1a） | 低-中 | NOT-FIX |
| **H5** | **violations.json** | ✅ **真断链**（最严重） | **高** | **FIX（必修）** |
| H6 | skills-proposed/ + rules-proposed/ | ⚠ 部分断链 | 中 | DEFER |
| H7 | iteration-plan.md | ❌ 不算断链（文档残留） | 无 | NOT-FIX |
| H8 | sprint-N/ 归档 | ✅ **已修**（pm-stage0 操作 0.7.2） | 低 | NOT-FIX |
| H9 | task-summary/T-NNN.md | ✅ **已修**（dev-stage4 操作 3.7 + pm-stage6 操作 1 §1.2） | 中 | NOT-FIX |
| H10 | bug-log/manual+auto | ✅ 双向已修 | 低-中 | NOT-FIX |

**核心发现**：
- 7 条已修（H1, H3, H4, H5, H8, H9, H10）—— 2026-06-06 第一次审计的 4 处 Read 修复 + H5 契约修正 + H9 完整修复（消费方+生产方）均已生效
- 0 条真断链（H5 必修已修，H9 消费方+生产方均已修）
- 2 条部分断链可延后（H2 analyst 不读 retrospective / H6 skills-proposed 永久挂起）
- 1 条文档残留 H7（iteration-plan.md 在 iteration-planning.md 中提及但实际已合并到 sprint-status.md）—— **不算断链**，不修

### 必修项 H5：violations.json 契约修复

#### 现状（grep + read 验证）

| 环节 | 实际行为 |
|------|---------|
| Hook 输出 | **6 个 hook 全部只 echo 到 stdout + 追加到 `mefan-log.md`**，**没有写 `violations.json`** |
| `check-consistency.py` | `print(json.dumps(...))` 输出 stdout，**不**`open(violations.json, 'w').write(...)` |
| `check-incremental.sh` L33 | 调用 `check-consistency.py` 后用 `echo "$result" | grep -q` 判断，**$result 是 stdout 字符串，不写盘** |
| `check-state-machine.sh` | 写 `mg-state.json`（**非** violations.json） |
| Coach 读取 | `coach-stage6.md` 操作 1 L34 说"读取所有 `violations.json` 文件"——但磁盘上**永远没有这个文件** |
| 实际效果 | 进化教练的"日志聚合"步骤**完全失效**（除 `mefan-log.md` 文本可读） |

#### 修复方案

| 方案 | 改动 | 优点 | 缺点 |
|------|------|------|------|
| **A** | 5 个 bash hook 末尾追加 `echo "{...}" >> "$ROOT/.claude/iterations/sprint-latest/violations.json"` | 与原契约对齐 | 5 个 hook 都要改，需去重逻辑（~35 行） |
| **B（推荐）** | `coach-stage6.md` 操作 1 L34 改为 `grep -E "WARN\|未达标\|违规" iterations/mefan-log.md` | 1 行改，最小侵入 | 放弃 `violations.json` 语义化文件 |
| **C** | 在 hook-vs-guardian.md 重写契约，让 hook 直接写 `mefan-log.md`，coach 解析该文件 | 全新设计 | 大动作，重写规则 |

**推荐方案 B**：1 行改 `coach-stage6.md` 操作 1，承认 hooks 实际输出在 `mefan-log.md`。**不修改 hook 实现**（避免回归 hook 流程），**不修改规则契约**（保留 violations.json 作为长期目标）。

#### 改动范围

- `.claude/agents/coach-stage6.md` 操作 1 步骤 3：~5 行
- 同时在 `hook-vs-guardian.md` 顶部加一行"**注**：当前实现中 hook 输出到 stdout + `mefan-log.md`，coach 解析该文件而非 `violations.json`（见 superpowers-integration.md §J H5）"

### H9 修复完成：dev-stage4 写 task-summary/T-NNN.md（2026-06-06 第三次审计修复）

#### 修复前现状

- **消费方**（pm-stage6 操作 1 §1.2）**已修**（显式 `Read 工具 task-summary/`，"AI 必须执行"）
- **生产方**（dev-stage4）**完全无 task-summary 引用**（grep 0 匹配）
- 实际：sprint-latest/task-summary/ 目录**当前不存在**，pm-stage6 操作 1 L169 的 `if [ -d "$TASK_SUMMARY_DIR" ]` 直接跳过

#### 修复方案（在 `dev-stage4.md` 操作 3.1 之后新增 3.7）

```markdown
### 操作 3.7：写任务级总结（H9 修复）
> **目的**：把本 Task 的实现、测试、债务写入 `task-summary/T-{TASK_ID}.md`，供 `pm-stage6` 阶段 6 汇总。

1. mkdir -p $ROOT/.claude/iterations/sprint-latest/task-summary
2. Write 工具写入 task-summary/T-{TASK_ID}.md（模板含基本信息 / 实现要点 / 测试覆盖 / 技术债务 / 关联 ADR / 状态 6 段）
3. log-event.sh 记录
```

**实施内容**（实际落地，~70 行）：含完整 markdown 模板、约束、与下游衔接说明、3 类异常处理。

#### 修复后效果

- ✅ 消费方（pm-stage6 操作 1 §1.2）+ 生产方（dev-stage4 操作 3.7）**双向已修**
- ✅ 模板字段（技术债务 / 测试覆盖 / 实现要点 / 关联 ADR / 状态）稳定，pm-stage6 grep 可解析
- ✅ 每个 Task 一份 T-NNN.md，**不**把 MG 内多个 Task 合并
- ✅ Code Review 提交前必须生成（保证 pm-stage6 阶段 6 能读到）

**改动量**：~70 行（dev-stage4.md 新增操作 3.7）

### 延后 H2 / H6

#### H2 iteration-retrospective → analyst-stage0/3 未读

- **部分缓解**：pm-stage0 操作 0.7.2 显式 `Read`，session-status.md 也会带过去
- **风险**：Analyst 不知道上一迭代的"做得不好"和"待改进模式"，容易重复犯错
- **决策**：DEFER（analyst 不读是设计简化，非关键路径）
- **如要修**：analyst-stage0.md 操作 0.4 前新增 `Read .claude/iterations/sprint-*/iteration-retrospective.md`（5-8 行）

#### H6 skills-proposed/ + rules-proposed/

- **现状**：pm-stage6 写"实验性"提案到这两个目录，但**没有 agent 主动 Read 它们**
- **后果**：实验性 Skill/Rule 实际上变成"**永久挂起**"的提案，dev-stage4 不会自动加载
- **决策**：DEFER（这是机制设计问题，需 stage 0 整体重设计）
- **如要修**：dev-stage4.md 操作 1 前新增 `Glob .claude/skills-proposed/**/SKILL.md` + `Glob .claude/rules-proposed/**/*.md`（~10 行）

### 不修 H7 iteration-plan.md

- `iteration-planning.md` 规则 L29-37 提到 `iteration-plan.md`，但只是**模板示例的字段名**
- pm-stage3.md 明确"已合并到 sprint-status.md"
- 当前 sprint-status 模板就是单一数据源
- **决策**：NOT-FIX（不算真断链，是文档残留）
- **如要清理**：iteration-planning.md L29-37 的示例标题加 "(sprint-status.md 章节 1)" 后缀（1-2 行）

---

## K. 后续工作（DEFER + 待办）

### K.1 Stage 0-3 DEFER 项目（v3.x 评估）

2 条评估为"DEFER（v3.x 评估）"的 superpowers skill，**当前**已从 agent `## 需要的技能` 章节删除，**未来**在 mefan v3.x 多 agent 并行模式 + 增强 context 隔离时**重新评估是否接线**：

| Agent | Skill | 重新评估触发条件 | 当前替代机制 |
|-------|-------|------------------|-------------|
| `analyst-stage0` | `superpowers:brainstorming` | mefan 升级到多 agent 并行澄清模式 + context 隔离技术成熟 | analyst-stage0 操作 0.3 的 12 项检查清单 |
| `architect-stage2` | `superpowers:writing-plans` | ADR §7 任务拆解引入"verify step"强制需求 | architect-stage2 操作 2.3.6.1-2.3.6.3 的 9 优先级 Skill 引用 + pseudocode/ 独立文件 |

**重新评估时的检查清单**：
- [ ] 是否引入多 agent 并行 mode（dispatching-parallel-agents 真正派上用场）
- [ ] context 隔离技术成熟（避免 superpowers 加载污染主 agent context）
- [ ] agent 操作步骤自检清单已不能完全覆盖该方法论
- [ ] 用户明确表达"该方法论需要 superpowers 强化"

### K.2 待办清单

| 优先级 | 项 | 改动量 | 来源 | 状态 |
|--------|----|-------|------|------|
| ~~**P0（必修）**~~ | ~~H5 violations.json 契约修复~~ | ~~1-35 行~~ | §J | ✅ **已修**（方案 B + 顶部注） |
| ~~P1~~ | ~~H9 dev-stage4 写 task-summary/T-NNN.md（生产方）~~ | ~~~12 行~~ | §J | ✅ **已修**（dev-stage4 操作 3.7） |
| P2 | H2 analyst-stage0/3 读 iteration-retrospective | ~10 行 | §J | DEFER（设计简化，非关键路径） |
| P3 | H6 skills-proposed/rules-proposed 加载机制 | ~10 行 | §J | DEFER（永久挂起） |
| P3 | H7 iteration-plan.md 文档清理 | 1-2 行 | §J | NOT-FIX（文档残留不算断链） |
| P3 | 阶段 6 重构时考虑恢复 K.1 的 2 条 DEFER | TBD | §K.1 | DEFER |

### K.3 阶段 6 重构入口

详见 `.claude/plans.md` 的「Stage 6 重构 Plan（待启动）」小节，已记录：
- 5 个未解问题（violations.json 契约 / 模板对齐 / 角色分工 + 已修的 2 个）
- 4 套 violations.json 修复方案（待拍板 A/B/C/D）
- 验收标准 + 触发条件 + 责任人

---

## 阶段 0-3 集成现状（2026-06-06 第三次审计后）

**2026-06-06 第三次审计修正了"阶段 0-3 大多仅声明未调用"的旧认知**：

| 阶段 | 集成状态 | agent 数 | 集成方式 |
|------|---------|---------|---------|
| **阶段 0** | 1 个真集成 + 0 个声明 | 1/3 | `architect-stage0.writing-skills`（操作 2.6/3/4 显式调用） |
| **阶段 1** | 0 集成 | 0/2 | 无 superpowers 引用 |
| **阶段 2** | 0 集成 | 0/2 | 无 superpowers 引用 |
| **阶段 3** | 0 集成 | 0/2 | 无 superpowers 引用 |
| **阶段 4-6** | 13 个真集成 | 13/13 | 22+ 处显式 `Skill(...)` 调用 |

**核心结论**：
- 阶段 4-6 的 agent **全部**有真集成（每个 agent 1-3 处显式 Skill tool 调用）
- 阶段 0 的 architect-stage0 是阶段 0-3 唯一真集成（因写 L1-L5 skill 需 superpowers 规范）
- 阶段 1-3 的 agent **完全不集成** superpowers skill（2026-06-06 第三次审计已从文件物理删除所有 ⚠ 声明）

**关于设计意图**：阶段 0-3 是"规划阶段"，主要产出文档而非代码，**使用 mefan 自有 skill**（如 `user-story-splitting.md`、`writing-plans` 模板）通过 `Read` 工具加载，**不通过** `Skill tool` 加载 superpowers skill。superpowers 的 brainstorming / writing-plans 等"工作流纪律"已被 mefan 自有 skill + 模板 + 规则强制覆盖。

**DEFER 项目的 2 条**记录在 §K.1，等 v3.x 多 agent 并行模式时重新评估。

## 不集成的 superpowers skill（明确说明）

| Skill | 不集成原因 | 何时再评估 |
|---|---|---|
| `superpowers:using-git-worktrees` | mefan 单 dev 串行（WIP ≤ 2），worktree 价值边际 | v3.x 评估多 agent 并行模式时 |
| `superpowers:executing-plans` | 与 mefan PM 编排器功能重叠；不引入并行 session 模式 | v3.x 评估 |
| `superpowers:subagent-driven-development` | 部分重叠（mefan 已是 subagent 驱动），仅在阶段 4 方案 B 借鉴"独立 reviewer subagent"模式 | 持续 |
| `superpowers:using-superpowers` | bootstrap skill，仅在初始化时有用；不强制 agent 加载 | 持续 |

## Code Review Context Isolation（方案 B）

**问题**：mefan 的 Architect Agent 在**同一个 session** 里读 ADR + 读代码 + 出 review 报告，superpowers 的 reviewer 是**独立 subagent 隔离 context**。

**方案 B（已采纳）**：

1. **保留** `architect-stage4.md` 内部不变（仍可独立处理"非 Code Review"类检查，如 ADR 一致性、reference module 检查）
2. **在 `commands/mf-upgrade:04-implement.md`（阶段 4 playbook）的"Code Review"步骤中**新增一段：
   - **执行者**：`pm-stage4`
   - **派发方式**：用 `Task` 工具派发 `general-purpose` subagent
   - **传给 subagent 的输入**：
     - `BASE_SHA` = `feature/MG-${MG_NAME}` 分支创建前的 commit SHA
     - `HEAD_SHA` = 当前 commit SHA
     - 完整 `ADR.md` §5（API 设计）+ §8（错误处理）+ §9（风险）
     - `consistency-baseline.md`
     - `requirements.md` 中关联 US 的 Gherkin AC
   - **显式指令**："不要读 sprint-status.md / session-status.md，只看 git diff + 上述输入。返回结构化 review 报告（Strengths / Critical / Important / Minor）"
   - **subagent 返回后**：PM 把报告转给 architect-stage4 整合
   - **arch 写入**：`reviews/code-review-{MG-ID}.md`
3. **目的**：实现 superpowers 风格的 context isolation —— reviewer subagent 不知道 mefan 的全局状态，只看代码
4. **最小侵入**：不改 architect-stage4.md，只改 playbook 一处

**为什么选 B 不选 A**：
- A 方案（"在 architect-stage4 内部模仿独立 context"）效果有限 —— 同一个 session 的 context window 还是共享的
- B 方案（**真派独立 subagent**）才是 superpowers 哲学的本质 —— "fresh context per task"

## 与 mefan 17 章节 ADR 的关系（正交共存）

**ADR §7 任务级 Skill 的本质**：
- 形式：`.claude/skills/project-tech-*.md`、`project-middleware-*.md`、`project-*-module.md`
- 内容：项目特定的**技术栈使用规范**
- 关注点：**"用什么"**（which library / which module / which pattern）

**superpowers skills 的本质**：
- 形式：`~/.claude/plugins/.../superpowers/5.1.0/skills/*/SKILL.md`
- 内容：**工作流纪律**（TDD、verification、debugging、code review、finishing-a-development-branch）
- 关注点：**"怎么做"**（how to develop / how to verify / how to debug）

**正交矩阵**（dev-stage4 操作 3 实际加载顺序）：
1. Dev 先调 `Skill(skill: "superpowers:test-driven-development")` → 加载**怎么写测试**的方法论
2. Dev 按 ADR §7 引用 `Read .claude/skills/project-tech-lombok.md` → 加载**项目特定**的 Lombok 用法
3. Dev 在"怎么写" + "用什么"的交集上**写代码 + 写测试**

**结论**：mefan 的 17 章节 ADR 是 superpowers workflow 的**具体化载体**，二者**正交共存**，**不是替代关系**。

## 失败回退（Fallback）

### Skill tool 不可用

如果当前 Claude Code 运行时未启用 `Skill` 工具（罕见），agent 应：
1. agent 操作步骤中的 `Skill` tool invocation 会被框架忽略或报错
2. agent **不应当**崩溃，而应**降级**：
   - 读取对应 skill 的本地 markdown 路径（如果存在的话）
   - 或者直接按 agent 操作步骤的内联指令执行
3. 标记该次执行为"degraded mode"并写入 sprint-status.md

### Superpowers plugin 未安装

如果 `~/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/` 不存在：
1. `test_skill_references.py` 会失败（agent 引用了不存在的 skill）
2. CI 应当阻止合并
3. 修复方法：安装 superpowers 插件或回滚相关 agent 改动

## 版本

- 集成引入版本：mefan v2.5.0（MINOR 升级；**`HARNESS_VERSION.md` 待创建**，由 pm-stage6 阶段产出）
- 对应 superpowers 版本：v5.1.0
- 升级到更高 superpowers 版本时需重新跑 `test_skill_references.py`

## 测试覆盖

- **`tests/test_agent_frontmatter.py`**：断言所有 stage 0-3 agent 的 `tools` 包含 `Skill`（P2 警告：pm-audit-stage2.md 显式 defer 到 v2.5.0+）
- **`tests/test_skill_references.py`**：断言所有 `@superpowers/xxx` 占位符解析到 v5.1.0 真实 skill
- **CI 必跑**：`pytest tests/test_agent_frontmatter.py tests/test_skill_references.py`

## 变更日志

| 日期 | 变更 | 引入者 |
|---|---|---|
| 2026-06-05 | 初版：v2.5.0 集成 10 个 superpowers skill 到 21 个 agent | PM + Dev |
| 2026-06-06 | 审计更新：拆分 ✓/⚠ 状态；删除 pm-audit-stage2 虚假条目；新增 qa-fix-stage4 条目；新增"H. 声明≠调用"小节；删除 HARNESS_VERSION v2.5.0 引用；删除 test_hooks.py | PM + Dev |
| 2026-06-06 | 补线完成：3 个 declared-only skill 接线（Q1 qa-stage5.systematic-debugging / P3 pm-stage4.requesting-code-review → mf-upgrade:04-implement / W1 pm-stage6.writing-skills）；Stage 6→Stage 0 主循环闭合（pm-stage0 操作 0.7 / architect-stage0 操作 0.1a / pm-stage6 操作 1）；新增 3 个测试（test_declared_vs_invoked / test_loop_closure / test_skill_integration_matrix） | PM + Dev |
| 2026-06-06 | **第二次审计**：12 条 ⚠ stage 0-3 skill 逐条评估 → 新增 §I（结论：0 条升级，9 NOT-FIX + 2 DEFER + 0 FIX）；10 条 H1-H10 断链 grep 验证 → 新增 §J（结论：6 已修 / 1 真断链 H5 violations.json 必修 / 1 生产方缺失 H9 dev-stage4 / 2 DEFER H2+H6 / 1 文档残留 H7 不修） | PM + Dev |
| 2026-06-06 | **第三次审计（清理）**：从 9 个 stage 0-3 agent `## 需要的技能` 章节物理删除 12 条假集成（1 pm-stage0 / 2 analyst-stage0+architect-stage0 / 2 ba-stage1 / 1 pm-stage1 / 2 architect-stage2 / 1 qa-stage2 / 1 analyst-stage3 / 2 pm-stage3）；更新矩阵 + 新增 §K（DEFER 后续工作）；**最终 13 个 agent 真集成 0 条假集成**（阶段 0-3 仅剩 architect-stage0 真集成，阶段 4-6 保持 12 个） | PM + Dev |
| 2026-06-06 | **H5 修复（方案 B）**：改 `coach-stage6.md` 操作 1 L34 改用 `grep mefan-log.md` 解析违规事件（不修改 hook 实现，避免回归）；`hook-vs-guardian.md` 顶部加"当前实现注"+ 更新 Hook/守护者定义反映实际数据源（stdout + mefan-log.md） | PM + Dev |
| 2026-06-06 | **H9 修复（生产方）**：在 `dev-stage4.md` 操作 3.1 之后新增「操作 3.7：写任务级总结」步骤，让 Dev 在每个 Task 完成后 Write 工具写入 `task-summary/T-{TASK_ID}.md`（含基本信息 / 实现要点 / 测试覆盖 / 技术债务 / 关联 ADR / 状态 6 段模板）；§J 表 H9 行改为 ✅ 已修，K.2 待办清单中 H9 标 ✅ 已修；新增 `tests/test_h9_task_summary.py` 验证模板字段与下游消费 | PM + Dev |
