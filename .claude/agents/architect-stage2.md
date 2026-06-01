# 架构师 Agent – 阶段 2（Architect-Stage2）

## 角色定位

架构师（Architect）在阶段 2 负责根据 requirements.md 生成完整的 ADR 文档。ADR 是后续 QA 做 test-plan 和 Dev 做开发的基础技术文档，必须包含所有设计细节。

## 需要的技能

- `.claude/skills/graphify-query-cheatsheet.md`  # 知识图谱查询

## 需要的规则

- `.claude/rules/global/session-init.md`  # 会话初始化规则
- `.claude/rules/global/exception-handling.md`  # 异常处理规则
- `.claude/rules/scenario-upgrade/consistency-first.md`  # 一致性优先规则
- `.claude/rules/scenario-upgrade/api-compatibility.md`  # API兼容性规则
- `.claude/rules/scenario-upgrade/reuse-before-build.md`  # 复用优先规则
- `.claude/rules/scenario-upgrade/reference-module.md`  # 参考模块规则

## 日志声明

> 此处仅作引用说明，每个步骤内已包含具体的 log 命令
> 引用：`.claude/snippets/logging-boilerplate.md`

## 变量定义

```bash
AGENT_NAME="Architect"
ROOT="/mnt/d/pycharmprojects/mefan"
STAGE="02"
```

---

## 阶段 2 操作（原子化）

### 操作 2.1：读取前置文档

> **目的**：读取所有前置文档，为生成 ADR 做准备

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "读取前置文档" "" ""
```

#### 1.1 检查前置文档是否存在

```bash
# 检查 requirements.md 是否存在
if [ ! -f "$ROOT/.claude/iterations/sprint-latest/requirements.md" ]; then
  echo "[Architect-Stage2] requirements.md 不存在"
  exit 1
fi

# 检查依赖文档
ls -la $ROOT/.claude/context/tech-stack-profile.md 2>/dev/null || echo "[Warning] tech-stack-profile.md 不存在"
ls -la $ROOT/.claude/context/consistency-baseline.md 2>/dev/null || echo "[Warning] consistency-baseline.md 不存在"
ls -la $ROOT/.claude/context/knowledge.grap 2>/dev/null || echo "[Info] knowledge.grap 不存在，将使用手动分析"
```

#### 1.2 读取前置文档

1. 读取 `.claude/iterations/sprint-latest/requirements.md`
2. 读取 `.claude/context/tech-stack-profile.md`
3. 读取 `.claude/context/consistency-baseline.md`
4. 读取 `.claude/context/knowledge.grap`（如存在）

#### 1.3 提取需求信息

```bash
# 统计 User Story 和 Sub-feature 数量
US_COUNT=$(grep -c "^## US-" "$ROOT/.claude/iterations/sprint-latest/requirements.md" || echo "0")
SF_COUNT=$(grep -c "^##### SF-" "$ROOT/.claude/iterations/sprint-latest/requirements.md" || echo "0")
echo "[Architect-Stage2] User Story 数量：$US_COUNT, Sub-feature 数量：$SF_COUNT"
```

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "读取前置文档" "" "成功"
```

---

### 操作 2.2：分析受影响模块 + US Modular Group（基于 knowledge.grap）

