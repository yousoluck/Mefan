#!/bin/bash
# check-incremental.sh - 检查已提交代码的增量问题
# 对比上次 Code Review 后的所有增量变更进行检查
# 用法: bash .claude/hooks/check-incremental.sh <MG_ID> [since_commit]
set -e

ROOT="/mnt/d/pycharmprojects/Mefan"
STAGE="04"
MG_ID="${1:-MG-001}"
SINCE_COMMIT="${2:-HEAD~10}"  # 默认检查最近10个提交
LOG_FILE="iterations/mefan-log.md"

echo "[check-incremental] MG $MG_ID 开始增量检查..."

# 1. 获取增量变更的文件
INCREMENTAL_FILES=$(git diff --name-only "$SINCE_COMMIT" HEAD 2>/dev/null | grep -v "^$" || echo "")

if [ -z "$INCREMENTAL_FILES" ]; then
    echo "[check-incremental] 没有增量变更，跳过检查"
    exit 0
fi

echo "[check-incremental] 检查以下文件的增量变更:"
echo "$INCREMENTAL_FILES"

# 2. 对每个增量文件运行一致性检查
CHECK_FAILED=0
CHECKED_FILES=0
VIOLATIONS_FOUND=()
for file in $INCREMENTAL_FILES; do
    if [ -f "$file" ]; then
        CHECKED_FILES=$((CHECKED_FILES + 1))
        result=$(python "$ROOT/.claude/hooks/check-consistency.py" "$file" 2>/dev/null)
        if echo "$result" | grep -q "violations_found"; then
            echo "[check-incremental] 违规: $file"
            VIOLATIONS_FOUND+=("$file")
            CHECK_FAILED=1
        fi
    fi
done

echo "[check-incremental] 检查了 $CHECKED_FILES 个增量文件"

# 3. 检查增量大小
echo "[check-incremental] 检查增量大小..."
for file in $INCREMENTAL_FILES; do
    if [ -f "$file" ]; then
        result=$(python "$ROOT/.claude/hooks/check-diff-size.py" "$file" 2>/dev/null)
        if echo "$result" | grep -q "size_warning"; then
            echo "[check-incremental] 警告: $file 超过行数限制"
        fi
    fi
done

# 4. 统计增量行数
INCREMENTAL_LINES=$(git diff --stat "$SINCE_COMMIT" HEAD 2>/dev/null | tail -1 | awk '{print $NF}' || echo "0")
echo "[check-incremental] 增量总行数: $INCREMENTAL_LINES"

# 5. 记录日志
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
if [ $CHECK_FAILED -eq 0 ]; then
    echo "| $TIMESTAMP | $STAGE | incremental-check | MG $MG_ID | $CHECKED_FILES 个文件, $INCREMENTAL_LINES 行 | 通过 |" >> "$LOG_FILE"
    echo "[check-incremental] 增量检查通过"
    exit 0
else
    echo "| $TIMESTAMP | $STAGE | incremental-check | MG $MG_ID | $CHECKED_FILES 个文件, $INCREMENTAL_LINES 行 | 失败 |" >> "$LOG_FILE"
    echo "[check-incremental] 增量检查失败，发现违规项: ${VIOLATIONS_FOUND[*]}"
    exit 1
fi