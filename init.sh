#!/bin/bash
# init-mefan-harness.sh
# 初始化 mefan Harness 框架（安装到 .claude/ 目录）
# 用法: bash init.sh [--uninstall]
#   --uninstall: 移除 .claude/ 目录（保留 .mefan/）

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEFAN_ROOT="$SCRIPT_DIR/.mefan"
UNINSTALL=false

# 解析参数
if [ "$1" = "--uninstall" ]; then
    UNINSTALL=true
fi

if [ "$UNINSTALL" = true ]; then
    echo ">>> 卸载 mefan Harness..."
    if [ -d "$SCRIPT_DIR/.claude" ]; then
        rm -rf "$SCRIPT_DIR/.claude"
        echo ">>> 已移除 .claude/ 目录"
    else
        echo ">>> .claude/ 目录不存在，跳过"
    fi
    echo ">>> 卸载完成（.mefan/ 保留）"
    exit 0
fi

echo ">>> 检查 mefan 框架完整性..."
if [ ! -d "$MEFAN_ROOT" ]; then
    echo "ERROR: .mefan/ 目录不存在。请确保在 Mefan 框架根目录运行此脚本。"
    exit 1
fi

echo ">>> 创建 .claude/ 目录结构..."
mkdir -p "$SCRIPT_DIR/.claude/commands"
mkdir -p "$SCRIPT_DIR/.claude/agents"
mkdir -p "$SCRIPT_DIR/.claude/rules/global"
mkdir -p "$SCRIPT_DIR/.claude/rules/scenario-upgrade"
mkdir -p "$SCRIPT_DIR/.claude/rules/scenario-refactor"
mkdir -p "$SCRIPT_DIR/.claude/skills"

echo ">>> 复制 Agents..."
for f in "$MEFAN_ROOT"/agents/*.md; do
    [ -f "$f" ] && cp "$f" "$SCRIPT_DIR/.claude/agents/"
done

echo ">>> 复制并重命名 Rules（knowledge/ → rules/）..."
for f in "$MEFAN_ROOT/knowledge/global/"*.md; do
    [ -f "$f" ] && cp "$f" "$SCRIPT_DIR/.claude/rules/global/"
done
for f in "$MEFAN_ROOT/knowledge/scenario-upgrade/"*.md; do
    [ -f "$f" ] && cp "$f" "$SCRIPT_DIR/.claude/rules/scenario-upgrade/"
done
for f in "$MEFAN_ROOT/knowledge/scenario-refactor/"*.md; do
    [ -f "$f" ] && cp "$f" "$SCRIPT_DIR/.claude/rules/scenario-refactor/"
done 2>/dev/null || true

echo ">>> 复制 Skills..."
for f in "$MEFAN_ROOT/skills/"*.md; do
    [ -f "$f" ] && cp "$f" "$SCRIPT_DIR/.claude/skills/"
done

echo ">>> 复制并重命名 Commands（添加场景前缀）..."
# project-upgrade → mf-upgrade:
if [ -d "$MEFAN_ROOT/commands/project-upgrade" ]; then
    for f in "$MEFAN_ROOT/commands/project-upgrade/"*.md; do
        [ -f "$f" ] || continue
        filename=$(basename "$f")
        case "$filename" in
            00-init.md)       newname="mf-upgrade:00-init.md" ;;
            01-requirements.md) newname="mf-upgrade:01-requirements.md" ;;
            02-arch-qa.md)    newname="mf-upgrade:02-arch-qa.md" ;;
            03-plan.md)        newname="mf-upgrade:03-plan.md" ;;
            04-implement.md)   newname="mf-upgrade:04-implement.md" ;;
            05-quality.md)     newname="mf-upgrade:05-quality.md" ;;
            06-retrospect.md) newname="mf-upgrade:06-retrospect.md" ;;
            auto.md)           newname="mf-upgrade:auto.md" ;;
            *)                 newname="$filename" ;;
        esac
        cp "$f" "$SCRIPT_DIR/.claude/commands/$newname"
    done
fi

echo ">>> 复制 Templates..."
mkdir -p "$SCRIPT_DIR/.claude/templates"
for f in "$MEFAN_ROOT/templates/"*.md; do
    [ -f "$f" ] && cp "$f" "$SCRIPT_DIR/.claude/templates/"
done

# project-refactor → mf-refactor:
if [ -d "$MEFAN_ROOT/commands/project-refactor" ]; then
    mkdir -p "$SCRIPT_DIR/.claude/commands/mf-refactor"
    for f in "$MEFAN_ROOT/commands/project-refactor/"*.md; do
        [ -f "$f" ] || continue
        filename=$(basename "$f")
        newname="mf-refactor:$filename"
        cp "$f" "$SCRIPT_DIR/.claude/commands/$newname"
    done
fi

# project-new → mf-new:
if [ -d "$MEFAN_ROOT/commands/project-new" ]; then
    mkdir -p "$SCRIPT_DIR/.claude/commands/mf-new"
    for f in "$MEFAN_ROOT/commands/project-new/"*.md; do
        [ -f "$f" ] || continue
        filename=$(basename "$f")
        newname="mf-new:$filename"
        cp "$f" "$SCRIPT_DIR/.claude/commands/$newname"
    done
fi

echo ">>> 生成 .claude/settings.json..."
cat > "$SCRIPT_DIR/.claude/settings.json" << 'EOSETTINGS'
{
  "permissions": {
    "allow": [
      "Bash(git:*)",
      "Edit(.claude)",
      "Read"
    ]
  }
}
EOSETTINGS

echo ""
echo ">>> =================================================="
echo ">>> mefan Harness 安装完成！"
echo ">>> =================================================="
echo ""
echo "可用命令（通过 / 前缀触发）："
echo "  /mf-upgrade:00-init      - 会话初始化"
echo "  /mf-upgrade:01-requirements - 需求澄清"
echo "  /mf-upgrade:02-arch-qa   - 架构设计"
echo "  /mf-upgrade:03-plan      - 迭代计划"
echo "  /mf-upgrade:04-implement - 迭代实现"
echo "  /mf-upgrade:05-quality   - 质量测试"
echo "  /mf-upgrade:06-retrospect - 迭代总结"
echo "  /mf-upgrade:auto         - 自动推进"
echo ""
echo "框架文件位置："
echo "  .claude/ - 命令、Agent、规则、技能（Claude Code 标准结构）"
echo "  .mefan/  - 模板、Hooks、迭代记录（框架自身）"
echo ""
echo "卸载：bash init.sh --uninstall"