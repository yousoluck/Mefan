# 阶段 0 文档生成统计

> 本文件记录阶段 0（会话初始化）期间生成的所有文档
> 生成时间：2026-05-22
> 统计范围：PM-Stage0、Architect-Stage0、Analyst-Stage0

---

## 文档总览

| 序号 | 文档名称 | 生成 Agent | 操作编号 | 文件路径 | 作用说明 |
|------|---------|-----------|---------|---------|---------|
| 1 | session-status.md | PM-Stage0 | 0.2.3 创建 / 0.5 更新 | `.claude/iterations/session-status.md` | 全局会话状态追踪，跨 sprint 记录阶段完成状态、产出物追踪、自动推进状态 |
| 2 | project.md | PM-Stage0 | 0.3 | `.claude/context/project.md` | 项目概述文档，记录项目基本信息、技术背景、迭代历史 |
| 3 | tech-stack-profile.md | PM-Stage0 | 0.4 | `.claude/context/tech-stack-profile.md` | 技术栈档案，详细记录前后端框架、数据库、工具链等 |
| 4 | consistency-baseline.md | Architect-Stage0 | 0.2 | `.claude/context/consistency-baseline.md` | 一致性基线，代码风格、设计模式、命名规范、反模式 |
| 5 | dependencies-overview.md | Architect-Stage0 | 0.3 | `.claude/context/dependencies-overview.md` | 依赖全景图，核心模块依赖关系、外部依赖清单、循环依赖检测 |
| 6 | feature.md | Analyst-Stage0 | 0.5 | `.claude/iterations/sprint-latest/feature.md` | 功能需求文档，功能要点列表、详细分析、澄清对话记录 |

---

## 文档详情

### 1. session-status.md

| 字段 | 内容 |
|------|------|
| **生成 Agent** | PM-Stage0 |
| **操作编号** | 0.2.3（创建）、0.5（更新） |
| **文件路径** | `.claude/iterations/session-status.md` |
| **作用** | 全局会话状态追踪，跨 sprint 记录阶段完成状态、产出物追踪、自动推进状态 |
| **模板来源** | `.claude/templates/session-status-template.md` |

**更新日志**：
- PM-Stage0 操作 0.5：更新阶段完成记录、产出物追踪表、自动推进状态、PM阶段完成报告
- Architect-Stage0 操作 0.5：更新 consistency-baseline.md、dependencies-overview.md 状态
- Analyst-Stage0 操作 0.7：更新 feature.md 状态

---

### 2. project.md

| 字段 | 内容 |
|------|------|
| **生成 Agent** | PM-Stage0 |
| **操作编号** | 0.3 |
| **文件路径** | `.claude/context/project.md` |
| **作用** | 项目概述文档，记录项目基本信息、技术背景、迭代历史 |
| **模板来源** | `.claude/templates/project-template.md` |

**迭代历史更新**：
- PM-Stage0 操作 0.3：初始化 `### 迭代 sprint-latest` 章节
- PM-Stage0 操作 5.6：更新 project.md、tech-stack-profile.md、session-status.md 状态
- Architect-Stage0 操作 5.6：更新 consistency-baseline.md、dependencies-overview.md 状态
- Analyst-Stage0 操作 0.6：更新 feature.md 状态

---

### 3. tech-stack-profile.md

| 字段 | 内容 |
|------|------|
| **生成 Agent** | PM-Stage0 |
| **操作编号** | 0.4 |
| **文件路径** | `.claude/context/tech-stack-profile.md` |
| **作用** | 技术栈档案，详细记录前后端框架、数据库、工具链、依赖版本 |
| **模板来源** | `.claude/templates/tech-stack-profile-template.md` |

---

### 4. consistency-baseline.md

| 字段 | 内容 |
|------|------|
| **生成 Agent** | Architect-Stage0 |
| **操作编号** | 0.2 |
| **文件路径** | `.claude/context/consistency-baseline.md` |
| **作用** | 一致性基线，提取项目代码风格、设计模式、命名规范、反模式，为 Dev Agent 提供开发参考 |
| **模板来源** | `.claude/templates/consistency-baseline-template.md` |
| **前置条件** | 如果已存在则跳过（用户可能从上一次迭代继续） |

---

### 5. dependencies-overview.md

| 字段 | 内容 |
|------|------|
| **生成 Agent** | Architect-Stage0 |
| **操作编号** | 0.3 |
| **文件路径** | `.claude/context/dependencies-overview.md` |
| **作用** | 依赖全景图，核心模块依赖关系、外部依赖清单、循环依赖检测、关键发现 |
| **模板来源** | `.claude/templates/dependencies-overview-template.md` |
| **前置条件** | 如果已存在则跳过 |

---

### 6. feature.md

| 字段 | 内容 |
|------|------|
| **生成 Agent** | Analyst-Stage0 |
| **操作编号** | 0.5 |
| **文件路径** | `.claude/iterations/sprint-latest/feature.md` |
| **作用** | 功能需求文档，包含功能要点列表、详细分析、澄清对话记录、非功能需求、验收标准 |
| **模板来源** | `.claude/templates/feature-template.md` |

---

## 目录结构

```
.claude/
├── context/                      # 项目上下文文档
│   ├── project.md               # 项目概述
│   ├── tech-stack-profile.md     # 技术栈档案
│   ├── consistency-baseline.md   # 一致性基线
│   └── dependencies-overview.md  # 依赖全景图
├── iterations/
│   ├── session-status.md         # 会话状态追踪
│   └── sprint-latest/           # 当前迭代工作目录
│       └── feature.md           # 功能需求文档
└── docs/
    └── files.md                  # 本文档（文档统计）
```

---

## Agent 与文档对应关系

| Agent | 生成文档 | 数量 |
|-------|---------|------|
| PM-Stage0 | session-status.md、project.md、tech-stack-profile.md | 3 |
| Architect-Stage0 | consistency-baseline.md、dependencies-overview.md | 2 |
| Analyst-Stage0 | feature.md | 1 |
| **合计** | | **6** |

---

## 产出物状态汇总

| 文档 | 状态 | 说明 |
|------|------|------|
| session-status.md | ✅ 已更新 | 阶段0完成后更新 |
| project.md | ✅ 已生成 | 迭代历史包含 sprint-latest |
| tech-stack-profile.md | ✅ 已生成 | 技术栈档案完整 |
| consistency-baseline.md | ✅ 已生成/⏳ 已存在 | 可能跳过（如已存在） |
| dependencies-overview.md | ✅ 已生成/⏳ 已存在 | 可能跳过（如已存在） |
| feature.md | ✅ 已创建 | 功能需求已澄清 |

---

## 关联文档

| 文档 | 路径 |
|------|------|
| PM-Stage0 Agent | `.claude/agents/pm-stage0.md` |
| Architect-Stage0 Agent | `.claude/agents/architect-stage0.md` |
| Analyst-Stage0 Agent | `.claude/agents/analyst-stage0.md` |
| 阶段 0 完整 playbook | `.claude/commands/mf-upgrade:00-init.md` |