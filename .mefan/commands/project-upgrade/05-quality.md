# /project-upgrade:05-quality – 质量测试与门禁
## 0. 日志声明（自动追加
执行本阶段所有步骤时，必须使用 `.mefan/hooks/log-event.sh` 记录日志。
- 进入阶段时：`bash .mefan/hooks/log-event.sh <阶段> <Agent> "阶段进入" "进入阶段X" "" "成功"`
- 结束阶段时：`bash .mefan/hooks/log-event.sh <阶段> <Agent> "阶段退出" "阶段X完成" "" "成功"`
- 在 Human Gate 前后记录审批事件

## 1. 角色激活
- **主导 Agent**：QA 工程师 (`agents/qa.md`)，负责测试执行、缺陷记录、人工测试指南。
- **修复 Agent**：开发者 (`agents/developer.md`)，负责修复被驳回的缺陷。
- **终审 Agent**：守护者 (`agents/guardian.md`)，执行最终门禁裁定。
- **决策 Agent**：项目经理 (`agents/pm.md`)，处理 P0 缺陷和进度异常。

## 2. 前置输入（必须读取）
- `.mefan/iterations/{sprint-name}/test-plan/upgrade-YYYY-MM-DD-title.md`
- `.mefan/iterations/{sprint-name}/iteration-plan.md`
- `.mefan/iterations/{sprint-name}/sprint-status.md`
- 阶段 4 产出的全部代码、单元测试、task-summary
- `.mefan/skills/write-manual-test-guide.md`
- `.mefan/skills/ug-triage-classification.md`

**前置检查**：执行前确认上述文件存在，若不存在则报错退出。

## 3. 强制规则
- `.mefan/knowledge/global/quality-gates.md`
- `.mefan/knowledge/global/exception-handling.md`
- `.mefan/knowledge/scenario-upgrade/api-compatibility.md`
- `.mefan/knowledge/scenario-upgrade/consistency-first.md`

## 4. 执行流程

### 4.1 自动化测试执行
**执行者**：QA 工程师

**目录检查**：确保 `.mefan/iterations/{sprint-name}/test-results/` 和 `.mefan/iterations/{sprint-name}/bug-log/` 目录存在。

1. **回归测试**：
   - 按照测试计划中的回归范围，运行全部回归测试套件。
   - 记录通过/失败结果到 `.mefan/iterations/{sprint-name}/test-results/regression-YYYY-MM-DD.log`。
   - 若回归测试发现失败，立即记录到 `.mefan/iterations/{sprint-name}/bug-log/auto-YYYY-MM-DD.md`（每条失败一个缺陷条目）。

2. **集成测试**：
   - 运行测试计划中设计的新增集成测试。
   - 记录结果，失败同上记录。

3. **性能测试**（若测试计划有要求）：
   - 运行性能基准对比测试。
   - 记录指标到质量报告。

### 4.2 探索性测试
**执行者**：QA 工程师

1. 基于需求文档中的核心流程和边界条件，设计并执行探索性测试。
2. 探索重点：边界值、异常路径、并发情况、兼容性。
3. 发现缺陷记录到 `.mefan/iterations/{sprint-name}/bug-log/auto-YYYY-MM-DD.md`。

### 4.3 缺陷分类与记录
**执行者**：QA 工程师

所有发现的缺陷（自动+探索）必须按 `.mefan/skills/ug-triage-classification.md` 进行分类：

| 维度 | 分类选项 |
|------|---------|
| 严重度 | P0(阻断)/P1(严重)/P2(一般)/P3(建议) |
| 类型 | 功能/性能/安全/兼容性/UI/文档 |
| 来源 | 自动化回归/自动化集成/探索性测试/人工测试 |

每次记录使用 `.mefan/templates/bug-log-template.md`。

### 4.4 人工测试指南生成
**执行者**：QA 工程师

1. 按 `.mefan/skills/write-manual-test-guide.md` 严格按照 `.mefan/templates/manual-test-guide-template.md` 生成 `.mefan/iterations/{sprint-name}/test-results/manual-test-guide.md`。
2. 内容必须包含：
   - 实现的功能清单及对应文件路径
   - 每个功能的测试用例（正常/边界/异常），含具体操作步骤和预期结果
   - 环境搭建步骤（如需）
   - 受影响模块的回归测试步骤
   - 明确的通过/失败判定标准

### 4.5 人机测试交接
**执行者**：QA 工程师 → 人类

