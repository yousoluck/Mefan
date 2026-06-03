# /mf-upgrade:00-init – 会话初始化与上下文建立

> **当前阶段**：阶段 0（会话初始化）
> **主导角色**：项目经理 (PM)
> **辅助角色**：架构师 (Architect)、需求分析师 (Analyst)
> **前置条件**：无（首次进入迭代）
> **执行模式**：PM → Architect → Analyst 串行执行（各 Agent 完成前，下一个 Agent 不得开始）

---

## 0. 概述

本阶段由 PM Agent 主导，执行环境确认和上下文建立。PM Agent 完成所有任务后，Architect Agent 才开始执行技术栈分析和一致性基线提取。Architect 完成后，PM Agent 执行校验，校验通过后 Analyst Agent 执行需求澄清对话，产出 feature.md。

**流程**：
```
PM Agent → Human Gate → Architect Agent → Human Gate → PM 校验 → Human Gate → Analyst Agent → Human Gate
```

---

## 1. 日志声明

执行本 playbook 时，必须使用 `.claude/hooks/log-event.sh` 记录日志：

| 事件类型 | 日志命令格式 |
|---------|-------------|
| 阶段进入 | `bash .claude/hooks/log-event.sh "00" "PM" "阶段进入" "阶段0开始" "" "成功"` |
| PM 激活 | `bash .claude/hooks/log-event.sh "00" "PM" "Agent激活" "PM开始执行" "" "进行中"` |
| PM 完成 | `bash .claude/hooks/log-event.sh "00" "PM" "Agent完成" "PM产出完成" "" "成功"` |
| Architect 激活 | `bash .claude/hooks/log-event.sh "00" "Architect" "Agent激活" "Architect开始执行" "" "进行中"` |
| Architect 完成 | `bash .claude/hooks/log-event.sh "00" "Architect" "Agent完成" "Architect产出完成" "" "成功"` |
| PM 校验激活 | `bash .claude/hooks/log-event.sh "00" "PM" "Agent激活" "PM开始校验" "" "进行中"` |
| PM 校验完成 | `bash .claude/hooks/log-event.sh "00" "PM" "Agent完成" "PM校验完成" "" "成功"` |
| Analyst 激活 | `bash .claude/hooks/log-event.sh "00" "Analyst" "Agent激活" "Analyst开始执行" "" "进行中"` |
| Analyst 完成 | `bash .claude/hooks/log-event.sh "00" "Analyst" "Agent完成" "Analyst产出完成" "" "成功"` |
| 阶段退出 | `bash .claude/hooks/log-event.sh "00" "PM" "阶段退出" "阶段0完成" "" "成功"` |

---

## 2. 变量定义

```bash
# 从 project.conf 加载 ROOT 和 SCENARIO
if [ -f "$(dirname "${BASH_SOURCE[0]}")/../project.conf" ]; then
    source "$(dirname "${BASH_SOURCE[0]}")/../project.conf"
else
    export ROOT="/mnt/d/pycharmprojects/Mefan"
fi
SCENARIO="upgrade"
```

---

## 3. Graphify 安装与初始化

> **重要**：阶段 0 执行前，必须完成 graphify 安装和项目扫描

**Graphify 安装步骤**：

```bash
# 1. 检查 graphify 是否已安装（系统级）
if ! command -v graphify &> /dev/null; then
    echo "[mf-upgrade:00-init] 正在安装 graphify..."
    pip install graphifyy 2>/dev/null || echo "[Warning] graphify 安装失败"
fi

# 2. 检查 graphify 是否可用
if command -v graphify &> /dev/null; then
    echo "[mf-upgrade:00-init] graphify 已安装: $(which graphify)"
else
    echo "[Warning] graphify 不可用，跳过图谱生成"
fi
```

**Graphify 项目初始化**：

```bash
# 3. 在项目根目录初始化 graphify（项目级配置）
cd "$ROOT"
if [ -f "$ROOT/graphify-out/.graphify_initialized" ]; then
    echo "[mf-upgrade:00-init] graphify 项目已初始化"
else
    echo "[mf-upgrade:00-init] 正在初始化 graphify 项目..."
    if command -v graphify &> /dev/null; then
        graphify install --project 2>/dev/null || echo "[Warning] graphify install --project 失败"
    fi
fi
```

**Graphify 图谱生成/更新**：

> 以下操作需要在 Claude Code 中执行（slash command 形式）

**首次扫描（之前未扫描过项目）**：
```
/graphify .
```

**增量更新（之前已扫描过项目）**：
```
/graphify . --update
```

