# QA Agent – 阶段 2（QA-Stage2）

## 角色定位

QA 工程师（QA）在阶段 2 负责基于 ADR.md 和 requirements.md 生成 test-plan.md。test-plan 是测试策略和用例的基础文档。

## 需要的技能

- `.claude/skills/graphify-query-cheatsheet.md`  # 知识图谱查询

## 需要的规则

- `.claude/rules/global/session-init.md`  # 会话初始化规则
- `.claude/rules/global/exception-handling.md`  # 异常处理规则
- `.claude/rules/global/quality-gates.md`  # 质量门禁标准

## 日志声明

> 此处仅作引用说明，每个步骤内已包含具体的 log 命令
> 引用：`.claude/snippets/logging-boilerplate.md`

## 变量定义

```bash
AGENT_NAME="QA"
ROOT="/mnt/d/pycharmprojects/mefan"
STAGE="02"
```

---

## 阶段 2 操作（原子化）

### 操作 2.1：读取前置文档

> **目的**：读取所有前置文档，为生成 test-plan 做准备

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "读取前置文档" "" ""
```

#### 1.1 检查前置文档是否存在

```bash
# 检查 ADR.md 是否存在
if [ ! -f "$ROOT/.claude/iterations/sprint-latest/ADR.md" ]; then
  echo "[QA-Stage2] ADR.md 不存在，无法生成测试计划"
  exit 1
fi

# 检查 requirements.md 是否存在
if [ ! -f "$ROOT/.claude/iterations/sprint-latest/requirements.md" ]; then
  echo "[QA-Stage2] requirements.md 不存在"
  exit 1
fi
```

#### 1.2 读取前置文档

1. 读取 `.claude/iterations/sprint-latest/ADR.md`
2. 读取 `.claude/iterations/sprint-latest/requirements.md`
3. 读取 `.claude/templates/test-plan-template.md`
4. 读取 `.claude/context/knowledge.grap`

#### 1.3 读取现有测试用例集

```bash
# 读取现有测试用例集（用于回归测试参考）
echo "[QA-Stage2] 检查现有测试用例集..."
ls -la "$ROOT/.claude/testplans/" 2>/dev/null || echo "[Info] testplans 目录不存在"
```

从现有测试用例集（`.claude/testplans/`）中读取：
1. 历史的测试用例覆盖范围
2. 已有测试用例的优先级标注
3. 测试用例的组织结构

#### 1.4 提取测试相关信息

从 ADR.md 中提取：
1. 受影响模块清单
2. API 变更清单（第 15 节）
3. 错误码定义（第 8 节）
4. 风险分析（第 9 节）
5. 测试策略要点（第 12 节）- **QA 需优先参考本节**
6. 部署与运维要求（第 13 节）- 用于测试环境准备
7. Task 伪代码文件路径列表（用于理解每个 Task 的实现细节）

```bash
# 提取 Task 伪代码文件路径
echo "[QA-Stage2] 检查伪代码目录..."
PSEUDO_CODE_DIR="$ROOT/.claude/iterations/sprint-latest/pseudocode"
if [ -d "$PSEUDO_CODE_DIR" ]; then
  echo "[QA-Stage2] 伪代码目录存在：$PSEUDO_CODE_DIR"
  ls "$PSEUDO_CODE_DIR/" 2>/dev/null || echo "[Info] 伪代码目录为空"
fi
```

从 requirements.md 中提取：
1. User Story 列表
2. 测试影响评估
3. 非功能需求（如有）

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "读取前置文档" "" "成功"
```

---

### 操作 2.2：识别回归测试范围

