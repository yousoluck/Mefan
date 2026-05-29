# Stage 4 Hook 增强方案

## 设计目标

1. **状态可视化** — 追踪 7 状态流转，防止非法状态跃迁
2. **ADR 伪代码对照** — 确保实现严格按 ADR 意图
3. **参考模块合规** — 新代码必须遵循参考模块模式
4. **TDD 节奏验证** — 红→绿→重构循环完整
5. **快速失败** — 简单错误在 hook 层阻断，不进入 Agent 审查

## 增强后的 Hook 架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Hook Layer (脚本)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ check-state  │  │ check-adr    │  │ check-ref    │      │
│  │ _machine.sh  │  │ _impl.sh     │  │ _consistency  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ check-tdd   │  │ check-test   │  │ check-arch   │      │
│  │ _rhythm.sh   │  │ _coverage.sh │  │ _contract.sh │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
├─────────────────────────────────────────────────────────────┤
│                    Guardian Layer (Agent)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Architect    │  │ QA           │  │ PM           │      │
│  │ Agent        │  │ Agent        │  │ Agent        │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

## 新增 Hook 清单

### 1. check-state-machine.sh

**职责**：验证 MG 状态流转合法性

```bash
# 用法: bash .claude/hooks/check-state-machine.sh <MG_ID> <expected_state>
# 退出码: 0=合法, 1=非法状态, 2=文件缺失

# 合法的状态流转
declare -A VALID_TRANSITIONS=(
  ["To Do"]="In Progress"
  ["In Progress"]="Self-Check"
  ["Self-Check"]="Code Review"
  ["Self-Check"]="In Progress"      # 打回
  ["Code Review"]="QA-Test-Coding"
  ["Code Review"]="In Progress"      # 打回
  ["QA-Test-Coding"]="Test Code Review"
  ["QA-Test-Coding"]="In Progress"    # 打回
  ["Test Code Review"]="Testing"
  ["Test Code Review"]="QA-Test-Coding" # 打回
  ["Testing"]="Close"
  ["Testing"]="In Progress"          # 打回
)

# 检查 sprint-status.md 中的 US 状态是否与 expected_state 匹配
# 检查是否有非法跃迁（如从 Dev 直接跳到 Close）
```

**触发时机**：
- 每次 Dev 完成一个阶段，准备进入下一个状态时
- Self-Check 开始时
- Code Review 开始时

---

### 2. check-adr-implementation.sh

**职责**：检查关键实现是否按 ADR 伪代码执行

```bash
# 用法: bash .claude/hooks/check-adr-implementation.sh <MG_ID>
# 检查内容：
# 1. ADR 中声明的"关键步骤"是否实现
# 2. 伪代码中的方法名/函数签名是否存在
# 3. 伪代码中的条件分支逻辑是否覆盖

# 读取 ADR.md 中该 MG 的 task 伪代码
# 对每个 task：
#   - 提取伪代码中的函数调用模式
#   - 在实现代码中搜索这些模式
#   - 报告缺失的实现
```

**关键检查点**：
- 方法名匹配（ADR 伪代码 vs 实际实现）
- 条件判断逻辑（if/else 分支覆盖）
- 异常处理模式（try/catch 是否按 ADR）

---

### 3. check-reference-consistency.sh

**职责**：确保新代码遵循参考模块的命名/结构

```bash
# 用法: bash .claude/hooks/check-reference-consistency.sh <file_path>
# 读取 consistency-baseline.md 中该模块类型对应的参考模块
# 对比 file_path 与参考模块的：
#   - 文件命名模式
#   - 类/函数命名模式
#   - 目录结构
#   - 注释风格

# 输出违规列表
```

**检查维度**：
- 文件名： snake_case vs camelCase vs PascalCase
- 类名： 前缀/后缀约定
- 方法名： 动词前缀约定（get, set, create, update）
- 错误处理： 是否使用相同的异常类型

---

### 4. check-tdd-rhythm.sh

**职责**：验证 TDD 红→绿→重构循环是否完整

