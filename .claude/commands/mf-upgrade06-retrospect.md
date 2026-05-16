# /mf-upgrade:06-retrospect – 迭代总结与进化

> **当前阶段**：阶段 6（迭代总结与进化）
> **前置条件**：阶段 5 已完成，质量门禁已通过

---

## 0. 日志声明

执行本阶段所有步骤时，必须使用 `.claude/hooks/log-event.sh` 记录日志：
- 进入阶段：`bash .claude/hooks/log-event.sh "06" "$AGENT_NAME" "阶段进入" "阶段6开始" "" "成功"`
- 结束阶段：`bash .claude/hooks/log-event.sh "06" "$AGENT_NAME" "阶段退出" "阶段6完成" "" "成功"`
- 产出文件：`bash .claude/hooks/log-event.sh "06" "$AGENT_NAME" "产出物" "生成 <文件>" "<文件>" "成功"`

---

## 1. 规则加载（按需引用）

| 规则/技能 | 用途 | 引用时机 |
|-----------|------|---------|
| `.claude/rules/global/session-init.md` | 阶段初始化三原则 | 步骤 2 开始前 |
| `.claude/rules/global/harness-version-control.md` | 版本控制规则 | pm-stage6 内部 |
| `.claude/rules/global/tech-debt-management.md` | 技术债务管理 | pm-stage6 内部 |
| `.claude/rules/global/evolution-process.md` | 进化流程规则 | coach-stage6 内部 |

---

## 2. 前置检查

**执行者**：框架自动检查

### 2.1 检查阶段 5 产出物

1. 读取 `.claude/iterations/{sprint-name}/session-status.md`
2. 确认阶段 5 已完成（状态为 ✅）
3. 若不存在或阶段 5 未完成，报错退出：
   ```
   [自动检查] 阶段 5 未完成或 session-status.md 缺失，请先执行 /mf-upgrade:05-quality
   ```

### 2.2 自动检查上一 Agent 产出物

#### 步骤 1 → 步骤 2 自动检查

**触发时机**：在激活 `coach-stage6.md` 之前

1. 检查 `.claude/iterations/{sprint-name}/iteration-retrospective.md` 是否存在
2. 若不存在，报错：
   ```
   [自动检查] pm-stage6 产出物不存在：iteration-retrospective.md 未找到
   错误：前置 Agent 未完成工作，请先执行 pm-stage6
   ```
3. 若存在，继续执行步骤 2

#### 步骤 2 → 步骤 3 自动检查

**触发时机**：在激活 `pm-stage6.md`（步骤 3）之前

1. 检查 `.claude/evolution-proposals/upgrade-*.md` 是否存在
2. 若不存在，报错：
   ```
   [自动检查] coach-stage6 产出物不存在：evolution-proposals/upgrade-*.md 未找到
   错误：前置 Agent 未完成工作，请先执行 coach-stage6
   ```
3. 若存在，继续执行步骤 3

#### 步骤 3 → 步骤 4 自动检查

**触发时机**：在激活 `pm-stage6.md`（步骤 4）之前

1. 检查 `.claude/evolution-proposals/guardian-verification-*.md` 是否存在
2. 若不存在，报错：
   ```
   [自动检查] guardian-stage6 产出物不存在：guardian-verification-*.md 未找到
   错误：前置 Agent 未完成工作，请先执行 guardian-stage6
   ```
3. 若存在，继续执行步骤 4

---

## 3. 工作流编排

### 步骤 1：PM 主导迭代总结

- **前置检查**：自动检查阶段 5 产出物
- **激活 Agent**：`agents/pm-stage6.md`
- **职责**：PM 执行完整的迭代总结工作（迭代数据汇总、迭代总结撰写、进化提案审批、版本与知识库更新、异常处理）
- **引用规则**：`.claude/rules/global/harness-version-control.md`、`.claude/rules/global/tech-debt-management.md`、`.claude/rules/global/evolution-process.md`
- **产出物**：
  - `.claude/iterations/{sprint-name}/iteration-retrospective.md`
  - `CHANGELOG.md`（更新）
  - `.claude/HARNESS_VERSION.md`（更新）
