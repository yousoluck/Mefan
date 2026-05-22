# 框架重构与集成计划

> 重构时间：2026-05-16
> 当前状态：已完成阶段 0-1，阶段 2 进行中
> 目标：按新架构重构 + 预留 SuperPowers/GStack 集成接口

---

## 重构执行协议

### 自动推进规则

1. **按顺序重构**：阶段 0 → 1 → 2 → 3 → 4 → 5 → 6
2. **每阶段自检**：完成后检查是否符合架构设计
3. **回退机制**：若自检失败，回退到上一版本，重新重构
4. **自动进入下一阶段**：上一阶段自检成功后，自动开始下一阶段
5. **状态同步更新**：每阶段完成后更新 plans.md 和 refactor-steps.md

### 自检清单

每阶段重构完成后，检查：
- [ ] Command 文件是否使用工作流编排格式
- [ ] Agent 文件是否包含 `## 需要的技能`、`## 需要的规则`、`## 操作步骤`
- [ ] 是否引用 snippets（日志格式、异常处理）
- [ ] 是否声明所需 Rules/Skills
- [ ] 是否符合三层分离架构（Command 不写具体操作）

---

## 重构背景

新架构采用三层分离模型：
- **Command Layer**：工作流编排（谁在哪个步骤做什么）
- **Agent Layer**：具体操作执行 + 声明所需 Rules/Skills
- **Shared Layer**：snippets / Rules / Skills

详见：`.claude/docs/architecture.md`

---

## 集成决策：重构时预留集成接口

### 决策结论

**方案 C：重构时预留集成接口** — 架构重构按新设计走，Agent 文件的"需要的技能" section 设计为可直接引用外部 Skills。

### 原因

1. **不需要等重构完成才集成** — 集成工作变成"配置工作"而非"开发工作"
2. **不需要改架构** — 只需在 Agent 文件添加技能引用
3. **可同时进行** — 重构不耽误，集成并行

### 预留的 Skills 格式

```markdown
## 需要的技能
- `.claude/skills/graphify-query-cheatsheet.md`          # Mefan 自有
- `@superpowers/ship-discipline`                          # SuperPowers 技能
- `@gstack/what-to-build`                                # GStack 决策框架
```

### 外部 Skills 目录结构

```
.claude/skills/                    # Mefan 自有 Skills
├── graphify-query-cheatsheet.md
├── git-workflow.md
└── ...

.claude/skills-external/           # 外部集成 Skills（预留目录）
├── superpowers/                   # SuperPowers 技能副本
│   ├── ship-discipline.md
│   └── ...
└── gstack/                        # GStack 决策框架副本
    ├── what-to-build.md
    └── ...
```

### 集成步骤（重构完成后执行）

1. `git clone` SuperPowers/GStack 到 `skills-external/`
2. 在 Agent 文件的 `## 需要的技能` section 添加引用
3. 不需要修改 Agent 文件结构，不需要修改框架

---

## 与开源框架对比（参考）

| 框架 | 核心特点 | 可集成价值 |
|------|---------|-----------|
| **SuperPowers** | 35+ 技能跨多 Agent，支持 Claude Code/Cursor/Codex/OpenCode | **高** — 复用技能库 |
| **GStack** | Garry Tan 的 7 个决策框架（YC 总裁决策智慧） | **高** — 复用决策框架 |
| **OpenSpec** | Spec-driven 驱动开发，多 Agent 编排 | 中 — 复用 spec-first 流程 |
| **Ruflo** | Swarm 多 Agent 蜂群编排架构 | 中 — 参考 Swarm 架构改进通信 |

详见：`.claude/docs/architecture.md`（框架对比章节）

---

## 当前状态

