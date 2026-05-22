# Skill 元数据

```yaml
name: frontend-redux
name_zh: 前端 Redux 框架调查
category: frontend
framework: redux
version: 1.1.0
author: Architect Agent
created: 2026-05-22
trigger: auto-detect
trigger_files:
  - package.json (contains "@reduxjs/toolkit" OR "redux" OR "react-redux")
  - src/store/index.ts
  - src/reducers/
```

---

## 1. 框架概述

| 项目 | 内容 |
|------|------|
| **框架版本** | React + Redux Toolkit |
| **核心作用** | 统一状态管理，支持复杂前端应用的数据流 |
| **状态管理方案** | Redux Toolkit (RTK) / Redux Thunk / Redux Saga |
| **配套库** | react-redux, reselect |

---

## 2. 目录结构规范

```
src/
├── store/                      # Redux Store 配置
│   ├── index.ts               # Store 入口，configureStore
│   ├── rootReducer.ts        # Root Reducer 合并
│   └── middleware.ts          # 中间件配置
├── reducers/                  # Reducer 目录（按模块划分）
│   ├── index.ts              # combineReducers 合并
│   └── {feature}/
│       ├── {feature}Slice.ts  # RTK createSlice
│       └── {feature}Types.ts  # 类型定义
├── actions/                   # Action Creators（传统方式）
│   ├── index.ts
│   └── {feature}Actions.ts
├── thunks/                    # Async Thunks
│   └── {feature}Thunks.ts
├── sagas/                     # Redux Saga（如使用）
│   ├── index.ts
│   └── {feature}Sagas.ts
├── selectors/                 # Memoized Selectors
│   └── {feature}Selectors.ts
├── types/                     # 全局类型定义
│   └── index.ts
└── api/                       # API 层
    └── {feature}Api.ts        # RTK Query endpoints
```

---

## 3. 核心元素调查清单

### 3.1 Store 配置

| 调查项 | 关键问题 | 证据文件:行号 |
|--------|---------|--------------|
| **Store 创建方式** | 使用 configureStore 还是 legacy createStore？ | |
| **中间件配置** | thunk/saga/observable 如何配置？ | |
| **DevTools** | 是否启用 Redux DevTools Extension？ | |
| **Store 结构** | state 如何组织（嵌套 vs 扁平）？ | |
| **Root Reducer** | 如何合并 sub-reducers？ | |

### 3.2 Redux Toolkit (RTK) 使用

| 调查项 | 关键问题 | 证据文件:行号 |
|--------|---------|--------------|
| **createSlice** | 是否使用 createSlice 替代手动 reducer？ | |
| **createAsyncThunk** | 异步操作是否使用 createAsyncThunk？ | |
| **createEntityAdapter** | 是否使用 normalize state？ | |
| **createSelector** | 是否使用 memoized selectors？ | |
| **configureStore** | 如何替代 legacy createStore？ | |

### 3.3 Action 定义模式

| 调查项 | 关键问题 | 证据文件:行号 |
|--------|---------|--------------|
| **Action Type 命名** | 命名规范是什么？ (`feature/action` vs `FEATURE/ACTION`) | |
| **Action Creators** | 使用 createAction 还是函数式？ | |
| **Payload 结构** | Immer produce 如何使用？ | |
| **Pending/Fulfilled/Rejected** | 异步 action 的命名约定？ | |

### 3.4 Reducer 编写模式

| 调查项 | 关键问题 | 证据文件:行号 |
|--------|---------|--------------|
| **Reducer 组织** | combineReducers vs createSlice？ | |
| **Immer 不可变更新** | 是否使用 `state.xxx = value` 直接修改？ | |
| **Initial State** | 如何定义初始状态？ | |
| **Extra Reducers** | createSlice.extraReducers 如何使用？ | |

### 3.5 异步处理模式

| 调查项 | 关键问题 | 证据文件:行号 |
|--------|---------|--------------|
| **异步方案选择** | thunk vs saga vs RTK Query？ | |
| **Async Thunk 定义** | createAsyncThunk 如何定义？ | |
| **Error 处理** | rejected action 如何处理？ | |
| **Loading 状态** | 如何追踪 loading 状态？ | |

