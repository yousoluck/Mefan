# /mf-upgrade:04-implement – 迭代实现（重构版）

> **当前阶段**：阶段 4（迭代实现）
> **前置条件**：阶段 3 已完成，sprint-status.md 存在（包含 MG 划分和 Task 清单）
> **执行模式**：按 MG 并行开发，每个 MG 经历 7 状态流转，每个检查点有循环修复机制（最多 3 次）

---

## 0. 概述

### 0.1 7状态流转（每个MG独立运行）

```
🏃 Dev → 🔍 Self-Check → 🖥️ Code Review → 🧪 QA-Test-Coding → 🔬 Test Code Review → ✅ Testing → 🎉 Close
         ↑                    ↑                  ↑                    ↑              ↑
         │                    │                  │                    │              │
    (无循环限制)         Dev-Fix循环        QA-Fix循环           QA-Fix循环     Dev-Fix循环
                          (≤3次)              (≤3次)               (≤3次)         (≤3次)
```

| 状态 | 名称 | 负责人 | 循环限制 |
|------|------|--------|----------|
| 🏃 Dev | 开发中 | Dev | - |
| 🔍 Self-Check | 自我检查 | Dev | 无限制 |
| 🖥️ Code Review | 代码检查 | Arch Agent | 3次 → Human Gate |
| 🧪 QA-Test-Coding | QA测试代码编写 | QA | 3次 → Human Gate |
| 🔬 Test Code Review | 测试代码检查 | Arch Agent | 3次 → Human Gate |
| ✅ Testing | 人工测试 | QA | 3次 → Human Gate |
| 🎉 Close | 完成 | PM | - |

### 0.2 循环修复机制（关键差异于阶段 2）

**循环流程**：
```
检查失败 → 记录到 review-log.md → 触发 Fix Agent 修复 → 重新检查 → repeat
                        ↑                                              │
                        └────── 循环 3 次未通过 → Human Gate ←──────┘
```

**每个检查点的循环**：

| 检查点 | Fix Agent | 循环次数 |
|--------|-----------|----------|
| Code Review | Dev-Fix | 3次 |
| QA-Test-Coding | QA-Fix | 3次 |
| Test Code Review | QA-Fix | 3次 |
| Testing Bug | Dev-Fix | 3次 |

### 0.3 并行策略

- 多个 MG 可并行开发（按 sprint-status.md 第 6 节并行策略）
- 同一 MG 内串行执行 7 状态
- 全部 MG 进入 Close 后，阶段 4 完成

### 0.4 Human Gate 策略

- 每个检查点最多 3 次循环，超时报告人类
- 所有问题同步到 `.claude/iterations/sprint-latest/reviews/review-log.md`
- P0 缺陷立即暂停，报告 Human Gate

---

## 1. 日志声明

执行本 playbook 时，必须使用 `.claude/hooks/log-event.sh` 记录日志：

| 事件类型 | 日志命令格式 |
|---------|-------------|
| 阶段进入 | `bash .claude/hooks/log-event.sh "04" "Command" "阶段进入" "阶段4开始" "" "成功"` |
| MG开发开始 | `bash .claude/hooks/log-event.sh "04" "Command" "MG开始" "MG-001开发开始" "" "进行中"` |
| 状态转换 | `bash .claude/hooks/log-event.sh "04" "Command" "状态转换" "MG-001:Dev→Self-Check" "" "成功"` |
| 问题发现 | `bash .claude/hooks/log-event.sh "04" "Command" "问题发现" "MG-001:CodeReview发现N个问题" "" "待修复"` |
| 循环计数 | `bash .claude/hooks/log-event.sh "04" "Command" "循环计数" "MG-001:CodeReview循环2/3" "" "进行中"` |
| MG完成 | `bash .claude/hooks/log-event.sh "04" "Command" "MG完成" "MG-001进入Close" "" "成功"` |
| 阶段退出 | `bash .claude/hooks/log-event.sh "04" "Command" "阶段退出" "阶段4完成" "" "成功"` |

---

## 2. 前置检查

### 2.1 阶段 3 完成状态检查

