#!/bin/bash
# generate-naming-skill.sh - 动态生成 Naming Convention Skills
# 通过 Graphify 查询项目的实际命名模式生成

set -e

SKILLS_DIR="$1"
ROOT="$2"

if [ -z "$SKILLS_DIR" ] || [ -z "$ROOT" ]; then
    echo "Usage: generate-naming-skill.sh <SKILLS_DIR> <ROOT>"
    exit 1
fi

echo "[generate-naming-skill] 开始生成 Naming Convention Skills..."

# =============================================
# 1. 查询项目的文件命名模式
# =============================================
echo "[generate-naming-skill] 查询文件命名模式..."
FILE_NAMING=$(graphify query "What are the file naming patterns in this project (camelCase, snake_case, kebab-case)?" 2>/dev/null | head -50 || echo "{动态检测}")

# =============================================
# 2. 查询项目的目录结构
# =============================================
echo "[generate-naming-skill] 查询目录结构..."
DIRECTORY_STRUCTURE=$(graphify query "What is the directory structure of this project and what are the responsibilities of each directory?" 2>/dev/null | head -80 || echo "{动态检测}")

# =============================================
# 3. 查询项目的变量/函数命名规范
# =============================================
echo "[generate-naming-skill] 查询命名规范..."
NAMING_CONVENTIONS=$(graphify query "What naming conventions are used in this project for variables, functions, classes?" 2>/dev/null | head -80 || echo "{动态检测}")

# =============================================
# 4. 查询模块组织方式
# =============================================
echo "[generate-naming-skill] 查询模块组织..."
MODULE_ORG=$(graphify query "How are modules organized in this project? What is the module dependency structure?" 2>/dev/null | head -80 || echo "{动态检测}")

# =============================================
# 生成 project-naming-convention.md
# =============================================
echo "[generate-naming-skill] 生成 project-naming-convention.md..."

cat > "$SKILLS_DIR/project-naming-convention.md" << EOF
# Naming Convention（命名规范）

> **路径**：\`.claude/skills/project-naming-convention.md\`
> **用途**：项目命名规范，供 Dev Agent 遵守
> **来源**：由 Architect Agent 通过 Graphify 分析项目代码动态生成
> **生成时间**：$(date +%Y-%m-%d)

---

## Skill 元数据

\`\`\`yaml
name: project-naming-convention
name_zh: 命名规范
category: naming-convention
version: 1.0.0
author: Architect Agent
created: $(date +%Y-%m-%d)
trigger: auto-generate
\`\`\`

---

## 1. Graphify 分析结果

### 1.1 项目使用的命名模式

\`\`\`
$FILE_NAMING
\`\`\`

### 1.2 命名规范详情

\`\`\`
$NAMING_CONVENTIONS
\`\`\`

---

## 2. 文件命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| TypeScript/JS | {动态检测} | {动态检测} |
| Python | {动态检测} | {动态检测} |
| Java/Kotlin | {动态检测} | {动态检测} |
| React/Vue 组件 | {动态检测} | {动态检测} |
| 配置文件 | {动态检测} | {动态检测} |
| 测试文件 | {动态检测} | {动态检测} |

---

## 3. 变量/函数命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 变量 | {动态检测} | {动态检测} |
| 常量 | {动态检测} | {动态检测} |
| 函数/方法 | {动态检测} | {动态检测} |
| 类名 | {动态检测} | {动态检测} |
| 接口名 | {动态检测} | {动态检测} |
| Hooks | {动态检测} | {动态检测} |

---

## 4. 数据库命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 表名 | {动态检测} | {动态检测} |
| 列名 | {动态检测} | {动态检测} |
| 索引名 | {动态检测} | {动态检测} |
| 外键名 | {动态检测} | {动态检测} |

---

## 5. API 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| RESTful 路径 | {动态检测} | {动态检测} |
| GraphQL | {动态检测} | {动态检测} |

---

## 6. 与其他 Skill 的关系

\`\`\`yaml
depends_on: []
provides_to:
  - dev-stage4
  - project-feature-*
\`\`\`
EOF

# =============================================
# 生成 project-directory-structure.md
# =============================================
echo "[generate-naming-skill] 生成 project-directory-structure.md..."

cat > "$SKILLS_DIR/project-directory-structure.md" << EOF
# Directory Structure（目录结构规范）

> **路径**：\`.claude/skills/project-directory-structure.md\`
> **用途**：项目目录结构规范，供 Dev Agent 遵守
> **来源**：由 Architect Agent 通过 Graphify 分析项目代码动态生成
> **生成时间**：$(date +%Y-%m-%d)

---

## Skill 元数据

\`\`\`yaml
name: project-directory-structure
name_zh: 目录结构规范
category: naming-convention
version: 1.0.0
author: Architect Agent
created: $(date +%Y-%m-%d)
trigger: auto-generate
\`\`\`

---

## 1. 项目目录结构

\`\`\`
$DIRECTORY_STRUCTURE
\`\`\`

---

## 2. 目录职责说明

| 目录 | 职责 | 说明 |
|------|------|------|
| {动态检测} | {动态检测} | {动态检测} |

---

## 3. 目录组织原则

| 原则 | 说明 |
|------|------|
| 单一职责 | 每个目录只负责一类功能 |
| 领域驱动 | 按业务领域组织代码 |
| 层级清晰 | 按 L1-L4 层次结构组织 |

---

## 4. 与其他 Skill 的关系

\`\`\`yaml
depends_on:
  - project-naming-convention
provides_to:
  - dev-stage4
  - project-feature-*
\`\`\`
EOF

# =============================================
# 生成 project-module-organization.md
# =============================================
echo "[generate-naming-skill] 生成 project-module-organization.md..."

cat > "$SKILLS_DIR/project-module-organization.md" << EOF
# Module Organization（模块组织规范）

> **路径**：\`.claude/skills/project-module-organization.md\`
> **用途**：模块组织与依赖管理规范
> **来源**：由 Architect Agent 通过 Graphify 分析项目代码动态生成
> **生成时间**：$(date +%Y-%m-%d)

---

## Skill 元数据

\`\`\`yaml
name: project-module-organization
name_zh: 模块组织规范
category: naming-convention
version: 1.0.0
author: Architect Agent
created: $(date +%Y-%m-%d)
trigger: auto-generate
\`\`\`

---

## 1. 模块组织分析

\`\`\`
$MODULE_ORG
\`\`\`

---

## 2. 模块组织原则

| 原则 | 说明 |
|------|------|
| 单一职责 | 每个模块只负责一个功能 |
| 依赖单向 | 上层依赖下层，禁止反向依赖 |
| 领域驱动 | 按业务领域划分模块 |
| 接口隔离 | 依赖接口而非实现 |

---

## 3. 模块依赖规则

\`\`\`
{动态检测}
\`\`\`

---

## 4. 与其他 Skill 的关系

\`\`\`yaml
depends_on:
  - project-naming-convention
  - project-directory-structure
provides_to:
  - dev-stage4
  - project-feature-*
\`\`\`
EOF

echo "[generate-naming-skill] Naming Convention Skills 生成完成"
