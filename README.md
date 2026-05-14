1. 目录结构
   1. 项目根目录/
   ├── .claude/                          # 【Claude Code 标准结构，安装时生成】
   │   ├── commands/                     # Command 入口文件（场景前缀命名）
   │   │   ├── mf-upgrade:00-init.md     → /mf-upgrade:00-init
   │   │   ├── mf-upgrade:01-requirements.md
   │   │   ├── mf-upgrade:02-arch-qa.md
   │   │   ├── mf-upgrade:03-plan.md
   │   │   ├── mf-upgrade:04-implement.md
   │   │   ├── mf-upgrade:05-quality.md
   │   │   ├── mf-upgrade:06-retrospect.md
   │   │   ├── mf-upgrade:auto.md
   │   │   └── mf-refactor:*/            → /mf-refactor:*
   │   ├── agents/                       # Agent 角色提示词（从 .mefan/ 复制）
   │   │   ├── pm.md
   │   │   ├── architect.md
   │   │   ├── analyst.md
   │   │   ├── developer.md
   │   │   ├── qa.md
   │   │   ├── guardian.md
   │   │   └── coach.md
   │   ├── rules/                        # Rules（从 .mefan/knowledge/ 重命名）
   │   │   ├── global/
   │   │   │   ├── session-init.md
   │   │   │   ├── quality-gates.md
   │   │   │   ├── exception-handling.md
   │   │   │   ├── tech-debt-management.md
   │   │   │   ├── harness-version-control.md
   │   │   │   ├── conflict-resolution.md
   │   │   │   ├── hook-vs-guardian.md
   │   │   │   └── logging.md
   │   │   ├── scenario-upgrade/         # 二次开发场景专用
   │   │   │   ├── consistency-first.md
   │   │   │   ├── api-compatibility.md
   │   │   │   └── reuse-before-build.md
   │   │   └── scenario-refactor/
   │   │       └── behavior-freeze.md
   │   └── skills/                       # 能力库（从 .mefan/skills/ 复制）
   │       ├── graphify-query-cheatsheet.md
   │       ├── query-third-party-docs.md
   │       ├── git-workflow.md
   │       ├── tdd-red-green-refactor.md
   │       ├── code-review-checklist.md
   │       ├── write-manual-test-guide.md
   │       ├── ug-triage-classification.md
   │   └── templates/                    # 模板（从 .claude/templates/ 复制）
   │       ├── session-status-template.md
   │       ├── tech-stack-profile-template.md
   │       └── ...
   │
   ├── .mefan/                           # 【框架自身存储位置】
   │   ├── CLAUDE.md                     # 项目宪法（含 SCENARIO 变量）
   │   ├── HARNESS_VERSION.md            # 框架版本
   │   ├── templates/                    # 模板源文件（安装时复制到 .claude/）
   │   ├── hooks/                        # 自动化检查脚本
   │   ├── hooks/                        # 自动化检查脚本
   │   │   ├── check-consistency.py
   │   │   ├── log-event.sh
   │   │   └── conversation-log.sh
   │   ├── context/                      # 全局技术上下文（跨迭代共享）
   │   │   ├── tech-stack-profile.md
   │   │   └── consistency-baseline.md
   │   ├── iterations/                   # 迭代总目录
   │   │   ├── mefan-log.md              # 全局日志
   │   │   ├── sprint-2026-05-14/        # 单个迭代
   │   │   │   ├── session-status.md
   │   │   │   ├── requirements/
   │   │   │   │   └── upgrade-2026-05-14-xxx.md
   │   │   │   ├── adr/
   │   │   │   │   └── upgrade-2026-05-14-xxx.md
   │   │   │   ├── test-plan/
   │   │   │   │   └── upgrade-2026-05-14-xxx.md
   │   │   │   ├── sprint-status.md
   │   │   │   ├── iteration-plan.md
   │   │   │   ├── task-summary/
   │   │   │   │   ├── T001.md
   │   │   │   │   └── ...
   │   │   │   ├── test-results/
   │   │   │   │   ├── regression-2026-05-14.log
   │   │   │   │   ├── manual-test-guide.md
   │   │   │   │   └── unit-T001.log
   │   │   │   ├── bug-log/
   │   │   │   │   ├── auto-2026-05-14.md
   │   │   │   │   └── manual-2026-05-14.md
   │   │   │   └── retrospective.md
   │   │   └── sprint-2026-05-28/
   │   │       └── ...
   │   ├── evolution-proposals/          # 进化提案
   │   │   └── upgrade-2026-05-14.md
   │   ├── reports/                      # 人类可读报告
   │   │   └── PROJECT_STATUS.md
   │   └── .claude/                      # Claude Code 配置（本地）
   │       └── settings.local.json
   │
   └── graphify-out/                    # 知识图谱（由工具生成）

