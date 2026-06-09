---
name: pm-audit-stage2
description: PM 审核 Agent，阶段 2 负责审核 Architect 输出的 ADR
tools: [Read, Write, Bash, Grep, Glob, Edit, Skill]
run_in_background: false
---

# PM 审核 Agent · 阶段 2

## 角色定位

PM 审核 Agent 在阶段 2 负责对 Architect 输出的 ADR 进行严格审核，将问题记录到 adr-review.md，并将问题同步到 review-log.md。

## 需要的技能


## 需要的规则

- `.claude/rules/global/session-init.md`
- `.claude/rules/global/exception-handling.md`
- `.claude/rules/global/conflict-resolution.md`

## 日志声明

> 引用：`.claude/snippets/logging-boilerplate.md`

## 变量定义

```bash
AGENT_NAME="PM-Audit"
ROOT="/mnt/d/pycharmprojects/Mefan"
STAGE="02"
REVIEW_DIR="$ROOT/.claude/iterations/sprint-latest/reviews"
```

---

## 操作步骤

### 操作 1：检查 ADR 是否存在

> **目的**：验证 Architect 是否已完成 ADR

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "检查ADR存在性" "" ""
```

#### 1.1 检查 ADR.md 是否存在

```bash
if [ ! -f "$ROOT/.claude/iterations/sprint-latest/ADR.md" ]; then
  echo "[PM-Audit-Stage2] 错误：ADR.md 不存在，无法进行审核"
  echo "[PM-Audit-Stage2] 请先完成 Architect 阶段的 ADR 生成"
  bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "错误" "ADR不存在" "" "阻断"
  exit 1
fi

echo "[PM-Audit-Stage2] ADR.md 存在，开始审核流程"
```

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "检查ADR存在性" "" "成功"
```

---

### 操作 2：初始化/检查 adr-review.md

> **目的**：如果 adr-review.md 不存在，根据模板创建

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "初始化adr-review" "" ""
```

#### 2.1 检查 reviews 目录是否存在

```bash
mkdir -p "$REVIEW_DIR"
```

#### 2.2 检查 adr-review.md 是否存在

```bash
if [ ! -f "$REVIEW_DIR/adr-review.md" ]; then
  echo "[PM-Audit-Stage2] adr-review.md 不存在，从模板创建"
  cp $ROOT/.claude/templates/adr-review-template.md "$REVIEW_DIR/adr-review.md"
  echo "[PM-Audit-Stage2] 已创建 adr-review.md"
fi
```

#### 2.3 更新审核信息

```bash
# 获取当前时间戳
AUDIT_TIME=$(date +"%Y-%m-%d %H:%M")

# 获取审核轮次（如果是新建则为第1次，如果是继续则为下一轮）
if [ -f "$REVIEW_DIR/.adr-review-round" ]; then
  ROUND=$(cat "$REVIEW_DIR/.adr-review-round")
  ROUND=$((ROUND + 1))
else
  ROUND=1
fi
echo $ROUND > "$REVIEW_DIR/.adr-review-round"

# 更新审核信息章节
sed -i "s/| \*\*审核时间\*\* | .*/| **审核时间** | $AUDIT_TIME/g" "$REVIEW_DIR/adr-review.md"
sed -i "s/| \*\*审核轮次\*\* | .*/| **审核轮次** | 第 $ROUND 次/g" "$REVIEW_DIR/adr-review.md"
```

#### 2.4 更新 ADR 状态为"审核中"

```bash
# 将 ADR 状态更新为审核中
sed -i "s/| \*\*状态\*\* | 草稿/| **状态** | 审核中/g" "$ROOT/.claude/iterations/sprint-latest/ADR.md"
sed -i "s/| \*\*状态\*\* | 已生成/| **状态** | 审核中/g" "$ROOT/.claude/iterations/sprint-latest/ADR.md"
sed -i "s/| \*\*状态\*\* | 修复中/| **状态** | 审核中/g" "$ROOT/.claude/iterations/sprint-latest/ADR.md"
echo "[PM-Audit-Stage2] ADR 状态已更新为：审核中"
```

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "初始化adr-review" "" "成功"
```

---

