#!/bin/bash
# conversation-log.sh - 对话日志自动保存脚本
# 用法: bash .claude/hooks/conversation-log.sh "<agent>" "<user_message>" "<ai_response>" "<operations>"

AGENT="${1:-assistant}"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
LOGFILE="/mnt/d/pycharmprojects/Mefan/logs/conversation-log.md"

# 初始化日志文件（如果不存在）
if [ ! -f "$LOGFILE" ]; then
    echo "# 对话日志 (Conversation Log)
> 自动生成，每次对话后追加

## 使用说明
- 本文件记录所有对话内容
- 每条记录包含：时间戳、用户输入、AI回复、操作记录
- 格式：Markdown Table

---

## 日志记录

| 时间 | Agent | 用户输入 | AI回复摘要 | 操作记录 |
|------|-------|---------|-----------|----------|
" > "$LOGFILE"
fi

USER_MSG="${2:-}"
AI_RESP="${3:-}"
OPS="${4:-}"

# 转义特殊字符
USER_MSG_ESC=$(echo "$USER_MSG" | sed 's/|/\\|/g; s/"/\\"/g; s/\n/<br>/g')
AI_RESP_ESC=$(echo "$AI_RESP" | sed 's/|/\\|/g; s/"/\\"/g; s/\n/<br>/g')
OPS_ESC=$(echo "$OPS" | sed 's/|/\\|/g; s/"/\\"/g; s/\n/<br>/g')

# 追加到日志
echo "| $TIMESTAMP | $AGENT | $USER_MSG_ESC | $AI_RESP_ESC | $OPS_ESC |" >> "$LOGFILE"