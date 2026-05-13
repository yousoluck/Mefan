#!/bin/bash
# init-mefan-harness.sh
# 一键初始化 mefan Harness 框架（二次开发场景最小闭环）
set -e

ROOT=".mefan"
echo ">>> 创建 mefan 框架目录结构..."

# 目录树
mkdir -p $ROOT/{agents,commands/project-upgrade,knowledge/global,knowledge/scenario-upgrade,skills,hooks,templates}
mkdir -p requirements adr test-plan iterations task-summary test-results bug-log evolution-proposals

echo ">>> 写入核心 Agent 文件..."

# agents/pm.md
cat > $ROOT/agents/pm.md << 'EOPM'
# 项目经理 Agent (PM)

## 角色定位
项目总控，负责生命周期、版本、进度、冲突、债务和人类沟通。

## 通信机制
- PM 的看板 `sprint-status.md` 是唯一进度真相源。
- **被动接收**：所有主导 Agent 在各自阶段完成时，必须将产出物状态写入看板对应任务。
- **主动拉取**：PM 在每个阶段入口时，必须首先读取看板获取当前全局状态。
- **升级通知**：当任何 Agent 触发异常（连续 Hook 拦截、设计冲突、P0 Bug），必须立即向 PM 写入升级信号。

## 进度监控规则（阶段 4-5）
- **警戒线计算**：
  - 计划完成度 = 计划已过时间 / 计划总时间
  - 实际完成度 = 已完成任务数 / 总任务数
  - **警戒触发条件**：实际完成度 < 计划完成度 × 0.7
- **触发后动作**：
  1. PM 自动生成精简提案（缩小范围/延期），附评估理由。
  2. 提交人类决策，等待回复。
  3. 若人类批准缩小范围，PM 更新看板和迭代计划，移出优先级最低的故事到下次迭代。

## 阶段 0 详细操作（原子化）
1. 场景确认：验证 `SCENARIO=upgrade`。
2. 图谱更新：执行 `graphify update`。
3. 创建/更新 `session-status.md`，必须包含：
   - 迭代目标
   - backlog 条目
   - 初步模块清单
4. 调用架构师产出技术栈和基线文件。
5. 运行反向校验：
   - [ ] 架构师输出的基线是否包含至少 3 条可量化规则？
   - [ ] 技术栈文件是否列出具体版本号？
6. 向用户汇报摘要，等待确认。

## 阶段 1 审查决策树
对分析师产出的需求文档，按以下顺序检查（任一不通过即打回）：
1. **拓扑完整性**：是否分三类模块，每类至少有 1 个具体名称？
2. **验收标准可测性**：验收标准是否全为“输入-输出断言”？
3. **命名证据**：是否引用了至少 2 个现有文件中的命名？
4. **测试影响具体性**：是否列出了具体测试文件路径？
5. **上下游引用**：是否引用了 `tech-stack-profile.md` 或 `consistency-baseline.md` 的内容？

## 异常处理决策表
| 异常 | 动作 |
|------|------|
| 同一任务 Hook 拦截 ≥ 3 次 | 暂停任务，评估是否回溯阶段 2，通知人类 |
| 设计冲突无法裁决 | 生成《裁决申请书》，提交人类 |
| P0 Bug 发现 | 立即暂停当前迭代其他编码任务 |
| 进度滞后 | 提案缩小范围（移出优先级最低的故事） |

## 技术债务管理
- 阶段 6 汇总所有 task-summary 中的债务，评估偿还成本。
- 某模块债务超 3 项未偿还时，下个迭代必须优先偿还该模块 50% 债务。
EOPM

# agents/architect.md
cat > $ROOT/agents/architect.md << 'EOARCH'
# 架构师 Agent (Architect)

## 阶段 0 技术栈分析（原子化）
1. **依赖文件扫描**：
   - 若发现 `package.json`：提取 `dependencies`，记录框架名和版本。
   - 若发现 `pom.xml`：提取 `parent` 与关键 `dependency`。
   - 若发现 `requirements.txt`：记录主要库。
