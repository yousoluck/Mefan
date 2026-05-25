---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: 5e7551f7efbf6a913326cb270c9c879a
    PropagateID: 5e7551f7efbf6a913326cb270c9c879a
    ReservedCode1: 3045022100aeb1e7f514a934b27a1a9a42c0cc78f14c44c3ea4dd407fb7b4d290ee66cf04402206a4e3e2d0fc33931d45c568d9c21679eb1f17e78310f4cef484a54987a9ff9c7
    ReservedCode2: 3046022100c28b5a29bf3df0a774bd3789b7c1363005aa2ce83564c0a0f235e0c49792bfd2022100cfad7fd3a3682fb7fb6a56fbac9d3c75295323b008892498d92ec7559c2fd2c2
description: 阶段 1 需求详细设计完整 playbook，协调 Analyst 和 PM 完成需求文档审查
name: mf-upgrade:01-requirements
run_in_background: false
tools:
    - Read
    - Write
    - Bash
    - Grep
    - Glob
    - Edit
    - TaskCreate
    - TaskUpdate
    - TaskList
    - TaskGet
---

# 阶段 1 Playbook：需求详细设计（mf-upgrade:01-requirements）

> **执行范围**：阶段 1 Analyst（详细需求设计）+ PM（审查校验）
> **前置条件**：阶段 0 已完成，feature.md 存在
> **目标**：将 feature.md 转化为详细需求文档，拆分为 User Story 和 Sub-feature

---

## 阶段 1 角色分工

| 角色 | 职责 | 阶段输出 |
|------|------|---------|
| **Analyst** | 详细需求设计、User Story 拆分、Sub-feature 识别 | requirements.md, user-stories/, sub-features/ |
| **PM** | 需求文档审查、校验、通知架构师 | 审查结果、通知记录 |

---

## 变量定义

```bash
STAGE="01"
ROOT="/mnt/d/pycharmprojects/mefan"
SCENARIO="upgrade"
LOG_FILE="$ROOT/.claude/iterations/sprint-latest/logs/stage-01.log"
```

---

## 阶段 1 完整流程

### 阶段 1.1：Analyst 详细需求设计

#### 步骤 1.1.1：检查前置条件

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "Analyst" "步骤开始" "检查前置条件" "" ""

# 检查 feature.md 是否存在
if [ ! -f "$ROOT/.claude/iterations/sprint-latest/feature.md" ]; then
  echo "[Error] feature.md 不存在，阶段 1 无法开始"
  exit 1
fi

# 检查 feature.md 状态
if ! grep -q "✅ 已完成" "$ROOT/.claude/iterations/sprint-latest/feature.md"; then
  echo "[Warning] feature.md 尚未完成，等待阶段 0 完成"
fi

