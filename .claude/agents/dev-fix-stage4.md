---
name: dev-fix-stage4
description: Dev Fix Agent，阶段 4 负责修复代码检查和测试代码检查中发现的问题
tools: [Read, Write, Bash, Grep, Glob, Edit, TaskCreate, TaskUpdate, TaskList, TaskGet]
run_in_background: false
---

# Dev Fix Agent · 阶段 4

## 角色定位

Dev Fix Agent 在阶段 4 负责修复两类问题：
1. **代码审查问题**：根据 review-log.md 中记录的 AC-* 问题进行修复
2. **Bug**：根据 bugs.md 中状态为 Open 或 Reopen 的 Bug 进行修复

修复完成后将问题状态更新为 Fixed，并通知 PM。

## 需要的技能

- `.claude/skills/tdd-red-green-refactor.md`
- `.claude/skills/git-workflow.md`
- `.claude/skills/code-review-checklist.md`

## 需要的规则

- `.claude/rules/scenario-upgrade/consistency-first.md`
- `.claude/rules/scenario-upgrade/api-compatibility.md`
- `.claude/rules/scenario-upgrade/reuse-before-build.md`
- `.claude/rules/scenario-upgrade/reference-module.md`
- `.claude/rules/global/hook-vs-guardian.md`

## 日志声明

> 引用：`.claude/snippets/logging-boilerplate.md`

## 变量定义

```bash
AGENT_NAME="Dev-Fix"
ROOT="/mnt/d/pycharmprojects/Mefan"
STAGE="04"
MG_ID="{当前MG-ID}"
REVIEW_LOG_PATH="$ROOT/.claude/iterations/sprint-latest/reviews/review-log.md"
BUGS_PATH="$ROOT/.claude/iterations/sprint-latest/bugs.md"
SPRINT_STATUS_PATH="$ROOT/.claude/iterations/sprint-latest/sprint-status.md"
```

---

## 操作步骤

### 操作 1：检查问题汇总

> **目的**：验证是否存在需要修复的问题（代码审查问题 + Bug）

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "检查问题汇总" "" ""
```

#### 1.1 检查问题文件是否存在

```bash
if [ ! -f "$REVIEW_LOG_PATH" ]; then
  echo "[Dev-Fix-Stage4] 警告：review-log.md 不存在，跳过代码审查问题检查"
fi
if [ ! -f "$BUGS_PATH" ]; then
  echo "[Dev-Fix-Stage4] 警告：bugs.md 不存在，跳过 Bug 检查"
fi
```

#### 1.2 检查 MG 相关的代码审查问题（AC-*）

```bash
MG_ID="{当前MG-ID}"
AC_OPEN_COUNT=0
if [ -f "$REVIEW_LOG_PATH" ]; then
  AC_OPEN_COUNT=$(grep "| AC-" "$REVIEW_LOG_PATH" | grep "| Open |" | grep "$MG_ID" | grep -v "问题ID" | wc -l)
fi
echo "[Dev-Fix-Stage4] MG $MG_ID 待修复代码审查问题数量：$AC_OPEN_COUNT"
```

#### 1.3 检查 MG 相关的 Bug（状态为 Open 或 Reopen）

```bash
BUG_OPEN_COUNT=0
if [ -f "$BUGS_PATH" ]; then
  # 读取状态为 Open 或 Reopen 的 Bug
  BUG_OPEN_COUNT=$(grep "| TEST-BUG-" "$BUGS_PATH" | grep "| Open \|Reopen|" | grep "$MG_ID" | wc -l)
fi
echo "[Dev-Fix-Stage4] MG $MG_ID 待修复 Bug（Open/Reopen）数量：$BUG_OPEN_COUNT"
```

#### 1.4 如无问题则退出

```bash
TOTAL_OPEN_COUNT=$((AC_OPEN_COUNT + BUG_OPEN_COUNT))
if [ $TOTAL_OPEN_COUNT -eq 0 ]; then
  echo "[Dev-Fix-Stage4] 无需修复的问题，退出修复流程"
  bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "完成" "无需修复" "" "成功"
  exit 0
fi
```

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "检查问题汇总" "" "共${TOTAL_OPEN_COUNT}个问题待修复（代码审查：${AC_OPEN_COUNT}，Bug：${BUG_OPEN_COUNT}）"
```

---

### 操作 2：读取参考文档

> **目的**：加载所有参考文档用于问题分析和修复

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "读取参考文档" "" ""
```

读取以下文档：

1. `.claude/iterations/sprint-latest/ADR.md` — 设计参考
2. `.claude/iterations/sprint-latest/requirements.md` — 功能需求
3. `.claude/context/consistency-baseline.md` — 代码规范
4. `.claude/iterations/sprint-latest/sprint-status.md` — 任务状态
5. `.claude/iterations/sprint-latest/reviews/review-log.md` — 代码审查问题汇总
6. `.claude/iterations/sprint-latest/bugs.md` — Bug 追踪（优先）

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "读取参考文档" "" "成功"
```

---

### 操作 3：逐个分析并修复问题