2. 框架文件
层级	                 文件	               状态
Agent	           .claude/agents/pm.md	        ✅ 已加固
                   .claude/agents/architect.md	✅ 已加固
                   .claude/agents/analyst.md	✅ 已加固
                   .claude/agents/developer.md	✅ 已加固
                   .claude/agents/qa.md	        ✅ 已加固
                   .claude/agents/guardian.md	✅ 已加固
                   .claude/agents/coach.md	    ✅ 已加固
Command	           .claude/commands/mf-upgrade:00-init.md	✅ 可用 /mf-upgrade:00-init
                   .claude/commands/mf-upgrade:01-requirements.md	✅ 可用 /mf-upgrade:01-requirements
                   .claude/commands/mf-upgrade:02-arch-qa.md	✅ 可用 /mf-upgrade:02-arch-qa
                   .claude/commands/mf-upgrade:03-plan.md	✅ 可用 /mf-upgrade:03-plan
                   .claude/commands/mf-upgrade:04-implement.md	✅ 可用 /mf-upgrade:04-implement
                   .claude/commands/mf-upgrade:05-quality.md	✅ 可用 /mf-upgrade:05-quality
                   .claude/commands/mf-upgrade:06-retrospect.md	✅ 可用 /mf-upgrade:06-retrospect
                   .claude/commands/mf-upgrade:auto.md	✅ 可用 /mf-upgrade:auto
Template	       .claude/templates/session-status-template.md	✅
                   .claude/templates/tech-stack-profile-template.md	✅
                   .claude/templates/consistency-baseline-template.md	✅
                   .claude/templates/requirements-template.md	✅ 已加固
                   .claude/templates/adr-template.md	✅ 已加固
                   .claude/templates/test-plan-template.md	✅ 已加固
                   .claude/templates/iteration-plan-template.md	✅ 已加固
                   .claude/templates/sprint-status-template.md	✅ 已加固
                   .claude/templates/task-summary-template.md	✅ 已加固
                   .claude/templates/quality-report-template.md	✅ 已加固
                   .claude/templates/manual-test-guide-template.md	✅ 已加固
                   .claude/templates/bug-log-template.md	✅ 已加固
                   .claude/templates/iteration-retrospective-template.md	✅ 已加固
                   .claude/templates/evolution-proposal-template.md	✅ 已加固
                   .claude/templates/log-entry-template.md	✅ 已加固
                   .claude/templates/project-status-template.md	✅ 已加固
Rule	           .claude/rules/global/session-init.md	✅
                   .claude/rules/scenario-upgrade/consistency-first.md	✅
                   .claude/rules/scenario-upgrade/api-compatibility.md	✅
                   .claude/rules/scenario-upgrade/reuse-before-build.md	✅
                   .claude/rules/global/conflict-resolution.md	✅ 已加固
                   .claude/rules/global/exception-handling.md	✅ 已加固
                   .claude/rules/global/tech-debt-management.md	✅ 已加固
                   .claude/rules/global/hook-vs-guardian.md	✅ 已加固
                   .claude/rules/global/harness-version-control.md	✅ 已加固
                   .claude/rules/global/quality-gates.md	✅ 已加固
                   .claude/rules/global/logging.md	✅ 已加固