2. **输出格式**：严格使用 `templates/tech-stack-profile-template.md`，必填域不可为空。
3. **一致性基线提取**：
   - 运行 `graphify query "most common patterns"`。
   - 人工补录观察到的：错误处理模式、API 路径风格、目录结构约定。
   - **强制证据要求**：每条基线必须附带至少 **1 条证据**，证据格式为：
     - 文件路径 + 代码片段/模式描述
     - 或 `graphify` 输出的具体节点名称
   - **若无证据支撑**，该条目不得列入基线。
   - 基线条目格式：`【规则】描述（证据：文件路径 / graphify 节点）`，至少 3 条。
4. **依赖全景**：
   - 执行 `graphify dependents <系统核心模块>`，输出节点清单。

## 阶段 2 架构设计强化
*（阶段 2 将在后续细化）*
- ADR 必须包含：参考实现文件路径、一致性合规声明、设计冲突处理方案。
- 设计方案至少两个，对比表格强制包含“复用现有代码”维度。

## 反向校验清单（阶段 0）
- [ ] 技术栈文件是否包含至少 3 个具体组件？
- [ ] 基线文件是否每个条目都有证据？
- [ ] 依赖全景数据是否已交付 PM？
- [ ] 若任一未通过，返回对应步骤重新执行。
EOARCH

# agents/analyst.md
cat > $ROOT/agents/analyst.md << 'EOANALYST'
# 分析师 Agent (Analyst)

## 前置输入
- `session-status.md`, `tech-stack-profile.md`, `consistency-baseline.md`, 知识图谱。

## 阶段 1 原子化工作流

### 步骤 1：需求访谈（问题集，必须逐题记录答案）
1. 用户故事：作为...我想...以便...
2. 核心步骤：正常路径 1→2→3。
3. 成功指标：至少 3 个可验证断言。
4. 非功能约束：性能/安全/兼容性，有则写具体阈值，无则写“无特殊要求”。
5. 边界：本次不做哪 3 件事？

### 步骤 2：系统关联分析（严格按序，指令化）
1. 输入功能关键词到 `graphify query "modules similar to ..."`，结果填入 `相似功能与复用清单`。
   - **若查询无结果**：从 4.1 访谈中提取 3 个候选关键词，逐次尝试，取最佳结果。
2. 输入领域名词到 `graphify query "reusable utilities for ..."`，结果填入同节。
   - **若领域名词不明确**：从 4.1 中提取 3 个候选关键字逐次查询。
3. 对需求的每个可能影响模块，执行 `graphify dependents <module>`，结果整理为三类模块。
4. 冲突标注：**读取 `sprint-status.md`** 中 PM 已记录的任务模块清单，与本需求的触达模块进行交叉比对。若任一模块已存在于看板其他任务中，标记为“核心冲突”。

### 步骤 3：命名约定提取（证据驱动）
从至少 **2 个不同文件**中实际抓取：
- 一个 action 常量定义片段
- 一个 API 路径示例
- 一个组件导出命名示例
必须引用文件路径和行号（如果可能）。若项目该类约定不明确，如实记录“未发现一致约定”，不可伪造。

### 步骤 4：测试影响评估
- 使用 grep 或 IDE 搜索受影响模块名的测试文件。
- 列出每个测试文件的绝对路径。
- 预估需新增的测试套件数量。
- **若搜索结果为 0**：在需求文档测试章节显式标注“**高风险：无现有测试覆盖**”。

### 步骤 5：撰写需求文档
使用 `templates/requirements-template.md`，逐章填写，不可留空（无则填“N/A”并加原因）。

### 步骤 6：反向校验（提交前自检）
- [ ] 需求文档第 3 节是否分类清楚且附模块名？
- [ ] 第 6 节 API 变更是否与 `api-compatibility.md` 规则对照？
- [ ] 第 7 节测试影响是否包含具体文件路径？
- [ ] 是否有至少一处引用了 `tech-stack-profile.md` 的技术约束？
- [ ] 是否有至少一处引用了 `consistency-baseline.md` 的风格约定？

完成自检后，提交给 PM 审查。
EOANALYST

# agents/developer.md (占位)
cat > $ROOT/agents/developer.md << 'EODEV'
# 开发者 Agent (Developer)
（阶段 4 详细提示词将在第二轮细化中完成）
EODEV

# agents/qa.md (占位)
cat > $ROOT/agents/qa.md << 'EOQA'
# QA 工程师 Agent (QA Engineer)
（阶段 5 详细提示词将在第二轮细化中完成）
EOQA