**注意**：
- `graphify install --project`：初始化项目级配置
- `/graphify .`：在 Claude Code 中执行全量扫描，生成图谱到 `graphify-out/`
- `/graphify . --update`：在 Claude Code 中执行增量更新
- 如果 graphify 不可用，Agent 会标注"手动分析 [Graphify不可用]"继续执行

---

## 3. 规则加载

按需引用（不在阶段开头集中声明）：

| 规则/技能 | 用途 | 引用时机 |
|-----------|------|---------|
| `.claude/rules/global/session-init.md` | 阶段初始化三原则 | PM 步骤执行前 |
| `.claude/agents/pm-stage0.md` | PM 阶段0完整业务流程 | PM Agent 执行时 |
| `.claude/agents/architect-stage0.md` | Architect 阶段0完整业务流程 | Architect Agent 执行时 |
| `.claude/agents/analyst-stage0.md` | Analyst 阶段0完整业务流程 | Analyst Agent 执行时 |

---

## 4. 执行流程

### 4.1 阶段进入日志

```bash
bash .claude/hooks/log-event.sh "00 Init" "PM" "PM Agent开始执行" "PM 初始化项目开始" "" "进行中"
```

### 4.2 PM Agent 执行（阶段 0 业务逻辑）

**前置条件**：无
**执行文件**：`.claude/agents/pm-stage0.md`

激活 PM Agent（串行，等待完成）：

```
Agent: pm-stage0.md
run_in_background: false
```

激活后等待 PM Agent 完成，记录日志：

```bash
bash .claude/hooks/log-event.sh "00" "PM" "产出物" "PM阶段0完成" ".claude/agents/pm-stage0.md" "成功"
bash .claude/hooks/log-event.sh "00" "PM" "步骤完成" "PM环境确认完成" "" "成功"
```

#### 3.2.1 Human Gate 确认（PM 阶段）
> PM Agent 完成执行后，必须等待用户确认才能继续

**一、session-status.md 状态检查**

| 检查项 | 期望状态 | 检查位置 |
|--------|---------|---------|
| 阶段 00 完成时间 | 已填写（时间戳） | `## 阶段完成记录` 表格 |
| 阶段 00 产出物状态 | ✅ | `## 阶段完成记录` 表格 |
| 当前阶段 | 0 | `## 自动推进状态` 表格 |
| 已完成阶段 | 包含 0 | `## 自动推进状态` 表格 |
| 迭代概览 - 迭代名称 | sprint-latest | `## 迭代概览` 表格 |
| 迭代概览 - 开始日期 | 当天日期 | `## 迭代概览` 表格 |
| 迭代概览 - 场景 | upgrade | `## 迭代概览` 表格 |

**二、迭代目录结构检查**

| 检查项 | 期望状态 |
|--------|---------|
| `.claude/iterations/sprint-latest/` | 目录已创建 |
| `.claude/iterations/session-status.md` | 文件已创建 |

**三、project.md 文档检查**

| 检查项 | 期望状态 | 路径 |
|--------|---------|------|
| project.md 是否生成 | ✅ | `.claude/context/project.md` |
| 迭代历史版块 | 包含 `### 迭代 sprint-latest` | `## 迭代历史` |
| sprint-latest 状态 | 🔍 进行中 | `### 迭代 sprint-latest` |
| sprint-latest 开始日期 | 当天日期 | `### 迭代 sprint-latest` |

**四、tech-stack-profile.md 文档检查**

| 检查项 | 期望状态 | 路径 |
|--------|---------|------|
| tech-stack-profile.md 是否生成 | ✅ | `.claude/context/tech-stack-profile.md` |
| 前端框架信息 | 已填写 | 核心框架章节 |
| 后端框架信息 | 已填写 | 核心框架章节 |
| 数据库信息 | 已填写 | 主数据库章节 |

**五、feature-elements.md 文档检查**

| 检查项 | 期望状态 | 路径 |
|--------|---------|------|
| feature-elements.md 是否生成 | ✅ | `.claude/context/feature-elements.md` |
| L1 基础层 | 已填写 | 基础层章节 |
| L2 框架层 | 已填写 | 框架层章节 |
| L3 工具层 | 已填写或待补充 | 工具层章节 |
| L4 业务层 | 已填写或待用户确认 | 业务层章节 |
| 架构图 | Mermaid 格式 | 架构图章节 |

**六、确认选项**

**快速验证命令**：
```bash
# 检查 session-status.md 阶段完成记录
grep -A1 "会话初始化" .claude/iterations/session-status.md

# 检查 project.md 迭代历史
grep "### 迭代 sprint-latest" .claude/context/project.md

# 检查 tech-stack-profile.md 是否存在
ls -la .claude/context/tech-stack-profile.md

# 检查 feature-elements.md 是否存在
ls -la .claude/context/feature-elements.md

# 检查迭代目录
ls -la .claude/iterations/sprint-latest/
```

