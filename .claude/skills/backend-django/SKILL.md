# Skill 元数据

```yaml
name: backend-django
name_zh: 后端 Django 框架调查
category: backend
framework: django
version: 1.0.0
author: Architect Agent
created: 2026-05-22
trigger: auto-detect
trigger_files:
  - requirements.txt (contains "django")
  - manage.py
  - settings.py
```

---

## 1. 框架概述

| 项目 | 内容 |
|------|------|
| **框架版本** | Django 5.x |
| **核心作用** | 全功能 Web 框架 |
| **ORM** | Django ORM |
| **Admin** | 内置 Admin 站点 |

---

## 2. 目录结构规范

```
project/
├── manage.py
├── project/
│   ├── __init__.py
│   ├── settings.py      # 配置
│   ├── urls.py          # URL 配置
│   └── wsgi.py
└── apps/
    └── {app}/
        ├── __init__.py
        ├── models.py    # 数据模型
        ├── views.py     # 视图
        ├── urls.py      # 应用路由
        ├── serializers.py # DRF 序列化
        ├── services.py   # 业务逻辑
        ├── admin.py      # Admin 配置
        └── tests.py      # 测试
```

---

## 3. 核心元素调查清单

### 3.1 Django 项目结构

| 调查项 | 文件位置 | 说明 |
|--------|---------|------|
| settings.py | `project/settings.py` | 配置管理 |
| URL 配置 | `project/urls.py` | 主路由 |
| WSGI/ASGI | `project/wsgi.py` | 部署入口 |

### 3.2 App 与 Model

| 调查项 | 说明 |
|--------|------|
| App 创建 | python manage.py startapp |
| Model 定义 | class Meta |
| 迁移 | makemigrations/migrate |
| QuerySet | ORM 查询 |

### 3.3 视图与路由

| 调查项 | 说明 |
|--------|------|
| FBV vs CBV | 函数视图 vs 类视图 |
| Class-Based Views | ListView/DetailView |
| URL 路由 | path/re_path |
| 装饰器 | @login_required |

### 3.4 REST API (DRF)

| 调查项 | 说明 |
|--------|------|
| Serializer | 序列化器 |
| ViewSet | 视图集 |
| Router | 自动路由生成 |
| 权限 | Permission classes |

---

## 4. 代码样例索引

| 模式 | 文件 | 说明 |
|------|------|------|
| Model | `apps/user/models.py` | Django 模型 |
| ViewSet | `apps/user/views.py` | DRF ViewSet |
| Serializer | `apps/user/serializers.py` | DRF 序列化 |
| URL | `apps/user/urls.py` | 应用路由 |

---

## 5. 命名约定调查

| 调查项 | 关键问题 | 证据文件:行号 |
|--------|---------|--------------|
| **App 命名** | Django app 目录名用下划线还是横线？如 `user_account` vs `user-account` | |
| **Model 类命名** | PascalCase？如 `class UserProfile` | |
| **Model 字段命名** | 下划线还是驼峰？如 `created_at` vs `createdAt` | |
| **View 函数命名** | 函数视图名用下划线？如 `user_list` | |
| **CBV 方法命名** | as_view() 的参数？如 `model = User`, `template_name = '...' ` | |
| **URL name 命名** | `:app:view` 格式？如 `'users:user_list'` | |
| **Serializer 字段命名** | 与 Model 字段一致还是用不同命名风格？ | |
| **Admin 类命名** | ModelAdmin 后缀？如 `UserAdmin` | |
| **测试函数命名** | test_ 前缀 + 下划线？如 `test_user_can_login` | |

---

## 6. 禁止做法（反模式）

| 禁止 | 原因 | 正确做法 | 证据 |
|------|------|---------|------|
| **在 Model 的 `__init__` 中处理业务逻辑** | Django ORM 不会调用 `__init__` | 使用 `save()` 重写或 signals | |
| **使用原始 SQL** | SQL 注入风险，难以维护 | 使用 ORM QuerySet 或参数化查询 | |
| **在 views.py 中直接返回字典** | 缺少模板渲染 | 使用 `render()` 或 DRF Response | |
| **FBV vs CBV 混用** | 代码风格不统一 | 统一使用 CBV 处理复杂逻辑 | |
| **未迁移就运行服务** | Schema 与 Model 不同步 | 始终先 makemigrations/migrate | |
| **在循环中执行数据库查询** | N+1 查询问题 | 使用 `select_related` / `prefetch_related` | |
| **硬编码 URL** | 模板中写死 `/users/` | 使用 `{% url 'users:user_detail' pk=user.pk %}` | |

---

## 7. 常见问题调查

| 调查项 | 关键问题 | 证据文件:行号 |
|--------|---------|--------------|
| **Migrations 管理** | 如何处理 migration 冲突？squash migrations？ | |
| **Manager vs QuerySet** | 自定义 Manager 还是直接在 Model 上定义方法？ | |
| **信号使用** | 是否使用 Django signals？ signals vs signals vs 直接调用 | |
| **CBV Mixins** | 使用哪些 Mixins？如 `LoginRequiredMixin` | |
| **DRF Serializer 嵌套** | 如何处理多层嵌套序列化？ | |
| **Admin 定制** | 是否深度定制 Admin？ModelAdmin 配置 | |
| **测试数据** | 使用 fixtures vs Factory Boy vs pytest-django | |
| **Static files** | 开发环境用 staticfiles，生产环境用 WhiteNoise/CDN | |

---

## 8. 依赖版本调查

| 调查项 | 关键问题 | 证据文件 |
|--------|---------|---------|
| **Django 版本** | Django 4.x 还是 5.x？LTS 版本？ | requirements.txt |
| **Django REST Framework 版本** | DRF 3.14+？最新特性支持情况？ | requirements.txt |
| **ASGI 服务器** | Uvicorn vs Gunicorn + Uvicorn workers？ | requirements.txt |
| **数据库** | PostgreSQL vs MySQL vs SQLite？ | requirements.txt |
| **Celery 版本** | 是否使用异步任务？Django-Celery-Beat？ | requirements.txt |
| **缓存后端** | Redis vs Memcached？django-redis？ | requirements.txt |
| **CORS 库** | django-cors-headers？如何配置？ | requirements.txt |
| **Python 版本** | Django 5.x 要求 Python 3.10+？ | requirements.txt |

---

## Scripts

| 脚本名 | 说明 |
|--------|------|
| detect-django.sh | 检测 Django 框架 |
| extract-django-patterns.sh | 提取 Django 代码模式 |

---

## Reference

- [Django 文档](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django ORM](https://docs.djangoproject.com/en/stable/topics/db/)