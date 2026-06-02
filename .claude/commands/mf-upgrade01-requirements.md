# /mf-upgrade:01-requirements – 需求详细设计

> **当前阶段**：阶段 1（需求详细设计）
> **主导角色**：业务分析师 (BA)
> **辅助角色**：项目经理 (PM)
> **前置条件**：阶段 0 已完成，feature.md 存在且状态为"✅ 已完成"
> **执行模式**：BA → PM 串行执行（BA 完成所有任务后，PM 开始审查）

---

## 0. 概述

本阶段由 BA Agent 主导，执行详细需求设计，将 feature.md 转化为完整的 requirements.md 文档。BA 完成产出后，PM Agent 执行需求文档审查（最多3次循环），验证文档符合标准后通知 Architect 进入阶段 2。

**流程**：
```
BA Agent → 生成 requirements.md
       ↓
PM Agent 审查（≤3次循环）
       ↓
阶段完成 → 通知 Architect 进入阶段 2
```

---

## 1. 日志声明

执行本 playbook 时，必须使用 `.claude/hooks/log-event.sh` 记录日志：

| 事件类型 | 日志命令格式 |
|---------|-------------|
| 阶段进入 | `bash .claude/hooks/log-event.sh "01" "Command" "阶段进入" "阶段1开始" "" "成功"` |
| BA Agent 激活 | `bash .claude/hooks/log-event.sh "01" "Command" "Agent激活" "BA开始执行" "" "进行中"` |
| BA Agent 完成 | `bash .claude/hooks/log-event.sh "01" "Command" "Agent完成" "BA产出完成" "" "成功"` |
| PM Agent 激活 | `bash .claude/hooks/log-event.sh "01" "Command" "Agent激活" "PM开始审查" "" "进行中"` |
| PM Agent 完成 | `bash .claude/hooks/log-event.sh "01" "Command" "Agent完成" "PM审查完成" "" "成功"` |
| 阶段退出 | `bash .claude/hooks/log-event.sh "01" "Command" "阶段退出" "阶段1完成" "" "成功"` |

---

## 2. 前置条件检查

> **重要**：阶段 1 开始前，必须验证所有前置条件

### 2.1 feature.md 检查

```bash
# 检查 feature.md 是否存在
if [ ! -f "$ROOT/.claude/iterations/sprint-latest/feature.md" ]; then
  echo "[Error] feature.md 不存在，阶段 1 无法开始"
  echo "请先完成阶段 0 或运行 /mf-upgrade:00-init"
  exit 1
fi

# 检查 feature.md 状态
if ! grep -q "✅ 已完成" "$ROOT/.claude/iterations/sprint-latest/feature.md"; then
  echo "[Warning] feature.md 尚未标记为完成，阶段 1 可能无法正常执行"
fi

# 统计功能要点数量
P0_COUNT=$(grep -c "P0" "$ROOT/.claude/iterations/sprint-latest/feature.md" || echo "0")
P1_COUNT=$(grep -c "P1" "$ROOT/.claude/iterations/sprint-latest/feature.md" || echo "0")
echo "[前置检查] 功能要点：P0=$P0_COUNT, P1=$P1_COUNT"
```

### 2.2 依赖文档检查

```bash
# 检查必要依赖文档是否存在
echo "[前置检查] 加载依赖文档..."
ls -la $ROOT/.claude/context/tech-stack-profile.md 2>/dev/null || echo "[Warning] tech-stack-profile.md 不存在"
ls -la $ROOT/.claude/context/consistency-baseline.md 2>/dev/null || echo "[Warning] consistency-baseline.md 不存在"
ls -la "$ROOT/graphify-out" 2>/dev/null || echo "[Info] graphify-out 不存在，将使用手动分析"
```

---

## 3. 规则加载

按需引用（不在阶段开头集中声明）：

| 规则/技能                                                  | 用途 | 引用时机 |
|--------------------------------------------------------|------|---------|
| `.claude/rules/global/session-init.md`                 | 阶段初始化规则 | 前置条件检查前 |
| `.claude/rules/scenario-upgrade/consistency-first.md`  | 一致性优先规则 | BA 需求设计时 |
| `.claude/rules/scenario-upgrade/reuse-before-build.md` | 复用优先规则 | BA 系统关联分析时 |
| `.claude/agents/ba-stage1.md`                          | BA 阶段 1 完整业务流程 | BA Agent 执行时 |
| `.claude/agents/pm-stage1.md`                          | PM 阶段 1 完整业务流程 | PM Agent 执行时 |

---

## 4. 执行流程

### 4.1 阶段进入日志

```bash
bash .claude/hooks/log-event.sh "01" "Command" "阶段进入" "阶段1开始" "" "成功"
```

---

### 4.2 BA Agent 执行（详细需求设计）

