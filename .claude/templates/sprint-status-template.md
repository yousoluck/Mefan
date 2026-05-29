# Sprint 状态（单一数据源）

> 文件：`.claude/iterations/sprint-latest/sprint-status.md`
> 创建时机：阶段 3 由 Analyst 生成草案，PM 补充定稿
> 更新时机：任务状态变更时由开发者/PM 更新
> **状态**：Dev 领任务 + 更新状态 的单一数据源
> **sprint name = iteration name**
> **包含**：Plan（MG划分、US列表、Task看板）+ Status（US生命周期、Task状态、进度仪表盘）

---

## 基本信息

| 字段 | 内容 |
|------|------|
| **Sprint ID** | sprint-YYYY-MM-DD |
| **关联 ADR** | adr-YYYY-MM-DD-001 |
| **创建时间** | YYYY-MM-DD HH:mm |
| **创建人** | Analyst + PM |
| **当前进度** | {已完成任务} / {总任务} = {百分比}% |

---

## 1. User Story 分组与 Modular Group [必填]

> 从 ADR 第 2.4 节提取，按依赖关系排序

### 1.1 Modular Group 划分

| Group ID | Group 名称 | 包含 US | 依赖关系 | 可独立开发 | 说明 |
|----------|-----------|---------|----------|-----------|------|
| MG-001 | 评论功能 | US-01, US-02 | 无 | ✅ | 后端 API + 前端 UI 打包 |
| MG-002 | 用户认证 | US-03 | 依赖 MG-001 | ❌ | 依赖评论功能的数据模型 |
| MG-003 | 通知系统 | US-04, US-05 | 依赖 MG-001, MG-002 | ❌ | 依赖用户认证和评论功能 |

### 1.2 US 依赖矩阵

| US | 依赖 US | 被依赖 US | 可独立开发 |
|----|---------|-----------|-----------|
| US-01 | - | US-02, US-03 | ✅ |
| US-02 | US-01 | US-04 | ❌ |
| US-03 | - | - | ✅ |
| US-04 | US-02, US-03 | - | ❌ |
| US-05 | US-02, US-03 | - | ❌ |

### 1.3 User Story 列表

| US ID | 标题 | 优先级 | 所属 Group | 关联 Task 数 |
|-------|------|--------|-----------|-------------|
| US-001 | 用户发表评论 | P0 | MG-001 | 4 |
| US-002 | 查看评论列表 | P0 | MG-001 | 3 |
| US-003 | 用户登录 | P1 | MG-002 | 2 |
| US-004 | 发送通知 | P2 | MG-003 | 3 |
| US-005 | 通知记录查询 | P2 | MG-003 | 2 |

> 从 ADR 第 2.2 节提取

---

## 2. 任务看板 [必填]

> Dev 领任务 + 更新状态 的核心区域

| Task ID | 关联 US/MG | 描述 | 类型 | 状态 | 生命周期状态 | 负责人 | 计划工时 | 实际工时 | 依赖 | 风险 | 警戒线触发点 |
|---------|-----------|------|------|------|-------------|--------|---------|---------|------|------|-------------|
| T-001 | US-01 / MG-001 | 创建 Comment 实体 | 编码 | To Do | 🏃 Dev | | 2h | | - | 🟢 低 | |
| T-002 | US-01 / MG-001 | 创建 Comment Repository | 编码 | To Do | 🏃 Dev | | 1h | | T-001 | 🟢 低 | |
| T-003 | US-01 / MG-001 | 创建 CommentService | 编码 | To Do | 🏃 Dev | | 3h | | T-002 | 🟡 中 | 涉及 PostService 修改 |
| T-004 | US-02 / MG-001 | 创建 CommentController | 编码 | To Do | 🏃 Dev | | 2h | | T-003 | 🟢 低 | 依赖 T-003 |
| T-005 | US-01 / MG-001 | 编写单元测试 | 测试 | To Do | 🧪 QA-Test-Coding | | 3h | | T-001 | 🟡 中 | |

**状态流转（Task级）**：To Do → In Progress → In Review → Done

**生命周期流转（US/MG级）**：🏃 Dev → 🔍 Self-Check → 🏛️ Arch-Check → 🧪 QA-Test-Coding → 🔬 Arch-Test-Check → ✅ Testing → 🎉 Close