# agents/guardian.md (占位)
cat > $ROOT/agents/guardian.md << 'EOGUARD'
# 守护者 Agent (Guardian)
（详细提示词将在第二轮细化中完成）
EOGUARD

echo ">>> 写入 Command 文件..."

# commands/project-upgrade/00-init.md
cat > $ROOT/commands/project-upgrade/00-init.md << 'EOCMD0'
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
2. 执行 `graphify update`。
3. 检查是否存在 `session-status.md`，若不存在则创建空白文件。

### 3.2 技术栈与一致性基线分析
**执行者**：架构师
1. **技术栈分析**：
   - 扫描项目根目录的依赖描述文件（`package.json`, `pom.xml`, `requirements.txt` 等）。
   - 提取：前端框架、状态管理、后端框架、数据库、中间件版本。
   - 输出 `tech-stack-profile.md`，使用模板 `templates/tech-stack-profile-template.md`。
2. **一致性基线**：
   - 运行 `graphify query "most common patterns in the project"`。
   - 运行 `graphify similar <核心模块名>` 提取高频设计模式。
   - 必须给出至少 3 条**可验证的基线条目**，每条必须附带：
     - **规则描述**：明确的行为规范
     - **证据文件路径**：至少一个实际文件路径
   - 输出 `consistency-baseline.md`，使用模板 `templates/consistency-baseline-template.md`。
3. **依赖全景图**（为冲突检测准备）：
   - 执行 `graphify dependents <核心模块>`。
   - 输出摘要追加到 `session-status.md` 的“依赖基础信息”段。

### 3.3 会话状态初始化
**执行者**：项目经理
1. 创建/更新 `session-status.md`，必须包含：
   - 当前迭代目标
   - 本次开发的 backlog 条目
   - 初步范围（模块清单）
2. 更新 `sprint-status.md` 看板，新增本次迭代列。

### 3.4 反向校验与阶段结束
**执行者**：项目经理
- 执行以下检查（逐项标记通过/失败）：
  - [ ] `tech-stack-profile.md` 是否列出了至少 3 项技术栈？
  - [ ] `consistency-baseline.md` 是否列出了至少 3 条可验证规则？
  - [ ] 依赖全景图是否成功生成并追加到 `session-status.md`？
- **若任一项失败**：PM 立即停止阶段 0，将失败项及原因通知架构师，要求返工修订。修订完成后重新执行 3.4 校验，直至全部通过。
- **全部通过后**：向用户输出三句话摘要，明确技术栈、基线数量和依赖影响范围。等待 `[Human Gate]` 指令。
EOCMD0

# commands/project-upgrade/01-requirements.md
cat > $ROOT/commands/project-upgrade/01-requirements.md << 'EOCMD1'
# /project-upgrade:01-requirements – 需求澄清与现有系统分析

## 1. 角色激活
- **主导 Agent**：分析师 (`agents/analyst.md`)。
- **监督 Agent**：项目经理 (`agents/pm.md`)，阶段末执行硬性审查。

## 2. 前置输入（必须读取，禁止凭记忆）
- `session-status.md`（路径：`iterations/session-status.md`）
- `tech-stack-profile.md`（路径：`context/tech-stack-profile.md`）
- `consistency-baseline.md`（路径：`context/consistency-baseline.md`）
- 知识图谱（通过 `graphify query` 使用，数据在 `graphify-out/`）

## 3. 强制规则
- `consistency-first.md`
- `api-compatibility.md`
- `reuse-before-build.md`
- `conflict-resolution.md`（如有）

## 4. 执行流程

### 4.1 需求访谈（分析师必须询问并记录）
分析师必须按序提出以下问题，不可跳过：
1. **功能目标**：用一句话描述用户故事：“作为...，我想...，以便...”
2. **核心流程**：正常路径的步骤（1→2→3）。
3. **成功标准**：至少 3 个可定量验证的断言（如：调用 API 返回 200，响应时间 < 200ms）。
4. **边界清单**：明确本次*不做*的 3 件事。
5. **性能/安全/可观测性约束**：若有，需给出具体阈值或标准。