**前置条件**：前置条件检查通过
**执行文件**：`.claude/agents/ba-stage1.md`

激活 BA Agent（串行，等待完成）：

```
Agent: ba-stage1.md
run_in_background: false
```

激活后等待 BA Agent 完成，记录日志：

```bash
bash .claude/hooks/log-event.sh "01" "Command" "Agent激活" "BA开始执行" "" "进行中"
# 等待 BA Agent 完成（由 Agent 自己写入日志）
bash .claude/hooks/log-event.sh "01" "Command" "Agent完成" "BA需求设计完成" "" "成功"
```

#### 4.2.1 Human Gate 确认（BA 产出）

> BA Agent 完成执行后，必须等待用户确认才能继续

**人工检查项**：

| 检查维度 | 检查内容 | 期望状态 | 不通过处理 |
|---------|---------|---------|-----------|
| **User Story 完整性** | 是否所有 P0/P1 功能都已拆分？每个 US 是否有验收标准？ | US 数量 ≥ P0+P1 功能数 | 打回补充 |
| **INVEST 原则** | 每个 User Story 是否满足：独立性、可协商、有价值、可估算、小型、可测试？ | 全部满足 | 打回修正 |
| **Sub-feature 粒度** | 每个 US 是否有 1-5 个 Sub-feature？边界是否清晰？ | 符合粒度要求 | 打回拆分 |
| **系统关联分析** | 冲突分析是否完整？复用机会是否识别？ | 有分析结果 | 打回补充 |
| **测试影响评估** | 是否列出受影响测试文件？是否估算新增测试用例？ | 有评估结果 | 打回补充 |
| **文档规范性** | requirements.md 是否使用模板？命名是否遵循一致性约定？ | 符合规范 | 打回修正 |

**快速验证命令**：
```bash
# 检查 requirements.md 是否存在
ls .claude/iterations/sprint-latest/requirements.md

# 检查 User Story 数量
grep -c "^## US-" .claude/iterations/sprint-latest/requirements.md

# 检查 Sub-feature 数量
grep -c "^##### SF-" .claude/iterations/sprint-latest/requirements.md

# 检查每个 US 是否有验收标准（Gherkin 格式）
grep -c "Given\|When\|Then" .claude/iterations/sprint-latest/requirements.md
```

**回复选项**：
- `继续` - 所有检查项通过，进入 PM 审查阶段
- `打回` - 列出需要修正的问题，BA 重新执行
- `暂停` - 暂停阶段 1，等待进一步指示

---

### 4.3 PM Agent 执行（需求文档审查）

**前置条件**：BA 产出通过 Human Gate
**执行文件**：`.claude/agents/pm-stage1.md`

激活 PM Agent（串行，等待完成）：

```
Agent: pm-stage1.md
run_in_background: false
```

激活后等待 PM Agent 完成，记录日志：

```bash
bash .claude/hooks/log-event.sh "01" "Command" "Agent激活" "PM开始审查" "" "进行中"
# 等待 PM Agent 完成
bash .claude/hooks/log-event.sh "01" "Command" "Agent完成" "PM审查完成" "" "成功"
```

#### 4.3.1 Human Gate 确认（PM 审查结果）

> PM Agent 完成审查后，必须等待用户确认才能进入阶段 2

**人工检查项**：

| 检查维度 | 检查内容 | 期望状态 | 不通过处理 |
|---------|---------|---------|-----------|
| **审查决策树结果** | 6 项检查是否全部通过？（拓扑完整性、验收标准可测性、受影响范围、非功能需求、AC完整性、需求一致性） | 全部 ✅ | 需 PM 说明 |
| **需求一致性** | requirements.md 是否与 feature.md 一致？功能点不能被篡改或删除 | 一致 | 需 BA 修正 |
| **审查打回次数** | 是否存在多次打回？（≥3 次需 Human Gate 决策） | < 3 次 | 需决策 |
| **产出物状态** | requirements.md 是否为单一文件且包含所有 US 和 SF？ | ✅ | 需补充 |
| **session-status.md 更新** | 阶段完成记录、产出物追踪表、自动推进状态是否已更新？ | 全部 ✅ | 需补充 |
| **project.md 更新** | 迭代历史章节中 requirements.md 状态是否已更新为 ✅？ | 已更新 | 需补充 |
| **通知 Architect** | PM 是否已记录通知 Architect 的时间？ | 已记录 | 需补记 |

**快速验证命令**：
```bash
# 检查 session-status.md 中阶段 1 完成记录
grep -A3 "阶段 1" .claude/iterations/session-status.md

# 检查 requirements.md 数量
ls .claude/iterations/sprint-latest/requirements.md

# 检查 US 和 SF 数量
grep "^## US-" .claude/iterations/sprint-latest/requirements.md | wc -l
grep "^##### SF-" .claude/iterations/sprint-latest/requirements.md | wc -l

# 检查通知记录
cat .claude/iterations/sprint-latest/.notifications.log 2>/dev/null || echo "[Info] 无通知记录"
```

