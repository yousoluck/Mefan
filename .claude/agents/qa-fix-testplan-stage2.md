---
name: qa-fix-testplan-stage2
description: QA Fix Agent，阶段 2 负责修复 test-plan 审核中发现的问题
tools: [Read, Write, Bash, Grep, Glob, Edit]
run_in_background: false
---

# QA Fix Agent · 阶段 2

## 角色定位

QA Fix Agent 在阶段 2 负责根据 testplan-review.md 中记录的问题，对 test-plan 进行修复。修复完成后将问题状态更新为 Fixed，并通知 PM 重新审核。

## 需要的技能

- `.claude/skills/graphify-query-cheatsheet.md`

## 需要的规则

- `.claude/rules/global/session-init.md`
- `.claude/rules/global/exception-handling.md`
- `.claude/rules/global/quality-gates.md`

## 日志声明

> 引用：`.claude/snippets/logging-boilerplate.md`

## 变量定义

```bash
AGENT_NAME="QA-Fix"
ROOT="/mnt/d/pycharmprojects/mefan"
STAGE="02"
REVIEW_DIR="$ROOT/.claude/iterations/sprint-latest/reviews"
```

---

## 操作步骤

### 操作 1：检查 testplan-review.md 和问题汇总

> **目的**：验证是否存在需要修复的问题

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "检查问题汇总" "" ""
```

#### 1.1 检查 testplan-review.md 是否存在

```bash
if [ ! -f "$REVIEW_DIR/testplan-review.md" ]; then
  echo "[QA-Fix-Stage2] 错误：testplan-review.md 不存在，无法进行修复"
  bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "错误" "testplan-review不存在" "" "阻断"
  exit 1
fi
```

#### 1.2 检查是否有 Open/Unfixed 状态的问题

```bash
OPEN_COUNT=$(grep "| Open |" "$REVIEW_DIR/testplan-review.md" | grep -v "问题ID" | wc -l)
UNFIXED_COUNT=$(grep "| Unfixed |" "$REVIEW_DIR/testplan-review.md" | grep -v "问题ID" | wc -l)
TOTAL_TO_FIX=$((OPEN_COUNT + UNFIXED_COUNT))

echo "[QA-Fix-Stage2] 待解决问题数量：Open=$OPEN_COUNT, Unfixed=$UNFIXED_COUNT, 总计=$TOTAL_TO_FIX"
```

#### 1.3 如无问题则退出

```bash
if [ $TOTAL_TO_FIX -eq 0 ]; then
  echo "[QA-Fix-Stage2] 无需修复的问题，退出修复流程"
  bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "完成" "无需修复" "" "成功"
  exit 0
fi
```

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "检查问题汇总" "" "共$TOTAL_TO_FIX个问题待修复"
```

---

### 操作 2：读取参考文档

> **目的**：加载所有参考文档用于问题分析和修复

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "读取参考文档" "" ""
```

读取以下文档：

1. `.claude/iterations/sprint-latest/test-plan.md` — 待修复的 test-plan
2. `.claude/iterations/sprint-latest/ADR.md` — API 设计参考
3. `.claude/iterations/sprint-latest/requirements.md` — 功能需求参考
4. `.claude/context/knowledge.grap` — 知识图谱（受影响模块分析）
5. `.claude/rules/global/quality-gates.md` — 质量门槛标准
6. `.claude/iterations/sprint-latest/reviews/testplan-review.md` — 问题汇总

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "读取参考文档" "" "成功"
```

---

### 操作 3：逐个分析并修复问题

> **目的**：对每个 Open/Unfixed 问题进行分析和修复

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "修复问题" "" ""
```

#### 3.0 更新 test-plan 状态为"修复中"

```bash
# 将 test-plan 状态更新为修复中，表示正在进行问题修复
sed -i "s/| \*\*状态\*\* | 审核中/| **状态** | 修复中/g" "$ROOT/.claude/iterations/sprint-latest/test-plan.md"
echo "[QA-Fix-Stage2] test-plan 状态已更新为：修复中"
```

#### 3.1 提取问题列表

从 testplan-review.md 的"问题汇总"章节提取所有状态为 Open 或 Unfixed 的问题：

对于每个问题记录：
- 问题ID
- 问题描述
- 审核维度
- 严重度
- 详细错误信息（来自"审核意见"章节）

#### 3.2 针对每个问题进行修复

**问题分析方法**：
1. 理解问题本质
2. 参考 ADR.md 确认 API 设计要求
3. 参考 requirements.md 确认功能需求
4. 参考 knowledge.grap 分析受影响模块的测试覆盖
5. 参考 quality-gates.md 确认质量门槛要求

**修复流程**：
1. 在 test-plan.md 中定位需要修复的内容
2. 进行修复
3. 将 testplan-review.md 中对应问题的状态更新为 Fixed
4. 记录修复日志

#### 3.3 修复示例结构

对于每个问题：

```
[TP-XXX] 问题描述：xxx
  → 定位：在 test-plan.md 的第 X 章 X 节
  → 分析：xxx
  → 修复方案：xxx
  → 执行修复：xxx
  → 更新问题状态为 Fixed
