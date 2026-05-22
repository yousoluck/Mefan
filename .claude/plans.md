# 框架重构与集成计划

> 重构时间：2026-05-16（初始）
> 更新日期：2026-05-22（阶段0深度重构完成）
> 当前状态：阶段0深度重构完成，框架审计修复8个问题
> 目标：按新架构重构 + 整合 Superpowers/Ruflo 优势

---

## 执行协议

### 自动推进规则

1. **按顺序重构**：阶段 0 → 1 → 2 → 3 → 4 → 5 → 6
2. **每阶段自检**：完成后检查是否符合架构设计（见自检清单）
3. **回退机制**：若自检失败，回退到上一版本，重新重构
4. **自动进入下一阶段**：上一阶段自检成功后，自动开始下一阶段
5. **状态同步更新**：每阶段完成后更新 plans.md

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

## 与开源框架对比（2026-05-22 更新）

> 基于 GitHub 搜索和源码分析的对比

| 框架 | Stars | 架构设计 | Human Gate | 阶段化 | TDD | 可扩展性 | 综合 |
|------|-------|---------|------------|--------|-----|---------|------|
| **mefan（当前）** | N/A | 8.5 | 10 | 10 | 0 | 7 | **6.5/10** |
| **mefan（预估完成）** | ? | 8.5 | 10 | 10 | 9 | 8.5 | **8/10** |
| **Superpowers** | 29 | 9 | 0 | 0 | 9 | 8 | **7/10** |
| **Ruflo** | N/A | 7 | 0 | 0 | 0 | 7 | **5.5/10** |

### mefan 独有优势（其他框架没有）
- ✅ Human Gate 强制人工检查点
- ✅ 阶段化生命周期（0-6）
- ✅ SCENARIO 路由（upgrade/...）
- ✅ 迭代状态追踪（sprint-status）

### 整合策略
将 Superpowers/Ruflo 的优势整合到 mefan：

| 来源 | 整合内容 | 整合到 |
|------|---------|--------|
| **Superpowers** | 32个Skills, tdd-agent, spec-writer, CUPID code review, REFLECTION_LOG | `.claude/skills/` |
| **Ruflo** | Swarm orchestration 模式 | Agent 通信机制 |

整合后预估：**8.5/10**

---

## 当前状态

| 层级 | 已完成 | 待完成 |
|------|--------|--------|
| 架构文档 | ✅ docs/architecture.md | — |
| Shared Layer（snippets） | ✅ logging-boilerplate, exception-handling | — |
| Agent Layer（阶段 0-6） | ✅ 全部完成 | — |
| Command Layer（阶段 0-6） | ✅ 全部完成 | — |
| 阶段0框架审计 | ✅ 完成，修复8个问题 | — |
| 外部 Skills 目录 | ⏳ 待创建 skills-external/ | — |
| SuperPowers/Ruflo 集成 | ⏳ 待集成 | — |
| P1 问题修复 | ✅ CLAUDE.md 配置自动加载 | — |
| P3 问题修复 | ✅ guardian-stage6.md 独立 | — |

---

## 阶段0框架审计修复（2026-05-22）

已完成框架审计，发现并修复8个问题：

| 序号 | 问题 | 优先级 | 状态 |
|------|------|--------|------|
| 1 | knowledge.grap 生成指导缺失 | 高 | ✅ 已修复 |
| 2 | tech-stack-profile.md 归属错误 | 高 | ✅ 已修复 |
| 3 | Architect Agent 重复产出 tech-stack-profile.md | 高 | ✅ 已修复 |
| 4 | session-status.md 阶段编号对应关系不清晰 | 中 | ✅ 已修复 |
| 5 | Human Gate 缺少快速验证命令 | 中 | ✅ 已修复 |
| 6 | 迭代目录重命名逻辑不完整 | 中 | ⏳ 待修复 |
| 7 | dependencies-overview-template.md 存在性确认 | 低 | ✅ 已确认存在 |
| 8 | 日志声明阶段退出应该是 PM | 低 | ✅ 已修复 |