**回复选项**：
- `继续` - 所有检查项通过，进入阶段 2
- `复查` - 需要重新审查，PM 重新执行
- `暂停` - 暂停阶段 1，等待进一步指示

---

### 4.4 阶段退出

```bash
bash .claude/hooks/log-event.sh "01" "Command" "阶段退出" "阶段1完成" "" "成功"
```

---

## 5. 产出物清单

阶段 1 完成时，应有如下产出物：

| 产出物 | 路径 | 状态 | 产出者 | 检查要点 |
|--------|------|------|--------|---------|
| **requirements 主文档** | `.claude/iterations/sprint-latest/requirements.md` | ✅ | BA | 包含所有 US 和 SF |
| **session-status.md 更新** | `.claude/iterations/session-status.md` | ✅ | PM | 阶段 1 完成记录 |
| **审查结果** | `.claude/iterations/sprint-latest/.review-count` | ✅ | PM | 审查通过次数 |
| **通知记录** | `.claude/iterations/sprint-latest/.notifications.log` | ✅ | PM | Architect 通知时间 |
| **project.md 更新** | `.claude/context/project.md` | ✅ | BA | 迭代历史详细文档状态 |

---

## 6. 状态更新职责

> 阶段 1 需要更新以下文档，详见各 Agent 执行文件

| 文档 | 更新者 | 更新内容 |
|------|--------|---------|
| **session-status.md** | PM | 阶段完成记录（阶段 01）、产出物追踪表（requirements.md ✅）、自动推进状态、PM 阶段完成报告 |
| **project.md** | BA | 迭代历史章节中 requirements.md 状态从 ⏳ 更新为 ✅ |

**更新时机**：BA 和 PM 分别完成各自任务后，Human Gate 确认前

---

## 7. 异常处理

| 异常场景 | 处理方式 |
|---------|---------|
| feature.md 不存在 | 报错退出，要求先完成阶段 0 |
| feature.md 未完成 | 警告并要求确认是否继续 |
| BA 执行失败 | 记录异常，提交 Human Gate 决策 |
| 审查打回次数 ≥ 3 | 提交 Human Gate 决策（扩大范围/延期/人工介入） |
| 知识图谱不可用 | BA 标注"手动分析"继续执行 |
| 产出物数量异常 | 记录差异，提交 Human Gate 决策 |

异常需记录到 `session-status.md` 的"异常记录"章节。

---

## 8. 关联文档

| 文档 | 路径 | 说明 |
|------|------|------|
| BA Agent 阶段 1 | `.claude/agents/ba-stage1.md` | BA 详细操作定义 |
| PM Agent 阶段 1 | `.claude/agents/pm-stage1.md` | PM 审查操作定义 |
| feature.md | `.claude/iterations/sprint-latest/feature.md` | 阶段 0 产出，本阶段输入 |
| requirements 模板 | `.claude/templates/requirements-template.md` | 需求文档模板 |
| User Story 拆分技能 | `.claude/skills/user-story-splitting.md` | US 拆分方法论 |
| Sub-feature 拆分技能 | `.claude/skills/sub-feature-splitting.md` | SF 拆分方法论 |
| tech-stack-profile.md | `.claude/context/tech-stack-profile.md` | 技术栈参考 |
| consistency-baseline.md | `.claude/context/consistency-baseline.md` | 代码风格参考 |
| graphify-out/ | `.claude/context/graphify-out/` | Graphify 图谱（必须分析） |
| session-status.md | `.claude/iterations/session-status.md` | 阶段状态追踪（需更新） |
| project.md | `.claude/context/project.md` | 项目上下文（需更新） |

---

## 9. 阶段 0 vs 阶段 1 结构对比（参考）

| 结构要素 | 阶段 0（00-init.md） | 阶段 1（重构后） |
|---------|---------------------|------------------|
| 概述 | ✅ 有，明确角色分工 | ✅ 有，明确执行模式 |
| 日志声明 | ✅ 有，表格化 | ✅ 有，表格化 |
| 前置条件检查 | ✅ 有，单独章节 | ✅ 有，单独章节 |
| 规则加载 | ✅ 有，表格化 | ✅ 有，表格化 |
| 执行流程 | Agent + Human Gate 交替 | Agent + Human Gate 交替 |
| Human Gate | 每个 Agent 后都有 | 每个 Agent 后都有 |
| 产出物清单 | ✅ 有，表格化 | ✅ 有，表格化+检查要点 |
| 状态更新职责 | ✅ 有（session-status + project） | ✅ 有（session-status + project） |
| 异常处理 | ✅ 有 | ✅ 有 |
| 关联文档 | ✅ 有 | ✅ 有（含需更新的文档标注） |