| 层级 | 已完成 | 待完成 |
|------|--------|--------|
| 架构文档 | ✅ docs/architecture.md | — |
| Shared Layer（snippets） | ✅ logging-boilerplate, exception-handling | — |
| Agent Layer（阶段 0-6） | ✅ 全部完成 | — |
| Command Layer（阶段 0-6） | ✅ 全部完成 | — |
| 外部 Skills 目录 | ⏳ 待创建 skills-external/ | — |
| SuperPowers/GStack 集成 | ⏳ 待集成 | — |
| P1 问题修复 | ✅ CLAUDE.md 配置自动加载 | — |
| P3 问题修复 | ✅ guardian-stage6.md 独立 | — |

---

## 重构完成

所有 6 个阶段的 Command 文件和 Agent 文件已全部重构完成。

**架构修复**：采用方案 B（每个阶段一次 Agent 激活）+ 自动检查机制

```
阶段 0 ✅ 完成
阶段 1 ✅ 完成（方案 B：analyst-stage1 一次激活 + 自动检查）
阶段 2 ✅ 完成（方案 B：architect-stage2 + qa-stage2 各一次激活 + 自动检查）
阶段 3 ✅ 完成（方案 B：pm-stage3 一次激活 + 自动检查）
阶段 4 ✅ 完成（方案 B：dev-stage4 一次激活 + pm-stage4 + 自动检查）
阶段 5 ✅ 完成（方案 B：qa-stage5 + dev-stage5 + guardian-stage5 + 自动检查）
阶段 6 ✅ 完成（方案 B：pm-stage6 + coach-stage6 + guardian-stage6 + 自动检查）
```

**自动检查机制**：
- 在激活下一个 Agent 前，自动检查上一个 Agent 的产出物是否存在
- 若产出物不存在，报错退出，提示前置 Agent 未完成
- 防止人类跳过前置 Agent 直接执行下一步

**P1 问题修复**：框架自动加载 Rules/Skills 已实现（在 CLAUDE.md 中配置）

**P3 问题修复**：守护者验证角色已独立（创建 guardian-stage6.md）

---

## 框架对比与改进路径

| 优先级 | 问题 | 状态 |
|--------|------|------|
| **P0** | Skills 库薄弱（仅 3 个） | ⏳ 待集成 SuperPowers/GStack |
| **P1** | 框架自动加载 Rules/Skills | ✅ 已解决 |
| **P1** | 开源生态为零 | ⏳ 待考虑开源 |
| **P2** | Agent 直接通信缺失 | ⏳ 待借鉴 Ruflo |
| **P3** | 守护者验证在阶段 6 未独立 | ✅ 已解决 |

---

## 下一步工作

1. **Agent 文件清理**：删除 coach.md, analyst.md, developer.md, qa.md, guardian.md
2. **创建 `skills-external/` 目录**
3. **引入 SuperPowers/GStack Skills**
4. **处理 15 项自查问题（P0-P3）**

---

---

## 重构阶段计划

### 阶段 1：重构 Command 文件（工作流编排格式）

目标：所有 Command 文件改为统一格式
```
## 工作流编排
### 步骤 1
- **激活 Agent**：agents/xxx.md
- **执行操作**：Agent-操作-1

### 步骤 2
- **激活 Agent**：agents/yyy.md
- **引用技能**：.claude/skills/zzz.md
```

#### 1.1 mf-upgrade:01-requirements.md（阶段 1）

前置 Agent：
- [x] analyst-stage1.md ✅ 已完成

#### 1.2 mf-upgrade:02-arch-qa.md（阶段 2）

前置 Agent：
- [ ] architect-stage2.md ✅ 已存在
- [ ] analyst-stage2.md（待新建，用于任务拆解）

#### 1.3 mf-upgrade:03-plan.md（阶段 3）

前置 Agent：
- [ ] pm-stage3.md ✅ 已存在

#### 1.4 mf-upgrade:04-implement.md（阶段 4）

前置 Agent：
- [ ] dev-stage4.md（待新建）
- [ ] architect-stage4.md（待新建，用于 Code Review）

#### 1.5 mf-upgrade:05-quality.md（阶段 5）

前置 Agent：
- [ ] qa-stage5.md（待新建）