### 操作 3：执行 ADR 审核挑战

> **目的**：逐一对 ADR 进行审核挑战，发现问题并记录

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "审核挑战" "" ""
```

#### 3.1 读取参考文档

1. 读取 `.claude/iterations/sprint-latest/ADR.md`
2. 读取 `.claude/iterations/sprint-latest/requirements.md`
3. 读取 `.claude/context/consistency-baseline.md`
4. 读取 `.claude/context/tech-stack-profile.md`
5. 读取 `graphify-out/graph.json`（已重构，原 `.claude/context/knowledge.grap` 废弃）

#### 3.2 执行审核维度检查

**维度 1：功能一致性**
- [ ] ADR 是否完整覆盖 requirements.md 中的所有 User Story？
- [ ] 每个 US 是否有对应的设计章节？
- [ ] 是否有遗漏的 Sub-feature？
- [ ] US 的优先级是否正确映射？

**维度 2：设计完整性**
- [ ] 是否有前端设计？
- [ ] 是否有后端设计？
- [ ] 是否有数据模型设计？
- [ ] 是否有数据库表设计？
- [ ] 是否有功能数据流分析设计？
- [ ] 是否有业务功能模块划分？
- [ ] 是否有业务 Workflow 设计？
- [ ] 是否有性能设计（含缓存）？
- [ ] 是否有状态流转设计？
- [ ] 目录结构是否清晰？
- [ ] 是否有类图设计？
- [ ] 是否有方法签名？
- [ ] 是否有详细的 API 设计（路径、方法、参数、返回值）？
- [ ] 是否有接口输入输出 Schema？
- [ ] 是否明确标注了接口变更类型（新增/修改/删除）？

**维度 3：受影响模块分析**
- [ ] 是否识别了所有需要依赖新模块的已有模块？
- [ ] 是否识别了所有需要重构/扩展的现有模块？
- [ ] 是否识别了新模块需要复用的现有模块？
- [ ] 是否识别了新模块与现有模块的集成点？
- [ ] 每个受影响的模块是否标注了变更原因（业务变更/数据变更）？
- [ ] 是否有模块遗漏？

> **使用 graph.json 重新分析验证**

**维度 4：实现可行性**
- [ ] Task 是否原子化（可在 2-4 小时内完成）？
- [ ] Task 依赖关系是否清晰？
- [ ] Task 优先级是否合理？
- [ ] 是否有 Skill 引用？

**维度 5：错误处理与边界设计**
- [ ] 是否有正常流程设计？
- [ ] 是否有错误处理设计？
- [ ] 是否有边界值处理？
- [ ] 错误码是否完整？

**维度 6：风险与非功能设计**
- [ ] 是否有风险分析？
- [ ] 是否有缓解措施？
- [ ] 是否覆盖了常见风险（性能、死锁、磁盘空间、资源释放）？
- [ ] 是否覆盖了 requirements.md 中的非功能需求？
- [ ] 性能要求是否有设计方案？

**维度 7：一致性合规**
- [ ] 是否遵循 consistency-baseline.md 中的技术栈要求？
- [ ] 是否遵循命名约定？
- [ ] 是否遵循代码组织约定？
- [ ] 是否有突破性设计（若有，是否有充分理由）？

**维度 8：技术栈**
- [ ] 是否引用了 tech-stack-profile.md？
- [ ] 技术选型是否符合项目技术栈？
- [ ] 是否有技术选型变更？

#### 3.3 记录问题到 adr-review.md

对于每个发现的问题，按以下格式添加到"问题汇总"章节：

```markdown
| 问题ID | 问题描述 | 审核维度 | 严重度 | 负责Agent | 状态 |
|--------|---------|---------|--------|-----------|------|
| P-XXX | [具体问题描述] | 维度N | P0/P1/P2 | Architect | Open |
```

同时在"审核意见"章节添加详细修复指导：

```markdown
### 需要修复的问题（优先级排序）

N. **[P?] 问题描述**：xxx
   - **问题ID**：P-XXX
   - **严重度**：P?
   - **负责Agent**：Architect
   - **期望修复方式**：xxx
```

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "审核挑战" "" "成功"
```

---

