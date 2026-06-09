# Results JSON Schema

> **输出文件**：`.claude/context/results.json`
> **生成者**：Architect Agent Stage 0 阶段 B（CB+Skills）、PM Agent Stage 0 阶段 B（PM context 文档）
> **消费者**：阶段 C（Skills / PM context 文档生成）、阶段 D（CB 生成）
> **生命周期**：阶段 B 写入 → 阶段 C/D 读取 → AI 重新组装时可复用
> **SCHEMA_VERSION**：`2.1.0`（2026-06-06 N-rows 重构：从 `2.0.0` 升至此版本；新 `data.questions: QuestionItem[]` 数组承载每原子 question 的执行结果，旧顶层 `fields` / `chapters` / `elements` 降级为可选聚合形式）

---

## Schema 定义

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Architect Stage 0 Query Results",
  "type": "object",
  "required": ["generated_at", "items"],
  "properties": {
    "generated_at": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 时间戳"
    },
    "project": {
      "type": "string",
      "description": "项目名称"
    },
    "items": {
      "type": "object",
      "description": "key 为目标 ID（与 query_plan.md 一致），value 为查询结果",
      "additionalProperties": { "$ref": "#/definitions/ResultItem" }
    },
    "summary": {
      "type": "object",
      "description": "执行汇总统计",
      "properties": {
        "total": { "type": "integer" },
        "success": { "type": "integer" },
        "fallback_used": { "type": "integer" },
        "no_data": { "type": "integer" },
        "failed": { "type": "integer" }
      }
    }
  },
  "definitions": {
    "ResultItem": {
      "type": "object",
      "required": ["type", "status"],
      "properties": {
        "type": {
          "type": "string",
          "enum": ["cb_section", "skill", "project_section", "tech_stack_section", "feature_elements_section"],
          "description": "结果类型：一致性基线章节 / Skill / PM 上下文文档章节（3 种）。其中 PM 上下文章节由 PM-Stage0 在模式 C 重构后新增（2026-06-05）。"
        },
        "template_ref": {
          "type": "string",
          "description": "模板来源引用，如 consistency-baseline-template.md#4.1 或 project-infra-database/SKILL.md"
        },
        "query": {
          "type": "string",
          "description": "实际执行的 graphify query（含扩展后的 tokens）"
        },
        "fallback_used": {
          "type": "boolean",
          "description": "是否使用了 bash fallback"
        },
        "fallback_query": {
          "type": "string",
          "description": "如果用了 fallback，记录原始 bash 命令"
        },
        "status": {
          "type": "string",
          "enum": ["success", "fallback", "no_data", "failed"],
          "description": "执行状态"
        },
        "executed_at": {
          "type": "string",
          "format": "date-time"
        },
        "data": {
          "type": "object",
          "description": "查询返回的结构化数据。结构因 type 而异，详见下方 Data 子 schema。**2026-06-06 N-rows 重构后必含 `questions: QuestionItem[]` 数组**——1 item per section 外壳不变，但 data 内部按原子问题（与 query_plan.md 的 parent_section_id 行一一对应）拆分装载。每个 question 的 `data` 字段可独立是 `success` / `fallback` / `no_data` / `failed`，实现细粒度失败表达（旧版 1 行承载 4 个 question，1 个失败全部 no_data）。",
          "properties": {
            "questions": {
              "$ref": "#/definitions/QuestionItem"
            }
          }
        },
        "evidence": {
          "type": "array",
          "items": {
            "type": "string",
            "pattern": "^[\\w./-]+:\\d+(-\\d+)?$"
          },
          "description": "证据引用列表，格式 file:line 或 file:line-line"
        },
        "snippets": {
          "type": "object",
          "description": "代码片段 map（仅 type=skill 有效）。key 是 path:line-line，value 是从源码文件提取的实际代码内容。精炼阶段 2026-06-06 新增。",
          "additionalProperties": {
            "type": "string",
            "minLength": 1,
            "maxLength": 5000
          },
          "examples": [
            {
              "src/db/config.py:15-25": "engine = create_engine(\n    DATABASE_URL,\n    pool_size=10,\n    max_overflow=20\n)",
              "src/db/session.py:30-45": "with session.begin():\n    ...\n    session.commit()\n    ...\n"
            }
          ]
        },
        "notes": {
          "type": "string",
          "description": "执行备注（如「词表无匹配，已降级到 bash」）"
        }
      }
    },
    "QuestionItem": {
      "type": "object",
      "description": "query_plan.md 中一个原子的 question 的执行结果（N-rows 重构 2026-06-06 新增）",
      "required": ["key", "question", "query", "status", "data", "executed_at"],
      "properties": {
        "key": {
          "type": "string",
          "description": "question 唯一键，通常是 `parent_section_id` + `_q` + `question_index`（如 `cb_1_1_q2`）",
          "pattern": "^[a-z_0-9]+_q\\d+$"
        },
        "question": {
          "type": "string",
          "description": "原子的中文问题短句（与 query_plan.md 调查项列一致）"
        },
        "query": {
          "type": "string",
          "description": "实际执行的 graphify query（含扩展后的 tokens）"
        },
        "fallback_used": {
          "type": "boolean",
          "description": "是否使用了 bash fallback"
        },
        "fallback_query": {
          "type": "string",
          "description": "如果用了 fallback，记录原始 bash 命令"
        },
        "status": {
          "type": "string",
          "enum": ["success", "fallback", "no_data", "failed"],
          "description": "该 question 的执行状态（独立于其他 question）"
        },
        "executed_at": {
          "type": "string",
          "format": "date-time"
        },
        "data": {
          "type": "object",
          "description": "该 question 的返回数据。结构自由——单值字段（如 `name: 'Mefan'`）或带源的对象（如 `{field: 'name', value: 'Mefan', source: 'package.json:5'}`）。**下游组装时按 parent_section_id 聚合多个 question 的 data 字段填模板**。"
        },
        "evidence": {
          "type": "array",
          "items": {
            "type": "string",
            "pattern": "^[\\w./-]+:\\d+(-\\d+)?$"
          },
          "description": "证据引用列表，格式 file:line 或 file:line-line"
        },
        "snippets": {
          "type": "object",
          "description": "代码片段 map（仅 type=skill 且该 question 命中 Code Target 时有效）。结构同顶层 snippets 字段。",
          "additionalProperties": {
            "type": "string",
            "minLength": 1,
            "maxLength": 5000
          }
        },
        "notes": {
          "type": "string",
          "description": "该 question 的执行备注"
        }
      }
    }
  }
}
```

---

## Data 子 Schema

### cb_section 类型

> **N-rows 重构（2026-06-06）后 `fields` 字段为可选项**：优先用 `questions[]` 数组承载每个 question 的独立返回值（细粒度失败）。`fields` 仅在阶段 C/D 直接聚合时**作为便捷聚合形式**保留（即 `fields = {project_name: 'Mefan', ...}` 等价于 `questions[*].data` 合并去重后的视图）。

```json
{
  "section_id": "1.1",
  "section_title": "项目元数据",
  "questions": [
    {
      "key": "cb_1_1_q1",
      "question": "项目名称",
      "query": "graphify query \"project name\"",
      "status": "success",
      "data": { "name": "Mefan", "source": "package.json:5" },
      "evidence": ["package.json:5"]
    },
    {
      "key": "cb_1_1_q2",
      "question": "项目版本",
      "query": "graphify query \"project version\"",
      "status": "success",
      "data": { "version": "0.1.0", "source": "package.json:6" },
      "evidence": ["package.json:6"]
    },
    {
      "key": "cb_1_1_q3",
      "question": "前端框架",
      "query": "graphify query \"frontend framework react vue angular\"",
      "fallback_used": true,
      "fallback_query": "grep -E '\"(react|vue|angular)\"' package.json",
      "status": "fallback",
      "data": { "framework": "react", "version": "18.2.0" },
      "evidence": ["package.json:12"]
    },
    {
      "key": "cb_1_1_q4",
      "question": "后端框架",
      "query": "graphify query \"backend framework fastapi django express\"",
      "status": "success",
      "data": { "framework": "fastapi", "version": "0.110.0" },
      "evidence": ["pyproject.toml:15"]
    }
  ],
  "fields": {
    "project_name": "Mefan",
    "project_version": "0.1.0",
    "project_type": "fullstack",
    "frontend_framework": "react",
    "backend_framework": "fastapi"
  },
  "raw_nodes": [
    {
      "id": "package_metadata",
      "label": "Mefan package.json",
      "source_file": "package.json",
      "source_location": "L1-50"
    }
  ]
}
```

### skill 类型

> **N-rows 重构（2026-06-06）后约定**：
> - 1 FE = 1 row（保持 1:1）→ `questions` 数组通常只含 1 个 question（`parent_section_id = target_id`，`question_index = 1`）
> - **`snippets` 字段下移到 `questions[0].snippets`**——便于按 question 粒度携带代码片段，不再顶层
> - `chapters` 字段保留为可选项（阶段 C AI 组装 SKILL.md 时**聚合** `questions[*].data` 填章节；与 `fields` 同理，是便捷聚合视图）

```json
{
  "fe_id": "FE-I-001",
  "fe_name_zh": "数据库",
  "template_used": "project-infra-database",
  "template_tier": "一级（特化）",
  "questions": [
    {
      "key": "skill_infra_database_q1",
      "question": "数据库连接配置 + 事务处理 + 代码样例",
      "query": "graphify query \"database connection configuration\"",
      "status": "success",
      "data": {
        "概述": "项目使用 PostgreSQL + SQLAlchemy 2.0...",
        "数据源配置": {
          "connection_string": "postgresql://localhost:5432/mefan",
          "pool_size": 10,
          "source": "src/db/config.py:15-25"
        },
        "事务处理": {
          "default_isolation": "READ_COMMITTED",
          "rollback_for": ["Exception"],
          "source": "src/db/session.py:30-45"
        },
        "代码样例": [
          "src/models/base.py:1-30",
          "src/db/session.py:1-50"
        ]
      },
      "snippets": {
        "src/db/config.py:15-25": "engine = create_engine(\n    DATABASE_URL,\n    pool_size=10,\n    max_overflow=20\n)",
        "src/db/session.py:30-45": "with session.begin():\n    try:\n        ...\n        session.commit()\n    except Exception:\n        session.rollback()\n        raise\n"
      },
      "evidence": ["src/db/config.py:1-30", "src/db/session.py:1-50"]
    }
  ],
  "chapters": {
    "概述": "项目使用 PostgreSQL + SQLAlchemy 2.0...",
    "数据源配置": {
      "connection_string": "postgresql://localhost:5432/mefan",
      "pool_size": 10,
      "source": "src/db/config.py:15-25"
    },
    "事务处理": {
      "default_isolation": "READ_COMMITTED",
      "rollback_for": ["Exception"],
      "source": "src/db/session.py:30-45"
    },
    "代码样例": [
      "src/models/base.py:1-30",
      "src/db/session.py:1-50"
    ]
  },
  "raw_nodes": [
    {
      "id": "db_config",
      "label": "DatabaseConfig",
      "source_file": "src/db/config.py",
      "source_location": "L15"
    }
  ]
}
```

**snippets 字段语义**：
- **来源**：arch-stage0 阶段 B 2.5.5 用 `sed -n "${start},${end}p" $ROOT/$path` 提取
- **触发条件**：query_plan.md 该行 `Code Target` 列非空
- **失败标记**：文件不存在 → `[SNIPPET_FETCH_FAILED: file not found]`；行范围空 → `[SNIPPET_FETCH_FAILED: empty range]`
- **大小保护**：单 snippet > 100 行截断并标 `[TRUNCATED]`；单 skill snippets 总量 > 500 行截断最末几个
- **下游使用**：阶段 C 2.6.4 决定是否升级为 Pattern C + 生成 `examples.md`
- **不需要此字段的类型**：`cb_section` / `project_section` / `tech_stack_section` / `feature_elements_section`（仅 `skill` 类型用）

### project_section 类型（PM-Stage0 用，新增 2026-06-05）

> **用途**：阶段 C 组装 `.claude/context/project.md` 时使用。`fields` 字典的 key 直接对应模板中的中文字段名（`项目名称`、`项目类型` 等）。
>
> **N-rows 重构（2026-06-06）**：每个章节的每个 question 独立装在 `questions[]` 数组。`fields` 保留为可选项（聚合视图）。

```json
{
  "section_id": "1.1",
  "section_title": "项目总体介绍",
  "questions": [
    {
      "key": "doc_project_s_1_1_q1",
      "question": "项目名称",
      "query": "graphify query \"project name\"",
      "status": "success",
      "data": { "项目名称": "Mefan", "source": "package.json:5" },
      "evidence": ["package.json:5"]
    },
    {
      "key": "doc_project_s_1_1_q2",
      "question": "项目类型/分类",
      "query": "graphify query \"project type category\"",
      "status": "success",
      "data": { "项目类型": "二次开发（Harness 框架升级）" },
      "evidence": ["pyproject.toml:3"]
    },
    {
      "key": "doc_project_s_1_1_q3",
      "question": "核心功能概述",
      "status": "fallback",
      "fallback_query": "cat README.md | head -50",
      "data": { "核心功能概述": "框架初始化 + 知识图谱 + 技能管理 + 迭代管理" },
      "evidence": ["README.md:1-30"]
    }
  ],
  "fields": {
    "项目名称": "Mefan",
    "项目类型": "二次开发（Harness 框架升级）",
    "核心功能概述": "框架初始化 + 知识图谱 + 技能管理 + 迭代管理",
    "项目背景": "Harness 框架版本升级迭代"
  },
  "raw_nodes": [
    {
      "id": "package_metadata",
      "label": "Mefan package.json",
      "source_file": "package.json",
      "source_location": "L1-50"
    }
  ]
}
```

### tech_stack_section 类型（PM-Stage0 用，新增 2026-06-05）

> **用途**：阶段 C 组装 `.claude/context/tech-stack-profile.md` 时使用。`fields` 字典的 key 对应模板的"组件"行（如"CORS"、"Helmet"、"Docker"）。
>
> **N-rows 重构（2026-06-06）**：每个中间件/组件独立一个 question。`fields` 保留为可选项（聚合视图）。

```json
{
  "section_id": "2.2",
  "section_title": "中间件",
  "questions": [
    {
      "key": "doc_tech_s_2_2_q1",
      "question": "CORS 中间件",
      "query": "graphify query \"CORS middleware\"",
      "status": "success",
      "data": { "CORS": "django-cors-headers 4.0.0" },
      "evidence": ["config/settings.py:48"]
    },
    {
      "key": "doc_tech_s_2_2_q2",
      "question": "Helmet 安全头",
      "status": "no_data",
      "data": { "Helmet": "未使用" },
      "notes": "graphify + grep 均无匹配（项目为 Django 后端，未引入 helmet）"
    },
    {
      "key": "doc_tech_s_2_2_q3",
      "question": "Compression 压缩",
      "query": "graphify query \"compression middleware\"",
      "status": "fallback",
      "fallback_query": "grep -rn \"compression\" --include=\"*.py\"",
      "data": { "Compression": "gzip middleware" },
      "evidence": ["config/settings.py:55"]
    }
  ],
  "fields": {
    "CORS": "django-cors-headers 4.0.0",
    "Helmet": "未使用",
    "Compression": "gzip middleware",
    "日志": "Python logging + Sentry",
    "验证": "DRF serializers"
  },
  "raw_nodes": [
    {
      "id": "middleware_config",
      "label": "MIDDLEWARE setting",
      "source_file": "config/settings.py",
      "source_location": "L45-60"
    }
  ]
}
```

### feature_elements_section 类型（PM-Stage0 用，新增 2026-06-05）

> **用途**：阶段 C 组装 `.claude/context/feature-elements.md` 时使用。`elements` 数组每项对应模板的 FE 行（FE-I-* / FE-D-* / FE-A-* / FE-F-* / BS-*）。注意：`elements` 与 `raw_nodes` 互补——`elements` 是模板表格行，`raw_nodes` 是 graphify 节点。
>
> **N-rows 重构（2026-06-06）特殊约定**：`feature_elements_section` 章节保持 **1 FE = 1 row**（不展开元数据字段，避免 N×M 爆炸）。`questions` 数组通常只含 1 个 question，包含该 FE 的所有元数据（聚合在 `data.elements[]` 或散列字段）。`elements` 字段保留为可选项（聚合视图，下游阶段 C 直接用）。

```json
{
  "section_id": "3.1",
  "section_title": "L1 基础设施层",
  "questions": [
    {
      "key": "doc_feature_s_3_1_q1",
      "question": "L1 基础设施层元数据（DB/Cache/MQ 等 FE）",
      "query": "graphify query \"database cache message queue\"",
      "status": "success",
      "data": {
        "elements": [
          {
            "id": "FE-I-001",
            "name_zh": "数据库（DB）",
            "tech_detected": "PostgreSQL 15",
            "category": "infrastructure",
            "dependency_source": "pyproject.toml:psycopg[binary]>=3.1",
            "code_ref": "config/settings.py:78-95"
          },
          {
            "id": "FE-I-002",
            "name_zh": "缓存（Cache）",
            "tech_detected": "Redis 7",
            "category": "infrastructure",
            "dependency_source": "pyproject.toml:redis>=5.0",
            "code_ref": "config/settings.py:88-95"
          },
          {
            "id": "FE-I-005",
            "name_zh": "消息队列（MessageQueue）",
            "tech_detected": "[未检测到]",
            "category": "infrastructure",
            "dependency_source": "",
            "code_ref": ""
          }
        ]
      },
      "evidence": ["pyproject.toml:12", "config/settings.py:78"]
    }
  ],
  "elements": [
    {
      "id": "FE-I-001",
      "name_zh": "数据库（DB）",
      "tech_detected": "PostgreSQL 15",
      "category": "infrastructure",
      "dependency_source": "pyproject.toml:psycopg[binary]>=3.1",
      "code_ref": "config/settings.py:78-95"
    },
    {
      "id": "FE-I-002",
      "name_zh": "缓存（Cache）",
      "tech_detected": "Redis 7",
      "category": "infrastructure",
      "dependency_source": "pyproject.toml:redis>=5.0",
      "code_ref": "config/settings.py:88-95"
    },
    {
      "id": "FE-I-005",
      "name_zh": "消息队列（MessageQueue）",
      "tech_detected": "[未检测到]",
      "category": "infrastructure",
      "dependency_source": "",
      "code_ref": ""
    }
  ],
  "raw_nodes": [
    {
      "id": "psycopg_dep",
      "label": "psycopg[binary]>=3.1",
      "source_file": "pyproject.toml",
      "source_location": "L12"
    }
  ],
  "notes": "FE-I-005 消息队列未检测到任何技术依赖，按 [需人工补充] 处理"
}
```

---

## 完整示例

```json
{
  "generated_at": "2026-06-05T10:30:00+08:00",
  "project": "Mefan",
  "items": {
    "cb_1_1": {
      "type": "cb_section",
      "template_ref": "consistency-baseline-template.md#1.1",
      "query": "graphify query \"project metadata package version\"",
      "fallback_used": false,
      "status": "success",
      "executed_at": "2026-06-05T10:30:01+08:00",
      "data": {
        "section_id": "1.1",
        "section_title": "项目元数据",
        "fields": {
          "project_name": "Mefan",
          "project_version": "0.1.0",
          "project_type": "fullstack",
          "frontend_framework": "react",
          "backend_framework": "fastapi"
        }
      },
      "evidence": ["package.json:1-10", "pyproject.toml:1-20"]
    },
    "skill_infra_database": {
      "type": "skill",
      "template_ref": "project-infra-database/SKILL.md",
      "query": "graphify query \"database connection configuration ORM\"",
      "fallback_used": false,
      "status": "success",
      "executed_at": "2026-06-05T10:30:05+08:00",
      "data": {
        "fe_id": "FE-I-001",
        "fe_name_zh": "数据库",
        "template_used": "project-infra-database",
        "template_tier": "一级（特化）",
        "chapters": {
          "数据源配置": {
            "engine": "SQLAlchemy 2.0",
            "dialect": "postgresql",
            "pool_size": 10
          },
          "事务处理": {
            "isolation": "READ_COMMITTED",
            "autocommit": false
          }
        }
      },
      "evidence": ["src/db/config.py:1-30", "src/db/session.py:1-50"]
    },
    "skill_infra_message_queue": {
      "type": "skill",
      "template_ref": "project-infra-message-queue/SKILL.md",
      "query": "graphify query \"message queue rabbitmq kafka\"",
      "fallback_used": true,
      "fallback_query": "grep -rn 'pika\\|kafka\\|RabbitMQ' --include='*.py' .",
      "status": "fallback",
      "executed_at": "2026-06-05T10:30:10+08:00",
      "data": {
        "fe_id": "FE-I-005",
        "fe_name_zh": "消息队列",
        "template_used": "project-infra-message-queue",
        "template_tier": "一级（特化）",
        "chapters": {
          "使用情况": "项目当前未使用消息队列"
        }
      },
      "evidence": [],
      "notes": "graphify 返回空（词表无匹配），降级到 bash 确认无引用"
    },
    "doc_project_s_1_1": {
      "type": "project_section",
      "template_ref": "project-template.md#1.1",
      "query": "graphify query \"project metadata name type\"",
      "fallback_used": false,
      "status": "success",
      "executed_at": "2026-06-05T10:30:15+08:00",
      "data": {
        "section_id": "1.1",
        "section_title": "项目总体介绍",
        "fields": {
          "项目名称": "Mefan",
          "项目类型": "二次开发（Harness 框架升级）",
          "核心功能概述": "框架初始化 + 知识图谱 + 技能管理 + 迭代管理",
          "项目背景": "Harness 框架 v2.4.1 → v3.x 升级"
        }
      },
      "evidence": ["package.json:1-10", "pyproject.toml:1-20"]
    },
    "doc_tech_s_2_1": {
      "type": "tech_stack_section",
      "template_ref": "tech-stack-profile-template.md#2.1",
      "query": "graphify query \"React Vue Angular frontend framework\"",
      "fallback_used": false,
      "status": "success",
      "executed_at": "2026-06-05T10:30:20+08:00",
      "data": {
        "section_id": "2.1",
        "section_title": "核心框架（前端）",
        "fields": {
          "框架": "Vue 3.4",
          "框架版本": "3.4.21"
        }
      },
      "evidence": ["package.json:5"]
    },
    "doc_feature_s_3_1": {
      "type": "feature_elements_section",
      "template_ref": "feature-elements-template.md#3.1",
      "query": "graphify query \"database cache message queue\"",
      "fallback_used": true,
      "fallback_query": "grep -E 'psycopg|redis|pika' pyproject.toml",
      "status": "fallback",
      "executed_at": "2026-06-05T10:30:25+08:00",
      "data": {
        "section_id": "3.1",
        "section_title": "L1 基础设施层",
        "elements": [
          {
            "id": "FE-I-001",
            "name_zh": "数据库（DB）",
            "tech_detected": "PostgreSQL 15",
            "category": "infrastructure",
            "dependency_source": "pyproject.toml:psycopg[binary]>=3.1",
            "code_ref": "config/settings.py:78-95"
          },
          {
            "id": "FE-I-005",
            "name_zh": "消息队列（MessageQueue）",
            "tech_detected": "[未检测到]",
            "category": "infrastructure",
            "dependency_source": "",
            "code_ref": ""
          }
        ]
      },
      "evidence": ["pyproject.toml:12", "config/settings.py:78"],
      "notes": "FE-I-005 消息队列：grep 0 命中，按 [需人工补充] 处理"
    }
  },
  "summary": {
    "total": 25,
    "success": 18,
    "fallback_used": 5,
    "no_data": 2,
    "failed": 0
  }
}
```

---

## 状态语义

| status | 含义 | 阶段 C/D 行为 |
|--------|------|---------------|
| `success` | graphify 返回有效数据 | 直接使用 data 撰写文档 |
| `fallback` | graphify 失败但 bash 找到数据 | 用 bash 结果撰写，标注 `[BASH_FALLBACK]` |
| `no_data` | 两者都失败或无匹配 | 章节写 `[需人工补充]`，禁止编造 |
| `failed` | 命令执行错误（如 graph.json 损坏） | 阶段 C/D 跳过该章节，提示修复 |

---

## 验证规则

阶段 B 完成后，AI 验证：

1. **覆盖率**：items 数量 = query_plan.md 中所有**唯一 parent_section_id** 的数量（即"去重后的章节数"）。**注意**：items 是 1-per-section 外壳，**不是 1-per-row**——query_plan.md 可能有 ~50 行，但 items 仍约 ~30（去重后）。
2. **必填项**：每个 item 都有 type + status + data.questions（questions.length ≥ 1）
3. **证据格式**：evidence 数组元素必须匹配 `file:line` 或 `file:line-line`（每个 question 自己的 evidence 独立检查）
4. **summary 一致性**：summary 数字相加 = total（**注意**：summary 的计数粒度应改为 question 级别：`total` = 所有 items 的 `data.questions.length` 之和）
5. **失败率**：`failed + no_data` 比例应 < 20%（按 question 计数）
6. **N-rows 不变量（N-rows 重构 2026-06-06 新增）**：对每个 item，**`data.questions.length` 必须等于 query_plan.md 中 `parent_section_id` 等于该 item key（去掉 `_qN` 后缀）的行数**。例如：query_plan.md 里 `cb_1_1` 下有 4 行（`_q1/_q2/_q3/_q4`）→ results.json 里 `items.cb_1_1.data.questions.length == 4`。
7. **唯一性不变量**：每个 question 的 `key` 在整个 results.json 中**唯一**（避免 `_qN` 序号冲突）
8. **legacy chapter-level data 检测**：items[*].data 下**不应**有顶层 `fields` / `chapters` / `elements`（这些字段在 N-rows 重构后应**仅作为便捷聚合形式**存在；如检测到顶层出现且缺 questions[]，则视为未完成迁移）

不通过则返回阶段 A 调整 query。

---

## 与其他文件的关系

- **输入**：`.claude/context/query_plan.md`
- **被引用**：
  - 阶段 C：每个 skill_* 项 → 生成一个 SKILL.md（architect-stage0），聚合 `data.questions[*].data` + `data.questions[*].snippets` 填 SKILL.md 章节
  - 阶段 D：每个 cb_* 项 → 生成 CB 的对应章节（architect-stage0），聚合 `data.questions[*].data` 填模板字段
  - **PM-Stage0 阶段 C：每个 doc_project_* / doc_tech_* / doc_feature_* 项 → 生成 project.md / tech-stack-profile.md / feature-elements.md 的对应章节（2026-06-05 新增）**；N-rows 重构后聚合 `data.questions[*].data` 填中文 key 字段
- **缓存策略**：模板或 feature-elements 不变时可复用，避免重跑 graphify
- **schema 版本**：query_plan.md 头部声明 `SCHEMA_VERSION` 应与本 schema 顶部一致（2026-06-06 N-rows 重构引入，从 `2.0.0` → `2.1.0`）