```bash
source "$(dirname "${BASH_SOURCE[0]}")/../snippets/source-root.sh"

# 检查 session-status.md 中阶段 3 状态
if ! grep -q "阶段 03.*✅" "$ROOT/.claude/iterations/session-status.md" 2>/dev/null; then
  echo "[Error] 阶段 3 尚未完成，阶段 4 无法开始"
  exit 1
fi

# 检查 sprint-status.md 是否存在
if [ ! -f "$ROOT/.claude/iterations/sprint-latest/sprint-status.md" ]; then
  echo "[Error] sprint-status.md 不存在，请先执行 /mf-upgrade:03-plan"
  exit 1
fi
```

### 2.2 检查 sprint-status.md 完整性

```bash
# 检查是否包含 MG 划分
grep -q "^## 1. User Story 分组与 Modular Group" "$ROOT/.claude/iterations/sprint-latest/sprint-status.md" || {
  echo "[Error] sprint-status.md 缺少 MG 划分，请检查阶段 3 产出物"
  exit 1
}

# 检查是否有 Task 清单
grep -q "^| T-" "$ROOT/.claude/iterations/sprint-latest/sprint-status.md" || {
  echo "[Error] sprint-status.md 缺少 Task 清单"
  exit 1
}
```

---

## 3. 工作流编排

### 步骤 1：初始化阶段 4 环境

- **激活 Agent**：`agents/pm-stage4.md`（阶段 4 初始化）
- **职责**：读取 sprint-status.md，确定本次迭代的 MG 列表和并行策略
- **产出物**：更新 session-status.md 中阶段 4 状态为"🔄 进行中"

```bash
# 更新 session-status.md
sed -i "s/| 04 | 迭代实现 |.*| ⏳ 待开始 |/| 04 | 迭代实现 | $(date +"%Y-%m-%d %H:%m") | 🔄 进行中 |/g" \
  "$ROOT/.claude/iterations/session-status.md"

# 安装 Git hooks（确保自动化检查可用）
bash .claude/hooks/install-hooks.sh
```

### 步骤 2：按 MG 并行开发

> 每个 MG 经历完整的 7 状态流转
>
> **触发时机**：步骤 1 完成后

对每个 Modular Group（MG）执行以下流程：

#### 步骤 2.1 🏃 Dev（开发中）

- **激活 Agent**：`agents/dev-stage4.md`
- **职责**：
  - 领取 MG 内所有 Task
  - 按 ADR 伪代码实现功能
  - 遵循 consistency-baseline.md 代码规范
  - 复用现有模块代码
- **前置检查**：
  - ADR.md 存在且包含 MG 对应的 Task 伪代码
  - consistency-baseline.md 可用
- **产出物**：
  - 源代码（按项目结构）
  - task-summary/T{NNN}.md（每个 Task 一个）
- **Self-Check 要求**：
  - Lint 检查通过
  - 单元测试通过
  - 手动功能验证通过
- **Hook 验证（状态转换门禁）**：
  ```bash
  # Dev 完成进入 Self-Check 前，必须通过以下 Hook 检查
  bash $ROOT/.claude/hooks/check-state-machine.sh "$MG_ID" "SelfCheck"
  bash $ROOT/.claude/hooks/check-adr-implementation.sh "$MG_ID"
  bash $ROOT/.claude/hooks/check-reference-consistency.sh
  ```
  - **失败则阻断状态转换**，Dev 继续修复直到通过
- **日志记录**：
  ```bash
  bash .claude/hooks/log-event.sh "04" "Dev" "领取任务" "MG-001:T-001,T-002,T-003" "" "进行中"
  bash .claude/hooks/log-event.sh "04" "Dev" "任务完成" "MG-001:T-001完成" "" "成功"
  bash .claude/hooks/log-event.sh "04" "Dev" "状态转换" "MG-001:Dev→SelfCheck" "" "待验证"
  ```

#### 步骤 2.2 🔍 Self-Check（自我检查）

- **执行者**：Dev（自己检查）
- **自动检查脚本**：`bash .claude/hooks/stage4-self-check.sh <MG_ID>`
- **检查项**：
  - [ ] Lint 检查通过（无 Error）
  - [ ] 单元测试通过
  - [ ] 手动功能验证通过
  - [ ] 无硬编码配置
  - [ ] 无 console.log/debugger 遗留
  - [ ] 符合 consistency-baseline 规范
  - [ ] **Hook 一致性检查通过**（`check-consistency.py`）
