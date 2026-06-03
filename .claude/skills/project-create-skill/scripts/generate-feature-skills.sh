#!/bin/bash
# generate-feature-skills.sh - 从 feature-elements.md 生成 Feature Skills
# 读取 L5 业务场景，用 Graphify 查询详情，生成 Feature Skill 文件

set -e

SKILLS_DIR="$1"
ROOT="$2"

if [ -z "$SKILLS_DIR" ] || [ -z "$ROOT" ]; then
    echo "Usage: generate-feature-skills.sh <SKILLS_DIR> <ROOT>"
    exit 1
fi

echo "[generate-feature-skills] 开始生成 Feature Skills..."

FE_FILE="$ROOT/.claude/context/feature-elements.md"

if [ ! -f "$FE_FILE" ]; then
    echo "[generate-feature-skills] feature-elements.md 不存在，跳过生成"
    echo "原因：PM-Stage0 尚未生成 feature-elements.md"
    exit 0
fi

echo "[generate-feature-skills] 读取 feature-elements.md: $FE_FILE"

# =============================================
# 1. 提取 L5 业务场景（Section 3.5 或 Section 5）
# =============================================
echo "[generate-feature-skills] 提取 L5 业务场景..."

# 尝试从 Section 3.5 提取（Business Scene 层）
L5_SCENES=$(grep "^| BS-" "$FE_FILE" 2>/dev/null || echo "")

if [ -z "$L5_SCENES" ]; then
    # 尝试从 Section 5 提取（业务场景层）
    L5_SCENES=$(grep "^| BS-" "$FE_FILE" 2>/dev/null || echo "")
fi

if [ -z "$L5_SCENES" ]; then
    echo "[generate-feature-skills] feature-elements.md 中无 L5 业务场景，跳过 Feature Skills 生成"
    exit 0
fi

echo "[generate-feature-skills] 检测到 L5 业务场景，开始生成..."

# =============================================
# 2. 对每个场景生成 Feature Skill
# =============================================
FEATURE_COUNT=0

echo "$L5_SCENES" | while read -r line; do
    # 解析：| BS-001 | 场景名称 | ...
    SCENE_ID=$(echo "$line" | cut -d'|' -f2 | tr -d ' ' || echo "")
    SCENE_NAME=$(echo "$line" | cut -d'|' -f3 | tr -d ' ' || echo "")

    if [ -z "$SCENE_ID" ] || [ -z "$SCENE_NAME" ]; then
        continue
    fi

    echo "[generate-feature-skills] 处理场景: $SCENE_ID - $SCENE_NAME"

    # 生成 Skill 名称
    SKILL_NAME="project-feature-$(echo $SCENE_NAME | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -d '_')"
    SKILL_FILE="$SKILLS_DIR/$SKILL_NAME.md"

    # 检查是否已存在（如果已存在，跳过）
    if [ -f "$SKILL_FILE" ]; then
        echo "[generate-feature-skills] $SKILL_NAME 已存在，跳过"
        continue
    fi

    # =============================================
    # 3. 使用 Graphify 查询场景详情
    # =============================================
    echo "[generate-feature-skills] Graphify 查询: $SCENE_NAME"

    GRAPHIFY_ENTITIES=$(graphify query "What are the domain entities related to $SCENE_NAME in this project?" 2>/dev/null | head -40 || echo "{待人工补充}")
    GRAPHIFY_SERVICES=$(graphify query "What are the application services that handle $SCENE_NAME?" 2>/dev/null | head -40 || echo "{待人工补充}")
    GRAPHIFY_APIS=$(graphify query "What are the API endpoints for $SCENE_NAME?" 2>/dev/null | head -40 || echo "{待人工补充}")
    GRAPHIFY_FLOWS=$(graphify query "What is the business flow or process for $SCENE_NAME?" 2>/dev/null | head -40 || echo "{待人工补充}")
    GRAPHIFY_RELATIONS=$(graphify query "What are the relationships between components in $SCENE_NAME feature?" 2>/dev/null | head -40 || echo "{待人工补充}")

    # =============================================
    # 4. 生成 Feature Skill 文件
    # =============================================
    cat > "$SKILL_FILE" << EOF
# Feature Skill: $SCENE_NAME

