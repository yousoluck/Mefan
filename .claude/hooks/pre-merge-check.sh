#!/bin/bash
# pre-merge-check.sh - merge 前自动检查
# 在合并分支前运行测试和检查
# 用法: 在 .git/hooks/pre-merge-commit 中调用此脚本
set -e

ROOT="/mnt/d/pycharmprojects/Mefan"
STAGE="04"
LOG_FILE="iterations/mefan-log.md"

echo "[pre-merge] 开始执行合并前检查..."

# 1. 获取即将合并的分支名
MERGE_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
TARGET_BRANCH=$(git name-rev --name-only HEAD 2>/dev/null | sed 's/^remotes\/origin\///' | awk '{print $1}' | tail -1)

if [ -z "$TARGET_BRANCH" ]; then
    echo "[pre-merge] 无法确定目标分支，跳过检查"
    exit 0
fi

echo "[pre-merge] 合并分支: $MERGE_BRANCH -> $TARGET_BRANCH"

# 2. 检查是否有测试文件
if [ -f "package.json" ]; then
    echo "[pre-merge] 运行单元测试..."
    npm run test --silent 2>/dev/null || {
        echo "[pre-merge] 错误：单元测试失败"
        echo "[pre-merge] 请确保所有测试通过后再合并"
        exit 1
    }
    echo "[pre-merge] 单元测试通过"
fi

# 3. 检查 lint
if [ -f "package.json" ]; then
    echo "[pre-merge] 运行 lint 检查..."
    npm run lint --silent 2>/dev/null || {
        echo "[pre-merge] 错误：lint 检查失败"
        exit 1
    }
    echo "[pre-merge] lint 检查通过"
fi

# 4. 记录日志
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
echo "| $TIMESTAMP | $STAGE | pre-merge | $MERGE_BRANCH -> $TARGET_BRANCH | - | 通过 |" >> "$LOG_FILE"

echo "[pre-merge] 合并前检查完成，允许合并"
exit 0