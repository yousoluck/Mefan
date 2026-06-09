# /mf-upgrade:skill-maintenance – Skill 维护（更新现有 / 创建新 Skill）

> **当前阶段**：阶段 0 后（Skill 维护）
> **主导角色**：架构师 (Architect)
> **辅助角色**：项目经理 (PM)、人工审核
> **前置条件**：
> - `.claude/context/consistency-baseline.md` 已存在
> - `.claude/skills/` 目录存在
>
> **执行模式**：双分支模式
> - **分支 A**：更新现有 Skill（模板 → 重新生成）
> - **分支 B**：创建新 Skill（无模板 → Graphify 动态生成 / 人工创建）

---

## 0. 概述

本 command 用于维护 Skills，解决两类问题：
1. **现有 Skill 内容不完整** → 更新模板 → 重新生成 → Human Review
2. **新 Feature 无对应 Skill** → 尝试 Graphify → 人工创建 → 更新索引

**主流程**：
```
Human 提出需求
    ↓
    ├─→ 分支 A：更新现有 Skill
    │       1. 选择要更新的 Skill
    │       2. 补充/修改内容
    │       3. 更新模板（_templates/）
    │       4. 重新生成 Skill（覆盖 .claude/skills/）
    │       5. Human Review
    │       6. 更新 consistency-baseline.md 索引（如需要）
    │
    └─→ 分支 B：创建新 Skill
            1. 确定新 Feature 名称
            2. 检查是否有模板（_templates/project-infra-{feature}/）
            3a. 有模板 → 复制并替换变量
            3b. 无模板
                ├─→ Graphify 查询实现 → 通用骨架 + 查询结果
                └─→ Graphify 查不到 → 人工创建
            4. Human Review
            5. 更新 consistency-baseline.md 索引
```

---

## 1. 日志声明

执行本 playbook 时，必须使用 `.claude/hooks/log-event.sh` 记录日志：

| 事件类型 | 日志命令格式 |
|---------|-------------|
| Skill 维护开始 | `bash .claude/hooks/log-event.sh "00" "Architect" "阶段进入" "Skill维护开始" "" "成功"` |
| 分支 A 激活 | `bash .claude/hooks/log-event.sh "00" "Architect" "分支激活" "分支A：更新现有Skill" "" "进行中"` |
| 分支 B 激活 | `bash .claude/hooks/log-event.sh "00" "Architect" "分支激活" "分支B：创建新Skill" "" "进行中"` |
| 模板更新 | `bash .claude/hooks/log-event.sh "00" "Architect" "模板更新" "{template_name}" "" "成功"` |
| Skill 生成 | `bash .claude/hooks/log-event.sh "00" "Architect" "Skill生成" "{skill_name}" "" "成功"` |
| Human Review | `bash .claude/hooks/log-event.sh "00" "Architect" "HumanReview" "{skill_name}" "" "等待"` |
| Human 批准 | `bash .claude/hooks/log-event.sh "00" "Architect" "HumanReview通过" "{skill_name}" "" "成功"` |
| 索引更新 | `bash .claude/hooks/log-event.sh "00" "Architect" "索引更新" "consistency-baseline.md" "" "成功"` |
| Skill 维护完成 | `bash .claude/hooks/log-event.sh "00" "Architect" "阶段完成" "Skill维护完成" "" "成功"` |

---

## 2. 变量定义

```bash
# 从 project.conf 加载 ROOT
if [ -f "$(dirname "${BASH_SOURCE[0]}")/../project.conf" ]; then
    source "$(dirname "${BASH_SOURCE[0]}")/../project.conf"
else
    export ROOT="/mnt/d/pycharmprojects/Mefan"
fi

SKILLS_DIR="$ROOT/.claude/skills"
TEMPLATES_DIR="$ROOT/.claude/skills/_templates"
CB_FILE="$ROOT/.claude/context/consistency-baseline.md"
AGENT_NAME="Architect"
```

---

## 3. 选择分支