```bash
# 用法: bash .claude/hooks/check-tdd-rhythm.sh <MG_ID>
# 检查规则：

# 1. RED 阶段：必须有对应的 test 文件但实现为空/仅抛异常
# 2. GREEN 阶段：实现必须让测试通过
# 3. REFACTOR 阶段：重构后测试仍然通过

# 检查模式：
# - 存在 test 文件但无实现 → RED 未完成
# - 实现代码但无对应测试 → 跳过 RED
# - 测试通过后仍无重构标记 → 缺少 REFACTOR
```

**失败场景**：
- 有 `*.test.ts` 但对应的实现文件不存在
- 实现文件被修改但测试未同步更新
- 缺少 `// REFACTOR:` 注释标记重构节点

---

### 5. check-test-coverage.sh

**职责**：验证关键模块的测试覆盖

```bash
# 用法: bash .claude/hooks/check-test-coverage.sh <MG_ID> [threshold]
# 默认阈值: 80%

# 统计：
# - 测试文件数 / 实现文件数
# - 测试函数数 / 实现函数数
# - 关键路径（如 API endpoint）是否有测试覆盖

# 报告格式：
# {
#   "coverage": 75,
#   "threshold": 80,
#   "failed_files": ["src/auth.py"],
#   "status": "FAIL"
# }
```

---

### 6. check-arch-contract.sh

**职责**：验证架构契约是否被遵守

```bash
# 用法: bash .claude/hooks/check-arch-contract.sh
# 检查：
# - 模块间依赖是否符合 ADR 中的依赖关系图
# - 是否有环形依赖
# - 公共 API 是否有不兼容变更

# 读取 ADR 中的"模块依赖"章节
# 遍历所有 import 语句，验证依赖方向
```

---

## Hook 触发时机

| Hook | Dev | Self-Check | Code Review | QA-Test-Coding | Test Code Review | Testing | Close |
|------|-----|------------|------------|----------------|-----------------|---------|-------|
| check-state-machine | ✅进入时 | ✅进入时 | ✅进入时 | ✅进入时 | ✅进入时 | ✅进入时 | ✅进入时 |
| check-adr-impl | ✅离开时 | - | ✅离开时 | - | - | - | - |
| check-ref-consistency | ✅实现时 | ✅检查时 | ✅检查时 | - | - | - | - |
| check-tdd-rhythm | ✅完成后 | - | - | ✅完成后 | - | - | - |
| check-test-coverage | - | ✅完成后 | - | ✅完成后 | ✅完成后 | ✅完成后 | - |
| check-arch-contract | - | - | ✅离开时 | - | ✅完成后 | - | ✅完成后 |

---

## 状态文件设计

创建一个状态追踪文件 `.claude/iterations/sprint-latest/mg-state.json`：

```json
{
  "MG-001": {
    "current_state": "Code Review",
    "state_history": [
      {"state": "In Progress", "entered_at": "2026-05-29T10:00:00"},
      {"state": "Self-Check", "entered_at": "2026-05-29T12:00:00"},
      {"state": "Code Review", "entered_at": "2026-05-29T14:00:00"}
    ],
    "violations": [],
    "last_check": "2026-05-29T14:30:00"
  }
}
```

---

## 与现有 Hook 的整合

### 现有 Hook（保留）

| Hook | 保留原因 |
|------|---------|
| `log-event.sh` | 通用日志，所有阶段都需要 |
| `check-consistency.py` | 基础静态检查（console.log、密钥） |
| `stage4-self-check.sh` | 触发 Self-Check 的入口脚本 |
| `enforce-diff-limit.sh` | 增量大小硬限制 |

### 现有 Hook（增强）

| Hook | 增强内容 |
|------|---------|
| `pre-commit.sh` | 增加 `check-state-machine.sh` 调用 |
| `pre-merge-check.sh` | 增加 `check-arch-contract.sh` 调用 |

---

## 实施状态

### ✅ 已实现（P0）

1. **`check-state-machine.sh`** — 防止非法状态跃迁
   - 验证 7 状态流转合法性
   - 更新 `mg-state.json` 状态追踪文件
   - 已融入 `dev-stage4.md`、`architect-stage4.md`、`qa-stage4.md`

2. **`check-adr-implementation.sh`** — 确保按 ADR 伪代码实现
   - 检查关键函数/方法是否实现
   - 检查模块路径是否存在
   - 已融入 `mf-upgrade:04-implement.md` 步骤 2.1