1. QA Agent 将 `.mefan/iterations/{sprint-name}/test-results/manual-test-guide.md` 提交给用户，附一段摘要。
2. 用户按指南执行人工测试。
3. 用户将发现的缺陷（如有）反馈到 `.mefan/iterations/{sprint-name}/bug-log/manual-YYYY-MM-DD.md`，使用 bug-log 模板。
4. QA Agent 读取人工反馈，进行统一分类和汇总。

### 4.6 缺陷修复闭环
**执行者**：PM（决策）、开发者（修复）

1. QA 将所有缺陷（自动+人工）汇总后提交守护者预审。
2. 守护者对 P0/P1 缺陷标记为"阻塞"。
3. PM 审阅缺陷清单：
   - **P0 缺陷**：立即暂停当前迭代所有其他任务，打回阶段 4 由开发者优先修复。
   - **P1 缺陷**：打回阶段 4 修复，但允许其他非冲突任务并行。
   - **P2/P3 缺陷**：记录为技术债务，可在下个迭代处理。
4. 开发者修复缺陷时：
   - 在 bug-log 中补充**根因分析**和**修复方案**。
   - 补充对应的回归测试用例，防止复现。
   - 修复后通知 QA 重新测试。

### 4.7 质量报告生成
**执行者**：QA 工程师

所有缺陷修复完成后，严格按照 `.mefan/templates/quality-report-template.md` 输出 `.mefan/iterations/{sprint-name}/test-results/quality-report.md`：
- 测试覆盖统计
- 缺陷统计（按严重度/类型/来源）
- 性能基线对比
- API 兼容性检查结果
- 人工测试结果摘要
- 质量就绪声明

### 4.8 守护者终审门禁
**执行者**：守护者

- [ ] 是否存在未修复的 P0/P1 缺陷？（存在则驳回）
- [ ] 测试覆盖率是否达到质量门槛？
- [ ] 性能退化是否在允许范围内？
- [ ] API 兼容性是否未破坏？
- [ ] 一致性基线是否未被违反？

全部通过则输出 `APPROVED`，否则 `REJECTED` 并附驳回清单。

### 4.9 阶段结束
- PM 汇总质量报告摘要，提交 `[Human Gate]` 审批。
- 审批通过后，PM 更新看板状态。
- 若人工测试发现的 P0/P1 缺陷经 PM 评估可延后，记录为已知技术债务。

## 5. 产出物

| 产出物 | 路径 | 模板 |
|--------|------|------|
| regression-YYYY-MM-DD.log | `.mefan/iterations/{sprint-name}/test-results/regression-YYYY-MM-DD.log` | - |
| manual-test-guide.md | `.mefan/iterations/{sprint-name}/test-results/manual-test-guide.md` | `.mefan/templates/manual-test-guide-template.md` |
| quality-report.md | `.mefan/iterations/{sprint-name}/test-results/quality-report.md` | `.mefan/templates/quality-report-template.md` |
| bug-log/auto-YYYY-MM-DD.md | `.mefan/iterations/{sprint-name}/bug-log/auto-YYYY-MM-DD.md` | `.mefan/templates/bug-log-template.md` |
| bug-log/manual-YYYY-MM-DD.md | `.mefan/iterations/{sprint-name}/bug-log/manual-YYYY-MM-DD.md` | `.mefan/templates/bug-log-template.md` |

## 6. 本阶段产出物清单（供后续依赖检查）

| 文件名 | 完整路径 | 模板 | 被依赖阶段 |
|--------|----------|------|-----------|
| regression-YYYY-MM-DD.log | `.mefan/iterations/{sprint-name}/test-results/regression-YYYY-MM-DD.log` | - | 06-retrospect (§2) |
| manual-test-guide.md | `.mefan/iterations/{sprint-name}/test-results/manual-test-guide.md` | `.mefan/templates/manual-test-guide-template.md` | - |
| quality-report.md | `.mefan/iterations/{sprint-name}/test-results/quality-report.md` | `.mefan/templates/quality-report-template.md` | 06-retrospect (§2) |
| bug-log/auto-YYYY-MM-DD.md | `.mefan/iterations/{sprint-name}/bug-log/auto-YYYY-MM-DD.md` | `.mefan/templates/bug-log-template.md` | 06-retrospect (§2) |
| bug-log/manual-YYYY-MM-DD.md | `.mefan/iterations/{sprint-name}/bug-log/manual-YYYY-MM-DD.md` | `.mefan/templates/bug-log-template.md` | 06-retrospect (§2) |