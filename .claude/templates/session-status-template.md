# Session Status Template

> 文件路径：`.claude/iterations/session-status.md`
> 更新时机：每个阶段完成后由 PM 更新
> **作用**：跨 sprint 全局追踪，记录所有 sprint 的状态和产出

---

## 迭代概览

| 字段 | 内容 |
|------|------|
| **迭代名称** | {sprint-name} |
| **开始日期** | |
| **预期结束日期** | |
| **场景** | upgrade |
| **目标描述** | |

---

## 自动推进状态

| 字段 | 内容 |
|------|------|
| **当前阶段** | N（0-6） |
| **已完成阶段** | [0, 1, 2, ...] |
| **阻塞标记** | {无 / 原因} |

---

## 阶段完成记录

> 每个阶段完成后，PM 必须更新此表

| 阶段 | 阶段名称 | 完成时间 | 产出物状态 | 备注 |
|------|---------|---------|-----------|------|
| 00 | 会话初始化 | | ✅/⏳/❌ | |
| 01 | 需求澄清 | | ✅/⏳/❌ | |
| 02 | 架构设计 | | ✅/⏳/❌ | |
| 03 | 迭代计划 | | ✅/⏳/❌ | |
| 04 | 迭代实现 | | ✅/⏳/❌ | |
| 05 | 质量测试 | | ✅/⏳/❌ | |
| 06 | 迭代总结 | | ✅/⏳/❌ | |

**状态说明**：✅ 已完成 | ⏳ 进行中/待处理 | ❌ 失败/缺失

---

## User Story 高层状态追踪

> 高层视图：快速了解各 US 的整体状态
> 详细追踪见 `sprint-status.md` 的 User Story 进度汇总

| User Story | US 状态 | 备注 |
|------------|---------|------|
| US-01 | ⏳ To Do | |
| US-02 | ⏳ To Do | |

**US 状态流转**：To Do → In Progress → Done
**更新时机**：sprint-status 中 task 状态变更时，由 PM 同步更新

---

## 产出物追踪表

> 每个阶段完成后，PM 更新对应条目状态

| 阶段 | 产出物 | 路径 | 状态 | 完成时间 |
|------|--------|------|------|---------|
| 00 | tech-stack-profile.md | `.claude/context/` | ✅ | |
| 00 | consistency-baseline.md | `.claude/context/` | ✅ | |
| 01 | requirements.md | `.claude/iterations/sprint-latest/requirements/` | ✅ | |
| 02 | adr.md | `.claude/iterations/sprint-latest/adr/` | ✅ | |
| 02 | test-plan.md | `.claude/iterations/sprint-latest/test-plan/` | ✅ | |
| 03 | iteration-plan.md | `.claude/iterations/sprint-latest/` | ✅ | |
| 03 | sprint-status.md | `.claude/iterations/sprint-latest/` | ✅ | |
| 04 | task-summary/T{NNN}.md | `.claude/iterations/sprint-latest/task-summary/` | ⏳ | |
| 05 | quality-report.md | `.claude/iterations/sprint-latest/test-results/` | ✅ | |
| 06 | iteration-retrospective.md | `.claude/iterations/sprint-latest/` | ✅ | |

---

## 历史 Sprint 索引

> 归档已完成迭代，由 PM 在每次新 sprint 创建时更新
> **路径基准**：`.claude/iterations/`

| Sprint 名称 | 开始日期 | 结束日期 | 状态 | 关键产出 |
|------------|---------|---------|------|---------|
| sprint-1 | | | ✅ Done | |
| sprint-2 | | | ✅ Done | |

**更新时机**：每次新 sprint 创建时，将上一个 sprint 追加到此表，并从 sprint-latest 重命名归档

---

## 异常记录

> 核心冲突、边缘冲突、处理决策

| 类型 | 描述 | 决策 | 时间 |
|------|------|------|------|
| 核心冲突 | | | |
| 边缘冲突 | | | |

---

## 实验规则/技能加载记录

> 来自 rules-proposed/ 和 skills-proposed/

| 类型 | 加载数 | 冲突处理 |
|------|--------|---------|
| 实验规则 | N | 稳定规则优先 |
| 实验技能 | N | 稳定技能优先 |

---

## PM 阶段完成报告（标准化格式）

> 每个阶段完成后，PM 必须按此格式填写并更新 session-status

```markdown
### 阶段 N 完成报告：{阶段名称}
- **完成时间**：YYYY-MM-DD HH:mm
- **执行摘要**：{一句话描述本阶段完成的核心内容}
- **关键产出**：
  - [产出1]：[路径] - ✅/⏳
  - [产出2]：[路径] - ✅/⏳
- **与上阶段的衔接**：{前置条件满足情况}
- **发现的问题**：{无/描述}
- **下一步**：进入阶段 N+1 的前置条件：{已满足/需补充}
- **需要 Human Gate 确认的事项**：{事项列表}
```

---

## 更新规则

| 操作 | 更新者 | 更新时机 |
|------|-------|---------|
| 阶段完成报告 | PM | 每个阶段完成后 |
| User Story 高层状态 | PM | sprint-status 中 task 状态变更时同步 |
| 产出物状态 | PM | 阶段产出确认时 |
| 异常记录 | PM | 冲突/问题发生时 |
| 阻塞标记 | PM/Auto | 阶段失败或恢复时 |

---

## 关联文档

| 文档 | 路径 | 说明 |
|------|------|------|
| Sprint 看板 | `sprint-status.md` | 详细 task 状态 + US 进度汇总 |
| 迭代计划 | `iteration-plan.md` | 任务拆解详情 |
| 任务详情 | `task-summary/T{NNN}.md` | 单任务实现详情 |