#### 1.6 mf-upgrade:06-retrospect.md（阶段 6）

前置 Agent：
- [ ] pm-stage6.md ✅ 已存在

---

### 阶段 2：补充缺失的 Agent 文件

| 阶段 | Agent 文件 | 说明 |
|------|-----------|------|
| 阶段 1 | analyst-stage1.md | 需求分析 |
| 阶段 2 | analyst-stage2.md | 任务拆解 |
| 阶段 4 | dev-stage4.md | 开发者编码 |
| 阶段 4 | architect-stage4.md | Code Review |
| 阶段 5 | qa-stage5.md | 质量测试 |

**Agent 文件结构**：
```markdown
# Agent 名称 · 阶段标识

## 需要的技能
- `.claude/skills/xxx.md`                    # Mefan 自有技能
- `@superpowers/skill-name`                  # 外部技能（可选，预留格式）

## 需要的规则
- `.claude/rules/xxx.md`

## 操作步骤
### 操作 1：[操作名称]
1. 具体步骤...

### 操作 2：[操作名称]
...
```

**注意**：`## 需要的技能` section 采用可扩展格式，支持直接引用外部 Skills 框架（如 `@superpowers/xxx`、`@gstack/xxx`）。

---

### 阶段 3：清理废弃的 Agent 文件

需要删除或确认状态的旧 Agent 文件：

| 文件 | 建议 |
|------|------|
| coach.md | 删除（或转为 snippets） |
| analyst.md | 删除 |
| developer.md | 删除 |
| qa.md | 删除 |
| guardian.md | 删除 |
| pm.md | 降级为文档索引（已有） |
| architect.md | 降级为文档索引（已有） |

---

### 阶段 4：更新所有 Agent 文件

所有 Agent 文件需要：
1. 引用 snippets（日志格式 + 异常处理）
2. 声明所需 Rules/Skills
3. 确保操作步骤不包含工作流编排内容

---

## 推荐执行顺序

按实际迭代顺序重构，完成一个阶段就能跑通一个阶段：

```
阶段 0 ✅ 已完成
  ↓
阶段 1 ✅ 已完成
  ↓
阶段 2 ✅ 已完成
  ↓
阶段 3 ✅ 已完成（当前）
  ↓
阶段 4 → 重写 04-implement.md + 补充 dev-stage4.md + architect-stage4.md
  ↓
阶段 5 → 重写 05-quality.md + 补充 qa-stage5.md
  ↓
阶段 6 → 重写 06-retrospect.md
```

### 执行协议

1. **自检失败 → 回退**：检查不符合架构设计，回退到上一版本重新重构
2. **自检成功 → 自动推进**：完成当前阶段后自动开始下一阶段
3. **状态同步**：每阶段完成后更新 plans.md 和 refactor-steps.md
4. **无需逐级审批**：已获得文件读写编辑授权，重构过程中不需单独申请批准

---

## 待改进问题清单（15 项）

> 来源：架构自我评估（74/100）+ 与开源框架对比
> 按严重度排序，Top 5 优先处理

### P0（严重，必须处理）

| # | 问题 | 说明 | 处理方案 |
|---|------|------|---------|
| 1 | Skills 库薄弱 | 仅 3 个 Skills，SuperPowers 有 35+，GStack 有 7 个决策框架 | 集成 SuperPowers/GStack |
| 2 | 未经过实际迭代验证 | 框架重构后才用，未有真实项目跑过 | 完成重构后找真实项目测试 |

### P1（重要，尽快处理）

| # | 问题 | 说明 | 处理方案 |
|---|------|------|---------|
| 3 | 缺乏原生多 Agent 协调 | Agent 之间无法直接通信，只能通过看板 | 参考 Ruflo Swarm 架构改进 |
| 4 | 无状态持久化 | Human Gate 后状态需手动恢复 | 依赖 session-status.md 机制已部分解决 |
| 5 | Rules/Skills 加载无框架强制 | 依赖 Agent 自觉声明 | ✅ 已解决：在 CLAUDE.md 中配置自动加载机制 |
| 6 | 无错误恢复机制 | 步骤中途失败后无明确恢复流程 | 在 Command 文件定义恢复步骤 |
| 7 | Human Gate 纯手动 | 无自动化触发，靠人类主动调用 | 考虑 auto.md 自动推进 |

