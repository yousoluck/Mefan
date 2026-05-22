# /mf-upgrade:03-plan – 迭代计划与任务排期

> **当前阶段**：阶段 3（迭代计划与任务排期）
> **前置条件**：阶段 2 已完成，ADR 和测试计划已产出

---

## 0. 日志声明

执行本阶段所有步骤时，必须使用 `.claude/hooks/log-event.sh` 记录日志：
- 进入阶段：`bash .claude/hooks/log-event.sh "03" "$AGENT_NAME" "阶段进入" "阶段3开始" "" "成功"`
- 结束阶段：`bash .claude/hooks/log-event.sh "03" "$AGENT_NAME" "阶段退出" "阶段3完成" "" "成功"`
- 产出文件：`bash .claude/hooks/log-event.sh "03" "$AGENT_NAME" "产出物" "生成 <文件>" "<文件>" "成功"`

---

## 1. 规则加载（按需引用）

| 规则/技能 | 用途 | 引用时机 |
|-----------|------|---------|
| `.claude/rules/global/session-init.md` | 阶段初始化三原则 | 步骤 2 开始前 |
| `.claude/rules/global/iteration-planning.md` | 任务拆解标准、WIP限制、警戒线设置 | pm-stage3 内部 |
| `.claude/rules/global/conflict-resolution.md` | 冲突裁决与串并行决策 | pm-stage3 内部 |
| `.claude/rules/scenario-upgrade/reuse-before-build.md` | 检查是否有任务可复用现有代码 | pm-stage3 内部 |

---

## 2. 前置检查

**执行者**：框架自动检查

### 2.1 检查阶段 2 产出物

1. 读取 `.claude/iterations/session-status.md`
2. 确认阶段 2 已完成（状态为 ✅）
3. 若不存在或阶段 2 未完成，报错退出：
   ```
   [自动检查] 阶段 2 未完成或 session-status.md 缺失，请先执行 /mf-upgrade:02-arch-qa
   ```

### 2.2 自动检查上一 Agent 产出物

#### 步骤 1 → 完成 自动检查

**触发时机**：在完成步骤 1 进入 Human Gate 前

1. 检查 `.claude/iterations/sprint-latest/iteration-plan.md` 是否存在
2. 检查 `.claude/iterations/sprint-latest/sprint-status.md` 是否存在
3. 若任一不存在，报错：
   ```
   [自动检查] pm-stage3 产出物不存在：iteration-plan.md 或 sprint-status.md 未找到
   错误：前置 Agent 未完成工作，请先执行 pm-stage3
   ```
4. 若存在，继续进入 Human Gate

---

## 3. 工作流编排

### 步骤 1：PM 主导迭代计划与任务排期

- **前置检查**：自动检查阶段 2 产出物
- **激活 Agent**：`agents/pm-stage3.md`
- **职责**：PM 执行完整的迭代计划工作（任务拆解、冲突裁决、生成迭代计划、初始化看板、自检与反向校验）
- **引用规则**：`.claude/rules/global/iteration-planning.md`、`.claude/rules/global/conflict-resolution.md`、`.claude/rules/scenario-upgrade/reuse-before-build.md`
- **产出物**：
  - `.claude/iterations/sprint-latest/iteration-plan.md`
  - `.claude/iterations/sprint-latest/sprint-status.md`
- **完成后**：更新 session-status.md 中阶段 3 完成状态为"✅"

---

## 4. Human Gate

**审查结果**：
- **全部通过**：提交 `[Human Gate]` 等待人类确认
- **任一未通过**：打回给 PM 修正，修正后重新提交审查

---

## 5. 产出物

| 产出物 | 路径 |
|--------|------|
| 迭代计划 | `.claude/iterations/sprint-latest/iteration-plan.md` |
| 看板 | `.claude/iterations/sprint-latest/sprint-status.md` |

---

## 6. 异常处理

| 异常场景 | 处理方式 |
|---------|---------|
| 前置文档缺失 | 报错退出 |
| 上一 Agent 产出物不存在 | 报错退出，提示前置 Agent 未完成 |
| 核心冲突无法裁决 | 生成《冲突裁决申请书》提交人类 |
| PM 自检 3 次仍不通过 | 提交 Human Gate |

---

## 关联文档

| 文档 | 路径 |
|------|------|
| PM Agent（阶段3） | `agents/pm-stage3.md` |
| 迭代计划模板 | `.claude/templates/iteration-plan-template.md` |
| 看板模板 | `.claude/templates/sprint-status-template.md` |