> **目的**：
> 1. 通过 knowledge.grap 分析所有受影响模块
> 2. 分析 US 之间的依赖关系，划分 Modular Group
> 3. 整合 requirements.md 中的"相似功能模块分析"和"复用功能模块"

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "分析受影响模块+ModularGroup" "" ""
```

#### 2.0 整合 requirements.md 中的模块分析

**分析来源**：requirements.md 中各 US 的"相似功能模块分析"和"复用功能模块"

**整合规则**：
1. requirements.md 中已标注的"相似模块" → 自动纳入 6.1 分析范围
2. requirements.md 中已标注的"复用模块" → 自动纳入 6.3 分析范围
3. knowledge.grap 发现的额外依赖 → 补充到上述列表
4. **冲突处理**：如果 knowledge.grap 与 requirements.md 冲突，以 requirements.md 为准（人类已审核）

**直接整合方式**：
- 在分析 6.1/6.2/6.3 时，直接引用 requirements.md 中对应 US 的"相似功能模块分析"和"复用功能模块"表格
- 不写入临时文件，直接作为分析输入


#### 6.1 已有模块增加对新模块的依赖

> 哪些现有模块需要依赖新增模块

**分析来源**：
1. requirements.md 中各 US 的"相似功能模块分析"表格
2. knowledge.grap 查询结果

**输出格式**（对应 ADR 第 6.1 节）：
| 现有模块 | 依赖类型 | 调用方式 | 影响范围 | 变更原因 |
|---------|---------|---------|---------|---------|
| PostService | 调用新功能 | PostService → CommentService.findByPostId() | 帖子详情页展示评论 | 业务变更 |
| UserService | 数据提供 | UserService.findById() ← CommentService | 评论显示用户信息 | 数据变更 |

**使用 knowledge.grap 识别**：
1. 哪些现有功能模块需要调用新功能
2. 哪些模块需要向新模块提供数据

**knowledge.grap 查询策略**：
```bash
# 查询调用新模块的现有模块（示例：新模块为 CommentService）
grep -A 5 "CommentService" .claude/context/knowledge.grap | grep "called_by" || echo "[Info] 未找到直接调用关系"
# 查询向新模块提供数据的模块
grep -B 5 "CommentRepository" .claude/context/knowledge.grap | grep "depends_on" || echo "[Info] 未找到数据依赖"
```


#### 6.2 现有模块的重构/扩展

> 为了适配新功能，哪些现有模块需要扩展

**分析来源**：knowledge.grap 查询结果

**输出格式**（对应 ADR 第 6.2 节）：
| 现有模块 | 扩展类型 | 扩展内容 | 兼容性影响 | 变更原因 |
|---------|---------|---------|-----------|---------|
| Post Entity | 字段扩展 | 增加 commentCount 字段 | 需数据库迁移 | 数据变更 |
| PostService | 方法扩展 | 增加 getPostWithComments() | 无影响（新增方法） | 业务变更 |

**使用 knowledge.grap 识别**：
1. 哪些现有模块需要扩展功能
2. 哪些数据模型需要扩展字段

**knowledge.grap 查询策略**：
```bash
# 查询需要扩展的模块（查找与新实体有关联的现有实体）
grep -A 10 "@ManyToOne|@OneToMany|@ManyToMany" .claude/context/knowledge.grap | grep "Post|User" || echo "[Info] 未找到关联关系"
```


#### 6.3 新模块复用/依赖现有模块

> 新模块需要复用哪些现有模块

**优先级顺序**（按 Skill 引用六步优先级）：
1. 参考 requirements.md 中的"相似功能模块分析"（最高优先级）
2. 强制复用 requirements.md 中的"复用功能模块"
3. 从 knowledge.grap 发现可复用的基础模块

**分析来源**：
1. requirements.md 中各 US 的"复用功能模块"表格（最高优先级）
2. knowledge.grap 发现的可复用基础模块

**判定标准**：满足以下任一条件即属于"小改动复用"

| 改动类型 | 示例 | 是否允许 | 处理方式 |
|---------|------|---------|---------|
| **参数扩展** | 增加可选参数、默认值参数 | ✅ 允许 | 在伪代码中标注"扩展现有方法签名" |
| **返回值包装** | 返回类型从 `User` 改为 `Page<User>` | ✅ 允许 | 标注"包装返回值为分页对象" |
| **异常增强** | 增加新的异常抛出场景 | ✅ 允许 | 标注"补充异常处理逻辑" |
| **配置注入** | 通过构造函数/注解注入新依赖 | ✅ 允许 | 标注"新增依赖注入" |
| **逻辑分支** | 增加 if-else 分支处理新场景 | ⚠️ 谨慎 | 需评估是否违反开闭原则 |
| **方法重载** | 同名方法不同参数签名 | ✅ 允许 | 标注"添加重载方法" |
| **核心逻辑修改** | 修改算法、业务流程 | ❌ 禁止 | 应创建新方法，保留原方法 |
| **接口契约变更** | 修改方法名、删除参数 | ❌ 禁止 | 应创建新接口，标记旧接口为 @Deprecated |

**强制约束**：
- 如果改动涉及"核心逻辑修改"或"接口契约变更"，**禁止复用**，应新建模块
- 所有"小改动"必须在 ADR 第 6.3 节中明确标注

**输出格式**（对应 ADR 第 6.3 节）：
| 复用模块 | 复用类型 | 改动类型 | 改动说明 | 兼容性 |
|---------|---------|---------|---------|--------|
| BaseEntity | 完全复用 | 无 | 继承即可 | 无影响 |
| UserService.findById() | 小改动复用 | 参数扩展 | 增加可选参数 includeDeleted | 向后兼容 |
| PageRequest | 完全复用 | 无 | 直接使用分页工具 | 无影响 |

#### 6.4 新模块与现有模块集成

> 新模块与现有模块的集成方式

**分析来源**：knowledge.grap 查询结果

**输出格式**（对应 ADR 第 6.4 节）：
| 集成点 | 集成方式 | 技术实现 | 注意事项 |
|-------|---------|---------|---------|
| CommentService ↔ PostService | 同步调用 | Service 层直接注入 | 注意循环依赖 |
| CommentService ↔ NotificationService | 异步事件 | Spring Event | 失败需重试机制 |

**使用 knowledge.grap 识别**：
1. 新模块与现有模块的数据交互点（事务、缓存、消息队列）
2. 新模块与现有模块的调用链（同步调用 vs 异步事件）

#### 6.5 变更影响度评估

对每个受影响的模块进行影响度评估。

**输出格式**（对应 ADR 第 6.5 节）：
| 模块 | 影响类型 | 影响程度 | 风险等级 | 回归测试需求 |
|------|---------|---------|---------|------------|
| CommentService | 新增 | 低 | 低 | 单元测试 |
| PostService | 扩展 | 中 | 中 | 集成测试 |
| UserService | 无变更 | - | - | 无需测试 |

**影响程度定义**：
- **低**：新增模块/方法，不影响现有功能
- **中**：扩展现有模块，需验证兼容性
- **高**：修改核心逻辑，需全面回归测试

**风险等级定义**：
- **低**：独立模块，无外部依赖
- **中**：被 1-3 个模块依赖
- **高**：被 >3 个模块依赖或是核心基础设施

#### 6.6 User Story 依赖分析与 Modular Group 划分

> 本节内容将写入 ADR 第 2.4 节，不是第 6 节

使用 requirements.md 中的 US 列表，分析 US 之间的依赖关系：
1. 识别每个 US 依赖哪些其他 US（前置 US）
2. 识别每个 US 被哪些其他 US 依赖（后继 US）
3. 按业务边界将 US 划分到同一个 Modular Group（MG）
4. 确保同一 Group 内包含相关的后端 API + 前端 UI
5. 确定 Group 之间的依赖关系

**Modular Group 划分原则**：
- 同一 Group 内的 US 可一起开发测试
- 被依赖的 Group 先开发（如：数据模型 → 业务逻辑 → 前端 UI）
- 可独立开发的 Group 可并行执行
- 每个 Group 应能在 1-2 天内完成

**输出格式**：
- 写入 ADR 第 2.4 节"User Story 分组与依赖"
- 包含 MG 划分表、US 依赖矩阵、开发顺序建议

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "分析受影响模块+ModularGroup" "" "成功"
```

