# 一致性基线
> 文件路径：`.claude/context/consistency-baseline.md`
> 更新时机：阶段 0 初始化，架构师基于知识图谱生成；仅在文件不存在时生成
> **用途**：Dev Agent 开发时的代码风格参考，确保与项目现有约定一致
> **架构**：通用骨架 + 框架特定 Skill 填充
> **重要性**：必须调查清楚以下所有维度，才能确保 Dev Agent 遵守 code consistency 原则

---

## 第一部分：通用骨架（所有框架适用）

### 1. 项目元数据

| 项目 | 内容 | 来源 |
|------|------|------|
| **项目名称** | | project.md |
| **项目类型** | frontend / backend / fullstack | |
| **前端框架** | 自动检测 | package.json |
| **后端框架** | 自动检测 | requirements.txt |
| **调查完成时间** | | 自动记录 |
| **调查人** | Architect Agent | |

---

### 2. 前端目录结构规范

> 前端源代码目录结构和各层职责

| 目录 | 职责 | 证据（文件路径:行号） |
|------|------|----------------------|
| `src/store/` | Redux Store 配置 | |
| `src/reducers/` | Reducer 目录 | |
| `src/actions/` | Action creators | |
| `src/sagas/` 或 `src/thunks/` | 异步处理 | |
| `src/api/` 或 `src/services/` | API 调用层 | |
| `src/components/` | 通用组件 | |
| `src/pages/` 或 `src/views/` | 页面组件 | |
| `src/hooks/` | 自定义 Hooks | |
| `src/types/` | TypeScript 类型定义 | |
| `src/utils/` | 工具函数 | |
| `src/config/` | 配置文件 | |

---

### 3. 后端目录结构规范

> 后端源代码目录结构和各层职责

| 目录 | 职责 | 证据（文件路径:行号） |
|------|------|----------------------|
| `app/` 或 `src/` | 应用根目录 | |
| `app/models/` 或 `models/` | 数据模型 | |
| `app/views/` 或 `app/api/` | 路由/视图 | |
| `app/services/` | 业务逻辑层 | |
| `app/schemas/` 或 `app/serializers/` | 数据序列化 | |
| `app/middleware/` | 中间件 | |
| `app/utils/` | 工具函数 | |
| `app/config/` | 配置 | |

---

### 4. 数据库架构

#### 4.1 数据库创建与模型定义

| 调查项 | 说明 | 证据（文件路径:行号） |
|--------|------|----------------------|
| **ORM/ODM 类型** | SQLAlchemy / Prisma / Eloquent / MongoDB | |
| **数据库模型定义位置** | `models/` / `entities/` / `schemas/` | |
| **模型基类** | 是否有统一的 Base 类？ | |
| **模型关系定义** | ForeignKey / OneToMany / ManyToMany 如何定义 | |
| **数据库迁移工具** | Alembic / Flyway / Prisma Migrate | |
| **迁移文件位置** | `migrations/` / `alembic/` | |
| **数据库连接配置** | 在哪个文件配置？`db.py` / `config.py`？ | |

#### 4.2 数据库调用范式

| 调查项 | 说明 | 证据（文件路径:行号） |
|--------|------|----------------------|
| **Session/Connection 管理** | 如何获取数据库连接？ | |
| **事务处理** | 事务如何开启、提交、回滚？ | |
| **查询构建方式** | ORM Query Builder vs Raw SQL | |
| **Repository/DAO 模式** | 数据访问是否封装？ | |
| **数据验证** | 数据库层面的数据验证在哪里做？ | |

---

### 5. 前台 Redux 架构深度调查

#### 5.1 Store 配置与创建

| 调查项 | 说明 | 证据（文件路径:行号） |
|--------|------|----------------------|
| **Store 创建位置** | `store/index.ts` 或 `store/configureStore.ts` | |
| **Store 配置方式** | configureStore vs legacy createStore | |
| **中间件配置** | thunk / saga / observable 如何配置 | |
| **DevTools 是否启用** | store.devTools 配置 | |
| **Root Reducer 合并方式** | combineReducers vs createSlice | |

#### 5.2 State 数据组织

