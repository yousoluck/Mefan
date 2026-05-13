# /project-upgrade:00-init – 会话初始化与上下文建立

## 1. 角色激活
- **主导 Agent**：项目经理 (`agents/pm.md`)，执行阶段 0 环境初始化。
- **辅助 Agent**：架构师 (`agents/architect.md`)，执行技术栈与基线分析。

## 2. 强制加载的规则（不可跳过）
- `knowledge/global/session-init.md`
- `knowledge/scenario-upgrade/consistency-first.md`
- `knowledge/scenario-upgrade/api-compatibility.md`

## 3. 执行流程（必须按序完成）

### 3.1 环境确认
**执行者**：项目经理
1. 确认 `SCENARIO=upgrade`。
2. 执行 `graphify update`（若未安装，标记“图谱待安装”，跳过此步，后续阶段以手动方式补充）。
3. 检查是否存在 `session-status.md`，若不存在则创建空白文件。

### 3.2 技术栈与一致性基线分析
**执行者**：架构师

#### 3.2.1 技术栈分析
- 扫描项目根目录的依赖描述文件（`package.json`, `pom.xml`, `requirements.txt`, `build.gradle` 等）。
- **若发现依赖文件**：提取前端框架、状态管理、后端框架、数据库、中间件及版本号。
- **若未发现任何依赖文件**：
  1. 向用户询问项目类型和技术栈信息（前端框架、后端框架、数据库）。
  2. 在 `tech-stack-profile.md` 中标注 **“人工补充”**，并逐条记录用户提供的技术栈。
- 输出 `context/tech-stack-profile.md`，使用模板 `templates/tech-stack-profile-template.md`。

#### 3.2.2 一致性基线提取
- 运行 `graphify query "most common patterns in the project"`。
- 运行 `graphify similar <核心模块名>` 提取高频设计模式。
- **若 graphify 查询失败（无结果、超时、未安装）**：
  1. 架构师手动扫描项目：打开 `src/` 下前 5 个高频目录，识别代码组织模式、命名规则、错误处理范式。
  2. 在 `consistency-baseline.md` 中标注 **“手动分析”**，并列出观察到的模式。
  3. 记录基线生成方式为“手动分析 + graphify（如可用）”。
- **若 graphify 查询成功**：正常提取至少 3 条可验证基线条目。
- **强制证据要求（无论何种方式）**：每条基线必须附带至少 1 条证据（文件路径 + 模式描述 或 graphify 节点名）。若无证据，该条目不得列入基线。
- 输出 `context/consistency-baseline.md`，使用模板 `templates/consistency-baseline-template.md`。

#### 3.2.3 依赖全景图
- 执行 `graphify dependents <核心模块>`，输出摘要追加到 `session-status.md` 的“依赖基础信息”段。
- **若 graphify 不可用**：在 `session-status.md` 中标注“**依赖全景图暂不可用，将在阶段 1 手动补充**”。

### 3.3 会话状态初始化
**执行者**：项目经理
1. 创建/更新 `iterations/session-status.md`，必须包含：
   - 当前迭代目标
   - 本次开发的 backlog 条目
   - 初步范围（模块清单）
   - 产出物追踪表（见下方模板）
2. 更新 `iterations/sprint-status.md` 看板，新增本次迭代列。

**产出物追踪表示例**：
| 产出物 | 路径 | 状态 | 校验结果 |
|--------|------|------|----------|
| tech-stack-profile.md | context/ | 已生成 | 待PM校验 |
| consistency-baseline.md | context/ | 已生成 | 待PM校验 |
| 依赖全景图 | session-status.md | 已生成/暂不可用 | 待PM校验 |

### 3.4 PM 对架构师输出的校验（新增）
**执行者**：项目经理

PM 在架构师完成 3.2 的所有产出后，必须执行以下校验：

#### 3.4.1 技术栈完整性校验
- [ ] 是否有前端框架记录？（若无，询问用户是否遗漏）
- [ ] 是否有后端框架记录？（若无，询问用户是否遗漏）
- [ ] 是否列出了所有主要直接依赖？（devDependencies 视项目类型而定，若不需则记录“N/A + 原因”）
- [ ] 若标注“人工补充”，用户提供的信息是否逐条记录并标记清楚？

#### 3.4.2 一致性基线有效性校验
- [ ] 每条基线是否至少有 1 条证据？
- [ ] 随机抽查 1-2 条证据中的文件路径：文件是否真实存在？（使用 `ls` 或文件查找验证）
- [ ] 基线条目是否可执行？（描述是否足够具体，可以直接作为阶段 4 开发者的检查标准？）

#### 3.4.3 校验结果处理
- **若全部通过**：更新 `session-status.md` 中的产出物追踪表（校验结果列标记为“通过”）。
- **若任一项未通过**：
  1. PM 列出未通过项，生成“校验失败通知”。
  2. 架构师根据通知修正产出物。
  3. PM 重新执行 3.4 校验，直至全部通过。

### 3.5 阶段结束
- 全部校验通过后，PM 向用户输出三句话摘要：技术栈组件数量、基线条目数和证据来源方式（手动/自动）、依赖全景图状态。
- 等待 `[Human Gate]` 确认后进入阶段 1。