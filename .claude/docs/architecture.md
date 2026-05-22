# Mefan 框架架构设计

> 本文档定义 Mefan 框架的核心架构原则和分层模型。
> 所有后续重构必须遵循本文档的设计。

---

## 1. 三层分层架构

Mefan 框架采用**三层分离架构**：

```
┌─────────────────────────────────────────────────────────────┐
│                    Command Layer (Playbook)                 │
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

---

## 2. 各层职责

### 2.1 Command Layer（命令层）

**职责**：工作流编排，是人类调用框架的入口

**具体内容**：
- 阶段标识（当前阶段编号和名称）
- 工作流编排（在哪个步骤激活哪个 Agent）
- 规则/技能引用（按需，不提前集中声明）
- 产出物清单
- Human Gate 位置

**关键原则**：
- Command 不写具体操作步骤
- Command 只写"谁在哪个步骤做什么"
- Command 通过文件名（`mf-upgrade:00-init.md`）标识阶段

**文件位置**：
```
.claude/commands/mf-upgrade:00-init.md
.claude/commands/mf-upgrade:01-requirements.md
...
```

---

### 2.2 Agent Layer（Agent 层）

**职责**：阶段内具体操作执行

**Agent 文件结构**：

```markdown
# Agent 名称 · 阶段标识

## 需要的技能
- `.claude/skills/xxx.md`

## 需要的规则
- `.claude/rules/xxx.md`

## 操作步骤
### 操作 1：[操作名称]
1. 具体步骤...
2. 具体步骤...

### 操作 2：[操作名称]
...
```

**关键原则**：
- Agent 不写工作流编排（不知道自己在哪个阶段）
- Agent 知道自己被哪个 Command 调用
- Agent 通过文件名（`pm-stage0.md`）标识角色和阶段
- Agent 激活时，框架自动加载其声明的 Rules/Skills

**文件位置**：
```
.claude/agents/pm-stage0.md
.claude/agents/architect-stage0.md
.claude/agents/pm-stage1.md
.claude/agents/architect-stage2.md
.claude/agents/pm-stage3.md
.claude/agents/pm-stage6.md
...
```

---

### 2.3 Shared Layer（共享层）

**职责**：跨阶段共享的内容

**包含三类**：

| 类型 | 内容 | 位置 |
|------|------|------|
| **Snippets** | 日志格式命令、异常处理表 | `.claude/snippets/` |
| **Rules** | 约束性规则（session-init、consistency-first 等） | `.claude/rules/` |
| **Skills** | 能力库（graphify-query、git-workflow 等） | `.claude/skills/` |

**Snippets 示例**：
```
.claude/snippets/logging-boilerplate.md    # 日志命令格式
.claude/snippets/exception-handling.md     # 异常处理表
```

---

## 3. 分层通信机制

### 3.1 Command → Agent 通信

```
mf-upgrade:00-init.md（Command）
└── "步骤 2：激活 agents/pm-stage0.md，执行 PM-操作-1 + PM-操作-2"
    ↓ 框架调用
pm-stage0.md（Agent）
└── 执行具体操作
```

Command 在工作流中明确写"激活哪个 Agent 文件，执行哪个操作"。

### 3.2 Agent ↔ Agent 通信（共享状态）

```
dev-stage4.md（DEV Agent）
└── 完成任务后 → 写入 sprint-status.md（task 状态改为 Done）
    ↓
architect-stage4.md（Architecture Agent）
└── 被 Command 04 调用 → 读取 sprint-status.md → 发现 T001 Done → 执行 Code Review
```

**核心**：Agent 之间不直接通信，通过共享状态（`sprint-status.md` 看板）间接协调。

### 3.3 Human Gate

Human Gate 是阶段分界线，AI 无法自行跨越。Command 在工作流中标注 Human Gate 位置。

---

## 4. Command 与 Agent 的边界

| 层级 | 写什么 | 不写什么 |
|------|--------|---------|
| **Command** | 工作流编排、规则引用、产出物清单、Human Gate 位置 | 具体操作步骤 |
| **Agent** | 具体操作步骤、所需技能/规则声明 | 工作流编排 |

**示例对比**：

```markdown
# mf-upgrade:00-init.md（Command）
## 2. 工作流编排

### 2.1 环境确认
- **激活 Agent**：`agents/pm-stage0.md`
- **执行操作**：PM-操作-1（SCENARIO 确认）+ PM-操作-2（session-status 初始化）

### 2.2 技术栈分析
- **激活 Agent**：`agents/architect-stage0.md`
- **执行操作**：Architect-操作-1（技术栈分析）
- **引用技能**：`.claude/skills/graphify-query-cheatsheet.md`
```

```markdown
# pm-stage0.md（Agent）

## 需要的技能
- `.claude/skills/graphify-query-cheatsheet.md`

## 操作步骤

### PM-操作-1：SCENARIO 确认
1. 读取 CLAUDE.md 中的 SCENARIO 变量
2. 若值不为 `upgrade`，报错退出

