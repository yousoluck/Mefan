#!/bin/bash
# 代码模式提取脚本 (Code Pattern Extractor)
# 用于从现有代码库自动提取模式，生成一致性 Skill 文件
#
# 用法：
#   bash code-pattern-extractor.sh --all                    # 提取所有类型
#   bash code-pattern-extractor.sh --type naming           # 只提取命名规范
#   bash code-pattern-extractor.sh --type tech-frontend    # 前端框架模式
#   bash code-pattern-extractor.sh --type tech-backend     # 后端框架模式
#   bash code-pattern-extractor.sh --type domain           # 业务领域 skill（人机对话）
#
# 依赖：
#   - graphify (pip install graphify 后，graphify install --project)
#   - tree, grep, sed, awk, jq

# ============== 加载项目配置 ==============
# ROOT 优先使用环境变量，否则从 script 同级目录的 project.conf 加载
if [ -n "$ROOT" ]; then
    # 使用已有的 ROOT
    :
elif [ -f "$(dirname "${BASH_SOURCE[0]}")/../project.conf" ]; then
    source "$(dirname "${BASH_SOURCE[0]}")/../project.conf"
else
    # 回退到默认值
    export ROOT="${ROOT:-/mnt/d/pycharmprojects/Mefan}"
fi

# 导出其他路径变量（基于 ROOT）
export GRAPHIFY_OUT="${GRAPHIFY_OUT:-$ROOT/graphify-out}"
export SKILLS_DIR="${SKILLS_DIR:-$ROOT/.claude/skills}"
export TEMPLATE_DIR="${TEMPLATE_DIR:-$ROOT/.claude/templates}"

# 确保必要目录存在
mkdir -p "$GRAPHIFY_OUT"
mkdir -p "$SKILLS_DIR"
mkdir -p "$GRAPHIFY_OUT/frontend"
mkdir -p "$GRAPHIFY_OUT/backend"

set -e

# ============== 工具函数 ==============

log_info() {
    echo "[INFO] $(date '+%Y-%m-%d %H:%M:%S') - $*"
}

log_warn() {
    echo "[WARN] $(date '+%Y-%m-%d %H:%M:%S') - $*"
}

log_error() {
    echo "[ERROR] $(date '+%Y-%m-%d %H:%M:%S') - $*"
}

check_dependency() {
    if ! command -v "$1" &> /dev/null; then
        log_warn "'$1' 未安装，将使用备用方案"
        return 1
    fi
    return 0
}

# ============== Graphify 集成 ==============

install_graphify() {
    log_info "检查 graphify 安装状态..."
    if ! command -v graphify &> /dev/null; then
        log_info "graphify 未安装，正在安装..."
        pip install graphify 2>/dev/null || {
            log_warn "graphify 安装失败"
            return 1
        }
    fi

    # 初始化项目（如果需要）
    if [ ! -f "$ROOT/graphify-out/.graphify_initialized" ]; then
        log_info "初始化 graphify 项目..."
        cd "$ROOT"
        graphify install --project 2>/dev/null || {
            log_warn "graphify install --project 失败"
            return 1
        }
        touch "$ROOT/graphify-out/.graphify_initialized"
    fi
    return 0
}

run_graphify() {
    log_info "运行 graphify 构建代码图谱..."
    cd "$ROOT"
    if command -v graphify &> /dev/null; then
        graphify . 2>/dev/null || {
            log_warn "graphify . 失败，将使用备用分析"
            return 1
        }
        log_info "graphify 构建完成: $GRAPHIFY_OUT"
        return 0
    else
        log_warn "graphify 未安装，使用备用分析方案"
        return 1
    fi
}

query_graphify() {
    local query="$1"
    local output_file="$GRAPHIFY_OUT/query_$(echo "$query" | md5sum | cut -d' ' -f1).txt"

    if command -v graphify &> /dev/null; then
        log_info "Graphify 查询: $query"
        graphify query "$query" --format markdown 2>/dev/null > "$output_file" || {
            log_warn "graphify query 失败"
            echo "" > "$output_file"
        }
        cat "$output_file"
    else
        echo ""
    fi
}

get_graphify_stats() {
    local stats_file="$GRAPHIFY_OUT/stats.json"
    if [ -f "$stats_file" ]; then
        cat "$stats_file"
    else
        echo "{}"
    fi
}

# ============== 框架检测 ==============

