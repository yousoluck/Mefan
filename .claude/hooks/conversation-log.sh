#!/bin/bash
# conversation-log.sh - 对话日志自动保存脚本
# 模式1: capture  - 从 stdin 读取 UserPromptSubmit JSON，保存用户输入
# 模式2: finalize <session_id> - 从 transcript 提取 AI 回复并写入日志

set -e

LOGFILE="/mnt/d/pycharmprojects/Mefan/logs/conversation-log.md"
TRANSCRIPT_DIR="$HOME/.claude/transcripts"
TEMP_DIR="/tmp/conversation-pending"
MODE="${1:-}"

mkdir -p "$TEMP_DIR"

# 初始化日志文件（如果不存在）
init_logfile() {
    if [ ! -f "$LOGFILE" ]; then
        cat > "$LOGFILE" << 'HEADER'
# 对话日志 (Conversation Log)
> 自动生成，每次对话后追加

## 使用说明
- 本文件记录所有对话内容
- 每条记录包含：时间戳、用户输入、AI回复、操作记录
- 格式：Markdown Table

---

## 日志记录

| 时间 | Agent | 用户输入 | AI回复摘要 | 操作记录 |
|------|-------|---------|-----------|----------|
HEADER
    fi
}

# 转义特殊字符（用于 Markdown table）
escape_markdown() {
    echo "$1" | sed 's/|/\\|/g; s/"/\\"/g; s/\n/ /g; s/\t/ /g' | xargs
}

# 模式1: capture - 从 stdin 读取 UserPromptSubmit JSON，保存用户输入
capture_user_input() {
    local session_id
    local user_msg

    # 从 stdin 读取 JSON
    local json_input
    json_input=$(cat)

    if command -v jq &> /dev/null; then
        session_id=$(echo "$json_input" | jq -r '.session_id // "unknown"')
        user_msg=$(echo "$json_input" | jq -r 'if .text then .text else "" end')
    else
        # 备用：使用 grep
        session_id=$(echo "$json_input" | grep -oP '"session_id":\s*"\K[^"]+' || echo "unknown")
        user_msg=$(echo "$json_input" | grep -oP '"text":\s*"\K[^"]+' || echo "")
    fi

    if [ -z "$user_msg" ]; then
        return
    fi

    local temp_file="$TEMP_DIR/user-$session_id.txt"
    local timestamp
    timestamp=$(date "+%Y-%m-%d %H:%M:%S")

    echo "[$timestamp] $user_msg" >> "$temp_file"
}

# 模式2: finalize - 从 transcript 提取对话并写入日志
finalize_log() {
    local session_id="${1:-}"

    # 如果没有提供 session_id，查找最新的 transcript 文件
    if [ -z "$session_id" ]; then
        # 等待一小段时间让 transcript 写入完成
        sleep 2
        # 找最新的 .json transcript 文件（按修改时间）
        session_id=$(ls -t "$TRANSCRIPT_DIR"/ 2>/dev/null | grep -E '\.json$' | head -1 | sed 's/\.json$//' || echo "")
    fi

    if [ -z "$session_id" ]; then
        echo "No transcript found" >&2
        return 1
    fi

    local transcript_file="$TRANSCRIPT_DIR/$session_id.json"

    if [ ! -f "$transcript_file" ]; then
        echo "Transcript not found: $transcript_file" >&2
        ls -la "$TRANSCRIPT_DIR/" 2>/dev/null || echo "Directory not found" >&2
        return 1
    fi

    init_logfile

    local timestamp
    timestamp=$(date "+%Y-%m-%d %H:%M:%S")

    # 读取临时文件中的用户输入
    local temp_file="$TEMP_DIR/user-$session_id.txt"
    local user_inputs=()
    if [ -f "$temp_file" ]; then
        while IFS= read -r line; do
            user_inputs+=("$line")
        done < "$temp_file"
        > "$temp_file"  # 清空
    fi

    # 提取 transcript 中的 assistant 消息
    local ai_responses=()
    if command -v jq &> /dev/null; then
        # 尝试多种 JSON 结构
        ai_responses=$(jq -r '.messages[]? | select(.type=="assistant" or .sender=="assistant" or .role=="assistant") | .content // .text // empty' "$transcript_file" 2>/dev/null || echo "")
    elif command -v python3 &> /dev/null; then
        # 使用 Python 解析
        ai_responses=$(python3 -c "
import json, sys
try:
    data = json.load(open('$transcript_file'))
    messages = data.get('messages', [])
    for msg in messages:
        if msg.get('type') == 'assistant' or msg.get('sender') == 'assistant' or msg.get('role') == 'assistant':
            content = msg.get('content') or msg.get('text') or ''
            if content:
                print(content)
except: pass
" 2>/dev/null || echo "")
    fi

    # 按顺序配对
    local total_pairs=${#user_inputs[@]}
    local ai_array=()
    while IFS= read -r line; do
        [ -n "$line" ] && ai_array+=("$line")
    done <<< "$ai_responses"

    local ai_count=${#ai_array[@]}
    local max_pairs=$((total_pairs > ai_count ? total_pairs : ai_count))

    for i in $(seq 0 $((max_pairs - 1))); do
        local user_part=""
        local ai_part="[AI回复]"

        if [ $i -lt $total_pairs ]; then
            user_part="${user_inputs[$i]}"
            user_part="${user_part#\[*\] }"
        fi

        if [ $i -lt $ai_count ]; then
            ai_part="${ai_array[$i]}"
        fi

        local user_esc=$(escape_markdown "$user_part")
        local ai_esc=$(escape_markdown "$ai_part")

        echo "| $timestamp | assistant | $user_esc | $ai_esc | transcript:$session_id |" >> "$LOGFILE"
    done

    if [ $max_pairs -eq 0 ]; then
        echo "| $timestamp | assistant | [用户消息] | [AI回复见transcript] | transcript:$session_id |" >> "$LOGFILE"
    fi

    echo "Log finalized: $max_pairs pairs written" >&2
}

# 主逻辑
case "$MODE" in
    capture)
        capture_user_input
        ;;
    finalize)
        finalize_log "${2:-}"
        ;;
    *)
        echo "Usage: $0 {capture|finalize} [session_id]" >&2
        exit 1
        ;;
esac