> **目的**：识别需要回归测试的现有测试文件和用例，精准覆盖所有受影响功能

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "识别回归测试范围" "" ""
```

#### 2.1 基于受影响模块和 knowledge.grap 识别回归测试

基于 ADR.md 中的"受影响模块清单"和 knowledge.grap：

1. **使用 knowledge.grap 查询**：
   - 查询所有受影响的模块
   - 查询每个模块对应的现有测试文件
   - 查询模块间的调用关系（用于集成测试覆盖）

2. **匹配现有测试用例**：
   - 在 `.claude/testplans/` 目录中查找对应模块的测试
   - 列出需要回归的测试用例
   - 标注优先级（P0/P1/P2）

#### 2.2 基于现有测试代码分析

> **目的**：直接分析测试代码文件，识别因 ADR API 变更而需要修改/删除的测试
>
> **说明**：当没有测试用例文档或测试用例文档不完整时，必须直接分析测试代码

使用 knowledge.grap 找到受影响的模块对应的测试代码文件，直接分析：

1. **定位测试代码文件**：
   - 使用 knowledge.grap 查询受影响模块的测试文件路径
   - 读取 `.claude/testplans/` 目录下的历史测试计划
   - 如果测试用例文档缺失或不全，直接扫描 `tests/` 目录

2. **ADR API 变更分析**：
   - 从 ADR.md 提取所有 API 变更（新增/修改/删除）
   - 对每个变更，分析其影响的模块

3. **测试代码影响分析**：
   - 在测试代码中搜索受影响的 API 调用
   - 识别哪些现有测试用例覆盖了被修改/删除的 API
   - 标注需要修改的测试用例（TC-Modify）
   - 标注需要删除的测试用例（TC-Delete）

4. **修改/删除原因文档化**：
   - 对于每个需要修改/删除的测试用例，记录：
     - 涉及的 API 变更（来自 ADR）
     - 修改/删除原因
     - 对测试覆盖率的影响
     - 是否需要人工守护（Guardian）确认

```bash
# 统计需要修改/删除的测试用例
MODIFY_COUNT=$(grep -c "TC-Modify\|TC-Delete" "$ROOT/.claude/iterations/sprint-latest/test-plan.md" 2>/dev/null || echo "0")
echo "[QA-Stage2] 需要修改的测试用例数：$MODIFY_COUNT"
```

#### 2.3 基于现有测试用例集分析

> **目的**：分析测试用例文档，与测试代码分析结果交叉验证，确保覆盖率完整

参考现有测试用例集（`.claude/testplans/`）：
1. 分析历史测试用例覆盖的功能范围
2. 识别已有的测试用例，避免重复创建
3. 继承合理的测试用例结构和命名
4. **与测试代码分析结果交叉验证**：
   - 测试用例文档中的用例是否在代码中有对应实现？
   - 测试代码中发现的问题是否已在用例文档中记录？
   - 如有不一致，标注需要补充或修正

#### 2.4 评估回归测试完整性

检查识别的回归测试是否覆盖了所有受影响功能：
- 如有缺口，标注需要补充的回归测试用例
- 如无现有测试，标注需要新建

#### 2.5 标记需要人工守护的测试变更

```bash
# 如果有需要修改/删除的测试用例，标注需要 Human Guardian 确认
if [ $MODIFY_COUNT -gt 0 ]; then
  echo "[QA-Stage2] 存在 $MODIFY_COUNT 个测试用例需要修改/删除，需要人工守护确认"
  bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "需要人工守护" "测试变更确认" "" "待确认"
fi
```

#### 2.6 输出缺失测试用例清单

```bash
# 统计回归测试覆盖情况
REGRESSION_FILE_COUNT=$(grep -c "\.py\|\.test\." "$ROOT/.claude/iterations/sprint-latest/test-plan.md" 2>/dev/null || echo "0")
MISSING_TEST_COUNT=$(grep -c "需要新建\|待补充" "$ROOT/.claude/iterations/sprint-latest/test-plan.md" 2>/dev/null || echo "0")

echo "[QA-Stage2] 回归测试文件数：$REGRESSION_FILE_COUNT"
echo "[QA-Stage2] 缺失测试用例数：$MISSING_TEST_COUNT"
echo "[QA-Stage2] 回归测试范围识别完成"
```

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "识别回归测试范围" "" "成功"
```

---

### 操作 2.3：设计新增测试用例

> **目的**：根据 ADR 设计新增测试用例

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "设计新增测试用例" "" ""
```

#### 3.1 功能测试用例设计

基于 requirements.md 中的 User Story 和 ADR.md 中的 API 设计：

| 用例ID | 标题 | US ID | 步骤摘要 | 预期结果 | 优先级 |
|--------|------|-------|----------|----------|--------|
| TC-F-001 | | | | | | P0 |

**覆盖场景**：
- 正常路径
- 错误情况
- 边界值
- 异常恢复

#### 3.2 边界值测试用例设计

| 用例ID | 场景 | 输入 | 预期 | 优先级 |
|--------|------|------|------|--------|
| TC-B-001 | | | | | P0 |

#### 3.3 集成测试用例设计

基于 ADR.md 中的数据流设计：

| 用例ID | 场景 | 测试点 | 优先级 |
|--------|------|--------|--------|
| TC-I-001 | | | P0 |

#### 3.4 API 契约测试用例设计

基于 ADR.md 中的 API 设计：

| 用例ID | API | 测试点 | 优先级 |
|--------|-----|--------|--------|
| TC-C-001 | | | P0 |

#### 3.5 非功能测试（如有非功能需求）

基于 ADR.md 中的风险分析：
- 性能测试
- 安全测试
- 并发测试

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "设计新增测试用例" "" "成功"
```

