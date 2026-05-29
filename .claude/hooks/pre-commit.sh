#!/bin/bash
# pre-commit hook - 在 git commit 前自动运行检查
# 用法: 在 .git/hooks/pre-commit 中调用此脚本
set -e

ROOT="/mnt/d/pycharmprojects/Mefan"
STAGE="04"
LOG_FILE="iterations/mefan-log.md"

echo "[pre-commit] 开始执行提交前检查..."

# 1. 检查是否在正确的分支上
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
if [ "$CURRENT_BRANCH" = "main" ] || [ "$CURRENT_BRANCH" = "master" ]; then
    echo "[pre-commit] 错误：禁止在 main/master 分支直接提交"
    exit 1
fi

# 2. 检查是否有变更文件
CHANGED_FILES=$(git diff --cached --name-only --diff-filter=ACM)
if [ -z "$CHANGED_FILES" ]; then
    echo "[pre-commit] 没有暂存的文件，跳过检查"
    exit 0
fi

# 3. 对每个变更文件运行一致性检查
echo "[pre-commit] 运行一致性检查..."
CHECK_FAILED=0
for file in $CHANGED_FILES; do
    if [ -f "$file" ]; then
        result=$(python "$ROOT/.claude/hooks/check-consistency.py" "$file" 2>/dev/null)
        if echo "$result" | grep -q "violations_found"; then
            echo "[pre-commit] 违规: $file"
            echo "$result"
            CHECK_FAILED=1
        fi
    fi
done

if [ $CHECK_FAILED -eq 1 ]; then
    echo "[pre-commit] 错误：存在违规项，请修复后重新提交"
    exit 1
fi

# 4. 检查变更文件大小（软限制200行，警告）
echo "[pre-commit] 检查变更文件大小..."
for file in $CHANGED_FILES; do
    if [ -f "$file" ]; then
        result=$(python "$ROOT/.claude/hooks/check-diff-size.py" "$file" 2>/dev/null)
        if echo "$result" | grep -q "size_warning"; then
            echo "[pre-commit] 警告: $file 超过行数限制"
            echo "$result"
        fi
    fi
done

# 5. 强制增量限制（硬限制300行，拒绝提交）
echo "[pre-commit] 强制增量限制检查..."
bash "$ROOT/.claude/hooks/enforce-diff-limit.sh" || {
    echo "[pre-commit] 增量限制检查失败，拒绝提交"
    exit 1
}

# 6. 记录日志
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
echo "| $TIMESTAMP | $STAGE | pre-commit | 提交前检查 | $CHANGED_FILES | 通过 |" >> "$LOG_FILE"

echo "[pre-commit] 检查完成，允许提交"
exit 0