#!/bin/bash
# generate-workflow-skills.sh - 扫描现有 Skills 并分类生成 Workflow Skills
# 扫描 .claude/skills 目录，将非 project-* 的 Skills 分类为 Workflow Skills

set -e

SKILLS_DIR="$1"
ROOT="$2"

if [ -z "$SKILLS_DIR" ] || [ -z "$ROOT" ]; then
    echo "Usage: generate-workflow-skills.sh <SKILLS_DIR> <ROOT>"
    exit 1
fi

echo "[generate-workflow-skills] 开始生成 Workflow Skills..."

# =============================================
# 1. 扫描 .claude/skills 目录
# =============================================
echo "[generate-workflow-skills] 扫描 Skills 目录: $SKILLS_DIR"

# 获取所有非 project-* 的 Skill 文件（排除目录本身）
ALL_SKILLS=$(find "$SKILLS_DIR" -maxdepth 2 -name "SKILL.md" -o -name "*.md" 2>/dev/null | grep -v "/project-" | grep -v "/_templates" || echo "")

# 分类统计
FRONTEND_COUNT=0
BACKEND_COUNT=0
OTHER_COUNT=0

# 收集分类结果
FRONTEND_SKILLS=""
BACKEND_SKILLS=""
OTHER_SKILLS=""

for skill in $ALL_SKILLS; do
    if echo "$skill" | grep -q "frontend"; then
        FRONTEND_SKILLS="$FRONTEND_SKILLS\n$(basename $(dirname $skill))"
        FRONTEND_COUNT=$((FRONTEND_COUNT + 1))
    elif echo "$skill" | grep -q "backend"; then
        BACKEND_SKILLS="$BACKEND_SKILLS\n$(basename $(dirname $skill))"
        BACKEND_COUNT=$((BACKEND_COUNT + 1))
    else
        OTHER_SKILLS="$OTHER_SKILLS\n$skill"
        OTHER_COUNT=$((OTHER_COUNT + 1))
    fi
done

echo "[generate-workflow-skills] 扫描结果：前端=$FRONTEND_COUNT, 后端=$BACKEND_COUNT, 其他=$OTHER_COUNT"

# =============================================
# 2. 生成 project-workflow-git.md
# =============================================
echo "[generate-workflow-skills] 生成 project-workflow-git.md..."

cat > "$SKILLS_DIR/project-workflow-git.md" << EOF
# Git Workflow（Git 工作流）