**回复选项**：
- `继续` - 所有检查项通过，允许 Architect-Stage0 开始执行
- `补充` - 列出需要补充的信息
- `暂停` - 暂停阶段 0，等待进一步指示

---

### 4.3 Architect Agent 执行（阶段 0 技术分析）

**前置条件**：PM Agent 全部完成
**执行文件**：`.claude/agents/architect-stage0.md`

激活 Architect Agent（串行，等待完成）：

```
Agent: architect-stage0.md
run_in_background: false
```

激活后等待 Architect Agent 完成，记录日志：

```bash
bash .claude/hooks/log-event.sh "00" "Architect" "步骤开始" "Architect开始技术栈分析" "" "成功"
# Architect Agent 执行中...
bash .claude/hooks/log-event.sh "00" "Architect" "产出物" "生成consistency-baseline.md" ".claude/context/consistency-baseline.md" "成功"
bash .claude/hooks/log-event.sh "00" "Architect" "产出物" "生成dependencies-overview.md" ".claude/context/dependencies-overview.md" "成功"
bash .claude/hooks/log-event.sh "00" "Architect" "步骤完成" "Architect技术分析完成" "" "成功"
```

#### 3.3.1 Human Gate 确认（Architect 阶段）
> Architect Agent 完成执行后，必须等待用户确认才能继续

**一、session-status.md 状态检查**

| 检查项 | 期望状态 | 检查位置 |
|--------|---------|---------|
| 阶段 00（会话初始化）完成时间 | 已填写（时间戳） | `## 阶段完成记录` 表格 |
| 阶段 00 产出物状态 | ✅ | `## 阶段完成记录` 表格 |
| consistency-baseline.md 产出物状态 | ✅ 已生成 / ⏳ 已存在 | `## 产出物追踪表` |
| dependencies-overview.md 产出物状态 | ✅ 已生成 / ⏳ 已存在 | `## 产出物追踪表` |

**二、consistency-baseline.md 文档检查**

| 检查项 | 期望状态 | 路径 |
|--------|---------|------|
| 文件是否存在 | ✅ | `.claude/context/consistency-baseline.md` |
| 设计模式数量 | ≥ 5 条 | 章节中每条规则必须有证据 |
| 错误处理规则 | 已填写 | 错误处理章节 |
| 命名规范 | 已填写 | 命名规范章节 |
| 反模式 | ≥ 2 条 | 反模式章节 |
| 代码示例 | 有证据（文件路径+行号） | 每条规则 |

**三、dependencies-overview.md 文档检查**

| 检查项 | 期望状态 | 路径 |
|--------|---------|------|
| 文件是否存在 | ✅ | `.claude/context/dependencies-overview.md` |
| 核心模块数量 | ≥ 3 个 | 核心模块章节 |
| 模块依赖关系图 | Mermaid 格式 | 依赖关系图章节 |
| 外部依赖清单 | 已填写 | 外部依赖章节 |
| 循环依赖检测 | 已完成（或标注不可用） | 关键发现章节 |

**四、project.md 更新检查**

| 检查项 | 期望状态 | 路径 |
|--------|---------|------|
| consistency-baseline.md 详细文档状态 | ✅ 已生成 | `### 迭代 sprint-latest` → `#### 详细文档` |
| dependencies-overview.md 详细文档状态 | ✅ 已生成 | `### 迭代 sprint-latest` → `#### 详细文档` |

**五、确认选项**

**快速验证命令**：
```bash
# 检查 consistency-baseline.md 是否存在且有内容
ls -la .claude/context/consistency-baseline.md
grep -c "##" .claude/context/consistency-baseline.md

# 检查 dependencies-overview.md 是否存在且有内容
ls -la .claude/context/dependencies-overview.md
grep -c "##" .claude/context/dependencies-overview.md

# 检查 project.md 是否已更新
grep -A1 "consistency-baseline.md" .claude/context/project.md
grep -A1 "dependencies-overview.md" .claude/context/project.md
```

**回复选项**：
- `继续` - 所有检查项通过，允许进入 PM 校验阶段
- `补充` - 列出需要补充的信息，返回 Architect-Stage0 重新执行
- `暂停` - 暂停阶段 0，等待进一步指示

---

### 4.4 PM 校验

**执行者**：PM Agent（回跳执行校验）

PM Agent 在 Architect 完成产出后，执行以下校验：
- 技术栈完整性检查
- 一致性基线有效性检查
- 校验结果写入 session-status.md

