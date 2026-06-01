# /mf-upgrade:03-plan – 迭代计划与任务排期

> **当前阶段**：阶段 3（迭代计划与任务排期）
> **主导角色**：项目经理 (PM)
> **辅助角色**：分析师 (Analyst)
> **前置条件**：阶段 2 已完成，ADR.md 存在且状态为"已审批"，test-plan.md 存在
> **执行模式**：Analyst 提取 Task → PM 审核 + 生成计划 → Human Gate

---

## 0. 概述

本阶段由 PM Agent 主导，Analyst Agent 辅助，从已审批的 ADR 中提取任务清单，生成 Sprint 状态文档（sprint-status.md）。

**核心变化**：
- `sprint-status.md` 是单一数据源（任务领取 + 状态更新），包含 Plan + Status
- 替代原来的 `iteration-plan.md` + `sprint-status.md` 分离模式

**流程**：
```
阶段进入 → 前置检查 → Analyst 提取 Task（含 Modular Group） → PM 审核 + 生成计划 → Human Gate → 阶段退出
```

---

## 1. 日志声明

执行本 playbook 时，必须使用 `.claude/hooks/log-event.sh` 记录日志：

| 事件类型 | 日志命令格式 |
|---------|-------------|
| 阶段进入 | `bash .claude/hooks/log-event.sh "03" "Command" "阶段进入" "阶段3开始" "" "成功"` |
| Analyst 激活 | `bash .claude/hooks/log-event.sh "03" "Command" "Agent激活" "Analyst开始提取Task" "" "进行中"` |
| Analyst 完成 | `bash .claude/hooks/log-event.sh "03" "Command" "Agent完成" "AnalystTask提取完成" "" "成功"` |
| PM 激活 | `bash .claude/hooks/log-event.sh "03" "Command" "Agent激活" "PM开始生成计划" "" "进行中"` |
| PM 完成 | `bash .claude/hooks/log-event.sh "03" "Command" "Agent完成" "PM计划生成完成" "" "成功"` |
| 阶段退出 | `bash .claude/hooks/log-event.sh "03" "Command" "阶段退出" "阶段3完成" "" "成功"` |

---

## 2. 前置条件检查

> **重要**：阶段 3 开始前，必须验证所有前置条件

### 2.1 阶段 2 完成状态检查

```bash
# 检查 session-status.md 中阶段 2 状态
if ! grep -q "阶段 02.*✅" "$ROOT/.claude/iterations/session-status.md" 2>/dev/null; then
  echo "[Error] 阶段 2 尚未完成，阶段 3 无法开始"
  echo "请先完成阶段 2 或运行 /mf-upgrade:02-arch-qa"
  exit 1
fi
echo "[前置检查] 阶段 2 完成状态：✅"
```

### 2.2 ADR.md 检查

```bash
# 检查 ADR.md 是否存在
if [ ! -f "$ROOT/.claude/iterations/sprint-latest/ADR.md" ]; then
  echo "[Error] ADR.md 不存在，阶段 3 无法开始"
  echo "请先完成阶段 2 的 ADR 生成"
  exit 1
fi

# 检查 ADR.md 状态是否为"已审批"
if ! grep -q "已审批" "$ROOT/.claude/iterations/sprint-latest/ADR.md"; then
  echo "[Warning] ADR.md 尚未标记为已审批，阶段 3 可能无法正常执行"
  echo "建议先完成 ADR 审核流程（阶段 2）"
fi

# 统计 ADR 中 Task 数量
TASK_COUNT=$(grep -c "^| T-" "$ROOT/.claude/iterations/sprint-latest/ADR.md" || echo "0")
echo "[前置检查] ADR.md Task 数量：$TASK_COUNT"

# 检查 ADR 第 2.4 节（Modular Group）是否存在
if grep -q "Modular Group" "$ROOT/.claude/iterations/sprint-latest/ADR.md"; then
  echo "[前置检查] ADR Modular Group：✅ 已定义"
else
  echo "[Warning] ADR 第 2.4 节（Modular Group）未找到，请检查 ADR 模板是否更新"
fi
```

### 2.3 test-plan.md 检查

```bash
# 检查 test-plan.md 是否存在
if [ ! -f "$ROOT/.claude/iterations/sprint-latest/test-plan.md" ]; then
  echo "[Warning] test-plan.md 不存在，将跳过 Test Plan 关联"
fi
```

### 2.4 前置检查汇总

