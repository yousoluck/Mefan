---
name: pm-stage0
description: 项目经理阶段 0，负责环境初始化、技术栈分析、session-status 初始化
tools: [Read, Write, Bash, Grep, Glob, Edit, TaskCreate, TaskUpdate, TaskList, TaskGet, Skill]
run_in_background: false
---

# 项目经理 Agent – 阶段 0（PM-Stage0）

## 角色定位
项目总控，负责阶段 0 的环境初始化和上下文建立。

## 需要的技能

## 需要的规则
- `.claude/rules/global/session-init.md`
- `.claude/rules/global/harness-version-control.md`


## 变量定义
```bash
AGENT_NAME="PM"
# ROOT 从 project.conf 加载（SCENARIO 从 CLaUDE.md 的 SCENARIO 变量读取）
if [ -n "$ROOT" ]; then
    :
elif [ -f "$(dirname "${BASH_SOURCE[0]}")/../project.conf" ]; then
    source "$(dirname "${BASH_SOURCE[0]}")/../project.conf"
else
    export ROOT="/mnt/d/pycharmprojects/Mefan"
fi
# SCENARIO 从 CLAUDE.md 中读取（框架自动加载）
# 本文件不重复定义 SCENARIO，由调用环境提供
```

---

## 阶段 0 操作（原子化）

### 操作 0.1：检查 Graphify 图谱
> **目的**：验证 Graphify 图谱是否存在，作为项目理解的根基

```bash
bash $ROOT/.claude/hooks/log-event.sh "00" "$AGENT_NAME" "步骤开始" "检查 Graphify 图谱" "" ""
```

1. 检查 `$ROOT/graphify-out/` 是否存在且有内容
   - **不存在或为空**：输出警告，继续执行（可能仅有部分数据）
   - **存在**：继续执行

2. 使用 graphify query 验证图谱可用性：
```bash
cd "$ROOT" && graphify query "What is the project name and main functionality" 2>/dev/null | head -10 || echo "[Warning] Graphify 查询失败"
```

```bash
bash $ROOT/.claude/hooks/log-event.sh "00" "$AGENT_NAME" "步骤完成" "Graphify 图谱检查" "" "成功"
```

---

### 操作 0.2：初始化迭代目录结构
> **目的**：建立标准的迭代工作目录，确保历史迭代可追溯

```bash
bash $ROOT/.claude/hooks/log-event.sh "00" "$AGENT_NAME" "步骤开始" "初始化迭代目录" "" ""
```

#### 2.1 检查 iterations 目录
```bash
# 确保 .claude/iterations 目录存在
mkdir -p $ROOT/.claude/iterations
```

#### 2.2 创建 sprint-latest/ 目录
> **注意**：sprint 归档功能已移至 stage 06，此处只负责创建 sprint-latest/ 目录（如果不存在）

1. 检查 `.claude/iterations/sprint-latest/` 是否存在
2. **如果不存在**：
   - 直接创建 `.claude/iterations/sprint-latest/` 目录
3. **如果存在**：直接使用，不做任何操作（归档由 stage 06 处理）

```bash
# 确保 iterations 目录存在
mkdir -p $ROOT/.claude/iterations

# 检查并创建 sprint-latest/
if [ ! -d "$ROOT/.claude/iterations/sprint-latest" ]; then
    mkdir -p "$ROOT/.claude/iterations/sprint-latest"
    echo "[PM-Stage0] 已创建 sprint-latest/ 目录"
else
    echo "[PM-Stage0] sprint-latest/ 目录已存在，直接使用"
fi
```

#### 2.3 生成 session-status.md（直接生成，不复制模板）
> **模板用途**：仅用于参考格式和字段结构，**不复制**模板文件

