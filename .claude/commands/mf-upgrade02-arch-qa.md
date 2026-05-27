# /mf-upgrade:02-arch-qa – 架构设计与测试策略

> **当前阶段**：阶段 2（架构设计与测试策略）
> **主导角色**：架构师 (Architect)
> **辅助角色**：项目经理 (PM)、质量保证 (QA)
> **前置条件**：阶段 1 已完成，requirements.md 存在且状态为"✅ 已完成"
> **执行模式**：Architect → PM 审核（≤3次循环）→ QA 串行执行

---

## 0. 概述

本阶段由架构师 Agent 主导，执行完整的架构设计，生成 ADR 文档。ADR 完成后交由 PM Agent 审核（最多3次循环），审核通过后由 QA Agent 执行测试策略设计，生成 test-plan 文档。

**流程**：
```
Architect Agent → 生成 ADR
       ↓
PM Agent 审核（≤3次循环）
       ↓
QA Agent → 生成 test-plan
```

---

## 1. 日志声明

执行本 playbook 时，必须使用 `.claude/hooks/log-event.sh` 记录日志：

| 事件类型 | 日志命令格式 |
|---------|-------------|
| 阶段进入 | `bash .claude/hooks/log-event.sh "02" "Command" "阶段进入" "阶段2开始" "" "成功"` |
| Architect 激活 | `bash .claude/hooks/log-event.sh "02" "Command" "Agent激活" "Architect开始执行" "" "进行中"` |
| Architect 完成 | `bash .claude/hooks/log-event.sh "02" "Command" "Agent完成" "Architect产出完成" "" "成功"` |
| PM 审核激活 | `bash .claude/hooks/log-event.sh "02" "Command" "Agent激活" "PM开始审核" "" "进行中"` |
| PM 审核完成 | `bash .claude/hooks/log-event.sh "02" "Command" "Agent完成" "PM审核完成" "" "成功"` |
| QA 激活 | `bash .claude/hooks/log-event.sh "02" "Command" "Agent激活" "QA开始执行" "" "进行中"` |
| QA 完成 | `bash .claude/hooks/log-event.sh "02" "Command" "Agent完成" "QA产出完成" "" "成功"` |
| 阶段退出 | `bash .claude/hooks/log-event.sh "02" "Command" "阶段退出" "阶段2完成" "" "成功"` |

---

## 2. 前置条件检查

> **重要**：阶段 2 开始前，必须验证所有前置条件

### 2.1 requirements.md 检查

```bash
# 检查 requirements.md 是否存在
if [ ! -f "$ROOT/.claude/iterations/sprint-latest/requirements.md" ]; then
  echo "[Error] requirements.md 不存在，阶段 2 无法开始"
  echo "请先完成阶段 1 或运行 /mf-upgrade:01-requirements"
  exit 1
fi

# 检查 requirements.md 状态
if ! grep -q "✅ 已完成" "$ROOT/.claude/iterations/sprint-latest/requirements.md"; then
  echo "[Warning] requirements.md 尚未标记为完成，阶段 2 可能无法正常执行"
fi

# 统计 User Story 和 Sub-feature 数量
US_COUNT=$(grep -c "^## US-" "$ROOT/.claude/iterations/sprint-latest/requirements.md" || echo "0")
SF_COUNT=$(grep -c "^##### SF-" "$ROOT/.claude/iterations/sprint-latest/requirements.md" || echo "0")
echo "[前置检查] User Story 数量：$US_COUNT, Sub-feature 数量：$SF_COUNT"
```

### 2.2 依赖文档检查

```bash
# 检查必要依赖文档是否存在
echo "[前置检查] 加载依赖文档..."
ls -la $ROOT/.claude/context/tech-stack-profile.md 2>/dev/null || echo "[Warning] tech-stack-profile.md 不存在"
ls -la $ROOT/.claude/context/consistency-baseline.md 2>/dev/null || echo "[Warning] consistency-baseline.md 不存在"
ls -la $ROOT/.claude/context/knowledge.grap 2>/dev/null || echo "[Info] knowledge.grap 不存在，将使用手动分析"
```

---

## 3. 规则加载

按需引用（不在阶段开头集中声明）：