```bash
echo ""
echo "========== 前置检查汇总 =========="
echo "[前置检查] 阶段 02 完成状态：$(grep '阶段 02' $ROOT/.claude/iterations/session-status.md | grep -o '✅' || echo '❌')"
echo "[前置检查] ADR.md 存在：$(test -f $ROOT/.claude/iterations/sprint-latest/ADR.md && echo '✅' || echo '❌')"
echo "[前置检查] ADR Modular Group：$(grep -q 'Modular Group' $ROOT/.claude/iterations/sprint-latest/ADR.md && echo '✅' || echo '⚠️')"
echo "[前置检查] test-plan.md 存在：$(test -f $ROOT/.claude/iterations/sprint-latest/test-plan.md && echo '✅' || echo '⚠️')"
echo "==================================="
```

---

## 3. 规则加载

按需引用（不在阶段开头集中声明）：

| 规则/技能 | 用途 | 引用时机 |
|-----------|------|---------|
| `.claude/rules/global/session-init.md` | 阶段初始化规则 | 前置条件检查前 |
| `.claude/rules/global/sprint-statusning.md` | 任务拆解标准、WIP限制、警戒线设置 | PM 生成迭代计划时 |
| `.claude/rules/global/conflict-resolution.md` | 冲突裁决与串并行决策 | PM 冲突裁决时 |
| `.claude/rules/scenario-upgrade/reuse-before-build.md` | 复用优先规则 | Analyst 标注可复用代码时 |
| `.claude/agents/analyst-stage3.md` | Analyst 阶段3完整业务流程 | Analyst 执行时 |
| `.claude/agents/pm-stage3.md` | PM 阶段3完整业务流程 | PM 执行时 |

---

## 4. 执行流程

### 4.1 阶段进入日志

```bash
bash .claude/hooks/log-event.sh "03" "Command" "阶段进入" "阶段3开始" "" "成功"
```

---

### 4.2 Analyst Agent 执行（提取 Task + Modular Group）

**前置条件**：前置检查通过
**执行文件**：`.claude/agents/analyst-stage3.md`

激活 Analyst Agent（串行，等待完成）：

```
Agent: analyst-stage3.md
run_in_background: false
```

激活后等待 Analyst Agent 完成，记录日志：

```bash
bash .claude/hooks/log-event.sh "03" "Command" "Agent激活" "Analyst开始提取Task" "" "进行中"
# 等待 Analyst Agent 完成（由 Agent 自己写入日志）
bash .claude/hooks/log-event.sh "03" "Command" "Agent完成" "AnalystTask提取完成" "" "成功"
```

#### 4.2.1 Human Gate 确认（Analyst 产出）

> Analyst Agent 完成执行后，必须等待用户确认才能继续

**人工检查项**：

| 检查维度 | 检查内容 | 期望状态 | 不通过处理 |
|---------|---------|---------|-----------|
| **Modular Group** | ADR 第 2.4 节是否正确映射到 sprint-status.md 第 1 节 | 是 | 打回 Analyst 修复 |
| **Task 清单** | ADR 中的 Task 是否已提取到 sprint-status.md | 是 | 打回 Analyst 修复 |
| **US/MG 关联** | 每个 Task 是否关联到具体的 US 和 Modular Group | 是 | 打回 Analyst 补充 |
| **Task 信息完整** | 每个 Task 是否有类型、工时、风险、Skills 引用 | 是 | 打回 Analyst 补充 |
| **可复用标注** | 每个 Task 是否标注了可复用代码 | 是 | 打回 Analyst 补充 |

**快速验证命令**：
```bash
# 检查 sprint-status.md 中的 Modular Group 数量
grep -c "^| MG-" $ROOT/.claude/iterations/sprint-latest/sprint-status.md

# 检查 sprint-status.md 中的 Task 数量
grep -c "^| T-" $ROOT/.claude/iterations/sprint-latest/sprint-status.md

# 检查 Task 是否有 US/MG 关联
grep "US-/MG-" $ROOT/.claude/iterations/sprint-latest/sprint-status.md | head -5

# 检查 Task 是否有工时信息
grep "工时" $ROOT/.claude/iterations/sprint-latest/sprint-status.md

# 检查是否有 Skills 引用
grep -c "Skills" $ROOT/.claude/iterations/sprint-latest/sprint-status.md
```

**回复选项**：
- `继续` - 所有检查项通过，进入 PM 审核阶段
- `打回` - 列出需要修正的问题，Analyst 重新执行
- `暂停` - 暂停阶段 3，等待进一步指示

---

