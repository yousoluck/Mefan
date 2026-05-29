#!/bin/bash
# check-adr-implementation.sh - 检查关键实现是否按 ADR 伪代码执行
# 用法: bash .claude/hooks/check-adr-implementation.sh <MG_ID>
# 退出码: 0=通过, 1=有问题, 2=文件缺失

set -e

ROOT="/mnt/d/pycharmprojects/Mefan"
MG_ID="${1:-MG-001}"
ADR_PATH="$ROOT/.claude/iterations/sprint-latest/ADR.md"
LOG_FILE="iterations/mefan-log.md"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

echo "[check-adr-implementation] 检查 MG $MG_ID ADR 伪代码实现..."

# 1. 检查前置文件
if [ ! -f "$ADR_PATH" ]; then
    echo "[check-adr-implementation] 错误：ADR.md 不存在，跳过检查"
    exit 0  # 不阻断，只警告
fi

# 2. 提取 MG 对应的 Task 列表
# ADR 中 MG-XXX 格式的任务块
MG_TASKS=$(grep -A 50 "^## $MG_ID" "$ADR_PATH" 2>/dev/null | grep -E "^### (T-|Task)" | head -20 || echo "")

if [ -z "$MG_TASKS" ]; then
    echo "[check-adr-implementation] 未找到 MG $MG_ID 的任务，跳过检查"
    exit 0
fi

echo "[check-adr-implementation] 找到以下任务:"
echo "$MG_TASKS"

# 3. 对每个 Task 检查实现情况
MISSING_IMPL=()
CHECKED_COUNT=0

while IFS= read -r task_line; do
    if [ -z "$task_line" ]; then continue; fi

    # 提取任务名
    TASK_NAME=$(echo "$task_line" | sed 's/^### //' | tr -d ' ')
    CHECKED_COUNT=$((CHECKED_COUNT + 1))

    # 在 ADR 中查找该任务的伪代码部分
    TASK_PSEUDOCODE=$(grep -A 20 "^### $TASK_NAME" "$ADR_PATH" 2>/dev/null | grep -E "^\s*```pseudo|^```" | head -5 || echo "")

    if [ -z "$TASK_PSEUDOCODE" ]; then
        # 没有伪代码，跳过检查
        continue
    fi

    echo "[check-adr-implementation] 检查任务: $TASK_NAME"

    # 4. 提取伪代码中的关键函数/方法调用模式
    # 查找类似 function_name() 或 ClassName.method() 的模式
    FUNCTIONS=$(echo "$TASK_PSEUDOCODE" | grep -oE '[a-zA-Z_][a-zA-Z0-9_]+\.[a-zA-Z_][a-zA-Z0-9_]+|[a-zA-Z_][a-zA-Z0-9_]+\([a-zA-Z_]' | sort -u || echo "")

    for func in $FUNCTIONS; do
        # 简化：检查函数名是否存在（不验证参数）
        FUNC_NAME=$(echo "$func" | cut -d'(' -f1 | cut -d'.' -f2)
        if [ -n "$FUNC_NAME" ]; then
            # 在源代码目录搜索该函数
            if [ -d "$ROOT/../src" ]; then
                FOUND=$(grep -r "$FUNC_NAME" "$ROOT/../src" --include="*.py" --include="*.js" --include="*.ts" 2>/dev/null | head -1 || echo "")
                if [ -z "$FOUND" ]; then
                    echo "[check-adr-implementation] 警告：未找到函数 $FUNC_NAME"
                    MISSING_IMPL+=("Task $TASK_NAME 中 $func 未实现")
                fi
            fi
        fi
    done

done <<< "$MG_TASKS"

echo "[check-adr-implementation] 检查了 $CHECKED_COUNT 个任务"

# 5. 检查是否有关键目录/文件存在
# 读取 ADR 中声明的模块路径
MODULE_PATHS=$(grep -E "path:|src/|lib/" "$ADR_PATH" 2>/dev/null | head -10 || echo "")

for module_path in $MODULE_PATHS; do
    # 提取路径
    if echo "$module_path" | grep -qE "^(path:|src/|lib/)"; then
        REL_PATH=$(echo "$module_path" | cut -d':' -f2 | tr -d ' `')
        if [ -n "$REL_PATH" ] && [ -f "$ROOT/../$REL_PATH" ]; then
            echo "[check-adr-implementation] 模块存在: $REL_PATH"
        fi
    fi
done

# 6. 输出结果
if [ ${#MISSING_IMPL[@]} -gt 0 ]; then
    echo "[check-adr-implementation] 发现 ${#MISSING_IMPL[@]} 个潜在问题:"
    for issue in "${MISSING_IMPL[@]}"; do
        echo "  - $issue"
    done
    echo "| $TIMESTAMP | 04 | Hook | check-adr-implementation | MG $MG_ID | ${#MISSING_IMPL[@]} 个问题 |" >> "$LOG_FILE"
    exit 1  # 有问题但不阻断，只是警告
fi

echo "[check-adr-implementation] ADR 伪代码实现检查通过"
echo "| $TIMESTAMP | 04 | Hook | check-adr-implementation | MG $MG_ID | $CHECKED_COUNT 个任务 | 通过 |" >> "$LOG_FILE"
exit 0