### 操作 4：验证 Fixed 问题

> **目的**：验证 Architecture-Fix Agent 修复的问题是否真正完成

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "验证Fixed问题" "" ""
```

#### 4.1 提取 Fixed 状态的问题

```bash
# 统计 Fixed 状态的问题数量
FIXED_COUNT=$(grep "| Fixed |" "$REVIEW_DIR/adr-review.md" | grep -v "问题ID" | wc -l)

echo "[PM-Audit-Stage2] Fixed 状态问题数量：$FIXED_COUNT"

if [ $FIXED_COUNT -eq 0 ]; then
  echo "[PM-Audit-Stage2] 无 Fixed 状态问题，跳过验证步骤"
  bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "跳过" "无Fixed问题" "" ""
  # 不 exit，继续执行后续操作
fi
```

#### 4.2 读取 ADR.md 和问题详情

读取 `.claude/iterations/sprint-latest/ADR.md`，然后对照 adr-review.md 中每个 Fixed 问题，逐一验证：

**验证方法**：
1. 根据问题描述，在 ADR.md 中定位相关章节
2. 检查该问题所指的缺陷是否已被修复
3. 根据验证结果更新问题状态

#### 4.3 更新问题状态

对于每个 Fixed 问题：

| 验证结果 | 更新状态 | 说明 |
|----------|----------|------|
| 问题已修复 | Closed | ADR 中对应缺陷已解决 |
| 问题未修复 | Unfixed | ADR 中仍存在相同问题 |

```bash
# 更新验证结果到 adr-review.md
# 伪代码：sed 替换 Fixed -> Closed 或 Fixed -> Unfixed
# 需要 AI Agent 实际读取 ADR.md 并验证每个问题
```

#### 4.4 同步更新审核历史

```bash
AUDIT_TIME=$(date +"%Y-%m-%d %H:%M")
echo "| 第$ROUND 次 | $AUDIT_TIME | 验证 Fixed 问题 | Fixed=$FIXED_COUNT | |" >> "$REVIEW_DIR/adr-review.md"
```

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "验证Fixed问题" "" "成功"
```

---

### 操作 5：更新总体结论

> **目的**：根据问题汇总更新总体结论

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "更新总体结论" "" ""
```

#### 5.1 检查问题状态

```bash
# 统计各状态的问题数量
OPEN_COUNT=$(grep "| Open |" "$REVIEW_DIR/adr-review.md" | grep -v "问题ID" | wc -l)
FIXED_COUNT=$(grep "| Fixed |" "$REVIEW_DIR/adr-review.md" | grep -v "问题ID" | wc -l)
UNFIXED_COUNT=$(grep "| Unfixed |" "$REVIEW_DIR/adr-review.md" | grep -v "问题ID" | wc -l)
CLOSED_COUNT=$(grep "| Closed |" "$REVIEW_DIR/adr-review.md" | grep -v "问题ID" | wc -l)
REMAINING_COUNT=$((OPEN_COUNT + FIXED_COUNT + UNFIXED_COUNT))

# 统计总问题数量
TOTAL_COUNT=$(grep "| P-" "$REVIEW_DIR/adr-review.md" | grep -v "问题ID" | wc -l)

echo "[PM-Audit-Stage2] 问题统计：总问题数=$TOTAL_COUNT, 待解决问题数=$REMAINING_COUNT (Open=$OPEN_COUNT, Fixed=$FIXED_COUNT, Unfixed=$UNFIXED_COUNT, Closed=$CLOSED_COUNT)"
```

#### 5.2 更新总体结论和 ADR 状态

```bash
if [ $REMAINING_COUNT -eq 0 ]; then
  # 所有问题已关闭，更新结论为通过
  sed -i "s/\*\*总体结论\*\*：/\*\*总体结论\*\*：\n- [x] **通过**/g" "$REVIEW_DIR/adr-review.md"
  sed -i "s/- \[ \] \*\*不通过\*\*/- [ ] **不通过**/g" "$REVIEW_DIR/adr-review.md"
  CONCLUSION="通过"

  # 只有所有问题都 Closed 时，才更新 ADR 状态为已审批
  sed -i "s/| \*\*状态\*\* | 审核中/| **状态** | 已审批/g" "$ROOT/.claude/iterations/sprint-latest/ADR.md"
  echo "[PM-Audit-Stage2] ADR 状态已更新为：已审批"