### 4.3 PM Agent 执行（审核 + 生成迭代计划）

**前置条件**：Analyst 产出通过 Human Gate
**执行文件**：`.claude/agents/pm-stage3.md`

#### 4.3.1 PM Agent 主要任务

激活 PM Agent（串行，等待完成）：

```
Agent: pm-stage3.md
run_in_background: false
```

激活后等待 PM Agent 完成，记录日志：

```bash
bash .claude/hooks/log-event.sh "03" "Command" "Agent激活" "PM开始生成计划" "" "进行中"
# 等待 PM Agent 完成
bash .claude/hooks/log-event.sh "03" "Command" "Agent完成" "PM计划生成完成" "" "成功"
```

#### 4.3.2 PM Agent 职责（详细）

| 职责 | 说明 | 产出物 |
|------|------|--------|
| **冲突裁决** | 检测任务间的模块冲突，应用决策树（串行化/分模块/人类裁决） | sprint-status.md 第 9 节 |
| **WIP 限制设定** | 根据团队规模和核心模块数设定 WIP 限制 | sprint-status.md 第 5 节 |
| **里程碑设定** | 设置至少 2 个里程碑检查点 | sprint-status.md 第 7 节 |
| **进度警戒线** | 为每个任务设置进度警戒线（黄色/红色） | sprint-status.md 第 2 节 |
| **生成 sprint-status.md** | 按模板生成迭代计划文档（单一数据源） | sprint-status.md |
| **生成 sprint-status.md** | 从 sprint-status.md 导出看板视图 | sprint-status.md（导出） |

#### 4.3.3 Human Gate 确认（PM 产出）

> PM Agent 完成执行后，必须等待用户确认才能结束阶段 3

**人工检查项**：

| 检查维度 | 检查内容 | 期望状态 | 不通过处理 |
|---------|---------|---------|-----------|
| **sprint-status.md** | 是否按模板生成，包含所有必填章节（12 节） | 是 | 打回 PM 修正 |
| **sprint-status.md** | 是否从 sprint-status.md 导出（状态以 sprint-status.md 为准） | 是 | 打回 PM 修正 |
| **Modular Group** | 是否完整映射，依赖关系是否正确 | 是 | 打回 PM 修正 |
| **WIP 限制** | 是否合理设置（默认 2） | 是 | 打回 PM 调整 |
| **里程碑** | 是否至少 2 个里程碑 | 是 | 打回 PM 添加 |
| **冲突裁决** | 是否有未解决的核心冲突 | 无 | 打回 PM 裁决 |
| **US 进度汇总** | 第 8 节 US 进度是否正确汇总 | 是 | 打回 PM 修正 |

**快速验证命令**：
```bash
# 检查 sprint-status.md 章节数量
grep -c "^## " $ROOT/.claude/iterations/sprint-latest/sprint-status.md

# 检查里程碑数量
grep -c "^- \[ \] M" $ROOT/.claude/iterations/sprint-latest/sprint-status.md

# 检查 sprint-status.md 是否标记为导出
grep "导出" $ROOT/.claude/iterations/sprint-latest/sprint-status.md

# 检查 US 进度汇总
grep "US-" $ROOT/.claude/iterations/sprint-latest/sprint-status.md | grep "MG-" | head -5
```

**回复选项**：
- `继续` - 所有检查项通过，阶段 3 完成
- `打回` - 列出需要修正的问题，PM 重新执行
- `暂停` - 暂停阶段 3，等待进一步指示

---

### 4.4 阶段退出

```bash
bash .claude/hooks/log-event.sh "03" "Command" "阶段退出" "阶段3完成" "" "成功"
```

更新 session-status.md 中阶段 3 完成状态为"✅"：

```bash
# 更新 session-status.md 阶段 3 状态
sed -i 's/| 3-迭代计划.*|/\| 3-迭代计划 | ✅ | $(date +%Y-%m-%d) |/' $ROOT/.claude/iterations/session-status.md
```

---

## 5. 产出物清单

阶段 3 完成时，应有如下产出物：

| 产出物 | 路径 | 状态 | 产出者 | 检查要点 |
|--------|------|------|--------|---------|
| **sprint-status.md** | `.claude/iterations/sprint-latest/sprint-status.md` | ✅ | Analyst + PM | 单一数据源：包含所有 US/Modular Group/Task，WIP、里程碑、警戒线、状态 |
| **sprint-status.md** | `.claude/iterations/sprint-latest/sprint-status.md` | ✅ | PM（导出） | 看板视图，声明"状态以 sprint-status.md 为准" |
| **session-status.md 更新** | `.claude/iterations/session-status.md` | ✅ | PM | 阶段 3 完成记录 |

