# 框架重构记录

> 重构时间：2026-05-16
> 本文档记录框架架构重构的过程和决策

---

## 重构背景

阶段 0 重构过程中发现以下问题：

1. **Rules/Skills 集中声明但未使用** — Section 2 列出的规则/技能，在执行流程中未被真正读取
2. **Agent 跨阶段职责重叠** — pm.md/architect.md 包含所有阶段的操作，AI 拿到后不知自己处于哪个阶段
3. **Command 与 Agent 职责不清** — 两个都在写"做什么"，没有区分"编排"和"执行"

---

## 新架构：三层分离模型

```
┌─────────────────────────────────────────────────────────────┐
│                    Command Layer                           │
│         工作流编排层 · 人类与 Agent 之间的桥接              │
└─────────────────────────────────────────────────────────────┘
                              ↓ 激活 / 引用
┌─────────────────────────────────────────────────────────────┐
│                      Agent Layer                            │
│                    阶段执行层 · 具体操作                     │
└─────────────────────────────────────────────────────────────┘
                              ↓ 共享状态
┌─────────────────────────────────────────────────────────────┐
│                     Shared Layer                            │
│              共享片段 · Rules · Skills                      │
└─────────────────────────────────────────────────────────────┘
```

### 各层职责

| 层级 | 职责 |
|------|------|
| **Command** | 工作流编排（谁在哪个步骤做什么），不写具体操作 |
| **Agent** | 具体操作执行，声明自己需要的 Rules/Skills |
| **Shared** | snippets（日志格式、异常处理）、Rules、Skills |

### Rules/Skills 加载机制

- **Command** 引用 Rules/Skills（告诉全局这个阶段需要什么）
- **Agent** 声明自己需要什么（框架激活时自动加载）
- **按需引用**，不在阶段开头集中声明

### Agent 间通信机制

- Agent 通过 `sprint-status.md`（看板）共享状态
- 下一个 Agent 由 Command 显式调用，不是自己主动触发
- Human Gate 是阶段分界线

---

## 重构动作（阶段 0）

### 1. 重写 `mf-upgrade:00-init.md`

**变更**：
- 删除原 Section 2（规则集中声明），改为步骤内按需引用
- 改为工作流编排格式（"激活哪个 Agent，执行哪个操作"）
- 删除与 Agent 职责重叠的具体操作描述

### 2. 新建阶段 Agent 文件

| 文件 | 内容 |
|------|------|
| `agents/pm-stage0.md` | PM 阶段 0 操作 |
| `agents/architect-stage0.md` | Architect 阶段 0 操作 |
| `agents/pm-stage1.md` | PM 阶段 1 操作（从原 pm.md 恢复） |
| `agents/pm-stage3.md` | PM 阶段 3 操作（从原 pm.md 恢复） |
| `agents/pm-stage6.md` | PM 阶段 6 操作（从原 pm.md 恢复） |
| `agents/architect-stage2.md` | Architect 阶段 2 操作（从原 architect.md 恢复） |

### 3. 新建共享片段

| 文件 | 内容 |
|------|------|
| `snippets/logging-boilerplate.md` | 日志格式（所有 Agent 复用） |
| `snippets/exception-handling.md` | 异常处理表（所有 Agent 复用） |

### 4. 新建架构文档

- `docs/architecture.md` — 完整框架架构设计文档

### 5. 更新 README.md

- 新增第 3 节"框架架构设计"
- 引用 `docs/architecture.md`

---

## 重构后的架构原则

### Command 职责
- 只写"谁在哪个步骤做什么"（工作流编排）
- 不写具体操作步骤
- 引用 Rules/Skills（告诉全局需要什么）
- 标注 Human Gate 位置

### Agent 职责
- 只写具体操作步骤
- 声明自己需要的 Rules/Skills（框架激活时自动加载）
- 不知道自己在哪个阶段（文件名标识）
- 不负责工作流编排

### Shared Layer
- snippets（日志格式、异常处理表）跨阶段复用
- Rules/Skills 按需引用，不集中声明

---

## 关联文件

```
.claude/
├── docs/
│   └── architecture.md            # 新建：框架架构设计文档
├── snippets/                      # 新建：共享片段
│   ├── logging-boilerplate.md
│   └── exception-handling.md
├── commands/
│   └── mf-upgrade:00-init.md     # 重写：工作流编排格式
├── agents/
│   ├── pm-stage0.md             # 新建
│   ├── pm-stage1.md             # 新建
│   ├── pm-stage3.md             # 新建
│   ├── pm-stage6.md             # 新建
│   ├── architect-stage0.md      # 新建
│   ├── architect-stage2.md      # 新建
│   ├── pm.md                    # 降级为文档索引
│   └── architect.md             # 降级为文档索引
└── rules/global/
    └── session-init.md          # 保留
```