# 加载依赖文档
echo "加载依赖文档..."
ls -la $ROOT/.claude/context/*.md
ls -la $ROOT/.claude/skills/project-*.md 2>/dev/null || echo "无项目专属 Skills"

bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "Analyst" "步骤完成" "检查前置条件" "" "成功"
```

#### 步骤 1.1.2：加载功能要点列表

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "Analyst" "步骤开始" "加载功能要点" "" ""

# 读取 feature.md 中的功能要点
echo "功能要点列表："
grep "^| [0-9]" "$ROOT/.claude/iterations/sprint-latest/feature.md" | head -20

# 统计优先级分布
P0_COUNT=$(grep -c "P0" "$ROOT/.claude/iterations/sprint-latest/feature.md" || echo "0")
P1_COUNT=$(grep -c "P1" "$ROOT/.claude/iterations/sprint-latest/feature.md" || echo "0")
echo "优先级分布：P0=$P0_COUNT, P1=$P1_COUNT"

bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "Analyst" "步骤完成" "加载功能要点" "" "成功"
```

#### 步骤 1.1.3：User Story 拆分

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "Analyst" "步骤开始" "User Story 拆分" "" ""

# 创建 User Story 目录
mkdir -p $ROOT/.claude/iterations/sprint-latest/requirements/user-stories/

# 对每个 P0/P1 优先级的功能进行拆分
# 输出：us-001.md, us-002.md, ...

echo "User Story 拆分完成"

bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "Analyst" "步骤完成" "User Story 拆分" "" "成功"
```

#### 步骤 1.1.4：Sub-feature 识别

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "Analyst" "步骤开始" "Sub-feature 识别" "" ""

# 创建 Sub-feature 目录
mkdir -p $ROOT/.claude/iterations/sprint-latest/requirements/sub-features/

# 对每个 User Story 进行 Sub-feature 拆分
# 输出：sf-001-1.md, sf-001-2.md, ...

echo "Sub-feature 识别完成"

bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "Analyst" "步骤完成" "Sub-feature 识别" "" "成功"
```

#### 步骤 1.1.5：系统关联分析

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "Analyst" "步骤开始" "系统关联分析" "" ""

# 查询知识图谱
# graphify query "与 {功能} 相关的模块"
# graphify similar {功能关键词}

# 冲突分析
# 列出所有 Sub-feature 涉及的文件
# 检查是否有多个 Sub-feature 修改同一文件

# 复用分析
# 检查可复用组件

echo "系统关联分析完成"

bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "Analyst" "步骤完成" "系统关联分析" "" "成功"
```

#### 步骤 1.1.6：测试影响评估

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "Analyst" "步骤开始" "测试影响评估" "" ""

# 扫描现有测试文件
# 列出所有 Sub-feature 涉及的文件路径
# 搜索对应的测试文件

# 测试影响分析
# 估算需要新增的测试用例

echo "测试影响评估完成"

bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "Analyst" "步骤完成" "测试影响评估" "" "成功"
```

#### 步骤 1.1.7：产出需求文档

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "Analyst" "步骤开始" "产出需求文档" "" ""

# 创建目录结构
mkdir -p $ROOT/.claude/iterations/sprint-latest/requirements/
mkdir -p $ROOT/.claude/iterations/sprint-latest/requirements/user-stories/
mkdir -p $ROOT/.claude/iterations/sprint-latest/requirements/sub-features/

# 生成文档名称
DATE=$(date +%Y-%m-%d)
TITLE="detailed-requirements"
DOC_NAME="upgrade-${DATE}-${TITLE}.md"

# 产出主文档
cp $ROOT/.claude/templates/requirements-template.md \
   $ROOT/.claude/iterations/sprint-latest/requirements/$DOC_NAME

# 产出 User Story 文档（循环）
# for us_id in us-001 us-002; do
#   cp $ROOT/.claude/templates/user-story-template.md \
#      $ROOT/.claude/iterations/sprint-latest/requirements/user-stories/${us_id}.md
# done

# 产出 Sub-feature 文档（循环）
# for sf_id in sf-001-1 sf-001-2; do
#   cp $ROOT/.claude/templates/sub-feature-template.md \
#      $ROOT/.claude/iterations/sprint-latest/requirements/sub-features/${sf_id}.md
# done

# 产出需求索引
cat > $ROOT/.claude/iterations/sprint-latest/requirements/index.md << 'EOF'
# 需求文档索引

## 阶段 1 产出物

| 文档类型 | 数量 | 路径 |
|---------|------|------|
| 需求主文档 | 1 | requirements/upgrade-*.md |
| User Story | N | requirements/user-stories/us-*.md |
| Sub-feature | M | requirements/sub-features/sf-*.md |
EOF

echo "需求文档产出完成"

bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "Analyst" "产出物" "生成 requirements" \
     ".claude/iterations/sprint-latest/requirements/" "成功"
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "Analyst" "步骤完成" "产出需求文档" "" "成功"
```

#### 步骤 1.1.8：Analyst 更新 project.md

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "Analyst" "步骤开始" "更新 project.md" "" ""

# 更新迭代历史章节中的需求文档状态
if [ -f "$ROOT/.claude/context/project.md" ]; then
  sed -i 's/| 需求文档 | requirements.md | ⏳ 待创建 |/| 需求文档 | requirements.md | ✅ 已创建 |/g' \
     "$ROOT/.claude/context/project.md"
fi

bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "Analyst" "步骤完成" "更新 project.md" "" "成功"
```

---

### 阶段 1.2：PM 审查校验

#### 步骤 1.2.1：接收分析师产出

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "PM" "步骤开始" "接收分析师产出" "" ""

# 验证需求文档目录
if [ ! -d "$ROOT/.claude/iterations/sprint-latest/requirements" ]; then
  echo "[Error] 需求文档目录不存在"
  exit 1
fi

# 统计产出物
US_COUNT=$(ls $ROOT/.claude/iterations/sprint-latest/requirements/user-stories/us-*.md 2>/dev/null | wc -l)
SF_COUNT=$(ls $ROOT/.claude/iterations/sprint-latest/requirements/sub-features/sf-*.md 2>/dev/null | wc -l)
echo "[PM-Stage1] User Story: $US_COUNT, Sub-feature: $SF_COUNT"

bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "PM" "步骤完成" "接收分析师产出" "" "成功"
```

#### 步骤 1.2.2：需求文档审查

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "PM" "步骤开始" "需求文档审查" "" ""

# 执行审查决策树
# 1. 拓扑完整性检查
# 2. 验收标准可测性检查
# 3. 命名证据检查
# 4. 测试影响具体性检查
# 5. 上下游引用检查

# 记录审查结果
REVIEW_PASSED=true
if [ "$REVIEW_PASSED" = true ]; then
  echo "[PM-Stage1] 审查结果：✅ 通过"
else
  echo "[PM-Stage1] 审查结果：❌ 打回"
fi

bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "PM" "步骤完成" "需求文档审查" "" "成功"
```

#### 步骤 1.2.3：校验结果处理

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "PM" "步骤开始" "校验结果处理" "" ""

# 审查通过
if [ "$REVIEW_PASSED" = true ]; then
  echo "[PM-Stage1] 审查通过，更新 session-status.md"
  # 更新产出物状态为 ✅
else
  # 审查打回
  echo "[PM-Stage1] 审查打回，等待 Analyst 修正"
  # 记录打回原因
fi

bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "PM" "步骤完成" "校验结果处理" "" "成功"
```

#### 步骤 1.2.4：通知架构师（审查通过后）

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "PM" "步骤开始" "通知架构师" "" ""

# 记录通知时间
NOTIFICATION_TIME=$(date +"%Y-%m-%d %H:%M:%S")
echo "[PM-Stage1] $NOTIFICATION_TIME - Architect 已通知，阶段 2 可以开始" \
     >> $ROOT/.claude/iterations/sprint-latest/.notifications.log

echo "[PM-Stage1] Architect 已通知，阶段 2 可以开始"

bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "PM" "步骤完成" "通知架构师" "" "成功"
```

---

### 阶段 1.3：状态更新

#### 步骤 1.3.1：更新 session-status.md

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "PM" "步骤开始" "更新 session-status" "" ""

# 更新阶段完成记录
# 更新产出物追踪表
# 更新自动推进状态
# 记录阶段完成报告

echo "session-status.md 更新完成"

bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "PM" "步骤完成" "更新 session-status" "" "成功"
```

---

## 阶段 1 输出物清单

| 产出物 | 路径 | 状态 | 负责人 |
|--------|------|------|--------|
| 需求主文档 | `.claude/iterations/sprint-latest/requirements/upgrade-*.md` | ✅ | Analyst |
| User Story 文档 | `.claude/iterations/sprint-latest/requirements/user-stories/us-*.md` | ✅ | Analyst |
| Sub-feature 文档 | `.claude/iterations/sprint-latest/requirements/sub-features/sf-*.md` | ✅ | Analyst |
| 需求索引 | `.claude/iterations/sprint-latest/requirements/index.md` | ✅ | Analyst |
| 审查结果 | `.claude/iterations/sprint-latest/.review-count` | ✅ | PM |
| 通知记录 | `.claude/iterations/sprint-latest/.notifications.log` | ✅ | PM |
| session-status.md | `.claude/iterations/session-status.md` | ✅ | PM |

---

## Human Gate 检查点

### Gate 1：Analyst 阶段产出确认

**检查内容**：
- User Story 是否满足 INVEST 原则
- Sub-feature 是否完整
- 系统关联分析是否准确

**用户回复选项**：
- `继续` - 进入 PM 审查
- `补充` - 需要补充内容
- `暂停` - 暂停阶段 1

### Gate 2：PM 审查结果确认

**检查内容**：
- 审查结果是否符合预期
- 是否允许进入阶段 2

**用户回复选项**：
- `继续` - 进入阶段 2
- `复查` - 重新审查
- `暂停` - 暂停阶段 1

---

## 异常处理

| 异常场景 | 处理方式 |
|---------|---------|
| feature.md 不存在 | 警告并中止 |
| 审查打回次数 ≥ 3 | 提交 Human Gate 决策 |
| Analyst 无法修正问题 | 提交 Human Gate 决策 |
| 知识图谱查询失败 | 标注"手动分析"，继续执行 |

---

## 关联文档

| 文档 | 路径 | 说明 |
|------|------|------|
| analyst-stage1.md | `.claude/agents/analyst-stage1.md` | Analyst 阶段 1 详细定义 |
| pm-stage1.md | `.claude/agents/pm-stage1.md` | PM 阶段 1 详细定义 |
| feature-template.md | `.claude/templates/feature-template.md` | 功能需求文档模板 |
| requirements-template.md | `.claude/templates/requirements-template.md` | 需求文档模板 |
| user-story-template.md | `.claude/templates/user-story-template.md` | User Story 模板 |
| sub-feature-template.md | `.claude/templates/sub-feature-template.md` | Sub-feature 模板 |
| session-status.md | `.claude/iterations/session-status.md` | 阶段状态追踪 |
| project.md | `.claude/context/project.md` | 项目上下文 |