```bash
echo "=========================================="
echo " Skill 维护工具"
echo "=========================================="
echo "请选择操作分支："
echo "  A - 更新现有 Skill（模板已有，补充内容）"
echo "  B - 创建新 Skill（无模板，需要新建）"
echo ""
read -p "请输入选项 [A/B]: " BRANCH

case "$BRANCH" in
    A|a)
        echo "[Skill-Maintenance] 选择分支 A：更新现有 Skill"
        bash $ROOT/.claude/hooks/log-event.sh "00" "$AGENT_NAME" "分支激活" "分支A：更新现有Skill" "" "进行中"
        ;;
    B|b)
        echo "[Skill-Maintenance] 选择分支 B：创建新 Skill"
        bash $ROOT/.claude/hooks/log-event.sh "00" "$AGENT_NAME" "分支激活" "分支B：创建新Skill" "" "进行中"
        ;;
    *)
        echo "[Error] 无效选项，退出"
        exit 1
        ;;
esac
```

---

## 4. 分支 A：更新现有 Skill

### 4.1 列出现有 Skills

```bash
echo ""
echo "=== 分支 A：更新现有 Skill ==="
echo ""
echo "当前可用的 Skills："
echo ""

# 列出所有 Skill 目录（排除模板）
ls -d $SKILLS_DIR/project-*/ 2>/dev/null | while read dir; do
    skill_name=$(basename "$dir")
    skill_file="$dir/SKILL.md"

    # 检查是否是从模板生成的
    template_dir="$TEMPLATES_DIR/$skill_name"
    if [ -d "$template_dir" ]; then
        source_type="[有模板]"
    else
        source_type="[无模板-需检查]"
    fi

    # 提取 name_zh
    if [ -f "$skill_file" ]; then
        name_zh=$(grep "^name_zh:" "$skill_file" 2>/dev/null | head -1 | sed 's/name_zh: *//' | tr -d ' ')
        if [ -z "$name_zh" ]; then
            name_zh="未知"
        fi
    else
        name_zh="（无 SKILL.md）"
    fi

    echo "  $source_type $skill_name ($name_zh)"
done
echo ""
```

### 4.2 选择要更新的 Skill