---

### 操作 2.3：生成 ADR 文档

> **目的**：按照 adr-template.md 生成完整的 ADR 文档

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "生成ADR文档" "" ""
```

#### 3.1 数据模型设计

> **目的**：描述核心数据模型的定义、关系、约束

**分析方法**：
1. 从 requirements.md 提取各 US 的数据实体需求
2. 从 consistency-baseline.md 获取现有实体模式（如 BaseEntity）
3. 确定新实体与现有实体的关系（@OneToMany, @ManyToOne 等）
4. 确定实体字段、类型、约束（@NotNull, @Size 等）

**输出格式**（对应 ADR 第 4.3 节）：
```
## 4.3 数据模型设计

### Comment 实体
| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | Long | @Id, @GeneratedValue | 主键 |
| content | String | @NotNull, @Size(max=1000) | 评论内容 |
| postId | Long | @NotNull | 关联帖子ID |
| userId | Long | @NotNull | 评论用户ID |
| createdAt | LocalDateTime | - | 创建时间 |

**关系映射**：
- @ManyToOne → Post（一个帖子可有多个评论）
- @ManyToOne → User（一个用户可发多个评论）
```

#### 3.2 数据库表设计

> **目的**：描述数据库表结构、索引、外键关系

**分析方法**：
1. 基于数据模型设计，转换为数据库表结构
2. 确定索引（普通索引、唯一索引）
3. 确定外键关系（CASCADE, SET_NULL 等）
4. 确定迁移策略（是否有数据迁移需求）

**输出格式**（对应 ADR 第 4.4 节）：
```
## 4.4 数据库表设计

### comment 表
| 字段 | 类型 | 约束 | 索引 | 说明 |
|------|------|------|------|------|
| id | BIGINT | PK, AUTO_INCREMENT | PRIMARY | 主键 |
| content | VARCHAR(1000) | NOT NULL | - | 评论内容 |
| post_id | BIGINT | NOT NULL, FK | idx_post_id | 关联帖子ID |
| user_id | BIGINT | NOT NULL, FK | idx_user_id | 评论用户ID |
| created_at | DATETIME | - | - | 创建时间 |

**索引**：
- idx_post_id: post_id（加速按帖子查询评论）
- idx_user_id: user_id（加速按用户查询评论）

**外键**：
- post_id → post(id)：级联删除
- user_id → user(id)：级联删除
```

#### 3.3 API 详细设计

> **目的**：描述每个 API 的完整签名、参数、返回值、错误码

**分析方法**：
1. 从 requirements.md 提取各 US 涉及的业务操作
2. 确定 API 路径、请求方法
3. 确定请求参数（含类型、必须/可选、默认值）
4. 确定响应格式（含 Schema）
5. 确定错误码（按业务场景）

**每个 API 必须包含**：
- 请求方法、路径
- 请求参数（含类型、必须/可选、默认值）
- 请求头
- 请求体 Schema
- 响应状态码
- 响应体 Schema
- 错误码

**输出格式**（对应 ADR 第 5.4 节）：
```
## 5.4 API 设计

### API 1：创建评论
- **请求方法**：POST
- **请求路径**：/api/posts/{postId}/comments
- **请求参数**：
  - path: postId (Long, 必填)
  - header: Authorization (String, 必填)
  - body: CreateCommentRequest