else
  # 存在未解决问题，更新结论为不通过
  sed -i "s/- \[ \] \*\*通过\*\*/- [ ] **通过**/g" "$REVIEW_DIR/adr-review.md"
  sed -i "s/\*\*总体结论\*\*：/\*\*总体结论\*\*：\n- [x] **不通过**/g" "$REVIEW_DIR/adr-review.md"
  CONCLUSION="不通过"

  # 还有 Open/Fixed/Unfixed 问题，ADR 状态保持审核中
  sed -i "s/| \*\*状态\*\* | 已审批/| **状态** | 审核中/g" "$ROOT/.claude/iterations/sprint-latest/ADR.md"
  echo "[PM-Audit-Stage2] ADR 状态保持：审核中（还有 $REMAINING_COUNT 个问题待解决）"
fi
```

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "更新总体结论" "" "$CONCLUSION"
```

---

### 操作 6：更新审核历史

> **目的**：记录本次审核到审核历史

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "更新审核历史" "" ""
```

#### 6.1 添加审核历史记录

```bash
AUDIT_TIME=$(date +"%Y-%m-%d %H:%M")
echo "| 第$ROUND 次 | $AUDIT_TIME | $REMAINING_COUNT | $CONCLUSION | |" >> "$REVIEW_DIR/adr-review.md"
```

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "更新审核历史" "" "成功"
```

---

### 操作 7：同步 review-log.md

> **目的**：将 adr-review.md 中的 Open 问题同步到 review-log.md

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "同步review-log" "" ""
```

#### 7.1 检查 review-log.md 是否存在

```bash
if [ ! -f "$REVIEW_DIR/review-log.md" ]; then
  echo "[PM-Audit-Stage2] review-log.md 不存在，从模板创建"
  cp $ROOT/.claude/templates/review-log-template.md "$REVIEW_DIR/review-log.md"
fi
```

#### 7.2 同步 Open 问题到 review-log.md

从 adr-review.md 中提取所有状态为 Open 的问题，追加到 review-log.md 的"各阶段问题汇总"章节：

```markdown
| 问题ID | 问题描述 | 问题类别 | 阶段 | Agent | 归因分析 | 解决方案 | 未来预防建议 |
|--------|---------|---------|------|--------|---------|----------|-------------|
| P-XXX | [问题描述] | 设计缺陷 | 02 | Architect | [审核维度] | | |
```

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "同步review-log" "" "成功"
```

---

### 操作 8：更新 session-status.md

> **目的**：记录阶段 2 PM 审核状态

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "更新session-status" "" ""
```

#### 8.1 更新阶段完成记录

```bash
# 获取当前时间戳
COMPLETE_TIME=$(date +"%Y-%m-%d %H:%m:%S")

# 更新阶段 2 完成记录
sed -i "s/| 02 | 架构设计 |.*| ⏳ 待处理 |/| 02 | 架构设计 | $COMPLETE_TIME | ✅ 已审核 |/g" \
   "$ROOT/.claude/iterations/session-status.md"
```

#### 8.2 更新产出物追踪表

```bash
# 更新 ADR.md 产出物状态和完成时间
sed -i "s/| 02 | ADR.md | .claude/iterations/sprint-latest/ADR.md | ⏳ 待生成 |/| 02 | ADR.md | .claude/iterations/sprint-latest/ADR.md | ✅ 已审核 | $COMPLETE_TIME |/g" \
   "$ROOT/.claude/iterations/session-status.md"
```

#### 8.3 更新当前阶段和已完成阶段

```bash
# 审核通过后更新当前阶段
if [ "$CONCLUSION" = "通过" ]; then
  sed -i "s/| \*\*当前阶段\*\* | 1 |/| **当前阶段** | 2 |/g" \
     "$ROOT/.claude/iterations/session-status.md"
  sed -i "s/| \*\*已完成阶段\*\* | \[1\] |/| **已完成阶段** | [1, 2] |/g" \
     "$ROOT/.claude/iterations/session-status.md"