- **通过条件**：自动检查脚本返回 0，所有检查项通过
- **不通过处理**：返回 Dev 状态继续修复（无循环限制）
- **Hook 验证（Self-Check 完成门禁）**：
  ```bash
  # Self-Check 完成进入 Code Review 前，必须通过以下 Hook 检查
  bash $ROOT/.claude/hooks/check-state-machine.sh "$MG_ID" "CodeReview"
  bash $ROOT/.claude/hooks/check-tdd-rhythm.sh "$MG_ID"
  ```
  - **失败则阻断状态转换**，Dev 继续修复直到通过

**自动检查输出示例**：
```
[stage4-self-check] MG MG-001 开始 Self-Check...
[stage4-self-check] 检查了 5 个文件
[stage4-self-check] lint 检查通过
[stage4-self-check] Self-Check 通过
```

#### 步骤 2.3 🖥️ Code Review（代码检查）+ 循环修复

> **Code Review 循环修复机制**（关键）

**循环流程**：
```
Arch Agent 检查 → 发现问题 → 记录到 review-log.md → Dev-Fix 修复 → Arch Agent 重新检查
                         ↑                                                    │
                         └────────────── 循环 3 次未通过 → Human Gate ←─────────┘
```

**第 N 轮检查流程**：

1. **激活 Arch Agent** 执行 Code Review：
   ```
   Agent: agents/architect-stage4.md
   run_in_background: false
   ```

   ```bash
   bash .claude/hooks/log-event.sh "04" "Arch" "步骤开始" "CodeReview" "MG-001" ""
   ```

2. **检查问题**：
   - 读取 `.claude/iterations/sprint-latest/reviews/code-review-{MG-ID}.md`
   - 如有问题，记录到 `review-log.md`

3. **Human Gate 确认**：
   - 如有问题，等待用户确认是否进入 Dev-Fix
   - 回复选项：`继续`（进入 Dev-Fix）、`暂停`

4. **激活 Dev-Fix Agent**（如有问题）：
   ```
   Agent: agents/dev-fix-stage4.md
   run_in_background: false
   ```

   ```bash
   bash .claude/hooks/log-event.sh "04" "Dev-Fix" "Agent激活" "Dev-Fix开始修复" "MG-001" "进行中"
   ```

5. **Dev-Fix 修复后重新提交 Code Review**

6. **循环控制**：
   ```bash
   # 检查循环次数
   CYCLE_COUNT=$(cat "$ROOT/.claude/iterations/sprint-latest/reviews/.code-review-cycle-${MG_ID}" 2>/dev/null || echo "0")

   if [ $CYCLE_COUNT -ge 3 ]; then
     echo "[CodeReview] MG $MG_ID 循环次数已达 3 次上限，提交 Human Gate"
     bash .claude/hooks/log-event.sh "04" "Arch" "Human Gate" "CodeReview循环超限" "MG-001" "需人类决策"
     # 生成 human-gate-report.md
   fi
   ```

**通过条件**：Arch Agent 确认所有检查项通过

---

#### 步骤 2.4 🧪 QA-Test-Coding（QA 测试代码编写）+ 循环修复

> **QA-Test-Coding 循环修复机制**

**循环流程**：
```
QA Agent 编写测试 → 发现问题 → 记录到 review-log.md → QA-Fix 修复 → QA 重新编写
                         ↑                                                    │
                         └────────────── 循环 3 次未通过 → Human Gate ←─────────┘
```

1. **激活 QA Agent** 执行 QA-Test-Coding：
   ```
   Agent: agents/qa-stage4.md
   run_in_background: false
   ```

2. **检查问题**：如有问题，生成 `.claude/iterations/sprint-latest/reviews/test-code-review-{MG-ID}.md`

3. **Human Gate 确认**：等待用户确认是否进入 QA-Fix

4. **激活 QA-Fix Agent**（如有问题）：
   ```
   Agent: agents/qa-fix-stage4.md
   run_in_background: false
   ```

5. **QA-Fix 修复后重新提交 QA-Test-Coding**

6. **循环控制**：最多 3 次，超时提交 Human Gate

**产出物**：
- `tests/{US-ID}/*.test.js`（自动化测试代码）
- `tests/{US-ID}/manual-test/*.md`（人工测试模板）

---

#### 步骤 2.5 🔬 Test Code Review（测试代码检查）+ 循环修复

> **Test Code Review 循环修复机制**

**循环流程**：
```
Arch Agent 检查测试代码 → 发现问题 → 记录到 review-log.md → QA-Fix 修复 → Arch Agent 重新检查
                                   ↑                                                    │
                                   └────────────── 循环 3 次未通过 → Human Gate ←─────────┘
```

