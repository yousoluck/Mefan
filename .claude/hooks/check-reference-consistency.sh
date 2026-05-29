#!/bin/bash
# check-reference-consistency.sh - 确保新代码遵循参考模块的命名/结构
# 用法: bash .claude/hooks/check-reference-consistency.sh [file_path]
# 如果不指定 file_path，检查所有修改的文件
# 退出码: 0=通过, 1=有问题, 2=异常

set -e

ROOT="/mnt/d/pycharmprojects/Mefan"
CONSISTENCY_BASELINE="$ROOT/.claude/context/consistency-baseline.md"
LOG_FILE="iterations/mefan-log.md"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

echo "[check-reference-consistency] 开始参考模块一致性检查..."

# 1. 检查前置文件
if [ ! -f "$CONSISTENCY_BASELINE" ]; then
    echo "[check-reference-consistency] 警告：consistency-baseline.md 不存在，跳过检查"
    exit 0
fi

# 2. 获取要检查的文件（从 git diff 或参数）
if [ -n "$1" ]; then
    FILES_TO_CHECK="$1"
else
    FILES_TO_CHECK=$(git diff --name-only --diff-filter=ACM 2>/dev/null | grep -v "^$" || echo "")
fi

if [ -z "$FILES_TO_CHECK" ]; then
    echo "[check-reference-consistency] 没有修改的文件，跳过检查"
    exit 0
fi

echo "[check-reference-consistency] 检查以下文件:"
echo "$FILES_TO_CHECK"

# 3. 读取参考模块的命名约定
# 格式：| 模块类型 | 命名模式 | 示例 |
NAMING_CONVENTIONS=$(grep -A 100 "## 命名约定" "$CONSISTENCY_BASELINE" 2>/dev/null | grep "| " | grep -v "模块类型" | head -20 || echo "")

if [ -z "$NAMING_CONVENTIONS" ]; then
    # 尝试其他格式
    NAMING_CONVENTIONS=$(grep -A 50 "命名约定" "$CONSISTENCY_BASELINE" 2>/dev/null | head -30 || echo "")
fi

# 4. 检查每个文件的命名一致性
VIOLATIONS=()
CHECKED_FILES=0

for file in $FILES_TO_CHECK; do
    if [ ! -f "$file" ]; then continue; fi
    CHECKED_FILES=$((CHECKED_FILES + 1))

    # 获取文件扩展名
    EXT="${file##*.}"
    FILENAME=$(basename "$file")

    echo "[check-reference-consistency] 检查文件: $file"

    # 检查 Python 文件命名
    if [ "$EXT" = "py" ]; then
        # Python 应该用 snake_case
        if echo "$FILENAME" | grep -qE '[A-Z]' && ! echo "$FILENAME" | grep -qE '__init__|test_'; then
            VIOLATIONS+=("文件 $file 使用 PascalCase，应使用 snake_case")
        fi
    fi

    # 检查 JS/TS 文件命名
    if [ "$EXT" = "js" ] || [ "$EXT" = "ts" ] || [ "$EXT" = "jsx" ] || [ "$EXT" = "tsx" ]; then
        # JS/TS 应该用 camelCase 或 kebab-case
        if echo "$FILENAME" | grep -qE '_' && ! echo "$FILENAME" | grep -qE 'test_|spec_|_test|_spec'; then
            VIOLATIONS+=("文件 $file 使用 snake_case，应使用 camelCase 或 kebab-case")
        fi
    fi

    # 检查目录命名
    SUBDIR=$(dirname "$file" | sed "s|$ROOT/../||")
    if echo "$SUBDIR" | grep -qE '[A-Z]' | grep -v "^tests$|^src$"; then
        VIOLATIONS+=("目录 $SUBDIR 使用 PascalCase，应使用 kebab-case 或 snake_case")
    fi
done

echo "[check-reference-consistency] 检查了 $CHECKED_FILES 个文件"

# 5. 输出结果
if [ ${#VIOLATIONS[@]} -gt 0 ]; then
    echo "[check-reference-consistency] 发现 ${#VIOLATIONS[@]} 个命名违规:"
    for v in "${VIOLATIONS[@]}"; do
        echo "  - $v"
    done
    echo "| $TIMESTAMP | 04 | Hook | check-ref-consistency | ${#VIOLATIONS[@]} 个违规 |" >> "$LOG_FILE"
    exit 1
fi

echo "[check-reference-consistency] 参考模块一致性检查通过"
echo "| $TIMESTAMP | 04 | Hook | check-ref-consistency | $CHECKED_FILES 个文件 | 通过 |" >> "$LOG_FILE"
exit 0