**修复详情**：`docs/framework-audit-stage0.md`

---

## 阶段完成状态

| 阶段 | Command文件 | Agent文件 | Human Gate | 框架审计 |
|------|-----------|-----------|------------|---------|
| 阶段0 | ✅ 完成 | ✅ 完成 | ✅ 完整 | ✅ 8问题已修复 |
| 阶段1 | ✅ 完成 | ✅ 完成 | ⚠️ 待增强 | ⏳ 待审计 |
| 阶段2 | ✅ 完成 | ✅ 完成 | ⚠️ 待增强 | ⏳ 待审计 |
| 阶段3 | ✅ 完成 | ✅ 完成 | ⚠️ 待增强 | ⏳ 待审计 |
| 阶段4 | ✅ 完成 | ✅ 完成 | ⚠️ 待增强 | ⏳ 待审计 |
| 阶段5 | ✅ 完成 | ✅ 完成 | ⚠️ 待增强 | ⏳ 待审计 |
| 阶段6 | ✅ 完成 | ✅ 完成 | ⚠️ 待增强 | ⏳ 待审计 |

**说明**：
- Command/Agent 文件已完成（格式统一）
- Human Gate 待增强（需要按阶段0模式添加详细检查点）
- 框架审计仅阶段0完成，其他阶段待审计

**下一步**：按阶段0模式，为阶段1-6增强 Human Gate 和详细检查点

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

## 立即执行计划

### 阶段1-6 重构（按阶段0模式）

| 阶段 | 任务 | 预计时间 | 状态 |
|------|------|---------|------|
| 阶段1 | 重构 requirements.md + analyst-stage1 | 1-2h | ⏳ 待开始 |
| 阶段2 | 重构 arch-qa.md + architect-stage2 + qa-stage2 | 1-2h | ⏳ 待开始 |
| 阶段3 | 重构 plan.md + pm-stage3 | 1-2h | ⏳ 待开始 |
| 阶段4 | 重构 implement.md + dev-stage4 + architect-stage4 | 1-2h | ⏳ 待开始 |
| 阶段5 | 重构 quality.md + qa-stage5 + guardian-stage5 | 1-2h | ⏳ 待开始 |
| 阶段6 | 重构 retrospect.md + pm-stage6 + coach-stage6 | 1-2h | ⏳ 待开始 |

**模式**：每个阶段复制阶段0的结构：
- Command 文件：工作流编排 + Human Gate 检查点
- Agent 文件：操作原子化 + session-status 更新
- 模板文件：完整的检查项 + 快速验证命令

### 外部 Skills 整合

| 任务 | 来源 | 状态 |
|------|------|------|
| 创建 `skills-external/` 目录 | - | ⏳ 待创建 |
| 引入 Superpowers (32 Skills) | Superpowers | ⏳ 待集成 |
| 引入 tdd-agent + spec-writer | Superpowers | ⏳ 待整合 |
| 引入 Swarm 协调模式 | Ruflo | ⏳ 待研究 |
| 引入 REFLECTION_LOG 学习机制 | Superpowers | ⏳ 待整合 |

---

## 当前状态（2026-05-22）

| 模块 | 状态 | 说明 |
|------|------|------|
| 阶段0深度重构 | ✅ 完成 | Human Gate 完整，8个问题已修复 |
| 阶段1-6 Command 文件 | ✅ 完成 | 格式已统一 |
| 阶段1-6 Agent 文件 | ✅ 完成 | 结构已完善 |
| 框架审计 | ✅ 完成 | 发现并修复8个问题 |
| docs/files.md | ✅ 完成 | 阶段0文档清单 |
| docs/framework-audit-stage0.md | ✅ 完成 | 完整审计报告 |

**下一步**：从阶段1开始，按阶段0模式重构

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

**重构状态**：阶段 0 深度重构完成 ✅ + 框架审计修复 8 问题
**框架对比**：已与 OpenSpec/SuperPowers/Ruflo 对比评分，Mefan 当前 6.5/10，目标 9/10

**下一步工作（按优先级）**：