1. **激活 Arch Agent** 执行 Test Code Review：
   ```
   Agent: agents/architect-stage4.md
   run_in_background: false
   ```

2. **检查问题**：如有问题，更新 `.claude/iterations/sprint-latest/reviews/test-code-review-{MG-ID}.md`

3. **Human Gate 确认**：等待用户确认是否进入 QA-Fix

4. **激活 QA-Fix Agent**（如有问题）：
   ```
   Agent: agents/qa-fix-stage4.md
   run_in_background: false
   ```

5. **QA-Fix 修复后重新提交 Test Code Review**

6. **循环控制**：最多 3 次，超时提交 Human Gate

---

#### 步骤 2.6 ✅ Testing（人工测试）+ Bug 循环修复

> **Testing Bug 循环修复机制**

**循环流程**：
```
QA 执行测试 → 发现 Bug → 记录到 bugs.md → Dev-Fix 修复 → QA 重新测试
                       ↑                                              │
                       └────────── 循环 3 次未修复 → Technical Debt ←─┘
```

1. **激活 QA Agent** 执行 Testing：
   ```
   Agent: agents/qa-stage4.md
   run_in_background: false
   ```

2. **执行测试**：
   - 自动化测试：`npm run test`
   - 人工测试：按模板执行

3. **Bug 处理**：
   - 发现 Bug 记录到 `bugs.md`
   - 通知 Dev-Fix 修复
   - 修复后 QA 重新验证

4. **循环控制**：最多 3 次，超时记录为 Technical Debt

5. **Testing 完成**：
   - 所有测试通过后，更新 sprint-status.md 中 MG 状态为"🎉 Close"
   - 生成 Test Report

---

#### 步骤 2.7 🎉 Close（完成）

- **激活 Agent**：`agents/pm-stage4.md`
- **职责**：
  - 验收确认（所有测试通过）
  - 执行最终 commit
  - 更新 sprint-status.md 中 MG 状态为 Close
  - 生成 Test Report
- **验收条件**：
  - [ ] 所有测试用例通过（自动化 + 人工）
  - [ ] 所有 Bug 已修复或已记录为 Technical Debt
  - [ ] Arch Code Check 通过
  - [ ] Arch Test Check 通过
  - [ ] Test Report 已生成

### 步骤 3：阶段 4 完成汇总

- **激活 Agent**：`agents/pm-stage4.md`
- **职责**：
  - 汇总所有 MG 的开发测试结果
  - 更新 session-status.md 中阶段 4 状态为"✅"
  - 生成阶段 4 完成报告

---

## 4. Human Gate

### 4.1 Human Gate 触发条件

| 触发条件 | 说明 |
|----------|------|
| Code Review 循环 3 次未通过 | 连续 3 次检查发现问题未修复 |
| QA-Test-Coding 循环 3 次未通过 | 连续 3 次测试代码未通过检查 |
| Test Code Review 循环 3 次未通过 | 连续 3 次测试代码检查未通过 |
| Testing Bug 循环 3 次未通过 | 连续 3 次测试执行发现 Bug 未修复 |
| 发现 P0 缺陷 | 立即暂停，报告人类 |

### 4.2 Human Gate 检查清单

| 检查维度 | 检查内容 | 期望状态 | 不通过处理 |
|---------|---------|---------|-----------|
| **MG 完成状态** | 所有 MG 是否进入 Close | 全部 Close | 未完成 MG 列出 |
| **Bug 状态** | 是否所有 Bug 已修复或记录为 Technical Debt | 是 | 列出未关闭 Bug |
| **测试覆盖率** | 是否达到项目基线（默认 80%） | ≥ 80% | 报告覆盖率差距 |
| **review-log** | review-log.md 中是否有未关闭问题 | 无 | 列出问题清单 |

### 4.3 Human Gate 响应选项

- `继续` - 检查通过，允许进入阶段 5
- `打回` - 列出需要修正的问题，返回对应 Agent 修复
- `暂停` - 暂停阶段 4，等待进一步指示

---

## 5. 问题追踪

### 5.1 review-log.md 结构

所有检查发现的问题同步到 `.claude/iterations/sprint-latest/reviews/review-log.md`：

