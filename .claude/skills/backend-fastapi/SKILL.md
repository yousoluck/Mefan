# Skill 元数据

```yaml
name: backend-fastapi
name_zh: 后端 FastAPI 框架调查
category: backend
framework: fastapi
version: 1.0.0
author: Architect Agent
created: 2026-05-22
trigger: auto-detect
trigger_files:
  - requirements.txt (contains "fastapi")
  - main.py
  - app.py
```

---

## 1. 框架概述

| 项目 | 内容 |
|------|------|
| **框架版本** | FastAPI 0.110+ |
| **核心作用** | 现代高性能异步 API 框架 |
| **ORM** | SQLAlchemy + asyncpg |
| **迁移** | Alembic |

---

## 2. 目录结构规范

```
app/
├── __init__.py
├── main.py              # FastAPI 实例
├── config.py            # 配置
├── api/                  # API 路由
│   ├── __init__.py
│   └── v1/
│       └── endpoints/
├── core/                 # 核心模块
│   ├── security.py       # 认证
│   └── exceptions.py     # 异常
├── db/                   # 数据库
│   ├── base.py           # Base
│   ├── session.py        # Session
│   └── repository.py     # Repository
├── models/               # Pydantic 模型
│   └── __init__.py
├── schemas/              # 请求/响应 schema
│   └── __init__.py
└── services/             # 业务逻辑
    └── __init__.py
```

---

## 3. 核心元素调查清单

### 3.1 FastAPI 实例

| 调查项 | 文件位置 | 说明 |
|--------|---------|------|
| App 创建 | `app/main.py` | FastAPI() |
| 中间件 | `app/main.py` | CORS/Auth |
| 路由注册 | `app/main.py` | include_router |

### 3.2 路由与依赖

| 调查项 | 说明 |
|--------|------|
| Path Operation | @app.get/post/put/delete |
| 依赖注入 | Depends() |
| 请求验证 | Pydantic BaseModel |
| 响应模型 | response_model |

### 3.3 异步数据库

| 调查项 | 说明 |
|--------|------|
| Async Session | async_sessionmaker |
| Repository 模式 | 异步数据访问 |
| 事务管理 | async with session |

### 3.4 安全

| 调查项 | 说明 |
|--------|------|
| JWT 处理 | python-jose |
| Password 哈希 | passlib |
| OAuth2 | Security dependency |

---

## 4. 代码样例索引

| 模式 | 文件 | 说明 |
|------|------|------|
| App 创建 | `app/main.py` | FastAPI 模板 |
| Endpoint | `app/api/v1/endpoints/user.py` | API 端点 |
| Schema | `app/schemas/user.py` | Pydantic 模型 |
| Repository | `app/db/repository/user.py` | 数据访问 |

---

## 5. 命名约定调查

| 调查项 | 关键问题 | 证据文件:行号 |
|--------|---------|--------------|
| **Router 变量命名** | 下划线还是驼峰？如 `router` vs `user_router` | |
| **Endpoint 函数命名** | 动词还是名词？如 `get_user` vs `getUser` vs `get_user_by_id` | |
| **Pydantic 模型命名** | PascalCase？如 `UserCreate`, `UserResponse` | |
| **Schema 字段命名** | 驼峰还是蛇形？如 `userName` vs `user_name` | |
| **路径参数命名** | 短还是完整？如 `uid` vs `user_id` | |
| **Query 参数命名** | 下划线分隔还是驼峰？ | |
| **Response 模型命名** | `Response` 后缀？如 `UserResponse` vs `User` | |
| **Service 函数命名** | 动词还是名词？ | |
| **Repository 函数命名** | `get_` vs `fetch_` vs `find_`？ | |

---

## 6. 禁止做法（反模式）

| 禁止 | 原因 | 正确做法 | 证据 |
|------|------|---------|------|
| **在路径函数中直接操作数据库** | 违反分层原则 | 使用 Service/Repository 层 | |
| **同步阻塞调用在 async 函数中** | 阻塞事件循环 | 使用 async SQLAlchemy 或 run_in_executor | |
| **Response 模型包含敏感字段** | 数据泄露风险 | 使用嵌套 Pydantic 模型排除敏感字段 | |
| **路径参数类型不声明** | 默认 str，缺少验证 | 使用 `Path(..., ge=1)` 类型注解 | |
| **使用 dict 而非 Pydantic 模型** | 丢失类型检查和验证 | 使用 BaseModel 定义请求/响应 | |
| **异常时返回错误状态码带敏感信息** | 信息泄露风险 | 统一错误响应格式，过滤敏感信息 | |
| **在依赖注入中执行数据库查询** | 导致数据库会话管理混乱 | 在路由函数中显式使用 session | |

---

## 7. 常见问题调查

| 调查项 | 关键问题 | 证据文件:行号 |
|--------|---------|--------------|
| **数据库会话管理** | 如何处理 async session lifecycle？ | |
| **依赖注入模式** | 使用 Depends 还是类作为依赖？ | |
| **分页实现** | Limit/Offset 还是 Cursor-based？ | |
| **认证方式** | JWT vs OAuth2 vs API Key？ | |
| **文件上传处理** | 上传文件如何存储和访问？ | |
| **后台任务** | 使用 BackgroundTasks 还是 Celery？ | |
| **OpenAPI 文档** | 自动生成文档是否完整？ | |
| **错误处理** | 统一异常处理如何实现？ | |

---

## 8. 依赖版本调查

| 调查项 | 关键问题 | 证据文件 |
|--------|---------|---------|
| **FastAPI 版本** | 0.110+？是否使用最新特性？ | requirements.txt |
| **Uvicorn vs Gunicorn** | 生产环境使用哪个 ASGI 服务器？ | requirements.txt |
| **SQLAlchemy 版本** | 1.4 vs 2.0？async 支持程度？ | requirements.txt |
| **Asyncpg vs aiomysql** | PostgreSQL 还是 MySQL？ | requirements.txt |
| **Pydantic 版本** | v1 还是 v2？是否使用 BaseModel 配置类？ | requirements.txt |
| **认证库** | python-jose vs pyjwt vs python-jose[turbojwt]？ | requirements.txt |
| **密码哈希** | passlib[bcrypt] vs bcrypt？ | requirements.txt |
| **Celery 集成** | 是否使用异步任务队列？ | requirements.txt |

---

## Scripts

| 脚本名 | 说明 |
|--------|------|
| detect-fastapi.sh | 检测 FastAPI 框架 |
| extract-fastapi-patterns.sh | 提取 FastAPI 代码模式 |

---

## Reference

- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [SQLAlchemy async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Pydantic](https://docs.pydantic.dev/)