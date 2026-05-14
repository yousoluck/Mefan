#!/bin/bash
# 用法: log-event.sh <阶段> <Agent> <事件类型> <描述> <关联> <结果>
LOG_FILE="iterations/mefan-log.md"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

# 若文件不存在，写入表头
if [ ! -f "$LOG_FILE" ]; then
  echo "| 时间戳 | 阶段 | Agent | 事件类型 | 描述 | 关联文件/规则/技能 | 结果 |" >> "$LOG_FILE"
  echo "|--------|------|-------|---------|------|-------------------|------|" >> "$LOG_FILE"
fi

echo "| $TIMESTAMP | $1 | $2 | $3 | $4 | $5 | $6 |" >> "$LOG_FILE"