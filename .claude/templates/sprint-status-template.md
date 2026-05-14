# Sprint 看板

> 文件：`.claude/iterations/{sprint-name}/sprint-status.md`
> 创建时机：阶段 3（03-plan）创建
> 更新时机：任务状态变更时（由开发者/QA 更新）
> **sprint name = iteration name**

## 📊 仪表盘

| 字段 | 内容 |
|------|------|
| **迭代名称** | {sprint-name} |
| **迭代开始** | |
| **预期结束** | |
| **当前进度** | {已完成任务} / {总任务} = {百分比}% |
| **状态分布** | To Do: X \| In Progress: Y \| In Review: Z \| Done: W |
| **关键里程碑** | [ ] M1: 基线测试完成 \| [ ] M2: 集成测试全绿 |
| **当前异常** | {从日志中提取的未关闭异常} |

---

## 📋 任务看板

> 详细任务拆解见 `iteration-plan.md`

| 任务ID | 关联 US | 描述 | 状态 | 负责人 | 计划工时 | 实际工时 | 风险 | 技术债务 | 备注 |
|--------|---------|------|------|--------|---------|---------|------|---------|------|
| T001   | US-01   |      | To Do |        |         |         |      |         |      |
| T002   | US-01   |      | To Do |        |         |         |      |         |      |
| T003   | US-02   |      | To Do |        |         |         |      |         |      |

**状态流转**：To Do → In Progress → In Review → Done
**风险标记**：高/中/低
**技术债务**：若标记，简要说明
jdf 
---

## 📈 User Story 进度汇总

> 此表由 PM 根据下方任务看板自动汇总更新

| User Story | 关联 Task 数 | 已完成 | 进行中 | US 状态 |
|------------|-------------|--------|--------|---------|
| US-01 | 2 | 0 | 0 | ⏳ To Do |
| US-02 | 1 | 0 | 0 | ⏳ To Do |

**US 状态计算规则**：
- `⏳ To Do`：所有关联 task 都是 To Do
- `🔄 In Progress`：至少一个 task 是 In Progress/In Review
- `✅ Done`：所有关联 task 都是 Done

---

## 🔗 关联文档

| 文档 | 路径 |
|------|------|
| 迭代计划 | `iteration-plan.md` |
| 任务详情 | `task-summary/T{NNN}.md` |
| Session 状态 | `session-status.md` |

---

## 更新规则

| 操作 | 更新者 | 更新内容 |
|------|-------|---------|
| 领取任务 | 开发者 | 状态 To Do → In Progress |
| 提交 CR | 开发者 | 状态 In Progress → In Review |
| CR 通过 | 守护者 | 状态 In Review → Done |
| CR 驳回 | 守护者 | 状态 In Review → In Progress |
| 任务完成 | QA | 更新实际工时 |

**注意**：每当 task 状态变更时，PM 应同步更新 `session-status.md` 中的 User Story 状态追踪表。