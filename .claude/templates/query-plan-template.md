# Query Plan 模板

> **输出文件**：`.claude/context/query_plan.md`
> **生成者**：Architect Agent Stage 0 阶段 A
> **用途**：把 CB 章节 + Skills 的调查项翻译成可执行的 graphify query + bash fallback
> **生命周期**：阶段 A 生成 → 阶段 B 执行 → 阶段 C/D 引用 → 模板变更或 feature-elements 变更时重生成

---

## 文件结构

```markdown
# Query Plan

> 生成时间：{ISO timestamp}
> 生成者：Architect Agent Stage 0
> 项目：{project name}
> 目标产物：consistency-baseline.md + {N} 个 SKILL.md

---

## 1. 一致性基线调查项（CB 章节 → Query）

> **行粒度约定（2026-06-06 N-rows 重构）**：每个 CB 章节的 `questions: []` 列表里**每个问题对应 1 行**。`parent_section_id` 列引用一个真实章节（去掉 `_qN` 后缀即为章节 ID），`question_index` 是该章节内的 1-based 序号。
>
> 例：§1.1 有 4 个问题（name / version / frontend / backend），拆 4 行。§4.1 只有 1 个问题（ORM 基类位置），拆 1 行。

| 目标 ID | 章节 | 调查项 | Graphify Query | Bash Fallback | 期望结果 | 优先级 | **父章节 ID** | **问题序号** |
|---------|------|--------|---------------|---------------|---------|--------|---------------|--------------|
| cb_1_1_q1 | §1.1 项目元数据 | 项目名称 | `graphify query "project name"` | `grep -E '"name"' package.json pyproject.toml 2>/dev/null` | name 字段值 | P0 | cb_1_1 | 1 |
| cb_1_1_q2 | §1.1 项目元数据 | 项目版本 | `graphify query "project version"` | `grep -E '"version"' package.json pyproject.toml 2>/dev/null` | version 字段值 | P0 | cb_1_1 | 2 |
| cb_1_1_q3 | §1.1 项目元数据 | 前端框架 | `graphify query "frontend framework react vue angular"` | `grep -E '"(react\|vue\|angular\|svelte)"' package.json` | 框架名 + 版本 | P0 | cb_1_1 | 3 |
| cb_1_1_q4 | §1.1 项目元数据 | 后端框架 | `graphify query "backend framework fastapi django express"` | `grep -E '"(fastapi\|django\|flask\|express)"' pyproject.toml requirements.txt 2>/dev/null` | 框架名 + 版本 | P0 | cb_1_1 | 4 |
| cb_4_1_q1 | §4.1 数据库模型 | ORM 基类/模型位置 | `graphify query "ORM model base class"` | `grep -rn "class.*Base" --include="*.py"` | 文件:行号 + 类名 | P0 | cb_4_1 | 1 |
| cb_5_2_q1 | §5.2 Redux State | state 结构和组织 | `graphify query "redux state slice"` | `grep -rn "createSlice\|initialState" --include="*.ts"` | slice 名称 + state 形状 | P1 | cb_5_2 | 1 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

## 2. Skill 调查项（FE → Query）

> **行粒度约定（2026-06-06 N-rows 重构）**：1 个 FE = 1 行（保持 1:1，**不做 N×M 拆解**，避免 320+ 行爆炸）。`parent_section_id` = `target_id`，`question_index` = 1。
>
> 例：14 个 FE → 14 行；不再为"数据库"的"连接配置"和"事务处理"拆 2 行——这些细节在阶段 C 组装 SKILL.md 时由 `data.questions[0].data.chapters` 内部展开。

| 目标 ID | FE 来源 | 模板选择（三级回退） | Graphify Query | Bash Fallback | **Code Target** | 期望结果 | 优先级 | **父章节 ID** | **问题序号** |
|---------|---------|---------------------|---------------|---------------|-----------------|---------|--------|---------------|--------------|
| skill_infra_database | FE-I-001 | 一级：project-infra-database | `graphify query "database connection configuration"` | `grep -rn "create_engine\|DB_URL" --include="*.py"` | `src/db/config.py:15-25`, `src/db/session.py:30-45` | 配置位置 + 连接模式 | P0 | skill_infra_database | 1 |
| skill_infra_cache | FE-I-002 | 一级：project-infra-cache | `graphify query "cache configuration redis"` | `grep -rn "Redis\|cache" --include="*.py"` | *(空)* | 缓存类型 + 失效策略 | P0 | skill_infra_cache | 1 |
| skill_domain_user | FE-D-001 | 二级：project-domain-generic | `graphify query "user entity domain model"` | `grep -rn "class User\b" --include="*.py"` | `src/models/user.py:1-50` | 实体字段 + 业务方法 | P1 | skill_domain_user | 1 |
| skill_service_auth | FE-A-001 | 二级：project-service-generic | `graphify query "authentication service"` | `grep -rn "def login\|def authenticate" --include="*.py"` | `src/services/auth.py:1-40` | 服务方法 + 调用链 | P1 | skill_service_auth | 1 |
| skill_api_user | FE-F-001 | 二级：project-api-generic | `graphify query "user API endpoint"` | `grep -rn "user.*router\|/api/user" --include="*.py"` | `src/api/user.py:1-50` | 端点 + 请求/响应 schema | P1 | skill_api_user | 1 |
| skill_ui_button | FE-F-002 | 二级：project-ui-generic | `graphify query "button component react"` | `grep -rn "function Button\|const Button" --include="*.tsx"` | `src/components/Button.tsx:1-40` | Props + 状态 + 事件 | P2 | skill_ui_button | 1 |
| skill_feature_checkout | BS-001 | 二级：project-feature-generic | `graphify path "Checkout" "Payment"` | `grep -rn "checkout\|def pay" --include="*.py"` | *(空)* | 流程节点 + 集成关系 | P1 | skill_feature_checkout | 1 |
| skill_framework_react | framework (frontend) | 三级：skill-template | `graphify query "React component patterns"` | `grep "react" package.json` | *(空)* | 框架版本 + 关键模式 | P2 | skill_framework_react | 1 |

### 2.1 Code Target 提取规则（精炼阶段 2026-06-06 新增）

> **目的**：让 `architect-stage0` 阶段 B 不仅返回 `path:line` 元数据，还能**真实提取源码内容**写入 `examples.md`（Pattern C 顶层 companion）。

**格式**：逗号分隔的 `path:line-line` 列表：
- 单点：`src/db/config.py:15-25`
- 多点：`src/db/config.py:15-25`, `src/db/session.py:30-45`
- 单行：`src/db/config.py:15`（等价于 `15-15`）
- 留空：*(空)* 或 `-` → 该调查点不提取代码

**填充规则**（模板作者）：
1. 优先填**该调查点最可能命中的源码位置**（基于领域知识）
2. 单点 ≤ 30 行（避免 SKILL.md 臃肿）
3. 不确定的点**留空**（让 AI 在运行时尝试）
4. 不填虚拟路径（如 `src/foo.py:1-100`）—— graphify 跑时找不到会失败

**提取规则**（arch-stage0 阶段 B 执行）：
1. 解析 `path:line-line`，用 `sed -n` 从 `$ROOT/{path}` 提取源码
2. 软失败：文件不存在 → 标 `[SNIPPET_FETCH_FAILED: file not found]`
3. 软失败：行范围为空 → 标 `[SNIPPET_FETCH_FAILED: empty range]`
4. 单 snippet > 100 行 → 截断并标 `[TRUNCATED]`
5. 单 skill snippets 总和 > 500 行 → 截断最末几个 snippet
6. snippet 缺失**不阻塞** pipeline，examples.md 对应位置标 `[需人工补充]`

**Schema 影响**：
- `results-json-schema.md` 的 `skill` 类型新增 `snippets: { [path:line-line: string]: string }` 字段
- 阶段 C 2.6.4 根据 snippets 是否非空决定 Pattern A → C 自动升级

## 3. PM context 文档调查项（PM-Stage0 用）

> **新增章节（2026-06-05 模式 C 重构）**：PM-Stage0 生成 3 份 context 文档（project.md / tech-stack-profile.md / feature-elements.md）时的 query 计划。与第 1、2 节的区别：**目标 ID 前缀为 `doc_`**、**多 1 列 `doc_type`** 区分 3 类文档。
>
> **行粒度约定（2026-06-06 N-rows 重构）**：
> - **`doc_project_s_*` 和 `doc_tech_s_*` 章节**：每个调查项的每个子问题拆 1 行（如 §1 项目介绍有 3 个子问题：name/type/description → 3 行）
> - **`doc_feature_s_*` 章节**：1 个 FE/章节 = 1 行（**保持 1:1**，避免 N×M 爆炸；FE 内的元数据字段通过 1 个 graphify query 整体拿）
> - `parent_section_id` = 去掉 `_qN` 后缀的 ID；`question_index` = 章节内 1-based 序号

| 目标 ID | 章节 | 调查项 | Graphify Query | Bash Fallback | 期望结果 | 优先级 | **doc_type** | **父章节 ID** | **问题序号** |
|---------|------|--------|---------------|---------------|---------|--------|--------------|---------------|--------------|
| doc_project_s_1_1_q1 | §1 项目总体介绍 | 项目名称 | `graphify query "project name"` | `grep -E '"name"' package.json pyproject.toml 2>/dev/null` | name 字段值 | P0 | `project` | doc_project_s_1_1 | 1 |
| doc_project_s_1_1_q2 | §1 项目总体介绍 | 项目类型/分类 | `graphify query "project type category"` | `grep -E '"(type\|category\|description)"' package.json pyproject.toml 2>/dev/null` | type + category 字段 | P0 | `project` | doc_project_s_1_1 | 2 |
| doc_project_s_1_1_q3 | §1 项目总体介绍 | 核心功能概述 | `graphify query "project core features description"` | `cat README.md 2>/dev/null \| head -50` | 一段功能描述 | P1 | `project` | doc_project_s_1_1 | 3 |
| doc_project_s_4_1_q1 | §4 前端 | 前端语言 | `graphify query "frontend language typescript javascript"` | `grep -E '"(typescript\|javascript)"' package.json` | TS / JS | P0 | `project` | doc_project_s_4_1 | 1 |
| doc_project_s_4_1_q2 | §4 前端 | 前端框架 | `graphify query "frontend framework react vue angular"` | `grep -E '"(react\|vue\|angular\|svelte)"' package.json` | 框架名 + 版本 | P0 | `project` | doc_project_s_4_1 | 2 |
| doc_project_s_4_1_q3 | §4 前端 | 构建工具 | `graphify query "build tool vite webpack"` | `grep -E '"(vite\|webpack\|rollup\|esbuild)"' package.json` | 构建工具 + 版本 | P1 | `project` | doc_project_s_4_1 | 3 |
| doc_tech_s_2_1_q1 | §2.1 核心框架（前端） | 框架名 | `graphify query "React Vue Angular frontend framework"` | `grep -E '"(react\|vue\|angular)"' package.json` | 框架名 | P0 | `tech_stack` | doc_tech_s_2_1 | 1 |
| doc_tech_s_2_1_q2 | §2.1 核心框架（前端） | 框架版本 | `graphify query "framework version"` | `grep -E '"(react\|vue\|angular)":' package.json \| grep -oE '"[0-9.]+"'` | 版本号 | P0 | `tech_stack` | doc_tech_s_2_1 | 2 |
| doc_tech_s_2_1_q3 | §2.1 核心框架（前端） | 框架用途/角色 | `graphify query "framework usage role"` | n/a | 一句话说明 | P1 | `tech_stack` | doc_tech_s_2_1 | 3 |
| doc_tech_s_2_2_q1 | §2.2 中间件（后端） | CORS 中间件 | `graphify query "CORS middleware"` | `grep -rn "cors" --include="*.py" --include="*.ts"` | 中间件名 + 配置 | P1 | `tech_stack` | doc_tech_s_2_2 | 1 |
| doc_tech_s_2_2_q2 | §2.2 中间件（后端） | Helmet 安全头 | `graphify query "helmet security headers"` | `grep -rn "helmet" --include="*.py" --include="*.ts"` | helmet + 配置 | P1 | `tech_stack` | doc_tech_s_2_2 | 2 |
| doc_tech_s_2_2_q3 | §2.2 中间件（后端） | Compression 压缩 | `graphify query "compression middleware"` | `grep -rn "compression" --include="*.py" --include="*.ts"` | compression + 配置 | P2 | `tech_stack` | doc_tech_s_2_2 | 3 |
| doc_tech_s_4_q1 | §4 DevOps 与基础设施 | Docker 容器化 | `graphify query "Docker container"` | `ls Dockerfile docker-compose.yml 2>/dev/null` | 工具 + 文件 | P1 | `tech_stack` | doc_tech_s_4 | 1 |
| doc_tech_s_4_q2 | §4 DevOps 与基础设施 | CI/CD 平台 | `graphify query "CI CD platform"` | `ls .github/workflows .gitlab-ci.yml 2>/dev/null` | 平台 + 工作流 | P1 | `tech_stack` | doc_tech_s_4 | 2 |
| doc_tech_s_4_q3 | §4 DevOps 与基础设施 | 监控/日志 | `graphify query "monitoring logging"` | `grep -rn "sentry\|prometheus\|datadog" --include="*.py" --include="*.ts"` | 工具名 | P2 | `tech_stack` | doc_tech_s_4 | 3 |
| doc_tech_s_5_q1 | §5 测试技术栈 | 单元测试框架 | `graphify query "unit test framework"` | `grep -E "pytest\|jest\|vitest" requirements.txt package.json` | 框架名 | P1 | `tech_stack` | doc_tech_s_5 | 1 |
| doc_tech_s_5_q2 | §5 测试技术栈 | E2E 测试框架 | `graphify query "e2e test framework"` | `grep -E "playwright\|cypress\|selenium" requirements.txt package.json` | 框架名 | P1 | `tech_stack` | doc_tech_s_5 | 2 |
| doc_tech_s_5_q3 | §5 测试技术栈 | 覆盖率工具 | `graphify query "test coverage tool"` | `grep -E "coverage\|c8\|istanbul" requirements.txt package.json` | 工具名 | P2 | `tech_stack` | doc_tech_s_5 | 3 |
| doc_feature_s_3_1_q1 | §3.1 L1 基础设施 | 数据库/缓存/MQ 实际技术 | `graphify query "database cache message queue"` | `grep -E "postgres\|mysql\|redis\|rabbitmq\|kafka" requirements.txt` | 实际技术栈 + 配置文件位置 | P0 | `feature_elements` | doc_feature_s_3_1 | 1 |
| doc_feature_s_3_2_q1 | §3.2 L2 领域 | 业务实体/聚合根 | `graphify query "domain entity aggregate root"` | `grep -rn "class.*Entity\|class.*Aggregate" --include="*.py"` | 实体类 + 文件:行号 | P1 | `feature_elements` | doc_feature_s_3_2 | 1 |
| doc_feature_s_4_1_q1 | §4.1 L1 详情 | FE-I-001~008 详情表 | （从 §3.1 衍生，每 FE 一个 sub-query） | （按 FE 类别 grep） | Element ID + 描述 + 文件位置 | P1 | `feature_elements` | doc_feature_s_4_1 | 1 |
| doc_feature_s_5_q1 | §5 依赖关系矩阵 | FE 间 uses 关系 | `graphify path "FE-D-001" "FE-I-001"` | 手动 + 模板 | 矩阵 | P2 | `feature_elements` | doc_feature_s_5 | 1 |
| doc_feature_s_6_q1 | §6 Graphify 查询模板 | 11 个查询示例 | （纯文本块，引用模板） | n/a | 完整 11 条 query | P2 | `feature_elements` | doc_feature_s_6 | 1 |
| doc_feature_s_7_q1 | §7 L5 业务场景识别流程 | 流程图 + 用户访谈 | `graphify query "business scenario end to end workflow"` | n/a | 流程 + 场景清单 | P2 | `feature_elements` | doc_feature_s_7 | 1 |

**doc_type 取值**：
- `project` — `.claude/context/project.md`（项目元信息，~112 行模板）
- `tech_stack` — `.claude/context/tech-stack-profile.md`（技术栈档案，~184 行模板）
- `feature_elements` — `.claude/context/feature-elements.md`（功能元素清单 L1-L5，~360 行模板）

## 4. 降级策略表

| Graphify 失败原因 | Bash Fallback 模板 | 二次降级 |
|-------------------|-------------------|----------|
| 返回 0 节点 | `grep -rn "<key_concept>" --include="*.{py,ts,js,go,rs,java}" .` | grep 也无果 → 标 `[NO_DATA]` |
| 节点太多（>50） | `grep -rn "<key_concept>" --include="*.{ext}" . \| head -20` | 取前 20 条 |
| 词表无匹配 token | 跳过 graphify，直接 bash | bash 也失败 → 标 `[NO_DATA]` |
| graph.json 不存在 | 提示用户先跑 `/graphify .` | 不再降级 |

## 5. 验证清单

- [ ] CB 章节覆盖率 ≥ 80%（17+ 章中至少 14 章有对应 query）
- [ ] Skills 覆盖率 100%（feature-elements.md 中所有 FE 都有 query）
- [ ] PM context 文档覆盖率：3 份文档（project / tech_stack / feature_elements）每份章节 ≥ 80%
- [ ] 每个 query 都有 bash fallback
- [ ] 期望结果明确可验证
- [ ] 优先级标注（P0/P1/P2）
- [ ] **Code Target 列填写规范**（逗号分隔 `path:line-line`；不填虚拟路径；详见 §2.1）
- [ ] **doc_type 列填写正确**（`project` / `tech_stack` / `feature_elements` 三选一）
- [ ] **每行必须有 `parent_section_id` 列**，引用一个真实存在的章节 ID（去掉 `_qN` 后缀）
- [ ] **`question_index` 列从 1 开始、章节内连续递增**（同 `parent_section_id` 下不重复）
- [ ] **行粒度符合约定**：CB / project / tech 章节按 question 拆 N 行；Skill / feature_elements 1 FE = 1 行（见 §1/§2/§3 开头说明）

## 6. 重生成触发条件

以下任一情况触发重生成：
- consistency-baseline-template.md 结构变更
- feature-elements.md L1-L5 元素变更
- Skill 模板新增/删除
- **project-template.md / tech-stack-profile-template.md / feature-elements-template.md 章节变更（PM-Stage0 用）**
- **schema 版本不匹配**（`results-json-schema.md` 头部声明的 SCHEMA_VERSION 与 query_plan.md 头部声明的版本对不上时强制重生成；2026-06-06 引入 SCHEMA_VERSION 字段，从 `2.0.0` 升到 `2.1.0` 以反映 N-rows 重构）
- 用户明确请求
```