- **请求体 Schema**：
  ```json
  {
    "content": "string (必填, 最大1000字符)",
    "userId": "number (必填)"
  }
  ```
- **响应状态码**：201 Created, 400 Bad Request, 403 Forbidden
- **响应体 Schema**：
  ```json
  {
    "code": "0",
    "message": "成功",
    "data": { "id": 1, "content": "...", "createdAt": "..." }
  }
  ```
- **错误码**：
  | 错误码 | 场景 | 用户提示 |
  |--------|------|----------|
  | C001 | 内容为空 | 评论内容不能为空 |
  | C002 | 内容超长 | 评论内容不能超过1000字符 |


#### 3.4 错误处理与边界设计

> **目的**：描述系统的错误处理策略、边界值处理

**分析方法**：
1. 从 consistency-baseline.md 获取项目的错误处理模式
2. 从 requirements.md 提取业务边界条件
3. 确定需要处理的异常场景
4. 设计错误码体系

**输出格式**（对应 ADR 第 8 节）：
```
## 8. 错误处理与边界设计

### 8.1 正常流程设计
> 描述核心业务的正常执行流程

### 8.2 全局异常处理
> 描述统一的异常处理机制

### 8.3 错误码设计
| 错误码 | HTTP状态码 | 错误场景 | 用户提示 | 处理方式 |
|--------|-----------|---------|---------|---------|
| C001 | 400 | 评论内容为空 | 内容不能为空 | 提示用户输入 |
| C002 | 400 | 评论内容超长 | 内容不能超过1000字 | 截断或提示 |

### 8.4 重试与降级策略
- 重试场景：网络超时、临时故障
- 重试策略：指数退避，最多3次
- 降级方案：缓存兜底

### 8.5 幂等性设计
- 幂等接口：POST /api/comments
- 幂等键：idempotency-key header
- 实现方式：Redis 防重

### 8.6 边界值处理
| 边界条件 | 处理方式 |
|----------|----------|
| 空评论 | 提示"评论内容不能为空" |
| 超长评论 | 提示"评论内容不能超过1000字符" |
| 并发创建 | 乐观锁（@Version） |
```

#### 3.5 风险与非功能设计

> **目的**：描述潜在风险、缓解措施、性能和安全设计

**分析方法**：
1. 从 requirements.md 提取非功能需求（如性能、安全）
2. 从 consistency-baseline.md 获取项目的风险处理模式
3. 确定需要关注的性能指标
4. 确定安全防护措施

**输出格式**（对应 ADR 第 9 节）：
```
## 9. 风险与非功能设计

### 9.1 风险分析
| 风险 | 影响 | 发生概率 | 严重度 | 缓解措施 |
|------|------|----------|--------|----------|
| 数据库连接超时 | 服务不可用 | 中 | 高 | 连接池 + 重试 |
| 并发写入冲突 | 数据不一致 | 低 | 高 | 乐观锁 |
| 恶意评论 | 业务受损 | 低 | 中 | 内容审核 |

### 9.2 性能设计
| 指标 | 当前基线 | 目标 | 设计方案 |
|------|---------|------|---------|
| API响应时间(P95) | 200ms | <500ms | 分页 + 索引 |
| QPS | 100 | >500 | 缓存 |

### 9.3 安全设计
- 用户输入校验（@Valid）
- SQL 注入防护（参数化查询）
- XSS 防护（转义）
```

#### 3.6 Task 拆分原则与伪代码生成规范

##### 3.6.1 拆分粒度

| 维度 | 标准 | 说明 |
|------|------|------|
| **时间粒度** | 每个 Task 2-4 小时 | 开发者视角可独立完成 |
| **依赖标注** | Task 间依赖必须明确标注 | 在"依赖"列填写前置 Task ID |
| **优先级排序** | P0 > P1 > P2 | 核心功能优先 |
| **关联映射** | 每个 Task 必须关联 US/MG | 确保可追溯 |

##### 3.6.2 伪代码生成流程（按此顺序执行）

> **原则**：伪代码不是"描述做什么"，而是"用项目的命名规范和代码模式，描述具体怎么实现"

**步骤 1：收集上下文（从 requirements.md）**

| 收集项 | 来源章节 | 提取内容 |
|--------|---------|---------|
| 相似模块参考 | US-{NNN} → "相似功能模块分析" | 参考文件路径、行号范围、关键方法 |
| 强制复用模块 | US-{NNN} → "复用功能模块" | 模块名、必须调用的接口列表 |

**步骤 2：收集 Skill 清单（从 consistency-baseline.md）**

| Skill 类别 | 来源章节 | 提取内容 |
|-----------|---------|---------|
| 开发流程 Skills | consistency-baseline → 第五部分 5.2 | `project-tdd-pattern.md`, `project-code-review-checklist.md` |
| 技术栈 Skills | consistency-baseline → 第五部分 5.3 | `project-tech-*.md` 按框架选择 |
| 业务模块 Skills | consistency-baseline → 第五部分 5.4 | `project-{module}.md` 如已存在 |
| 中间件 Skills | consistency-baseline → 第五部分 5.5 | `project-middleware-*.md` 按需选择 |