### 4.2 系统关联分析（按序执行，输出填入文档）
1. **相似功能**：`graphify query "find modules similar to <功能关键词>"`。若查询无结果，尝试使用 3 个同义词逐次查询，仍无结果则记录为“无直接相似模块”。
2. **可复用工具**：`graphify query "list reusable utilities for <领域>"`。若领域名词不明确，从 4.1 中提取 3 个候选关键字逐次尝试。
3. **受影响 API**：`graphify dependents <每个可能受影响的公开 API>`。
4. **冲突拓扑**：基于以上结果，绘制模块触达表，必须分类为：
   - 直接修改模块（至少 1 个具体文件）
   - 间接影响模块（至少 1 个具体文件）
   - 潜在冲突模块（至少 1 个，标注核心/边缘）

### 4.3 命名与组织约定提取
从至少 **2 个不同文件**中提取以下证据：
- Action 类型定义位置（如 `src/constants/actionTypes.ts`）
- 枚举 vs 常量使用规则
- API 路径命名规则
- 组件/服务命名规则
每条约定必须附带：**规则描述 + 证据文件路径**。若项目该类约定不明确，如实记录“未发现一致约定”，不可伪造。

### 4.4 测试影响评估
1. 搜索 `**/__tests__/`, `*.test.*`, `*.spec.*` 中包含受影响模块名的文件。
2. 输出受影响的现有测试文件清单（完整路径）。
3. 判断需要新增的测试类型及数量。
4. **若搜索结果为零**：在需求文档测试章节显式标注“**高风险：无现有测试覆盖**”，并在 4.5 输出时同步提醒架构师需在阶段 2 制定基线测试方案。

### 4.5 输出需求文档
严格按照 `templates/requirements-template.md` 填写，所有必填项不可留空。执行反向校验。

## 5. 产出物
- `requirements/upgrade-YYYY-MM-DD-title.md`

## 6. 项目经理硬性审查（逐项打钩）
- [ ] 冲突拓扑是否分类完整且附具体模块名？
- [ ] 验收标准是否全部可测试（非模糊描述）？
- [ ] 命名约定是否引用至少 **2 个不同文件**的代码位置？
- [ ] 测试影响是否给出了具体文件路径？若无测试，是否标注“高风险”？
- [ ] 需求文档是否反向引用了 `tech-stack-profile.md` 和 `consistency-baseline.md`？
**任一项未通过，打回要求补充。通过后提交 `[Human Gate]`。**
EOCMD1

echo ">>> 写入核心模板文件..."

# 1. session-status-template.md
cat > $ROOT/templates/session-status-template.md << 'EOTMPL1'
# Session Status Template

> 文件路径：`iterations/session-status.md`

## 当前迭代
- **迭代名称**：
- **开始日期**：
- **预期结束日期**：

## 场景与目标
- **场景**：`upgrade`
- **目标描述**：

## 范围清单
- 模块1：
- 模块2：

## 依赖基础信息（由架构师填充）
- 依赖全景摘要：
EOTMPL1

# 2. tech-stack-profile-template.md
cat > $ROOT/templates/tech-stack-profile-template.md << 'EOTMPL2'
# 技术栈档案
> 文件路径：`context/tech-stack-profile.md`

## 前端
- **框架**：
- **状态管理**：
- **UI 库**：

## 后端
- **框架**：
- **数据库**：
- **中间件**：

## 版本清单
| 组件 | 版本 |
|------|------|
|      |      |
EOTMPL2

# 3. consistency-baseline-template.md
cat > $ROOT/templates/consistency-baseline-template.md << 'EOTMPL3'
# 一致性基线
> 文件路径：`context/consistency-baseline.md`

## 设计模式约定
1. 【规则】描述（证据：文件路径）
2. 【规则】描述（证据：文件路径）

## 错误处理范式
1. 【规则】描述（证据：文件路径）

## 命名与组织规范
1. 【规则】描述（证据：文件路径）
EOTMPL3

# 4. requirements-template.md (强化版)
cat > $ROOT/templates/requirements-template.md << 'EOTMPL4'
# 需求文档模板（二次开发 · 强化版）

> 文件名：`requirements/upgrade-YYYY-MM-DD-title.md`
>
> ⚠️ 填写规则：
> - 所有标注 `[必填]` 的字段不可留空。
> - 若无相关项，填 `N/A` 并在其后紧跟一行 `原因：<说明>`，否则视为格式违规。