#### 3.4.1 Human Gate 确认（PM 校验）
> PM 校验完成后，必须等待用户确认才能进入 Analyst Agent

**一、PM 校验结果检查**

| 检查项 | 期望状态 | 检查方法 |
|--------|---------|---------|
| 技术栈完整性 | 通过 | tech-stack-profile.md 包含前后端框架、数据库等核心信息 |
| 一致性基线有效性 | 通过 | consistency-baseline.md 包含至少 5 条规则，每条有证据 |
| 校验结果写入 | 已完成 | session-status.md 中有校验记录 |

**二、session-status.md 状态检查**

| 检查项 | 期望状态 | 检查位置 |
|--------|---------|---------|
| 阶段完成记录 | PM阶段00、Architect阶段00均为 ✅ | `## 阶段完成记录` 表格 |
| 产出物追踪表 | 所有阶段 0 产出物状态为 ✅ | `## 产出物追踪表` |
| 自动推进状态 - 当前阶段 | 0 | `## 自动推进状态` |
| 自动推进状态 - 已完成阶段 | 包含 0 | `## 自动推进状态` |
| 阻塞标记 | 无 | `## 自动推进状态` |

**三、阶段 0 产出物完成度检查**

| 产出物 | 路径 | 状态 | 检查要点 |
|--------|------|------|---------|
| session-status.md | `.claude/iterations/` | ✅ | 阶段完成记录、产出物追踪表已更新 |
| project.md | `.claude/context/` | ✅ | 迭代历史、详细文档表格已更新 |
| tech-stack-profile.md | `.claude/context/` | ✅ | 前端/后端框架、数据库信息已填写 |
| feature-elements.md | `.claude/context/` | ✅ | L1-L4 层次已填写，架构图已生成 |
| consistency-baseline.md | `.claude/context/` | ✅/⏳ | 至少 5 条规则，有代码示例证据 |
| dependencies-overview.md | `.claude/context/` | ✅/⏳ | 至少 3 个核心模块，有依赖图 |
| feature.md | `.claude/iterations/sprint-latest/` | ⏳ 待生成 | Analyst-Stage0 尚未执行 |

**四、确认选项**

**快速验证命令**：
```bash
# 检查技术栈完整性
grep -A5 "核心框架" .claude/context/tech-stack-profile.md | head -20

# 检查一致性基线有效性
grep -c "^##" .claude/context/consistency-baseline.md

# 检查 session-status.md 校验记录
grep -A5 "PM校验" .claude/iterations/session-status.md
```

**回复选项**：
- `继续` - 所有检查项通过，允许 Analyst-Stage0 开始执行
- `补充` - 列出需要补充的信息
- `暂停` - 暂停阶段 0，等待进一步指示

---

### 4.5 Analyst Agent 执行（阶段 0 需求澄清）

**前置条件**：PM 校验完成且用户确认
**执行文件**：`.claude/agents/analyst-stage0.md`

激活 Analyst Agent（串行，等待完成）：

```
Agent: analyst-stage0.md
run_in_background: false
```

激活后等待 Analyst Agent 完成，记录日志：

```bash
bash .claude/hooks/log-event.sh "00" "Analyst" "步骤开始" "Analyst开始需求澄清" "" "成功"
# Analyst Agent 执行中...
bash .claude/hooks/log-event.sh "00" "Analyst" "产出物" "生成feature.md" ".claude/iterations/sprint-latest/feature.md" "成功"
bash .claude/hooks/log-event.sh "00" "Analyst" "步骤完成" "Analyst需求澄清完成" "" "成功"
```

#### 3.5.1 Human Gate 确认（Analyst 阶段）
> Analyst Agent 完成执行后，必须等待用户确认才能继续

**一、session-status.md 状态检查**

| 检查项 | 期望状态 | 检查位置 |
|--------|---------|---------|
| 阶段 00（Analyst）完成时间 | 已填写（时间戳） | `## 阶段完成记录` 表格 |
| 阶段 00 产出物状态 | ✅ | `## 阶段完成记录` 表格 |
| feature.md 产出物状态 | ✅ 已生成 | `## 产出物追踪表` |

**二、feature.md 文档检查**

| 检查项 | 期望状态 | 路径 |
|--------|---------|------|
| 文件是否存在 | ✅ | `.claude/iterations/sprint-latest/feature.md` |
| 功能要点数量 | ≥ 1 | `## 功能要点列表` 表格 |
| 功能要点优先级 | P0/P1/P2 已标注 | `## 功能要点列表` 表格 |
| 澄清对话记录 | 已记录 | `## 澄清对话记录` 表格 |
| 验收标准 | 有内容 | 每个功能要点的 `#### 9. 验收标准` |