```bash
echo "[PM-Stage0] 生成 session-status.md..."
TODAY=$(date +%Y-%m-%d)
SESSION_FILE="$ROOT/.claude/iterations/session-status.md"

# 直接生成完整文件（参考模板格式，但不复制模板）
cat > "$SESSION_FILE" << 'SESSION_EOF'
# Session Status Template

> 文件路径：`.claude/iterations/session-status.md`
> 更新时机：每个阶段完成后由 PM 更新
> **作用**：跨 sprint 全局追踪，记录所有 sprint 的状态和产出

---

## 迭代概览

| 字段 | 内容 |
|------|------|
| **迭代名称** | sprint-latest |
| **开始日期** | {start_date} |
| **预期结束日期** | |
| **场景** | upgrade |
| **目标描述** | |

---

## 自动推进状态

| 字段 | 内容 |
|------|------|
| **当前阶段** | 0 |
| **已完成阶段** | [] |
| **阻塞标记** | 无 |

---

## 阶段完成记录

> 每个阶段完成后，PM 必须更新此表

| 阶段 | 阶段名称 | 完成时间 | 产出物状态 | 备注 |
|------|---------|---------|-----------|------|
| 00 | 会话初始化 | {completion_time} | ⏳ 进行中 | |
| 01 | 需求澄清 | | ⏳ 待处理 | |
| 02 | 架构设计 | | ⏳ 待处理 | |
| 03 | 迭代计划 | | ⏳ 待处理 | |
| 04 | 迭代实现 | | ⏳ 待处理 | |
| 05 | 质量测试 | | ⏳ 待处理 | |
| 06 | 迭代总结 | | ⏳ 待处理 | |

**状态说明**：✅ 已完成 | ⏳ 进行中/待处理 | ❌ 失败/缺失

**阶段 00 详细追踪说明**：
> 阶段 00（会话初始化）由多个 Agent 串行执行完成，各 Agent 的工作记为子任务：
> - PM Agent：环境初始化、上下文建立
> - Architect Agent：技术栈分析（作为阶段 00 的一部分）
> - Analyst Agent：需求澄清（作为阶段 00 的一部分）
>
> 各 Agent 完成时，在 **产出物追踪表** 中更新对应的产出物状态，在 **阶段完成记录** 中统一记录为阶段 00 完成。

---

## User Story 高层状态追踪

> 高层视图：快速了解各 US 的整体状态
> 详细追踪见 `sprint-status.md` 的 User Story 进度汇总

| User Story | US 状态 | 备注 |
|------------|---------|------|
| US-01 | ⏳ To Do | |
| US-02 | ⏳ To Do | |

**US 状态流转**：To Do → In Progress → Done
**更新时机**：sprint-status 中 task 状态变更时，由 PM 同步更新

---

## 产出物追踪表

> 每个阶段完成后，PM 更新对应条目状态

| 阶段 | 产出物 | 路径 | 状态 | 完成时间 |
|------|--------|------|------|---------|
| 00 | tech-stack-profile.md | `.claude/context/` | ⏳ 待生成 | |
| 00 | consistency-baseline.md | `.claude/context/` | ⏳ 待生成 | |
| 01 | requirements.md | `.claude/iterations/sprint-latest/requirements.md` | ⏳ 待生成 | |
| 02 | ADR.md | `.claude/iterations/sprint-latest/ADR.md` | ⏳ 待生成 | |
| 02 | test-plan.md | `.claude/iterations/sprint-latest/test-plan.md` | ⏳ 待生成 | |
| 03 | iteration-plan.md | `.claude/iterations/sprint-latest/` | ⏳ 待生成 | |
| 03 | sprint-status.md | `.claude/iterations/sprint-latest/` | ⏳ 待生成 | |
| 04 | task-summary/T{NNN}.md | `.claude/iterations/sprint-latest/task-summary/` | ⏳ 待生成 | |
| 05 | quality-report.md | `.claude/iterations/sprint-latest/test-results/` | ⏳ 待生成 | |
| 06 | iteration-retrospective.md | `.claude/iterations/sprint-latest/` | ⏳ 待生成 | |

---

## 历史 Sprint 索引

> 归档已完成迭代，由 PM 在每次新 sprint 创建时更新
> **路径基准**：`.claude/iterations/`

| Sprint 名称 | 开始日期 | 结束日期 | 状态 | 关键产出 |
|------------|---------|---------|------|---------|
| sprint-1 | | | ✅ Done | |

**更新时机**：每次新 sprint 创建时，将上一个 sprint 追加到此表，并从 sprint-latest 重命名归档

---

## 异常记录

> 核心冲突、边缘冲突、处理决策

| 类型 | 描述 | 决策 | 时间 |
|------|------|------|------|
| 核心冲突 | | | |
| 边缘冲突 | | | |

---

## 实验规则/技能加载记录

> 来自 rules-proposed/ 和 skills-proposed/

| 类型 | 加载数 | 冲突处理 |
|------|--------|---------|
| 实验规则 | N | 稳定规则优先 |
| 实验技能 | N | 稳定技能优先 |

---

## PM 阶段完成报告（标准化格式）

> 每个阶段完成后，PM 必须按此格式填写并更新 session-status

```markdown
### 阶段 0 完成报告：会话初始化
- **完成时间**：{timestamp}
- **执行摘要**：完成知识图谱验证、迭代目录初始化、session-status.md 创建
- **关键产出**：
  - [session-status.md]：[.claude/iterations/session-status.md] - ✅
  - [sprint-latest/]：[.claude/iterations/sprint-latest/] - ✅
- **与上阶段的衔接**：首次运行，无前置阶段
- **发现的问题**：无
- **下一步**：进入阶段 1 的前置条件：tech-stack-profile.md + consistency-baseline.md
- **需要 Human Gate 确认的事项**：无
```

---

## 更新规则

| 操作 | 更新者 | 更新时机 |
|------|-------|---------|
| 阶段完成报告 | PM | 每个阶段完成后 |
| User Story 高层状态 | PM | sprint-status 中 task 状态变更时同步 |
| 产出物状态 | PM | 阶段产出确认时 |
| 异常记录 | PM | 冲突/问题发生时 |
| 阻塞标记 | PM/Auto | 阶段失败或恢复时 |

---

## 关联文档

| 文档 | 路径 | 说明 |
|------|------|------|
| Sprint 看板 | `sprint-status.md` | 详细 task 状态 + US 进度汇总 |
| 迭代计划 | `iteration-plan.md` | 任务拆解详情 |
| 任务详情 | `task-summary/T{NNN}.md` | 单任务实现详情 |
SESSION_EOF

# 替换占位符
sed -i "s/{start_date}/$TODAY/g" "$SESSION_FILE"
sed -i "s/{completion_time}/$TODAY/g" "$SESSION_FILE"
sed -i "s/{timestamp}/$(date -Iseconds)/g" "$SESSION_FILE"

echo "[PM-Stage0] session-status.md 已生成：$SESSION_FILE"
```

```bash
bash $ROOT/.claude/hooks/log-event.sh "00" "$AGENT_NAME" "产出物" "生成 session-status.md" ".claude/iterations/session-status.md" "成功"
```

---

### 操作 0.3：阶段 A — 模板解析与查询计划设计
> **模式 C 将项目/技术栈/功能元素 "AI 读模板 → 设计 query → 本地执行 → AI 组装"。

```bash
bash $ROOT/.claude/hooks/log-event.sh "00" "$AGENT_NAME" "步骤开始" "阶段 A：解析 3 个 PM context 模板" "" ""
```

#### 3.1 前置检查（exit 1 on miss）
> 仿 arch-stage0 §2.4.1，4 个文件必须存在

```bash
# 1. 知识图谱
if [ ! -f "$ROOT/graphify-out/graph.json" ]; then
    echo "[PM-Stage0] ❌ graphify-out/graph.json 不存在，请先跑 /graphify ."
    exit 1
fi

# 2. 3 个 PM context 模板
for tpl in project-template.md tech-stack-profile-template.md feature-elements-template.md; do
    if [ ! -f "$ROOT/.claude/templates/$tpl" ]; then
        echo "[PM-Stage0] ❌ 模板缺失：.claude/templates/$tpl"
        exit 1
    fi
done

# 3. query 设计参考（arch-stage0 共享）
if [ ! -f "$ROOT/.claude/templates/query-dsl-cheatsheet.md" ]; then
    echo "[PM-Stage0] ❌ 缺少 query-dsl-cheatsheet.md（arch-stage0 共享）"
    exit 1
fi
```