```bash
read -p "请输入要更新的 Skill 名称（不含前缀，如 user, auth）: " SKILL_NAME

# 列出所有已有的 Skills供选择
echo ""
echo "当前可用的 Skills（按类型分组）："
echo ""
echo "L1 基础设施类："
ls -d $SKILLS_DIR/project-infra-*/ 2>/dev/null | while read dir; do echo "  - $(basename "$dir")"; done
echo "L2 领域模型类："
ls -d $SKILLS_DIR/project-domain-*/ 2>/dev/null | while read dir; do echo "  - $(basename "$dir")"; done
echo "L3 应用服务类："
ls -d $SKILLS_DIR/project-service-*/ 2>/dev/null | while read dir; do echo "  - $(basename "$dir")"; done
echo "L4 接口类："
ls -d $SKILLS_DIR/project-api-*/ $SKILLS_DIR/project-ui-*/ 2>/dev/null | while read dir; do echo "  - $(basename "$dir")"; done
echo "L5 业务场景类："
ls -d $SKILLS_DIR/project-feature-*/ 2>/dev/null | while read dir; do echo "  - $(basename "$dir")"; done
echo ""
read -p "请输入完整 Skill 名称（带前缀，如 project-infra-database）: " FULL_SKILL_NAME

# 从完整名称推断前缀类型
if [[ "$FULL_SKILL_NAME" == project-infra-* ]]; then
    SKILL_TYPE="infra"
    SKILL_PREFIX="project-infra-"
elif [[ "$FULL_SKILL_NAME" == project-domain-* ]]; then
    SKILL_TYPE="domain"
    SKILL_PREFIX="project-domain-"
elif [[ "$FULL_SKILL_NAME" == project-service-* ]]; then
    SKILL_TYPE="service"
    SKILL_PREFIX="project-service-"
elif [[ "$FULL_SKILL_NAME" == project-api-* ]]; then
    SKILL_TYPE="api"
    SKILL_PREFIX="project-api-"
elif [[ "$FULL_SKILL_NAME" == project-ui-* ]]; then
    SKILL_TYPE="ui"
    SKILL_PREFIX="project-ui-"
elif [[ "$FULL_SKILL_NAME" == project-feature-* ]]; then
    SKILL_TYPE="feature"
    SKILL_PREFIX="project-feature-"
else
    echo "[Error] 无法识别的 Skill 类型：$FULL_SKILL_NAME"
    echo "Skill 名称必须以 project-infra-, project-domain-, project-service-, project-api-, project-ui-, project-feature- 开头"
    exit 1
fi

SKILL_DIR="$SKILLS_DIR/$FULL_SKILL_NAME"
SKILL_FILE="$SKILL_DIR/SKILL.md"

# 查找对应的模板目录
case "$SKILL_TYPE" in
    infra)
        TEMPLATE_DIR="$TEMPLATES_DIR/project-infra-$SKILL_NAME"
        ;;
    domain)
        TEMPLATE_DIR="$TEMPLATES_DIR/project-domain-generic"
        ;;
    service)
        TEMPLATE_DIR="$TEMPLATES_DIR/project-service-generic"
        ;;
    api)
        TEMPLATE_DIR="$TEMPLATES_DIR/project-api-generic"
        ;;
    ui)
        TEMPLATE_DIR="$TEMPLATES_DIR/project-ui-generic"
        ;;
    feature)
        TEMPLATE_DIR="$TEMPLATES_DIR/project-feature-generic"
        ;;
esac

if [ ! -d "$SKILL_DIR" ]; then
    echo "[Error] Skill 目录不存在：$SKILL_DIR"
    exit 1
fi

echo ""
echo "选中的 Skill: $FULL_SKILL_NAME"
echo "Skill 类型: L${SKILL_TYPE_NUM:-?} ($SKILL_TYPE)"
echo "Skill 路径: $SKILL_DIR"
echo "模板路径: $TEMPLATE_DIR"

if [ -d "$TEMPLATE_DIR" ]; then
    echo "模板状态: 已存在"
else
    echo "模板状态: 不存在（将使用 Skill 内容作为基础创建模板）"
fi
echo ""
```

### 4.3 选择更新模式

```bash
echo "更新模式选择："
echo "  1 - 在现有 SKILL.md 中直接补充内容（不修改模板）"
echo "  2 - 修改模板（推荐，会自动重新生成 Skill）"
echo "  3 - 仅查看当前内容，不做任何修改"
read -p "请输入选项 [1/2/3]: " UPDATE_MODE
```

### 4.4 执行更新

#### 模式 1：直接修改 SKILL.md

```bash
if [ "$UPDATE_MODE" = "1" ]; then
    echo ""
    echo "=== 模式 1：直接修改 SKILL.md ==="
    echo ""
    echo "当前 Skill 位置：$SKILL_FILE"
    echo ""
    echo "请手动编辑该文件补充内容。"
    echo "提示：查看当前内容 → cat $SKILL_FILE | head -100"
    echo ""

    # 显示当前文件结构
    echo "当前 SKILL.md 章节结构："
    grep "^## " "$SKILL_FILE" 2>/dev/null | head -20
    echo ""

    read -p "是否打开编辑器进行修改？[y/N]: " OPEN_EDITOR
    if [ "$OPEN_EDITOR" = "y" ] || [ "$OPEN_EDITOR" = "Y" ]; then
        ${EDITOR:-vi} "$SKILL_FILE"
        echo "[Mode 1] SKILL.md 已直接修改"
    fi
fi
```

#### 模式 2：修改模板（推荐）