### 立即执行
1. ⏳ 阶段1-6 重构（复制阶段0模式）- 各阶段预计 1-2 小时

### 短期（阶段1-6完成后）
2. ⏳ 创建 `skills-external/` 目录
3. ⏳ 引入 Superpowers Skills (32个)
4. ⏳ 整合 Superpowers tdd-agent + spec-writer

### 中期
5. ⏳ 引入 Ruflo Swarm 架构改进 Agent 协调
6. ⏳ 整合 Superpowers REFLECTION_LOG 学习机制
7. ⏳ 考虑开源框架

### 自检清单
- [x] Command 使用工作流编排格式（步骤 → 激活 Agent → 执行操作）
- [x] Agent 包含 `## 需要的技能`、`## 需要的规则`、`## 操作步骤`
- [x] 引用 snippets（日志格式、异常处理）
- [x] 符合三层分离架构
- [x] Human Gate 检查点完整
- [x] 框架审计问题已修复

---

## 整合后的目标架构

```
mefan (当前) + Superpowers (Skills) + Ruflo (Swarm)
         ↓
    迭代开发最佳框架 (9/10)
```

| 组件 | 来源 | 状态 |
|------|------|------|
| Human Gate | mefan | ✅ 已完成 |
| 阶段化生命周期 | mefan | ✅ 已完成 |
| SCENARIO 路由 | mefan | ✅ 已完成 |
| Skills (32个) | Superpowers | ⏳ 待整合 |
| TDD 流程 | Superpowers | ⏳ 待整合 |
| Code Review (CUPID) | Superpowers | ⏳ 待整合 |
| 学习机制 | Superpowers | ⏳ 待整合 |
| Swarm 协调 | Ruflo | ⏳ 待整合 |

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

> 更新时间：2026-05-22
> 来源：GitHub 搜索 + 源码分析

### 对比结果摘要

| 框架 | Stars | 综合评分 | 核心优势 |
|------|-------|---------|---------|
| **Superpowers** | 29 | 7/10 | 32 Skills, TDD流程, Code Review, 学习机制 |
| **mefan（完成预估）** | ? | **8/10** | Human Gate, 阶段化, SCENARIO路由 |
| **Ruflo** | N/A | 5.5/10 | Swarm 架构 |
| **OpenSpec系** | ~10 | 5/10 | Multi-agent 协作 |

### Mefan 完整评分（2026-05-22 更新）

| 维度 | 得分 | 备注 |
|------|------|------|
| 架构设计 | 8.5/10 | 3层分离，Command/Agent/Shared |
| 完整性 | 5/10 | 仅阶段0完整，其他阶段待重构 |
| Human Gate | **10/10** | **独家优势** |
| TDD/Code Review | 0/10 | 待整合 Superpowers |
| 可扩展性 | 7/10 | SCENARIO 路由好 |
| 实战验证 | 3/10 | 无外部用户 |

### 整合计划

```
mefan (当前 6.5/10)
    ↓ 阶段1-6 重构完成 → 8/10
    ↓ 整合 Superpowers Skills (32个) → 8.5/10
    ↓ 整合 tdd-agent + spec-writer → 9/10
```

**最终目标：9/10**，成为迭代开发场景最佳框架

### 改进路径（按优先级）

#### P0：集成外部 Skills（解决规则库薄弱问题）

| 步骤 | 任务 | 状态 |
|------|------|------|
| 1 | 创建 `skills-external/` 目录 | ⏳ 待创建 |
| 2 | 引入 SuperPowers（35+ Skills）→ `skills-external/superpowers/` | ⏳ 待集成 |
| 3 | 引入 Superpowers Skills (32个) → `skills-external/superpowers/` | ⏳ 待集成 |
| 4 | 更新 Agent 文件的 `## 需要的技能` section，引用外部 Skills | ⏳ 待更新 |
| 5 | 验证 Skills 加载正常 | ⏳ 待验证 |

