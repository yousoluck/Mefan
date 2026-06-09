# Graphify Query DSL 速查表

> **用途**：Architect-Stage0 阶段 A 设计 query 时参考，避免 AI 瞎猜 graphify 能力
> **来源**：基于 `.claude/skills/graphify/SKILL.md` 提取
> **维护者**：随 graphify 升级同步更新

---

## 1. 可用命令（graphify CLI 实际能力）

| 命令 | 用途 | 关键参数 | 适用场景 |
|------|------|---------|---------|
| `graphify query "<question>"` | BFS 遍历，广度上下文（默认） | 无 flag | 「X 连接了什么？」类问题 |
| `graphify query "<question>" --dfs` | DFS 遍历，追踪特定调用链 | `--dfs` | 「X 怎么到 Y？」类问题 |
| `graphify query "<question>" --budget N` | 限制返回 token 数 | `--budget 1500` | 控制输出大小 |
| `graphify path "NODE_A" "NODE_B"` | 两概念间最短路径 | 无 | 跨模块依赖追踪 |
| `graphify explain "NODE_NAME"` | 单节点平实语言解释 | 无 | 理解某个具体概念 |

> ⚠️ `graphify query` 必须**先**走 Step 0 词表扩展，**再**用扩展后的 query 串执行。详见 §2。

---

## 2. 强制工作流（设计 query 前必读）

### Step 0 — 约束性 Query 扩展（REQUIRED）

graphify 的 `query` 子命令采用大小写折叠子串 + IDF 匹配——**没有词干提取、同义词、跨语言匹配**。如果用户/AI 的问题用的是不同语言或不同领域词汇，匹配会返回 0 条结果，答案退化为噪声。

**强制流程**：

```bash
# 2.1 提取图谱词表
$(cat graphify-out/.graphify_python) -c "
import json, re
from pathlib import Path
data = json.loads(Path('graphify-out/graph.json').read_text())
vocab = set()
for n in data['nodes']:
    for c in re.findall(r'[^\W\d_]+', n.get('label','') or '', re.UNICODE):
        parts = re.findall(r'[A-Z]+(?=[A-Z][a-z])|[A-Z]?[a-z]+|[A-Z]+', c) or [c]
        for p in parts:
            t = p.lower()
            if 3 <= len(t) <= 30:
                vocab.add(t)
Path('graphify-out/.vocab.txt').write_text('\n'.join(sorted(vocab)))
print(f'vocab: {len(vocab)} tokens')
"
```

**AI 选 token 硬约束**：
- 必须**仅**从 `.vocab.txt` 选 token，**禁止编造**
- 最多选 **12 个** token
- 跨语言翻译需谨慎：俄语 `аутентификация` → `auth`/`credential`/`token`/`security`（前提是这些 token **存在于词表**）
- 形态学处理：`handlers` → `handler`（前提是存在）
- 找不到匹配时**输出空列表并告知用户**，不要伪造

### Step 1 — 用扩展后的 Query 串执行

```bash
graphify query "EXTENDED_QUESTION"
# 复杂查询可加 token 限制
graphify query "EXTENDED_QUESTION" --budget 1500
```

**输出原则**：
- 答案**必须基于 graph 输出**（`source_location` 引用）
- 信息不足时直接说「信息不足」，**不要幻觉**

---

## 3. 返回数据结构

### 节点（nodes）

```json
{
  "id": "auth_session_validatetoken",
  "label": "ValidateToken",
  "file_type": "code",
  "source_file": "src/auth/session.py",
  "source_location": "L42-58",
  "source_url": null,
  "captured_at": null,
  "author": null,
  "contributor": null
}
```

**`file_type` 取值**（仅这 6 个，其他值会被拒绝）：

| 值 | 含义 |
|----|------|
| `code` | 源代码 |
| `document` | 文档 |
| `paper` | 论文 |
| `image` | 图片 |
| `rationale` | 设计理念、决策理由 |
| `concept` | 抽象概念、模式 |

### 边（edges）

```json
{
  "source": "session_validatetoken",
  "target": "user_model",
  "relation": "calls",
  "confidence": "EXTRACTED",
  "confidence_score": 1.0,
  "source_file": "src/auth/session.py",
  "weight": 1.0
}
```

**`relation` 取值**：`calls` / `implements` / `references` / `cites` / `conceptually_related_to` / `shares_data_with` / `semantically_similar_to` / `rationale_for`

**`confidence` 取值**（与 `confidence_score` 强相关）：