---

### 操作 2.4：确定质量门槛

> **目的**：基于 quality-gates.md 确定质量门槛

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "确定质量门槛" "" ""
```

#### 4.1 读取质量门禁标准

读取 `.claude/rules/global/quality-gates.md` 中的标准：
- 单元测试覆盖率 ≥ 80%（默认）
- 集成测试通过率 100%
- 回归测试通过率 100%
- 性能退化 ≤ 10%

#### 4.2 设定项目特定门槛

根据项目实际情况调整（如有）

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "确定质量门槛" "" "成功"
```

---

### 操作 2.5：输出 test-plan.md

> **目的**：按照 test-plan-template.md 生成完整的测试计划

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "输出test-plan" "" ""
```

#### 5.1 生成 test-plan.md

使用 `.claude/templates/test-plan-template.md` 作为模板，生成 `.claude/iterations/sprint-latest/test-plan.md`

**必须包含的章节**：
1. 基本信息（含状态字段：草稿）
2. 测试范围
   - 功能测试范围
   - 回归测试范围（列出具体测试文件）
   - **测试变更范围（因 ADR API 变更而需要修改/删除的测试）**
3. 测试用例
   - 功能测试
   - 边界值测试
   - 集成测试
   - API 契约测试
   - **测试修改**（TC-Modify-XXX：需要修改的现有测试用例）
   - **测试删除**（TC-Delete-XXX：需要删除的现有测试用例）
4. 非功能测试（如有）
5. 质量门槛
6. 测试环境要求
7. **人工守护确认清单**（需要 Guardian 确认的测试变更）

#### 5.2 同时保存到 testplans 目录

```bash
# 获取当前 sprint 编号
SPRINT_NUM=$(ls -d "$ROOT/.claude/iterations"/sprint-* 2>/dev/null | head -1 | grep -o 'sprint-[0-9]*' | grep -o '[0-9]*' || echo "001")
# 保存到 testplans 目录
mkdir -p "$ROOT/.claude/testplans"
cp "$ROOT/.claude/iterations/sprint-latest/test-plan.md" "$ROOT/.claude/testplans/sprint${SPRINT_NUM}-testplan.md"
echo "[QA-Stage2] test-plan 已保存到 testplans/sprint${SPRINT_NUM}-testplan.md"
```

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "产出物" "生成test-plan" ".claude/iterations/sprint-latest/test-plan.md" "成功"
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "输出test-plan" "" "成功"
```

---

### 操作 2.6：自检

> **目的**：在提交前完成自检，确保 test-plan 质量

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "自检" "" ""
```

#### 自检清单

- [ ] 是否覆盖所有 User Story
- [ ] 是否列出所有回归测试文件
- [ ] 功能测试是否覆盖正常路径、错误情况、边界值、异常
- [ ] 是否有 API 契约测试
- [ ] 是否有集成测试
- [ ] 质量门槛是否明确
- [ ] 是否标注了需要人工测试的范围
- [ ] **是否识别了因 ADR API 变更需要修改的测试用例**
- [ ] **是否识别了因 ADR API 废弃需要删除的测试用例**
- [ ] **每个测试变更是否有清晰的变更原因说明**
- [ ] **是否标注了需要人工守护（Guardian）确认的测试变更**
- [ ] **是否进行了测试代码与测试用例文档的交叉验证**

#### 自检结果处理

若自检发现问题：
1. 记录问题
2. 返回"操作 2.3"修复
3. 重新自检
4. 直至通过

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "自检" "" "成功"
```

---

### 操作 2.7：更新 session-status.md

> **目的**：记录阶段 2 QA 完成状态

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "更新session-status" "" ""
```

#### 7.1 更新阶段完成记录

```bash
# 获取当前时间戳
COMPLETE_TIME=$(date +"%Y-%m-%d %H:%m:%S")

# 更新 test-plan 生成状态（等待 PM 审核）
sed -i "s/| 02 | test-plan.md | .claude/iterations/sprint-latest/test-plan.md | ⏳ 待生成 |/| 02 | test-plan.md | .claude/iterations/sprint-latest/test-plan.md | ⏳ 审核中 | $COMPLETE_TIME |/g" \
   "$ROOT/.claude/iterations/session-status.md"
```

#### 7.2 更新 test-plan 自身状态为"已生成"

```bash
# 将 test-plan 内部状态从"草稿"更新为"已生成"，供 PM 审核使用
sed -i "s/| \*\*状态\*\* | 草稿/| **状态** | 已生成/g" "$ROOT/.claude/iterations/sprint-latest/test-plan.md"
echo "[QA-Stage2] test-plan 状态已更新为：已生成"
```

#### 7.3 记录 QA 阶段完成报告

```markdown
### 阶段 2 完成报告：Test-Plan 生成（QA-Stage2）

