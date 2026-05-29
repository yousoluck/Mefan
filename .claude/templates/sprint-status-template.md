# Sprint 看板（导出视图）

> 文件：`.claude/iterations/sprint-latest/sprint-status.md`
> 创建时机：阶段 3 由 PM 从 iteration-plan.md 导出
> 更新时机：由 iteration-plan.md 同步，不单独维护
> **重要**：本文件是从 `iteration-plan.md` 导出的看板视图，状态以 iteration-plan.md 为准

---

## 仪表盘

| 字段 | 内容 |
|------|------|
| **迭代名称** | {sprint-name} |
| **迭代开始** | YYYY-MM-DD |
| **预期结束** | YYYY-MM-DD |
| **当前进度** | {已完成任务} / {总任务} = {百分比}% |
| **状态分布** | To Do: X \| In Progress: Y \| In Review: Z \| Done: W |
| **WIP 限制** | 2 |
| **关键里程碑** | [ ] M1: 基础设施完成 \| [ ] M2: 核心功能完成 \| [ ] M3: 测试完成 |
| **当前异常** | {从 iteration-plan.md 提取的未关闭异常} |

---

## 任务看板

> 详细任务拆解见 `iteration-plan.md`

| 任务ID | 关联 US/MG | 描述 | 状态 | 负责人 | 计划工时 | 实际工时 | 风险 | 技术债务 | 备注 |
|--------|-----------|------|------|--------|---------|---------|------|---------|------|
| T-001 | US-01 / MG-001 | 创建 Comment 实体 | To Do | | 2h | | 🟢 低 | | |
| T-002 | US-01 / MG-001 | 创建 Comment Repository | To Do | | 1h | | 🟢 低 | | |
| T-003 | US-01 / MG-001 | 创建 CommentService | To Do | | 3h | | 🟡 中 | | 依赖 T-001 |
| T-004 | US-02 / MG-001 | 创建 CommentController | To Do | | 2h | | 🟢 低 | | 依赖 T-003 |
| T-005 | US-01 / MG-001 | 编写单元测试 | To Do | | 3h | | 🟡 中 | | |

**状态流转**：To Do → In Progress → In Review → Done

**状态说明**：
- To Do：任务待开始
- In Progress：任务进行中
- In Review：等待 Code Review
- Done：任务完成

**风险标记**：🟢 低 / 🟡 中 / 🔴 高

---

## User Story 进度汇总

| User Story | 所属 Group | 关联 Task 数 | 已完成 | 进行中 | US 状态 |
|------------|-----------|-------------|--------|--------|---------|
| US-01 | MG-001 | 4 | 0 | 0 | ⏳ To Do |
| US-02 | MG-001 | 3 | 0 | 0 | ⏳ To Do |

**US 状态计算规则**：
- ⏳ To Do：所有关联 task 都是 To Do
- 🔄 In Progress：至少一个 task 是 In Progress/In Review
- ✅ Done：所有关联 task 都是 Done

---

## 并行策略

### 并行组

| 并行组 | Task 列表 | 可并行条件 |
|--------|-----------|-----------|
| 组 1 | T-001, T-002, T-005 | 无冲突，可同时执行 |
| 组 2 | T-003, T-004 | 依赖组 1 完成 |

---

## 里程碑进度

| 里程碑 | 目标日期 | 需完成任务 | 完成情况 |
|--------|----------|-----------|----------|
| M1：基础设施完成 | YYYY-MM-DD | T-001, T-002, T-005 | ⏳ 进行中 |
| M2：核心功能完成 | YYYY-MM-DD | T-003, T-004 | ⏳ To Do |
| M3：测试完成 | YYYY-MM-DD | T-006 | ⏳ To Do |

---

## 导出说明

本文件是从 `iteration-plan.md` 导出的看板视图，用于快速浏览任务状态。

**操作规则**：
- Dev 在 `iteration-plan.md` 中领任务 + 更新状态
- 本文件仅供快速查看，不单独维护
- 如需更新状态，请编辑 `iteration-plan.md` 的第 2 节"任务看板"

---

## 关联文档

| 文档 | 路径 |
|------|------|
| 迭代计划（单一数据源） | `iteration-plan.md` |
| Session 状态 | `session-status.md` |