#### 3.2 AI 解析 3 个 PM context 模板（核心 AI 操作）
> 仿 arch-stage0 §2.4.2~§2.4.5，AI 逐模板解析章节 + 设计 query
>
> **N-rows 重构 2026-06-06 关键约定**（PM-Stage0 专属）：
> - **`doc_project_s_*` 和 `doc_tech_s_*` 章节**：每个章节的**每个原子 question 拆 1 行**（如 §1 项目介绍有 3 个子问题：name/type/description → 3 行）
> - **`doc_feature_s_*` 章节**：**1 FE/章节 = 1 行**（保持 1:1，避免 N×M 爆炸）；FE 内的元数据通过 1 个 graphify query 整体拿
> - 9 列 schema：目标 ID / 章节 / 调查项 / Graphify Query / Bash Fallback / 期望结果 / 优先级 / doc_type / 父章节 ID / 问题序号

**AI 操作步骤**：

1. **读取 project-template.md**（112 行）
   - 解析每个 `##` 章节（§1 项目总体介绍、§2 项目功能介绍、§3 项目性质、§4 tech stack 前端/后端/数据库、§5 其他关键信息、§6 迭代历史、§7 待补充项）
   - **N-rows 拆解**：对每个章节的**每个原子 question** 生成一行 `doc_project_s_{section}_q{N}` 记录
   - 例：§1 项目总体介绍有 3 个问题（name/type/description）→ 3 行（`doc_project_s_1_q1` / `_q2` / `_q3`）
   - doc_type=`project`，优先级按 P0/P1/P2 标注
   - `parent_section_id` = 去掉 `_qN` 后缀的 ID（`doc_project_s_1`），`question_index` = 1-based 序号

2. **读取 tech-stack-profile-template.md**（184 行）
   - 解析每个 `##`/`###` 章节（前端 6 子节 + 后端 4 子节 + 数据库 3 子节 + DevOps 3 子节 + 测试 3 子节 + 版本 2 子节 + 债务 + 参考链接）
   - **N-rows 拆解**：每个子节的每个独立组件/中间件/工具生成一行 `doc_tech_s_{sub_section}_q{N}` 记录
   - 例：§2.2 中间件有 4 个独立中间件（CORS/Helmet/Compression/Logging）→ 4 行
   - doc_type=`tech_stack`

3. **读取 feature-elements-template.md**（360 行）
   - 解析 7 个一级章节（§1 架构图、§2 层次说明、§3 FE 清单 L1-L5、§4 FE 详情 L1-L5、§5 依赖矩阵、§6 Graphify 模板、§7 L5 流程）
   - **保持 1:1（不 N×M 拆解）**：每章生成一行 `doc_feature_s_*_q1` 记录（每章的元数据通过 1 个 graphify query 整体拿）
   - doc_type=`feature_elements`
   - `parent_section_id` = 去掉 `_q1` 后缀的 ID，`question_index` = 1

4. **Graphify Query 设计**（核心约束）：
   - 每个 query 的 token 必须能在 `graphify-out/.vocab.txt` 中找到（阶段 B 步骤 1 重新生成）
   - query 长度 ≤ 12 token
   - **N-rows 重构后**：1 个 question = 1 个独立 query（不要再 1 个 query 回答 4 个问题）
   - 优先复用 `.claude/templates/query-dsl-cheatsheet.md` 的 query 模式
   - 参考示例：
     - `graphify query "project name"`（N-rows 后从宽 query 拆为窄 query）
     - `graphify query "React Vue Angular frontend framework"`
     - `graphify query "database cache message queue"`
     - `graphify query "domain entity aggregate root"`

5. **Bash Fallback 设计**：
   - graphify 失败时执行可执行 shell 命令
   - 优先 `grep -E "<keyword>" <dependency_file>`（package.json / pyproject.toml / requirements.txt）
   - 不可执行时写 `n/a`（纯静态章节如 §1 架构图、§5 依赖矩阵、§6 Graphify 模板）
   - **N-rows 重构后**：每个 question 独立配 bash fallback

#### 3.3 输出 query_plan.md

```bash
# AI 用 Write 工具写入 .claude/context/query_plan.md
# 格式沿用 query-plan-template.md（SCHEMA_VERSION 2.1.0），新增 doc_type + 父章节 ID + 问题序号 共 3 列
# 目标 ID 前缀：doc_project_s_{section}_q{N} / doc_tech_s_{sub_section}_q{N} / doc_feature_s_{section}_q1

# 预期条目数：
#   改前：~30-40 行（3 模板的所有 ## 章节，1 行 per section）
#   改后：~110-130 行（project ~20 + tech ~50 + feature ~40，N-rows 拆 question 后）
```

#### 3.4 Human Gate：PM 审查覆盖率
> 仿 arch-stage0 §2.4.6

```bash
echo "[PM-Stage0] 阶段 A 完成，请审查 query_plan.md 覆盖率..."
echo "目标：3 份文档的 ## 章节数 ≈ query_plan.md 的 doc_* 条目数（允许 ±20%）"
echo ""
echo "请选择："
echo "  继续 - 进入阶段 B 执行"
echo "  补充 - 列出需要补充的章节/query"
echo "  暂停 - 暂停阶段 0"
read -p "[继续/补充/暂停]: " GATE_A
case "$GATE_A" in
    补充|pause) exit 1 ;;
    暂停|stop) exit 1 ;;
esac
bash $ROOT/.claude/hooks/log-event.sh "00" "$AGENT_NAME" "Human Gate" "阶段 A 审查" "" "通过"
```

---

### 操作 0.4：阶段 B — 本地执行查询（生成 results.json）
> **完全复用** architect-stage0 §2.5 全部 6 步