| 规则/技能 | 用途 | 引用时机 |
|-----------|------|---------|
| `.claude/rules/global/session-init.md` | 阶段初始化规则 | 前置条件检查前 |
| `.claude/rules/scenario-upgrade/consistency-first.md` | 一致性优先规则 | Architect 架构设计时 |
| `.claude/rules/scenario-upgrade/api-compatibility.md` | API兼容性规则 | Architect API 设计时 |
| `.claude/rules/scenario-upgrade/reuse-before-build.md` | 复用优先规则 | Architect 设计时 |
| `.claude/rules/scenario-upgrade/reference-module.md` | 参考模块规则 | Architect 参考实现定位时 |
| `.claude/rules/global/conflict-resolution.md` | 设计冲突升级 | Architect 设计冲突时 |
| `.claude/rules/global/quality-gates.md` | 质量门禁标准 | QA 测试策略设计时 |
| `.claude/agents/architect-stage2.md` | Architect 阶段2完整业务流程 | Architect 执行时 |
| `.claude/agents/pm-stage2.md` | PM 阶段2完整业务流程 | PM 审核时 |
| `.claude/agents/qa-stage2.md` | QA 阶段2完整业务流程 | QA 执行时 |

---

## 4. 执行流程

### 4.1 阶段进入日志

```bash
bash .claude/hooks/log-event.sh "02" "Command" "阶段进入" "阶段2开始" "" "成功"
```

---

### 4.2 Architect Agent 执行（生成 ADR）

**前置条件**：前置条件检查通过
**执行文件**：`.claude/agents/architect-stage2.md`

激活 Architect Agent（串行，等待完成）：

```
Agent: architect-stage2.md
run_in_background: false
```

激活后等待 Architect Agent 完成，记录日志：

```bash
bash .claude/hooks/log-event.sh "02" "Command" "Agent激活" "Architect开始执行" "" "进行中"
# 等待 Architect Agent 完成（由 Agent 自己写入日志）
bash .claude/hooks/log-event.sh "02" "Command" "Agent完成" "Architect产出完成" "" "成功"
```

#### 4.2.1 Human Gate 确认（Architect 产出）

> Architect Agent 完成执行后，必须等待用户确认才能继续

**人工检查项**：

| 检查维度 | 检查内容 | 期望状态 | 不通过处理 |
|---------|---------|---------|-----------|
| **ADR 生成** | ADR.md 是否已生成在 `.claude/iterations/sprint-latest/ADR.md` | 存在 | 打回 Architect 修复 |
| **自检清单** | Architect 是否已完成自检 | 自检通过 | 打回 Architect 修复 |
| **产出完整性** | ADR 是否覆盖所有 User Story | 覆盖所有 US | 打回 Architect 补充 |

**快速验证命令**：
```bash
# 检查 ADR.md 是否存在
ls .claude/iterations/sprint-latest/ADR.md

# 检查 ADR.md 章节数量
grep -c "^## " .claude/iterations/sprint-latest/ADR.md

# 检查是否包含所有 User Story
grep "^## US-" .claude/iterations/sprint-latest/ADR.md
```

**回复选项**：
- `继续` - 所有检查项通过，进入 PM 审核阶段
- `打回` - 列出需要修正的问题，Architect 重新执行
- `暂停` - 暂停阶段 2，等待进一步指示

---

### 4.3 PM Agent 执行（审核 ADR）

**前置条件**：Architect 产出通过 Human Gate
**执行文件**：`.claude/agents/pm-audit-stage2.md`

#### 4.3.1 审核循环机制（≤3次）

**循环流程**：
```
PM-Audit Agent（审核） → [发现问题] → Architecture-Fix Agent（修复） → [循环]
                            ↓ [无问题]
                         审核通过
```

**第 N 轮审核流程**：

1. **激活 PM-Audit Agent**（串行，等待完成）：
   ```
   Agent: pm-audit-stage2.md
   run_in_background: false
   ```

   ```bash
   bash .claude/hooks/log-event.sh "02" "Command" "Agent激活" "PM-Audit开始审核" "" "进行中"
   # 等待 PM-Audit Agent 完成
   bash .claude/hooks/log-event.sh "02" "Command" "Agent完成" "PM-Audit审核完成" "" "成功"
   ```

