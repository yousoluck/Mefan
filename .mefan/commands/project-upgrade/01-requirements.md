# /project-upgrade:01-requirements – 需求澄清与现有系统分析
## 0. 日志声明（自动追加
执行本阶段所有步骤时，必须使用 `.mefan/hooks/log-event.sh` 记录日志。
- 进入阶段时：`bash .mefan/hooks/log-event.sh <阶段> <Agent> "阶段进入" "进入阶段X" "" "成功"`
- 结束阶段时：`bash .mefan/hooks/log-event.sh <阶段> <Agent> "阶段退出" "阶段X完成" "" "成功"`
- 在 Human Gate 前后记录审批事件

## 1. 角色激活
- **主导 Agent**：分析师 (`agents/analyst.md`)。
- **监督 Agent**：项目经理 (`agents/pm.md`)，阶段末执行硬性审查。

## 2. 前置输入（必须读取，禁止凭记忆）
- `.mefan/iterations/{sprint-name}/session-status.md`
- `.mefan/context/tech-stack-profile.md`
- `.mefan/context/consistency-baseline.md`
- 知识图谱（通过 `graphify query` 使用，数据在 `graphify-out/`；若不可用，使用手动方式）

**前置检查**：
- 执行前确认上述 3 个文件存在，若任一不存在则报错退出。
- 若 `session-status.md` 不存在，报错："阶段 0 未完成或 session-status.md 缺失，请先执行 /project-upgrade:00-init"

## 3. 强制规则
- `.mefan/knowledge/scenario-upgrade/consistency-first.md`
- `.mefan/knowledge/scenario-upgrade/api-compatibility.md`
- `.mefan/knowledge/scenario-upgrade/reuse-before-build.md`
- `.mefan/knowledge/global/conflict-resolution.md`（如有）

## 4. 执行流程

### 4.1 需求访谈（分析师必须询问并记录）
分析师必须按序提出以下问题，不可跳过：
1. **功能目标**：用一句话描述用户故事："作为...，我想...，以便..."
2. **核心流程**：正常路径的步骤（1→2→3）。
3. **成功标准**：至少 3 个可定量验证的断言（如：调用 API 返回 200，响应时间 < 200ms）。
4. **边界清单**：明确本次*不做*的 3 件事。
5. **性能/安全/可观测性约束**：若有，需给出具体阈值或标准。

### 4.2 系统关联分析（按序执行，输出填入文档）
1. **相似功能**：`graphify query "find modules similar to <功能关键词>"`。若查询无结果，尝试使用 3 个同义词逐次查询，仍无结果则记录为"无直接相似模块"。
2. **可复用工具**：`graphify query "list reusable utilities for <领域>"`。若领域名词不明确，从 4.1 中提取 3 个候选关键字逐次尝试。
3. **受影响 API**：`graphify dependents <每个可能受影响的公开 API>`。
4. **冲突拓扑**：基于以上结果，绘制模块触达表，必须分类为：
   - 直接修改模块（至少 1 个具体文件路径）
   - 间接影响模块（至少 1 个具体文件路径）
   - 潜在冲突模块（至少 1 个，按 4.2.1 精确定义分类）

#### 4.2.1 冲突识别与升级
**执行者**：分析师

1. **识别冲突**：读取 `.mefan/iterations/{sprint-name}/session-status.md` 中的 backlog 条目和已有任务列表，与本需求的"触达模块"交叉比对。
   - 若任一模块已在 backlog 或其他任务中存在，记录为冲突。
   - **注意**：sprint-status.md 是阶段 3 产出，阶段 1 无法读取。冲突检查基于 session-status.md 中的 backlog。

2. **冲突分类**：
   - **核心冲突**：两个任务修改**同一文件的同一区域**（如同一函数的同一段逻辑），或修改有**直接依赖关系**的模块（如 A 模块调用 B 模块的同一接口）。
   - **边缘冲突**：两个任务修改**同一目录下的不同文件**，或修改**同一技术栈的相邻模块**但无直接调用关系。

3. **冲突处理决策树**：
   - **边缘冲突**：在需求文档 3.3 节中标注冲突信息，通知 PM。PM 决定是否需调整任务顺序，无需暂停流程。
   - **核心冲突**：立即通知 PM，暂停当前需求的进一步文档化。PM 必须做出以下决策之一：
     a. **串行化**：标记为需串行的任务，暂停其中一个，待另一个完成后继续。
     b. **分模块**：将冲突任务拆分为更小的子任务，使其不再交叉。
     c. **人类裁决**：若 PM 无法通过 a 或 b 解决，生成《冲突裁决申请书》，列出冲突双方和 PM 分析，提交人类决策。
   - PM 做出决策后，分析师根据决策结果继续或暂停工作。

4. **升级记录**：若产生核心冲突，PM 在 `.mefan/iterations/{sprint-name}/session-status.md` 的"异常记录"段追加：
   - 冲突描述：[任务 A] vs [任务 B] 在 [模块/文件] 上的核心冲突
   - 处理方式：[串行化 / 分模块 / 人类裁决]
   - 决策结果：[具体描述]
   - 决议时间：YYYY-MM-DD

### 4.3 命名与组织约定提取
从至少 **2 个不同文件**中提取以下证据：
- Action 类型定义位置（如 `src/constants/actionTypes.ts`）
- 枚举 vs 常量使用规则
- API 路径命名规则
- 组件/服务命名规则
每条约定必须附带：**规则描述 + 证据文件路径**。若项目该类约定不明确，如实记录"未发现一致约定"，不可伪造。

### 4.4 测试影响评估
1. 搜索 `**/__tests__/`, `*.test.*`, `*.spec.*` 中包含受影响模块名的文件。
2. 输出受影响的现有测试文件清单（完整路径）。
3. 判断需要新增的测试类型及数量。
4. **若搜索结果为零**：在需求文档测试章节显式标注"**高风险：无现有测试覆盖**"，并在 4.5 输出时同步提醒架构师需在阶段 2 制定基线测试方案。

### 4.5 输出需求文档
**目录检查**：确保 `.mefan/iterations/{sprint-name}/requirements/` 目录存在，若不存在则创建。
严格按照 `.mefan/templates/requirements-template.md` 填写，所有必填项不可留空。执行反向校验。

## 5. 产出物
- `.mefan/iterations/{sprint-name}/requirements/upgrade-YYYY-MM-DD-title.md`

## 6. 项目经理硬性审查（逐项打钩）
- [ ] 冲突拓扑是否分类完整且附具体模块名？核心/边缘分类是否准确？
- [ ] 验收标准是否全部可测试（非模糊描述）？
- [ ] 命名约定是否引用至少 **2 个不同文件**的代码位置？
- [ ] 测试影响是否给出了具体文件路径？若无测试，是否标注"高风险"？
- [ ] 需求文档是否反向引用了 `tech-stack-profile.md` 和 `consistency-baseline.md`？
- [ ] 若有核心冲突，是否已完成升级决策并记录在 session-status.md？
**任一项未通过，打回要求补充。通过后提交 `[Human Gate]`。**

## 7. 本阶段产出物清单（供后续依赖检查）

| 文件名 | 完整路径 | 模板 | 被依赖阶段 |
|--------|----------|------|-----------|
| requirements/*.md | `.mefan/iterations/{sprint-name}/requirements/upgrade-YYYY-MM-DD-title.md` | `.mefan/templates/requirements-template.md` | 02-arch-qa (§2), 03-plan (§2), 05-quality (§2) |