```bash
if [ "$UPDATE_MODE" = "2" ]; then
    echo ""
    echo "=== 模式 2：修改模板 ==="
    echo ""

    # 创建模板目录（如果不存在）
    if [ ! -d "$TEMPLATE_DIR" ]; then
        echo "[Info] 模板目录不存在，创建：$TEMPLATE_DIR"
        mkdir -p "$TEMPLATE_DIR/references"

        # 从现有 Skill 复制内容到模板
        cp "$SKILL_FILE" "$TEMPLATE_DIR/SKILL.md"
        echo "[Info] 已复制现有 SKILL.md 到模板"
    fi

    TEMPLATE_FILE="$TEMPLATE_DIR/SKILL.md"
    echo "模板文件位置：$TEMPLATE_FILE"
    echo ""

    echo "当前模板章节结构："
    grep "^## " "$TEMPLATE_FILE" 2>/dev/null | head -20
    echo ""

    read -p "是否打开模板编辑器进行修改？[y/N]: " OPEN_EDITOR
    if [ "$OPEN_EDITOR" = "y" ] || [ "$OPEN_EDITOR" = "Y" ]; then
        ${EDITOR:-vi} "$TEMPLATE_FILE"
        bash $ROOT/.claude/hooks/log-event.sh "00" "$AGENT_NAME" "模板更新" "$TEMPLATE_DIR" "" "成功"
    fi

    # 重新生成 Skill（使用修改后的模板）
    echo ""
    echo "[Info] 使用修改后的模板重新生成 Skill..."
    rm -rf "$SKILL_DIR"
    cp -r "$TEMPLATE_DIR" "$SKILL_DIR"

    # 替换变量
    TIMESTAMP=$(date -Iseconds)
    find "$SKILL_DIR" -name "*.md" -exec sed -i "s/{timestamp}/$TIMESTAMP/g" {} \;
    find "$SKILL_DIR" -name "*.md" -exec sed -i "s/{feature-name}/$SKILL_NAME/g" {} \;
    # 尝试替换中文名称（如果模板中有的话）
    if [ -n "$FEATURE_NAME_ZH" ]; then
        find "$SKILL_DIR" -name "*.md" -exec sed -i "s/{feature-name-zh}/$FEATURE_NAME_ZH/g" {} \;
    fi

    echo "[Mode 2] 模板已更新，Skill 已重新生成"
    bash $ROOT/.claude/hooks/log-event.sh "00" "$AGENT_NAME" "Skill生成" "$SKILL_DIR" "" "成功"
fi
```

#### 模式 3：仅查看

```bash
if [ "$UPDATE_MODE" = "3" ]; then
    echo ""
    echo "=== 模式 3：仅查看内容 ==="
    echo ""
    cat "$SKILL_FILE" | head -150
    echo ""
    echo "...（省略其余内容）"
    echo ""
fi
```

---

## 5. 分支 B：创建新 Skill

### 5.1 列出已有模板

```bash
echo ""
echo "=== 分支 B：创建新 Skill ==="
echo ""
echo "当前已有的模板（按类型分组）："
echo ""
echo "L1 基础设施类："
ls -d $TEMPLATES_DIR/project-infra-*/ 2>/dev/null | while read dir; do
    if [[ "$(basename "$dir")" != "project-infra-generic" ]]; then
        echo "  - $(basename "$dir")"
    fi
done
echo "L2 领域模型类："
ls -d $TEMPLATES_DIR/project-domain-*/ 2>/dev/null | while read dir; do echo "  - $(basename "$dir")"; done
echo "L3 应用服务类："
ls -d $TEMPLATES_DIR/project-service-*/ 2>/dev/null | while read dir; do echo "  - $(basename "$dir")"; done
echo "L4 接口类："
ls -d $TEMPLATES_DIR/project-api-*/ $TEMPLATES_DIR/project-ui-*/ 2>/dev/null | while read dir; do echo "  - $(basename "$dir")"; done
echo "L5 业务场景类："
ls -d $TEMPLATES_DIR/project-feature-*/ 2>/dev/null | while read dir; do echo "  - $(basename "$dir")"; done
echo "通用骨架："
ls -d $TEMPLATES_DIR/*-generic/ 2>/dev/null | while read dir; do echo "  - $(basename "$dir")"; done
echo ""
```

### 5.2 输入新 Skill 信息