---

## 列说明

| 列 | 含义 | 取值约束 |
|----|------|---------|
| 目标 ID | 唯一标识，用于 results.json 关联 | `cb_{section}_q{N}` / `skill_{type}_{name}_q{N}` / `doc_{type}_s{section}_q{N}`；**N-rows 重构（2026-06-06）后必带 `_qN` 后缀** |
| 章节 | CB 模板中的章节号 / FE 编号 | §1.1、FE-I-001 等 |
| 调查项 | 该 question 要回答的具体子问题 | 中文短句（**每行 1 个原子问题**） |
| Graphify Query | 必须先走词表扩展再执行的 query | `graphify query "..."` |
| Bash Fallback | graphify 失败时执行的 grep/find | 真实可执行的 shell 命令 |
| 期望结果 | 该 query 应该返回的内容 | 用于阶段 B 验证 |
| 优先级 | P0=核心、P1=重要、P2=可选 | 单字符 |
| 模板选择 | 三级回退中的一级、二级、三级 | 标注"一级/二级/三级"（仅 Skill 行用） |
| **Code Target** | **代码片段提取目标（仅 Skill 行用）** | **逗号分隔的 `path:line-line`；空 = 不提取；详见 §2.1** |
| **doc_type** | **PM 上下文文档类型（仅 PM 上下文行用）** | **`project` / `tech_stack` / `feature_elements`** |
| **父章节 ID** | **该行归属的章节 ID（去掉 `_qN` 后缀）** | **`cb_1_1` / `skill_xxx` / `doc_xxx`；必须等于一个真实存在的章节 ID；N-rows 重构（2026-06-06）新增列** |
| **问题序号** | **该 question 在父章节内的 1-based 序号** | **正整数；同 `parent_section_id` 下从 1 开始连续递增** |