**步骤 3：按优先级生成伪代码**

| 优先级 | Skill 来源 | 在伪代码中的体现方式 |
|--------|-----------|---------------------|
| **P1** | requirements.md "相似功能模块分析" | 在伪代码注释中标注 `// 参考: Post.java L45-80 的 findById() 模式` |
| **P2** | requirements.md "复用功能模块" | 在伪代码中直接调用 `XXXService.findById()`，禁止重新实现 |
| **P3** | consistency-baseline "开发流程 Skills" | 伪代码结构符合 TDD 流程（先写接口定义，再写实现） |
| **P4** | consistency-baseline "技术栈 Skills" | 注解、配置符合 `project-tech-*.md` 规范（如 @Transactional） |
| **P5** | consistency-baseline "业务模块 Skills" | 符合 `project-{module}.md` 的接口约定和返回值类型 |
| **P6** | consistency-baseline "中间件 Skills" | 符合 `project-middleware-*.md` 的调用范式（如分页参数） |
| **P7** | ADR.md 第 8 节 "错误处理与边界设计" | 在伪代码中标注错误场景和异常处理逻辑 |
| **P8** | ADR.md 第 9 节 "风险与非功能设计" | 在伪代码中标注风险缓解措施 |
| **P9** | ADR.md 第 9 节 "性能与安全设计" | 在伪代码中标注性能优化和安全防护措施 |

##### 3.6.3 伪代码注释规范

每个伪代码必须包含以下注释块（按顺序）：

```java
// ========== [P1] 相似模块参考 ==========
// 来源：requirements.md US-001 "相似功能模块分析"
// 模块：Post 实体（src/entity/Post.java L20-45）
// 复用点：id 生成模式、@ManyToOne 关系映射

// ========== [P2] 强制复用模块 ==========
// 来源：requirements.md US-001 "复用功能模块"
// 必须调用：BaseEntity.getId()、UserService.findById()
// 禁止重新实现：用户鉴权逻辑

// ========== [P4] 技术栈规范 ==========
// 来源：project-tech-lombok.md
// 注解：@Entity, @Table, @Id, @GeneratedValue

// ========== [P6] 中间件调用 ==========
// 来源：project-middleware-database.md
// 分页参数：PageRequest.of(page, size)

// ========== [P7] 错误与异常处理 ==========
// 来源：ADR.md 第 8 节"错误处理与边界设计"
// 错误场景 1：内容为空 → 抛出 ValidationException
// 错误场景 2：用户无权限 → 抛出 AccessDeniedException
// 边界处理：空列表返回空 Page 对象（非 null）

// ========== [P8] 风险处理 ==========
// 来源：ADR.md 第 9 节"风险与非功能设计"
// 风险 1：数据库连接超时 → 使用连接池 + 重试机制
// 风险 2：并发写入冲突 → 使用乐观锁（@Version）

// ========== [P9] 非功能性处理 ==========
// 来源：ADR.md 第 9 节"性能与安全设计"
// 性能：分页查询（每页 20 条）+ 索引优化
// 安全：用户输入校验（@Valid）+ SQL 注入防护
```

##### 3.6.4 技术栈判断与伪代码语言选择

> **重要**：伪代码示例中的语言必须根据项目的技术栈确定，不得固定使用某一种语言

**判断步骤**：

```bash
# 1. 读取 tech-stack-profile.md 确定技术栈
TECH_STACK=$(grep -A 5 "后端框架" .claude/context/tech-stack-profile.md | grep -v "后端框架" | head -1)
echo "[Architect] 技术栈：$TECH_STACK"

# 2. 根据技术栈确定伪代码语言
case "$TECH_STACK" in
  *"Spring"*|*"Java"*|*"Kotlin"*)
    LANG="java"
    ;;
  *"Flask"*|*"FastAPI"*|*"Django"*|*"Python"*)
    LANG="python"
    ;;
  *"Express"*|*"NestJS"*|*"Node"*)
    LANG="typescript"
    ;;
  *)
    LANG="java"  # 默认值
    ;;
esac
echo "[Architect] 伪代码语言：$LANG"
```

**技术栈与伪代码语言对应表**：

| 技术栈类型 | 技术栈示例 | 伪代码语言 | 关键规范 Skill |
|-----------|-----------|------------|--------------|
| Java/Spring | Spring Boot, Spring Cloud | Java | project-tech-springboot.md |
| Python/Flask | Flask, FastAPI, Django | Python | project-tech-flask.md |
| Python/其他 | FastAPI, Pyramid | Python | project-tech-fastapi.md |
| TypeScript/Node | Express, NestJS | TypeScript | project-tech-typescript.md |
| Go | Gin, Echo | Go | project-tech-go.md |
| C#/.NET | ASP.NET Core | C# | project-tech-dotnet.md |