**状态说明**：
- To Do：任务待开始（可领取）
- In Progress：任务进行中（已领取）
- In Review：等待 Code Review
- Done：任务完成

**生命周期状态说明**：
- 🏃 Dev：开发中
- 🔍 Self-Check：自我检查
- 🏛️ Arch-Check：架构检查
- 🧪 QA-Test-Coding：QA 测试编码
- 🔬 Arch-Test-Check：测试审查
- ✅ Testing：测试执行
- 🎉 Close：完成

**风险标记**：🟢 低 / 🟡 中 / 🔴 高

**警戒线触发点**：当任务完成进度落后预估进度 30% 时触警

---

## 3. Task 详细信息

### 3.1 关联 Test Plan

| Task ID | 关联测试用例 | 说明 |
|---------|-------------|------|
| T-001 | TC-F-001 | 创建评论功能 |
| T-002 | TC-F-001, TC-I-001 | 查询评论列表 |

### 3.2 引用的 Skills

| Task ID | 引用的 Skill | 使用原因 |
|---------|-------------|----------|
| T-001 | project-service-pattern.md | Service 层实现规范 |
| T-002 | project-mybatis-pattern.md | Mapper 规范 |

### 3.3 可复用代码

| Task ID | 已有代码 | 复用方式 | 复用位置 |
|---------|---------|----------|----------|
| T-001 | PostService.java L45-80 | findById() 模式参考 | CommentServiceImpl |
| T-002 | PageHelper | 分页工具 | CommentRepository |

### 3.4 风险说明

| Task ID | 风险等级 | 风险原因 | 缓解措施 |
|---------|---------|----------|----------|
| T-003 | 🟡 中 | 涉及 PostService 修改 | 全量回归测试 |

---

## 4. 状态汇总仪表盘

| 字段 | 内容 |
|------|------|
| **迭代名称** | {sprint-name} |
| **迭代开始** | YYYY-MM-DD |
| **预期结束** | YYYY-MM-DD |
| **当前进度** | {已完成任务} / {总任务} = {百分比}% |
| **状态分布** | To Do: X \| In Progress: Y \| In Review: Z \| Done: W |
| **WIP 限制** | 2 |
| **关键里程碑** | [ ] M1: 基础设施完成 \| [ ] M2: 核心功能完成 \| [ ] M3: 测试完成 |
| **当前异常** | {从日志中提取的未关闭异常} |

---

## 5. WIP 限制 [必填]

- 最大并行任务数：2
- 计算依据：团队 2 人，核心模块 1 个，安全并行数 = min(2, 1×1) = 1，实际取 2

---

## 6. 并行策略

### 6.1 并行组

| 并行组 | Task 列表 | 可并行条件 |
|--------|-----------|-----------|
| 组 1 | T-001, T-002, T-005 | 无冲突，可同时执行 |
| 组 2 | T-003, T-004 | 依赖组 1 完成 |

### 6.2 串行任务

| Task | 必须在前置任务完成后执行 |
|------|------------------------|
| T-006 | T-003, T-004, T-005 全部完成 |

---

## 7. 里程碑 [必填]

- [ ] M1：基础设施完成（日期：YYYY-MM-DD）
  - 需完成任务：T-001（Entity）、T-002（Repository）、T-005（DTO）
- [ ] M2：核心功能完成（日期：YYYY-MM-DD）
  - 需完成任务：T-003（Service）、T-004（Controller）
- [ ] M3：测试完成（日期：YYYY-MM-DD）
  - 需完成任务：T-006（单元测试）、T-007（集成测试）

---

## 8. User Story 进度汇总 + 生命周期

> 由 PM 根据上方任务看板自动汇总更新

### 8.1 US 7状态生命周期

| 状态 | 说明 | 触发条件 |
|------|------|---------|
| 🏃 **Dev** | 开发中 | Dev 领取任务开始开发 |
| 🔍 **Self-Check** | 自我检查 | 代码提交等待 self-check |
| 🏛️ **Arch-Check** | 架构检查 | Self-Check 通过，等待 Arch 检查 |
| 🧪 **QA-Test-Coding** | 测试编码 | Arch-Check 通过，QA 编写测试代码 |
| 🔬 **Arch-Test-Check** | 测试审查 | QA 测试编码完成，等待 Arch 审查 |
| ✅ **Testing** | 测试执行 | Arch-Test-Check 通过，执行模块测试 |
| 🎉 **Close** | 完成 | 测试通过，US 结束 |