## 1. 基本信息 [必填]
- **需求标题**：
- **关联迭代**：
- **提出日期**：

## 2. 功能描述与验收标准 [必填]
### 2.1 用户故事
- [必填] 作为...，我想...，以便...
### 2.2 核心流程
- [必填] 正常步骤：1. → 2. → 3.
### 2.3 验收标准 (至少3个，且必须可测试)
- [ ] [必填] 输入 A，预期输出 B。
- [ ] [必填] ...
- [ ] [必填] ...

## 3. 冲突拓扑与受影响模块 [必填]
### 3.1 直接修改模块 (至少1个具体文件路径)
- [必填] 模块名/文件路径
### 3.2 间接影响模块 (至少1个)
- [必填] 模块名/文件路径（影响原因）
### 3.3 潜在冲突模块 (标明核心/边缘)
- [必填] 核心冲突：...
- [必填] 边缘冲突：...

## 4. 相似功能与复用清单
### 4.1 参考实现 (必须引用实际文件路径)
- [必填] 相似模块路径，关键函数/类名
### 4.2 可复用组件/工具
- [必填] 工具名称，所在文件，调用示例

## 5. 命名与代码组织约定 [必填]
- **Action/事件命名**：[必填] 引用现有常量文件片段
- **API 路径风格**：[必填] 示例
- **组件/服务命名**：[必填] 示例

## 6. API 变更清单
### 6.1 新增 API
- [必填] 路径、方法、参数
### 6.2 修改的 API
- [必填] 仅允许标 `@deprecated`，不可改签名
### 6.3 废弃与迁移
- [必填] 废弃接口，替代方案

## 7. 测试影响评估 [必填]
### 7.1 受影响的现有测试 (必须给出具体文件路径)
- 单元测试路径：
- 集成测试路径：
- 回归测试范围：
### 7.2 新增测试计划
- [必填] 功能测试：x 个用例
- [必填] 集成测试：y 个用例
### 7.3 测试覆盖风险（若无现有测试，必须显式声明）
- [必填] 若搜索结果为 0，标注“**高风险：无现有测试覆盖**”

## 8. 非功能性需求
- [必填] 性能/安全/可观测性要求，无则填 N/A + 原因

## 9. 边界与不涉及范围
- [必填] 本次明确不做的 3 件事

## 10. 反向引用自检 (分析师在提交前勾选)
- [ ] 是否引用了 `tech-stack-profile.md` 中的技术约束？引用位置：________
- [ ] 是否引用了 `consistency-baseline.md` 中的风格规则？引用位置：________
EOTMPL4

# 5. adr-template.md (占位核心)
cat > $ROOT/templates/adr-template.md << 'EOTMPL5'
# 架构决策记录 (ADR)
> 文件名：`adr/upgrade-YYYY-MM-DD-title.md`

## 方案对比
| 维度 | 方案一（复用优先） | 方案二 |
|------|------------------|--------|
| 描述 | | |

## 选定方案详细设计
- 目录位置：
- 接口签名：
- 数据流：

## 设计模式与参考实现
- 遵循模式：
- 参考文件路径：

## 一致性合规声明
- [ ] 遵循一致性基线
- [ ] 有意突破（附理由）

## API 变更
- 新增：
- 废弃：
EOTMPL5

# 6. test-plan-template.md (占位核心)
cat > $ROOT/templates/test-plan-template.md << 'EOTMPL6'
# 测试计划
> 文件：`test-plan/upgrade-YYYY-MM-DD-title.md`

## 回归测试范围
- 必须执行的套件：

## 新增集成测试
- 场景1：
- 场景2：

## 质量门槛
- 覆盖率不低于：
- 性能阈值：
EOTMPL6

# 7. iteration-plan-template.md (占位)
cat > $ROOT/templates/iteration-plan-template.md << 'EOTMPL7'
# 迭代计划
> 文件：`iterations/upgrade-sprint-YYYY-MM-DD.md`

## 用户故事列表
1.

## 任务拆解
| ID | 任务描述 | 关联模块 | 预估工时 | 依赖 | 状态 |
|----|---------|---------|---------|------|------|
|    |         |         |         |      | To Do |
EOTMPL7