2. **Human Gate 确认（PM-Audit 产出）**

   **等待用户确认以下内容**：

   - `继续` - 允许进入 Architecture-Fix 阶段修复问题
   - `暂停` - 暂停阶段 2，等待进一步指示

3. **检查审核结论**

   如果 adr-review.md 中"总体结论"为"通过"：
   - 审核通过，流程结束
   - 直接进入 4.4 QA 阶段

   如果 adr-review.md 中"总体结论"为"不通过"：
   - 继续执行 Architecture-Fix Agent

4. **激活 Architecture-Fix Agent**（修复问题）：

   ```
   Agent: architecture-fix-adr-stage02.md
   run_in_background: false
   ```

   ```bash
   bash .claude/hooks/log-event.sh "02" "Command" "Agent激活" "Architecture-Fix开始修复" "" "进行中"
   # 等待 Architecture-Fix Agent 完成
   bash .claude/hooks/log-event.sh "02" "Command" "Agent完成" "Architecture-Fix修复完成" "" "成功"
   ```

5. **Human Gate 确认（Architecture-Fix 产出）**

   **等待用户确认以下内容**：

   - `继续` - 允许返回 PM-Audit 进行下一轮审核
   - `暂停` - 暂停阶段 2，等待进一步指示

6. **循环控制**
   ```bash
   # 检查审核轮次
   REVIEW_COUNT=$(cat "$ROOT/.claude/iterations/sprint-latest/reviews/.adr-review-round" 2>/dev/null || echo "0")
   echo "[PM-Stage2] 当前审核轮次：$REVIEW_COUNT / 3"

   if [ $REVIEW_COUNT -ge 3 ]; then
     echo "[PM-Stage2] 审核轮次已达3次上限，提交 Human Decision"
     bash .claude/hooks/log-event.sh "02" "PM" "警告" "审核轮次超限" "" "需 Human Decision"
   fi
   ```

7. **返回步骤 1 进行下一轮审核**

#### 4.3.2 审核通过条件

> 满足以下任一条件视为审核通过：
> 1. adr-review.md 中所有问题状态为 Closed
> 2. adr-review.md 中总体结论标示为通过
> 3. 审核轮次达 3 次上限但问题数量 ≤ 3

#### 4.3.3 Human Gate 确认（PM 审核结果）

> PM Agent 完成审核后，必须等待用户确认才能进入 QA 阶段

**人工检查项**：

| 检查维度 | 检查内容                | 期望状态 | 不通过处理 |
|---------|---------------------|---------|-----------|
| **审核结果** | adr-review.md 中问题状态 | 所有问题为 Closed | 需修复 |
| **审核轮次** | 审核是否已达3次上限          | < 3 次 | 需 Human Decision |
| **ADR 状态** | ADR.md 是否标记为已审批     | ✅ | 需确认 |

**快速验证命令**：
```bash
# 检查 adr-review.md 中的问题状态
grep "| Open |" .claude/iterations/sprint-latest/reviews/adr-review.md
grep "| Unfixed |" .claude/iterations/sprint-latest/reviews/adr-review.md

# 检查审核轮次
cat .claude/iterations/sprint-latest/reviews/.adr-review-round

# 检查总体结论
grep "总体结论" .claude/iterations/sprint-latest/reviews/adr-review.md
```

**回复选项**：
- `继续` - 审核通过，进入 QA 阶段
- `复查` - 需要重新审核，PM 重新执行
- `暂停` - 暂停阶段 2，等待进一步指示

---

### 4.4 QA Agent 执行（生成 test-plan）

**前置条件**：ADR 审核通过
**执行文件**：`.claude/agents/qa-stage2.md`

#### 4.4.1 QA Agent 生成 test-plan

激活 QA Agent（串行，等待完成）：

```
Agent: qa-stage2.md
run_in_background: false
```

激活后等待 QA Agent 完成，记录日志：

```bash
bash .claude/hooks/log-event.sh "02" "Command" "Agent激活" "QA开始执行" "" "进行中"
# 等待 QA Agent 完成
bash .claude/hooks/log-event.sh "02" "Command" "Agent完成" "QA产出完成" "" "成功"
```