---

## 6. 状态更新职责

| 文档 | 更新者 | 更新内容 |
|------|--------|---------|
| **sprint-status.md** | Dev（领任务+更新状态）、PM（更新进度） | Task 状态、US 进度、里程碑完成情况 |
| **sprint-status.md** | 无（导出视图，不单独维护） | 由 sprint-status.md 同步 |
| **session-status.md** | PM | 阶段完成记录（阶段 03）、产出物追踪表 |

**更新时机**：
- Dev 领取任务时：更新 sprint-status.md 第 2 节"任务看板"状态
- Task 状态变更时：PM 同步更新 sprint-status.md 第 8 节"US 进度汇总"
- sprint-status.md 由 PM 在阶段 3 结束时导出，后续由 sprint-status.md 自动同步

---

## 7. 异常处理

| 异常场景 | 处理方式 |
|---------|---------|
| ADR.md 不存在 | 报错退出，要求先完成阶段 2 |
| ADR.md 未审批 | 警告并要求确认是否继续 |
| ADR 第 2.4 节（Modular Group）缺失 | 警告，需要手动补充后才能继续 |
| test-plan.md 不存在 | 警告，继续执行（跳过关联） |
| Analyst 提取 Task 失败 | 记录异常，提交 Human Gate 决策 |
| PM 生成迭代计划失败 | 记录异常，提交 Human Gate 决策 |
| 核心冲突无法裁决 | 生成《冲突裁决申请书》提交人类 |
| Human Gate 3 次打回 | 提交 Human Decision |

异常需记录到 `session-status.md` 的"异常记录"章节。

---

## 8. 关联文档

| 文档 | 路径 | 说明 |
|------|------|------|
| Analyst Agent 阶段3 | `.claude/agents/analyst-stage3.md` | Analyst 提取 Task + Modular Group |
| PM Agent 阶段3 | `.claude/agents/pm-stage3.md` | PM 生成迭代计划和导出看板 |
| sprint-status.md 模板 | `.claude/templates/sprint-status-template.md` | 迭代计划文档模板（单一数据源） |
| sprint-status.md 模板 | `.claude/templates/sprint-status-template.md` | Sprint 看板模板（导出视图） |
| ADR.md | `.claude/iterations/sprint-latest/ADR.md` | 阶段 2 产出，本阶段 Task 来源（含第 2.4 节 Modular Group） |
| test-plan.md | `.claude/iterations/sprint-latest/test-plan.md` | 阶段 2 产出，本阶段测试关联 |
| session-status.md | `.claude/iterations/session-status.md` | 阶段状态追踪（需更新） |

---

## 9. 阶段 2 vs 阶段 3 结构对比

| 结构要素 | 阶段 2（02-arch-qa.md） | 阶段 3（03-plan.md） |
|---------|-------------------------|---------------------|
| 概述 | ✅ 有，明确执行模式 | ✅ 有，明确执行模式 |
| 日志声明 | ✅ 有，表格化 | ✅ 有，表格化 |
| 前置条件检查 | ✅ 有，单独章节 | ✅ 有，单独章节（含 Modular Group 检查） |
| 规则加载 | ✅ 有，表格化 | ✅ 有，表格化 |
| 执行流程 | Architect → PM-Audit 循环 → QA → PM-Audit-TP 循环 | Analyst 提取 → PM 审核 → Human Gate |
| Human Gate | 每个 Agent 后都有 | Analyst 后有，PM 后有 |
| 产出物清单 | ✅ 有，表格化+检查要点 | ✅ 有，表格化+检查要点 |
| 状态更新职责 | ✅ 有 | ✅ 有（明确 sprint-status 为导出视图） |
| 异常处理 | ✅ 有 | ✅ 有 |
| 关联文档 | ✅ 有（含需更新的文档标注） | ✅ 有（含需更新的文档标注） |
| **审核循环** | ✅ 有（≤3次） | ❌ 无（方案A简化） |
| **多 Agent 协同** | ✅ 有（Architect + PM-Audit + QA） | ✅ 有（Analyst + PM） |
| **Modular Group 支持** | ❌ 无（新增第 2.4 节） | ✅ 有（ADR 第 2.4 节 → sprint-status 第 1 节） |
| **单一数据源** | ❌ 无（sprint-status + sprint-status 独立） | ✅ 有（sprint-status 为单一数据源） |