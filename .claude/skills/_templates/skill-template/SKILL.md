# Skill 模板

> **路径**：`.claude/skills/<category>-<framework>/SKILL.md`
> **用途**：当 Architect Agent 检测到对应框架时，调用此 Skill 进行深度调查
> **触发条件**：自动检测（package.json扫描） + 人工确认

---

## Skill 元数据

```yaml
name: frontend-redux
name_zh: 前端 Redux 框架调查
category: frontend
framework: redux
version: 1.0.0
author: Architect Agent
created: 2026-05-22
trigger: auto-detect
trigger_files:
  - package.json (contains "redux")
  - src/store/index.ts
  - src/reducers/
```

---

## 1. 框架概述

> 此框架在项目中的定位和技术选型理由

| 项目 | 内容 |
|------|------|
| **框架版本** | React 18.x + Redux Toolkit |
| **核心作用** | 统一状态管理，支持复杂前端应用的数据流 |
| **为什么选型** | [从 knowledge.grap 或人工访谈获取] |
| **替代方案对比** | Redux vs MobX vs Zustand vs Context API |

---

## 2. 目录结构规范

> 框架相关代码的目录组织

```
src/
├── store/                 # Redux Store 配置
│   ├── index.ts          # Store 入口
│   ├── configureStore.ts # Store 创建
│   └── rootReducer.ts    # Root Reducer
├── reducers/             # Reducer 目录（按模块划分）
│   ├── index.ts          # Reducer 合并
│   └── {feature}/
│       └── {feature}Slice.ts  # RTK Slice
├── actions/              # Action Creators（传统方式）
│   └── {feature}Actions.ts
├── sagas/                # Redux Saga（如果使用）
│   └── {feature}Saga.ts
├── selectors/            # Memoized Selectors
│   └── {feature}Selectors.ts
├── types/                # TypeScript 类型定义
│   └── redux.ts          # Redux 全局类型
└── middleware/           # 中间件
    └── {custom}Middleware.ts
```

---

## 3. 核心元素调查清单

### 3.1 Store 配置

| 调查项 | 文件位置 | 行号 | 说明 |
|--------|---------|------|------|
| Store 创建方式 | `src/store/index.ts` | : | configureStore vs legacy createStore |
| 中间件配置 | `src/store/index.ts` | : | thunk/saga/observable |
| DevTools 配置 | `src/store/index.ts` | : | 是否启用 |

### 3.2 Action 定义

| 调查项 | 文件位置 | 行号 | 说明 |
|--------|---------|------|------|
| Action Type 常量定义 | `src/actions/` | : | 命名规范（FIXME_ / feature/action） |
| Action Creator 模式 | `src/actions/` | : | createAction vs 函数 |
| Payload 结构 | `src/actions/` | : | 是否使用 Immer |

### 3.3 Reducer 编写

| 调查项 | 文件位置 | 行号 | 说明 |
|--------|---------|------|------|
| Reducer 组织方式 | `src/reducers/` | : | combineReducers vs createSlice |
| State 结构 | `src/reducers/` | : | 嵌套 vs 扁平 |
| Immer 使用 | `src/reducers/` | : | 是否启用 |

### 3.4 异步处理

| 调查项 | 文件位置 | 行号 | 说明 |
|--------|---------|------|------|
| 异步方案 | `src/` | : | thunk vs saga vs RTK Query |
| 异步 Action 命名 | `src/` | : | pending/fulfilled/rejected 约定 |
| Error 处理 | `src/` | : | rejected action 处理 |

---

## 4. 代码样例索引

> Dev Agent 需要引用的关键代码位置

| 模式 | 文件 | 行号 | 说明 |
|------|------|------|------|
| Store 创建 | `src/store/index.ts` | 1-20 | 完整示例 |
| Slice 定义 | `src/reducers/user/userSlice.ts` | 1-30 | RTK slice 模板 |
| Selector | `src/selectors/userSelectors.ts` | 1-15 | createSelector 示例 |
| API 调用 | `src/api/userApi.ts` | 1-40 | RTK Query 定义 |

---

## 5. 命名约定

| 元素 | 规范 | 示例 |
|------|------|------|
| Action Type | `feature/action` 小写下划线 | `user/login` |
| Action Creator | `use` 前缀或动词 | `loginUser()` |
| Reducer | 名词，`Slice` 后缀 | `userSlice` |
| Selector | `use` 前缀 | `useSelectUser()` |
| State | 驼峰名词 | `currentUser` |

---

## 6. 禁止做法

| 禁止 | 原因 | 正确做法 |
|------|------|---------|
| 在组件内直接 dispatch | 违反单一数据流 | 使用 useDispatch hook |
| 直接修改 state | Immer 不可变更新 | 使用 spread 或 produce |
| 在 reducer 内调用 API | 副作用 | 使用 thunk/saga |

---

## 7. 依赖版本清单

| 库 | 版本 | 文件证据 |
|----|------|---------|
| react | | package.json |
| react-redux | | package.json |
| @reduxjs/toolkit | | package.json |
| redux-thunk | | package.json |

---

## 8. 常见问题与解决

| 问题 | 解决方案 | 证据文件 |
|------|---------|---------|
| 异步状态管理 | RTK Query / createAsyncThunk | |
| 范式化 state | normalize state with entityAdapter | |
| 重置 store | store.reset() | |
| 持久化 | redux-persist 配置 | |

---

## 9. Reference（参考文档）

| 文档 | 路径 |
|------|------|
| Redux 官方文档 | https://redux.js.org |
| RTK 官方文档 | https://redux-toolkit.js.org |
| TypeScript 集成 | https://redux.js.org/tutorials/typescript-quick-start |

---

## Scripts（执行脚本）

> 此 Skill 相关的自动化脚本

| 脚本名 | 路径 | 说明 |
|--------|------|------|
| detect-redux.sh | `scripts/detect-redux.sh` | 检测项目是否使用 Redux |
| extract-redux-patterns.sh | `scripts/extract-redux-patterns.sh` | 提取 Redux 代码模式 |

---

## 与其他 Skill 的关系

```yaml
depends_on:
  - frontend-common  # 前端公共调查能力
  - api-contract    # API 契约调查能力
provides_to:
  - architect-stage0  # 为 Architect Agent 提供框架知识
  - dev-stage4        # 为 Dev Agent 提供代码规范
```