#!/bin/bash
# extract-redux-patterns.sh - 提取 Redux 代码模式

echo "[extract-redux-patterns] 开始提取 Redux 代码模式..."

# 提取 Store 配置
echo "=== Store Configuration ===" >> $PATTERN_OUTPUT
find src -name "store.ts" -o -name "configureStore.ts" -o -name "index.ts" | while read f; do
  echo "File: $f" >> $PATTERN_OUTPUT
  head -50 "$f" >> $PATTERN_OUTPUT
  echo "---" >> $PATTERN_OUTPUT
done

# 提取 Reducer
echo "=== Reducers ===" >> $PATTERN_OUTPUT
find src -path "*/reducers/*.ts" | while read f; do
  echo "File: $f" >> $PATTERN_OUTPUT
  head -30 "$f" >> $PATTERN_OUTPUT
  echo "---" >> $PATTERN_OUTPUT
done

# 提取 Slices
echo "=== Slices ===" >> $PATTERN_OUTPUT
find src -name "*Slice.ts" | while read f; do
  echo "File: $f" >> $PATTERN_OUTPUT
  head -40 "$f" >> $PATTERN_OUTPUT
  echo "---" >> $PATTERN_OUTPUT
done

echo "[extract-redux-patterns] ✅ 提取完成"