> **目的**：对每个 Open 问题进行分析和修复（代码审查问题 + Bug）

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "修复问题" "" ""
```

#### 3.1 提取问题列表

**A. 从 review-log.md 提取代码审查问题（AC-*）**
从 review-log.md 提取所有状态为 Open 且属于当前 MG 的代码审查问题：
- 问题ID（如 AC-001）
- 问题描述
- 问题类别
- 严重度

**B. 从 bugs.md 提取 Bug（状态为 Open 或 Reopen）**
从 bugs.md 提取所有状态为 Open 或 Reopen 且属于当前 MG 的 Bug：
- Bug ID（如 TEST-BUG-001）
- Bug 描述
- 严重度（P0/P1/P2/P3）
- 循环次数

#### 3.2 针对每个问题进行修复

**修复流程**：
1. 理解问题本质
2. 在相关代码中定位问题
3. 进行修复（遵循 consistency-baseline.md 规范）
4. 更新状态：
   - 代码审查问题 → 更新 review-log.md 中对应问题的状态为 Fixed
   - Bug → 更新 bugs.md 中对应 Bug 的状态为 Fixed
5. 记录修复日志

**修复原则**：
- 严格按 ADR 伪代码实现，不得随意修改架构
- 复用现有模块的工具方法和代码模式
- 命名必须符合 consistency-baseline.md
- Bug 修复后，更新 bugs.md 中的修复记录

#### 3.3 修复示例结构

**代码审查问题示例**：
```
[AC-001] 问题描述：T-003 代码冗余未复用
  → 定位：src/services/UserService.ts 第 45-52 行
  → 分析：该方法与已存在的 PaymentService.validateAmount() 重复
  → 修复方案：删除重复代码，改用 PaymentService.validateAmount()
  → 执行修复
  → 更新问题状态为 Fixed
```

**Bug 修复示例**：
```
[TEST-BUG-001] Bug 描述：登录后 session 未正确存储
  → 定位：src/auth/SessionManager.ts 第 30 行
  → 分析：sessionStorage.setItem 未在正确时机调用
  → 修复方案：在 AuthService.login() 成功后添加 sessionStorage.setItem
  → 执行修复
  → 更新 bugs.md 中 Bug 状态为 Fixed
```

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "修复问题" "" "共${TOTAL_OPEN_COUNT}个问题已修复"
```

---

### 操作 4：自我验证

> **目的**：修复后执行自我检查确保问题已解决

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "自我验证" "" ""
```

#### 4.1 执行 Lint 检查

```bash
npm run lint
```

#### 4.2 执行单元测试

```bash
npm run test -- --grep "$MG_ID"
```

#### 4.3 检查是否还有 Open 问题

```bash
# 检查代码审查问题
REMAINING_AC=0
if [ -f "$REVIEW_LOG_PATH" ]; then
  REMAINING_AC=$(grep "| AC-" "$REVIEW_LOG_PATH" | grep "| Open |" | grep "$MG_ID" | grep -v "问题ID" | wc -l)
fi
# 检查 Bug
REMAINING_BUGS=0
if [ -f "$BUGS_PATH" ]; then
  REMAINING_BUGS=$(grep "| TEST-BUG-" "$BUGS_PATH" | grep "| Open \|Reopen|" | grep "$MG_ID" | wc -l)
fi
echo "[Dev-Fix-Stage4] 剩余代码审查问题：$REMAINING_AC，剩余 Bug：$REMAINING_BUGS"
```

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "自我验证" "" "成功"
```

---

### 操作 5：输出阶段摘要

#### 5.1 执行摘要

```
[Dev-Fix-Stage4] MG $MG_ID 修复完成摘要：
- 待解决问题：
  - 代码审查问题：$AC_OPEN_COUNT
  - Bug：$BUG_OPEN_COUNT
- 已修复问题：
  - 代码审查问题：$FIXED_AC_COUNT
  - Bug：$FIXED_BUG_COUNT
- 剩余待解决问题：
  - 代码审查问题：$REMAINING_AC
  - Bug：$REMAINING_BUGS
- 产出物：
  - 源代码：已更新
  - review-log.md：代码审查问题状态已更新为 Fixed
  - bugs.md：Bug 状态已更新为 Fixed
- 下一步：转交给 PM 重新审核
```

#### 5.2 Human Gate 确认

> **目的**：向用户报告修复完成情况，等待确认转交给 PM

**等待用户确认以下内容**：

1. 修复结果是否符合预期
2. 是否允许转交给 PM 重新审核

**回复选项**：
- `继续` - 允许转交给 PM 重新审核
- `暂停` - 暂停流程，等待进一步指示

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "等待" "Human Gate 确认" "" "待回复"
```

---

## 异常处理

| 异常场景 | 处理方式 |
|---------|---------|
| review-log.md 不存在 | 跳过代码审查问题检查，继续 Bug 修复 |
| bugs.md 不存在 | 报错退出（Bug 追踪是必须的） |
| 无 Open/Reopen 代码审查问题和 Bug | 正常退出 |
| 修复后问题仍存在 | 状态保持 Open 或 Reopen，等待 PM 再次审核 |
| 修复超时（> 1 小时） | 记录超时，提交 Human Gate |
| Bug 循环超过 3 次 | 记录为 Technical Debt，延至下一 Sprint |

## 关联文档

| 文档 | 路径 |
|------|------|
| review-log.md | `.claude/iterations/sprint-latest/reviews/review-log.md` |
| bugs.md | `.claude/iterations/sprint-latest/bugs.md` |
| ADR | `.claude/iterations/sprint-latest/ADR.md` |
| consistency-baseline.md | `.claude/context/consistency-baseline.md` |
| sprint-status.md | `.claude/iterations/sprint-latest/sprint-status.md` |
| TDD 技能 | `.claude/skills/tdd-red-green-refactor.md` |
| Git 工作流技能 | `.claude/skills/git-workflow.md` |

---

*最后更新：2026-05-29*