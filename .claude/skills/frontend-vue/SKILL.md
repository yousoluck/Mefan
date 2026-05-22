# Skill 元数据

```yaml
name: frontend-vue
name_zh: 前端 Vue 框架调查
category: frontend
framework: vue
version: 1.0.0
author: Architect Agent
created: 2026-05-22
trigger: auto-detect
trigger_files:
  - package.json (contains "vue")
  - src/store/index.ts (Vuex)
  - src/pinia/
```

---

## 1. 框架概述

| 项目 | 内容 |
|------|------|
| **框架版本** | Vue 3.x |
| **核心作用** | 渐进式前端框架，响应式状态管理 |
| **状态管理** | Pinia / Vuex |
| **路由** | Vue Router |

---

## 2. 目录结构规范

```
src/
├── stores/                # Pinia Store
│   └── {feature}/
│       ├── index.ts      # Store 定义
│       └── actions.ts    # Action
├── composables/          # Composition API
│   └── use{Feature}.ts   # 可复用逻辑
├── views/                # 页面组件
├── components/           # 通用组件
├── router/
│   └── index.ts          # 路由配置
└── assets/
```

---

## 3. 核心元素调查清单

### 3.1 状态管理（Pinia/Vuex）

| 调查项 | 文件位置 | 说明 |
|--------|---------|------|
| Store 定义方式 | `src/stores/` | defineStore 用法 |
| State 结构 | `src/stores/` | 响应式 state |
| Getters | `src/stores/` | computed 属性 |
| Actions | `src/stores/` | 同步/异步操作 |

### 3.2 组件模式

| 调查项 | 说明 |
|--------|------|
| Composition API vs Options API | 风格选择 |
| props/emits 定义 | 类型定义方式 |
| provide/inject | 跨层级通信 |

### 3.3 路由

| 调查项 | 说明 |
|--------|------|
| 路由守卫 | beforeEach/afterEach |
| 懒加载 | () => import() |
| 动态路由 | 路由参数处理 |

---

## 4. 代码样例索引

| 模式 | 文件 | 行号 | 说明 |
|------|------|------|------|
| Store 创建 | `src/stores/user.ts` | 1-20 | Pinia store 模板 |
| Composables | `src/composables/useAuth.ts` | 1-15 | 组合式函数 |
| 路由守卫 | `src/router/index.ts` | 1-30 | 权限验证 |

---

## 5. 命名约定调查

| 调查项 | 关键问题 | 证据文件:行号 |
|--------|---------|--------------|
| **组件文件命名** | PascalCase 还是 kebab-case？如 `UserCard.vue` vs `user-card.vue` | |
| **组件名命名** | 多个单词？如 `TodoItem` vs `todo-item` | |
| **Composables 命名** | `use` 前缀？如 `useAuth` vs `AuthComposable` | |
| **Pinia Store 命名** | `use` 前缀 + 文件名？如 `useUserStore` in `user.ts` | |
| **Props 定义命名** | 驼峰还是短横线？TS 类型定义方式？ | |
| **常量命名** | 全大写下划线还是 PascalCase？ | |
| **API 方法命名** | get/fetch/load？如 `fetchUser` vs `getUser` | |
| **事件名命名** | kebab-case？如 `item-click` vs `itemClick` | |
| **目录命名** | 复数还是单数？如 `components/` vs `component/` | |

---

## 6. 禁止做法（反模式）

| 禁止 | 原因 | 正确做法 | 证据 |
|------|------|---------|------|
| **在 template 中使用箭头函数** | 每次渲染创建新函数，违反响应式原则 | 在 methods 中定义或使用 computed | |
| **直接修改 props** | 违反单向数据流原则 | 使用 emit 通知父组件 | |
| **在 computed 中修改 state** | 产生副作用，违反 computed 纯粹性 | 使用 watch 或 methods | |
| **v-if 和 v-show 混用** | 两者语义不同，混用导致困惑 | 显示/隐藏用 v-show，条件渲染用 v-if | |
| **在组件内直接调用 API** | 违反分层原则 | 使用 composables 或 services 层 | |
| **不使用 key 的 v-for** | 导致状态错乱和渲染问题 | 必须提供唯一 key | |
| **Provide/inject 滥用** | 导致隐式依赖，难以追踪 | 优先使用 props/emits | |

---

## 7. 常见问题调查

| 调查项 | 关键问题 | 证据文件:行号 |
|--------|---------|--------------|
| **Pinia Store 持久化** | 使用 pinia-plugin-persistedstate？如何配置？ | |
| **跨组件状态共享** | EventBus vs Provide/Inject vs Pinia Store | |
| **异步状态管理** | 加载中/错误/成功状态如何追踪？ | |
| **组件复用模式** | Mixins vs Composables vs Slots | |
| **TypeScript 集成** | 是否使用 `<script setup lang="ts">`？ | |
| **样式作用域** | 使用 scoped CSS 还是 CSS Modules？ | |
| **依赖注入** | 如何处理深层 props 传递？ | |
| **性能优化** | 如何避免不必要的重渲染？ | |

---

## 8. 依赖版本调查

| 调查项 | 关键问题 | 证据文件 |
|--------|---------|---------|
| **Vue 版本** | Vue 2 还是 Vue 3？具体小版本？ | package.json |
| **Pinia vs Vuex** | 项目使用哪个状态管理库？为什么？ | package.json |
| **Vue Router 版本** | 路由懒加载如何配置？ | package.json |
| **Vite vs Webpack** | 构建工具是什么？ | package.json |
| **TypeScript 版本** | 是否使用 TS？版本多少？ | package.json |
| **UI 组件库** | Element Plus / Ant Design Vue / Naive UI？ | package.json |
| **HTTP 客户端** | Axios vs Fetch vs ky？ | package.json |
| **测试框架** | Vitest vs Jest？ | package.json |

---

## Scripts

| 脚本名 | 说明 |
|--------|------|
| detect-vue.sh | 检测 Vue 框架 |
| extract-vue-patterns.sh | 提取 Vue 代码模式 |

---

## Reference

- [Vue 3 文档](https://vuejs.org/)
- [Pinia 文档](https://pinia.vuejs.org/)
- [Vue Router](https://router.vuejs.org/)