### PM-操作-2：session-status 初始化
1. 检查 `.claude/iterations/session-status.md` 是否存在
2. 若不存在，使用模板生成
3. 初始化阶段 0 完成记录（状态 ⏳）
```

---

## 5. Agent 间通信：DEV → Architecture（Code Review 示例）

```
mf-upgrade:04-implement.md（Command）
├── "步骤 1：激活 dev-stage4.md 执行 T001 编码"
├── "步骤 2：DEV 完成后在 sprint-status.md 标记 T001 Done"
└── "步骤 3：激活 architect-stage4.md 执行 Code Review"

dev-stage4.md（DEV Agent）
├── 执行编码
└── 写入 sprint-status.md：T001 = Done

architect-stage4.md（Architecture Agent）
├── 被激活后读取 sprint-status.md
├── 发现 T001 Done
└── 执行 Code Review，写入评审结果
```

**关键**：Architecture Agent 不是自己主动触发的，是被 Command（通过 PM）显式调用。

---

## 6. Rules/Skills 加载机制

### 6.1 职责划分

| 位置 | 职责 |
|------|------|
| **Command** | 引用 Rules/Skills（告诉全局这个阶段需要什么） |
| **Agent** | 声明自己需要什么（确保被激活时能正确执行） |
| **框架** | 激活 Agent 时，自动加载 Agent 声明的依赖 |

### 6.2 示例

```markdown
# mf-upgrade:00-init.md（Command）
### 3.2 技术栈分析
- **激活 Agent**：`agents/architect-stage0.md`
- **引用技能**：`.claude/skills/graphify-query-cheatsheet.md`
```

```markdown
# architect-stage0.md（Agent）

## 需要的技能
- `.claude/skills/graphify-query-cheatsheet.md`

## 操作步骤
### Architect-操作-1：技术栈分析
1. 使用 graphify query "..." 查询项目模式
2. ...
```

框架激活 `architect-stage0.md` 时，自动加载 `graphify-query-cheatsheet.md`。

---

## 7. 目录结构

```
.claude/
├── commands/                      # Command Layer
│   ├── mf-upgrade:00-init.md      # 阶段 0：会话初始化
│   ├── mf-upgrade:01-requirements.md  # 阶段 1：需求澄清
│   ├── mf-upgrade:02-arch-qa.md   # 阶段 2：架构设计
│   ├── mf-upgrade:03-plan.md      # 阶段 3：迭代计划
│   ├── mf-upgrade:04-implement.md # 阶段 4：迭代实现
│   ├── mf-upgrade:05-quality.md   # 阶段 5：质量测试
│   └── mf-upgrade:06-retrospect.md # 阶段 6：迭代总结
│
├── agents/                        # Agent Layer
│   ├── pm-stage0.md              # PM - 阶段 0
│   ├── pm-stage1.md              # PM - 阶段 1
│   ├── pm-stage3.md              # PM - 阶段 3
│   ├── pm-stage6.md              # PM - 阶段 6
│   ├── architect-stage0.md      # Architect - 阶段 0
│   ├── architect-stage2.md      # Architect - 阶段 2
│   ├── architect-stage4.md      # Architect - 阶段 4（Code Review）
│   └── ...                        # 其他 Agent 文件
│
├── snippets/                      # Shared Layer - Snippets
│   ├── logging-boilerplate.md    # 日志格式（所有 Agent 复用）
│   └── exception-handling.md      # 异常处理表（所有 Agent 复用）
│
├── rules/                         # Shared Layer - Rules
│   ├── global/                   # 全局规则
│   │   ├── session-init.md       # 必选
│   │   ├── quality-gates.md      # 必选
│   │   └── ...
│   └── scenario-upgrade/          # 场景规则
│
├── skills/                        # Shared Layer - Skills
│   ├── graphify-query-cheatsheet.md
│   ├── git-workflow.md
│   └── ...
│
└── templates/                    # 模板文件
```

---

## 8. 核心原则总结

| 原则 | 说明 |
|------|------|
| **Command 是编排层** | 只写"谁在哪个步骤做什么"，不写具体操作 |
| **Agent 是执行层** | 只写"怎么做"，不知道自己处于哪个阶段 |
| **Human Gate 是分界线** | AI 无法自行跨越阶段 |
| **Rules/Skills 按需引用** | 不在阶段开头集中声明，在步骤中按需引用 |
| **Agent 声明所需依赖** | 框架激活时自动加载 |
| **共享状态协调通信** | Agent 通过 `sprint-status.md` 间接通信 |
| **下一个 Agent 由 Command 调用** | 不是自己主动触发 |

---

## 9. 待完成项

| 任务 | 状态 |
|------|------|
| 创建 `snippets/logging-boilerplate.md` | 待完成 |
| 创建 `snippets/exception-handling.md` | 待完成 |
| 更新 `mf-upgrade:00-init.md` 为正确的工作流编排格式 | 待完成 |
| 在 Agent 文件中声明所需 Rules/Skills | 待完成 |
| 更新 README.md 架构章节 | 待完成 |
| 删除废弃的 Agent 文件 | 待完成 |

---

*本文档为框架核心设计，所有重构必须遵循此架构。*
*最后更新：2026-05-16*