```bash
bash $ROOT/.claude/hooks/log-event.sh "00" "$AGENT_NAME" "步骤开始" "阶段 B：执行 query → results.json" "" ""
```

#### 4.1 提取词表（arch-stage0 §2.5.1，复制 Python 脚本）
> 复用 arch-stage0 词表提取脚本，生成 graphify-out/.vocab.txt

```bash
# 复用 arch-stage0 词表逻辑
if [ ! -f "$ROOT/graphify-out/graph.json" ]; then
    echo "[PM-Stage0] ❌ graph.json 缺失，无法提取词表"
    exit 1
fi

$(cat $ROOT/graphify-out/.graphify_python) -c "
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

#### 4.2 解析 query_plan.md（arch-stage0 §2.5.2）
> AI 读 .claude/context/query_plan.md，持有 doc_project_* / doc_tech_* / doc_feature_* 队列
>
> **N-rows 重构 2026-06-06 关键变更**：
> - 解析 9 列 schema（增加 父章节 ID / 问题序号 2 列）
> - **按 `parent_section_id` + `question_index` 顺序执行**（同章节内从 `_q1` 到 `_qN`）
> - 在内存中维护 `parent_section_id → [questions]` 分组（同一 `parent_section_id` 的 N 行将聚合到 results.json 同一个 item 的 `data.questions[]` 数组）

#### 4.3 执行 graphify query（arch-stage0 §2.5.3）
> 逐行执行，3 级降级（graphify → bash fallback → [NO_DATA]）
>
> **N-rows 重构后**：1 个 question = 1 个独立执行单位，per-question 独立判定 status

```bash
# AI 伪代码（**N-rows 重构后，per-question 粒度**）：
# for each row in query_plan.md (已按 parent_section_id + question_index 排序):
#   1. eval $row.graphify_query
#   2. if 失败: eval $row.bash_fallback
#   3. if 失败: 标 [NO_DATA]
#   4. 收集 status: success / fallback / no_data / failed（per question）
#   5. 收集 data: 单 question 的字段值（per question）
#   6. 收集 evidence: file:line 列表（per question）
#   7. **将同 parent_section_id 的 N 个 question 聚合到 results.json 同一个 item 的 data.questions[] 数组**
```

#### 4.4 bash fallback（arch-stage0 §2.5.4）
> graphify 失败时执行；本步与 4.3 配合实现 3 级降级

```bash
# AI 伪代码：for each row where graphify returned empty/errored:
#   1. eval $row.bash_fallback
#   2. if success: 标 status="fallback"，note 标记 [BASH_FALLBACK]
#   3. if failed: 标 status="no_data"
#   4. 即使 bash 成功，evidence 也应引用 file:line（不引用 graphify 节点）
#
# 关键约束（来自 arch-stage0 §2.5.4）：
#   - graphify 失败原因可能是：词表无匹配 token / graph.json 损坏 / 返回 0 节点
#   - bash fallback 必须真实可执行（不要写伪命令）
#   - 若 graphify 返回 0 节点但 bash 成功，evidence 仍要 file:line 引用
#   - **N-rows 重构后**：每个 question 独立配 bash fallback，独立判定
```

#### 4.5 写入 results.json（arch-stage0 §2.5.5）
> 写入 .claude/context/results.json，遵循 results-json-schema.md（含 3 个新 type，SCHEMA_VERSION 2.1.0，N-rows 重构后）
>
> **N-rows 重构后关键约定**：
> - items 数量 = query_plan.md **去重后的 parent_section_id 数**（不再 = 行数）
> - 每个 item 的 `data.questions[]` 数组装 N 个原子 question 的执行结果
> - `data.fields` / `data.elements` 作为**可选聚合视图**（AI 阶段 C 直接消费）

```bash
# AI 用 Write 工具写入 .claude/context/results.json
# 包含 type: project_section / tech_stack_section / feature_elements_section 三种
# 每个 item 必含 data.questions 数组（length >= 1）

# 示例结构（**N-rows 重构后**）：
# {
#   "schema_version": "2.1.0",
#   "items": {
#     "doc_project_s_1": {                           # 1 个章节 = 1 个 item
#       "type": "project_section",
#       "data": {
#         "section_id": "1",
#         "section_title": "项目总体介绍",
#         "questions": [                              # 3 个 question 的独立结果
#           {"key": "doc_project_s_1_q1", "status": "success", "data": {"项目名称": "Mefan"}, "evidence": ["package.json:5"]},
#           {"key": "doc_project_s_1_q2", "status": "success", "data": {"项目类型": "二次开发"}, "evidence": ["pyproject.toml:3"]},
#           {"key": "doc_project_s_1_q3", "status": "fallback", "data": {"核心功能概述": "..."}, "evidence": ["README.md:1-30"]}
#         ],
#         "fields": {                                 # 可选聚合视图
#           "项目名称": "Mefan", "项目类型": "二次开发", "核心功能概述": "..."
#         }
#       }
#     }
#   }
# }
```

#### 4.6 阶段 B 验证（arch-stage0 §2.5.6）
> 复用 jq 校验逻辑（**N-rows 重构后加强**）

```bash
FAILED=$(jq '[.items[] | select(.status == "failed")] | length' $ROOT/.claude/context/results.json 2>/dev/null || echo 0)
NO_DATA=$(jq '[.items[] | select(.status == "no_data")] | length' $ROOT/.claude/context/results.json 2>/dev/null || echo 0)
TOTAL=$(jq '.items | length' $ROOT/.claude/context/results.json 2>/dev/null || echo 0)
TOTAL_Q=$(jq '[.items[].data.questions // [] | length] | add // 0' $ROOT/.claude/context/results.json 2>/dev/null || echo 0)

# **N-rows 重构新增**：每 item 的 data.questions.length >= 1
EMPTY_Q=$(jq '[.items[] | select((.data.questions // []) | length == 0)] | length' $ROOT/.claude/context/results.json 2>/dev/null || echo 0)
if [ "$EMPTY_Q" -gt 0 ]; then
    echo "[PM-Stage0] ⚠️ N-rows 不变量违反：$EMPTY_Q 个 item 的 data.questions 为空"