### 3.6 组件与 Store 连接

| 调查项 | 关键问题 | 证据文件:行号 |
|--------|---------|--------------|
| **useSelector** | 如何高效订阅 state？ | |
| **useDispatch** | 如何 dispatch action？ | |
| **connect HOC** | 是否还使用 connect？ | |
| **useActions** | 是否使用 bound action creators？ | |
| **Context** | Redux Context 如何配置？ | |

---

## 4. 代码样例索引（必须提供行号）

| 模式 | 文件路径 | 行号范围 | 说明 |
|------|---------|---------|------|
| **Store 创建** | `src/store/index.ts` | : | configureStore 完整配置 |
| **Slice 定义** | `src/reducers/user/userSlice.ts` | : | createSlice 模板 |
| **Async Thunk** | `src/thunks/userThunks.ts` | : | createAsyncThunk 模板 |
| **Selector** | `src/selectors/userSelectors.ts` | : | createSelector 模板 |
| **API Endpoint** | `src/api/userApi.ts` | : | RTK Query endpoint |
| **Type 定义** | `src/types/redux.ts` | : | Action/State 类型 |
| **Middleware** | `src/store/middleware.ts` | : | 中间件配置 |

---

## 5. 命名约定调查

| 调查项 | 关键问题 | 证据文件:行号 |
|--------|---------|--------------|
| **Action Type 格式** | 使用 `feature/action` 小写 还是 `FEATURE/ACTION` 大写？还是枚举类型？ | |
| **Action Type 定义位置** | 在 `types/actionTypes.ts` 还是直接在 slice 里定义？ | |
| **Slice 命名** | 后缀是 `Slice` 还是其他？如 `userSlice` vs `userReducer` | |
| **Selector 命名** | 前缀是 `use` 还是 `select`？如 `useSelectUser` vs `selectUserById` | |
| **Thunk 命名** | 前缀用什么？`fetchUser` vs `loadUser` vs `getUser`？ | |
| **State 变量** | 驼峰还是下划线？如 `currentUser` vs `current_user`？ | |
| **文件命名** | 驼峰还是 kebab-case？如 `userSlice.ts` vs `user-slice.ts`？ | |

---

## 6. 禁止做法（反模式）

| 禁止 | 原因 | 正确做法 | 证据 |
|------|------|---------|------|
| **在 reducer 直接修改 state** | 违反 Immer 不可变原则 | 使用 `produce()` 或展开运算符 | `src/reducers/userSlice.ts:23` |
| **在组件内直接调用 API** | 违反分层架构 | 通过 thunk/saga 调用 | |
| **在 reducer 内 dispatch** | 导致循环 dispatch | 使用中间件处理副作用 | |
| **使用 class 风格的 action type** | 已被 RTK 替代 | 使用 `createSlice` | |
| **在 render 中 dispatch** | 导致性能问题 | 使用回调或 useCallback | |

---

## 7. 依赖版本调查

| 调查项 | 关键问题 | 证据文件 |
|--------|---------|---------|
| **react 版本** | 项目使用的 React 版本？ | package.json |
| **Redux 版本** | Redux vs Redux Toolkit？具体版本？ | package.json |
| **react-redux 版本** | 使用的 hooks API 还是 connect HOC？ | package.json |
| **reselect** | 是否使用 createSelector？ | package.json |
| **其他中间件** | thunk / saga / observable？ | package.json |

---

## 8. 常见问题调查

| 调查项 | 关键问题 | 证据文件:行号 |
|--------|---------|--------------|
| **持久化方案** | 使用 redux-persist？如何配置？ | |
| **重置 store** | 如何实现 store reset？自定义 rootReducer？ | |
| **Normalized State** | 是否使用 createEntityAdapter？结构如何？ | |
| **性能优化** | 使用 createSelector 做 memoization？ | |
| **TypeScript 类型** | 如何定义 RootState/AppDispatch？ | |

