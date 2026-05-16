# /mf-upgrade:04-implement – 迭代实现

> **当前阶段**：阶段 4（迭代实现）
> **前置条件**：阶段 3 已完成，迭代计划和看板已初始化

---

## 0. 日志声明

执行本阶段所有步骤时，必须使用 `.claude/hooks/log-event.sh` 记录日志：
- 进入阶段：`bash .claude/hooks/log-event.sh "04" "$AGENT_NAME" "阶段进入" "阶段4开始" "" "成功"`
- 结束阶段：`bash .claude/hooks/log-event.sh "04" "$AGENT_NAME" "阶段退出" "阶段4完成" "" "成功"`
- 产出文件：`bash .claude/hooks/log-event.sh "04" "$AGENT_NAME" "产出物" "生成 <文件>" "<文件>" "成功"`

---

## 1. 规则加载（按需引用）

| 规则/技能 | 用途 | 引用时机 |
|-----------|------|---------|
| `.claude/rules/global/session-init.md` | 阶段初始化三原则 | 步骤 2 开始前 |
| `.claude/rules/scenario-upgrade/consistency-first.md` | 一致性优先规则 | dev-stage4 内部 |
| `.claude/rules/scenario-upgrade/api-compatibility.md` | API兼容性规则 | dev-stage4 内部 |
| `.claude/rules/scenario-upgrade/reuse-before-build.md` | 复用优先规则 | dev-stage4 内部 |
| `.claude/rules/scenario-upgrade/reference-module.md` | 参考模块规则 | dev-stage4 内部 |
| `.claude/rules/global/hook-vs-guardian.md` | Hook与守护者边界 | dev-stage4 内部 |
| `.claude/rules/global/exception-handling.md` | 异常处理规则 | dev-stage4 内部 |

---

## 2. 前置检查

**执行者**：框架自动检查

### 2.1 检查阶段 3 产出物

1. 读取 `.claude/iterations/{sprint-name}/session-status.md`
2. 确认阶段 3 已完成（状态为 ✅）
3. 若不存在或阶段 3 未完成，报错退出：
   ```
   [自动检查] 阶段 3 未完成或 session-status.md 缺失，请先执行 /mf-upgrade:03-plan
   ```

### 2.2 自动检查上一 Agent 产出物

#### 步骤 1 → 步骤 2 自动检查

**触发时机**：在激活 `pm-stage4.md` 之前

1. 检查 `.claude/iterations/{sprint-name}/task-summary/T{NNN}.md` 是否存在（至少一个）
2. 若不存在，报错：
   ```
   [自动检查] dev-stage4 产出物不存在：task-summary/T{NNN}.md 未找到
   错误：前置 Agent 未完成工作，请先执行 dev-stage4
   ```
3. 若存在，继续执行步骤 2

---

## 3. 工作流编排

### 步骤 1：开发者主导迭代实现

- **前置检查**：自动检查阶段 3 产出物（iteration-plan.md 和 sprint-status.md）
- **激活 Agent**：`agents/dev-stage4.md`
- **职责**：开发者执行完整的迭代实现工作（领取任务、TDD 开发循环、Hook 检查、Code Review、任务收尾）
- **引用技能**：`.claude/skills/tdd-red-green-refactor.md`、`.claude/skills/git-workflow.md`、`.claude/skills/query-third-party-docs.md`
- **引用规则**：`.claude/rules/scenario-upgrade/consistency-first.md`、`.claude/rules/scenario-upgrade/api-compatibility.md`、`.claude/rules/global/hook-vs-guardian.md`
- **产出物**：
  - `.claude/iterations/{sprint-name}/task-summary/T{NNN}.md`
  - `.claude/iterations/{sprint-name}/test-results/unit-T{NNN}.log`
  - interception-analysis.md（仅 Hook 拦截 ≥2 次时）
- **完成后**：更新 session-status.md 中阶段 4 Dev 完成状态为"✅"

### 步骤 2：PM 执行进度监控

- **前置检查**：自动检查步骤 1 产出物（至少一个 task-summary 存在）
- **激活 Agent**：`agents/pm-stage4.md`
- **职责**：PM 监控开发进度，处理异常（Hook 拦截、进度滞后、核心冲突）
- **引用规则**：`.claude/rules/global/exception-handling.md`、`.claude/rules/global/iteration-planning.md`
- **产出物**：更新 session-status.md 中阶段 4 完成状态为"✅"

---

## 4. Human Gate

**触发条件**：所有任务完成或达到迭代里程碑
**审查内容**：进度摘要、实际工时 vs 计划工时、异常记录

---

## 5. 产出物

| 产出物 | 路径 |
|--------|------|
| task-summary/T{NNN}.md | `.claude/iterations/{sprint-name}/task-summary/T{NNN}.md` |
| test-results/unit-T{NNN}.log | `.claude/iterations/{sprint-name}/test-results/unit-T{NNN}.log` |
| interception-analysis.md | `.claude/iterations/{sprint-name}/interception-analysis.md`（仅 Hook 拦截 ≥2 次时） |

---

## 6. 异常处理

| 异常场景 | 处理方式 |
|---------|---------|
| 前置文档缺失 | 报错退出 |
| 上一 Agent 产出物不存在 | 报错退出，提示前置 Agent 未完成 |
| Hook 拦截第 1 次 | 开发者自行修复 |
| Hook 拦截第 2 次 | 必须编写 interception-analysis.md |
| Hook 拦截第 3 次 | 暂停任务，PM 介入，可能回溯阶段 2 |
| 进度滞后 > 50% | PM 评估调整后续任务 |
| 设计冲突 | 记录到 session-status.md，提交 Human Gate |

---

## 关联文档

| 文档 | 路径 |
|------|------|
| 开发者 Agent（阶段4） | `agents/dev-stage4.md` |
| PM Agent（阶段4） | `agents/pm-stage4.md` |
| TDD 技能 | `.claude/skills/tdd-red-green-refactor.md` |
| Git 工作流技能 | `.claude/skills/git-workflow.md` |
| Code Review 技能 | `.claude/skills/code-review-checklist.md` |
| Task Summary 模板 | `.claude/templates/task-summary-template.md` |
| Hook 与守护者规则 | `.claude/rules/global/hook-vs-guardian.md` |
| 异常处理规则 | `.claude/rules/global/exception-handling.md` |