| 调查项 | 说明 | 证据（文件路径:行号） |
|--------|------|----------------------|
| **State 结构设计** | 嵌套 vs 扁平？normalized？ | |
| **State 集中定义** | 所有 state 在一个地方定义还是分散在各 slice？ | |
| **State 初始化** | initialState 如何定义？来自 API 还是静态？ | |
| **Immutable 更新** | 如何确保不可变？Immer produce？展开运算符？ | |

#### 5.3 Action 与 Reducer 开发

| 调查项 | 说明 | 证据（文件路径:行号） |
|--------|------|----------------------|
| **Action Type 定义** | 在哪里定义？常量文件 vs 直接在 slice | |
| **Action Type 格式** | `feature/action` 小写 vs `FEATURE/ACTION` 大写 vs 枚举 | |
| **Action Creator 模式** | createAction vs 函数式 | |
| **Reducer 注册** | 如何注册到 store？combineReducers 位置？ | |
| **Reducer 编写方式** | createSlice vs 手动 switch-case | |
| **Extra Reducers** | createSlice.extraReducers 如何使用 | |

#### 5.4 Action Dispatch 与业务逻辑触发

| 调查项 | 说明 | 证据（文件路径:行号） |
|--------|------|----------------------|
| **Dispatch 方式** | useDispatch hook vs connect HOC | |
| **异步 Action 触发** | createAsyncThunk vs thunk 手动封装 | |
| **业务逻辑在哪里** | saga / thunk / RTK Query 如何组织 | |
| **Pending/Fulfilled/Rejected** | 异步 action 生命周期处理 | |
| **Loading/Error 状态** | 如何追踪和管理 | |

#### 5.5 组件间状态传递

| 调查项 | 说明 | 证据（文件路径:行号） |
|--------|------|----------------------|
| **Props drilling** | 组件如何接收父组件数据？ | |
| **Context/Provider** | Context 如何组织和使用？ | |
| **useSelector** | 如何高效订阅 store？ | |
| **组件通信方式** | props vs callback vs context vs Redux | |
| **HOC 使用** | 是否使用高阶组件？connect？ | |

#### 5.6 页面间状态传递

| 调查项 | 说明 | 证据（文件路径:行号） |
|--------|------|----------------------|
| **路由状态** | React Router / Vue Router 状态管理 | |
| **URL 参数传递** | params / query string 如何获取 | |
| **持久化状态** | localStorage / sessionStorage / URL | |
| **全局状态** | Redux / Context 在页面间共享 | |
| **页面跳转后状态恢复** | 如何保持滚动位置等状态 | |

---

### 6. 前台 API 调用层

#### 6.1 API 访问架构

| 调查项 | 说明 | 证据（文件路径:行号） |
|--------|------|----------------------|
| **API 调用层位置** | `api/` / `services/` / `endpoints/` | |
| **统一接口调用** | 是否通过统一的 API 层？还是直接组件内调用 | |
| **Base URL 配置** | 在哪个文件配置？axios instance？ | |
| **请求拦截器** | 请求如何添加 auth token 等 | |
| **响应拦截器** | 响应如何统一处理错误、数据转换 | |
| **API 模块化** | 每个功能模块有独立的 API 文件？ | |

#### 6.2 API 契约定义

| 调查项 | 说明 | 证据（文件路径:行号） |
|--------|------|----------------------|
| **请求参数类型** | TypeScript interface 定义在哪里？ | |
| **响应数据类型** | Response 类型如何定义？ | |
| **API 版本控制** | `/api/v1/` vs `/api/` | |
| **错误码定义** | 错误码在哪里定义？前端如何处理？ | |

#### 6.3 API 数据处理

| 调查项 | 说明 | 证据（文件路径:行号） |
|--------|------|----------------------|
| **响应数据格式** | JSON / XML / 二进制 | |
| **状态码处理** | HTTP 状态码如何映射到业务错误码 | |
| **数据归一化** | 响应数据如何转换？ | |
| **错误处理流程** | 网络错误 vs 业务错误如何区分 | |
| **Loading/Error 状态** | API 调用时如何管理状态 | |

---

### 7. 后台业务架构

#### 7.1 URL 接口定义

