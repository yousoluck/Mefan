# 阶段状态更新完整性检查报告

> **检查依据**：`phase-check.md` 中定义的必须更新章节
> **检查范围**：阶段 0 ~ 阶段 4 的 Command 文件和 Agent 文件

---

## 1. session-status.md 必须更新章节总览

| 章节 | 必须更新时机 |
|------|-------------|
| `## 阶段完成记录` | 每个子阶段完成时 |
| `## 产出物追踪表` | 每个产出物完成时 |
| `## PM 阶段完成报告（标准化格式）` | 每个阶段完成时 |
| `## 自动推进状态` | 阶段进入/完成时 |

---

## 2. project.md 必须更新章节总览

| 章节 | 必须更新时机 |
|------|-------------|
| `### 迭代 sprint-latest` | 阶段 0 进入时 |
| `#### 详细文档` | 产出物完成时 |

---

## 3. 各阶段状态更新详细检查

### 阶段 0（00-init）- 会话初始化与上下文建立

#### 3.1.1 session-status.md 更新检查

| 章节 | 更新者 | Command/Agent | 操作位置 | 状态 |
|------|--------|---------------|----------|------|
| `## 阶段完成记录` | PM | `00-init.md` / `pm-stage0.md` | 操作 5.1 | ✅ 完整 |
| `## 产出物追踪表` | PM | `00-init.md` / `pm-stage0.md` | 操作 5.3 | ✅ 完整 |
| `## PM 阶段完成报告` | PM | `00-init.md` / `pm-stage0.md` | 操作 5.5 | ✅ 完整 |
| `## 自动推进状态` | PM | `00-init.md` / `pm-stage0.md` | 操作 5.4 | ✅ 完整 |
| `## 阶段完成记录` | Architect | `00-init.md` / `architect-stage0.md` | 操作 5.1 | ✅ 完整 |
| `## 产出物追踪表` | Architect | `00-init.md` / `architect-stage0.md` | 操作 5.3 | ✅ 完整 |
| `## PM 阶段完成报告` | Architect | `00-init.md` / `architect-stage0.md` | 操作 5.5 | ✅ 完整 |
| `## 自动推进状态` | Architect | `00-init.md` / `architect-stage0.md` | 操作 5.4 | ✅ 完整 |
| `## 阶段完成记录` | Analyst | `00-init.md` / `analyst-stage0.md` | 操作 6.1 | ✅ 完整 |
| `## 产出物追踪表` | Analyst | `00-init.md` / `analyst-stage0.md` | 操作 6.2 | ✅ 完整 |
| `## 阶段完成报告` | Analyst | `00-init.md` / `analyst-stage0.md` | 操作 6.4 | ✅ 完整 |
| `## 自动推进状态` | Analyst | `00-init.md` / `analyst-stage0.md` | 操作 6.3 | ✅ 完整 |

#### 3.1.2 project.md 更新检查

| 章节 | 更新者 | Command/Agent | 操作位置 | 状态 |
|------|--------|---------------|----------|------|
| `#### 详细文档` | PM | `00-init.md` / `pm-stage0.md` | 操作 5.6 | ✅ 完整 |
| `#### 详细文档` | Architect | `00-init.md` / `architect-stage0.md` | 操作 5.6 | ✅ 完整 |
| `#### 详细文档` | Analyst | `00-init.md` / `analyst-stage0.md` | 操作 6.5 | ❌ **不完整** |

**不完整原因**：Analyst Agent 文件 `analyst-stage0.md` 中声称会更新 project.md（见输出表格中"project.md 更新"），但实际代码中只有操作 6.4 记录阶段完成报告，操作 6.5 虽然存在但内容被截断。**需要在操作 6.5 中补充 project.md 详细文档状态更新代码**。

---

### 阶段 1（01-requirements）- 需求详细设计

#### 3.2.1 session-status.md 更新检查