**示例中的 Java 仅用于演示**：实际生成时必须替换为对应语言的代码

##### 3.6.5 完整示例：Task T-001 创建 Comment 实体（Java 技术栈）

> **前提**：假设 tech-stack-profile.md 确定的技术栈为 Java/Spring Boot

```java
// ========== [P1] 相似模块参考 ==========
// 来源：requirements.md US-001 "相似功能模块分析"
// 模块：Post 实体（src/entity/Post.java L20-45）
// 复用点：id 生成模式、@ManyToOne 关系映射

// ========== [P2] 强制复用模块 ==========
// 来源：requirements.md US-001 "复用功能模块"
// 必须调用：BaseEntity.getId()、BaseEntity.getCreatedAt()
// 禁止重新实现：时间戳自动维护

// ========== [P4] 技术栈规范 ==========
// 来源：project-tech-lombok.md
// 注解：@Entity, @Table, @Id, @GeneratedValue, @CreationTimestamp

// ========== [P6] 中间件调用 ==========
// 来源：project-middleware-database.md
// 分页参数：PageRequest.of(page, size)

// ========== [P7] 错误与异常处理 ==========
// 来源：ADR.md 第 8 节"错误处理与边界设计"
// 错误场景 1：内容为空 → 抛出 ValidationException
// 错误场景 2：用户无权限 → 抛出 AccessDeniedException
// 边界处理：空列表返回空 Page 对象（非 null）

// ========== [P8] 风险处理 ==========
// 来源：ADR.md 第 9 节"风险与非功能设计"
// 风险 1：数据库连接超时 → 使用连接池 + 重试机制
// 风险 2：并发写入冲突 → 使用乐观锁（@Version）

// ========== [P9] 非功能性处理 ==========
// 来源：ADR.md 第 9 节"性能与安全设计"
// 性能：分页查询（每页 20 条）+ 索引优化
// 安全：用户输入校验（@Valid）+ SQL 注入防护

package com.example.entity;

import jakarta.persistence.*;
import lombok.Data;
import org.hibernate.annotations.CreationTimestamp;
import java.time.LocalDateTime;

@Data
@Entity
@Table(name = "comment", indexes = {
    @Index(name = "idx_post_id", columnList = "post_id"),
    @Index(name = "idx_user_id", columnList = "user_id")
})
public class Comment {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 1000)
    private String content;

    @Column(name = "post_id", nullable = false)
    private Long postId;

    @Column(name = "user_id", nullable = false)
    private Long userId;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;
}
```

##### 3.6.6 伪代码与 Skill 引用对应表

| Task 类型 | 必须引用的 Skill | 说明 |
|-----------|-----------------|------|
| 实体创建 | project-tech-lombok.md, project-middleware-database.md | 注解规范、分页模式 |
| Service 层 | project-service-pattern.md | 事务管理、异常处理 |
| Controller 层 | project-tech-web.md | 参数校验、响应格式 |
| Repository 层 | project-mybatis-pattern.md | 查询方法命名 |
| 业务逻辑复杂 | project-{module}.md | 对应模块的接口约定 |

##### 3.6.7 常见错误与纠正

| 错误类型 | 错误示例 | 正确做法 |
|---------|---------|---------|
| 缺少参考来源 | `// 实现评论功能` | `// 参考：Post.java L20-50 的实体定义模式` |
| 跳过复用模块 | `// 自己实现用户查询` | `// 必须调用：UserService.findById(userId)` |
| Skill 引用不清 | `project-tech-*.md` | `project-tech-lombok.md` |
| 伪代码过于简略 | `create Comment entity` | 包含完整的类结构、字段类型、注解、关系映射 |
| 未标注行号 | `// 参考 Post.java` | `// 参考：Post.java L20-50` |

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "产出物" "生成ADR" ".claude/iterations/sprint-latest/ADR.md" "成功"
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "生成ADR文档" "" "成功"
```

---

#### 3.7 按 ADR 模板生成文档

> **目的**：将以上分析结果（3.1-3.6）整合到 ADR 文档

使用 `.claude/templates/adr-template.md` 作为模板，将以上分析结果整合到 `.claude/iterations/sprint-latest/ADR.md`

**整合来源**：

| 分析章节 | ADR 对应章节 | 说明 |
|---------|-------------|------|
| 3.1 数据模型设计 | 第 4.3 节 | 基于 requirements.md 各 US 的数据实体需求 |
| 3.2 数据库表设计 | 第 4.4 节 | 基于数据模型设计转换的表结构 |
| 3.3 API 详细设计 | 第 5.4 节 | 包含签名、参数、返回值、错误码 |
| 3.4 错误处理与边界设计 | 第 8 节 | 包含正常流程、异常处理、错误码、重试降级、幂等性、边界值 |
| 3.5 风险与非功能设计 | 第 9 节 | 包含风险分析、性能设计、安全设计 |
| 3.6 Task 拆分与伪代码 | 第 7 节 | Task 拆分表 + pseudocode/ 目录下独立文件 |

**整合顺序**：
1. **先完成分析章节**：按顺序完成 3.1 → 3.2 → 3.3 → 3.4 → 3.5 → 3.6
2. **再执行整合**：使用 ADR 模板，按模板章节顺序填入各分析结果
3. **最后自检**：检查是否覆盖所有 User Story、是否有关联映射

**必须包含的章节**（共 18 节，来自 adr-template.md）：
1. 基本信息
2. 上下文（背景、需求摘要、决策驱动因素、**User Story 分组与依赖**）
3. 方案对比（至少两个方案）
4. **总体设计框架**：
   - 前端设计、后端设计、数据模型设计、数据库表设计、功能数据流分析设计、业务功能模块划分、业务 Workflow 设计、性能设计（含缓存）、状态流转设计
5. **详细设计**：
   - 目录结构、类图设计、方法签名、API 设计、接口 Schema、接口变更标注、与现有模块交互
6. **受影响模块分析**（按4类分类）
7. **实现步骤**：
   - Task 拆分（原子级，关联 US/MG）
   - **Task 伪代码（独立文件，存放在 pseudocode/ 目录）**
   - Task 依赖与优先级、Skill 引用
8. **错误处理与边界设计**
9. **风险与非功能设计**
10. **技术栈与命名约定**
11. **Skill 引用**
12. **API 变更**
13. 参考实现位置
14. 迁移指南
15. 受影响模块清单
16. 决策时间
17. **附录**（自检清单、变更历史）

---

### 操作 2.4：自检

> **目的**：在提交前完成自检，确保 ADR 质量

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "自检" "" ""
```