---

## 使用流程

```
1. AI 读取 consistency-baseline-template.md
   → 解析每个 ### 章节的 YAML 调查项
   → **对每个章节的 questions: [] 列表的每个 question 填 1 行 cb_{section}_q{N} 记录**（N-rows 重构）
   → 同一章节的 N 行共享 parent_section_id = cb_{section}

2. AI 读取 feature-elements.md
   → 遍历所有 FE-I-* / FE-D-* / FE-A-* / FE-F-* / BS-*
   → 为每个 FE 选模板（三级回退）
   → **1 FE = 1 行**（保持 1:1，不展开字段；parent_section_id = target_id）

3. **AI 读取 3 个 PM context 模板（PM-Stage0 专属）**
   → 读 project-template.md → **对每个章节的每个 question 填 1 行 doc_project_s_{section}_q{N}**
   → 读 tech-stack-profile-template.md → **同 project 模式**
   → 读 feature-elements-template.md → **1 FE/章节 = 1 行**（保持 1:1，避免 N×M 爆炸）
   → 每行 doc_type 标注正确

4. AI 输出 query_plan.md（路径 .claude/context/query_plan.md）
   → 头部声明 `SCHEMA_VERSION: 2.1.0`（N-rows 重构后版本）

5. Human Gate：PM 审查覆盖率与 fallback 合理性

6. 进入阶段 B 执行
```

---

## 与其他文件的关系

- **输入**：
  - `.claude/templates/consistency-baseline-template.md`（CB 章节来源，architect-stage0 用）
  - `.claude/skills/_templates/**/*.md`（Skill 模板来源，architect-stage0 用）
  - `.claude/context/feature-elements.md`（FE 列表来源，architect-stage0 用）
  - `.claude/templates/project-template.md`（PM-Stage0 用，新增 2026-06-05）
  - `.claude/templates/tech-stack-profile-template.md`（PM-Stage0 用，新增 2026-06-05）
  - `.claude/templates/feature-elements-template.md`（PM-Stage0 用，新增 2026-06-05）
  - `.claude/templates/query-dsl-cheatsheet.md`（query 设计参考）
- **输出**：
  - `.claude/context/results.json`（阶段 B 产物）
- **被引用**：
  - 阶段 C（Skills 生成，arch-stage0）
  - 阶段 D（CB 生成，arch-stage0）
  - **PM-Stage0 阶段 C（project/tech_stack/feature_elements 3 份 context 文档 AI 组装，新增 2026-06-05）**