```markdown
## 2. 各阶段问题汇总

| 问题ID | 问题描述 | 问题类别 | 阶段 | Agent | 循环次数 | 归因分析 | 解决方案 | 未来预防建议 |
|--------|---------|---------|------|--------|----------|---------|----------|-------------|
| AC-001 | T-003 代码冗余未复用 | 代码质量 | 04 | Arch | 1/3 | 自检不充分 | 复用现有模块 | Dev 自检增加冗余检查 |
| ATC-001 | US-101 TC-004 未覆盖 | 测试覆盖 | 04 | Arch | 1/3 | QA 自检不充分 | 补充测试用例 | QA 自检增加覆盖率检查 |
```

### 5.2 问题状态流转

```
Open → In Progress → Fixed → Verified → Closed
                    ↑                            │
                    └────── Reopen (验证失败) ←┘
```

### 5.3 循环次数跟踪

| 阶段 | 循环限制 |
|------|----------|
| Code Review | 3次 |
| QA-Test-Coding | 3次 |
| Test Code Review | 3次 |
| Testing Bug | 3次 |

---

## 6. 产出物

| 产出物 | 路径 | 负责人 |
|--------|------|--------|
| 源代码 | 按项目结构 | Dev |
| task-summary/T{NNN}.md | `.claude/iterations/sprint-latest/task-summary/` | Dev |
| 自动化测试代码 | `tests/{US-ID}/*.test.js` | QA |
| 人工测试模板 | `tests/{US-ID}/manual-test/*.md` | QA |
| review-log.md | `.claude/iterations/sprint-latest/reviews/review-log.md` | 所有 Agent |
| bugs.md | `.claude/iterations/sprint-latest/bugs.md` | QA |
| Test Report | `.claude/iterations/sprint-latest/test-report.md` | PM |

---

## 7. 异常处理

| 异常场景 | 处理方式 |
|---------|---------|
| 前置文档缺失 | 报错退出 |
| Code Review 循环 3 次未通过 | 报告 Human Gate，记录到 review-log.md |
| QA-Test-Coding 循环 3 次未通过 | 报告 Human Gate，记录到 review-log.md |
| Test Code Review 循环 3 次未通过 | 报告 Human Gate，记录到 review-log.md |
| Testing 循环 3 次未通过 | 报告 Human Gate，记录到 review-log.md |
| 发现 P0 缺陷 | 立即暂停，报告 Human Gate |
| 进度滞后 > 70% | PM 评估调整后续任务 |

---

## 8. 关联文档

| 文档 | 路径 |
|------|------|
| Dev Agent（阶段4） | `agents/dev-stage4.md` |
| Dev-Fix Agent（阶段4） | `agents/dev-fix-stage4.md` |
| Arch Agent（阶段4） | `agents/architect-stage4.md` |
| QA Agent（阶段4） | `agents/qa-stage4.md` |
| QA-Fix Agent（阶段4） | `agents/qa-fix-stage4.md` |
| PM Agent（阶段4） | `agents/pm-stage4.md` |
| Sprint 状态 | `.claude/iterations/sprint-latest/sprint-status.md` |
| Session 状态 | `.claude/iterations/session-status.md` |
| 审查日志 | `.claude/iterations/sprint-latest/reviews/review-log.md` |
| ADR | `.claude/iterations/sprint-latest/ADR.md` |
| Test Plan | `.claude/iterations/sprint-latest/test-plan.md` |

### 模板文件

| 模板 | 路径 | 用途 |
|------|------|------|
| Code Review | `.claude/templates/code-review-template.md` | Code Review 产出 |
| Test Code Review | `.claude/templates/test-code-review-template.md` | Test Code Review 产出 |
| Bug Tracker | `.claude/templates/bugs-template.md` | Bug 追踪 |
| Human Gate Report | `.claude/templates/human-gate-report-template.md` | Human Gate 触发报告 |
| review-log-template | `.claude/templates/review-log-template.md` | 问题追踪日志 |

### Hooks 文件