3. **`check-reference-consistency.sh`** — 参考模块命名/结构合规
   - 检查文件命名（snake_case vs camelCase）
   - 检查目录命名规范
   - 已融入 `mf-upgrade:04-implement.md` 步骤 2.1

4. **`mg-state.json`** — 状态追踪文件
   - 记录每个 MG 的当前状态和历史
   - 被 `check-state-machine.sh` 读写

### ✅ 已实现（P1）

5. **`check-tdd-rhythm.sh`** — 验证 TDD 红→绿→重构循环
   - 检查测试文件覆盖率
   - 检查 RED/GREEN 阶段标记
   - 已融入 `mf-upgrade:04-implement.md` 步骤 2.2

6. **`check-test-coverage.sh`** — 验证关键模块测试覆盖
   - 统计实现文件/测试文件数量
   - 计算覆盖率是否达标（默认 80%）
   - 已融入 `qa-stage4.md` 操作 6

### 📋 已融入的文件

| 文件 | 融入位置 |
|------|---------|
| `mf-upgrade:04-implement.md` | 步骤 2.1（Dev）、步骤 2.2（Self-Check） |
| `dev-stage4.md` | 操作 4.1（状态转换门禁）、操作 6（进入 Code Review） |
| `architect-stage4.md` | 操作 2.1（Code Review 前置验证）、操作 4（输出报告前验证） |
| `qa-stage4.md` | 操作 6（Testing 完成门禁） |
| `install-hooks.sh` | 新增 5 个 hook 的可执行权限设置 |

### ⏳ 待实现（P2）

7. **`check-arch-contract.sh`** — 验证架构契约（模块依赖关系）
   - 读取 ADR 中的依赖关系图
   - 验证无环形依赖
   - 验证无不兼容变更

## 三层防御融入总结

```
┌──────────────────────────────────────────────────────────────────┐
│                        7 状态流转 + Hook                         │
│                                                                  │
│  🏃 Dev → 🔍 Self-Check → 🖥️ Code Review → 🧪 QA-Test-Coding    │
│          │                │                │                     │
│          ↓                ↓                ↓                     │
│    check-state-    check-state-     check-state-                 │
│    machine.sh      machine.sh       machine.sh                   │
│          │                │                │                     │
│          │         check-adr-impl.sh      │                     │
│          │                │                │                     │
│          ↓                ↓                ↓                     │
│    check-tdd-       check-ref-       check-tdd-                   │
│    rhythm.sh        consistency.sh   rhythm.sh                    │
│          │                │                │                     │
│          ↓                ↓                ↓                     │
│   🖥️ Code Review → 🧪 QA-Test-Coding → 🔬 Test Code Review        │
│         │                      │                │               │
│         ↓                      ↓                ↓               │
│   check-state-           check-state-      check-state-         │
│   machine.sh             machine.sh        machine.sh           │
│         │                      │                │               │
│         │             check-test-           check-arch-        │
│         │             coverage.sh           contract.sh         │
│         │                      │                │               │
│         ↓                      ↓                ↓               │
│   🔬 Test Code Review → ✅ Testing → 🎉 Close                     │
│         │                      │                │               │
│         ↓                      ↓                ↓               │
│   check-arch-          check-test-         check-arch-         │
│   contract.sh          coverage.sh         contract.sh          │
└──────────────────────────────────────────────────────────────────┘
```

**Hook 触发时机矩阵**：

| Hook | Dev→Self | Self→CodeReview | CodeReview→QA | QA→TestCodeReview | TestCodeReview→Test | Test→Close |
|------|----------|-----------|---------|-------------|---------------|------------|
| check-state-machine | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| check-adr-implementation | ✅ | - | ✅ | - | - | - |
| check-reference-consistency | ✅ | - | - | - | - | - |
| check-tdd-rhythm | - | ✅ | - | - | - | - |
| check-test-coverage | - | - | - | - | ✅ | ✅ |
| check-arch-contract | - | - | ✅ | - | - | ✅ |

---

## 示例：check-state-machine.sh 实现