detect_frontend_stack() {
    # 注意：本函数只输出检测结果，不做日志记录
    # 调用者负责日志记录

    local package_json="$ROOT/package.json"
    local result="{}"

    if [ -f "$package_json" ]; then
        # 检测主要框架
        local react_ver=$(grep -o '"react":"[^"]*"' "$package_json" | head -1 | cut -d'"' -f4)
        local redux=$(grep -o '"@reduxjs/toolkit":"[^"]*"' "$package_json" | head -1 | cut -d'"' -f4)
        local ant_design=$(grep -o '"antd":"[^"]*"' "$package_json" | head -1 | cut -d'"' -f4)
        local react_router=$(grep -o '"react-router-dom":"[^"]*"' "$package_json" | head -1 | cut -d'"' -f4)
        local axios=$(grep -o '"axios":"[^"]*"' "$package_json" | head -1 | cut -d'"' -f4)

        # 输出检测结果（供 eval 捕获）
        echo "FRONTEND_REACT=${react_ver:-未检测}"
        echo "FRONTEND_REDUX=${redux:-未检测}"
        echo "FRONTEND_ANTD=${ant_design:-未检测}"
        echo "FRONTEND_REACT_ROUTER=${react_router:-未检测}"
        echo "FRONTEND_AXIOS=${axios:-未检测}"

        # 返回检测到的框架列表
        [ -n "$react_ver" ] && echo "HAS_REACT=1" || echo "HAS_REACT=0"
        [ -n "$redux" ] && echo "HAS_REDUX=1" || echo "HAS_REDUX=0"
        [ -n "$ant_design" ] && echo "HAS_ANTD=1" || echo "HAS_ANTD=0"
        [ -n "$react_router" ] && echo "HAS_REACT_ROUTER=1" || echo "HAS_REACT_ROUTER=0"
        [ -n "$axios" ] && echo "HAS_AXIOS=1" || echo "HAS_AXIOS=0"
    else
        echo "FRONTEND_REACT=未检测"
        echo "FRONTEND_REDUX=未检测"
        echo "FRONTEND_ANTD=未检测"
        echo "FRONTEND_REACT_ROUTER=未检测"
        echo "FRONTEND_AXIOS=未检测"
        echo "HAS_REACT=0"
        echo "HAS_REDUX=0"
        echo "HAS_ANTD=0"
        echo "HAS_REACT_ROUTER=0"
        echo "HAS_AXIOS=0"
    fi
}

detect_backend_stack() {
    # 注意：本函数只输出检测结果，不做日志记录
    # 调用者负责日志记录

    local result="{}"

    # 检测 Node.js 后端
    if [ -f "$ROOT/package.json" ]; then
        local express=$(grep -o '"express":"[^"]*"' "$ROOT/package.json" | head -1 | cut -d'"' -f4)
        local fastify=$(grep -o '"fastify":"[^"]*"' "$ROOT/package.json" | head -1 | cut -d'"' -f4)
        local koa=$(grep -o '"koa":"[^"]*"' "$ROOT/package.json" | head -1 | cut -d'"' -f4)

        [ -n "$express" ] && echo "BACKEND_EXPRESS=$express" && echo "HAS_EXPRESS=1" || echo "HAS_EXPRESS=0"
        [ -n "$fastify" ] && echo "BACKEND_FASTIFY=$fastify" && echo "HAS_FASTIFY=1" || echo "HAS_FASTIFY=0"
        [ -n "$koa" ] && echo "BACKEND_KOA=$koa" && echo "HAS_KOA=1" || echo "HAS_KOA=0"
    fi

    # 检测 Python 后端
    if [ -f "$ROOT/requirements.txt" ]; then
        local fastapi=$(grep -o "fastapi[^,]*" "$ROOT/requirements.txt" | head -1)
        local django=$(grep -o "django[^,]*" "$ROOT/requirements.txt" | head -1)
        local flask=$(grep -o "flask[^,]*" "$ROOT/requirements.txt" | head -1)

        [ -n "$fastapi" ] && echo "BACKEND_FASTAPI=$fastapi" && echo "HAS_FASTAPI=1" || echo "HAS_FASTAPI=0"
        [ -n "$django" ] && echo "BACKEND_DJANGO=$django" && echo "HAS_DJANGO=1" || echo "HAS_DJANGO=0"
        [ -n "$flask" ] && echo "BACKEND_FLASK=$flask" && echo "HAS_FLASK=1" || echo "HAS_FLASK=0"
    fi

    # 检测 Java 后端
    if [ -f "$ROOT/pom.xml" ]; then
        local spring=$(grep -o "<spring-boot.version>[^<]*</spring-boot.version>" "$ROOT/pom.xml" | head -1 | cut -d'>' -f2 | cut -d'<' -f1)
        [ -n "$spring" ] && echo "BACKEND_SPRING=$spring" && echo "HAS_SPRING=1" || echo "HAS_SPRING=0"
    fi
}

# ============== 代码示例提取 ==============

find_example_file() {
    local pattern="$1"
    local lang="$2"
    find "$ROOT/src" -name "*.${lang}" -type f 2>/dev/null | xargs grep -l "$pattern" 2>/dev/null | head -1
}

extract_code_by_pattern() {
    local pattern="$1"
    local lang="$2"
    local max_lines="${3:-50}"

    local file=$(find_example_file "$pattern" "$lang")
    if [ -n "$file" ]; then
        grep -A "$max_lines" "$pattern" "$file" 2>/dev/null | head -"$max_lines"
    fi
}

# ============== Graphify 查询封装 ==============

query_symbols() {
    # 查询所有导出的函数/类
    query_graphify "Show me all exported functions and classes"
}

query_components() {
    # 查询 React 组件
    query_graphify "Show me all React components"
}

query_apis() {
    # 查询 API 路由
    query_graphify "Show me all API routes and endpoints"
}

query_slices() {
    # 查询 Redux slices
    query_graphify "Show me all Redux slices and actions"
}

# ============== 提取函数 ==============