| 调查项 | 说明 | 证据（文件路径:行号） |
|--------|------|----------------------|
| **URL 定义集中位置** | `urls.py` / `routes/` / `endpoints/` | |
| **URL 命名规范** | path vs name 如何命名 | |
| **路由模块化** | Blueprint / App Router / Controller | |
| **RESTful 规范** | HTTP 方法使用 GET/POST/PUT/DELETE | |

#### 7.2 业务逻辑组织

| 调查项 | 说明 | 证据（文件路径:行号） |
|--------|------|----------------------|
| **Service 层** | 业务逻辑是否封装在 Service？ | |
| **业务逻辑流转** | Request → Controller → Service → Model → DB | |
| **事务管理** | 跨多个操作的事务如何处理 | |
| **业务规则验证** | 验证逻辑在哪里做？Service？Model？ | |
| **类/函数设计** | 核心类和函数有哪些？职责划分 | |

#### 7.3 中间件与拦截器

| 调查项 | 说明 | 证据（文件路径:行号） |
|--------|------|----------------------|
| **中间件定义** | 认证/日志/错误处理中间件在哪里 | |
| **请求/响应拦截** | 拦截器如何实现 | |
| **权限验证** | 路由守卫/装饰器如何实现 | |

---

### 8. 前后台 API 交互契约

#### 8.1 认证与鉴权

| 调查项 | 说明 | 证据（文件路径:行号） |
|--------|------|----------------------|
| **认证方式** | JWT / Session / OAuth | |
| **Token 存储** | 前台存储在哪里？localStorage / cookie / memory | |
| **Token 传递** | Authorization header 如何发送 | |
| **刷新 Token** | Token 过期如何刷新 | |
| **路由守卫** | 前台路由如何验证权限 | |
| **后端鉴权中间件** | 中间件如何验证 token | |

#### 8.2 异常处理统一规范

| 调查项 | 说明 | 证据（文件路径:行号） |
|--------|------|----------------------|
| **统一响应格式** | `{code, message, data}` vs 其他格式 | |
| **错误码定义位置** | 错误码在哪个文件定义 | |
| **前台异常处理** | try/catch vs 拦截器统一处理 | |
| **后台异常定义** | 自定义异常类如何定义 | |
| **异常日志** | 异常如何记录和追踪 | |

---

### 9. 命名与组织规范（通用）

#### 9.1 文件命名规范
| 序号 | 规则描述 | 证据（文件路径） | 示例 |
|------|---------|----------------|------|
| 1 | 【规则】描述 | | 例如：`user.controller.ts` |
| 2 | 【规则】描述 | | |

#### 9.2 变量/函数命名规范
| 序号 | 规则描述 | 证据（文件路径） | 示例 |
|------|---------|----------------|------|
| 1 | 【规则】描述 | | 例如：`useGetUser()` |
| 2 | 【规则】描述 | | |

#### 9.3 模块命名规范
| 序号 | 规则描述 | 证据（文件路径） | 示例 |
|------|---------|----------------|------|
| 1 | 【规则】描述 | | |

---

### 10. 模块耦合规则（通用）

> 模块间依赖关系的约束

| 序号 | 规则描述 | 证据（文件路径） | 说明 |
|------|---------|----------------|------|
| 1 | 【规则】描述 | `src/xxx.ts` | 允许的依赖 |
| 2 | 【规则】描述 | `src/xxx.ts` | 禁止的依赖 |
| 3 | 【规则】描述 | `src/xxx.ts` | 循环依赖检测结果 |

---

### 11. 代码复用约定（通用）

> 公共代码的复用方式和位置

| 序号 | 复用类型 | 复用位置 | 证据（文件路径） | 说明 |
|------|---------|---------|----------------|------|
| 1 | 工具函数 | `utils/` 目录 | `src/utils/xxx.ts` | |
| 2 | 公共组件 | `components/` 目录 | `src/components/xxx.ts` | |
| 3 | 公共类型 | `types/` 目录 | `src/types/xxx.ts` | |
| 4 | 配置常量 | `config/` 目录 | `src/config/xxx.ts` | |

---

### 12. 反模式（禁止做法）（通用）

> 项目中明确禁止的做法