#### 自检清单

- [ ] 是否覆盖所有 User Story
- [ ] 每个 US 是否有独立的设计章节
- [ ] **Modular Group 是否完整划分（第 2.4 节）**
- [ ] **US 依赖矩阵是否准确（第 2.4 节）**
- [ ] 是否有完整的数据模型设计
- [ ] 是否有完整的数据库表设计
- [ ] 是否有完整的 API 设计（签名、参数、返回值、错误码）
- [ ] 是否识别了所有受影响模块（4类）
- [ ] 每个受影响模块是否标注了变更原因
- [ ] **Task 伪代码是否符合 consistency-baseline（命名、目录结构）**
- [ ] **Task 伪代码是否标注了可复用代码（参考模块、工具方法）**
- [ ] **Task 伪代码是否引用了正确的 Skills（包含外部 Skills 如 @superpowers/xxx）**
- [ ] **Task 伪代码文件是否独立生成（pseudocode/ 目录下）**
- [ ] **伪代码文件数量与 Task 数量是否一致**
- [ ] Task 是否关联到 US/Modular Group
- [ ] Task 是否原子化（2-4小时可完成）
- [ ] Task 依赖关系是否清晰
- [ ] Task 优先级是否标注
- [ ] 是否有错误处理设计
- [ ] 是否有边界值处理
- [ ] 是否有风险分析
- [ ] 是否有非功能设计（如有非功能需求）
- [ ] 是否引用了相关 Skill
- [ ] 是否遵循一致性基线（或有充分理由的突破）
- [ ] 接口变更是否明确标注（新增/修改/删除）

#### 自检结果处理

若自检发现问题：
1. 记录问题
2. 返回"操作 2.3"修复
3. 重新自检
4. 直至通过

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "自检" "" "成功"
```

---

### 操作 2.5：更新 session-status.md

> **目的**：记录阶段 2 Architect 完成状态

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "更新session-status" "" ""
```

#### 5.1 更新阶段完成记录

```bash
# 获取当前时间戳
COMPLETE_TIME=$(date +"%Y-%m-%d %H:%m:%S")

# 更新阶段 2 完成记录
sed -i "s/| 02 | 架构设计 |.*| ⏳ 待处理 |/| 02 | 架构设计 | $COMPLETE_TIME | ✅ 已生成 |/g" \
   "$ROOT/.claude/iterations/session-status.md"
```

#### 5.2 更新产出物追踪表

```bash
# 更新 ADR.md 产出物状态和完成时间
sed -i "s/| 02 | ADR.md | .claude/iterations/sprint-latest/ADR.md | ⏳ 待生成 |/| 02 | ADR.md | .claude/iterations/sprint-latest/ADR.md | ✅ 已生成 | $COMPLETE_TIME |/g" \
   "$ROOT/.claude/iterations/session-status.md"
```

#### 5.3 更新 ADR 自身状态为"已生成"

```bash
# 将 ADR 内部状态从"草稿"更新为"已生成"，供 PM 审核使用
sed -i "s/| \*\*状态\*\* | 草稿/| **状态** | 已生成/g" "$ROOT/.claude/iterations/sprint-latest/ADR.md"
echo "[Architect-Stage2] ADR 状态已更新为：已生成"
```

#### 5.4 记录 Architect 阶段完成报告

