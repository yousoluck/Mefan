#!/bin/bash
# detect-redux.sh - 检测项目是否使用 Redux

echo "[detect-redux] 检查项目是否使用 Redux 框架..."

# 检测 package.json
if [ -f "package.json" ]; then
  if grep -q '"@reduxjs/toolkit"\|"redux"\|"react-redux"' package.json; then
    echo "[detect-redux] ✅ 检测到 Redux 相关依赖"
    echo "REDFRM=redux" >> $TMP_ENV
    return 0
  fi
fi

# 检测 src/store 目录
if [ -d "src/store" ] || [ -d "src/redux" ]; then
  echo "[detect-redux] ✅ 检测到 Redux 目录结构"
  echo "REDFRM=redux" >> $TMP_ENV
  return 0
fi

# 检测 redux 配置文件
if [ -f "src/store/index.ts" ] || [ -f "src/store/configureStore.ts" ]; then
  echo "[detect-redux] ✅ 检测到 Redux 配置文件"
  echo "REDFRM=redux" >> $TMP_ENV
  return 0
fi

echo "[detect-redux] ❌ 未检测到 Redux"
return 1