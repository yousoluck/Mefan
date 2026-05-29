#!/bin/bash
# check-tdd-rhythm.sh - 验证 TDD 红→绿→重构循环是否完整
# 用法: bash .claude/hooks/check-tdd-rhythm.sh <MG_ID>
# 退出码: 0=通过, 1=有问题, 2=异常

set -e

ROOT="/mnt/d/pycharmprojects/Mefan"
MG_ID="${1:-MG-001}"
LOG_FILE="iterations/mefan-log.md"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

echo "[check-tdd-rhythm] 检查 MG $MG_ID TDD 节奏..."

# 1. 查找测试文件和实现文件
TESTS_DIR="$ROOT/../tests"
SRC_DIR="$ROOT/../src"

ISSUES=()

# 2. 检查是否每个实现文件都有对应的测试文件
if [ -d "$TESTS_DIR" ] && [ -d "$SRC_DIR" ]; then
    echo "[check-tdd-rhythm] 检查测试文件覆盖率..."

    # 查找 src 目录下的实现文件
    find "$SRC_DIR" -type f \( -name "*.py" -o -name "*.js" -o -name "*.ts" \) 2>/dev/null | while read -r impl_file; do
        impl_basename=$(basename "$impl_file")
        impl_name="${impl_basename%.*}"

        # 对应的测试文件可能的命名
        test_candidates=(
            "${TESTS_DIR}/${impl_name}.test.js"
            "${TESTS_DIR}/${impl_name}.test.ts"
            "${TESTS_DIR}/${impl_name}.spec.js"
            "${TESTS_DIR}/${impl_name}.spec.ts"
            "${TESTS_DIR}/$(echo "$impl_name" | sed 's/_test$//').test.js"
        )

        test_found=false
        for tc in "${test_candidates[@]}"; do
            if [ -f "$tc" ]; then
                test_found=true
                break
            fi
        done

        if [ "$test_found" = false ]; then
            # 排除 __init__.py 等非功能文件
            if ! echo "$impl_name" | grep -qE "^__|test_|spec_"; then
                echo "[check-tdd-rhythm] 警告：缺少测试文件 for $impl_file"
                ISSUES+=("缺少测试: $impl_name")
            fi
        fi
    done
fi

# 3. 检查测试文件中的 RED 阶段标记
# 正常 TDD 流程：测试文件应该先存在（RED），然后实现
# 检查测试文件是否为空（只有 describe/it 没有实际断言）
find "$TESTS_DIR" -type f \( -name "*.test.js" -o -name "*.test.ts" -o -name "*.spec.js" -o -name "*.spec.ts" \) 2>/dev/null | while read -r test_file; do
    if [ ! -s "$test_file" ]; then
        echo "[check-tdd-rhythm] 警告：测试文件为空 $test_file"
        ISSUES+=("空测试文件: $test_file")
    fi

    # 检查是否有 expect 语句（GREEN 阶段的标记）
    if ! grep -qE "expect\(|assert\(" "$test_file" 2>/dev/null; then
        # 没有 expect，可能是 RED 阶段的占位符（可接受）
        echo "[check-tdd-rhythm] 提示：测试文件可能处于 RED 阶段 $test_file"
    fi
done

# 4. 检查是否存在 "// REFACTOR:" 注释标记（重构节点）
# 这个检查是可选的，因为不是所有重构都需要标记
find "$SRC_DIR" -type f \( -name "*.py" -o -name "*.js" -o -name "*.ts" \) 2>/dev/null | while read -r impl_file; do
    refactor_count=$(grep -c "// REFACTOR:" "$impl_file" 2>/dev/null || echo "0")
    if [ "$refactor_count" -gt 0 ]; then
        echo "[check-tdd-rhythm] 重构标记: $impl_file 有 $refactor_count 个 REFACTOR 注释"
    fi
done

# 5. 输出结果
echo "[check-tdd-rhythm] TDD 节奏检查完成，发现 ${#ISSUES[@]} 个问题"

if [ ${#ISSUES[@]} -gt 0 ]; then
    for issue in "${ISSUES[@]}"; do
        echo "  - $issue"
    done
    echo "| $TIMESTAMP | 04 | Hook | check-tdd-rhythm | MG $MG_ID | ${#ISSUES[@]} 个问题 |" >> "$LOG_FILE"
    exit 1  # 有问题但只是警告
fi

echo "[check-tdd-rhythm] TDD 节奏检查通过"
echo "| $TIMESTAMP | 04 | Hook | check-tdd-rhythm | MG $MG_ID | 通过 |" >> "$LOG_FILE"
exit 0