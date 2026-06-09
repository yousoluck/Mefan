#!/bin/bash
# check-test-coverage.sh - 验证关键模块的测试覆盖
# 用法: bash .claude/hooks/check-test-coverage.sh <MG_ID> [threshold]
# 默认阈值: 80%
# 退出码: 0=通过, 1=未达标, 2=异常

set -e

ROOT="/mnt/d/pycharmprojects/Mefan"
MG_ID="${1:-MG-001}"
THRESHOLD="${2:-80}"
# Fixed: 原先路径使用了"向上跳一层"的形式（注释掉向下走一层的旧写法，避免目录永远不存在），
# 导致 hook 静默 no-op。改为相对项目根的写法。
TESTS_DIR="$ROOT/tests"
SRC_DIR="$ROOT/src"
LOG_FILE="iterations/mefan-log.md"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

echo "[check-test-coverage] 检查 MG $MG_ID 测试覆盖率..."

# 1. 检查目录是否存在
if [ ! -d "$TESTS_DIR" ]; then
    echo "[check-test-coverage] 警告：tests 目录不存在，跳过覆盖率检查"
    exit 0
fi

if [ ! -d "$SRC_DIR" ]; then
    echo "[check-test-coverage] 警告：src 目录不存在，跳过覆盖率检查"
    exit 0
fi

# 2. 统计实现文件和测试文件数量
impl_count=0
test_count=0

# 统计实现文件
impl_files=$(find "$SRC_DIR" -type f \( -name "*.py" -o -name "*.js" -o -name "*.ts" \) ! -name "__init__*" ! -name "*_test*" ! -name "*_spec*" 2>/dev/null || echo "")
impl_count=$(echo "$impl_files" | grep -v "^$" | wc -l)

# 统计测试文件
test_files=$(find "$TESTS_DIR" -type f \( -name "*.test.js" -o -name "*.test.ts" -o -name "*.spec.js" -o -name "*.spec.ts" -o -name "*.py" \) 2>/dev/null | grep -v "^$" || echo "")
test_count=$(echo "$test_files" | grep -v "^$" | wc -l)

echo "[check-test-coverage] 实现文件数: $impl_count"
echo "[check-test-coverage] 测试文件数: $test_count"

if [ "$impl_count" -eq 0 ]; then
    echo "[check-test-coverage] 没有实现文件，跳过覆盖率检查"
    exit 0
fi

# 3. 计算覆盖率
if [ "$impl_count" -gt 0 ]; then
    coverage=$((test_count * 100 / impl_count))
else
    coverage=0
fi

echo "[check-test-coverage] 测试覆盖率: $coverage% (阈值: ${THRESHOLD}%)"

# 4. 检查每个实现文件是否有对应的测试
MISSING_TESTS=()
for impl_file in $impl_files; do
    impl_basename=$(basename "$impl_file")
    impl_name="${impl_basename%.*}"

    # 对应的测试文件可能的命名
    test_found=false
    for suffix in "test" "spec" "_test" "_spec"; do
        for ext in "js" "ts" "py"; do
            candidate="${TESTS_DIR}/${impl_name}${suffix}.${ext}"
            if [ -f "$candidate" ]; then
                test_found=true
                break 2
            fi
        done
    done

    # 尝试其他模式
    if [ "$test_found" = false ]; then
        for pattern in "test_${impl_name}" "${impl_name}_test"; do
            candidate=$(find "$TESTS_DIR" -name "${pattern}.*" 2>/dev/null | head -1 || echo "")
            if [ -n "$candidate" ] && [ -f "$candidate" ]; then
                test_found=true
                break
            fi
        done
    fi

    if [ "$test_found" = false ]; then
        MISSING_TESTS+=("$impl_name")
    fi
done

# 5. 输出结果
if [ ${#MISSING_TESTS[@]} -gt 0 ]; then
    echo "[check-test-coverage] 警告：${#MISSING_TESTS[@]} 个实现文件缺少测试:"
    for mt in "${MISSING_TESTS[@]}"; do
        echo "  - $mt"
    done
fi

if [ "$coverage" -lt "$THRESHOLD" ]; then
    echo "[check-test-coverage] 错误：覆盖率 $coverage% 未达到阈值 ${THRESHOLD}%"
    echo "| $TIMESTAMP | 04 | Hook | check-test-coverage | MG $MG_ID | 覆盖率 $coverage% < ${THRESHOLD}% | 未达标 |" >> "$LOG_FILE"
    exit 1
fi

echo "[check-test-coverage] 测试覆盖率检查通过"
echo "| $TIMESTAMP | 04 | Hook | check-test-coverage | MG $MG_ID | 覆盖率 $coverage% | 通过 |" >> "$LOG_FILE"
exit 0