```bash
#!/bin/bash
# check-state-machine.sh - 验证 MG 状态流转合法性
set -e

ROOT="/mnt/d/pycharmprojects/Mefan"
MG_ID="${1:-MG-001}"
EXPECTED_STATE="${2:-}"
SPRINT_STATUS="$ROOT/.claude/iterations/sprint-latest/sprint-status.md"
STATE_FILE="$ROOT/.claude/iterations/sprint-latest/mg-state.json"
LOG_FILE="iterations/mefan-log.md"

echo "[check-state-machine] 检查 MG $MG_ID 状态..."

# 读取当前状态（从 sprint-status.md 或 mg-state.json）
CURRENT_STATE=$(grep -A5 "MG-$MG_ID" "$SPRINT_STATUS" 2>/dev/null | grep "状态" | head -1 | awk -F':' '{print $2}' | tr -d ' ')

if [ -z "$CURRENT_STATE" ]; then
    echo "[check-state-machine] 错误：无法读取 MG $MG_ID 当前状态"
    exit 2
fi

echo "[check-state-machine] MG $MG_ID 当前状态: $CURRENT_STATE"

# 如果指定了 expected_state，验证是否匹配
if [ -n "$EXPECTED_STATE" ]; then
    if [ "$CURRENT_STATE" != "$EXPECTED_STATE" ]; then
        echo "[check-state-machine] 错误：状态不匹配。期望: $EXPECTED_STATE, 实际: $CURRENT_STATE"
        exit 1
    fi
fi

# 定义合法流转
declare -A VALID_TRANSITIONS=(
    ["ToDo"]="InProgress"
    ["InProgress"]="SelfCheck"
    ["SelfCheck"]="CodeReview"
    ["SelfCheck"]="InProgress"
    ["CodeReview"]="QATestCoding"
    ["CodeReview"]="InProgress"
    ["QATestCoding"]="TestCodeReview"
    ["QATestCoding"]="InProgress"
    ["TestCodeReview"]="Testing"
    ["TestCodeReview"]="QATestCoding"
    ["Testing"]="Close"
    ["Testing"]="InProgress"
)

# 获取上一步状态（从 state_history 最后一条）
PREVIOUS_STATE=$(python3 -c "
import json
try:
    with open('$STATE_FILE', 'r') as f:
        data = json.load(f)
        if '$MG_ID' in data and data['$MG_ID']['state_history']:
            return data['$MG_ID']['state_history'][-1]['state']
except: pass
    return ''
" 2>/dev/null || echo "")

if [ -n "$PREVIOUS_STATE" ]; then
    # 验证流转是否合法
    KEY="${PREVIOUS_STATE}${CURRENT_STATE}"
    if [[ ! -v VALID_TRANSITIONS["$KEY"] ]]; then
        echo "[check-state-machine] 错误：非法状态流转 $PREVIOUS_STATE → $CURRENT_STATE"
        echo "[check-state-machine] 允许的下一个状态: ${VALID_TRANSITIONS[$PREVIOUS_STATE]}"
        exit 1
    fi
    echo "[check-state-machine] 状态流转合法: $PREVIOUS_STATE → $CURRENT_STATE"
fi

# 更新 state 文件
python3 -c "
import json, os
from datetime import datetime

state_file = '$STATE_FILE'
mg_id = '$MG_ID'
current_state = '$CURRENT_STATE'

data = {}
if os.path.exists(state_file):
    with open(state_file, 'r') as f:
        data = json.load(f)

if mg_id not in data:
    data[mg_id] = {'current_state': '', 'state_history': [], 'violations': [], 'last_check': ''}

data[mg_id]['current_state'] = current_state
data[mg_id]['state_history'].append({
    'state': current_state,
    'entered_at': datetime.now().isoformat()
})
data[mg_id]['last_check'] = datetime.now().isoformat()

with open(state_file, 'w') as f:
    json.dump(data, f, indent=2)
" 2>/dev/null

echo "[check-state-machine] 状态检查通过"
exit 0
```

---

## 总结

增强后的 Hook 系统：

| 层级 | 数量 | 职责 |
|------|------|------|
| **Hook Layer** | 6 个新增 + 4 个保留 | 快速失败，阻断简单错误 |
| **Guardian Layer** | 3 个 Agent | 深度语义审查，推理判断 |
| **Human Gate** | 1 个 | 最终审批，特殊决策 |

总代码量：约 1500 行（Hook 脚本）+ 现有 Agent（不变）

是否需要我立即实现这些 hook？