#### 4.4.2 Human Gate 确认（QA 产出）

> QA Agent 完成执行后，必须等待用户确认才能进入 test-plan 审核阶段

**人工检查项**：

| 检查维度 | 检查内容 | 期望状态 | 不通过处理 |
|---------|---------|---------|-----------|
| **test-plan 生成** | test-plan.md 是否已生成 | 存在 | 打回 QA 修复 |
| **回归测试范围** | 是否列出受影响模块的回归测试 | 有列表 | 打回 QA 补充 |
| **新增测试用例** | 是否列出新增测试用例 | 有列表 | 打回 QA 补充 |

**快速验证命令**：
```bash
# 检查 test-plan.md 是否存在
ls .claude/iterations/sprint-latest/test-plan.md

# 检查测试用例数量
grep -c "^### TC-" .claude/iterations/sprint-latest/test-plan.md
```

**回复选项**：
- `继续` - 所有检查项通过，进入 PM-Audit-TP 审核阶段
- `打回` - 列出需要修正的问题，QA 重新执行
- `暂停` - 暂停阶段 2，等待进一步指示

---

### 4.5 PM-Audit-TP Agent 执行（审核 test-plan）

**前置条件**：QA 产出通过 Human Gate
**执行文件**：`.claude/agents/pm-audit-testplan-stage2.md`

#### 4.5.1 审核循环机制（≤3次）

**循环流程**：
```
PM-Audit-TP Agent（审核） → [发现问题] → QA-Fix-TP Agent（修复） → [循环]
                            ↓ [无问题]
                         审核通过
```

**第 N 轮审核流程**：

1. **激活 PM-Audit-TP Agent**（串行，等待完成）：
   ```
   Agent: pm-audit-testplan-stage2.md
   run_in_background: false
   ```

   ```bash
   bash .claude/hooks/log-event.sh "02" "Command" "Agent激活" "PM-Audit-TP开始审核" "" "进行中"
   # 等待 PM-Audit-TP Agent 完成
   bash .claude/hooks/log-event.sh "02" "Command" "Agent完成" "PM-Audit-TP审核完成" "" "成功"
   ```

2. **Human Gate 确认（PM-Audit-TP 产出）**

   **等待用户确认以下内容**：

   - `继续` - 允许进入 QA-Fix-TP 阶段修复问题
   - `暂停` - 暂停阶段 2，等待进一步指示

3. **检查审核结论**

   如果 testplan-review.md 中"总体结论"为"通过"：
   - 审核通过，流程结束
   - 直接进入 4.6 阶段退出

   如果 testplan-review.md 中"总体结论"为"不通过"：
   - 继续执行 QA-Fix-TP Agent

4. **激活 QA-Fix-TP Agent**（修复问题）：

   ```
   Agent: qa-fix-testplan-stage2.md
   run_in_background: false
   ```

   ```bash
   bash .claude/hooks/log-event.sh "02" "Command" "Agent激活" "QA-Fix-TP开始修复" "" "进行中"
   # 等待 QA-Fix-TP Agent 完成
   bash .claude/hooks/log-event.sh "02" "Command" "Agent完成" "QA-Fix-TP修复完成" "" "成功"
   ```

5. **Human Gate 确认（QA-Fix-TP 产出）**

   **等待用户确认以下内容**：

   - `继续` - 允许返回 PM-Audit-TP 进行下一轮审核
   - `暂停` - 暂停阶段 2，等待进一步指示

6. **循环控制**
   ```bash
   # 检查审核轮次
   REVIEW_COUNT=$(cat "$ROOT/.claude/iterations/sprint-latest/reviews/.testplan-review-round" 2>/dev/null || echo "0")
   echo "[PM-Audit-TP-Stage2] 当前审核轮次：$REVIEW_COUNT / 3"

   if [ $REVIEW_COUNT -ge 3 ]; then
     echo "[PM-Audit-TP-Stage2] 审核轮次已达3次上限，提交 Human Decision"
     bash .claude/hooks/log-event.sh "02" "PM" "警告" "审核轮次超限" "" "需 Human Decision"
   fi
   ```

7. **返回步骤 1 进行下一轮审核**