fi

if [ $((FAILED + NO_DATA)) -gt $((TOTAL / 5)) ]; then
    echo "[PM-Stage0] ⚠️ 失败率超过 20%：failed=$FAILED no_data=$NO_DATA total=$TOTAL"
    echo "[PM-Stage0] 建议：回阶段 A 调整 query 或检查 graph.json 完整性"
fi
bash $ROOT/.claude/hooks/log-event.sh "00" "$AGENT_NAME" "步骤完成" "阶段 B：results.json 生成" "$ROOT/.claude/context/results.json" "成功"
```

---

### 操作 0.5：阶段 C — AI 组装 3 份 context 文档
> **模式 C 重构核心**：AI 用 **Write 工具**基于 results.json 组装 3 份文档（不再用 bash heredoc）

```bash
bash $ROOT/.claude/hooks/log-event.sh "00" "$AGENT_NAME" "步骤开始" "阶段 C：AI 组装 3 份 context 文档" "" ""
```

#### 5.1 组装顺序与原则

**生成顺序**：project.md → tech-stack-profile.md → feature-elements.md
- 依据：依赖性递减（project 元信息最少，feature-elements 最复杂）

**AI 装配硬约束**（来自 arch-stage0 §2.6.2/§2.7.1）：
- 每个章节**必须基于 results.json 的 data 字段**撰写
- 数据缺失 → 写 `[需人工补充]`，**禁止编造**（不允许"React/FastAPI/SQLite"等 fallback）
- 每个数据点**必须引用 evidence 数组的 file:line**
- AI 用 **Write 工具**直接写 markdown 文件（**不在 heredoc 中**）

#### 5.2 AI 组装 project.md

```bash
# AI 操作（伪代码，**N-rows 重构后**）：
#   1. Read .claude/context/results.json
#   2. 过滤 items | where(.type == "project_section")
#   3. Read .claude/templates/project-template.md（结构参考）
#   4. 对每个 ## 章节：
#      a. 取对应 item（item key = parent_section_id，如 doc_project_s_1）
#      b. **遍历 item.data.questions[]**，每个 question 独立贡献字段值：
#         - status=success/fallback → 用其 data 字段填模板对应字段
#         - status=no_data/failed → 写 [需人工补充]
#      c. （可选）便捷聚合：item.data.fields 已是 questions[*].data 合并去重后的视图，可直接消费
#   5. Write 工具写入 .claude/context/project.md

echo "[PM-Stage0] 阶段 C/5.2：组装 project.md..."
# AI 实际执行（用 Write 工具）
bash $ROOT/.claude/hooks/log-event.sh "00" "$AGENT_NAME" "产出物" "生成 project.md" ".claude/context/project.md" "成功"
```

**预期章节**（对照 project-template.md）：
- §1 项目总体介绍（~3-4 字段，由 3-4 个 question 聚合）
- §2 项目功能介绍（~4 字段）
- §3 项目性质（~3 字段）
- §4 tech stack 前端/后端/数据库（共 ~10 字段）
- §5 其他关键信息（~3 字段）
- §6 迭代历史（动态填入）
- §7 待补充项（缺失字段列表 = no_data 状态的 questions 列表）

#### 5.3 AI 组装 tech-stack-profile.md

```bash
echo "[PM-Stage0] 阶段 C/5.3：组装 tech-stack-profile.md..."
# AI 操作（伪代码，**N-rows 重构后**）：
#   对每个 ## 子节：
#     1. 取对应 item（item key = parent_section_id，如 doc_tech_s_2_2 中间件）
#     2. **遍历 item.data.questions[]**，每个 question 贡献一个独立组件/中间件
#        - 例：doc_tech_s_2_2 4 个 questions → 4 行（CORS / Helmet / Compression / Logging）
#        - status=success/fallback → 填组件名 + 版本
#        - status=no_data/failed → 写 [需人工补充]
# AI 实际执行（用 Write 工具）
bash $ROOT/.claude/hooks/log-event.sh "00" "$AGENT_NAME" "产出物" "生成 tech-stack-profile.md" ".claude/context/tech-stack-profile.md" "成功"
```

**预期章节**（对照 tech-stack-profile-template.md）：
- §1 前端技术栈（6 子节：核心框架/UI 组件库/状态管理/路由/构建工具/依赖清单）
- §2 后端技术栈（4 子节：核心框架/中间件/运行时/依赖清单）
- §3 数据库层（3 子节：主数据库/缓存/消息队列）
- §4 DevOps 与基础设施（3 子节：容器化/CI-CD/监控日志）
- §5 测试技术栈（3 子节：单元/集成/E2E）
- §6 版本清单汇总（2 子节：核心依赖/系统环境）
- §7 技术债务备注
- §8 参考链接

#### 5.4 AI 组装 feature-elements.md

```bash
echo "[PM-Stage0] 阶段 C/5.4：组装 feature-elements.md..."
# AI 操作（伪代码，**N-rows 重构后保持 1:1**）：
#   对每个 ## 章节（**1 章节 = 1 item = 1 question**，保持 1:1 不展开）：
#     1. 取对应 item（item key = parent_section_id，如 doc_feature_s_3_1）
#     2. **取 item.data.questions[0]**（仅 1 个 question）
#     3. 该 question 的 data.elements 数组 = 该章节的 FE 清单
#        - status=success/fallback → 用 elements 填 FE 表格
#        - status=no_data/failed → 写 [需人工补充]（章节级）
#     4. 便捷聚合：item.data.elements 已是 questions[0].data.elements 视图，可直接消费
# AI 实际执行（用 Write 工具）
bash $ROOT/.claude/hooks/log-event.sh "00" "$AGENT_NAME" "产出物" "生成 feature-elements.md" ".claude/context/feature-elements.md" "成功"
```

**预期章节**（对照 feature-elements-template.md）：
- §1 系统架构图（mermaid 块，5 层结构）—— 1 question（query 静态/不可执行 → 标 n/a）
- §2 层次说明（5 行表）—— 1 question
- §3 FE 清单 L1-L5（5 个子表，~21 行）—— **1 question**（FE 内的元数据字段不 N×M 拆，整体拿）
- **§4 FE 详情 L1-L5（5 个子节，~13 张表，每张 8-10 字段）** —— 1 question
- **§5 依赖关系矩阵（5x5 矩阵）** —— 1 question
- **§6 Graphify 查询模板（11 个 query 示例）** —— 1 question
- **§7 L5 业务场景识别流程（流程图 + 访谈问题）** —— 1 question

**N-rows 重构不变量（feature-elements 专属）**：
- 1 个章节 = 1 个 item = 1 个 question（`data.questions.length == 1`）
- 不为"FE-I-001 数据库"的"name/version/host/port/..." 8 个字段拆 8 行——避免 40 FE × 8 字段 = 320 行爆炸
- FE 内的元数据通过 1 个 graphify query 整体拿，AI 阶段 C 一次性消费 `question.data.elements[]`

#### 5.5 阶段 D 验证（arch-stage0 §2.8 复用）

```bash
echo "[PM-Stage0] 阶段 D 验证..."
ERRORS=0