# 1. 提取命名规范
extract_naming() {
    log_info "提取命名规范..."

    local output="$SKILLS_DIR/project-tech-naming.md"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    # 使用 graphify 查询实际代码中的命名模式
    local symbol_query=$(query_symbols)
    local var_patterns=""
    local func_patterns=""

    # 备用：直接分析代码
    if [ -d "$ROOT/src" ]; then
        var_patterns=$(grep -roh -E '\b[a-z][a-zA-Z0-9]*\s*=' "$ROOT/src" 2>/dev/null | grep -v '^[[:space:]]*//' | sort | uniq -c | sort -rn | head -20)
        func_patterns=$(grep -roh -E 'function\s+[a-zA-Z_][a-zA-Z0-9_]*' "$ROOT/src" 2>/dev/null | sort | uniq -c | sort -rn | head -20)
    fi

    cat > "$output" << EOF
# 命名规范 Skill（自动提取）
> 本文件由 code-pattern-extractor.sh 自动生成
> 生成时间：${timestamp}
> 来源：src/ 目录下的代码文件 + Graphify 分析

## 变量命名

| 类型 | 格式 | 示例 |
|------|------|------|
| 局部变量 | camelCase | \`userName\`, \`orderTotal\` |
| 全局变量 | g_camelCase | \`g_configValue\` |
| 常量 | UPPER_SNAKE_CASE | \`MAX_RETRY_COUNT\` |

## 函数命名

| 类型 | 格式 | 示例 |
|------|------|------|
| 公开方法 | camelCase | \`getUserById()\` |
| 私有方法 | _camelCase | \`_validateInput()\` |
| 异步方法 | async 前缀 | \`async fetchData()\` |
| 回调方法 | on/handle 前缀 | \`onClick()\`, \`handleSubmit()\` |

## 类命名

| 类型 | 后缀 | 示例 |
|------|------|------|
| 业务类 | Service | \`UserService\` |
| 数据类 | Entity/Model | \`OrderEntity\` |
| 控制类 | Controller | \`OrderController\` |
| 工具类 | Util/Helper | \`StringUtil\` |
| 组件 | Component/Page | \`UserCardComponent\` |

## 文件命名

| 类型 | 格式 | 示例 |
|------|------|------|
| 源文件 | kebab-case | \`user-service.ts\` |
| 测试文件 | *.test.ts | \`user-service.test.ts\` |
| 配置文件 | kebab-case | \`webpack.config.js\` |

## 实际代码中的命名模式分析

\`\`\`
高频变量模式:
${var_patterns:-（无数据）}
\`\`\`

\`\`\`
高频函数模式:
${func_patterns:-（无数据）}
\`\`\`

## Graphify 分析结果

\`\`\`
${symbol_query:-（Graphify 不可用）}
\`\`\`

## 来源

- 提取自：\`src/**/*.{ts,js,py,java}\` + Graphify 分析
- 分析时间：${timestamp}
EOF

    log_info "命名规范已生成: $output"
}

# 2. 提取前端框架模式（详细版）
extract_tech_frontend() {
    log_info "提取前端框架模式..."

    local output="$SKILLS_DIR/project-tech-frontend.md"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    # 加载框架检测结果
    eval "$(detect_frontend_stack)"

    # 使用 graphify 查询前端代码结构
    local component_query=$(query_components)
    local slice_query=$(query_slices)

    # 查找实际的代码示例
    local redux_slice_file ts_file
    ts_file=$(find_example_file "createSlice" "ts") && redux_slice_file="$ts_file" || redux_slice_file=""
    ts_file=$(find_example_file "React.FC" "tsx") && component_file="$ts_file" || component_file=""
    ts_file=$(find_example_file "axios" "ts") && api_file="$ts_file" || api_file=""

    # 从 graphify-out 读取分析结果
    local graphify_components="$GRAPHIFY_OUT/frontend/components.md"
    local graphify_slices="$GRAPHIFY_OUT/frontend/slices.md"

    cat > "$output" << EOF
# 前端框架使用规范 Skill（自动提取）
> 本文件由 code-pattern-extractor.sh 自动生成
> 生成时间：${timestamp}
> 来源：src/ 目录下的前端代码 + Graphify 分析

## 检测到的技术栈

| 框架/库 | 版本 | 用途 |
|---------|------|------|
| React | ${FRONTEND_REACT:-未检测} | UI 框架 |
| Redux Toolkit | ${FRONTEND_REDUX:-未检测} | 状态管理 |
| Ant Design | ${FRONTEND_ANTD:-未检测} | UI 组件库 |
| React Router | ${FRONTEND_REACT_ROUTER:-未检测} | 路由 |
| Axios | ${FRONTEND_AXIOS:-未检测} | HTTP 客户端 |

## 目录组织

前端代码组织原则：
\`\`\`
src/
├── api/              # API 调用层（axios 实例封装）
├── components/       # 通用组件
│   ├── common/       # 通用 UI 组件
│   └── business/     # 业务组件
├── pages/            # 页面组件
├── store/            # Redux store
│   ├── slices/       # RTK slice
│   └── index.ts     # store 配置
├── hooks/            # 自定义 hooks
├── utils/            # 工具函数
└── types/            # TypeScript 类型定义
\`\`\`

## Graphify 分析结果

### 组件结构
\`\`\`
${component_query:-（无数据）}
\`\`\`

### Redux Slice 结构
\`\`\`
${slice_query:-（无数据）}
\`\`\`

## 实际代码示例

### Redux Slice（来源：${redux_slice_file:-未找到}）

\`\`\`typescript
$(cat "$redux_slice_file" 2>/dev/null || echo "// 未找到 Redux Slice 示例")\`\`\`

### React 组件（来源：${component_file:-未找到}）

\`\`\`tsx
$(head -80 "$component_file" 2>/dev/null || echo "// 未找到 React 组件示例")\`\`\`

### API 层（来源：${api_file:-未找到}）

\`\`\`typescript
$(cat "$api_file" 2>/dev/null || echo "// 未找到 API 示例")\`\`\`

## Redux Toolkit 模式

### Slice 文件结构

\`\`\`typescript
// store/slices/{feature}Slice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

// 1. 定义 State 类型
interface {Feature}State {
  items: any[];
  loading: boolean;
  error: string | null;
}

// 2. 定义初始状态
const initialState: {Feature}State = {
  items: [],
  loading: false,
  error: null,
};

// 3. 创建 Slice
const {feature}Slice = createSlice({
  name: '{feature}',
  initialState,
  reducers: {
    // 同步 action
    setItems: (state, action: PayloadAction<any[]>) => {
      state.items = action.payload;
    },
    // 异步 action (thunk)
    fetchItems: createAsyncThunk(
      '{feature}/fetchItems',
      async (params: any, { rejectWithValue }) => {
        try {
          const response = await api.get('/{feature}', { params });
          return response.data;
        } catch (error) {
          return rejectWithValue(error.message);
        }
      }
    ),
  },
});

// 4. 导出 actions
export const { setItems } = {feature}Slice.actions;

// 5. 导出 reducer
export default {feature}Slice.reducer;
\`\`\`

### Store 配置

\`\`\`typescript
// store/index.ts
import { configureStore } from '@reduxjs/toolkit';
import {feature}Reducer from './slices/{feature}Slice';

export const store = configureStore({
  reducer: {
    {feature}: {feature}Reducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
\`\`\`

### 在组件中使用

\`\`\`typescript
// hooks/use{Feature}.ts
import { useDispatch, useSelector } from 'react-redux';
import type { TypedUseSelectorHook } from 'react-redux';
import type { RootState, AppDispatch } from '../store';

export const useAppDispatch: () => AppDispatch = useDispatch;
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;

// 使用方式
const items = useAppSelector(state => state.{feature}.items);
const fetchItems = () => dispatch(fetchItemsAsync(params));
\`\`\`

## API 层模式

### Axios 实例封装

\`\`\`typescript
// api/client.ts
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL || '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = \`Bearer \${token}\`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// 响应拦截器
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
\`\`\`

### API 模块定义

\`\`\`typescript
// api/{feature}.ts
import api from './client';

export const {feature}Api = {
  list: (params: any) => api.get('/{feature}', { params }),
  get: (id: string) => api.get(\`/{feature}/\${id}\`),
  create: (data: any) => api.post('/{feature}', data),
  update: (id: string, data: any) => api.put(\`/{feature}/\${id}\`, data),
  delete: (id: string) => api.delete(\`/{feature}/\${id}\`),
};
\`\`\`

## Ant Design 组件使用模式

### 基础组件引入

\`\`\`typescript
import { Button, Table, Form, Input, Select, Modal, message } from 'antd';
import { useForm } from 'antd/lib/form/Form';
\`\`\`

### Table 组件模式

\`\`\`typescript
const columns = [
  { title: '名称', dataIndex: 'name', key: 'name' },
  { title: '状态', dataIndex: 'status', key: 'status',
    render: (status: string) => (
      <Tag color={status === 'active' ? 'green' : 'red'}>{status}</Tag>
    )
  },
  { title: '操作', key: 'action',
    render: (_: any, record: any) => (
      <Space>
        <Button size="small" onClick={() => handleEdit(record)}>编辑</Button>
        <Button size="small" danger onClick={() => handleDelete(record.id)}>删除</Button>
      </Space>
    )
  },
];

<Table columns={columns} dataSource={data} rowKey="id" loading={loading} />
\`\`\`

### Form 组件模式

\`\`\`typescript
const [form] = useForm();

const onFinish = async (values: any) => {
  try {
    await {feature}Api.create(values);
    message.success('创建成功');
    onClose();
  } catch (error) {
    message.error('创建失败');
  }
};

<Form form={form} onFinish={onFinish} layout="vertical">
  <Form.Item name="name" label="名称" rules={[{ required: true }]}>
    <Input />
  </Form.Item>
  <Form.Item name="status" label="状态">
    <Select>
      <Select.Option value="active">启用</Select.Option>
      <Select.Option value="inactive">禁用</Select.Option>
    </Select>
  </Form.Item>
</Form>
\`\`\`

### Modal 组件模式

\`\`\`typescript
const [visible, setVisible] = useState(false);
const [confirmLoading, setConfirmLoading] = useState(false);

const showModal = () => setVisible(true);

const handleOk = async () => {
  setConfirmLoading(true);
  try {
    await form.submit();
    setVisible(false);
  } finally {
    setConfirmLoading(false);
  }
};

<Modal title="标题" open={visible} onOk={handleOk} confirmLoading={confirmLoading} onCancel={() => setVisible(false)}>
  {/* 表单内容 */}
</Modal>
\`\`\`

## React Router v6 路由模式

### 路由配置

\`\`\`typescript
// routes/index.tsx
import { Routes, Route, Navigate } from 'react-router-dom';
import { lazy, Suspense } from 'react';

const Home = lazy(() => import('../pages/Home'));
const UserList = lazy(() => import('../pages/UserList'));

const routes = [
  { path: '/', element: <Home /> },
  { path: '/users', element: <UserList /> },
  { path: '/users/:id', element: <UserDetail /> },
];

export default function AppRoutes() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Routes>
        {routes.map(route => (
          <Route key={route.path} path={route.path} element={route.element} />
        ))}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Suspense>
  );
}
\`\`\`

### 在组件中使用导航

\`\`\`typescript
import { useNavigate, useParams } from 'react-router-dom';

const navigate = useNavigate();
const { id } = useParams();

navigate('/users');
navigate(\`/users/\${id}\`);
navigate('/users', { state: { from: 'list' } });
\`\`\`

## 组件组合模式

### 容器组件 + 展示组件

\`\`\`typescript
// 容器组件 (Container)
const UserListContainer: React.FC = () => {
  const dispatch = useAppDispatch();
  const { items, loading } = useAppSelector(state => state.users);

  useEffect(() => {
    dispatch(fetchUsers());
  }, [dispatch]);

  return <UserListPresentation items={items} loading={loading} />;
};

// 展示组件 (Presentation)
interface UserListProps {
  items: User[];
  loading: boolean;
}

const UserListPresentation: React.FC<UserListProps> = ({ items, loading }) => {
  if (loading) return <Spin />;
  return <Table dataSource={items} columns={columns} />;
};
\`\`\`

### 自定义 Hook 封装

\`\`\`typescript
// hooks/use{Feature}.ts
export function use{Feature}(id: string) {
  const dispatch = useAppDispatch();
  const { feature, loading, error } = useAppSelector(state => state.{feature});

  useEffect(() => {
    dispatch(fetch{Feature}ById(id));
  }, [id, dispatch]);

  return { feature, loading, error };
}
\`\`\`

## 来源

- 提取自：\`src/**/*.{ts,tsx}\` + Graphify 分析
- Graphify 输出：${GRAPHIFY_OUT}
- 检测时间：${timestamp}
EOF

    log_info "前端框架模式已生成: $output"
}

# 3. 提取后端框架模式（详细版）
extract_tech_backend() {
    log_info "提取后端框架模式..."

    local output="$SKILLS_DIR/project-tech-backend.md"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    # 加载框架检测结果
    eval "$(detect_backend_stack)"

    # 使用 graphify 查询后端代码结构
    local api_query=$(query_apis)

    # 查找实际的代码示例
    local express_file
    express_file=$(find_example_file "express()" "js") || express_file=""
    express_file=$(find_example_file "app.get" "js") || express_file="$express_file"

    cat > "$output" << EOF
# 后端框架使用规范 Skill（自动提取）
> 本文件由 code-pattern-extractor.sh 自动生成
> 生成时间：${timestamp}
> 来源：src/ 目录下的后端代码 + Graphify 分析

## 检测到的技术栈

| 框架 | 版本 | 状态 |
|------|------|------|
EOF

    # 追加检测结果
    [ "$HAS_EXPRESS" = "1" ] && echo "| Express | ${BACKEND_EXPRESS} | ✅ 检测到 |" >> "$output"
    [ "$HAS_FASTIFY" = "1" ] && echo "| Fastify | ${BACKEND_FASTIFY} | ✅ 检测到 |" >> "$output"
    [ "$HAS_KOA" = "1" ] && echo "| Koa | ${BACKEND_KOA} | ✅ 检测到 |" >> "$output"
    [ "$HAS_FASTAPI" = "1" ] && echo "| FastAPI | ${BACKEND_FASTAPI} | ✅ 检测到 |" >> "$output"
    [ "$HAS_DJANGO" = "1" ] && echo "| Django | ${BACKEND_DJANGO} | ✅ 检测到 |" >> "$output"
    [ "$HAS_FLASK" = "1" ] && echo "| Flask | ${BACKEND_FLASK} | ✅ 检测到 |" >> "$output"
    [ "$HAS_SPRING" = "1" ] && echo "| Spring Boot | ${BACKEND_SPRING} | ✅ 检测到 |" >> "$output"

    # 继续添加通用内容
    cat >> "$output" << 'EOF'

## 目录组织

\`\`\`
src/
├── controllers/     # 控制器层
├── services/        # 业务逻辑层
├── repositories/     # 数据访问层
├── models/          # 数据模型
├── middleware/      # 中间件
├── routes/          # 路由定义
├── utils/           # 工具函数
└── config/          # 配置
\`\`\`

## Graphify API 分析结果

\`\`\`
${api_query:-（无数据）}
\`\`\`

## 实际代码示例

### Express 服务器入口（来源：${express_file:-未找到}）

\`\`\`javascript
$(cat "$express_file" 2>/dev/null | head -60 || echo "// 未找到 Express 示例")\`\`\`

## Express 模式

### 服务器入口

\`\`\`javascript
// src/index.js
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const bodyParser = require('body-parser');
const { errorHandler } = require('./middleware/errorHandler');

const app = express();

// 1. 安全中间件
app.use(helmet());
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || '*',
  credentials: true
}));

// 2. 解析中间件
app.use(bodyParser.json({ limit: '10mb' }));
app.use(bodyParser.urlencoded({ extended: true }));

// 3. 路由
app.use('/api', require('./routes'));

// 4. 错误处理
app.use(errorHandler);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(\`Server running on port \${PORT}\`);
});
\`\`\`

### 路由定义

\`\`\`javascript
// src/routes/{resource}.js
const express = require('express');
const router = express.Router();
const {resource}Controller = require('../controllers/{resource}Controller');
const { validateResource } = require('../middleware/validation');

router.get('/', {resource}Controller.list);
router.get('/:id', {resource}Controller.get);
router.post('/', validateResource, {resource}Controller.create);
router.put('/:id', validateResource, {resource}Controller.update);
router.delete('/:id', {resource}Controller.delete);

module.exports = router;
\`\`\`

### 控制器模式

\`\`\`javascript
// src/controllers/{resource}Controller.js
const {resource}Service = require('../services/{resource}Service');

const asyncHandler = (fn) => (req, res, next) =>
  Promise.resolve(fn(req, res, next)).catch(next);

const list = asyncHandler(async (req, res) => {
  const { page = 1, limit = 10 } = req.query;
  const result = await {resource}Service.list({ page: parseInt(page), limit: parseInt(limit) });
  res.json({ code: 0, data: result.items, pagination: result.pagination });
});

const get = asyncHandler(async (req, res) => {
  const { id } = req.params;
  const item = await {resource}Service.get(id);
  if (!item) {
    return res.status(404).json({ code: 404, message: 'Not found' });
  }
  res.json({ code: 0, data: item });
});

module.exports = { list, get, create, update, delete };
\`\`\`

### 服务层模式

\`\`\`javascript
// src/services/{resource}Service.js
const {resource}Repository = require('../repositories/{resource}Repository');

class {Resource}Service {
  async list(params) {
    return await {resource}Repository.findAll(params);
  }

  async get(id) {
    const item = await {resource}Repository.findById(id);
    if (!item) {
      throw new Error('Not found');
    }
    return item;
  }

  async create(data) {
    if (!data.name) {
      throw new Error('Name is required');
    }
    return await {resource}Repository.create(data);
  }
}

module.exports = new {Resource}Service();
\`\`\`

## 错误处理模式

### 统一错误响应

\`\`\`javascript
// src/middleware/errorHandler.js
class AppError extends Error {
  constructor(statusCode, code, message) {
    super(message);
    this.statusCode = statusCode;
    this.code = code;
  }
}

const errorHandler = (err, req, res, next) => {
  console.error(err.stack);

  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      code: err.code,
      message: err.message,
      data: null
    });
  }

  res.status(500).json({
    code: 'INTERNAL_ERROR',
    message: process.env.NODE_ENV === 'production' ? 'Internal server error' : err.message,
    data: null
  });
};

module.exports = { errorHandler, AppError };
\`\`\`

## 中间件注册顺序

1. **安全中间件**：helmet, cors
2. **解析中间件**：bodyParser, cookieParser
3. **日志中间件**：morgan
4. **路由中间件**：/api 路由
5. **错误处理**：errorHandler

## RESTful API 设计规范

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/{resource} | 获取资源列表 |
| GET | /api/{resource}/:id | 获取单个资源 |
| POST | /api/{resource} | 创建资源 |
| PUT | /api/{resource}/:id | 更新资源 |
| DELETE | /api/{resource}/:id | 删除资源 |

## 来源

- 提取自：\`src/**/*.{js,ts,py,java}\` + Graphify 分析
- 检测时间：${timestamp}
EOF

    log_info "后端框架模式已生成: $output"
}

# 4. 提取中间件模式
extract_middleware() {
    log_info "提取中间件模式..."

    local output="$SKILLS_DIR/project-middleware.md"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    # 查找实际的中间件代码
    local cors_file js_file ts_file
    js_file=$(find_example_file "cors(" "js") || js_file=""
    ts_file=$(find_example_file "cors(" "ts") || ts_file=""
    cors_file="${js_file:-$ts_file}"
    js_file=$(find_example_file "helmet(" "js") || js_file=""
    ts_file=$(find_example_file "helmet(" "ts") || ts_file=""
    helmet_file="${js_file:-$ts_file}"

    cat > "$output" << EOF
# 中间件使用规范 Skill（自动提取）
> 本文件由 code-pattern-extractor.sh 自动生成
> 生成时间：${timestamp}
> 来源：src/ 目录下的中间件代码

## 中间件注册顺序

\`\`\`javascript
const app = express();

// 1. 安全中间件
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || '*',
  credentials: true
}));
app.use(helmet({
  contentSecurityPolicy: false
}));

// 2. 解析中间件
app.use(bodyParser.json({ limit: '10mb' }));
app.use(bodyParser.urlencoded({ extended: true }));

// 3. 路由中间件
app.use('/api', router);

// 4. 错误处理
app.use(errorHandler);
\`\`\`

## 常用中间件配置

| 中间件 | 常用配置 | 用途 |
|--------|----------|------|
| cors | origin, credentials | 跨域控制 |
| helmet | contentSecurityPolicy | 安全头 |
| bodyParser | limit, type | 请求体解析 |
| morgan | format | HTTP 日志 |
| cookieParser | secret | Cookie 解析 |

## 实际代码示例

### CORS 配置（来源：${cors_file:-未找到}）

\`\`\`javascript
$(cat "$cors_file" 2>/dev/null | head -40 || echo "// 未找到 CORS 配置示例")\`\`\`

### Security 头配置（来源：${helmet_file:-未找到}）

\`\`\`javascript
$(cat "$helmet_file" 2>/dev/null | head -40 || echo "// 未找到 helmet 配置示例")\`\`\`

## 自定义中间件模式

### 认证中间件

\`\`\`javascript
// middleware/auth.js
const jwt = require('jsonwebtoken');

const authMiddleware = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];

  if (!token) {
    return res.status(401).json({ message: 'No token provided' });
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    return res.status(401).json({ message: 'Invalid token' });
  }
};

module.exports = authMiddleware;
\`\`\`

### 日志中间件

\`\`\`javascript
// middleware/logger.js
const logger = (req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = Date.now() - start;
    console.log(\`\${req.method} \${req.path} \${res.statusCode} \${duration}ms\`);
  });
  next();
};

module.exports = logger;
\`\`\`

## 错误处理模式

\`\`\`javascript
// 同步错误处理
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(err.status || 500).json({
    code: err.code || 'INTERNAL_ERROR',
    message: err.message
  });
});

// 异步错误处理包装
const asyncHandler = (fn) => (req, res, next) =>
  Promise.resolve(fn(req, res, next)).catch(next);
\`\`\`

## 来源

- 提取自：\`src/**/middleware*.{js,ts}\`
- 分析文件：${cors_file:-$helmet_file}
- 检测时间：${timestamp}
EOF

    log_info "中间件模式已生成: $output"
}

# 5. 提取架构模式
extract_architecture() {
    log_info "提取架构模式..."

    local output="$SKILLS_DIR/architecture-pattern.md"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    # 使用 graphify 查询调用链
    local callchain_query=$(query_graphify "Show me the call chain from controller to database")

    cat > "$output" << EOF
# 项目架构模式 Skill（自动提取）
> 本文件由 code-pattern-extractor.sh 自动生成
> 生成时间：${timestamp}
> 来源：调用链分析 + Graphify

## 分层结构

\`\`\`
┌─────────────────────────────────┐
│       Presentation Layer        │
│  (Controllers, Components, UI)   │
└─────────────┬───────────────────┘
              │
┌─────────────▼───────────────────┐
│        Service Layer            │
│   (Business Logic, Services)    │
└─────────────┬───────────────────┘
              │
┌─────────────▼───────────────────┐
│       Data Access Layer         │
│  (Repositories, DAOs, ORM)     │
└─────────────────────────────────┘
\`\`\`

## 调用链分析

\`\`\`
${callchain_query:-（Graphify 不可用，使用默认结构）}
\`\`\`

### 默认调用链示例

\`\`\`
UserController
  └── UserService
        ├── UserRepository
        │     └── Database
        └── NotificationService
              └── EmailService
                    └── SMTP
\`\`\`

## 依赖规则

| 规则 | 说明 |
|------|------|
| 上层 → 下层 | Controller 调用 Service |
| 下层 → 上层 | 禁止 Service 调用 Controller |
| 同层调用 | 需通过接口/抽象 |
| 共享层 | 可被所有层调用 |

## 来源

- 提取自：调用链分析 (Graphify)
- Graphify 输出：${GRAPHIFY_OUT}
- 检测时间：${timestamp}
EOF

    log_info "架构模式已生成: $output"
}

# 6. 提取目录结构
extract_directory() {
    log_info "提取目录结构..."

    local output="$SKILLS_DIR/directory-structure.md"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    local dir_tree=""
    if command -v tree &> /dev/null; then
        dir_tree=$(tree -L 3 -I 'node_modules|.git|dist|build' "$ROOT/src" 2>/dev/null || echo "（tree 不可用）")
    else
        dir_tree="\`\`\`\n$ROOT/src\n"
        find "$ROOT/src" -maxdepth 3 -type d 2>/dev/null | while read -r dir; do
            local depth=$(echo "$dir" | tr -cd '/' | wc -c)
            local prefix=$(printf '%*s' "$((depth - ${#ROOT}))" '' | tr ' ' '  ')
            echo "${prefix}$(basename "$dir")/" >> "$output.tmp"
        done
        dir_tree=$(cat "$output.tmp" 2>/dev/null || echo "（请安装 tree 工具）")
        rm -f "$output.tmp"
    fi

    cat > "$output" << EOF
# 项目目录结构 Skill（自动提取）
> 本文件由 code-pattern-extractor.sh 自动生成
> 生成时间：${timestamp}
> 来源：目录扫描

## 目录结构

\`\`\`
$dir_tree
\`\`\`

## 目录规则

| 规则 | 说明 |
|------|------|
| 每层目录 ≤ 10 个子目录 | 超过则拆分子域 |
| 测试文件就近放置 | \`*.test.ts\` 与源文件同目录 |
| 配置与代码分离 | \`config/\` 目录存放配置 |
| 共享代码集中管理 | \`shared/\` 或 \`common/\` 目录 |

## 文件组织原则

1. **高内聚**：相关功能放同一目录
2. **低耦合**：目录间依赖最小化
3. **可发现**：按功能/领域组织，非按类型
4. **可测试**：测试文件靠近源文件

## 来源

- 提取自：目录扫描
- 分析深度：3 层
- 检测时间：${timestamp}
EOF

    log_info "目录结构已生成: $output"
}

# 7. 生成业务领域 Skill（人机对话模式）
extract_domain_skill() {
    log_info "生成业务领域 Skill..."

    local output="$SKILLS_DIR/project-domain.md"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    # 读取项目描述
    local project_desc=""
    if [ -f "$ROOT/.claude/context/project.md" ]; then
        project_desc=$(grep -A5 "## 项目描述" "$ROOT/.claude/context/project.md" 2>/dev/null | head -20 || echo "")
    fi

    # 读取 feature.md 了解业务领域
    local feature_content=""
    if [ -f "$ROOT/.claude/iterations/sprint-latest/feature.md" ]; then
        feature_content=$(cat "$ROOT/.claude/iterations/sprint-latest/feature.md" 2>/dev/null || echo "")
    fi

    cat > "$output" << EOF
# 业务领域 Skill（人工引导生成）
> 本文件由 code-pattern-extractor.sh 自动生成
> 生成时间：${timestamp}
> 状态：需要人工补充

## 引导问卷

请回答以下问题以生成准确的业务领域 Skill：

### 1. 业务领域概述

**Q1: 项目的主要业务领域是什么？**
（例：电商平台、企业管理系统、社交网络、数据分析平台）

**Q2: 核心用户群体有哪些？**
（例：B端企业用户、C端消费者、内部员工、合作伙伴）

### 2. 领域实体

**Q3: 系统中有哪些核心实体（Entity）？**
（例：用户、订单、产品、库存、支付）

**Q4: 实体之间的关系是什么？**
（例：用户-订单 一对多，产品-库存 一对多）

### 3. 业务流程

**Q5: 核心业务流程是什么？**
请描述主要业务场景：
1.
2.
3.

**Q6: 有哪些关键的业务规则？**
（例：订单超过30分钟未支付自动取消，库存低于10触发补货提醒）

### 4. 领域术语

**Q7: 业务中常用的专业术语及定义？**

| 术语 | 定义 |
|------|------|
|  |  |
|  |  |

### 5. 系统边界

**Q8: 系统与外部系统的交互有哪些？**

| 外部系统 | 交互内容 | 集成方式 |
|----------|----------|----------|
|  |  |  |
|  |  |  |

## 项目上下文（供参考）

\`\`\`
${project_desc:-（无项目描述，请参考 feature.md）}
\`\`\`

## Feature 概要（供参考）

\`\`\`
${feature_content:0:2000}
...
\`\`\`

## 生成指南

请根据上述问卷的回答，补充以下内容到本文件：

### 领域模型

\`\`\`
## 领域模型

### 实体定义
- User: （描述）
- Order: （描述）
- Product: （描述）

### 聚合根
- OrderAggregate: （包含哪些实体，边界是什么）

### 值对象
- Money: （金额表示）
- Address: （地址）
\`\`\`

### 领域服务

\`\`\`
## 领域服务

### 订单服务 (OrderService)
- createOrder(): 创建订单
- cancelOrder(): 取消订单
- payOrder(): 支付订单

### 库存服务 (InventoryService)
- reserveStock(): 预留库存
- releaseStock(): 释放库存
- deductStock(): 扣减库存
\`\`\`

### 领域事件

\`\`\`
## 领域事件

- OrderCreated: 订单创建
- OrderPaid: 订单支付
- StockReserved: 库存预留
\`\`\`

## 来源

- 检测时间：${timestamp}
EOF

    log_info "业务领域 Skill 已生成（需人工补充）: $output"
}

# ============== 主流程 ==============

show_usage() {
    echo "用法: bash code-pattern-extractor.sh [选项]"
    echo ""
    echo "选项:"
    echo "  --all              提取所有类型的 Skill（默认）"
    echo "  --type <类型>       只提取指定类型"
    echo ""
    echo "支持的类型:"
    echo "  naming            命名规范"
    echo "  tech-frontend     前端框架模式（详细）"
    echo "  tech-backend      后端框架模式（详细）"
    echo "  middleware        中间件模式"
    echo "  architecture      架构模式"
    echo "  directory         目录结构"
    echo "  domain            业务领域 Skill（人机对话）"
    echo ""
    echo "示例:"
    echo "  bash code-pattern-extractor.sh --all"
    echo "  bash code-pattern-extractor.sh --type tech-frontend"
    echo "  bash code-pattern-extractor.sh --type domain"
}

main() {
    local type="${1:-all}"

    log_info "开始代码模式提取..."
    log_info "项目根目录: $ROOT"
    log_info "输出目录: $SKILLS_DIR"

    # 注意：graphify 安装和初始化已在阶段 0 PM-Stage0 完成
    # 此处只进行查询和生成，如 graphify 不可用则使用备用分析

    case "$type" in
        --all)
            extract_naming
            extract_tech_frontend
            extract_tech_backend
            extract_middleware
            extract_architecture
            extract_directory
            extract_domain_skill
            log_info "全部 Skill 提取完成！"
            ;;
        --type)
            local subtype="$2"
            case "$subtype" in
                naming)          extract_naming ;;
                tech-frontend)   extract_tech_frontend ;;
                tech-backend)    extract_tech_backend ;;
                middleware)      extract_middleware ;;
                architecture)    extract_architecture ;;
                directory)       extract_directory ;;
                domain)          extract_domain_skill ;;
                *)               log_error "未知类型: $subtype"; show_usage; exit 1 ;;
            esac
            ;;
        --help|-h)
            show_usage
            ;;
        *)
            log_error "未知参数: $type"
            show_usage
            exit 1
            ;;
    esac

    log_info "生成的文件:"
    ls -la "$SKILLS_DIR"/project-*.md "$SKILLS_DIR"/architecture-*.md "$SKILLS_DIR"/directory-*.md 2>/dev/null || true
}

main "$@"