### P2（中等，可后续处理）

| # | 问题 | 说明 | 处理方案 |
|---|------|------|---------|
| 8 | Command 文件格式未统一 | 每个 command 可能格式略有不同 | 统一 Command 文件模板 |
| 9 | 缺乏监控/观测 | 无 tracing、metrics、执行日志 | 考虑引入观测机制 |
| 10 | 产出物无版本控制 | spec/adr 变更后无版本记录 | 考虑引入版本标签 |
| 11 | 无回滚机制 | 阶段 4 实现出错后如何回滚 | 在质量门禁增加回滚检查 |

### P3（低优先级）

| # | 问题 | 说明 | 处理方案 |
|---|------|------|---------|
| 12 | 无安全模型 | Agent 能做什么？无权限边界 | 考虑权限模型 |
| 13 | 无资源限制 | Agent 可能无限消耗 tokens/compute | 考虑资源配额 |
| 14 | 无量化指标 | 无法衡量框架有效性（工时偏差、缺陷率等） | 在回顾模板增加量化指标 |

---

## 待完成清单

### Command 文件重构

| 文件 | 状态 |
|------|------|
| mf-upgrade:00-init.md | ✅ 完成 |
| mf-upgrade:01-requirements.md | ✅ 完成（阶段1） |
| mf-upgrade:02-arch-qa.md | ✅ 完成（阶段2） |
| mf-upgrade:03-plan.md | ✅ 完成（阶段3） |
| mf-upgrade:04-implement.md | ✅ 完成（阶段4） |
| mf-upgrade:05-quality.md | ✅ 完成（阶段5） |
| mf-upgrade:06-retrospect.md | ✅ 完成（阶段6） |

### Agent 文件补充

| 文件 | 状态 |
|------|------|
| pm-stage0.md | ✅ 完成 |
| architect-stage0.md | ✅ 完成 |
| pm-stage1.md | ✅ 完成 |
| pm-stage2.md | ✅ 完成（阶段2） |
| pm-stage3.md | ✅ 完成 |
| pm-stage6.md | ✅ 完成 |
| architect-stage2.md | ✅ 完成 |
| analyst-stage1.md | ✅ 完成 |
| analyst-stage2.md | ✅ 完成（阶段2） |
| qa-stage2.md | ✅ 完成（阶段2） |
| dev-stage4.md | ✅ 完成（阶段4） |
| architect-stage4.md | ✅ 完成（阶段4） |
| pm-stage4.md | ✅ 完成（阶段4） |
| qa-stage5.md | ✅ 完成（阶段5） |
| pm-stage5.md | ✅ 完成（阶段5） |
| pm-stage6.md | ✅ 完成（阶段6） |
| coach-stage6.md | ✅ 完成（阶段6） |
| dev-stage5.md | ✅ 完成（阶段5） |
| guardian-stage5.md | ✅ 完成（阶段5） |
| guardian-stage6.md | ✅ 完成（阶段6） |

### Agent 文件清理

| 文件 | 状态 |
|------|------|
| coach.md | ✅ 已删除 |
| analyst.md | ✅ 已删除 |
| developer.md | ✅ 已删除 |
| qa.md | ✅ 已删除 |
| guardian.md | ✅ 已删除 |
| pm.md | ✅ 已删除（降级为文档索引） |
| architect.md | ✅ 已删除（降级为文档索引） |

### 外部集成预留