> **路径**：\`.claude/skills/$SKILL_NAME.md\`
> **用途**：$SCENE_NAME 业务功能的开发规范
> **来源**：基于 L5 场景 $SCENE_ID + Graphify 分析动态生成
> **生成时间**：$(date +%Y-%m-%d)

---

## Skill 元数据

\`\`\`yaml
name: $SKILL_NAME
name_zh: $SCENE_NAME
category: feature
subcategory: business-application
version: 1.0.0
author: Architect Agent
created: $(date +%Y-%m-%d)
source: L5 Scene $SCENE_ID
trigger: auto-generate
\`\`\`

---

## 1. Feature 描述

> $SCENE_NAME 的业务描述和核心价值

| 项目 | 内容 |
|------|------|
| **功能名称** | $SCENE_NAME |
| **业务场景** | $SCENE_ID |
| **核心职责** | {待人工补充} |
| **外部依赖** | {待人工补充} |

---

## 2. Feature 组织结构

> $SCENE_NAME 涉及的代码元素及其文件位置

### 2.1 Graphify 分析结果

#### 领域实体
\`\`\`
$GRAPHIFY_ENTITIES
\`\`\`

#### 应用服务
\`\`\`
$GRAPHIFY_SERVICES
\`\`\`

#### API 端点
\`\`\`
$GRAPHIFY_APIS
\`\`\`

#### 业务流程
\`\`\`
$GRAPHIFY_FLOWS
\`\`\`

#### 组件关系
\`\`\`
$GRAPHIFY_RELATIONS
\`\`\`

### 2.2 文件组织结构

```
src/features/{feature-name}/
├── domain/                 # L2 领域层
│   ├── entities/           # 领域实体
│   ├── value-objects/     # 值对象
│   └── services/          # 领域服务
├── application/           # L3 应用层
│   ├── services/          # 应用服务
│   ├── commands/          # 命令
│   └── queries/           # 查询
├── infrastructure/        # L1 基础设施
│   ├── repositories/      # 仓储实现
│   └── external/          # 外部集成
└── interfaces/           # L4 接口层
    ├── controllers/       # 控制器
    ├── routes/            # 路由
    └── dto/               # 数据传输对象
```

---

## 3. Feature 元素关系

> $SCENE_NAME 内部各元素之间的关系

### 3.1 类关系图

\`\`\`mermaid
graph LR
    Controller --> Service
    Service --> Entity
    Service --> Repository
    Repository --> Database
\`\`\`

### 3.2 关系类型

| 关系 | 源 → 目标 | 说明 |
|------|-----------|------|
| **HAS-A** | {待人工补充} | {待人工补充} |
| **IS-A** | {待人工补充} | {待人工补充} |
| **依赖** | {待人工补充} | {待人工补充} |

---

## 4. Feature 状态与 Action

> $SCENE_NAME 的状态机定义和可执行的操作

### 4.1 状态定义

| 状态 | 说明 | 触发条件 |
|------|------|---------|
| {待人工补充} | | |

### 4.2 Action 定义

| Action | 前置条件 | 后置条件 |
|--------|----------|----------|
| {待人工补充} | | |

---

## 5. Feature 数据流

> $SCENE_NAME 的数据流转方式

### 5.1 数据传递方式

| 层级间传递 | 方式 | 说明 |
|------------|------|------|
| L4 → L3 | DTO / Request Object | 接口层传入应用层 |
| L3 → L2 | Domain Object | 应用服务调用领域实体 |
| L2 → L1 | Repository Interface | 领域实体通过仓储持久化 |

### 5.2 数据流图

\`\`\`mermaid
sequenceDiagram
    participant Client
    participant Controller
    participant Service
    participant Entity
    participant Repository
    participant Database

    Client->>Controller: HTTP Request
    Controller->>Service: Command/Query
    Service->>Entity: Domain Operation
    Entity->>Repository: Persist
    Repository->>Database: SQL/NoSQL
\`\`\`

---

## 6. Feature 业务流

> $SCENE_NAME 的核心业务流程

### 6.1 业务流程描述

```
1. {待人工补充}
2. {待人工补充}
```

### 6.2 异常处理流程

| 异常场景 | 处理方式 | 回滚操作 |
|----------|----------|----------|
| {待人工补充} | | |

---

## 7. 使用场景

> 此 Skill 的适用场景和使用说明

| 场景 | 使用方式 |
|------|----------|
| 开发新功能 | 参考此 Skill 的结构和模式 |
| Bug 修复 | 参考此 Skill 的数据流和状态 |
| 代码审查 | 参考此 Skill 的规范检查 |
| 重构 | 参考此 Skill 的元素关系 |

---

## 8. 与其他 Skill 的关系

\`\`\`yaml
depends_on:
  - project-naming-convention
  - project-directory-structure
  - project-module-organization
  - project-workflow-git
provides_to:
  - dev-stage4
\`\`\`
EOF

    echo "[generate-feature-skills] 已生成 $SKILL_NAME"
    FEATURE_COUNT=$((FEATURE_COUNT + 1))
done

echo "[generate-feature-skills] Feature Skills 生成完成，共 $FEATURE_COUNT 个"