```bash
# 选择 Skill 类型
echo "请选择 Skill 类型（对应 feature-elements.md 的层）："
echo "  1 - L1 基础设施类（对应 project-infra-*）"
echo "  2 - L2 领域模型类（对应 project-domain-*）"
echo "  3 - L3 应用服务类（对应 project-service-*）"
echo "  4 - L4 接口类 - API（对应 project-api-*）"
echo "  5 - L4 接口类 - UI（对应 project-ui-*）"
echo "  6 - L5 业务场景类（对应 project-feature-*）"
echo ""
read -p "请输入选项 [1-6]: " SKILL_TYPE_NUM

case "$SKILL_TYPE_NUM" in
    1) SKILL_TYPE="infra"; SKILL_PREFIX="project-infra-"; FEATURE_CATEGORY="FE-I-*" ;;
    2) SKILL_TYPE="domain"; SKILL_PREFIX="project-domain-"; FEATURE_CATEGORY="FE-D-*" ;;
    3) SKILL_TYPE="service"; SKILL_PREFIX="project-service-"; FEATURE_CATEGORY="FE-A-*" ;;
    4) SKILL_TYPE="api"; SKILL_PREFIX="project-api-"; FEATURE_CATEGORY="FE-F-*" ;;
    5) SKILL_TYPE="ui"; SKILL_PREFIX="project-ui-"; FEATURE_CATEGORY="FE-F-*" ;;
    6) SKILL_TYPE="feature"; SKILL_PREFIX="project-feature-"; FEATURE_CATEGORY="BS-*" ;;
    *)
        echo "[Error] 无效选项"
        exit 1
        ;;
esac

echo ""
read -p "请输入新 Feature 的英文名称（如 search, user）: " FEATURE_NAME
read -p "请输入新 Feature 的中文名称（如 搜索引擎，用户）: " FEATURE_NAME_ZH

# 清理输入（去空格，转小写用于目录名）
FEATURE_SLUG=$(echo "$FEATURE_NAME" | tr '[:upper:]' '[:lower:]' | tr -d ' ')
FULL_SKILL_NAME="${SKILL_PREFIX}${FEATURE_SLUG}"
SKILL_TARGET_DIR="$SKILLS_DIR/$FULL_SKILL_NAME"
TEMPLATE_TARGET_DIR="$TEMPLATES_DIR/$FULL_SKILL_NAME"

# 对于 generic 类型的模板，使用通用模板
case "$SKILL_TYPE" in
    domain|service|api|ui|feature)
        GENERIC_TEMPLATE="$TEMPLATES_DIR/project-${SKILL_TYPE}-generic"
        ;;
    infra)
        GENERIC_TEMPLATE="$TEMPLATES_DIR/project-infra-generic"
        ;;
esac

echo ""
echo "新 Skill 信息："
echo "  Skill 类型: $SKILL_TYPE (L$SKILL_TYPE_NUM - $FEATURE_CATEGORY)"
echo "  英文名称: $FEATURE_NAME"
echo "  中文名称: $FEATURE_NAME_ZH"
echo "  完整名称: $FULL_SKILL_NAME"
echo "  目标路径: $SKILL_TARGET_DIR"
echo "  通用模板: $GENERIC_TEMPLATE"
echo ""
```

### 5.3 检查模板是否存在

```bash
if [ -d "$TEMPLATE_TARGET_DIR" ]; then
    echo "[Info] 已有对应模板，使用模板生成"
    USE_TEMPLATE=true
else
    echo "[Info] 无对应模板"
    USE_TEMPLATE=false
fi
```

### 5.4 生成 Skill

#### 5.4.1 有模板 → 复制并替换变量

