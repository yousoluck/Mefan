# /mf-upgrade:05-quality – 质量测试与门禁

> **当前阶段**：阶段 5（质量测试与门禁）
> **前置条件**：阶段 4 已完成，代码已产出

---

## 0. 日志声明

执行本阶段所有步骤时，必须使用 `.claude/hooks/log-event.sh` 记录日志：
- 进入阶段：`bash .claude/hooks/log-event.sh "05" "$AGENT_NAME" "阶段进入" "阶段5开始" "" "成功"`
- 结束阶段：`bash .claude/hooks/log-event.sh "05" "$AGENT_NAME" "阶段退出" "阶段5完成" "" "成功"`
- 产出文件：`bash .claude/hooks/log-event.sh "05" "$AGENT_NAME" "产出物" "生成 <文件>" "<文件>" "成功"`

---

## 1. 规则加载（按需引用）

| 规则/技能 | 用途 | 引用时机 |
|-----------|------|---------|
| `.claude/rules/global/session-init.md` | 阶段初始化三原则 | 步骤 2 开始前 |
| `.claude/rules/global/quality-gates.md` | 质量门禁标准 | qa-stage5 内部 |
| `.claude/rules/global/exception-handling.md` | 异常处理规则 | qa-stage5 内部 |
| `.claude/rules/global/manual-test-bug-handling.md` | 人工测试Bug处理 | qa-stage5 内部 |
| `.claude/rules/scenario-upgrade/api-compatibility.md` | API兼容性 | qa-stage5 内部 |
| `.claude/rules/scenario-upgrade/consistency-first.md` | 一致性优先 | qa-stage5 内部 |

---

## 2. 前置检查

**执行者**：框架自动检查

### 2.1 检查阶段 4 产出物

1. 读取 `.claude/iterations/{sprint-name}/session-status.md`
2. 确认阶段 4 已完成（状态为 ✅）
3. 若不存在或阶段 4 未完成，报错退出：
   ```
   [自动检查] 阶段 4 未完成或 session-status.md 缺失，请先执行 /mf-upgrade:04-implement
   ```

### 2.2 自动检查上一 Agent 产出物

#### 步骤 1 → 步骤 2 自动检查

**触发时机**：在激活 `pm-stage5.md` 之前

1. 检查 `.claude/iterations/{sprint-name}/test-results/quality-report.md` 是否存在
2. 若不存在，报错：
   ```
   [自动检查] qa-stage5 产出物不存在：test-results/quality-report.md 未找到
   错误：前置 Agent 未完成工作，请先执行 qa-stage5
   ```
3. 若存在，继续执行步骤 2

#### 步骤 2 → 步骤 3 自动检查

**触发时机**：在激活 `dev-stage5.md` 之前

1. 检查 `.claude/iterations/{sprint-name}/bug-log/auto-*.md` 或 `.claude/iterations/{sprint-name}/bug-log/manual-*.md` 是否存在
2. 若存在缺陷记录（bug-log 中有 P0/P1），继续执行步骤 3
3. 若不存在且无缺陷记录，跳过步骤 3（无缺陷需修复）
4. 若存在但 PM 决策为"延期"，跳过步骤 3

#### 步骤 3 → 步骤 4 自动检查

**触发时机**：在激活 `guardian-stage5.md` 之前

1. 检查 dev-stage5 是否完成（如果步骤 3 被跳过，则直接检查）
2. 若缺陷修复未完成但 Human Gate 审批通过，继续执行步骤 4
3. 否则报错：

---

## 3. 工作流编排

### 步骤 1：QA 主导质量测试

- **前置检查**：自动检查阶段 4 产出物
- **激活 Agent**：`agents/qa-stage5.md`
- **职责**：QA 执行完整质量测试工作（自动化测试、探索性测试、缺陷分类与记录、人工测试指南生成、缺陷汇总、质量报告生成）
- **引用技能**：`.claude/skills/write-manual-test-guide.md`、`.claude/skills/bug-triage-classification.md`
- **引用规则**：`.claude/rules/global/quality-gates.md`、`.claude/rules/global/manual-test-bug-handling.md`
- **产出物**：
  - `.claude/iterations/{sprint-name}/test-results/regression-YYYY-MM-DD.log`
  - `.claude/iterations/{sprint-name}/test-results/manual-test-guide.md`
  - `.claude/iterations/{sprint-name}/test-results/quality-report.md`
  - `.claude/iterations/{sprint-name}/bug-log/auto-YYYY-MM-DD.md`
  - `.claude/iterations/{sprint-name}/bug-log/manual-YYYY-MM-DD.md`
