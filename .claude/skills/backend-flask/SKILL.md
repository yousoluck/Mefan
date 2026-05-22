# Skill 元数据

```yaml
name: backend-flask
name_zh: 后端 Flask 框架调查
category: backend
framework: flask
version: 1.0.0
author: Architect Agent
created: 2026-05-22
trigger: auto-detect
trigger_files:
  - requirements.txt (contains "flask")
  - app.py
  - run.py
```

---

## 1. 框架概述

| 项目 | 内容 |
|------|------|
| **框架版本** | Flask 3.x |
| **核心作用** | 轻量级 WSGI 微框架 |
| **ORM** | SQLAlchemy |
| **模板引擎** | Jinja2 |

---

## 2. 目录结构规范

```
app/
├── __init__.py          # Flask App 工厂
├── config.py            # 配置
├── models/              # 数据库模型
│   └── __init__.py
├── views/               # 视图（路由处理）
│   ├── __init__.py
│   └── {feature}/
├── services/            # 业务逻辑
│   └── __init__.py
├── utils/               # 工具函数
│   └── __init__.py
├── extensions.py       # 扩展初始化
└── errors.py            # 错误处理
```

---

## 3. 核心元素调查清单

### 3.1 App 工厂模式

| 调查项 | 文件位置 | 说明 |
|--------|---------|------|
| Flask 应用创建 | `app/__init__.py` | create_app() 工厂 |
| 配置管理 | `app/config.py` | 配置类 |
| 扩展初始化 | `app/extensions.py` | DB/Migrate 等 |

### 3.2 路由与视图

| 调查项 | 说明 |
|--------|------|
| Blueprint 使用 | 模块化路由 |
| 视图函数 | @app.route 定义 |
| 请求处理 | request 对象 |
| 响应返回 | JSON vs Template |

### 3.3 数据库

| 调查项 | 说明 |
|--------|------|
| ORM 配置 | SQLAlchemy 初始化 |
| 模型定义 | class Model(db.Model) |
| 迁移 | Flask-Migrate/Alembic |
| 查询 | Query API |

### 3.4 业务逻辑

| 调查项 | 说明 |
|--------|------|
| Service 层 | 业务逻辑封装 |
| 事务管理 | session.begin() |
| 验证逻辑 | 业务规则验证 |

---

## 4. 代码样例索引

| 模式 | 文件 | 说明 |
|------|------|------|
| App 工厂 | `app/__init__.py` | create_app 模板 |
| Blueprint | `app/views/auth.py` | 路由模块化 |
| Model | `app/models/user.py` | SQLAlchemy 模型 |
| Service | `app/services/user_service.py` | 业务逻辑 |

---

## 5. 命名约定调查

| 调查项 | 关键问题 | 证据文件:行号 |
|--------|---------|--------------|
| **Blueprint 命名** | 变量名用下划线还是 CamelCase？如 `auth_bp` vs `authBlueprint` | |
| **视图函数命名** | 下划线还是驼峰？如 `get_user` vs `getUser` | |
| **路由 URL 命名** | 斜杠分隔还是下划线？如 `/api/users` vs `/api/users_list` | |
| **Model 类命名** | PascalCase？如 `class UserProfile` | |
| **Model 字段命名** | 驼峰还是蛇形？如 `userName` vs `user_name` | |
| **Config 类属性** | 全大写还是驼峰？如 `SECRET_KEY` vs `secretKey` | |
| **Service 函数命名** | 动词还是名词？如 `create_user` vs `user_creation` | |
| **错误处理函数** | 命名模式？如 `handle_404` vs `not_found_error` | |
| **数据库表名** | 复数还是单数？如 `users` vs `user` | |

---

## 6. 禁止做法（反模式）

| 禁止 | 原因 | 正确做法 | 证据 |
|------|------|---------|------|
| **app.config 直接访问** | 配置分散，难以测试 | 使用 `current_app.config` 或 Config 类 | |
| **在视图函数中直接查询** | 违反分层原则 | 使用 Service 层封装业务逻辑 | |
| **使用 Flask 扩展的快捷方式** | 如 `db.session.add()` 而非 SQLAlchemy session | 直接使用 SQLAlchemy session | |
| **Blueprint 循环导入** | 常见于 `__init__.py` 导入顺序错误 | 使用延迟导入或重构 | |
| **请求处理函数中抛出异常** | 未捕获异常导致 500 错误 | 使用 errorhandler 统一处理 | |
| **在请求开始前提交事务** | 可能导致部分更新 | 使用 `after_request` 或 try/finally | |
| **全局变量存储用户数据** | 线程安全问题 | 使用 `g` 对象或请求上下文 | |

---

## 7. 常见问题调查

| 调查项 | 关键问题 | 证据文件:行号 |
|--------|---------|--------------|
| **App 工厂模式** | 是否使用 `create_app()`？配置如何传递？ | |
| **Blueprint 注册顺序** | 路由注册顺序是否影响路径匹配？ | |
| **数据库会话管理** | session.permanent 还是请求级 session？ | |
| **Migration 管理** | Flask-Migrate 还是 Flask-Alembic？ | |
| **请求参数验证** | 使用 Flask-WTF 还是手工验证？ | |
| **CORS 配置** | 如何处理跨域请求？ | |
| **分页实现** | 自己实现还是使用 flask-sqlalchemy 的 paginate？ | |
| **静态文件处理** | Nginx 代理还是 Flask serving？ | |

---

## 8. 依赖版本调查

| 调查项 | 关键问题 | 证据文件 |
|--------|---------|---------|
| **Flask 版本** | Flask 2.x 还是 3.x？具体版本？ | requirements.txt |
| **SQLAlchemy 版本** | 1.4 还是 2.0？async 支持情况？ | requirements.txt |
| **Flask-SQLAlchemy 版本** | 与 SQLAlchemy 版本兼容性？ | requirements.txt |
| **Migration 工具** | Flask-Migrate vs Flask-Alembic？ | requirements.txt |
| **WSGI 服务器** | Gunicorn vs uWSGI vs Waitress？ | requirements.txt |
| **API 框架** | 是否使用 Flask-RESTful？ | requirements.txt |
| **认证扩展** | Flask-JWT-Extended vs Flask-JWT vs Flask-Login？ | requirements.txt |
| **Celery 集成** | 是否使用异步任务？Flask-Celery？ | requirements.txt |

---

## Scripts

| 脚本名 | 说明 |
|--------|------|
| detect-flask.sh | 检测 Flask 框架 |
| extract-flask-patterns.sh | 提取 Flask 代码模式 |

---

## Reference

- [Flask 文档](https://flask.palletsprojects.com/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-Migrate](https://flask-migrate.readthedocs.io/)