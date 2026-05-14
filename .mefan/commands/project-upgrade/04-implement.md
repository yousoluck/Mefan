# /project-upgrade:04-implement – 迭代实现
## 0. 日志声明（自动追加
执行本阶段所有步骤时，必须使用 `.mefan/hooks/log-event.sh` 记录日志。
- 进入阶段时：`bash .mefan/hooks/log-event.sh <阶段> <Agent> "阶段进入" "进入阶段X" "" "成功"`
- 结束阶段时：`bash .mefan/hooks/log-event.sh <阶段> <Agent> "阶段退出" "阶段X完成" "" "成功"`
- 在 Human Gate 前后记录审批事件

## 1. 角色激活
- **主导 Agent**：开发者 (`agents/developer.md`)，按任务清单逐个实现。
- **自动审查 Agent**：守护者 (`agents/guardian.md`)，通过 Hook 和子代理执行检查。
- **监控 Agent**：PM (`agents/pm.md`)，监控进度，处理异常。

## 2. 前置输入（必须读取）
- `iterations/upgrade-sprint-YYYY-MM-DD.md`（获取任务列表和顺序）
- `adr/upgrade-YYYY-MM-DD-title.md`（获取详细设计和参考实现）
- `context/consistency-baseline.md`（获取风格约束）
- `skills/tdd-red-green-refactor.md`（TDD 操作指南）
- `skills/git-workflow.md`（版本控制规范）
- `skills/query-third-party-docs.md`（若需新依赖）

## 3. 强制规则
- `consistency-first.md`
- `api-compatibility.md`
- `reuse-before-build.md`
- `knowledge/global/hook-vs-guardian.md`
- `knowledge/global/exception-handling.md`

## 4. 执行流程

### 4.1 开发环境准备（每个任务开始前）
**执行者**：开发者

1. 从看板中领取一个 `To Do` 任务，更新状态为 `In Progress`。
2. 创建 Git 特性分支：按 `skills/git-workflow.md` 规范命名。
3. 确认任务的前置依赖任务已完成，若未完成则暂停并通知 PM。
4. 若任务涉及新依赖，调用 `skills/query-third-party-docs.md` 查询官方 API，将关键用法记录在 task-summary 中。禁止臆造 API。

### 4.2 TDD 开发循环（每个任务的核心流程）
**执行者**：开发者

**必须严格按照 TDD 三步循环执行：**

#### 4.2.1 红色阶段（写失败测试）
1. 根据测试计划中本任务关联的测试用例，编写一个最小化的失败测试。
2. 运行测试，确认测试失败（红色）。若测试意外通过，重新检查测试逻辑。
3. 保存文件。

#### 4.2.2 绿色阶段（写最小实现）
1. 编写刚好能让测试通过的最小代码。
2. **强约束**：
   - 必须遵循 ADR 中的参考实现路径，模仿其风格。
   - 必须使用项目中已有的工具函数（从需求文档的可复用清单查找）。
   - 新增 API 必须符合 `api-compatibility.md`。
   - 不可夹带无关格式化、重构、优化。
3. 运行测试，确认变绿。
4. 保存文件。

#### 4.2.3 重构阶段（优化结构）
1. 在测试保护下，对代码进行结构优化（消除重复、提升可读性），但不改变行为。
2. 确保代码与一致性基线完全对齐。
3. 运行所有相关测试，确认全部通过。
4. 保存文件。

### 4.3 自动化 Hook 检查（每次保存后自动触发）
每次 `Write`/`Edit` 操作后，系统自动运行以下 Hook：

| Hook 脚本 | 检查内容 | 失败处理 |
|-----------|---------|---------|
| `hooks/check-consistency.py` | 命名风格、文件位置、模式一致性 | 返回违规列表，开发者必须修复 |
| `hooks/check-api-compatibility.py` | API 签名是否被修改 | 若修改且未经审批，阻断 |
| `hooks/check-diff-size.py` | 单次变更行数是否异常 | 超阈值（200行）警告，需人工确认 |

**Hook 拦截处理流程**（参见 `exception-handling.md`）：
- **第 1 次拦截**：开发者根据违规列表自行修复。
- **第 2 次拦截**：必须编写 `interception-analysis.md` 说明根因和修复计划。
- **第 3 次拦截**：暂停当前任务，通知 PM 介入，可能回溯到阶段 2 调整设计。

### 4.4 守护者 Code Review（任务完成后）
**执行者**：守护者（子代理模式）

1. 开发者完成 TDD 循环且所有 Hook 通过后，提交 Code Review 请求。
2. 守护者子代理启动，执行深度审查（详见 `skills/code-review-checklist.md`）：
   - 语义正确性
   - 安全漏洞
   - 性能隐患
   - 代码重复与可合并性
   - 一致性深度检查
3. 审查结果：
   - **通过**：进入步骤 4.5。
   - **有条件通过**：列出建议项，开发者可选择采纳。
   - **驳回**：列出必须修复的阻塞项，开发者修复后重新提交 CR。

### 4.5 任务收尾
**执行者**：开发者

1. 更新看板任务状态为 `In Review` → `Done`。
2. 生成 `task-summary/<task-id>.md`，包含：修改清单、新 API、技术债务、优化建议。
3. 提交代码到特性分支，按 `skills/git-workflow.md` 规范编写 commit message。
4. 更新 `iterations/sprint-status.md` 的实际工时。

### 4.6 进度监控与异常处理
**执行者**：PM

1. 每完成一个任务，检查看板整体进度。
2. 若某任务实际工时超过计划 50%，触发进度警戒。PM 评估是否需要调整后续任务。
3. 若开发者触发“连续 Hook 拦截 ≥3 次”异常，PM 暂停任务并按 `exception-handling.md` 决策。

## 5. 产出物
- 实现代码（在特性分支）
- 单元测试代码
- `task-summary/<task-id>.md`
- `test-results/unit-<task-id>.log`
- `interception-analysis.md`（如触发）

## 6. 阶段结束
- 所有任务全部完成后，PM 输出进度摘要，等待用户确认进入阶段 5。