#!/bin/bash
# enforce-diff-limit.sh - 强制限制单次变更的行数
# 如果变更超过阈值（默认300行），直接拒绝提交
# 用法: 在 pre-commit hook 中调用
set -e

ROOT="/mnt/d/pycharmprojects/Mefan"
STAGE="04"
THRESHOLD="${DIFF_THRESHOLD:-300}"  # 默认300行硬限制
LOG_FILE="iterations/mefan-log.md"

echo "[enforce-diff-limit] 检查增量变更大小..."

# 1. 获取暂存的增量文件变更行数
CHANGED_FILES=$(git diff --cached --name-only --diff-filter=ACM 2>/dev/null || echo "")

if [ -z "$CHANGED_FILES" ]; then
    echo "[enforce-diff-limit] 没有暂存的文件，跳过检查"
    exit 0
fi

# 2. 检查每个文件的增量
EXCEEDED_FILES=()
for file in $CHANGED_FILES; do
    if [ -f "$file" ]; then
        # 获取该文件的增量行数
        added=$(git diff --cached "$file" 2>/dev/null | grep "^+" | grep -v "^+++" | wc -l || echo "0")
        removed=$(git diff --cached "$file" 2>/dev/null | grep "^-" | grep -v "^---" | wc -l || echo "0")
        delta=$((added + removed))

        if [ $delta -gt $THRESHOLD ]; then
            echo "[enforce-diff-limit] 文件 $file 增量 $delta 行超过阈值 $THRESHOLD"
            EXCEEDED_FILES+=("$file (${delta}行)")
        fi
    fi
done

# 3. 如果有文件超过阈值，拒绝提交
if [ ${#EXCEEDED_FILES[@]} -gt 0 ]; then
    echo "[enforce-diff-limit] 错误：以下文件超过单次变更阈值 $THRESHOLD 行："
    for f in "${EXCEEDED_FILES[@]}"; do
        echo "  - $f"
    done
    echo "[enforce-diff-limit] 请将大文件拆分或增加注释说明原因"
    echo "[enforce-diff-limit] 如需临时绕过，可使用: git commit --no-verify"
    exit 1
fi

echo "[enforce-diff-limit] 增量检查通过，所有文件在阈值内"
exit 0