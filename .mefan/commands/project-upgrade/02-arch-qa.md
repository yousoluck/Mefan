# /project-upgrade:02-arch-qa – 架构设计与测试策略
## 0. 日志声明（自动追加
执行本阶段所有步骤时，必须使用 `.mefan/hooks/log-event.sh` 记录日志。
- 进入阶段时：`bash .mefan/hooks/log-event.sh <阶段> <Agent> "阶段进入" "进入阶段X" "" "成功"`
- 结束阶段时：`bash .mefan/hooks/log-event.sh <阶段> <Agent> "阶段退出" "阶段X完成" "" "成功"`
- 在 Human Gate 前后记录审批事件

## 1. 角色激活
- **主导 Agent**：架构师 (`agents/architect.md`)，负责技术方案和详细设计。
- **辅助 Agent**：QA 工程师 (`agents/qa.md`)，负责测试策略与测试计划。
- **监督 Agent**：PM (`agents/pm.md`)，阶段末执行硬性审查。

## 2. 前置输入（必须读取）
- `.mefan/iterations/{sprint-name}/requirements/upgrade-YYYY-MM-DD-title.md`
- `.mefan/context/tech-stack-profile.md`
- `.mefan/context/consistency-baseline.md`
- 知识图谱（`.mefan/graphify-out/`，若不可用则以手动方式补充）

**前置检查**：执行前确认上述文件存在，若不存在则报错退出。

## 3. 强制规则
- `.mefan/knowledge/scenario-upgrade/consistency-first.md`
- `.mefan/knowledge/scenario-upgrade/api-compatibility.md`
- `.mefan/knowledge/scenario-upgrade/reuse-before-build.md`
- `.mefan/knowledge/global/conflict-resolution.md`（设计冲突升级用）
- `.mefan/knowledge/global/exception-handling.md`（如有）

## 4. 执行流程

### 4.1 架构方案设计
**执行者**：架构师

1. **方案对比**：
   - 至少提供两个方案，方案一必须最大化复用现有代码/模式。
   - 对比维度：复用度、复杂度、风险、开发成本、对上游影响。
   - 输出到 ADR 方案对比表。

2. **详细设计**：
   - 新文件/类/服务的目录位置（必须与一致性基线中的目录结构一致）。
   - 接口签名：API 路径、HTTP 方法、请求体/响应体结构、错误码（遵循项目现有风格）。
   - 数据流：新模块与现有模块的数据交互序列（可文字描述或序列图）。
   - 数据库变更（若有）：表结构、索引、迁移脚本。
   - 设计模式：显式声明用了项目中的哪个现有模式，引用 `.mefan/context/consistency-baseline.md` 中的条目。

3. **参考实现**：
   - 使用 `graphify similar <关键模块名>` 找到相似模块，列出至少 2 个可参考的文件路径和关键函数。
   - 若 graphify 不可用，手动扫描 `src/` 中近似功能模块。

4. **一致性合规声明**：
   - 检查设计方案是否违反一致性基线中的任何条规则。
   - 若完全遵循：声明"**遵循一致性基线**"。
   - 若有意突破：必须详细说明理由，并提交 **"一致性基线修正提案"**（草稿），写入 ADR。
   - **若架构师无法判断是否冲突**：上升为设计冲突，启动冲突升级（见 4.3）。

5. **API 变更合规性**：
   - 列出所有新增 API（路径、方法、参数、返回）。
   - 列出被标记为 `@deprecated` 的 API 及替代方案。
   - 确认无修改公共 API 签名，若有必须重新审视设计。

### 4.2 测试策略设计
**执行者**：QA 工程师

1. **回归测试范围**：
   - 基于需求文档中的测试影响评估，列出必须回归的测试套件清单（具体文件路径）。
   - 若需求文档标注"无现有测试"，QA 必须规划 **基线测试套件** 的编写方案。

2. **新增测试场景**：
   - 功能测试用例：正常路径、边界值、异常输入。
   - 集成测试用例：新 API 与上下游的交互。
   - 非功能测试：性能基准对比测试（若需求有性能约束）、安全扫描范围。

3. **质量门槛**：
   - 单元测试覆盖率不低于项目现有水平（从 project-config 或全局 quality-gates 读取，若无则默认 ≥80%）。
   - 集成测试必须覆盖所有新增 API 的正常与异常路径。
   - 回归测试必须 100% 通过。
   - 性能退化不允许超过基线值的 10%。

4. **人工测试指南需求**：
   - 若涉及前端 UI 或无法自动化的场景，QA 标记需要编写人工测试指南，指明范围。

### 4.3 设计冲突处理流程（若发生）
**触发条件**：架构师发现设计方案无法同时满足需求与一致性基线，或与当前 iteration 中其他任务产生核心模块冲突。

**处理步骤**：
1. 架构师将冲突写入 ADR 的"设计冲突声明"章节，说明冲突原因和备选方案。
2. PM 读取冲突声明，尝试通过调整设计（如切换备选方案）解决。
3. 若 PM 无法裁定，生成《设计冲突裁决申请书》提交人类决策。
4. 记录冲突和决议到 `.mefan/iterations/{sprint-name}/session-status.md` 的异常记录。

## 5. 产出物
**目录检查**：确保以下目录存在，若不存在则创建：
- `.mefan/iterations/{sprint-name}/adr/`
- `.mefan/iterations/{sprint-name}/test-plan/`

| 产出物 | 路径 | 模板 |
|--------|------|------|
| adr/*.md | `.mefan/iterations/{sprint-name}/adr/upgrade-YYYY-MM-DD-title.md` | `.mefan/templates/adr-template.md` |
| test-plan/*.md | `.mefan/iterations/{sprint-name}/test-plan/upgrade-YYYY-MM-DD-title.md` | `.mefan/templates/test-plan-template.md` |

## 6. PM 硬性审查（逐项打钩）
- [ ] ADR 是否包含至少两个方案的对比？
- [ ] 详细设计是否给出了目录位置和接口签名？
- [ ] 是否声明了一致性合规状态（遵循/突破并附理由）？
- [ ] 是否提供了至少 2 个参考实现文件路径？
- [ ] 测试计划是否列出具体回归测试文件路径？
- [ ] 质量门槛是否明确（覆盖率、性能基线）？
- [ ] 若有设计冲突，是否已记录并启动升级？
**任一项未通过，打回。通过后提交 `[Human Gate]`。**

## 7. 本阶段产出物清单（供后续依赖检查）

| 文件名 | 完整路径 | 模板 | 被依赖阶段 |
|--------|----------|------|-----------|
| adr/*.md | `.mefan/iterations/{sprint-name}/adr/upgrade-YYYY-MM-DD-title.md` | `.mefan/templates/adr-template.md` | 03-plan (§2), 04-implement (§2) |
| test-plan/*.md | `.mefan/iterations/{sprint-name}/test-plan/upgrade-YYYY-MM-DD-title.md` | `.mefan/templates/test-plan-template.md` | 03-plan (§2), 05-quality (§2) |