### 8.2 US 进度汇总

| User Story | 所属 Group | 关联 Task 数 | 当前状态 | 生命周期状态 | 完成时间 |
|------------|-----------|-------------|---------|--------------|---------|
| US-01 | MG-001 | 4 | 🔄 In Progress | Dev | - |
| US-02 | MG-001 | 3 | ⏳ To Do | Dev | - |
| US-03 | MG-002 | 2 | ⏳ To Do | - | - |

**US 状态计算规则**：
- ⏳ To Do：所有关联 task 都是 To Do
- 🔄 In Progress：至少一个 task 是 In Progress/In Review
- ✅ Done：所有关联 task 都是 Done

**US 生命周期状态**：基于 MG 内所有 Task 的最先进状态

---

### 8.3 阶段 4 US 7状态追踪表

> 阶段 4 专用追踪表，按 US 追踪 7 状态流转

| US ID | Dev | Self Check | Arch Code Check | QA Test Coding | Arch Test Check | Testing | Close | Bug Count |
|-------|-----|------------|-----------------|----------------|-----------------|---------|-------|-----------|
| US-01 | ✅ | ✅ | ✅ | 🔄 | ⏳ | ⏳ | ⏳ | 2 |
| US-02 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 0 |
| US-03 | 🔄 | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | - |

**图例**：
- ✅: 已完成
- 🔄: 进行中
- ⏳: 等待中
- -: 未开始

**循环限制**：
- Arch Code Check: 3次 → Human Gate
- QA Test Coding: 3次 → Human Gate
- Arch Test Check: 3次 → Human Gate
- Testing Bug: 3次 → Technical Debt

**更新时机**：每个状态转换时由负责的 Agent 更新

| Agent | 负责更新状态 |
|-------|-------------|
| Dev | Dev, Self Check |
| Arch | Arch Code Check, Arch Test Check |
| QA | QA Test Coding, Testing |
| PM | Close |

---

## 9. 冲突记录

### 9.1 核心冲突及处理

| 冲突 Task | 冲突类型 | 处理方式 | 决策依据 |
|-----------|----------|----------|----------|
| T-003 vs T-004 | 修改同一 Service | 串行执行 | T-003 完成后 T-004 才能开始 |
| - | - | - | - |

### 9.2 边缘冲突及标记

| 冲突 Task | 冲突类型 | 处理方式 |
|---------|----------|----------|
| T-001 vs T-002 | 同一模块不同方法 | 可并行，无需处理 |
| - | - | - |

---

## 10. 更新规则

| 操作 | 更新者 | 更新内容 |
|------|-------|---------|
| 领取任务 | 开发者 | 状态 To Do → In Progress |
| 提交 CR | 开发者 | 状态 In Progress → In Review |
| CR 通过 | 守护者 | 状态 In Review → Done |
| CR 驳回 | 守护者 | 状态 In Review → In Progress |
| 任务完成 | QA | 更新实际工时 |

**注意**：每当 task 状态变更时，PM 应同步更新 `session-status.md` 中的 User Story 状态追踪表。

---

## 11. 自检清单

> PM 生成迭代计划前的自检项

- [ ] Modular Group 是否完整划分
- [ ] US 依赖矩阵是否准确
- [ ] Task 数量与 ADR 第 7 节一致
- [ ] 每个 Task 都有预估工时
- [ ] 每个 Task 都有风险等级
- [ ] WIP 限制设置合理
- [ ] 里程碑至少 2 个
- [ ] 无未解决的核心冲突

---

## 12. 关联文档

| 文档 | 路径 | 说明 |
|------|------|------|
| ADR | `.claude/iterations/sprint-latest/ADR.md` | 阶段 2 产出，本计划 Task 来源 |
| test-plan | `.claude/iterations/sprint-latest/test-plan.md` | 阶段 2 产出，本计划测试关联 |
| Session 状态 | `.claude/iterations/sprint-latest/session-status.md` | 阶段状态追踪（与本文件不同用途） |