```bash
if [ "$USE_TEMPLATE" = "true" ]; then
    echo ""
    echo "=== 使用模板生成 Skill ==="
    echo ""

    # 复制模板到目标
    rm -rf "$SKILL_TARGET_DIR" 2>/dev/null
    cp -r "$TEMPLATE_TARGET_DIR" "$SKILL_TARGET_DIR"

    # 替换变量
    TIMESTAMP=$(date -Iseconds)
    find "$SKILL_TARGET_DIR" -name "*.md" -exec sed -i "s/{timestamp}/$TIMESTAMP/g" {} \;
    find "$SKILL_TARGET_DIR" -name "*.md" -exec sed -i "s/{feature-name}/$FEATURE_SLUG/g" {} \;
    find "$SKILL_TARGET_DIR" -name "*.md" -exec sed -i "s/{feature-name-zh}/$FEATURE_NAME_ZH/g" {} \;

    echo "[Branch B] Skill 已生成：$SKILL_TARGET_DIR"
    bash $ROOT/.claude/hooks/log-event.sh "00" "$AGENT_NAME" "Skill生成" "$SKILL_TARGET_DIR" "" "成功"
fi
```

#### 5.4.2 无模板 → Graphify 动态生成

```bash
if [ "$USE_TEMPLATE" = "false" ]; then
    echo ""
    echo "=== 无模板，尝试 Graphify 动态生成 ==="
    echo ""

    # 使用 5.2 节定义的 GENERIC_TEMPLATE（根据 Skill 类型选择对应的 generic 模板）
    if [ ! -d "$GENERIC_TEMPLATE" ]; then
        echo "[Error] 通用骨架模板不存在：$GENERIC_TEMPLATE"
        echo "无法动态生成，需要人工创建模板。"
        read -p "是否人工创建模板？[y/N]: " CREATE_MANUAL
        if [ "$CREATE_MANUAL" != "y" ] && [ "$CREATE_MANUAL" != "Y" ]; then
            echo "[Branch B] 放弃创建 Skill"
            exit 0
        fi

        # 人工创建模板
        echo ""
        echo "=== 人工创建模板 ==="
        mkdir -p "$TEMPLATE_TARGET_DIR/references"
        echo "[Info] 已创建目录：$TEMPLATE_TARGET_DIR/references"
        echo "[Info] 请手动创建 $TEMPLATE_TARGET_DIR/SKILL.md"
        read -p "是否现在编辑模板文件？[y/N]: " OPEN_EDITOR
        if [ "$OPEN_EDITOR" = "y" ] || [ "$OPEN_EDITOR" = "Y" ]; then
            ${EDITOR:-vi} "$TEMPLATE_TARGET_DIR/SKILL.md"
        fi
    else
        echo "[Info] 使用通用骨架 + Graphify 查询生成"
        rm -rf "$SKILL_TARGET_DIR" 2>/dev/null
        cp -r "$GENERIC_TEMPLATE" "$SKILL_TARGET_DIR"

        # 替换变量
        TIMESTAMP=$(date -Iseconds)
        find "$SKILL_TARGET_DIR" -name "*.md" -exec sed -i "s/{timestamp}/$TIMESTAMP/g" {} \;
        find "$SKILL_TARGET_DIR" -name "*.md" -exec sed -i "s/{feature-name}/$FEATURE_SLUG/g" {} \;
        find "$SKILL_TARGET_DIR" -name "*.md" -exec sed -i "s/{feature-name-zh}/$FEATURE_NAME_ZH/g" {} \;

        # Graphify 查询
        echo ""
        echo "正在 Graphify 查询 '$FEATURE_NAME' 的实现..."
        GRAPHIFY_RESULT=$(graphify query "How is $FEATURE_NAME implemented in this project" 2>/dev/null)

        if [ -n "$GRAPHIFY_RESULT" ]; then
            echo "[Graphify] 查询到结果，填充 description..."
            DESCRIPTION=$(echo "$GRAPHIFY_RESULT" | head -200 | tr -d '\n' | sed 's/"/\\"/g')
            find "$SKILL_TARGET_DIR" -name "SKILL.md" -exec sed -i "s/{feature-description}/$DESCRIPTION/g" {} \;
        else
            echo "[Graphify] 未查到结果，使用默认描述"
            find "$SKILL_TARGET_DIR" -name "SKILL.md" -exec sed -i "s/{feature-description}/动态生成，详见 Graphify 查询结果。如内容不完整，请手动补充。/g" {} \;
        fi

        echo "[Branch B] Skill 已生成：$SKILL_TARGET_DIR"
        bash $ROOT/.claude/hooks/log-event.sh "00" "$AGENT_NAME" "Skill生成" "$SKILL_TARGET_DIR" "" "成功"
    fi
fi
```