#### 4.5.2 审核通过条件

> 满足以下任一条件视为审核通过：
> 1. testplan-review.md 中所有问题状态为 Closed
> 2. testplan-review.md 中总体结论标示为通过
> 3. 审核轮次达 3 次上限但问题数量 ≤ 3

#### 4.5.3 Human Gate 确认（PM-Audit-TP 审核结果）

> PM-Audit-TP Agent 完成审核后，必须等待用户确认才能结束阶段 2

**人工检查项**：

| 检查维度 | 检查内容                | 期望状态 | 不通过处理 |
|---------|---------------------|---------|-----------|
| **审核结果** | testplan-review.md 中问题状态 | 所有问题为 Closed | 需修复 |
| **审核轮次** | 审核是否已达3次上限          | < 3 次 | 需 Human Decision |
| **test-plan 状态** | test-plan.md 是否标记为已审批     | ✅ | 需确认 |

**快速验证命令**：
```bash
# 检查 testplan-review.md 中的问题状态
grep "| Open |" .claude/iterations/sprint-latest/reviews/testplan-review.md
grep "| Unfixed |" .claude/iterations/sprint-latest/reviews/testplan-review.md

# 检查审核轮次
cat .claude/iterations/sprint-latest/reviews/.testplan-review-round

# 检查总体结论
grep "总体结论" .claude/iterations/sprint-latest/reviews/testplan-review.md
```

**回复选项**：
- `继续` - 审核通过，进入阶段退出
- `复查` - 需要重新审核，PM-Audit-TP 重新执行
- `暂停` - 暂停阶段 2，等待进一步指示

---

### 4.6 阶段退出

```bash
bash .claude/hooks/log-event.sh "02" "Command" "阶段退出" "阶段2完成" "" "成功"
```

---

## 5. 产出物清单

阶段 2 完成时，应有如下产出物：

| 产出物 | 路径 | 状态 | 产出者 | 检查要点 |
|--------|------|------|--------|---------|
| **ADR 主文档** | `.claude/iterations/sprint-latest/ADR.md` | ✅ | Architect | 包含所有 US 设计 |
| **adr-review.md** | `.claude/iterations/sprint-latest/reviews/adr-review.md` | ✅ | PM-Audit | ADR 审核问题汇总 |
| **review-log.md** | `.claude/iterations/sprint-latest/reviews/review-log.md` | ✅ | PM-Audit | 跨阶段问题追踪 |
| **test-plan.md** | `.claude/iterations/sprint-latest/test-plan.md` | ✅ | QA | 测试策略和用例 |
| **testplan-review.md** | `.claude/iterations/sprint-latest/reviews/testplan-review.md` | ✅ | PM-Audit-TP | test-plan 审核问题汇总 |
| **session-status.md 更新** | `.claude/iterations/sprint-latest/session-status.md` | ✅ | 各Agent | 阶段完成记录 |
| **project.md 更新** | `.claude/context/project.md` | ✅ | Architect/PM-Audit | 迭代历史状态 |

---

## 6. 状态更新职责

> 阶段 2 需要更新以下文档，详见各 Agent 执行文件

| 文档 | 更新者 | 更新内容 |
|------|--------|---------|
| **session-status.md** | Architect/PM-Audit/QA | 阶段完成记录（阶段 02）、产出物追踪表 |
| **project.md** | Architect/PM-Audit | 迭代历史中 ADR/test-plan 状态 |
| **ADR.md** | Architect | ADR 基本信息（状态） |
| **adr-review.md** | PM-Audit | ADR 问题汇总、审核历史 |
| **review-log.md** | PM-Audit | 跨阶段问题追踪 |
| **test-plan.md** | QA | test-plan 基本信息（状态） |
| **testplan-review.md** | PM-Audit-TP | test-plan 问题汇总、审核历史 |

**更新时机**：各 Agent 完成各自任务后，Human Gate 确认前

---

## 7. 异常处理