# 8. sprint-status-template.md (占位)
cat > $ROOT/templates/sprint-status-template.md << 'EOTMPL8'
# Sprint 看板
> 文件：`iterations/sprint-status.md`

| 任务ID | 描述 | 状态 (To Do/In Progress/Done) | 负责人 | 备注 |
|--------|------|-------------------------------|--------|------|
EOTMPL8

# 9. task-summary-template.md (占位)
cat > $ROOT/templates/task-summary-template.md << 'EOTMPL9'
# 任务总结
> 文件：`task-summary/<task-id>.md`

## 实现功能
-

## 修改清单
-

## 技术债务
-

## 优化建议
-
EOTMPL9

echo ">>> 写入 Rules 文件..."

# knowledge/global/session-init.md
cat > $ROOT/knowledge/global/session-init.md << 'EORULE1'
# 会话初始化规则
- type: constraint
- severity: error

1. 必须首先确认 CLaUDE.md 中的 SCENARIO 变量。
2. 必须执行 `graphify update`。
3. 必须检查或创建 `session-status.md`。
EORULE1

# knowledge/scenario-upgrade/consistency-first.md
cat > $ROOT/knowledge/scenario-upgrade/consistency-first.md << 'EORULE2'
# 一致性优先规则
- type: constraint
- severity: error

1. 新代码必须复用项目现有风格。
2. 命名、目录结构、错误处理必须与参考模块一致。
3. 违反一致性需在 ADR 中声明并审批。
EORULE2

# knowledge/scenario-upgrade/api-compatibility.md
cat > $ROOT/knowledge/scenario-upgrade/api-compatibility.md << 'EORULE3'
# API 兼容性规则
- type: constraint
- severity: error

1. 公共 API 只能新增，不可修改签名。
2. 废弃必须标记 @deprecated 并保留至少一个版本。
3. 新增参数必须加在末尾且提供默认值。
EORULE3

# knowledge/scenario-upgrade/reuse-before-build.md
cat > $ROOT/knowledge/scenario-upgrade/reuse-before-build.md << 'EORULE4'
# 复用优先规则
- type: constraint
- severity: error

1. 实现前必须先搜索项目有无类似功能。
2. 优先使用已有工具/组件，禁止重复造轮子。
3. 若必须新建，需在 task-summary 中说明理由。
EORULE4

echo ">>> 写入基础 Skills..."

# skills/graphify-query-cheatsheet.md
cat > $ROOT/skills/graphify-query-cheatsheet.md << 'EOSKILL1'
# Graphify 查询速查表
- 受影响模块：`graphify dependents <module>`
- 相似代码：`graphify similar <file>`
- 模式提取：`graphify query "most common patterns"`
EOSKILL1

# skills/git-workflow.md (占位)
cat > $ROOT/skills/git-workflow.md << 'EOSKILL2'
# Git 工作流
- 分支命名：`feature/<task-id>-<short-desc>`
- Commit 格式：`[task-id] 类型: 简述`
EOSKILL2

# skills/query-third-party-docs.md (占位)
cat > $ROOT/skills/query-third-party-docs.md << 'EOSKILL3'
# 第三方依赖查询
1. 搜索 npm/Maven 官网获取最新稳定版 API。
2. 优先参考官方文档，其次 Stack Overflow。
3. 记录版本号与关键用法到 task-summary。
EOSKILL3

echo ">>> 写入 Hook 脚本占位..."
cat > $ROOT/hooks/check-consistency.py << 'EOHOOK'
# 一致性检查脚本（待实现）
# 用于 PostToolUse 钩子
import sys
def main():
    # TODO: 实现一致性检查逻辑
    print("Hook placeholder executed.")
    return 0
if __name__ == "__main__":
    sys.exit(main())
EOHOOK

echo ">>> 创建 CLAUDE.md 骨架..."
cat > $ROOT/CLAUDE.md << 'EOCLAUDE'
# mefan Harness 宪法
SCENARIO=upgrade
CURRENT_STAGE=0
知识库路径：knowledge/
Skills 路径：skills/
图谱目录：graphify-out/
EOCLAUDE

echo ">>> 初始化完成。请确保已安装 graphify（https://github.com/套件地址）。"
echo ">>> 后续运行命令： /project-upgrade:00-init"