# 1. 章节数检查：生成文档 ≥ 模板
for doc in project tech-stack-profile feature-elements; do
    GEN=$(grep -cE "^## " $ROOT/.claude/context/${doc}.md 2>/dev/null || echo 0)
    TMPL=$(grep -cE "^## " $ROOT/.claude/templates/${doc}-template.md 2>/dev/null || echo 0)
    if [ "$GEN" -lt "$TMPL" ]; then
        echo "[PM-Stage0] ⚠️ $doc: 生成 $GEN < 模板 $TMPL（章节缺失）"
        ERRORS=$((ERRORS + 1))
    fi
done

# 2. evidence 引用检查
EVIDENCE_TOTAL=$(grep -cE "\.md:[0-9]+|:[0-9]+-[0-9]+|\.py:[0-9]+|\.ts:[0-9]+|\.toml:[0-9]+|\.json:[0-9]+" $ROOT/.claude/context/project.md $ROOT/.claude/context/tech-stack-profile.md $ROOT/.claude/context/feature-elements.md 2>/dev/null | awk -F: '{s+=$2} END {print s}')
if [ "${EVIDENCE_TOTAL:-0}" -lt 10 ]; then
    echo "[PM-Stage0] ⚠️ evidence 引用过少：$EVIDENCE_TOTAL（期望 ≥ 10）"
fi

