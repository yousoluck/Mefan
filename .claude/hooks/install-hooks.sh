#!/bin/bash
# install-hooks.sh - 安装所有阶段 4 相关的 Git hooks
# 用法: bash .claude/hooks/install-hooks.sh
set -e

ROOT="/mnt/d/pycharmprojects/Mefan"
GIT_HOOKS_DIR="$ROOT/.git/hooks"

echo "[install-hooks] 开始安装 Git hooks..."

# 确保 hooks 目录存在
mkdir -p "$GIT_HOOKS_DIR"

# 1. 安装 pre-commit hook
if [ -f "$ROOT/.claude/hooks/pre-commit.sh" ]; then
    ln -sf "$ROOT/.claude/hooks/pre-commit.sh" "$GIT_HOOKS_DIR/pre-commit"
    chmod +x "$ROOT/.claude/hooks/pre-commit.sh"
    echo "[install-hooks] pre-commit hook 已安装"
fi

# 2. 安装 pre-merge-check hook
if [ -f "$ROOT/.claude/hooks/pre-merge-check.sh" ]; then
    ln -sf "$ROOT/.claude/hooks/pre-merge-check.sh" "$GIT_HOOKS_DIR/pre-merge-commit"
    chmod +x "$ROOT/.claude/hooks/pre-merge-check.sh"
    echo "[install-hooks] pre-merge-commit hook 已安装"
fi

# 3. 安装 prepare-commit-msg hook（自动生成 commit message 前缀）
if [ -f "$ROOT/.claude/hooks/prepare-commit-msg.sh" ]; then
    ln -sf "$ROOT/.claude/hooks/prepare-commit-msg.sh" "$GIT_HOOKS_DIR/prepare-commit-msg"
    chmod +x "$ROOT/.claude/hooks/prepare-commit-msg.sh"
    echo "[install-hooks] prepare-commit-msg hook 已安装"
fi

# 4. 设置所有 hook 脚本为可执行
chmod +x "$ROOT/.claude/hooks/stage4-self-check.sh"
chmod +x "$ROOT/.claude/hooks/check-incremental.sh"
chmod +x "$ROOT/.claude/hooks/enforce-diff-limit.sh"
chmod +x "$ROOT/.claude/hooks/check-state-machine.sh"
chmod +x "$ROOT/.claude/hooks/check-adr-implementation.sh"
chmod +x "$ROOT/.claude/hooks/check-reference-consistency.sh"
chmod +x "$ROOT/.claude/hooks/check-tdd-rhythm.sh"
chmod +x "$ROOT/.claude/hooks/check-test-coverage.sh"

echo "[install-hooks] Git hooks 安装完成"
echo ""
echo "已安装的 hooks:"
ls -la "$GIT_HOOKS_DIR" | grep -E "^-(l.*)" | awk '{print "  " $NF}'