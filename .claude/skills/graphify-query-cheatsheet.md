# Graphify 查询速查表
- 触发条件：阶段 0、2、4 需要分析代码结构或依赖关系时
- 适用 Agent：架构师、开发者、PM

> **重要**（2026-06-08）：
> 1. **真实命令**：`query` / `path` / `explain` / `extract` / `cluster-only` / `update` / `clone` / `add`
> 2. **不存在的命令**（已废弃）：`similar` / `dependents` / `scan` / `update`（作为子命令）
> 3. **真实文件位置**：`graphify-out/graph.json`（已重构，原 `.claude/context/knowledge.grap` 废弃）
> 4. **典型错误**：用 grep 搜 `knowledge.grap` 中的 `called_by` / `depends_on` 模式 → **JSON 文件无此文本模式**，必须用 `graphify query` / `graphify path`

## 输入
- 查询类型（query/path/explain）
- 目标模块名或问题描述

## 输出
- Graphify 分析结果（文本/结构化数据）
- 用于生成 consistency-baseline.md、分析模块依赖

## 查询命令

### 1. 通用查询（BFS 遍历）
```bash
graphify query "<自然语言描述>"
```
**用途**：用自然语言查询代码库中的模式
**示例**：
- `graphify query "What are the main modules and components"`
- `graphify query "What framework is used for API"`
- `graphify query "What database configuration exists"`

### 2. 最短路径查询
```bash
graphify path "NODE_A" "NODE_B"
```
**用途**：查找两个节点之间的最短路径
**场景**：分析模块间依赖关系、追踪调用链

### 3. 节点解释
```bash
graphify explain "NODE_NAME"
```
**用途**：获取节点的详细信息和所有连接
**示例**：
- `graphify explain "AuthService"`
- `graphify explain "Database"`

### 4. 图谱更新
```bash
# 首次扫描
graphify extract .

# 增量更新
graphify . --update
```
**注意**：这些命令需要在 Claude Code 中作为 slash command 执行

## 在 Agent 中调用 Graphify

```bash
# 在 Agent 的 bash 块中调用
cd "$ROOT"

# 通用查询
RESULT=$(graphify query "What is the tech stack" 2>/dev/null | head -30 || echo "[Graphify不可用]")

# 最短路径
PATH_RESULT=$(graphify path "AuthModule" "Database" 2>/dev/null || echo "[Graphify不可用]")

# 节点解释
EXPLAIN_RESULT=$(graphify explain "UserService" 2>/dev/null | head -30 || echo "[Graphify不可用]")
```

## 异常处理
- 若 graphify 不可用：标注"[Graphify不可用]"，跳过此步，用手动分析替代
- 若查询失败：标注"[查询失败]"，继续执行

## 替换旧命令

> 以下旧命令已废弃，请使用新命令替代：

| 旧命令 | 新命令 |
|--------|--------|
| `graphify dependents <module>` | `graphify path <module> <target>` 或 `graphify query "what depends on <module>"` |
| `graphify similar <file>` | `graphify query "similar to <file>"` 或 `graphify path <file> <target>` |
| `graphify update` | `/graphify . --update`（Claude Code slash command）|