| 章节 | 更新者 | Command/Agent | 操作位置 | 状态 |
|------|--------|---------------|----------|------|
| `## 阶段完成记录` | BA | `01-requirements.md` / `ba-stage1.md` | 需确认 | ⚠️ **需检查** |
| `## 产出物追踪表` | BA | `01-requirements.md` / `ba-stage1.md` | 需确认 | ⚠️ **需检查** |
| `## PM 阶段完成报告` | BA | `01-requirements.md` / `ba-stage1.md` | 需确认 | ⚠️ **需检查** |
| `## 自动推进状态` | BA | `01-requirements.md` / `ba-stage1.md` | 需确认 | ⚠️ **需检查** |
| `## 阶段完成记录` | PM | `01-requirements.md` / `pm-stage1.md` | 操作 5.1 | ✅ 完整 |
| `## 产出物追踪表` | PM | `01-requirements.md` / `pm-stage1.md` | 操作 5.2 | ✅ 完整 |
| `## PM 阶段完成报告` | PM | `01-requirements.md` / `pm-stage1.md` | 操作 5.4 | ✅ 完整 |
| `## 自动推进状态` | PM | `01-requirements.md` / `pm-stage1.md` | 操作 5.3 | ✅ 完整 |

#### 3.2.2 project.md 更新检查

| 章节 | 更新者 | Command/Agent | 操作位置 | 状态 |
|------|--------|---------------|----------|------|
| `#### 详细文档` | BA | `01-requirements.md` / `ba-stage1.md` | 需确认 | ⚠️ **需检查** |
| `#### 详细文档` | PM | `01-requirements.md` / `pm-stage1.md` | 操作 5.6 | ✅ 完整 |

**不完整原因**：
- BA Agent 的 session-status 和 project.md 更新**未在 phase-check 中明确**，但根据 phase-check 规范，BA 也应该在产出物完成时更新。
- BA 的 `ba-stage1.md` 文件**未包含更新 session-status.md 和 project.md 的操作步骤**，这与 PM 的操作不对称。

---

### 阶段 2（02-arch-qa）- 架构设计与测试策略

#### 3.3.1 session-status.md 更新检查

| 章节 | 更新者 | Command/Agent | 操作位置 | 状态 |
|------|--------|---------------|----------|------|
| `## 阶段完成记录` | Architect | `02-arch-qa.md` / `architect-stage2.md` | 操作 5.1 | ✅ 完整 |
| `## 产出物追踪表` | Architect | `02-arch-qa.md` / `architect-stage2.md` | 操作 5.2 | ✅ 完整 |
| `## 阶段完成报告` | Architect | `02-arch-qa.md` / `architect-stage2.md` | 操作 5.3 | ✅ 完整 |
| `## 阶段完成记录` | QA | `02-arch-qa.md` / `qa-stage2.md` | 操作 7.1 | ✅ 完整 |
| `## 产出物追踪表` | QA | `02-arch-qa.md` / `qa-stage2.md` | 操作 7.1 | ✅ 完整（仅更新test-plan为审核中） |
| `## 阶段完成报告` | QA | `02-arch-qa.md` / `qa-stage2.md` | 操作 7.2 | ✅ 完整 |
| `## 阶段完成记录` | PM-Audit | `02-arch-qa.md` / `pm-audit-stage2.md` | 操作 8.1 | ✅ 完整 |
| `## 产出物追踪表` | PM-Audit | `02-arch-qa.md` / `pm-audit-stage2.md` | 操作 8.2 | ✅ 完整 |
| `## 自动推进状态` | PM-Audit | `02-arch-qa.md` / `pm-audit-stage2.md` | 操作 8.3 | ✅ 完整 |
| `## 阶段完成报告` | PM-Audit | `02-arch-qa.md` / `pm-audit-stage2.md` | 操作 8.4 | ✅ 完整 |
| `## 阶段完成记录` | PM-Audit-TP | `02-arch-qa.md` / `pm-audit-testplan-stage2.md` | 操作 8.1 | ✅ 完整 |
| `## 产出物追踪表` | PM-Audit-TP | `02-arch-qa.md` / `pm-audit-testplan-stage2.md` | 操作 8.2 | ✅ 完整 |
| `## 阶段完成报告` | PM-Audit-TP | `02-arch-qa.md` / `pm-audit-testplan-stage2.md` | 操作 8.3 | ✅ 完整 |