> **路径**：\`.claude/skills/project-workflow-git.md\`
> **用途**：Git 工作流规范
> **来源**：通用规范
> **生成时间**：$(date +%Y-%m-%d)

---

## Skill 元数据

\`\`\`yaml
name: project-workflow-git
name_zh: Git 工作流
category: workflow
subcategory: development
version: 1.0.0
author: Architect Agent
created: $(date +%Y-%m-%d)
trigger: auto-generate
\`\`\`

---

## 1. 分支策略

| 分支类型 | 命名规则 | 合并目标 |
|----------|----------|----------|
| main/master | 主分支 | - |
| develop | 开发分支 | main |
| feature/* | 功能分支 | develop |
| fix/* | 修复分支 | develop/main |
| hotfix/* | 热修复分支 | main |

---

## 2. 工作流程

```
1. 从 develop 创建 feature 分支
2. 在 feature 分支开发
3. 提交 PR 到 develop
4. Code Review 通过后合并
5. 迭代结束时合并到 main
```

---

## 3. Commit 规范

遵循 Conventional Commits 格式：
\`\`\`
<type>(<scope>): <description>

[optional body]
[optional footer]
\`\`\`

| 类型 | 说明 | 示例 |
|------|------|------|
| feat | 新功能 | \`feat(auth): add login with JWT\` |
| fix | Bug 修复 | \`fix(order): fix quantity validation\` |
| docs | 文档变更 | \`docs: update README\` |
| refactor | 重构 | \`refactor(user): extract validation\` |
| test | 测试 | \`test: add unit tests for auth\` |
| chore | 构建/工具 | \`chore: update dependencies\` |

---

## 4. 与其他 Skill 的关系

\`\`\`yaml
depends_on: []
provides_to:
  - dev-stage4
\`\`\`
EOF

# =============================================
# 3. 生成 project-workflow-tdd.md
# =============================================
echo "[generate-workflow-skills] 生成 project-workflow-tdd.md..."

cat > "$SKILLS_DIR/project-workflow-tdd.md" << EOF
# TDD Workflow（测试驱动开发）

> **路径**：\`.claude/skills/project-workflow-tdd.md\`
> **用途**：TDD 开发流程规范
> **来源**：通用规范
> **生成时间**：$(date +%Y-%m-%d)

---

## Skill 元数据

\`\`\`yaml
name: project-workflow-tdd
name_zh: TDD 开发流程
category: workflow
subcategory: development
version: 1.0.0
author: Architect Agent
created: $(date +%Y-%m-%d)
trigger: auto-generate
\`\`\`

---

## 1. TDD 流程

| 阶段 | 说明 | 原则 |
|------|------|------|
| **Red** | 先写测试，测试失败 | 测试驱动开发 |
| **Green** | 写最简代码让测试通过 | 最小化实现 |
| **Refactor** | 重构代码 | 持续改进 |

---

## 2. 测试组织结构

\`\`\`
tests/
├── unit/          # 单元测试
├── integration/   # 集成测试
└── e2e/          # 端到端测试
\`\`\`

---

## 3. 测试命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 测试文件 | \`*.test.ts\` / \`test_*.py\` | \`user.test.ts\` |
| 测试函数 | \`it_should_*\` / \`test_*\` | \`it_should_return_user_by_id\` |

---

## 4. 与其他 Skill 的关系

\`\`\`yaml
depends_on:
  - project-workflow-git
provides_to:
  - dev-stage4
\`\`\`
EOF

# =============================================
# 4. 生成 project-workflow-code-review.md
# =============================================
echo "[generate-workflow-skills] 生成 project-workflow-code-review.md..."

cat > "$SKILLS_DIR/project-workflow-code-review.md" << EOF
# Code Review Workflow（代码审查流程）

> **路径**：\`.claude/skills/project-workflow-code-review.md\`
> **用途**：Code Review 规范
> **来源**：通用规范
> **生成时间**：$(date +%Y-%m-%d)

---

## Skill 元数据

\`\`\`yaml
name: project-workflow-code-review
name_zh: Code Review 流程
category: workflow
subcategory: development
version: 1.0.0
author: Architect Agent
created: $(date +%Y-%m-%d)
trigger: auto-generate
\`\`\`

---

## 1. Review 检查清单

| 检查项 | 说明 | 优先级 |
|--------|------|--------|
| 命名规范 | 变量、函数、类命名是否清晰 | P0 |
| 代码复杂度 | 是否过于复杂需要拆分 | P1 |
| 测试覆盖 | 是否有足够的测试 | P1 |
| 安全问题 | 是否有安全漏洞 | P0 |
| 性能问题 | 是否有性能隐患 | P2 |
| 错误处理 | 是否有完整的错误处理 | P1 |

---

## 2. Review 流程

```
1. 开发者提交 PR
2. Reviewer 收到通知
3. Reviewer 检查代码
4. 留下评论或批准
5. 开发者修复问题
6. 合并代码
```

---

## 3. 与其他 Skill 的关系

\`\`\`yaml
depends_on:
  - project-workflow-git
  - project-naming-convention
provides_to:
  - dev-stage4
\`\`\`
EOF

# =============================================
# 5. 生成 project-workflow-commit.md
# =============================================
echo "[generate-workflow-skills] 生成 project-workflow-commit.md..."

cat > "$SKILLS_DIR/project-workflow-commit.md" << EOF
# Commit Convention（提交规范）

> **路径**：\`.claude/skills/project-workflow-commit.md\`
> **用途**：Git 提交信息规范
> **来源**：通用规范
> **生成时间**：$(date +%Y-%m-%d)

---

## Skill 元数据

\`\`\`yaml
name: project-workflow-commit
name_zh: 提交规范
category: workflow
subcategory: development
version: 1.0.0
author: Architect Agent
created: $(date +%Y-%m-%d)
trigger: auto-generate
\`\`\`

---

## 1. Commit 类型

| 类型 | 说明 | 使用场景 |
|------|------|----------|
| feat | 新功能 | 添加新功能 |
| fix | Bug 修复 | 修复缺陷 |
| docs | 文档 | 文档更新 |
| style | 格式 | 代码格式（不影响功能） |
| refactor | 重构 | 重构代码（不修复bug不添功能） |
| perf | 性能 | 性能优化 |
| test | 测试 | 添加/修改测试 |
| chore | 构建/工具 | 构建工具、依赖更新 |

---

## 2. Commit 格式

\`\`\`
<type>(<scope>): <subject>

<body>

[optional footer]
\`\`\`

| 部分 | 说明 | 约束 |
|------|------|------|
| type | 类型 | 必须 |
| scope | 范围 | 可选 |
| subject | 主题 | 必须，50字符以内 |
| body | 详细描述 | 可选 |
| footer | 关联问题 | 可选 |

---

## 3. 与其他 Skill 的关系

\`\`\`yaml
depends_on:
  - project-workflow-git
provides_to:
  - dev-stage4
\`\`\`
EOF

# =============================================
# 6. 生成 Deploy Skills
# =============================================
echo "[generate-workflow-skills] 生成部署工作流 Skills..."

cat > "$SKILLS_DIR/project-deploy-build.md" << 'EOF'
# Build Workflow（构建流程）

> **路径**：`.claude/skills/project-deploy-build.md`
> **用途**：项目构建规范
> **来源**：通用规范
> **生成时间**：$(date +%Y-%m-%d)

---

## Skill 元数据

```yaml
name: project-deploy-build
name_zh: 构建流程
category: workflow
subcategory: deployment
version: 1.0.0
author: Architect Agent
created: $(date +%Y-%m-%d)
trigger: auto-generate
```

---

## 1. 构建命令

| 环境 | 命令 |
|------|------|
| 开发 | `npm run dev` / `python manage.py runserver` |
| 测试 | `npm run test` / `pytest` |
| 生产 | `npm run build` / `python manage.py build` |

---

## 2. 构建产物

| 类型 | 路径 |
|------|------|
| 前端 | `dist/` / `build/` |
| 后端 | `*.whl` / `*.jar` |

---

## 3. 与其他 Skill 的关系

```yaml
depends_on:
  - project-workflow-git
