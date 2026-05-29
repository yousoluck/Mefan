#!/bin/bash
# prepare-commit-msg.sh - 自动生成 commit message 前缀
# 根据分支名自动添加前缀，如 [MG-001] feat: ...
# 用法: 在 .git/hooks/prepare-commit-msg 中调用此脚本
set -e

ROOT="/mnt/d/pycharmprojects/Mefan"
COMMIT_MSG_FILE="$1"
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")

# 如果分支是 feature/MG-* 格式，提取 MG ID
if [[ "$CURRENT_BRANCH" =~ ^feature/MG-([A-Za-z0-9-]+) ]]; then
    MG_ID="[MG-${BASH_REMATCH[1]}]"

    # 读取当前 commit message
    CURRENT_MSG=$(cat "$COMMIT_MSG_FILE")

    # 如果消息还没有 MG-ID 前缀，添加它
    if ! echo "$CURRENT_MSG" | grep -q "$MG_ID"; then
        echo "$MG_ID $CURRENT_MSG" > "$COMMIT_MSG_FILE"
        echo "[prepare-commit-msg] 已添加前缀: $MG_ID"
    fi
fi

exit 0