| Hook | 路径 | 用途 |
|------|------|------|
| **install-hooks.sh** | `.claude/hooks/install-hooks.sh` | 一键安装所有 Git hooks |
| pre-commit hook | `.claude/hooks/pre-commit.sh` | Git 提交前自动检查 |
| pre-merge hook | `.claude/hooks/pre-merge-check.sh` | Git 合并前自动检查 |
| prepare-commit-msg hook | `.claude/hooks/prepare-commit-msg.sh` | 自动生成 commit message 前缀 |
| Self-Check hook | `.claude/hooks/stage4-self-check.sh` | Self-Check 阶段自动检查 |
| 增量检查 | `.claude/hooks/check-incremental.sh` | 检查已提交代码的增量问题 |
| 变更限制 | `.claude/hooks/enforce-diff-limit.sh` | 强制限制单次变更行数（默认300行） |
| 一致性检查 | `.claude/hooks/check-consistency.py` | 代码一致性检查 |
| Diff 大小检查 | `.claude/hooks/check-diff-size.py` | 文件大小超限检查（软限制200行） |
| **状态机检查** | `.claude/hooks/check-state-machine.sh` | 验证 7 状态流转合法性（P0） |
| **ADR 实现检查** | `.claude/hooks/check-adr-implementation.sh` | 验证 ADR 伪代码实现（P0） |
| **参考模块一致性** | `.claude/hooks/check-reference-consistency.sh` | 验证命名/结构合规（P1） |
| **TDD 节奏检查** | `.claude/hooks/check-tdd-rhythm.sh` | 验证红→绿→重构循环（P1） |
| **测试覆盖率检查** | `.claude/hooks/check-test-coverage.sh` | 验证关键模块测试覆盖（P2） |

**Hook 分层职责**：

| 层级 | Hook | 职责 | 失败处理 |
|------|------|------|---------|
| **Hook Layer** | check-state-machine | 防止非法状态跃迁 | 阻断状态转换 |
| | check-adr-implementation | 确保按 ADR 实现 | 警告，不阻断 |
| | check-reference-consistency | 参考模块合规 | 警告，不阻断 |
| | check-tdd-rhythm | TDD 循环完整 | 警告，不阻断 |
| | check-test-coverage | 测试覆盖达标 | 阻断 Close |
| **Guardian Layer** | Agent 推理审查 | 深度语义检查 | 循环修复（≤3次） |
| **Human Gate** | 人工审批 | 最终决策 | 暂停/打回 |

**安装所有 Git hooks（推荐）**：
```bash
# 一键安装所有 hooks
bash .claude/hooks/install-hooks.sh

# 验证安装
ls -la .git/hooks/ | grep -E "^-(l.*)"
```

**临时绕过 hook（不推荐）**：
```bash
git commit --no-verify  # 绕过 pre-commit 检查
git merge --no-verify   # 绕过 pre-merge 检查
```

---

## 9. 状态更新职责

> 阶段 4 需要更新以下文档，详见各 Agent 执行文件

| 文档 | 更新者 | 更新内容 |
|------|--------|---------|
| **session-status.md** | PM | 阶段完成记录（04）、产出物追踪表（04 实现 ✅）、自动推进状态、PM 阶段完成报告 |
| **project.md** | PM | 迭代历史章节中实现阶段文档状态从 ⏳ 更新为 ✅ |

**更新时机**：所有 MG 进入 Close 后，PM 执行阶段 4 完成汇总时

| PM 执行 Close 验收 | PM 执行阶段完成汇总 |
|-------------------|-------------------|
| 更新 MG 状态为 🎉 Close | 更新 session-status.md 阶段 4 为 ✅ |

---

## 10. 与阶段 2 的结构对比

| 结构要素 | 阶段 2 | 阶段 4（重构后） |
|---------|--------|-----------------|
| 概述 | ✅ 有 | ✅ 有 |
| 日志声明 | ✅ 有 | ✅ 有 |
| 前置条件检查 | ✅ 有 | ✅ 有 |
| 规则加载 | ✅ 有 | ✅ 有 |
| 执行流程 | Architect → PM-Audit 循环 → QA → PM-Audit-TP 循环 | Dev → Self-Check → Code Review 循环 → QA-Test-Coding 循环 → Test Code Review 循环 → Testing 循环 → Close |
| **循环修复机制** | ✅ PM-Audit → Architecture-Fix 循环 | ✅ Dev-Fix/QA-Fix 循环 |
| Human Gate | ✅ 有 | ✅ 有 |
| 产出物清单 | ✅ 有 | ✅ 有 |
| 状态更新职责 | ✅ 有 | ✅ 有 |
| 异常处理 | ✅ 有 | ✅ 有 |
| 关联文档 | ✅ 有 | ✅ 有 |
| **review-log 更新** | ✅ 有 | ✅ 有 |

---

*最后更新：2026-05-29（重构版）*