Skill	           .claude/skills/graphify-query-cheatsheet.md	✅ 核心
                   .claude/skills/git-workflow.md	✅ 已加固
                   .claude/skills/query-third-party-docs.md	✅ 已加固
                   .claude/skills/tdd-red-green-refactor.md	✅ 已加固
                   .claude/skills/code-review-checklist.md	✅ 已加固
                   .claude/skills/write-manual-test-guide.md	✅ 已加固
                   .claude/skills/ug-triage-classification.md	✅ 已加固
                   .claude/skills/root-cause-analysis.md	✅ 已加固
                   .claude/skills/pattern-extraction-from-logs.md	✅ 已加固
Hook	           .mefan/hooks/check-consistency.py	✅ 已提供
                   .mefan/hooks/log-event.sh	✅ 已提供
                   .mefan/hooks/conversation-log.sh	✅ 已提供
初始化	           .mefan/init-mefan-harness.sh	✅ 已提供（待更新）

---

## 3. 进度追踪体系

### 3.1 四层追踪架构

本框架采用**四层追踪架构**，从全局到任务逐级细化：

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 1: PROJECT STATUS (.mefan/reports/PROJECT_STATUS.md) │
│  全局视角 · 跨迭代追踪 · 决策层使用                           │
└─────────────────────────────────────────────────────────────┘
                              ↑
┌─────────────────────────────────────────────────────────────┐
│  Layer 2: SESSION STATUS (.mefan/iterations/{sprint-name}/session-status.md) │
│  迭代视角 · 阶段进度追踪 · 自动推进断点                        │
└─────────────────────────────────────────────────────────────┘
                              ↑
┌─────────────────────────────────────────────────────────────┐
│  Layer 3: SPRINT STATUS (.mefan/iterations/{sprint-name}/sprint-status.md)  │
│  看板视角 · 任务状态流转 · 执行层使用                           │
└─────────────────────────────────────────────────────────────┘
                              ↑