---

## 6. Human Review

### 6.1 展示生成的 Skill

```bash
echo ""
echo "=========================================="
echo " Human Review"
echo "=========================================="
echo ""
echo "请人工审核以下 Skill："
echo ""

if [ -f "$SKILL_TARGET_DIR/SKILL.md" ]; then
    echo "=== $SKILL_TARGET_DIR/SKILL.md ==="
    cat "$SKILL_TARGET_DIR/SKILL.md" | head -80
    if [ $(wc -l < "$SKILL_TARGET_DIR/SKILL.md") -gt 80 ]; then
        echo "...（省略其余内容）"
    fi
else
    echo "[Error] SKILL.md 不存在"
fi

echo ""
echo "references/ 目录内容："
ls -la "$SKILL_TARGET_DIR/references/" 2>/dev/null || echo "  （空或不存在）"
echo ""
```

### 6.2 审核选项

```bash
echo "=========================================="
echo " Human Review 选项"
echo "=========================================="
echo "  A - 批准通过，完成 Skill 创建/更新"
echo "  R - 驳回，需要修改（将重新打开编辑器）"
echo "  T - 仅修改模板（分支 A 特有）"
echo "  Q - 放弃本次操作"
echo ""

read -p "请输入选项 [A/R/T/Q]: " REVIEW_CHOICE

case "$REVIEW_CHOICE" in
    A|a)
        echo "[Human Review] 批准通过"
        bash $ROOT/.claude/hooks/log-event.sh "00" "$AGENT_NAME" "HumanReview通过" "$SKILL_TARGET_DIR" "" "成功"
        ;;
    R|r)
        echo "[Human Review] 驳回，需要修改"
        bash $ROOT/.claude/hooks/log-event.sh "00" "$AGENT_NAME" "HumanReview驳回" "$SKILL_TARGET_DIR" "" "修改"
        echo "请修改以下文件后重新提交 Review："
        echo "  $SKILL_TARGET_DIR/SKILL.md"
        read -p "是否现在修改？[y/N]: " MODIFY_NOW
        if [ "$MODIFY_NOW" = "y" ] || [ "$MODIFY_NOW" = "Y" ]; then
            ${EDITOR:-vi} "$SKILL_TARGET_DIR/SKILL.md"
        fi
        echo "[Info] 请重新执行 /mf-upgrade:skill-maintenance 进行 Review"
        ;;
    T|t)
        if [ "$BRANCH" = "A" ] && [ "$UPDATE_MODE" = "2" ]; then
            echo "[Human Review] 仅修改模板（不影响已生成的 Skill）"
            ${EDITOR:-vi} "$TEMPLATE_FILE"
            echo "[Info] 模板已修改，如需重新生成 Skill 请选择分支 A 模式 2"
        else
            echo "[Error] 选项 T 仅适用于分支 A 模式 2"
        fi
        ;;
    Q|q)
        echo "[Human Review] 放弃本次操作"
        exit 0
        ;;
    *)
        echo "[Error] 无效选项"
        exit 1
        ;;
esac
```

---

## 7. 更新 consistency-baseline.md 索引