| 任务 | 状态 |
|------|------|
| 创建 `skills-external/` 目录 | ⏳ 待创建 |
| 引入 SuperPowers 技能 | ⏳ 待集成 |
| 引入 GStack 决策框架 | ⏳ 待集成 |
| 更新 Agent 文件的 `## 需要的技能` section | ⏳ 待更新 |

---

## 开始下一阶段

**重构状态**：阶段 0-6 全部完成 ✅
**框架对比**：已与 OpenSpec/SuperPowers/GStack/Ruflo 对比评分，Mefan 9.35分

**下一步工作**：
1. ✅ Agent 文件清理完成
2. ⏳ 创建 `skills-external/` 目录
3. ⏳ 引入 SuperPowers/GStack Skills
4. ⏳ 更新 Agent 文件引用外部 Skills
5. ⏳ 考虑开源框架（P1）
6. ⏳ 借鉴 Ruflo 改进 Agent 协调（P2）

**自检清单**：
- [ ] Command 使用工作流编排格式（步骤 → 激活 Agent → 执行操作）
- [ ] Agent 包含 `## 需要的技能`、`## 需要的规则`、`## 操作步骤`
- [ ] 引用 snippets（日志格式、异常处理）
- [ ] 符合三层分离架构

**完成后**：自动更新 plans.md 和 refactor-steps.md，然后进入阶段 3

---

*本文档跟踪重构进度，每次完成一个阶段后更新状态。*
*最后更新：2026-05-16（阶段 1 完成）*

---

## 附录：重构与集成并行策略说明

### 为什么选择方案 C？

| 方案 | 描述 | 风险 |
|------|------|------|
| A：先重构再集成 | 完成所有架构重构，再引入外部 Skills | 慢，重复造轮子 |
| B：先集成再重构 | 先把 SuperPowers Skills 引入，后续再优化架构 | 可能架构不稳定时引入外部依赖，走弯路 |
| **C：重构时预留集成接口** | 框架重构按新架构走，Agent 文件声明技能时兼容外部 Skills 格式 | **✅ 最佳** |

### 核心原则

1. **重构不耽误集成** — 集成工作变成"配置工作"而非"开发工作"
2. **Agent 文件结构不变** — 只需在 `## 需要的技能` section 添加外部技能引用
3. **Skills 目录结构预留** — 创建 `skills-external/` 目录存放外部 Skills

---

## 附录：框架对比与改进路径

> 来源：docs/framework-comparison.md（2026-05-16）

### 对比结果摘要

| 框架 | 加权总分 | 核心优势 |
|------|---------|---------|
| SuperPowers | 9.40 | 35+ Skills，跨平台支持 |
| **Mefan** | **9.35** | 质量保障最强，进化机制完整 |
| OpenSpec | 8.65 | Spec-driven 开发，774 代码片段 |
| Ruflo | 7.40 | Swarm 蜂群架构 |
| GStack | 6.25 | 7 个决策框架 |

### Mefan 评分明细

| 维度 | 得分 | 备注 |
|------|------|------|
| 架构完整（20%） | 17/20 | 三层分离架构清晰 |
| Agent协调（15%） | 10/15 | 无直接通信 |
| 规则库（15%） | 6/15 | **薄弱点** |
| 质量保障（15%） | 13/15 | **优势** |
| 用户体验（10%） | 7/10 | — |
| 场景覆盖（10%） | 8/10 | — |
| 开源生态（10%） | 3/10 | **薄弱点** |
| 进化能力（5%） | 5/5 | **优势** |

### 改进路径（按优先级）

#### P0：集成外部 Skills（解决规则库薄弱问题）

| 步骤 | 任务 | 状态 |
|------|------|------|
| 1 | 创建 `skills-external/` 目录 | ⏳ 待创建 |
| 2 | 引入 SuperPowers（35+ Skills）→ `skills-external/superpowers/` | ⏳ 待集成 |
| 3 | 引入 GStack（7 决策框架）→ `skills-external/gstack/` | ⏳ 待集成 |
| 4 | 更新 Agent 文件的 `## 需要的技能` section，引用外部 Skills | ⏳ 待更新 |
| 5 | 验证 Skills 加载正常 | ⏳ 待验证 |