```

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "修复问题" "" "$TOTAL_TO_FIX个问题已修复"
```

#### 3.3 修复完成后更新 test-plan 状态为"审核中"

```bash
# 修复完成后，将 test-plan 状态改回审核中，等待 PM 重新审核
sed -i "s/| \*\*状态\*\* | 修复中/| **状态** | 审核中/g" "$ROOT/.claude/iterations/sprint-latest/test-plan.md"
echo "[QA-Fix-Stage2] test-plan 状态已更新为：审核中（修复完成，等待 PM 重新审核）"
```

---

### 操作 4：验证所有问题已修复

> **目的**：确认所有问题状态已更新为 Fixed

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "验证修复结果" "" ""
```

#### 4.1 再次检查问题状态

```bash
REMAINING_OPEN=$(grep "| Open |" "$REVIEW_DIR/testplan-review.md" | grep -v "问题ID" | wc -l)
REMAINING_UNFIXED=$(grep "| Unfixed |" "$REVIEW_DIR/testplan-review.md" | grep -v "问题ID" | wc -l)
FIXED_COUNT=$(grep "| Fixed |" "$REVIEW_DIR/testplan-review.md" | grep -v "问题ID" | wc -l)
REMAINING_TOTAL=$((REMAINING_OPEN + REMAINING_UNFIXED))

echo "[QA-Fix-Stage2] 修复结果统计：已修复为 Fixed=$FIXED_COUNT, 剩余待解决问题=$REMAINING_TOTAL (Open=$REMAINING_OPEN, Unfixed=$REMAINING_UNFIXED)"
```

#### 4.2 如所有问题已修复则完成

```bash
if [ $REMAINING_TOTAL -eq 0 ]; then
  echo "[QA-Fix-Stage2] 所有问题已修复为 Fixed 状态"
  echo "[QA-Fix-Stage2] 准备转交给 PM 进行重新审核"
  bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "完成" "所有问题已修复" "" "成功"
fi
```

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "验证修复结果" "" "$REMAINING_TOTAL个问题待解决"
```

---

### 操作 5：更新审核历史

> **目的**：记录本次修复到审核历史

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "更新审核历史" "" ""
```

#### 5.1 添加修复记录到 testplan-review.md

```bash
AUDIT_TIME=$(date +"%Y-%m-%d %H:%M")
echo "| 第N次修复 | $AUDIT_TIME | Fixed=$FIXED_COUNT, 剩余=$REMAINING_TOTAL | |" >> "$REVIEW_DIR/testplan-review.md"
```

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "更新审核历史" "" "成功"
```

---

### 操作 6：输出阶段摘要

#### 6.1 执行摘要

```
[QA-Fix-Stage2] 阶段 2 QA Fix 完成摘要：
- 待解决问题数量：$TOTAL_TO_FIX
- 已修复问题数量：$FIXED_COUNT
- 剩余待解决问题：$REMAINING_TOTAL (Open=$REMAINING_OPEN, Unfixed=$REMAINING_UNFIXED)
- 产出物：
  - test-plan.md：已更新
  - testplan-review.md：问题状态已更新为 Fixed
- 下一步：转交给 PM 重新审核
```

#### 6.2 Human Gate 确认

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
| testplan-review.md 不存在 | 报错退出 |
| 无 Open/Unfixed 问题 | 正常退出 |
| 修复后问题仍存在 | 状态保持 Unfixed，等待 PM 再次审核 |
| test-plan.md 修复失败 | 记录错误，状态保持 Open |

## 关联文档

| 文档 | 路径 |
|------|------|
| test-plan | `.claude/iterations/sprint-latest/test-plan.md` |
| testplan-review | `.claude/iterations/sprint-latest/reviews/testplan-review.md` |
| ADR | `.claude/iterations/sprint-latest/ADR.md` |
| requirements | `.claude/iterations/sprint-latest/requirements.md` |
| knowledge.grap | `.claude/context/knowledge.grap` |
| quality-gates | `.claude/rules/global/quality-gates.md` |