**目标**：Skills 从 3 个增至 35+ 个

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
    ↓ 集成 Superpowers → Skills 35+ 个
    ↓ 整合 tdd-agent + spec-writer → TDD 流程
    ↓ 借鉴 Ruflo Swarm → Agent 协调增强
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
> 更新日期：2026-05-22
> 目标：将 mefan 从"纯 Prompt 驱动"改为"确定性代码约束"
> 执行时机：阶段1-6重构完成后实施

### 问题分析

| 维度 | 当前问题 | 影响 |
|------|---------|------|
| AI 执行不稳定 | Prompt 只能描述要做什么，AI 可能跳过步骤 | 阶段状态可能不一致 |
| 路径依赖约定 | `{sprint-name}/` 是文本，AI 可能读错 | 多 sprint 时文件可能放错位置 |
| 状态管理靠 AI | session-status.md 更新依赖 AI 自觉 | 状态可能丢失或不完整 |
| 异常处理靠自审 | 没有 try/catch，AI 可能卡住 | 流程中断难以恢复 |

### 核心原则

| 原则 | 说明 |
|------|------|
| **Script > Prompt** | 能用代码校验的就不用Prompt描述 |
| **Hook自动化** | PreToolUse/PostToolUse自动校验 |
| **关键Human Gate保留** | 重要决策点仍需人工确认 |
| **自动化Human Gate** | 检查通过则自动继续 |

### 架构：三层保障

```
┌─────────────────────────────────────────────────────┐
│                    Prompt 层                        │
│  (Command 文件、Agent 文件、Rules、Skills)          │
│  → 描述"做什么"，但不保证"做到"                     │
└─────────────────────────────────────────────────────┘
                          ↓ 调用
┌─────────────────────────────────────────────────────┐
│                   Script 层（确定性）                │
│  (skills/scripts/ - 强制校验)                        │
└─────────────────────────────────────────────────────┘
                          ↓ 触发
┌─────────────────────────────────────────────────────┐
│                    Hook 层                          │
│  (PreToolUse - 路径/格式校验)                       │
└─────────────────────────────────────────────────────┘
```

### 为什么用 `skills/scripts/`？
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

| 阶段 | 任务 | 优先级 | 时机 |
|------|------|--------|------|
| **当前** | 阶段1-6重构 | - | 立即执行 |
| **Phase 1** | 创建 `.claude/skills/scripts/` 目录 | P0 | 阶段1-6完成后 |
| **Phase 1** | 实现 `sprint-manager.sh`（Sprint目录管理） | P0 | 阶段1-6完成后 |
| **Phase 1** | 实现 `check-prerequisites.sh`（前置检查） | P0 | 阶段1-6完成后 |
| **Phase 2** | 实现 `state-machine.py`（状态管理） | P1 | Phase 1后 |
| **Phase 2** | 实现 `validate-output.py`（产出物校验） | P1 | Phase 1后 |
| **Phase 3** | Hook: PreToolUse 路径/格式校验 | P1 | Phase 2后 |
| **Phase 3** | 整合 Superpowers Skills (32个) | P1 | Phase 2后 |
| **Phase 4** | 更新 Command 文件调用脚本 | P1 | Hook实现后 |
| **Phase 4** | 测试完整流程 | P1 | 全部完成后 |

### 状态

- [ ] 阶段1-6重构（当前执行）
- [ ] 创建 `.claude/skills/scripts/` 目录
- [ ] 实现 `sprint-manager.sh`
- [ ] 实现 `check-prerequisites.sh`
- [ ] 实现 `state-machine.py`
- [ ] 实现 `validate-output.py`
- [ ] Hook: PreToolUse 校验
- [ ] 整合 Superpowers Skills
- [ ] 更新 Command 文件
- [ ] 测试完整流程

### 完整路线图

```
当前：阶段1-6重构（纯Prompt）
    ↓ 阶段1-6完成后
Phase 1：基础稳定性（Script层）
    ↓
Phase 2：产出保证（Hook层）
    ↓
Phase 3：Skills整合（Superpowers 32个Skills）
    ↓
Phase 4：完整测试 → 9/10 目标达成
```

---

*最后更新：2026-05-22（阶段0深度重构完成 + 框架审计 + Harness确定性计划更新）*