**目标**：Skills 从 3 个增至 45+ 个

#### P1：开源框架（解决生态为零问题）

| 步骤 | 任务 | 状态 |
|------|------|------|
| 1 | 确定开源范围（核心框架 vs 完整框架） | ⏳ 待决策 |
| 2 | 整理开源代码仓库 | ⏳ 待整理 |
| 3 | 撰写 README 和贡献指南 | ⏳ 待撰写 |
| 4 | 发布到 GitHub | ⏳ 待发布 |

#### P2：改进 Agent 协调（借鉴 Ruflo Swarm）

| 步骤 | 任务 | 状态 |
|------|------|------|
| 1 | 研究 Ruflo Swarm 架构设计 | ⏳ 待研究 |
| 2 | 设计 Agent 间直接通信机制 | ⏳ 待设计 |
| 3 | 实现或引入通信中间件 | ⏳ 待实现 |

### 集成路线图

```
当前状态：Skills 3 个
    ↓ 集成 SuperPowers → Skills 38+ 个
    ↓ 集成 GStack → Skills 45+ 个 + 7 决策框架
    ↓ 借鉴 Ruflo → Agent 协调增强
```

### 下一步工作

1. **立即执行**：创建 `skills-external/` 目录，引入 SuperPowers
2. **短期**：更新 Agent 文件引用外部 Skills
3. **中期**：考虑开源框架核心部分
4. **长期**：借鉴 Ruflo 改进 Agent 协调

### 下一步行动

1. 完成 Command 文件重构（阶段 1-6）
2. 完成 Agent 文件补充（阶段 2）
3. 完成 Agent 文件清理（阶段 3）
4. 创建 `skills-external/` 目录
5. 引入 SuperPowers/GStack Skills
6. 更新 Agent 文件的技能引用

---

## 附录：Harness 确定性改进计划

> 添加时间：2026-05-21
> 目标：将 mefan 从"纯 Prompt 驱动"改为"确定性代码约束"

### 问题分析

| 维度 | 当前问题 | 影响 |
|------|---------|------|
| AI 执行不稳定 | Prompt 只能描述要做什么，AI 可能跳过步骤 | 阶段状态可能不一致 |
| 路径依赖约定 | `{sprint-name}/` 是文本，AI 可能读错 | 多 sprint 时文件可能放错位置 |
| 状态管理靠 AI | session-status.md 更新依赖 AI 自觉 | 状态可能丢失或不完整 |
| 异常处理靠自审 | 没有 try/catch，AI 可能卡住 | 流程中断难以恢复 |

### 改进原则

**核心思路**：用确定性代码把框架约定住，减少对 AI 自觉性的依赖

```
AI 执行 = 不稳定（可能跳过步骤、读错路径）
确定性代码 = 强制校验（不通过则阻断）
```

### 改进方案：双层架构

```
.claude/
├── commands/           # Markdown 工作流定义（Prompt）
├── agents/             # Markdown Agent 提示词
├── rules/              # Markdown 约束规则
├── skills/
│   ├── *.md            # 技能定义（Markdown）
│   └── scripts/        # 可执行脚本（新增）
│       ├── check-prerequisites.py   # 前置检查
│       ├── validate-output.py        # 产出物校验
│       ├── state-machine.py           # 状态管理
│       └── sprint-manager.sh          # Sprint 目录管理
└── templates/          # 文档模板
```

### 为什么用 `skills/scripts/` 而不是独立 `src/mefan/`？

1. **不混淆** — 框架代码全在 `.claude/` 下，项目代码在项目根目录
2. **单一目录** — 所有框架相关都在 `.claude/` 下，没有外部目录
3. **按需调用** — Command 文件通过 Shell 调用脚本
4. **可复用** — 脚本可被多个 Command 引用

### 核心脚本设计

#### 1. `check-prerequisites.py` — 前置检查