- **完成后**：更新 session-status.md 中阶段 5 QA 完成状态为"✅"

### 步骤 2：PM 处理 P0/P1 缺陷决策

- **前置检查**：自动检查步骤 1 产出物（quality-report.md 存在）
- **激活 Agent**：`agents/pm-stage5.md`
- **职责**：PM 审阅缺陷清单，做 P0/P1 缺陷决策，协调开发者和 QA
- **引用规则**：`.claude/rules/global/exception-handling.md`、`.claude/rules/global/manual-test-bug-handling.md`
- **产出物**：更新 session-status.md 中阶段 5 PM 完成状态为"✅"

### 步骤 3：开发者执行缺陷修复（如有 P0/P1 缺陷）

- **前置检查**：自动检查步骤 2 决策（若有 P0/P1 缺陷需修复）
- **激活 Agent**：`agents/dev-stage5.md`
- **职责**：开发者接收 PM 分配的缺陷修复任务，执行修复并补充回归测试
- **引用技能**：`.claude/skills/tdd-red-green-refactor.md`
- **引用规则**：`.claude/rules/scenario-upgrade/consistency-first.md`、`.claude/rules/scenario-upgrade/api-compatibility.md`
- **完成后**：更新 session-status.md 中阶段 5 Dev 完成状态为"✅"

### 步骤 4：守护者执行终审门禁

- **前置检查**：自动检查步骤 2 和步骤 3（若需要）产出物
- **激活 Agent**：`agents/guardian-stage5.md`
- **职责**：守护者检查所有质量门禁，输出 APPROVED 或 REJECTED
- **引用规则**：`.claude/rules/global/quality-gates.md`
- **产出物**：更新 session-status.md 中阶段 5 完成状态为"✅"

---

## 4. Human Gate

**审查内容**：质量报告摘要、P0/P1 缺陷状态、人工测试结果
**通过条件**：全部门禁检查通过

---

## 5. 产出物

| 产出物 | 路径 |
|--------|------|
| regression-YYYY-MM-DD.log | `.claude/iterations/{sprint-name}/test-results/regression-YYYY-MM-DD.log` |
| manual-test-guide.md | `.claude/iterations/{sprint-name}/test-results/manual-test-guide.md` |
| quality-report.md | `.claude/iterations/{sprint-name}/test-results/quality-report.md` |
| bug-log/auto-YYYY-MM-DD.md | `.claude/iterations/{sprint-name}/bug-log/auto-YYYY-MM-DD.md` |
| bug-log/manual-YYYY-MM-DD.md | `.claude/iterations/{sprint-name}/bug-log/manual-YYYY-MM-DD.md` |

---

## 6. 异常处理

| 异常场景 | 处理方式 |
|---------|---------|
| 前置文档缺失 | 报错退出 |
| 上一 Agent 产出物不存在 | 报错退出，提示前置 Agent 未完成 |
| P0 缺陷发现 | 立即暂停其他任务，优先修复 P0 |
| P1 缺陷发现 | 允许非冲突任务并行 |
| P2/P3 缺陷 | 记录为技术债务，下个迭代处理 |
| 门禁未通过 | 驳回清单，修复后重新测试 |

---

## 关联文档

| 文档 | 路径 |
|------|------|
| QA Agent（阶段5） | `agents/qa-stage5.md` |
| PM Agent（阶段5） | `agents/pm-stage5.md` |
| DEV Agent（阶段5） | `agents/dev-stage5.md` |
| 守护者 Agent（阶段5） | `agents/guardian-stage5.md` |
| 质量门禁规则 | `.claude/rules/global/quality-gates.md` |
| Bug 处理规则 | `.claude/rules/global/manual-test-bug-handling.md` |
| 质量报告模板 | `.claude/templates/quality-report-template.md` |
| Bug 日志模板 | `.claude/templates/bug-log-template.md` |