| Confidence | Score | 含义 |
|------------|-------|------|
| `EXTRACTED` | 1.0 | 源码显式存在（import、call、citation） |
| `INFERRED` | 0.55-0.95 | 推理得出（共享数据结构、隐含依赖） |
| `AMBIGUOUS` | 0.1-0.3 | 不确定，需人工审查 |

### 超边（hyperedges）

当 3+ 节点共同参与某个概念/流程时使用，**慎用**，每 chunk 最多 3 条。

---

## 4. 设计 Query 的最佳实践

### ✅ DO

- **用名词短语**而非完整问句：「ORM model base class」优于「How is the ORM model defined?」
- **优先高频 token**：选词表里出现在多个节点 label 中的 token
- **一个 query 一次只问一件事**：避免「Auth、Cache、DB 的实现」这种复合查询
- **失败时降级**：graphify 返回空 → 执行 bash fallback → 标记 `[NO_DATA]`
- **复用 .vocab.txt**：每次设计 query 前先看词表，避免凭空构造

### ❌ DON'T

- **不要凭训练记忆造 token**——必须从 `.vocab.txt` 选
- **不要超过 12 个 token**——扩展后的 query 串越长噪声越多
- **不要用完整问句**——「What is X?」「How does Y work?」几乎都返回 0 结果
- **不要用陌生缩略语**——除非你确认该缩写在词表里
- **不要直接信任 `AMBIGUOUS` 边**——confidence_score < 0.3 的要标 `[需人工确认]`

---

## 5. 典型用例（Architect-Stage0 阶段 A 参考）

### 5.1 查 ORM 模型定义

```bash
graphify query "ORM model base class"
# fallback
grep -rn "class.*Base" --include="*.py" .
```

### 5.2 查 Redux Store 配置

```bash
graphify query "redux store configuration"
# fallback
grep -rn "configureStore\|createStore" --include="*.ts" --include="*.tsx" .
```

### 5.3 查 API 端点

```bash
graphify query "REST API endpoint route"
# fallback
grep -rn "@app.route\|@router.get\|router.post" --include="*.py" .
```

### 5.4 查数据库连接配置

```bash
graphify query "database connection configuration"
# fallback
grep -rn "create_engine\|database_url\|DB_URL" --include="*.py" .
```

### 5.5 查领域实体（动态）

```bash
# 先用 vocab 找到 "user"、"entity" 是否存在
graphify query "user entity fields"
# fallback
grep -rn "class User" --include="*.py" .
```

### 5.6 查跨模块依赖

```bash
# 用 path 而非 query，因为是已知两概念
graphify path "UserController" "Database"
```

### 5.7 理解某个具体类

```bash
# 用 explain 获取单节点的完整解释
graphify explain "ValidateToken"
```

---

## 6. 前置条件（设计 Query 前必确认）

- [ ] `graphify-out/graph.json` 存在
- [ ] `graphify-out/.vocab.txt` 已生成（执行 Step 0.1）
- [ ] `.claude/context/feature-elements.md` 已存在（PM-Stage0 产物）
- [ ] 若图谱为空或文件未提取完 → **先跑 `/graphify .` 构建图谱**

---

## 7. 失败处理决策树

```
graphify query 执行
  ├─ 返回结果（nodes 非空）→ 用 source_location 引用，组装文档
  ├─ 返回 0 节点 → 执行 bash fallback
  │     ├─ bash 有结果 → 标记 [BASH_FALLBACK]，引用 file:line
  │     └─ bash 无结果 → 标记 [NO_DATA]，写入 query_plan.md
  └─ 命令报错（graph.json 损坏）→ 提示用户跑 /graphify --update
```

---

## 8. 进阶技巧

### 8.1 控制 token 消耗

```bash
# 默认返回可能很大，加 --budget 限制
graphify query "ORM model" --budget 800
```

### 8.2 DFS vs BFS 选择

| 问题类型 | 模式 |
|---------|------|
| 「X 是什么」「X 连接什么」 | BFS（默认） |
| 「X 怎么到 Y」「X 的调用链」 | DFS (`--dfs`) |

### 8.3 反向引用

如果图谱有 `conceptually_related_to` 或 `semantically_similar_to` 边，可以从一个已知节点找到「意想不到的连接」。这正是 graphify 的价值所在。

---

## 9. 参考

- 完整能力：`.claude/skills/graphify/SKILL.md`
- 触发命令：`/graphify` 或 `graphify <子命令>`
- 输出目录：`graphify-out/`