┌─────────────────────────────────────────────────────────────┐
│  Layer 4: TASK SUMMARY (.mefan/iterations/{sprint-name}/task-summary/*.md)  │
│  任务视角 · 单任务详情 · 开发者使用                             │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 各层职责定义

| 层级 | 文件 | 追踪粒度 | 更新时机 | 使用者 |
|------|------|---------|---------|-------|
| **L1 全局** | `PROJECT_STATUS.md` | 迭代维度 | 阶段6 + 人工更新 | PM/决策者 |
| **L2 迭代** | `session-status.md` | 阶段维度 | 每阶段完成时 | PM/Auto Command |
| **L3 看板** | `sprint-status.md` | 任务维度 | 任务状态变更时 | 开发者/QA |
| **L4 任务** | `task-summary/T{NNN}.md` | 原子维度 | 任务完成时 | 开发者 |

### 3.3 各层内容规范

#### L1: PROJECT_STATUS.md（全局项目状态）

```
PROJECT_STATUS.md
├── 🗓️ 整体迭代概况
│   ├── 总迭代数：已完成 N / 计划 N_total
│   └── 最近迭代：Sprint-YYYY-MM-DD，完成度 X%，工时偏差 ±Y%
├── 📋 需求完成矩阵
│   ├── User Story
│   ├── 所属迭代
│   ├── 拆解任务数
│   ├── 完成率
│   └── 状态
├── 🐛 缺陷分布（按模块/严重度）
├── 🧪 测试覆盖（单元/集成）
├── ⚙️ 技术债务清单（按模块/风险）
└── 🔄 框架进化状态（提案数/实验/采纳/驳回）
```

#### L2: SESSION-STATUS.md（迭代会话状态）

```
session-status.md
├── 当前迭代
│   ├── 迭代名称
│   ├── 开始日期
│   └── 预期结束日期
├── 自动推进状态        ← 【新增】追踪阶段进度
│   ├── 当前阶段：N
│   ├── 已完成阶段：[0, 1, 2, ...]
│   └── 阻塞标记：{无/原因}
├── 场景与目标
├── 范围清单
├── 依赖基础信息
├── 产出物追踪表        ← 【新增】记录每个阶段的产出
│   ├── 阶段0：tech-stack ✅ | consistency-baseline ✅
│   ├── 阶段1：requirements ✅
│   ├── 阶段2：adr ✅ | test-plan ✅
│   ├── 阶段3：iteration-plan ✅ | sprint-status ✅
│   ├── 阶段4：task-summary (T001-T00N) ⏳
│   ├── 阶段5：quality-report ✅
│   └── 阶段6：retrospective ✅
├── 异常记录            ← 核心冲突、边缘冲突处理结果
└── 实验规则/技能加载记录  ← 记录本次迭代加载的实验内容
```

#### L3: SPRINT-STATUS.md（看板状态）

```
sprint-status.md
├── 📊 仪表盘
│   ├── 迭代开始/预期结束
│   ├── 当前进度：已完成/总任务 = X%
│   ├── 状态分布：To Do X | In Progress Y | In Review Z | Done W
│   └── 关键里程碑（基线测试✓ | 集成测试✓）
├── 📋 任务看板
│   ├── 任务ID | 描述 | 状态 | 负责人 | 计划工时 | 实际工时 | 风险 | 技术债务
│   └── 状态流转：To Do → In Progress → In Review → Done
└── 关联文档
    └── 迭代计划：iteration-plan.md（包含任务拆解详情、里程碑定义）
```

#### L4: TASK-SUMMARY/T{NNN}.md（单任务详情）

```
task-summary/T{NNN}.md
├── 任务基本信息
│   ├── 任务ID | 描述 | 类型 | 关联模块
│   ├── 计划工时 | 实际工时
│   └── 状态：Done
├── 修改清单
│   ├── 新增文件
│   ├── 修改文件
│   └── 删除文件
├── 新增API
│   ├── 路径 | 方法 | 说明
├── 技术债务
│   └── 债务描述 | 风险
└── 优化建议
```

### 3.4 阶段与产出物追踪（闭环表）

> 合并产出追踪与更新职责：每个阶段的产出物、路径、状态记录位置、更新者一目了然

| 阶段 | 产出物 | 完整路径 | 更新者 | 更新时机 | 更新内容 |
|------|--------|----------|--------|---------|---------|
| **00** | tech-stack-profile.md | `.mefan/context/` | 架构师 | 阶段完成时 | 技术栈组件列表 |
| **00** | consistency-baseline.md | `.mefan/context/` | 架构师 | 阶段完成时 | 基线条目 + 证据 |
| **00** | session-status.md | `.mefan/iterations/{sprint-name}/` | PM | 阶段完成时 | 自动推进状态、产出物追踪表、PM 报告 |
| **01** | requirements.md | `.mefan/iterations/{sprint-name}/requirements/` | 分析师 | 阶段完成时 | 需求文档（完整填写） |
| **02** | adr.md | `.mefan/iterations/{sprint-name}/adr/` | 架构师 | 阶段完成时 | 方案对比、详细设计、参考实现 |
| **02** | test-plan.md | `.mefan/iterations/{sprint-name}/test-plan/` | QA | 阶段完成时 | 回归范围、新增场景、质量门槛 |
| **03** | iteration-plan.md | `.mefan/iterations/{sprint-name}/` | PM | 阶段完成时 | 用户故事、任务清单、里程碑、WIP 限制 |
| **03** | sprint-status.md | `.mefan/iterations/{sprint-name}/` | PM | 阶段完成时 | 任务看板初始化（全任务 To Do） |
| **04** | task-summary/T{NNN}.md | `.mefan/iterations/{sprint-name}/task-summary/` | 开发者 | 任务完成时 | 修改清单、新 API、技术债务 |
| **04** | unit-T{NNN}.log | `.mefan/iterations/{sprint-name}/test-results/` | 开发者 | 测试执行时 | 单元测试输出 |
| **04** | violations.json | `.mefan/iterations/{sprint-name}/` | Hook（自动） | 每次拦截时 | 违规记录 |
| **05** | regression-YYYY-MM-DD.log | `.mefan/iterations/{sprint-name}/test-results/` | QA | 测试执行时 | 回归测试结果 |
| **05** | manual-test-guide.md | `.mefan/iterations/{sprint-name}/test-results/` | QA | 阶段完成时 | 测试用例、操作步骤、判定标准 |
| **05** | quality-report.md | `.mefan/iterations/{sprint-name}/test-results/` | QA | 缺陷修复完成后 | 测试覆盖、缺陷统计、质量就绪声明 |
| **05** | bug-log/auto-YYYY-MM-DD.md | `.mefan/iterations/{sprint-name}/bug-log/` | QA | 发现缺陷时 | 缺陷分类、根因分析 |
| **05** | bug-log/manual-YYYY-MM-DD.md | `.mefan/iterations/{sprint-name}/bug-log/` | QA | 人工测试反馈时 | 缺陷分类、根因分析 |
| **06** | retrospective.md | `.mefan/iterations/{sprint-name}/` | PM | 阶段完成时 | 迭代概览、缺陷分析、待改进项 |
| **06** | evolution-proposal.md | `.mefan/evolution-proposals/` | 进化教练 | 阶段完成时 | 提案触发原因、草案、预期效果 |
| **06** | PROJECT_STATUS.md | `.mefan/reports/` | PM | 阶段完成时 | 迭代概况、需求矩阵、缺陷分布、技术债务 |
| **06** | CHANGELOG.md | `CHANGELOG.md`（根目录） | PM | 阶段完成时 | 功能和修复追加 |
| **06** | HARNESS_VERSION.md | `.mefan/HARNESS_VERSION.md` | PM | 阶段完成时 | 语义版本递增 |
| 全局 | mefan-log.md | `.mefan/iterations/mefan-log.md` | 所有 Agent | 每次操作 | 阶段进入/退出、异常、Human Gate 审批 |

### 3.5 AUTO COMMAND 断点续跑机制

auto.md 通过 **L2 session-status.md + L3 sprint-status.md** 共同实现断点续跑：

```
启动 auto
    ↓
读取 session-status.md
    ↓
检查 ## 自动推进状态
    ├── 当前阶段：N
    ├── 已完成阶段：[0, 1, ..., N-1]
    └── 阻塞标记：无 / 原因
    ↓
循环执行（当前阶段 N → 6）
    ↓
每个阶段开始前：
    1. 检查 session-status 产出物追踪表，验证前置文件存在
    2. 若有文件缺失 → 报错退出，说明缺少的阶段
    3. 若有阻塞标记 → 等待人类决策（重试/回退/跳过）
    ↓
每个阶段完成后（按阶段分别判断）：
    ├── 阶段 0-3, 5-6：检查 session-status 产出物追踪表是否标记 ✅
    └── 阶段 4：检查 sprint-status 所有 task 是否全部 Done
        └── 若未全部 Done，设置阻塞标记"阶段4进行中：X/N task 完成"
    ↓
    1. 更新 L2 自动推进状态（当前阶段 +1，已完成追加 N）
    2. 更新 L2 阶段完成记录（标记阶段 N 为 ✅）
    3. 更新 L2 产出物追踪表（标记阶段 N 产出物为 ✅）
    4. 填写 L2 PM 阶段完成报告（标准化格式）
    5. 更新 L3 sprint-status（若阶段 4 完成，更新 US 进度汇总）
    6. 等待 Human Gate（若有）
    ↓
全部完成 → 退出