**注意**：
- Architect 没有更新 `## 自动推进状态`，因为Architect完成后需要等PM-Audit审核通过后才能更新。
- QA 没有更新 `## 自动推进状态`，因为QA完成后需要等PM-Audit-TP审核通过后才能更新。
- PM-Audit（ADR审核）通过后更新了 `## 自动推进状态`。
- PM-Audit-TP（test-plan审核）通过后**未更新** `## 自动推进状态`（因为阶段2已完成，状态已经在PM-Audit时更新过了）。

#### 3.3.2 project.md 更新检查

| 章节 | 更新者 | Command/Agent | 操作位置 | 状态 |
|------|--------|---------------|----------|------|
| `#### 详细文档` | Architect | `02-arch-qa.md` / `architect-stage2.md` | 操作 6.2 | ✅ 完整 |
| `#### 详细文档` | QA | `02-arch-qa.md` / `qa-stage2.md` | 操作 8.2 | ✅ 完整 |
| `#### 详细文档` | PM-Audit | `02-arch-qa.md` / `pm-audit-stage2.md` | 操作 9.2 | ✅ 完整 |

---

### 阶段 3（03-plan）- 迭代计划与任务排期

#### 3.4.1 session-status.md 更新检查

| 章节 | 更新者 | Command/Agent | 操作位置 | 状态 |
|------|--------|---------------|----------|------|
| `## 阶段完成记录` | Analyst | `03-plan.md` / `analyst-stage3.md` | 无 | ❌ **不完整** |
| `## 产出物追踪表` | Analyst | `03-plan.md` / `analyst-stage3.md` | 无 | ❌ **不完整** |
| `## 阶段完成报告` | Analyst | `03-plan.md` / `analyst-stage3.md` | 无 | ❌ **不完整** |
| `## 阶段完成记录` | PM | `03-plan.md` / `pm-stage3.md` | 操作 8.1 | ✅ 完整 |
| `## 产出物追踪表` | PM | `03-plan.md` / `pm-stage3.md` | 操作 8.1 | ✅ 完整 |
| `## 自动推进状态` | PM | `03-plan.md` / `pm-stage3.md` | 操作 8.1 | ✅ 完整 |
| `## PM 阶段完成报告` | PM | `03-plan.md` / `pm-stage3.md` | 操作 8.2 | ✅ 完整 |

**不完整原因**：
- Analyst Agent 的 `analyst-stage3.md` **没有更新 session-status.md 的操作步骤**，只生成了 sprint-status.md 供 PM 使用。
- 根据 phase-check 规范，Analyst 也应该在产出物完成时更新 session-status.md。

#### 3.4.2 project.md 更新检查

| 章节 | 更新者 | Command/Agent | 操作位置 | 状态 |
|------|--------|---------------|----------|------|
| `#### 详细文档` | PM | `03-plan.md` / `pm-stage3.md` | 操作 8.3 | ✅ 完整 |

**不完整原因**：Analyst 没有更新 project.md。

---

### 阶段 4（04-implement）- 迭代实现

#### 3.5.1 session-status.md 更新检查

| 章节 | 更新者 | Command/Agent | 操作位置 | 状态 |
|------|--------|---------------|----------|------|
| `## 阶段完成记录` | PM | `04-implement.md` / `pm-stage4.md` | 步骤 3 | ⚠️ **部分完整** |
| `## 产出物追踪表` | PM | `04-implement.md` / `pm-stage4.md` | 步骤 3 | ⚠️ **部分完整** |
| `## 阶段完成报告` | PM | `04-implement.md` / `pm-stage4.md` | 步骤 3 | ⚠️ **部分完整** |
| `## 自动推进状态` | PM | `04-implement.md` / `pm-stage4.md` | 步骤 3 | ⚠️ **部分完整** |

**不完整原因**：
- `04-implement.md` 的"步骤 3：阶段 4 完成汇总"只提到更新 session-status.md 状态为"✅"，**没有明确的操作步骤**。
- `pm-stage4.md` 文件需要检查是否包含完整的 4 个章节更新代码。

#### 3.5.2 project.md 更新检查

| 章节 | 更新者 | Command/Agent | 操作位置 | 状态 |
|------|--------|---------------|----------|------|
| `#### 详细文档` | PM | `04-implement.md` / `pm-stage4.md` | 无 | ❌ **未定义** |