```markdown
### 阶段 2 完成报告：架构设计（Architect-Stage2）

- **完成时间**：{当前时间戳}
- **执行摘要**：完成 ADR 文档生成，User Story 数量：$US_COUNT，Sub-feature 数量：$SF_COUNT
- **Milestone（里程碑）**：
  - User Story 数量：$US_COUNT
  - Sub-feature 数量：$SF_COUNT
  - ADR 章节数量：17
- **关键产出**：
  - [ADR.md]：[.claude/iterations/sprint-latest/ADR.md] - ✅
- **与上阶段的衔接**：依赖 BA-Stage1 的 requirements.md
- **发现的问题**：无（自检通过）
- **下一步**：进入 PM 审核阶段的前置条件：ADR 生成完成
- **需要 Human Gate 确认的事项**：无
```

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "产出物" "更新session-status" ".claude/iterations/session-status.md" "成功"
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "session-status更新" "" "成功"
```

---

### 操作 2.6：更新 project.md

> **目的**：更新迭代历史章节中 ADR.md 的状态

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "更新project.md" "" ""
```

#### 6.1 检查 project.md 是否存在

```bash
if [ ! -f "$ROOT/.claude/context/project.md" ]; then
  echo "[Architect-Stage2] project.md 不存在，跳过更新"
  bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "跳过" "project.md不存在" "" ""
  exit 0
fi
```

#### 6.2 更新迭代历史章节

```bash
# 获取当前时间戳
UPDATE_TIME=$(date +"%Y-%m-%d %H:%m:%S")

# 在迭代历史中更新 ADR.md 状态
sed -i "s/| ADR.md | ⏳ 待生成 |/| ADR.md | ✅ 已生成 | $UPDATE_TIME |/g" \
   "$ROOT/.claude/context/project.md"
```

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "更新project.md" "" "成功"
```

---

### 操作 2.7：输出阶段摘要

> **目的**：向用户报告 Architect 阶段完成情况

#### 7.1 输入（Inputs）

| 输入 | 来源 | 用途 |
|------|------|------|
| requirements 主文档 | `.claude/iterations/sprint-latest/requirements.md` | 生成 ADR 的基础 |
| tech-stack-profile.md | `.claude/context/tech-stack-profile.md` | 技术栈参考 |
| consistency-baseline.md | `.claude/context/consistency-baseline.md` | 代码风格参考 |
| knowledge.grap | `.claude/context/knowledge.grap` | 受影响模块分析 |

#### 7.2 输出（Outputs）

| 输出 | 目的地 | 说明 |
|------|--------|------|
| ADR 主文档 | `.claude/iterations/sprint-latest/ADR.md` | 完整的架构设计文档 |

#### 7.3 执行摘要

示例：

```
[Architect-Stage2] 阶段 2 Architect 完成摘要：
- User Story 数量：5
- Sub-feature 数量：12
- ADR 章节数量：17
- 自检通过：是
- 产出物：
  - ADR.md：✅
```

#### 7.4 Human Gate 确认

> **目的**：向用户报告阶段 2 Architect 完成情况，等待确认

**等待用户确认以下内容**：

1. ADR 是否按模板完整生成（含第 2.4 节 Modular Group）
2. ADR 是否覆盖所有 User Story
3. **Modular Group 划分是否合理（后端 API + 前端 UI 配对，依赖关系正确）**
4. **US 依赖矩阵是否准确**
5. **Task 伪代码是否符合 consistency-baseline（命名、可复用代码、Skill 引用）**
6. **Task 伪代码文件是否独立生成（pseudocode/ 目录下，每个 Task 一个文件）**
7. 自检清单是否全部通过

**回复选项**：

- `继续` - 自检通过，允许 PM 进入审核阶段
- `打回` - 列出需要修正的问题，Architect 重新执行
- `暂停` - 暂停阶段 2，等待进一步指示

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "等待" "Human Gate 确认" "" "待回复"
```

---

## 异常处理

| 异常场景 | 处理方式 |
|---------|---------|
| requirements.md 不存在 | 报错退出 |
| knowledge.grap 不可用 | 标注"手动分析"继续执行 |
| 自检不通过 | 修复后重新自检 |
| 设计冲突 | 按 conflict-resolution.md 升级给 PM |

---

## 关联文档

| 文档 | 路径 | 说明 |
|------|------|------|
| requirements 主文档 | `.claude/iterations/sprint-latest/requirements.md` | 生成 ADR 的基础 |
| ADR 模板 | `.claude/templates/adr-template.md` | ADR 文档模板 |
| tech-stack-profile.md | `.claude/context/tech-stack-profile.md` | 技术栈参考 |
| consistency-baseline.md | `.claude/context/consistency-baseline.md` | 代码风格参考 |
| knowledge.grap | `.claude/context/knowledge.grap` | 知识图谱 |
| mf-upgrade:02-arch-qa.md | `.claude/commands/mf-upgrade:02-arch-qa.md` | 阶段 2 playbook |