```bash
if [ "$REVIEW_CHOICE" = "A" ] || [ "$REVIEW_CHOICE" = "a" ]; then
    echo ""
    echo "=== 更新 consistency-baseline.md 索引 ==="
    echo ""

    if [ ! -f "$CB_FILE" ]; then
        echo "[Warning] consistency-baseline.md 不存在，跳过索引更新"
    else
        # 根据 Skill 类型确定对应的章节
        case "$SKILL_TYPE" in
            infra)
                SECTION="5.2 L1 基础设施类（FE-I-*）"
                TABLE_FORMAT="| $FULL_SKILL_NAME/ | FE-I-* | $FEATURE_NAME_ZH | L1 Infrastructure |"
                ;;
            domain)
                SECTION="5.3 L2 领域模型类（FE-D-*）"
                TABLE_FORMAT="| $FULL_SKILL_NAME/ | FE-D-* | $FEATURE_NAME_ZH | L2 Domain |"
                ;;
            service)
                SECTION="5.4 L3 应用服务类（FE-A-*）"
                TABLE_FORMAT="| $FULL_SKILL_NAME/ | FE-A-* | $FEATURE_NAME_ZH | L3 Application |"
                ;;
            api)
                SECTION="5.5 L4 接口组件类（FE-F-*）"
                TABLE_FORMAT="| $FULL_SKILL_NAME/ | FE-F-* | $FEATURE_NAME_ZH | L4 Interface/API |"
                ;;
            ui)
                SECTION="5.5 L4 接口组件类（FE-F-*）"
                TABLE_FORMAT="| $FULL_SKILL_NAME/ | FE-F-* | $FEATURE_NAME_ZH | L4 Interface/UI |"
                ;;
            feature)
                SECTION="5.6 L5 业务场景类（BS-*）"
                TABLE_FORMAT="| $FULL_SKILL_NAME/ | BS-* | $FEATURE_NAME_ZH | L5 Business Scene |"
                ;;
        esac

        # 检查是否已存在该 Skill 的索引
        if grep -q "$FULL_SKILL_NAME" "$CB_FILE"; then
            echo "[Info] Skill 已存在于索引中，跳过添加"
        else
            echo "[Info] 需要在 consistency-baseline.md 第五部分添加索引"
            echo "目标章节：### $SECTION"
            echo "添加内容："
            echo "  $TABLE_FORMAT"
            echo ""
            echo "文件位置：$CB_FILE"
            echo ""
            echo "是否自动添加到索引？（建议人工确认）[y/N]: " AUTO_ADD
            if [ "$AUTO_ADD" = "y" ] || [ "$AUTO_ADD" = "Y" ]; then
                # 使用 sed 在对应章节的表格末尾添加一行
                # 这里简化处理，实际可能需要更复杂的 sed 脚本来精确定位
                echo "[Info] 自动添加功能待实现，请手动添加上述内容到 $CB_FILE"
            fi
        fi

        bash $ROOT/.claude/hooks/log-event.sh "00" "$AGENT_NAME" "索引更新" "consistency-baseline.md 第五部分" "" "待手动更新"
    fi
fi
```

---

## 8. 完成

```bash
echo ""
echo "=========================================="
echo " Skill 维护完成"
echo "=========================================="
echo ""
echo "生成的 Skill 位置："
echo "  $SKILL_TARGET_DIR/"
echo ""
if [ -d "$TEMPLATE_TARGET_DIR" ]; then
    echo "模板位置："
    echo "  $TEMPLATE_TARGET_DIR/"
fi
echo ""
echo "下一步："
echo "  1. 如果需要，更新 consistency-baseline.md 第五部分"
echo "  2. 重新执行 /mf-upgrade:00-init 进行质量门禁检查"
echo ""

bash $ROOT/.claude/hooks/log-event.sh "00" "$AGENT_NAME" "阶段完成" "Skill维护完成" "" "成功"
```

---

## 附录：错误处理

### 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| `Skill 目录不存在` | 输入的 Skill 名称有误 | 检查 `.claude/skills/` 目录中的实际目录名 |
| `模板目录不存在` | 尝试用不存在的模板生成 | 使用分支 B，Graphify 会用通用骨架兜底 |
| `Graphify 查询失败` | graphify 未安装或项目未扫描 | 手动创建模板，或使用通用骨架后人工补充 |

### 调试模式

```bash
# 查看详细执行过程
bash -x .claude/commands/mf-upgrade:skill-maintenance.md

# 只列出现有 Skills
ls -d .claude/skills/project-*/

# 只列出已有模板
ls -d .claude/skills/_templates/project-infra-*/
```