- **完成后**：更新 session-status.md 中阶段 6 PM 完成状态为"✅"

### 步骤 2：进化教练主导进化分析

- **前置检查**：自动检查步骤 1 产出物（iteration-retrospective.md 存在）
- **激活 Agent**：`agents/coach-stage6.md`
- **职责**：进化教练从全量迭代日志中提取可复用的改进模式，生成结构化的进化提案
- **引用技能**：`.claude/skills/pattern-extraction-from-logs.md`、`.claude/skills/root-cause-analysis.md`
- **产出物**：`.claude/evolution-proposals/upgrade-YYYY-MM-DD-title.md`
- **完成后**：更新 session-status.md 中阶段 6 Coach 完成状态为"✅"

### 步骤 3：守护者验证进化提案

- **前置检查**：自动检查步骤 2 产出物（evolution-proposal.md 存在）
- **激活 Agent**：`agents/guardian-stage6.md`
- **职责**：守护者验证进化提案的可合并性、框架版本影响，输出验证报告
- **引用规则**：`.claude/rules/global/evolution-process.md`、`.claude/rules/global/harness-version-control.md`
- **产出物**：`.claude/evolution-proposals/guardian-verification-YYYY-MM-DD.md`
- **完成后**：更新 session-status.md 中阶段 6 Guardian 完成状态为"✅"

### 步骤 4：PM 生成项目全局进度报告

- **前置检查**：自动检查步骤 3 产出物（guardian-verification 存在）
- **激活 Agent**：`agents/pm-stage6.md`
- **职责**：PM 生成项目状态报告，覆盖更新 PROJECT_STATUS.md
- **产出物**：`.claude/reports/PROJECT_STATUS.md`
- **完成后**：更新 session-status.md 中阶段 6 完成状态为"✅"

---

## 4. Human Gate

**审查内容**：迭代总结摘要、进化提案数量、技术债务趋势、守护者验证报告
**通过条件**：人类审批通过 + 守护者验证通过

---

## 5. 产出物

| 产出物 | 路径 |
|--------|------|
| iteration-retrospective.md | `.claude/iterations/{sprint-name}/iteration-retrospective.md` |
| evolution-proposal.md | `.claude/evolution-proposals/upgrade-YYYY-MM-DD-title.md` |
| guardian-verification.md | `.claude/evolution-proposals/guardian-verification-YYYY-MM-DD.md` |
| PROJECT_STATUS.md | `.claude/reports/PROJECT_STATUS.md` |
| CHANGELOG.md | `CHANGELOG.md`（更新） |
| HARNESS_VERSION.md | `.claude/HARNESS_VERSION.md`（更新） |

---

## 6. 异常处理

| 异常场景 | 处理方式 |
|---------|---------|
| 前置文档缺失 | 报错退出 |
| 上一 Agent 产出物不存在 | 报错退出，提示前置 Agent 未完成 |
| 进化提案连续 3 条被驳回 | 汇总驳回理由，提交 Human Gate 决策 |
| CHANGELOG.md 更新失败 | 报错退出，检查文件权限 |
| HARNESS_VERSION.md 更新失败 | 报错退出，检查文件权限 |
| 提案合并时冲突 | 标注"冲突待解决"，阻止合并，提交 Human Gate |
| 实验规则验证失败连续 3 次 | 撤销实验，标记为"不采纳"，记录教训 |

---

## 关联文档

| 文档 | 路径 |
|------|------|
| PM Agent（阶段6） | `agents/pm-stage6.md` |
| 进化教练 Agent（阶段6） | `agents/coach-stage6.md` |
| 守护者 Agent（阶段6） | `agents/guardian-stage6.md` |
| 迭代总结模板 | `.claude/templates/iteration-retrospective-template.md` |
| 进化提案模板 | `.claude/templates/evolution-proposal-template.md` |
| 项目状态模板 | `.claude/templates/project-status-template.md` |
| 版本控制规则 | `.claude/rules/global/harness-version-control.md` |
| 技术债务管理规则 | `.claude/rules/global/tech-debt-management.md` |
| 进化流程规则 | `.claude/rules/global/evolution-process.md` |