| 序号 | 禁止做法 | 原因 | 正确做法示例 |
|------|---------|------|-------------|
| 1 | 描述 | 描述 | `src/xxx.ts:12` 展示正确做法 |
| 2 | 描述 | 描述 | `src/xxx.ts:45` 展示正确做法 |

---

### 13. 测试规范（通用）

| 调查项 | 说明 | 证据 |
|--------|------|------|
| 测试框架 | jest / vitest / pytest | package.json / requirements.txt |
| 测试目录 | `tests/` 或 `__tests__/` | 目录结构 |
| 测试命名规范 | `*.test.ts` / `test_*.py` | |
| 测试覆盖率要求 | 80% / 100% | |

---

### 14. 部署与环境（通用）

| 调查项 | 说明 | 证据 |
|--------|------|------|
| 环境管理 | `.env` / `config.yaml` | |
| 多环境配置 | dev / staging / prod | |
| Docker 配置 | Dockerfile / docker-compose.yml | |
| CI/CD 配置 | GitHub Actions / Jenkins | |

---

### 15. 类型定义规范

| 调查项 | 说明 | 证据（文件路径:行号） |
|--------|------|----------------------|
| **类型定义文件位置** | `types/` / `interfaces/` | |
| **全局类型** | RootState / AppDispatch 在哪里定义 | |
| **API 类型** | 请求/响应类型在哪里定义 | |
| **组件 Props 类型** | 如何定义和传递 | |

---

### 16. 日志与监控

| 调查项 | 说明 | 证据（文件路径:行号） |
|--------|------|----------------------|
| **日志级别** | DEBUG / INFO / WARN / ERROR | |
| **日志格式** | JSON vs 文本格式 | |
| **日志输出位置** | console / file / remote | |
| **错误追踪** | Sentry / Bugsnag / 自建 | |

---

### 17. 缓存策略

| 调查项 | 说明 | 证据（文件路径:行号） |
|--------|------|----------------------|
| **前端缓存** | React Query / SWR / Redux Persist | |
| **后端缓存** | Redis / Memcached / 内存缓存 | |
| **缓存失效** | 缓存如何更新和清除 | |

---

## 第二部分：框架特定调查（由对应 Skill 填充）

> 以下章节由对应的 Framework Skill 自动填充，Architect Agent 调用 Skill 执行调查

### 18. 前端框架特定规范

> **由 frontend-{framework} Skill 填充**

| 调查项 | 内容 |
|--------|------|
| **框架类型** | React / Vue / Angular / Svelte |
| **框架版本** | |
| **UI 组件库** | |
| **状态管理** | Redux Toolkit / Pinia / Vuex |
| **样式方案** | CSS Modules / Styled-Components / Tailwind / CSS-in-JS |
| **路由方案** | react-router / vue-router / @angular/router |

**状态**：⏳ 待 Skill 填充

---

### 19. 后端框架特定规范

> **由 backend-{framework} Skill 填充**

| 调查项 | 内容 |
|--------|------|
| **框架类型** | Flask / FastAPI / Django / Express / Spring |
| **框架版本** | |
| **ORM** | SQLAlchemy / Prisma / Eloquent / TypeORM |
| **数据库** | PostgreSQL / MySQL / SQLite / MongoDB |
| **API 风格** | REST / GraphQL / gRPC |

**状态**：⏳ 待 Skill 填充

---

### 20. 关键代码样例索引

> Dev Agent 需要引用的关键代码位置

| 模式 | 文件路径 | 行号范围 | 用途 |
|------|---------|---------|------|
| Store 创建 | | | Redux store 初始化 |
| Slice 定义 | | | RTK slice 模板 |
| Action 定义 | | | Action creators |
| Reducer 编写 | | | Reducer 实现 |
| API 调用 | | | HTTP 请求 |
| 错误处理 | | | 异常捕获 |
| 认证流程 | | | 登录/鉴权 |
| 数据库模型 | | | ORM 模型定义 |
| Service 层 | | | 业务逻辑 |
| 中间件 | | | 拦截器/中间件 |

---

## 第三部分：框架 Skill 调用记录

> 记录本次调查中调用的 Framework Skills

