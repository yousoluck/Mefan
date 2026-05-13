# /project-upgrade:03-plan – 迭代计划与任务排期

## 1. 角色激活
- **主导 Agent**：项目经理 (`agents/pm.md`)，负责迭代范围、任务拆解、冲突裁决、看板初始化。
- **辅助 Agent**：分析师 (`agents/analyst.md`)，负责将 ADR 中的实现步骤拆解为原子任务。

## 2. 前置输入（必须读取）
- `adr/upgrade-YYYY-MM-DD-title.md`
- `test-plan/upgrade-YYYY-MM-DD-title.md`
- `requirements/upgrade-YYYY-MM-DD-title.md`（用于对照功能优先级）
- `iterations/session-status.md`（查看是否有异常记录或遗留冲突）

## 3. 强制规则
- `knowledge/global/iteration-planning.md`（任务拆解标准）
- `knowledge/global/conflict-resolution.md`
- `knowledge/scenario-upgrade/reuse-before-build.md`（检查是否有任务可复用现有代码）

## 4. 执行流程

### 4.1 任务拆解
**执行者**：分析师（PM 审核）

1. 读取 ADR 中的详细设计（目录、接口、数据流）和测试计划中的测试场景。
2. 将整体工作拆解为**原子任务**，原子任务标准：
   - 单任务预计完成时间 ≤ 1 天（若超 1 天，强制进一步拆分）。
   - 每个任务有明确的输入和输出（不能是“继续开发”这类模糊描述）。
   - 每个任务关联具体的模块/文件。
3. 为每个任务标注：
   - 任务类型：编码 / 测试编写 / 重构 / 文档
   - 预估工时
   - 依赖的前置任务
   - 风险等级（高/中/低，依据模块冲突历史和新度）
   - 是否需要引入新依赖（如需要，标记“待依赖审查”）
4. 输出任务列表草案，提交给 PM。

### 4.2 冲突裁决与串并行决策
**执行者**：PM

1. 接收分析师的任务列表，对照 `sprint-status.md` 中其他正在进行的任务。
2. 对每个任务运行的模块，执行冲突检测：
   - 若任务涉及模块与其他活跃任务产生**核心冲突**，按 `conflict-resolution.md` 决策树处理：
     a. 串行化（优先）
     b. 分模块（若可拆分）
     c. 人类裁决（生成《冲突裁决申请书》）
   - 若仅为**边缘冲突**，允许并行，但在迭代计划中标注风险。
3. 最终确定任务执行顺序，标注串行/并行关系。

### 4.3 生成迭代计划
**执行者**：PM

1. 创建 `iterations/upgrade-sprint-YYYY-MM-DD.md`，使用模板 `templates/iteration-plan-template.md`。
2. 填入：
   - 用户故事列表（从需求文档提取）
   - 任务清单（从 4.2 裁决结果）
   - WIP 限制（并行任务数上限，默认为 2，特殊情况可根据模块独立性调高）
   - 里程碑检查点（至少设置 2 个：所有基线测试完成、集成测试通过）
3. 为每个任务设置**进度警戒线**：
   - 计划耗时和计划完成度基线（按任务预估工时占总工时的百分比）。

### 4.4 看板初始化
**执行者**：PM

1. 创建或更新 `iterations/sprint-status.md`，使用模板 `templates/sprint-status-template.md`。
2. 将所有任务初始化为 `To Do` 状态。看板必须包含列：任务ID、描述、状态、负责人、计划工时、实际工时、风险标记、技术债务。

### 4.5 PM 自检与反向校验
**执行者**：PM

- [ ] 每个任务是否都满足原子化标准（≤1 天，输入输出明确）？
- [ ] 是否存在未解决的核心冲突？（若有则不能进入下一阶段，必须完成裁决）
- [ ] WIP 限制是否合理？
- [ ] 进度警戒线是否已设置？
- [ ] 看板与迭代计划是否一致？

## 5. 产出物
- `iterations/upgrade-sprint-YYYY-MM-DD.md`
- `iterations/sprint-status.md`（更新）

## 6. 阶段结束
- PM 向用户输出迭代计划摘要（任务总数、并行vs串行分布、里程碑），等待 `[Human Gate]` 审批。