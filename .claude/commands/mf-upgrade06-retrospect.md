# /mf-upgrade:06-retrospect – 迭代总结与进化
## 0. 日志声明（自动追加
执行本阶段所有步骤时，必须使用 `.claude/hooks/log-event.sh` 记录日志。
- 进入阶段时：`bash .claude/hooks/log-event.sh <阶段> <Agent> "阶段进入" "进入阶段X" "" "成功"`
- 结束阶段时：`bash .claude/hooks/log-event.sh <阶段> <Agent> "阶段退出" "阶段X完成" "" "成功"`
- 在 Human Gate 前后记录审批事件

## 1. 角色激活
- **主导 Agent**：项目经理 (`agents/pm.md`)，撰写迭代总结、管理版本和债务。
- **分析 Agent**：进化教练 (`agents/coach.md`)，分析缺陷模式、生成进化提案。
- **验证 Agent**：守护者 (`agents/guardian.md`)，在下一迭代验证进化提案的有效性。

## 2. 前置输入（必须读取）
- 本迭代全部产出物：需求文档、ADR、测试计划、task-summary、质量报告、bug-log
- `.claude/iterations/{sprint-name}/sprint-status.md`
- `.claude/iterations/{sprint-name}/session-status.md`
- Hook 拦截日志（所有 `violations.json`）
- `.claude/skills/pattern-extraction-from-logs.md`
- `.claude/skills/root-cause-analysis.md`
- `.claude/rules/global/tech-debt-management.md`

**前置检查**：执行前确认上述文件存在，若不存在则报错退出。

## 3. 强制规则
- `.claude/rules/global/harness-version-control.md`
- `.claude/rules/global/tech-debt-management.md`
- `.claude/rules/global/evolution-process.md`（进化提案的实验验证、合并流程）

## 4. 执行流程

### 4.1 迭代数据汇总
**执行者**：PM

收集本迭代的关键数据：
- 用户故事总数及完成数
- 任务总数及完成数（来自 sprint-status.md）
- 缺陷总数及分类统计（来自 quality-report.md）
- Hook 拦截次数及高频违规类型
- 工时汇总（计划 vs 实际）

### 4.2 迭代总结撰写
**执行者**：PM

**目录检查**：确保 `.claude/iterations/{sprint-name}/` 目录存在。

输出 `.claude/iterations/{sprint-name}/retrospective.md`，**必须使用** `.claude/templates/iteration-retrospective-template.md`：

1. **迭代概览**：用户故事数、任务完成率、工时偏差。
2. **缺陷分析**：按类型和严重度分布图（文字描述）。
3. **做得好的地方**：至少列出 3 个正面案例（如某任务零拦截通过、某 Bug 半小时修复）。
4. **做得不好的地方**：至少列出 3 个问题案例（如连续 Hook 拦截、P0 缺陷发生）。
5. **技术债务评估**：按 `.claude/rules/global/tech-debt-management.md` 要求评估当前债务分布和风险。
6. **待改进项清单**：列出可分配给具体阶段或 Agent 的改进点。

### 4.3 进化分析
**执行者**：进化教练

1. 审查本迭代全量日志（按 `.claude/skills/pattern-extraction-from-logs.md`）：
   - Hook 拦截日志 → 找出高频违规模式
   - bug-log 中的根因分类 → 找出知识缺失/规则不完备占比最高的类型
   - task-summary 中的技术债务 → 找出重复出现的债务类型
   - retrospective 中的待改进项

2. 识别可沉淀为 Rule/Skill 的模式：
   - **反复出现相同违规** → 建议新增或加强 Rule
   - **开发者频繁查阅同一文档** → 建议新建 Skill
   - **某类缺陷反复发生** → 建议修改阶段 2 的设计检查项或阶段 4 的 CR 清单

3. **目录检查**：确保 `.claude/evolution-proposals/` 目录存在。
3. 输出 `.claude/evolution-proposals/upgrade-YYYY-MM-DD-title.md`，**必须使用** `.claude/templates/evolution-proposal-template.md`：
   - 每条提案需含：触发原因（数据支撑）、具体修改草案、预期效果

### 4.4 进化提案审批
**执行者**：PM

1. 审阅进化教练的提案，逐条判断是否采纳。
2. 若采纳：
   - 标记为"实验状态"，写入 `.claude/rules-proposed/` 或 `.claude/skills-proposed/`。
   - 在下个迭代中作为实验规则运行。
3. 若驳回：记录驳回理由。
4. 提交 `[Human Gate]` 对采纳的提案进行最终审批。

### 4.5 版本与知识库更新
**执行者**：PM

1. 更新 `CHANGELOG.md`：追加本次迭代的功能和修复。
2. 更新 `.claude/HARNESS_VERSION.md`：按语义版本递增框架版本号。
3. 将已审批通过且完成实验验证（从上一个迭代的实验池中）的 Rule/Skill 正式合并入 `.claude/rules/` 和 `.claude/skills/`。
4. 更新知识库索引（如有）。

### 4.6 阶段结束
- PM 输出迭代总结摘要，包含进化提案数量和技术债务趋势。
- 等待 `[Human Gate]` 审批。
- 审批通过后，标记本迭代关闭，准备下一迭代。

### 4.7 生成项目全局进度报告
**执行者**：PM

1. **目录检查**：确保 `.claude/reports/` 目录存在。
2. 根据 `.claude/templates/project-status-template.md` 生成 `.claude/reports/PROJECT_STATUS.md`。
3. 完成后记录日志：`bash .claude/hooks/log-event.sh 6 PM "产出物" "生成 PROJECT_STATUS.md" "PROJECT_STATUS.md" "成功"`

## 5. 产出物

| 产出物 | 路径 | 模板 |
|--------|------|------|
| retrospective.md | `.claude/iterations/{sprint-name}/retrospective.md` | `.claude/templates/iteration-retrospective-template.md` |
| evolution-proposal.md | `.claude/evolution-proposals/upgrade-YYYY-MM-DD-title.md` | `.claude/templates/evolution-proposal-template.md` |
| PROJECT_STATUS.md | `.claude/reports/PROJECT_STATUS.md` | `.claude/templates/project-status-template.md` |
| CHANGELOG.md | `CHANGELOG.md`（更新） | - |
| HARNESS_VERSION.md | `.claude/HARNESS_VERSION.md`（更新） | - |

## 6. 本阶段产出物清单（供后续依赖检查）

| 文件名 | 完整路径 | 模板 | 被依赖阶段 |
|--------|----------|------|-----------|
| retrospective.md | `.claude/iterations/{sprint-name}/retrospective.md` | `.claude/templates/iteration-retrospective-template.md` | 下一 iteration 的 00-init |
| evolution-proposal.md | `.claude/evolution-proposals/upgrade-YYYY-MM-DD-title.md` | `.claude/templates/evolution-proposal-template.md` | 框架维护用 |
| PROJECT_STATUS.md | `.claude/reports/PROJECT_STATUS.md` | `.claude/templates/project-status-template.md` | 全局可读 |
| CHANGELOG.md | `CHANGELOG.md` | - | 全局可读 |
| HARNESS_VERSION.md | `.claude/HARNESS_VERSION.md` | - | 所有阶段（版本参考） |