| Skill 名称 | 调用时间 | 检测方式 | 确认状态 |
|-----------|---------|---------|---------|
| frontend-redux | | auto-detect | ⏳ 待确认 |
| | | | |

**Human Confirmation Required**：请确认检测到的框架是否正确，如有误请手动指定。

---

## 第五部分：项目 Skills 清单

> **用途**：供 Arch-Stage2 生成 Task 伪代码时引用，为 Dev Agent 提供完整的 Skill 索引
>
> **Skill 分类体系（方案 B 混合分类）**：
> 1. **通用规范类** - 跨层通用（Naming、Workflow 等）
> 2. **L1 基础设施类** - 来自 FE-I-*
> 3. **L2 领域模型类** - 来自 FE-D-*
> 4. **L3 应用服务类** - 来自 FE-A-*
> 5. **L4 接口组件类** - 来自 FE-F-*
> 6. **L5 业务场景类** - 来自 BS-*
> 7. **框架特定类** - frontend-*/backend-*
>
> **更新时机**：阶段 0 初始化时生成，Skill 目录变化时更新

### 5.1 通用规范类（跨层）

> **说明**：所有项目成员必须遵守的通用规范，适用范围 L1-L5

| Skill 文件 | 描述 | 适用范围 | 关键要点 |
|-----------|------|---------|---------|
| project-naming-convention.md | 命名规范 | L1-L5 | 文件命名、变量命名、函数命名、数据库命名、API命名、全局配置 |
| project-directory-structure.md | 目录结构 | L1-L5 | 各目录职责、层级关系 |
| project-git-workflow.md | Git 工作流 | L1-L5 | 分支策略、提交规范 |
| project-tdd-pattern.md | TDD 开发流程 | L1-L5 | RED-GREEN-REFACTOR |
| project-code-review-checklist.md | Code Review 标准 | L1-L5 | 命名、复杂度、安全检查 |
| project-commit-convention.md | 提交规范 | L1-L5 | conventional commit 格式 |
| project-build.md | 构建规范 | L1-L5 | 构建命令、产物管理 |
| project-deploy.md | 部署规范 | L1-L5 | 环境配置、部署步骤 |
| project-docker.md | Docker 规范 | L1-L5 | Dockerfile、docker-compose |

### 5.2 L1 基础设施类（FE-I-*）

> **说明**：来源于 feature-elements.md L1 层基础设施类别

| Skill 文件 | 对应 FE | 描述 | 关键模式 |
|-----------|---------|------|---------|
| project-infra-database.md | FE-I-001 | 数据库基础设施 | 连接管理、事务、ORM |
| project-infra-cache.md | FE-I-002 | 缓存基础设施 | Redis/Memcached 使用 |
| project-infra-filesystem.md | FE-I-003 | 文件系统 | 文件读写、存储抽象 |
| project-infra-network.md | FE-I-004 | 网络通信 | HTTP 客户端、API 调用 |
| project-infra-message-queue.md | FE-I-005 | 消息队列 | RabbitMQ/Kafka 使用 |
| project-infra-security.md | FE-I-006 | 安全认证 | JWT、OAuth、加密 |
| project-infra-logging.md | FE-I-007 | 日志 | 日志配置、格式规范 |
| project-infra-config.md | FE-I-008 | 配置管理 | 环境配置、参数管理 |

### 5.3 L2 领域模型类（FE-D-*）

> **说明**：来源于 feature-elements.md L2 层领域模型，定义业务实体、值对象、聚合根

| Skill 文件 | 对应 FE | 描述 | 核心元素 |
|-----------|---------|------|---------|
| project-domain-{entity}.md | FE-D-001 | 用户领域模型 | User 实体、属性、方法 |
| project-domain-{entity}.md | FE-D-002 | 产品领域模型 | Product 实体、值对象 |
| ... | FE-D-*** | 其他领域模型 | 按项目实际检测结果 |

### 5.4 L3 应用服务类（FE-A-*）

> **说明**：来源于 feature-elements.md L3 层应用服务，定义用例服务、工作流编排、事件处理