**三、project.md 更新检查**

| 检查项 | 期望状态 | 路径 |
|--------|---------|------|
| feature.md 详细文档状态 | ✅ 已创建 | `### 迭代 sprint-latest` → `#### 详细文档` |
| 迭代功能概述 | 已填写 | `### 迭代 sprint-latest` → `迭代功能概述` |
| 功能要点数 | 已填写 | `### 迭代 sprint-latest` → `功能要点数` |

**四、阶段 0 产出物完成度最终检查**

| 产出物 | 路径 | 最终状态 | 检查要点 |
|--------|------|----------|---------|
| session-status.md | `.claude/iterations/` | ✅ | 阶段 00 (PM、Architect、Analyst) 完成记录 |
| project.md | `.claude/context/` | ✅ | 迭代历史、详细文档表格、迭代概述 |
| tech-stack-profile.md | `.claude/context/` | ✅ | 完整技术栈信息 |
| feature-elements.md | `.claude/context/` | ✅ | L1-L4 层次已填写，架构图已生成 |
| consistency-baseline.md | `.claude/context/` | ✅/⏳ | 规则≥5条，有证据 |
| dependencies-overview.md | `.claude/context/` | ✅/⏳ | 核心模块≥3个 |
| feature.md | `.claude/iterations/sprint-latest/` | ✅ | 功能要点≥1，验收标准已定义 |

**五、确认选项**

**快速验证命令**：
```bash
# 检查 feature.md 是否存在
ls -la .claude/iterations/sprint-latest/feature.md

# 检查功能要点数量
grep -c "^| [0-9]" .claude/iterations/sprint-latest/feature.md

# 检查 project.md 是否已更新
grep "迭代功能概述" .claude/context/project.md -A1
grep "功能要点数" .claude/context/project.md -A1

# 检查验收标准
grep -c "验收标准" .claude/iterations/sprint-latest/feature.md
```

**回复选项**：
- `继续` - 所有检查项通过，允许进入阶段退出
- `补充` - 列出需要补充的信息，返回 Analyst-Stage0 重新执行
- `暂停` - 暂停阶段 0，等待进一步指示

---

### 4.6 阶段退出

```bash
bash .claude/hooks/log-event.sh "00" "PM" "阶段退出" "阶段0完成" "" "成功"
```

---

## 5. 产出物清单

| 产出物 | 路径 | 状态 | 产出者 |
|--------|------|------|--------|
| session-status.md | `.claude/iterations/` | ⏳→✅ | PM |
| project.md | `.claude/context/` | ⏳→✅ | PM |
| tech-stack-profile.md | `.claude/context/` | ⏳→✅ | PM |
| feature-elements.md | `.claude/context/` | ⏳→✅ | PM |
| consistency-baseline.md | `.claude/context/` | ⏳→✅（可能跳过） | Architect |
| dependencies-overview.md | `.claude/context/` | ⏳→✅（可能跳过） | Architect |
| feature.md | `.claude/iterations/sprint-latest/` | ⏳→✅ | Analyst |

---

## 6. 异常处理

| 异常场景 | 处理方式 |
|---------|---------|
| SCENARIO 未定义 | 报错退出 |
| 迭代目录未创建 | 报错退出 |
| PM Agent 执行失败 | 阻断，提交 Human Gate |
| Architect Agent 执行失败 | 阻断，提交 Human Gate |
| Analyst Agent 执行失败 | 阻断，提交 Human Gate |
| PM 校验重试 3 次仍失败 | 提交 Human Gate |

异常需记录到 session-status.md 的"异常记录"章节。

---

## 7. 关联文档

| 文档 | 路径 |
|------|------|
| PM Agent 阶段0 | `.claude/agents/pm-stage0.md` |
| Architect Agent 阶段0 | `.claude/agents/architect-stage0.md` |
| Analyst Agent 阶段0 | `.claude/agents/analyst-stage0.md` |
| session-init 规则 | `.claude/rules/global/session-init.md` |
| graphify 技能 | `.claude/skills/graphify-query-cheatsheet.md` |
| tech-stack 模板 | `.claude/templates/tech-stack-profile-template.md` |
| feature-elements 模板 | `.claude/templates/feature-elements-template.md` |
| consistency-baseline 模板 | `.claude/templates/consistency-baseline-template.md` |
| dependencies-overview 模板 | `.claude/templates/dependencies-overview-template.md` |
| session-status 模板 | `.claude/templates/session-status-template.md` |
| feature 模板 | `.claude/templates/feature-template.md` |