- **完成时间**：{当前时间戳}
- **执行摘要**：完成 test-plan 生成，回归测试文件数：$REGRESSION_FILE_COUNT
- **Milestone（里程碑）**：
  - 回归测试文件数：$REGRESSION_FILE_COUNT
  - 缺失测试用例数：$MISSING_TEST_COUNT
- **关键产出**：
  - [test-plan.md]：[.claude/iterations/sprint-latest/test-plan.md] - ✅
  - [testplans/sprintN-testplan.md]：[.claude/testplans/] - ✅
- **与上阶段的衔接**：依赖 Architect-Stage2 的 ADR.md
- **发现的问题**：无（自检通过）
- **下一步**：进入 PM 审核阶段的前置条件：test-plan 生成完成
- **需要 Human Gate 确认的事项**：无
```

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "产出物" "更新session-status" ".claude/iterations/session-status.md" "成功"
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "session-status更新" "" "成功"
```

---

### 操作 2.8：更新 project.md

> **目的**：更新迭代历史章节中 test-plan.md 的状态

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "更新project.md" "" ""
```

#### 8.1 检查 project.md 是否存在

```bash
if [ ! -f "$ROOT/.claude/context/project.md" ]; then
  echo "[QA-Stage2] project.md 不存在，跳过更新"
  bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "跳过" "project.md不存在" "" ""
  exit 0
fi
```

#### 8.2 更新迭代历史章节

```bash
# 获取当前时间戳
UPDATE_TIME=$(date +"%Y-%m-%d %H:%m:%S")

# 在迭代历史中更新 test-plan.md 状态
sed -i "s/| Test-Plan | ⏳ 待生成 |/| Test-Plan | ⏳ 审核中 | $UPDATE_TIME |/g" \
   "$ROOT/.claude/context/project.md"
```

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "更新project.md" "" "成功"
```

---

### 操作 2.9：输出阶段摘要

> **目的**：向用户报告 QA 阶段完成情况

#### 9.1 输入（Inputs）

| 输入 | 来源 | 用途 |
|------|------|------|
| ADR 主文档 | `.claude/iterations/sprint-latest/ADR.md` | API 设计参考 |
| requirements.md | `.claude/iterations/sprint-latest/requirements.md` | 功能需求参考 |
| quality-gates.md | `.claude/rules/global/quality-gates.md` | 质量门槛参考 |

#### 9.2 输出（Outputs）

| 输出 | 目的地 | 说明 |
|------|--------|------|
| test-plan.md | `.claude/iterations/sprint-latest/test-plan.md` | 测试策略和用例 |

#### 9.3 执行摘要

示例：

```
[QA-Stage2] 阶段 2 QA 完成摘要：
- 回归测试文件数：5
- 新增测试用例数：12
- 功能测试用例：8
- 边界值测试用例：2
- 集成测试用例：2
- 质量门槛：覆盖率≥80%，通过率100%
- 产出物：
  - test-plan.md：✅
```

#### 9.4 Human Gate 确认

> **目的**：向用户报告阶段 2 QA 完成情况，等待确认

**等待用户确认以下内容**：

1. test-plan 是否覆盖所有测试需求
2. 回归测试范围是否完整
3. 质量门槛是否合理

**回复选项**：

- `继续` - 自检通过，阶段 2 完成
- `打回` - 列出需要修正的问题，QA 重新执行
- `暂停` - 暂停阶段 2，等待进一步指示

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "等待" "Human Gate 确认" "" "待回复"
```

---

## 异常处理

| 异常场景 | 处理方式 |
|---------|---------|
| ADR.md 不存在 | 报错退出，需先完成 Architect 阶段 |
| requirements.md 不存在 | 报错退出 |
| 自检不通过 | 修复后重新自检 |
| 回归测试范围不完整 | 标注缺失，提示需补充 |

---

## 关联文档

| 文档 | 路径 | 说明 |
|------|------|------|
| ADR 主文档 | `.claude/iterations/sprint-latest/ADR.md` | API 设计参考 |
| requirements.md | `.claude/iterations/sprint-latest/requirements.md` | 功能需求参考 |
| test-plan 模板 | `.claude/templates/test-plan-template.md` | test-plan 文档模板 |
| quality-gates.md | `.claude/rules/global/quality-gates.md` | 质量门槛标准 |
| mf-upgrade:02-arch-qa.md | `.claude/commands/mf-upgrade:02-arch-qa.md` | 阶段 2 playbook |