| Skill 文件 | 对应 FE | 描述 | 核心服务 |
|-----------|---------|------|---------|
| project-service-auth.md | FE-A-001 | 认证服务 | 登录、注册、Token 刷新 |
| project-service-order.md | FE-A-002 | 订单服务 | 创建、查询、取消 |
| ... | FE-A-*** | 其他应用服务 | 按项目实际检测结果 |

### 5.5 L4 接口组件类（FE-F-*）

> **说明**：来源于 feature-elements.md L4 层接口层，定义 API 端点、UI 组件

#### 5.5.1 API 接口

| Skill 文件 | 对应 FE | 描述 | 端点 |
|-----------|---------|------|------|
| project-api-user.md | FE-F-001 | 用户 API | GET/POST /api/users |
| project-api-order.md | FE-F-002 | 订单 API | GET/POST /api/orders |
| ... | FE-F-*** | 其他 API | 按项目实际检测结果 |

#### 5.5.2 UI 组件

| Skill 文件 | 对应 FE | 描述 | 组件类型 |
|-----------|---------|------|---------|
| project-ui-button.md | FE-F-*** | 按钮组件 | atomic |
| project-ui-form.md | FE-F-*** | 表单组件 | molecular |
| ... | FE-F-*** | 其他 UI 组件 | 按项目实际检测结果 |

### 5.6 L5 业务场景类（BS-*）

> **说明**：来源于 feature-elements.md L5 层业务场景，横跨 L1-L4 的完整业务流程

| Skill 文件 | 对应场景 | 描述 | 涉及层次 |
|-----------|---------|------|---------|
| project-feature-checkout.md | BS-001 | 结账流程 | L2用户+L3订单+L4接口+L1支付 |
| project-feature-search.md | BS-002 | 商品搜索 | L4接口+L3搜索服务+L2商品+L1数据库 |
| ... | BS-*** | 其他业务场景 | 按项目实际检测结果 |

### 5.7 框架特定类

> **说明**：来源于检测到的技术栈，由对应 Framework Skill 填充

| Skill 文件 | 描述 | 关键模式 |
|-----------|------|---------|
| frontend-react.md | 前端 React 规范 | 组件编写、Hooks、State 管理 |
| frontend-vue.md | 前端 Vue 规范 | 组件编写、Composition API |
| backend-django.md | 后端 Django 规范 | View、Model、ORM |
| backend-fastapi.md | 后端 FastAPI 规范 | 路由、依赖注入、Schema |
| backend-flask.md | 后端 Flask 规范 | 路由、Blueprint、SQLAlchemy |

### 5.8 Skills 索引表（汇总）

> **说明**：下表中 Skill 文件路径表示目录（如 `project-infra-database/`），实际使用时引用其中的 `SKILL.md`

| Skill 文件 | Layer | Category | 描述 | 优先级 |
|-----------|-------|----------|------|--------|
| project-naming-convention/ | 通用 | General | 命名规范 | P0 |
| project-directory-structure/ | 通用 | General | 目录规范 | P0 |
| project-git-workflow/ | 通用 | General | Git 工作流 | P0 |
| project-tdd-pattern/ | 通用 | General | TDD 开发 | P1 |
| project-code-review-checklist/ | 通用 | General | Code Review | P1 |
| project-commit-convention/ | 通用 | General | 提交规范 | P1 |
| project-build/ | 通用 | General | 构建规范 | P2 |
| project-deploy/ | 通用 | General | 部署规范 | P2 |
| project-docker/ | 通用 | General | Docker 规范 | P2 |
| project-infra-*/ | L1 | Infrastructure | 基础设施 | P3 |
| project-domain-*/ | L2 | Domain | 领域模型 | P3 |
| project-service-*/ | L3 | Application | 应用服务 | P3 |
| project-api-*/ | L4 | Interface/API | API 规范 | P3 |
| project-ui-*/ | L4 | Interface/UI | UI 组件 | P3 |
| project-feature-*/ | L5 | Business Scene | 业务功能 | P3 |
| frontend-*/ | 框架 | Frontend | 前端框架 | P4 |
| backend-*/ | 框架 | Backend | 后端框架 | P4 |

---

## 参考链接

| 文档 | 链接 | 说明 |
|------|------|------|
| 项目架构图 | | |
| 核心模块说明 | | |
| Framework 官方文档 | | |
| API 文档 | | |