provides_to:
  - dev-stage4
```
EOF

cat > "$SKILLS_DIR/project-deploy-docker.md" << 'EOF'
# Docker Workflow（Docker 容器化）

> **路径**：`.claude/skills/project-deploy-docker.md`
> **用途**：Docker 部署规范
> **来源**：通用规范
> **生成时间**：$(date +%Y-%m-%d)

---

## Skill 元数据

```yaml
name: project-deploy-docker
name_zh: Docker 部署
category: workflow
subcategory: deployment
version: 1.0.0
author: Architect Agent
created: $(date +%Y-%m-%d)
trigger: auto-generate
```

---

## 1. Docker 规范

| 项 | 规范 |
|----|------|
| Dockerfile 位置 | 项目根目录 |
| 多阶段构建 | 使用多阶段构建减小镜像 |
| 非 root 用户 | 使用非 root 用户运行 |
| 健康检查 | 添加 HEALTHCHECK 指令 |

---

## 2. 与其他 Skill 的关系

```yaml
depends_on:
  - project-deploy-build
provides_to:
  - dev-stage4
```
EOF

cat > "$SKILLS_DIR/project-deploy-cicd.md" << 'EOF'
# CI/CD Workflow（持续集成/部署）

> **路径**：`.claude/skills/project-deploy-cicd.md`
> **用途**：CI/CD 流程规范
> **来源**：通用规范
> **生成时间**：$(date +%Y-%m-%d)

---

## Skill 元数据

```yaml
name: project-deploy-cicd
name_zh: CI/CD 流程
category: workflow
subcategory: deployment
version: 1.0.0
author: Architect Agent
created: $(date +%Y-%m-%d)
trigger: auto-generate
```

---

## 1. CI/CD 流程

```
代码提交 → Lint → Test → Build → Deploy to staging → Deploy to production
```

---

## 2. 流程说明

| 阶段 | 说明 |
|------|------|
| Lint | 代码风格检查 |
| Test | 单元测试、集成测试 |
| Build | 构建产物 |
| Deploy staging | 部署到预发布环境 |
| Deploy production | 部署到生产环境 |

---

## 3. 与其他 Skill 的关系

```yaml
depends_on:
  - project-workflow-git
  - project-deploy-build
  - project-deploy-docker
provides_to:
  - dev-stage4
```
EOF

echo "[generate-workflow-skills] Workflow Skills 生成完成"
