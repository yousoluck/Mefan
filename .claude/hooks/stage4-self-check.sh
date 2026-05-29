#!/bin/bash
# stage4-self-check.sh - 开发阶段 4 Self-Check 自动检查
# 在 Self-Check 阶段对所有修改的文件运行一致性检查
# 用法: bash .claude/hooks/stage4-self-check.sh <MG_ID>
set -e

ROOT="/mnt/d/pycharmprojects/Mefan"
STAGE="04"
MG_ID="${1:-MG-001}"
LOG_FILE="iterations/mefan-log.md"

echo "[stage4-self-check] MG $MG_ID 开始 Self-Check..."

# 1. 获取当前分支的修改文件
CHANGED_FILES=$(git diff --name-only --diff-filter=ACM 2>/dev/null || echo "")
if [ -z "$CHANGED_FILES" ]; then
    echo "[stage4-self-check] 没有修改的文件，跳过检查"
    exit 0
fi

# 2. 对每个修改的文件运行一致性检查
CHECK_FAILED=0
CHECKED_FILES=0
for file in $CHANGED_FILES; do
    if [ -f "$file" ]; then
        CHECKED_FILES=$((CHECKED_FILES + 1))
        result=$(python "$ROOT/.claude/hooks/check-consistency.py" "$file" 2>/dev/null)
        if echo "$result" | grep -q "violations_found"; then
            echo "[stage4-self-check] 违规: $file"
            violations=$(echo "$result" | python -c "import sys,json; data=json.load(sys.stdin); print(data.get('violations',[]))" 2>/dev/null || echo "[]")
            echo "$violations"
            CHECK_FAILED=1
        fi
    fi
done

echo "[stage4-self-check] 检查了 $CHECKED_FILES 个文件"

# 3. 检查是否有 lint 错误
if command -v npm &> /dev/null && [ -f "package.json" ]; then
    echo "[stage4-self-check] 运行 lint 检查..."
    npm run lint --silent 2>/dev/null || {
        echo "[stage4-self-check] lint 检查失败"
        CHECK_FAILED=1
    }
fi

# 4. 记录日志
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
if [ $CHECK_FAILED -eq 0 ]; then
    echo "| $TIMESTAMP | $STAGE | Self-Check | MG $MG_ID | $CHECKED_FILES 个文件 | 通过 |" >> "$LOG_FILE"
    echo "[stage4-self-check] Self-Check 通过"
    exit 0
else
    echo "| $TIMESTAMP | $STAGE | Self-Check | MG $MG_ID | $CHECKED_FILES 个文件 | 失败 |" >> "$LOG_FILE"
    echo "[stage4-self-check] Self-Check 失败，发现违规项"
    exit 1
fi