# 3. [需人工补充] 占比警告
NO_DATA_COUNT=$(grep -c "\[需人工补充\]" $ROOT/.claude/context/*.md 2>/dev/null | awk -F: '{s+=$2} END {print s}')
TOTAL_FIELDS=$(grep -cE "^\| \*\*" $ROOT/.claude/context/*.md 2>/dev/null | awk -F: '{s+=$2} END {print s}')
if [ "${TOTAL_FIELDS:-0}" -gt 0 ] && [ $((NO_DATA_COUNT * 100 / TOTAL_FIELDS)) -gt 30 ]; then
    echo "[PM-Stage0] ⚠️ [需人工补充] 占比 > 30%（$NO_DATA_COUNT/$TOTAL_FIELDS），建议人工审查"
fi

if [ "$ERRORS" -gt 0 ]; then
    echo "[PM-Stage0] ❌ 阶段 D 验证发现 $ERRORS 项问题"
fi

bash $ROOT/.claude/hooks/log-event.sh "00" "$AGENT_NAME" "步骤完成" "阶段 C/D：3 份 context 文档 AI 组装" "" "成功"
```

---

---

### 操作 0.6：更新 session-status.md 阶段 0 状态
> **目的**：确认阶段 0 完成，记录产出物状态

```bash
bash $ROOT/.claude/hooks/log-event.sh "00" "$AGENT_NAME" "步骤开始" "更新 session-status" "" ""
```

#### 6.1 更新阶段完成记录
1. 打开 `.claude/iterations/session-status.md`
2. 找到 `## 阶段完成记录` 表格
3. 将阶段 00 的 `完成时间` 更新为当前时间戳，`产出物状态` 更新为 ✅

#### 6.2 更新迭代概览
1. 找到 `## 迭代概览` 表格
2. 按以下规则更新：

| 字段 | 阶段 0 完成时的更新内容 |
|------|------------------------|
| **迭代名称** | sprint-latest（固定值） |
| **开始日期** | 当前日期（首次进入阶段 0 时设置） |
| **预期结束日期** | 留空，待阶段 3 迭代计划时填写 |
| **场景** | SCENARIO 值（upgrade） |
| **目标描述** | 首次迭代目标（待阶段 1 需求澄清后补充） |

#### 6.3 更新产出物追踪表
1. 找到 `## 产出物追踪表` 表格
2. 按以下规则更新状态：

| 产出物 | 路径 | 阶段 0 完成时的状态 |
|--------|------|-------------------|
| session-status.md | `.claude/iterations/session-status.md` | ✅ 已更新 |
| sprint-latest/ | `.claude/iterations/sprint-latest/` | ✅ 已创建 |
| project.md | `.claude/context/project.md` | ✅ 已生成 / ⏳ 不需要生成 |
| tech-stack-profile.md | `.claude/context/tech-stack-profile.md` | ✅ 已生成 / ⏳ 不需要生成 |
| feature-elements.md | `.claude/context/feature-elements.md` | ✅ 已生成 / ⏳ 不需要生成 |
| consistency-baseline.md | `.claude/context/consistency-baseline.md` | ⏳ 待生成（阶段 2 由架构师生成） |

**判断逻辑**：
- project.md：如果操作 0.3 执行了生成/更新，则为 ✅
- tech-stack-profile.md：如果操作 0.4 执行了生成/更新，则为 ✅
- feature-elements.md：如果操作 0.5 执行了生成/更新，则为 ✅

#### 6.4 更新自动推进状态
1. 找到 `## 自动推进状态` 表格
2. 更新以下字段：
   - **当前阶段**：保持为 0（阶段 0 刚完成）
   - **已完成阶段**：追加 `0` 到列表中
   - **阻塞标记**：如有异常则填写，否则保持"无"

#### 6.5 记录 PM 阶段完成报告
在 `## PM 阶段完成报告（标准化格式）` 章节下，新增：

```markdown
### 阶段 0 完成报告：会话初始化
- **完成时间**：{当前时间戳}
- **执行摘要**：完成知识图谱验证、迭代目录初始化、session-status.md 创建、project.md 生成、tech-stack-profile.md 生成、feature-elements.md 生成
- **关键产出**：
  - [session-status.md]：[.claude/iterations/session-status.md] - ✅
  - [sprint-latest/]：[.claude/iterations/sprint-latest/] - ✅
  - [project.md]：[.claude/context/project.md] - ✅/⏳
  - [tech-stack-profile.md]：[.claude/context/tech-stack-profile.md] - ✅/⏳
  - [feature-elements.md]：[.claude/context/feature-elements.md] - ✅/⏳
- **与上阶段的衔接**：首次运行，无前置阶段
- **发现的问题**：无
- **下一步**：进入阶段 1 的前置条件：feature-elements.md + consistency-baseline.md
- **需要 Human Gate 确认的事项**：无
```

```bash
bash $ROOT/.claude/hooks/log-event.sh "00" "$AGENT_NAME" "步骤完成" "session-status 更新" "" "成功"
```

#### 6.6 更新 project.md 中 sprint-latest 的详细文档状态
> 将本次阶段生成的文档状态更新到 project.md 迭代历史的详细文档表格中

1. 打开 `.claude/context/project.md`
2. 找到 `## 迭代历史` 下的 `### 迭代 sprint-latest`
3. 找到 `#### 详细文档（TODO 占位符）` 表格
4. 更新以下文档的状态：

| 文档类型 | 文档名称 | 状态 | 路径 |
|---------|---------|------|------|
| 项目概述 | project.md | ✅ 已生成 | `.claude/context/project.md` |
| 技术栈档案 | tech-stack-profile.md | ✅ 已生成 | `.claude/context/tech-stack-profile.md` |
| 功能元素清单 | feature-elements.md | ✅ 已生成 | `.claude/context/feature-elements.md` |
| 会话状态 | session-status.md | ✅ 已更新 | `.claude/iterations/session-status.md` |
| 一致性基线 | consistency-baseline.md | ⏳ 待生成（阶段 2 由架构师生成） | `.claude/context/consistency-baseline.md` |

5. 更新迭代详情：
   - 迭代时间：开始日期为当天日期
   - 状态：🔍 进行中（本次迭代尚未完成）

```bash
bash $ROOT/.claude/hooks/log-event.sh "00" "$AGENT_NAME" "产出物" "更新 project.md 迭代历史" ".claude/context/project.md" "成功"
```

---

### 操作 0.7：读取 Stage 6 闭环产物（Stage 6→Stage 0 主循环）
> **目的**：建立 Stage 6 → 下一迭代 Stage 0 的显式闭环。读取 4 类历史产物，避免迭代知识丢失。

```bash
bash $ROOT/.claude/hooks/log-event.sh "00" "$AGENT_NAME" "步骤开始" "读取 Stage 6 闭环产物" "" ""
```

#### 7.1 读取 evolution-proposals（教练提案 + PM 审批）
> 来自阶段 6（coach-stage6 + pm-stage6）的进化提案。若有 Approved 状态，本迭代需落地。

```bash
# 1. 列出所有 evolution-proposals 文件
EVOLUTION_FILES=$(ls $ROOT/.claude/evolution-proposals/*.md 2>/dev/null || echo "")

# 2. 若有提案，PM 必须在 session-status.md 记录"本迭代进化项"小节
if [ -n "$EVOLUTION_FILES" ]; then
    echo "[PM-Stage0] 发现 $(echo "$EVOLUTION_FILES" | wc -l) 个 evolution-proposal"
    for f in $EVOLUTION_FILES; do
        STATUS=$(grep -E "^- \[ \]|^- \[x\]" "$f" | head -3)
        echo "[PM-Stage0] 提案：$(basename $f) | 状态：$STATUS"
    done
fi
```

**AI 操作**：
1. Read 工具 `.claude/evolution-proposals/*.md`（教练提案 + PM 审批）
2. 识别 Approved 状态的提案
3. 在 session-status.md 的 `## 实验规则/技能加载记录` 章节追加"本迭代进化项"小节
4. 把待落地的实验项纳入本迭代的迭代计划

#### 7.2 读取上一迭代 retrospective（复盘 + 改进模式）
> 来自 pm-stage6 的迭代复盘，含技术债务、缺陷趋势、改进建议

```bash
# 读取 sprint-latest 的复盘
RETRO_FILE="$ROOT/.claude/iterations/sprint-latest/iteration-retrospective.md"
if [ -f "$RETRO_FILE" ]; then
    echo "[PM-Stage0] 读取上一迭代复盘：$RETRO_FILE"
    # 提取关键章节
    grep -E "^## " "$RETRO_FILE" | head -20
else
    echo "[PM-Stage0] ⚠️ 暂无 sprint-latest/iteration-retrospective.md（首次迭代或未完成 stage 6）"
fi

# 读取最近归档 sprint 的复盘
LATEST_SPRINT=$(ls -dt $ROOT/.claude/iterations/sprint-* 2>/dev/null | head -1)
if [ -n "$LATEST_SPRINT" ] && [ -f "$LATEST_SPRINT/iteration-retrospective.md" ]; then
    echo "[PM-Stage0] 读取最近归档复盘：$LATEST_SPRINT/iteration-retrospective.md"
    grep -E "^## " "$LATEST_SPRINT/iteration-retrospective.md" | head -20
fi
```

**AI 操作**：
1. Read 工具 `.claude/iterations/sprint-latest/iteration-retrospective.md`（本迭代复盘，可能不存在）
2. Read 工具 `.claude/iterations/sprint-*/iteration-retrospective.md`（最近归档的 sprint 复盘）
3. 提取"待改进模式"和"技术债务"章节
4. 把改进项纳入 session-status.md 的 `## 异常记录` 或本迭代的 feature 列表

#### 7.3 读取 PROJECT_STATUS.md（全局视角）
> 来自 pm-stage6 步骤 4 的全局状态报告

```bash
STATUS_FILE="$ROOT/reports/PROJECT_STATUS.md"
if [ -f "$STATUS_FILE" ]; then
    echo "[PM-Stage0] 读取项目状态：$STATUS_FILE"
    grep -E "^## " "$STATUS_FILE" | head -20
else
    echo "[PM-Stage0] ⚠️ 暂无 reports/PROJECT_STATUS.md（首次迭代或未完成 stage 6）"
fi
```

**AI 操作**：
1. Read 工具 `reports/PROJECT_STATUS.md`（项目全局状态）
2. 提取"项目健康度"、"技术债务总览"、"下一迭代建议"章节
3. 把建议纳入本迭代的 feature 优先级

#### 7.4 记录闭环读取结果

在 `session-status.md` 追加：

```markdown
## Stage 6 闭环读取记录

| 产物 | 路径 | 状态 | 关键摘要 |
|------|------|------|---------|
| evolution-proposals | `.claude/evolution-proposals/*.md` | ✅/⏳ N 项 | （摘要） |
| iteration-retrospective | `.claude/iterations/sprint-*/iteration-retrospective.md` | ✅/⏳ | （摘要） |
| PROJECT_STATUS | `reports/PROJECT_STATUS.md` | ✅/⏳ | （摘要） |
```

```bash
bash $ROOT/.claude/hooks/log-event.sh "00" "$AGENT_NAME" "步骤完成" "读取 Stage 6 闭环产物" "" "成功"
```

---

### 操作 0.8：输出阶段摘要

#### 8.1 输入（Inputs）
| 输入 | 来源 | 用途 |
|------|------|------|
| graphify-out/ | `$ROOT/graphify-out/` | 提供项目信息和技术栈数据 |
| session-status.md | `.claude/iterations/session-status.md` | 读取已完成状态，汇总产出物 |
| project.md | `.claude/context/project.md`（如已生成） | 读取项目信息 |
| tech-stack-profile.md | `.claude/context/tech-stack-profile.md`（如已生成） | 读取技术栈统计 |
| feature-elements.md | `.claude/context/feature-elements.md`（如已生成） | 读取功能元素清单 |

#### 8.2 输出（Outputs）
| 输出 | 目的地 | 说明 |
|------|--------|------|
| 阶段摘要文本 | 控制台/用户消息 | 三句话摘要 + 下一步建议 |
| [Human Gate] 请求 | 用户确认 | 等待用户批准继续 |

#### 8.3 执行步骤
1. 汇总本次阶段完成情况：
   - 从 session-status.md 读取产出物状态
   - 从 project.md（如存在）读取项目基本信息
   - 从 tech-stack-profile.md（如存在）读取技术栈统计
2. 生成三句话摘要：
   - 知识图谱验证结果
   - 产出物生成情况（project.md / tech-stack-profile.md）
   - 依赖全景状态
3. 报告下一步建议（进入阶段 1 的前置条件）

示例：
```
[PM-Stage0] 阶段 0 完成摘要：
- 知识图谱：✅ 验证通过，已加载项目信息
- 产出物：session-status.md ✅ | project.md ✅ | tech-stack-profile.md ✅ | feature-elements.md ✅
- 下一步建议：确认是否进入阶段 1（需求澄清）

下一步：请确认是否继续进入下一个步骤：架构师分析Tech consistency或需要补充其他信息。
```

#### 8.4 Human Gate 确认
> 在输出阶段摘要后，必须等待用户确认才能结束 PM-Stage0

**等待用户确认以下内容**：
1. 知识图谱验证是否通过
2. 迭代目录结构（sprint-latest/）是否正确
3. session-status.md 状态是否正确
4. project.md、tech-stack-profile.md 和 feature-elements.md 生成是否完整
5. 是否允许 Architect-Stage0 开始执行

**回复选项**：
- `继续` - 允许 Architect-Stage0 开始执行
- `补充` - 需要补充信息，列出需要补充的内容
- `暂停` - 暂停阶段 0，等待进一步指示

**超时处理**：如果用户未在规定时间内回复，PM Agent 应记录为"待确认"状态并等待。

```bash
bash $ROOT/.claude/hooks/log-event.sh "00" "$AGENT_NAME" "等待" "Human Gate 确认" "" "待回复"
```

---

## 异常处理

| 异常场景 | 处理方式 |
|---------|---------|
| 知识图谱不存在 | 退出 Sub Agent，提示用户先生成知识图谱 |
| 迭代目录创建失败 | 报错退出，检查目录权限 |
| session-status.md 生成失败 | 报错退出，检查文件权限 |
| project.md 生成失败 | 报错退出，检查写入权限 |
| tech-stack-profile.md 生成失败 | 报错退出，检查写入权限 |
| feature-elements.md 生成失败 | 报错退出，检查写入权限 |
| SCENARIO 未定义 | 报错退出 |

---

## 关联文档

| 文档 | 路径 | 说明 |
|------|------|------|
| session-status-template.md | `.claude/templates/session-status-template.md` | session-status 模板 |
| project-template.md | `.claude/templates/project-template.md` | project.md 模板 |
| tech-stack-profile-template.md | `.claude/templates/tech-stack-profile-template.md` | tech-stack-profile 模板 |
| feature-elements-template.md | `.claude/templates/feature-elements-template.md` | feature-elements 模板 |
| mf-upgrade:00-init.md | `.claude/commands/mf-upgrade:00-init.md` | 阶段 0 完整 playbook |
| architect-stage0.md | `.claude/agents/architect-stage0.md` | 架构师阶段 0 操作 |