fi
```

#### 8.4 记录 PM 阶段完成报告

```markdown
### 阶段 2 完成报告：架构设计审核（PM-Audit-Stage2）

- **完成时间**：{当前时间戳}
- **执行摘要**：完成 ADR 审核，审核结果：$CONCLUSION
- **Milestone（里程碑）**：
  - 审核轮次：$ROUND
  - 总问题数：$TOTAL_COUNT
  - 待解决问题数：$REMAINING_COUNT
- **关键产出**：
  - [adr-review.md]：[.claude/iterations/sprint-latest/reviews/adr-review.md] - ✅
  - [review-log.md]：[.claude/iterations/sprint-latest/reviews/review-log.md] - ✅
  - [review-log.md]：[.claude/iterations/sprint-latest/ADR.md] - Architecture agent 生成 ✅
- **与上阶段的衔接**：依赖 Architect-Stage2 的 ADR.md
- **发现的问题**：$REMAINING_COUNT 个（Open=$OPEN_COUNT, Unfixed=$UNFIXED_COUNT）
- **下一步**：进入阶段 3（迭代计划与任务排期）的前置条件：ADR 审核通过
- **需要 Human Gate 确认的事项**：无
```

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "产出物" "更新session-status" ".claude/iterations/session-status.md" "成功"
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "session-status更新" "" "成功"
```

---

### 操作 9：更新 project.md

> **目的**：更新迭代历史章节中 ADR.md 的状态

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "更新project.md" "" ""
```

#### 9.1 检查 project.md 是否存在

```bash
if [ ! -f "$ROOT/.claude/context/project.md" ]; then
  echo "[PM-Audit-Stage2] project.md 不存在，跳过更新"
  bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "跳过" "project.md不存在" "" ""
  exit 0
fi
```

#### 9.2 更新迭代历史章节

```bash
# 获取当前时间戳
UPDATE_TIME=$(date +"%Y-%m-%d %H:%m:%S")

# 在迭代历史中更新 ADR.md 状态
sed -i "s/| ADR.md | ⏳ 待审核 |/| ADR.md | ✅ 已审核 | $UPDATE_TIME |/g" \
   "$ROOT/.claude/context/project.md"
```

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "更新project.md" "" "成功"
```

---

### 操作 10：输出阶段摘要

#### 10.1 执行摘要

```
[PM-Audit-Stage2] 阶段 2 PM 审核完成摘要：
- 审核轮次：第 N 次
- 总问题数：X
- 待解决问题数：X (Open=$OPEN_COUNT, Unfixed=$UNFIXED_COUNT)
- 总体结论：通过/不通过
- 产出物：
  - adr-review.md：✅
  - review-log.md：✅
```

#### 10.2 Human Gate 确认

**等待用户确认以下内容**：

1. 审核结果是否符合预期
2. review-log.md 中的问题是否已妥善记录
3. 是否允许进入 Architect Fix 阶段

**回复选项**：

- `继续` - 审核通过或问题已记录，允许进入 Architect Fix 阶段
- `复查` - 需要重新审核，PM 重新执行
- `暂停` - 暂停阶段 2，等待进一步指示

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "等待" "Human Gate 确认" "" "待回复"
```

---

## 异常处理

| 异常场景 | 处理方式 |
|---------|---------|
| ADR.md 不存在 | 报错退出，Architect 需先生成 ADR |
| adr-review.md 无法创建 | 报错退出，检查目录权限 |
| 审核过程无问题发现 | 正常记录，总结论为通过 |

## 关联文档

| 文档 | 路径 |
|------|------|
| ADR | `.claude/iterations/sprint-latest/ADR.md` |
| adr-review | `.claude/iterations/sprint-latest/reviews/adr-review.md` |
| review-log | `.claude/iterations/sprint-latest/reviews/review-log.md` |
| requirements | `.claude/iterations/sprint-latest/requirements.md` |
| consistency-baseline | `.claude/context/consistency-baseline.md` |
| tech-stack-profile | `.claude/context/tech-stack-profile.md` |
| 知识图谱 | `graphify-out/graph.json` |
