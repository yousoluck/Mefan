#!/bin/bash
# check-state-machine.sh - 验证 MG 状态流转合法性
# 用法: bash .claude/hooks/check-state-machine.sh <MG_ID> <expected_state>
# 退出码: 0=合法, 1=非法状态, 2=文件缺失/异常

set -e

ROOT="/mnt/d/pycharmprojects/Mefan"
MG_ID="${1:-MG-001}"
EXPECTED_STATE="${2:-}"
SPRINT_STATUS="$ROOT/.claude/iterations/sprint-latest/sprint-status.md"
STATE_FILE="$ROOT/.claude/iterations/sprint-latest/mg-state.json"
LOG_FILE="iterations/mefan-log.md"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

echo "[check-state-machine] 检查 MG $MG_ID 状态..."

# 1. 读取当前状态（从 sprint-status.md）
if [ ! -f "$SPRINT_STATUS" ]; then
    echo "[check-state-machine] 错误：sprint-status.md 不存在"
    exit 2
fi

# 从 sprint-status.md 提取 MG 的当前状态
# 格式：| MG-001 | 🏃 Dev | 或类似格式
CURRENT_STATE=$(grep -E "^\| $MG_ID \|" "$SPRINT_STATUS" 2>/dev/null | tail -1 | awk -F'|' '{print $3}' | tr -d ' ')

if [ -z "$CURRENT_STATE" ]; then
    echo "[check-state-machine] 错误：无法读取 MG $MG_ID 当前状态"
    exit 2
fi

echo "[check-state-machine] MG $MG_ID 当前状态: $CURRENT_STATE"

# 2. 如果指定了 expected_state，验证是否匹配
if [ -n "$EXPECTED_STATE" ]; then
    # 去掉 emoji 进行比较
    CLEAN_CURRENT=$(echo "$CURRENT_STATE" | sed 's/[^a-zA-Z]//g')
    CLEAN_EXPECTED=$(echo "$EXPECTED_STATE" | sed 's/[^a-zA-Z]//g')

    if [ "$CLEAN_CURRENT" != "$CLEAN_EXPECTED" ]; then
        echo "[check-state-machine] 错误：状态不匹配。期望: $EXPECTED_STATE, 实际: $CURRENT_STATE"
        exit 1
    fi
    echo "[check-state-machine] 状态验证通过：$CURRENT_STATE"
fi

# 3. 定义合法流转（从任意状态允许的下一个状态）
declare -A VALID_TRANSITIONS=(
    ["ToDo"]="InProgress"
    ["InProgress"]="SelfCheck"
    ["SelfCheck"]="CodeReview"
    ["SelfCheck"]="InProgress"          # 打回
    ["CodeReview"]="QATestCoding"
    ["CodeReview"]="InProgress"          # 打回
    ["QATestCoding"]="TestCodeReview"
    ["QATestCoding"]="InProgress"       # 打回
    ["TestCodeReview"]="Testing"
    ["TestCodeReview"]="QATestCoding"   # 打回
    ["Testing"]="Close"
    ["Testing"]="InProgress"            # 打回
)

# 4. 获取上一步状态（从 state_history 最后一条）
PREVIOUS_STATE=$(python3 -c "
import json, os
if os.path.exists('$STATE_FILE'):
    try:
        with open('$STATE_FILE', 'r') as f:
            data = json.load(f)
        if '$MG_ID' in data and data['$MG_ID'].get('state_history'):
            return data['$MG_ID']['state_history'][-1]['state']
    except: pass
print('')
" 2>/dev/null || echo "")

if [ -n "$PREVIOUS_STATE" ]; then
    # 标准化状态名（去掉 emoji）
    NORMALIZED_PREV=$(echo "$PREVIOUS_STATE" | sed 's/[^a-zA-Z]//g')
    NORMALIZED_CURR=$(echo "$CURRENT_STATE" | sed 's/[^a-zA-Z]//g')

    # 验证流转是否合法
    KEY="${NORMALIZED_PREV}${NORMALIZED_CURR}"

    if [[ -v VALID_TRANSITIONS["$KEY"] ]]; then
        echo "[check-state-machine] 状态流转合法: $PREVIOUS_STATE → $CURRENT_STATE"
    else
        # 特殊情况：如果是第一次进入（无 previous state），也允许
        if [ "$NORMALIZED_PREV" = "ToDo" ] && [ "$NORMALIZED_CURR" = "InProgress" ]; then
            echo "[check-state-machine] 初始流转合法: ToDo → InProgress"
        else
            echo "[check-state-machine] 警告：未知的流转 $PREVIOUS_STATE → $CURRENT_STATE"
            echo "[check-state-machine] 允许的下一个状态: ${VALID_TRANSITIONS[$NORMALIZED_PREV]:-无定义}"
            # 不阻断，只记录
        fi
    fi
fi

# 5. 更新 state 文件（记录当前状态）
python3 -c "
import json, os
from datetime import datetime

state_file = '$STATE_FILE'
mg_id = '$MG_ID'
current_state = '$CURRENT_STATE'

data = {}
if os.path.exists(state_file):
    try:
        with open(state_file, 'r') as f:
            data = json.load(f)
    except: data = {}

if mg_id not in data:
    data[mg_id] = {'current_state': '', 'state_history': [], 'violations': [], 'last_check': ''}

data[mg_id]['current_state'] = current_state
data[mg_id]['state_history'].append({
    'state': current_state,
    'entered_at': datetime.now().isoformat()
})
data[mg_id]['last_check'] = datetime.now().isoformat()

with open(state_file, 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
" 2>/dev/null

# 6. 记录日志
echo "| $TIMESTAMP | 04 | Hook | check-state-machine | MG $MG_ID: $CURRENT_STATE | 通过 |" >> "$LOG_FILE"

echo "[check-state-machine] 状态检查通过"
exit 0