---

## 待完成项

| 任务 | 状态 |
|------|------|
| 创建 snippets/logging-boilerplate.md | ✅ 完成 |
| 创建 snippets/exception-handling.md | ✅ 完成 |
| 创建 docs/architecture.md | ✅ 完成 |
| 更新 README.md 架构章节 | ✅ 完成 |
| 更新所有 Agent 文件，引用 snippets | 待完成 |
| 更新所有 Agent 文件，声明所需 Rules/Skills | 待完成 |
| 更新 mf-upgrade:03-plan.md 等其他 Command | 待完成 |
| 删除废弃的 Agent 文件（coach.md, analyst.md 等） | ✅ 完成 |
| - 已删除：analyst.md, architect.md, coach.md, developer.md, qa.md, guardian.md | ✅ 完成 |
| **阶段 1 Command + Agent 重构** | ✅ 完成 |
| - 重写 mf-upgrade:01-requirements.md（工作流编排格式） | ✅ 完成 |
| - 新建 analyst-stage1.md（从 analyst.md 恢复内容） | ✅ 完成 |
| - 更新 pm-stage1.md（符合新 Agent 文件结构） | ✅ 完成 |
| **阶段 2 Command + Agent 重构** | ✅ 完成 |
| - 重写 mf-upgrade:02-arch-qa.md（工作流编排格式） | ✅ 完成 |
| - 新建 analyst-stage2.md（任务拆解） | ✅ 完成 |
| - 新建 qa-stage2.md（测试策略设计） | ✅ 完成 |
| - 新建 pm-stage2.md（PM 审查） | ✅ 完成 |
| **阶段 3 Command + Agent 重构** | ✅ 完成 |
| - 重写 mf-upgrade:03-plan.md（工作流编排格式） | ✅ 完成 |
| - 新建 analyst-stage3.md（任务拆解） | ✅ 完成 |
| - 更新 pm-stage3.md（符合新 Agent 文件结构） | ✅ 完成 |
| **阶段 4 Command + Agent 重构** | ✅ 完成 |
| - 重写 mf-upgrade:04-implement.md（工作流编排格式） | ✅ 完成 |
| - 新建 dev-stage4.md（开发者编码） | ✅ 完成 |
| - 新建 architect-stage4.md（Code Review） | ✅ 完成 |
| - 新建 pm-stage4.md（进度监控） | ✅ 完成 |
| **阶段 5 Command + Agent 重构** | ✅ 完成 |
| - 重写 mf-upgrade:05-quality.md（工作流编排格式） | ✅ 完成 |
| - 新建 qa-stage5.md（质量测试） | ✅ 完成 |
| - 新建 pm-stage5.md（P0/P1 缺陷决策） | ✅ 完成 |
| - 新建 dev-stage5.md（缺陷修复） | ✅ 完成 |
| - 新建 guardian-stage5.md（终审门禁） | ✅ 完成 |
| **阶段 6 Command + Agent 重构** | ✅ 完成 |
| - 重写 mf-upgrade:06-retrospect.md（工作流编排格式） | ✅ 完成 |
| - 更新 pm-stage6.md（符合新 Agent 文件结构） | ✅ 完成 |
| - 新建 coach-stage6.md（进化分析） | ✅ 完成 |
| **架构修复：方案 B（每个阶段一次 Agent 激活）** | ✅ 完成 |
| - 01-requirements.md：analyst-stage1 一次激活完成所有工作 | ✅ 完成 |
| - 02-arch-qa.md：architect-stage2 + qa-stage2 各一次激活 | ✅ 完成 |
| - 03-plan.md：pm-stage3 一次激活完成所有工作 | ✅ 完成 |
| - 04-implement.md：dev-stage4 一次激活完成所有工作 | ✅ 完成 |
| - 05-quality.md：qa-stage5 + dev-stage5 + guardian-stage5 | ✅ 完成 |
| - 06-retrospect.md：pm-stage6 + coach-stage6 | ✅ 完成 |
| **架构修复：添加自动检查机制** | ✅ 完成 |
| - 所有 Command 文件添加"自动检查上一 Agent 产出物"逻辑 | ✅ 完成 |
| - 在激活下一个 Agent 前检查上一 Agent 产出物是否存在 | ✅ 完成 |
| - 若产出物不存在则报错退出 | ✅ 完成 |
| **全部阶段重构完成** | ✅ 完成 |

---

*本文档为框架核心设计，所有重构必须遵循此架构。*
*最后更新：2026-05-16（阶段 0-6 全部完成）*