---

## 8.1 组件间状态传递调查

| 调查项 | 关键问题 | 证据文件:行号 |
|--------|---------|--------------|
| **Props drilling** | 组件如何接收父组件数据？逐层传递还是 Context？ | |
| **Context/Provider** | Context 如何组织？多个 Provider 还是单一 Provider？ | |
| **useSelector 高效订阅** | 如何避免不必要的 re-render？selector 如何优化？ | |
| **组件通信方式** | props/callback/Context/Redux 如何选择？ | |
| **HOC 使用** | 是否使用高阶组件？connect HOC vs hooks API？ | |

---

## 8.2 页面间状态传递调查

| 调查项 | 关键问题 | 证据文件:行号 |
|--------|---------|--------------|
| **路由状态** | React Router 如何管理路由状态？ | |
| **URL 参数获取** | params/query string 如何获取和使用？ | |
| **持久化状态** | localStorage/sessionStorage/URL 参数如何选择？ | |
| **全局状态共享** | Redux/Context 如何在页面间共享数据？ | |
| **页面跳转后状态恢复** | 如何保持滚动位置等状态？ | |

---

## 8.3 API 数据处理流程调查

| 调查项 | 关键问题 | 证据文件:行号 |
|--------|---------|--------------|
| **API 调用层位置** | `api/`/`services/`/`endpoints/` 哪个目录？ | |
| **统一接口调用** | 是否通过统一 API 层？还是组件内直接调用？ | |
| **Base URL 配置** | axios instance 如何配置？ | |
| **请求拦截器** | 如何添加 auth token 等通用参数？ | |
| **响应拦截器** | 响应如何统一处理错误、数据转换？ | |
| **响应数据格式** | JSON 结构如何？data/data.result 分层？ | |
| **Loading/Error 状态** | API 调用时如何管理 loading 和 error 状态？ | |
| **数据归一化** | 响应数据如何转换和规范化？ | |

---

## 8.4 数据库模式调查（前端相关）

| 调查项 | 关键问题 | 证据文件:行号 |
|--------|---------|--------------|
| **本地存储方案** | localStorage/IndexedDB 如何组织？ | |
| **缓存策略** | React Query/SWR/Redux Persist 如何使用？ | |
| **数据持久化** | 刷新页面后如何恢复状态？ | |
| **离线支持** | 是否支持离线操作？如何同步？ | |

---

## 9. Scripts（执行脚本）

| 脚本名 | 路径 | 说明 |
|--------|------|------|
| `detect-redux.sh` | `scripts/detect-redux.sh` | 检测项目是否使用 Redux |
| `extract-redux-patterns.sh` | `scripts/extract-redux-patterns.sh` | 提取 Redux 代码模式 |

### detect-redux.sh
```bash
#!/bin/bash
# 检测项目是否使用 Redux
# 返回：REDFRM=redux 或返回错误
```

### extract-redux-patterns.sh
```bash
#!/bin/bash
# 提取 Redux 代码模式到 $PATTERN_OUTPUT
# 提取：Store/Slice/Thunk/API 定义
```

---

## 10. Reference（参考文档）

| 文档 | 链接 |
|------|------|
| Redux 官方文档 | https://redux.js.org |
| Redux Toolkit | https://redux-toolkit.js.org |
| React Redux Hooks | https://react-redux.js.org/ |
| TypeScript Quick Start | https://redux.js.org/tutorials/typescript-quick-start |
| Redux DevTools | https://github.com/reduxjs/redux-devtools |

---

## 与其他 Skill 的关系

```yaml
depends_on:
  - frontend-common    # 前端公共调查能力
  - api-contract       # API 契约调查能力

provides_to:
  - architect-stage0    # 为 Architect Agent 提供框架知识
  - dev-stage4          # 为 Dev Agent 提供代码规范
```

---

## 更新记录

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| 1.0.0 | 2026-05-22 | 初始版本 |
| 1.1.0 | 2026-05-22 | 新增组件间/页面间状态传递调查、API数据处理流程、数据库模式调查 |