| 异常场景 | 处理方式 |
|---------|---------|
| requirements.md 不存在 | 报错退出，要求先完成阶段 1 |
| requirements.md 未完成 | 警告并要求确认是否继续 |
| ADR.md 不存在 | 报错退出，Architect 需先生成 ADR |
| Architect 执行失败 | 记录异常，提交 Human Gate 决策 |
| PM-Audit 审核失败 | 记录异常，提交 Human Gate 决策 |
| Architecture-Fix 修复失败 | 记录异常，提交 Human Gate 决策 |
| QA 执行失败 | 记录异常，提交 Human Gate 决策 |
| PM-Audit-TP 审核失败 | 记录异常，提交 Human Gate 决策 |
| QA-Fix-TP 修复失败 | 记录异常，提交 Human Gate 决策 |
| ADR 审核循环 3 次仍不通过 | 提交 Human Decision |
| test-plan 审核循环 3 次仍不通过 | 提交 Human Decision |
| knowledge.grap 不可用 | Architect/QA 标注"手动分析"继续执行 |
| 产出物数量异常 | 记录差异，提交 Human Gate 决策 |

异常需记录到 `session-status.md` 的"异常记录"章节。

---

## 8. 关联文档

| 文档 | 路径 | 说明 |
|------|------|------|
| Architect Agent 阶段2 | `.claude/agents/architect-stage2.md` | Architect 生成 ADR |
| PM-Audit Agent 阶段2 | `.claude/agents/pm-audit-stage2.md` | PM 审核 ADR |
| Architecture-Fix Agent 阶段2 | `.claude/agents/architecture-fix-adr-stage02.md` | Architect 修复 ADR 问题 |
| QA Agent 阶段2 | `.claude/agents/qa-stage2.md` | QA 生成 test-plan |
| PM-Audit-TP Agent 阶段2 | `.claude/agents/pm-audit-testplan-stage2.md` | PM 审核 test-plan |
| QA-Fix-TP Agent 阶段2 | `.claude/agents/qa-fix-testplan-stage2.md` | QA 修复 test-plan 问题 |
| requirements.md | `.claude/iterations/sprint-latest/requirements.md` | 阶段 1 产出，本阶段输入 |
| ADR 模板 | `.claude/templates/adr-template.md` | ADR 文档模板 |
| ADR Review 模板 | `.claude/templates/adr-review-template.md` | ADR 审核模板 |
| test-plan Review 模板 | `.claude/templates/test-plan-review-template.md` | test-plan 审核模板 |
| review-log 模板 | `.claude/templates/review-log-template.md` | 审核记录模板 |
| test-plan 模板 | `.claude/templates/test-plan-template.md` | 测试计划模板 |
| tech-stack-profile.md | `.claude/context/tech-stack-profile.md` | 技术栈参考 |
| consistency-baseline.md | `.claude/context/consistency-baseline.md` | 代码风格参考 |
| knowledge.grap | `.claude/context/knowledge.grap` | 知识图谱（必须分析） |
| session-status.md | `.claude/iterations/session-status.md` | 阶段状态追踪（需更新） |
| project.md | `.claude/context/project.md` | 项目上下文（需更新） |

---

## 9. 阶段 1 vs 阶段 2 结构对比（参考）

| 结构要素 | 阶段 1（01-requirements.md） | 阶段 2（重构后） |
|---------|------------------------------|-----------------|
| 概述 | ✅ 有，明确角色分工 | ✅ 有，明确执行模式 |
| 日志声明 | ✅ 有，表格化 | ✅ 有，表格化 |
| 前置条件检查 | ✅ 有，单独章节 | ✅ 有，单独章节 |
| 规则加载 | ✅ 有，表格化 | ✅ 有，表格化 |
| 执行流程 | BA → PM 串行 | Architect → PM-Audit 审核循环 → QA → PM-Audit-TP 审核循环 |
| Human Gate | 每个 Agent 后都有 | Architect 后有，PM-Audit 循环后有，QA 后有，PM-Audit-TP 循环后有 |
| 产出物清单 | ✅ 有，表格化 | ✅ 有，表格化+检查要点 |
| 状态更新职责 | ✅ 有 | ✅ 有 |
| 异常处理 | ✅ 有 | ✅ 有 |
| 关联文档 | ✅ 有 | ✅ 有（含需更新的文档标注） |
| **审核循环** | 无 | ✅ 有（≤3次） |
| **review-log** | 无 | ✅ 有 |