**不完整原因**：`04-implement.md` 的状态更新职责章节（应新增第6节）**未定义 project.md 更新**。PM 完成阶段 4 后应更新 project.md 中相关文档状态。

---

## 4. 问题汇总表

### 4.1 必须补充的更新操作

| 阶段 | 文档 | 章节 | 更新者 | 当前状态 | 需要补充的内容 |
|------|------|------|--------|----------|----------------|
| **00** | project.md | `#### 详细文档` | Analyst | ❌ 不完整 | 在操作 6.5 中补充 project.md 详细文档状态更新代码 |
| **01** | session-status.md | `## 阶段完成记录/产出物追踪表/阶段完成报告` | BA | ❌ 未定义 | 在 `ba-stage1.md` 中补充 session-status.md 更新操作 |
| **01** | project.md | `#### 详细文档` | BA | ❌ 未定义 | 在 `ba-stage1.md` 中补充 project.md 更新操作 |
| **03** | session-status.md | `## 阶段完成记录/产出物追踪表/阶段完成报告` | Analyst | ❌ 不完整 | 在 `analyst-stage3.md` 中补充 session-status.md 更新操作 |
| **03** | project.md | `#### 详细文档` | Analyst | ❌ 不完整 | 在 `analyst-stage3.md` 中补充 project.md 更新操作 |
| **04** | session-status.md | `## 阶段完成记录/产出物追踪表/阶段完成报告/自动推进状态` | PM | ⚠️ 部分完整 | 在 `04-implement.md` 步骤 3 和 `pm-stage4.md` 中补充明确的 4 个章节更新代码 |
| **04** | project.md | `#### 详细文档` | PM | ❌ 未定义 | 在 `04-implement.md` 新增状态更新职责章节，定义 project.md 更新 |
| **05** | session-status.md | 所有章节 | 各Agent | ⚠️ 部分完整 | 在 `05-quality.md` 新增状态更新职责章节 |
| **05** | project.md | `#### 详细文档` | 各Agent | ❌ 未定义 | 在 `05-quality.md` 新增状态更新职责章节 |
| **06** | session-status.md | 所有章节 | 各Agent | ⚠️ 部分完整 | 在 `06-retrospect.md` 新增状态更新职责章节 |
| **06** | project.md | `#### 详细文档` | 各Agent | ❌ 未定义 | 在 `06-retrospect.md` 新增状态更新职责章节 |

### 4.2 问题严重度分类

| 严重度 | 问题描述 | 影响阶段 |
|--------|----------|----------|
| **P1** | BA 在阶段 1 未更新 session-status.md 和 project.md | 01 |
| **P1** | Analyst 在阶段 3 未更新 session-status.md | 03 |
| **P1** | 阶段 4 session-status.md 更新操作不明确 | 04 |
| **P2** | 阶段 4-6 未定义 project.md 更新职责 | 04, 05, 06 |
| **P3** | 阶段 0 Analyst project.md 更新不完整 | 00 |

---

## 5. 建议修复优先级

### 立即修复（P1）

1. **`ba-stage1.md`**：补充 session-status.md 和 project.md 更新操作
2. **`analyst-stage3.md`**：补充 session-status.md 更新操作
3. **`04-implement.md` + `pm-stage4.md`**：补充明确的 session-status.md 4 个章节更新代码

### 稍后修复（P2）

4. **`00-init.md` / `analyst-stage0.md`**：补充 project.md 更新操作
5. **`04-implement.md`**：新增状态更新职责章节，定义 project.md 更新
6. **`05-quality.md`**：新增状态更新职责章节
7. **`06-retrospect.md`**：新增状态更新职责章节

---

## 6. 检查方法

每个阶段结束时，使用以下命令验证状态更新是否完整：

```bash
# 检查 session-status.md 各章节是否有内容
grep -A5 "## 阶段完成记录" .claude/iterations/session-status.md
grep -A5 "## 产出物追踪表" .claude/iterations/session-status.md
grep -A10 "## PM 阶段完成报告" .claude/iterations/session-status.md
grep -A5 "## 自动推进状态" .claude/iterations/session-status.md

# 检查 project.md 详细文档状态
grep -A10 "#### 详细文档" .claude/context/project.md
```