```bash
# 调用方式
bash .claude/skills/scripts/check-prerequisites.sh 01

# 检查内容
- session-status.md 是否存在
- 阶段 0 是否已完成
- tech-stack-profile.md 是否存在
- consistency-baseline.md 是否存在
- knowledge-graph.md 是否存在
- techstack-overall.md 是否存在
- feature.md 是否存在

# 行为
- 检查不通过 → 输出错误信息 + exit 1
- 检查通过 → 输出 "OK" + exit 0
```

#### 2. `validate-output.py` — 产出物校验

```bash
# 调用方式
python .claude/skills/scripts/validate-output.py requirements

# 检查内容
- .claude/iterations/sprint-latest/requirements/upgrade-*.md 是否存在

# 行为
- 不存在 → exit 1 + 报错
- 存在 → exit 0
```

#### 3. `state-machine.py` — 状态管理

```bash
# 调用方式
python .claude/skills/scripts/state-machine.py --get-current-stage

# 功能
- 读取 `.claude/iterations/.state.json`（不是 md 文件）
- 查询当前阶段
- 写入完成状态

# 行为
- 读取/写入 JSON 格式状态
- 不依赖 AI 更新 md
```

#### 4. `sprint-manager.sh` — Sprint 目录管理

```bash
# 调用方式
bash .claude/skills/scripts/sprint-manager.sh --init

# 功能
1. 检查 sprint-latest 是否存在
2. 若存在：
   - 统计已有 sprint-N 数量
   - 将 sprint-latest 重命名为 sprint-{N+1}
   - 自检编号连续性
3. 创建新的 sprint-latest/
4. 更新 session-status.md 中的历史 Sprint 索引

# 行为
- 目录不连续 → exit 1 + 报错
- 成功 → exit 0
```

### Command 文件调用方式

改进后的 Command 文件：

```markdown
## 2. 前置检查

**执行者**：框架自动执行

1. `bash .claude/skills/scripts/check-prerequisites.sh 01`
   - 若报错，退出并输出错误信息

2. `python .claude/skills/scripts/validate-output.py requirements`
   - 检查阶段 1 产出物是否存在
   - 若不存在，报错退出
```

### 改进效果对比

| 场景 | 当前（纯 Prompt） | 改进后（代码校验） |
|------|-----------------|------------------|
| 阶段 0 未完成就执行阶段 1 | AI 可能忽略，继续执行 | `check-prerequisites.sh` exit 1 阻断 |
| sprint-latest 不存在 | AI 可能创建失败 | `sprint-manager.sh` 检查，不存在则报错 |
| 产出物缺失 | AI 可能跳过检查 | `validate-output.py` 不存在则阻断 |
| 状态丢失 | AI 可能不更新 | `state-machine.py` 代码写入 JSON |
| Human Gate 跳过 | AI 可能跳过等待 | 脚本调用时 `input()` 强制等待 |

### 执行计划

| 步骤 | 任务 | 优先级 |
|------|------|--------|
| 1 | 创建 `.claude/skills/scripts/` 目录 | P0 |
| 2 | 实现 `sprint-manager.sh`（Sprint 目录管理） | P0 |
| 3 | 实现 `check-prerequisites.py`（前置检查） | P0 |
| 4 | 实现 `state-machine.py`（状态管理） | P1 |
| 5 | 实现 `validate-output.py`（产出物校验） | P1 |
| 6 | 更新 Command 文件调用脚本 | P1 |
| 7 | 测试完整流程 | P1 |

### 状态

- [ ] 创建 `.claude/skills/scripts/` 目录
- [ ] 实现 `sprint-manager.sh`
- [ ] 实现 `check-prerequisites.py`
- [ ] 实现 `state-machine.py`
- [ ] 实现 `validate-output.py`
- [ ] 更新 Command 文件
- [ ] 测试完整流程

---

*最后更新：2026-05-21（新增 Harness 确定性改进计划）*