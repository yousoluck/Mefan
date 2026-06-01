# Phase Check - 各阶段 Agent 状态更新明细

> **目的**：明确每个阶段中，哪个 Agent 对哪个文件做了什么更新，确保迭代状态可追踪。
> **适用范围**：阶段 0 ~ 阶段 6

---

## 更新规范

### 必须更新的文件

| 文件 | 路径 | 说明 |
|------|------|------|
| **session-status.md** | `.claude/iterations/session-status.md` | 跨迭代全局状态追踪 |
| **project.md** | `.claude/context/project.md` | 项目上下文与迭代历史 |

### session-status.md 必须更新的章节

| 章节 | 内容 | 更新时机 |
|------|------|----------|
| `## 阶段完成记录` | 阶段完成时间戳 + 状态 | 每个子阶段完成时 |
| `## 产出物追踪表` | 产出物路径 + 状态 + 时间 | 每个产出物完成时 |
| `## PM 阶段完成报告（标准化格式）` | 阶段完成报告（执行摘要、关键产出、问题、下一步） | 每个阶段完成时 |
| `## 自动推进状态` | 当前阶段 + 已完成阶段 | 阶段进入/完成时 |
| `## 异常记录` | 异常描述 + 处理结果 | 发生异常时 |

### project.md 必须更新的章节

| 章节 | 内容 | 更新时机 |
|------|------|----------|
| `### 迭代 sprint-latest` | 迭代基本信息 + 开始日期 | 阶段 0 进入时 |
| `#### 详细文档` | 各文档状态（⏳ → ✅） | 产出物完成时 |

---

## 各阶段更新明细

### 阶段 0（00-init）- 会话初始化与上下文建立

#### PM Agent

| 更新文件 | 章节 | 段落 | 更新内容 |
|---------|------|------|----------|
| session-status.md | `## 阶段完成记录` | 阶段 00 行 | 状态：⏳ → ✅，填入完成时间 |
| session-status.md | `## 产出物追踪表` | project.md 行 | 状态：⏳ → ✅，填入完成时间 |
| session-status.md | `## 自动推进状态` | 当前阶段 | 值：0 → 0 |
| session-status.md | `## 自动推进状态` | 已完成阶段 | 值：[] → [0] |
| session-status.md | `## PM 阶段完成报告（标准化格式）` | 阶段 0 完成报告 | 执行摘要、关键产出、与上阶段衔接、下一步 |
| project.md | `### 迭代 sprint-latest` | 迭代名称/开始日期/状态 | 填入迭代基本信息 |
| project.md | `#### 详细文档` | project.md 行 | 状态：⏳ → ✅ |

#### Architect Agent

| 更新文件 | 章节 | 段落 | 更新内容 |
|---------|------|------|----------|
| session-status.md | `## 产出物追踪表` | tech-stack-profile.md 行 | 状态：⏳ → ✅，填入完成时间 |
| session-status.md | `## 产出物追踪表` | consistency-baseline.md 行 | 状态：⏳/✅，填入完成时间 |
| session-status.md | `## 产出物追踪表` | dependencies-overview.md 行 | 状态：⏳/✅，填入完成时间 |
| session-status.md | `## PM 阶段完成报告（标准化格式）` | Architect 阶段完成报告 | 执行摘要、关键产出、与上阶段衔接 |
| project.md | `#### 详细文档` | tech-stack-profile.md 行 | 状态：⏳ → ✅ |
| project.md | `#### 详细文档` | consistency-baseline.md 行 | 状态：⏳ → ✅ |
| project.md | `#### 详细文档` | dependencies-overview.md 行 | 状态：⏳ → ✅ |

#### Analyst Agent

| 更新文件 | 章节 | 段落 | 更新内容 |
|---------|------|------|----------|
| session-status.md | `## 产出物追踪表` | feature.md 行 | 状态：⏳ → ✅，填入完成时间 |
| session-status.md | `## PM 阶段完成报告（标准化格式）` | Analyst 阶段完成报告 | 执行摘要、关键产出、与上阶段衔接 |
| project.md | `#### 详细文档` | feature.md 行 | 状态：⏳ → ✅ |

---

### 阶段 1（01-requirements）- 需求详细设计

#### BA Agent

| 更新文件 | 章节 | 段落 | 更新内容 |
|---------|------|------|----------|
| session-status.md | `## 阶段完成记录` | 阶段 01（BA）行 | 状态：⏳ → ✅，填入完成时间 |
| session-status.md | `## 产出物追踪表` | requirements.md 行 | 状态：⏳ → ✅，填入完成时间 |
| session-status.md | `## PM 阶段完成报告（标准化格式）` | BA 阶段完成报告 | 执行摘要、关键产出、与上阶段衔接 |
| project.md | `#### 详细文档` | requirements.md 行 | 状态：⏳ → ✅ |

#### PM Agent

| 更新文件 | 章节 | 段落 | 更新内容 |
|---------|------|------|----------|
| session-status.md | `## 阶段完成记录` | 阶段 01（PM）行 | 状态：⏳ → ✅，填入完成时间（审查通过后） |
| session-status.md | `## 自动推进状态` | 当前阶段 | 值：0 → 1 |
| session-status.md | `## 自动推进状态` | 已完成阶段 | 值：[0] → [0, 1] |
| session-status.md | `## PM 阶段完成报告（标准化格式）` | PM 阶段完成报告 | 执行摘要、关键产出、发现的问题、下一步 |

---

### 阶段 2（02-arch-qa）- 架构设计与测试策略

#### Architect Agent

| 更新文件 | 章节 | 段落 | 更新内容 |
|---------|------|------|----------|
| session-status.md | `## 阶段完成记录` | 阶段 02（Architect）行 | 状态：⏳ → ✅，填入完成时间 |
| session-status.md | `## 产出物追踪表` | ADR.md 行 | 状态：⏳ → ✅，填入完成时间 |
| session-status.md | `## PM 阶段完成报告（标准化格式）` | Architect 阶段完成报告 | 执行摘要、关键产出、与上阶段衔接 |
| project.md | `#### 详细文档` | ADR.md 行 | 状态：⏳ → ✅ |

#### QA Agent

| 更新文件 | 章节 | 段落 | 更新内容 |
|---------|------|------|----------|
| session-status.md | `## 阶段完成记录` | 阶段 02（QA）行 | 状态：⏳ → ✅，填入完成时间 |
| session-status.md | `## 产出物追踪表` | test-plan.md 行 | 状态：⏳ → ✅，填入完成时间 |
| session-status.md | `## PM 阶段完成报告（标准化格式）` | QA 阶段完成报告 | 执行摘要、关键产出、与上阶段衔接 |
| project.md | `#### 详细文档` | test-plan.md 行 | 状态：⏳ → ✅ |

#### PM-Audit Agent（ADR 审核）

| 更新文件 | 章节 | 段落 | 更新内容 |
|---------|------|------|----------|
| session-status.md | `## 阶段完成记录` | 阶段 02（PM-Audit）行 | 状态：⏳ → ✅，填入完成时间 |
| session-status.md | `## 产出物追踪表` | ADR.md 行 | 状态：✅ → ✅ 已审核，填入审核时间 |
| session-status.md | `## 自动推进状态` | 当前阶段 | 值：1 → 2 |
| session-status.md | `## 自动推进状态` | 已完成阶段 | 值：[0, 1] → [0, 1, 2] |
| session-status.md | `## PM 阶段完成报告（标准化格式）` | PM-Audit 阶段完成报告 | 审核结果、驳回/通过、下一步 |

#### PM-Audit-TP Agent（Test-Plan 审核）

| 更新文件 | 章节 | 段落 | 更新内容 |
|---------|------|------|----------|
| session-status.md | `## 阶段完成记录` | 阶段 02（PM-Audit-TP）行 | 状态：⏳ → ✅，填入完成时间 |
| session-status.md | `## 产出物追踪表` | test-plan.md 行 | 状态：✅ → ✅ 已审核，填入审核时间 |
| session-status.md | `## PM 阶段完成报告（标准化格式）` | PM-Audit-TP 阶段完成报告 | 审核结果、驳回/通过、下一步 |
| project.md | `#### 详细文档` | ADR.md 行 | 状态：⏳ → ✅（完成/审核时间） |
| project.md | `#### 详细文档` | test-plan.md 行 | 状态：⏳ → ✅（完成/审核时间） |

---

### 阶段 3（03-plan）- 迭代计划与任务排期

#### Analyst Agent

| 更新文件 | 章节 | 段落 | 更新内容 |
|---------|------|------|----------|
| session-status.md | `## 阶段完成记录` | 阶段 03（Analyst）行 | 状态：⏳ → ✅，填入完成时间 |
| session-status.md | `## 产出物追踪表` | sprint-status.md 行 | 状态：⏳ → ✅，填入完成时间 |
| session-status.md | `## PM 阶段完成报告（标准化格式）` | Analyst 阶段完成报告 | 执行摘要、关键产出、与上阶段衔接 |
| project.md | `#### 详细文档` | sprint-status.md 行 | 状态：⏳ → ✅ |

#### PM Agent

| 更新文件 | 章节 | 段落 | 更新内容 |
|---------|------|------|----------|
| session-status.md | `## 阶段完成记录` | 阶段 03（PM）行 | 状态：⏳ → ✅，填入完成时间 |
| session-status.md | `## 产出物追踪表` | sprint-status.md 行 | 状态：✅ → ✅ 审查通过，填入审查时间 |
| session-status.md | `## 自动推进状态` | 当前阶段 | 值：2 → 3 |
| session-status.md | `## 自动推进状态` | 已完成阶段 | 值：[0, 1, 2] → [0, 1, 2, 3] |
| session-status.md | `## PM 阶段完成报告（标准化格式）` | PM 阶段完成报告 | 执行摘要、关键产出、发现的问题、下一步 |

---

### 阶段 4（04-implement）- 迭代实现

#### PM Agent

| 更新文件 | 章节 | 段落 | 更新内容 |
|---------|------|------|----------|
| session-status.md | `## 阶段完成记录` | 阶段 04 行 | 状态：⏳ → 🔄 → ✅，填入开始/完成时间 |
| session-status.md | `## 产出物追踪表` | 04 实现 行 | 状态：⏳ → 🔄 → ✅，填入完成时间 |
| session-status.md | `## 自动推进状态` | 当前阶段 | 值：3 → 4 → 4 |
| session-status.md | `## 自动推进状态` | 已完成阶段 | 值：[0, 1, 2, 3] → [0, 1, 2, 3, 4] |
| session-status.md | `## PM 阶段完成报告（标准化格式）` | PM 阶段完成报告 | 开发结果、测试结果、Bug统计、问题追踪 |
| project.md | `#### 详细文档` | 04 实现阶段 行 | 状态：⏳ → ✅ |

**PM Agent 阶段 4 完成汇总时必须执行的具体更新**：

```bash
# 1. 更新 session-status.md 中阶段 4 状态为"✅ 完成"
sed -i 's/| 04 | 迭代实现 |.*| 🔄 进行中 |/| 04 | 迭代实现 | $(date +"%Y-%m-%d %H:%M") | ✅ 完成 |/g' \
  "$ROOT/.claude/iterations/session-status.md"

# 2. 更新 ## 阶段完成记录
echo "| 04 | PM | $(date +"%Y-%m-%d %H:%M") | 阶段 4 完成，MG 全部 Close | ✅ |" >> \
  "$ROOT/.claude/iterations/session-status.md"

# 3. 更新 ## 产出物追踪表
sed -i 's/| 04 实现.*| ⏳ |/| 04 实现 | ✅ 完成 |/g' \
  "$ROOT/.claude/iterations/session-status.md" 2>/dev/null || true

# 4. 更新 ## 自动推进状态
sed -i 's/| 04.*🔄/| 04 | ✅ |/g' \
  "$ROOT/.claude/iterations/session-status.md" 2>/dev/null || true

# 5. 追加 ## PM 阶段完成报告
cat >> "$ROOT/.claude/iterations/session-status.md" << 'EOF'

### PM 阶段 4 完成报告

#### 执行摘要
阶段 4 完成，所有 MG 进入 Close 状态。

#### 关键产出
- 完成 MG 数：X / Y
- 完成 US 数：X / Y
- 完成 Task 数：X / Y

#### 测试结果
- 自动化测试：X / X 通过
- 人工测试：X / X 通过

#### Bug 统计
- 发现 Bug 数：X
- 已修复：X
- 技术债务：X

#### 问题追踪
- review-log.md 记录数：X
- Human Gate 触发次数：X
EOF

# 6. 更新 project.md
if [ -f "$ROOT/.claude/context/project.md" ]; then
  sed -i 's/| 04 实现阶段.*| ⏳ 待开始 |/| 04 实现阶段 | ✅ 已完成 |/g' \
    "$ROOT/.claude/context/project.md"
fi
```

---

### 阶段 5（05-quality）- 质量测试与门禁

#### QA Agent

| 更新文件 | 章节 | 段落 | 更新内容 |
|---------|------|------|----------|
| session-status.md | `## 阶段完成记录` | 阶段 05（QA）行 | 状态：⏳ → ✅，填入完成时间 |
| session-status.md | `## 产出物追踪表` | quality-report.md 行 | 状态：⏳ → ✅，填入完成时间 |
| session-status.md | `## 产出物追踪表` | bug-log/auto-*.md 行 | 状态：⏳ → ✅，填入完成时间 |
| session-status.md | `## 产出物追踪表` | bug-log/manual-*.md 行 | 状态：⏳ → ✅，填入完成时间 |
| session-status.md | `## PM 阶段完成报告（标准化格式）` | QA 阶段完成报告 | 质量测试结果、缺陷发现统计 |
| project.md | `#### 详细文档` | quality-report.md 行 | 状态：⏳ → ✅ |

#### PM Agent

| 更新文件 | 章节 | 段落 | 更新内容 |
|---------|------|------|----------|
| session-status.md | `## 阶段完成记录` | 阶段 05（PM）行 | 状态：⏳ → ✅，填入完成时间 |
| session-status.md | `## 自动推进状态` | 当前阶段 | 值：4 → 5 |
| session-status.md | `## 自动推进状态` | 已完成阶段 | 值：[0, 1, 2, 3, 4] → [0, 1, 2, 3, 4, 5] |
| session-status.md | `## PM 阶段完成报告（标准化格式）` | PM 阶段完成报告 | P0/P1 缺陷决策、处理结果 |

#### Dev Agent（如有 P0/P1 缺陷修复）

| 更新文件 | 章节 | 段落 | 更新内容 |
|---------|------|------|----------|
| session-status.md | `## 阶段完成记录` | 阶段 05（Dev）行 | 状态：⏳ → ✅，填入完成时间 |
| session-status.md | `## 产出物追踪表` | bug-log/auto-*.md 行 | 状态：⏳ → ✅，填入修复时间 |
| session-status.md | `## 产出物追踪表` | bug-log/manual-*.md 行 | 状态：⏳ → ✅，填入修复时间 |
| session-status.md | `## PM 阶段完成报告（标准化格式）` | Dev 阶段完成报告 | 缺陷修复统计 |

#### Guardian Agent

| 更新文件 | 章节 | 段落 | 更新内容 |
|---------|------|------|----------|
| session-status.md | `## 阶段完成记录` | 阶段 05（守护者）行 | 状态：⏳ → ✅，填入完成时间 |
| session-status.md | `## PM 阶段完成报告（标准化格式）` | Guardian 阶段完成报告 | 门禁结果（APPROVED/REJECTED）、质量报告摘要 |

---

### 阶段 6（06-retrospect）- 迭代总结与进化

#### PM Agent

| 更新文件 | 章节 | 段落 | 更新内容 |
|---------|------|------|----------|
| session-status.md | `## 阶段完成记录` | 阶段 06（PM）行 | 状态：⏳ → ✅，填入完成时间 |
| session-status.md | `## 产出物追踪表` | iteration-retrospective.md 行 | 状态：⏳ → ✅，填入完成时间 |
| session-status.md | `## 自动推进状态` | 当前阶段 | 值：5 → 6 |
| session-status.md | `## 自动推进状态` | 已完成阶段 | 值：[0, 1, 2, 3, 4, 5] → [0, 1, 2, 3, 4, 5, 6] |
| session-status.md | `## PM 阶段完成报告（标准化格式）` | PM 阶段完成报告（迭代总结） | 迭代数据汇总、技术债务评估 |
| project.md | `#### 详细文档` | iteration-retrospective.md 行 | 状态：⏳ → ✅ |

#### Coach Agent（进化教练）

| 更新文件 | 章节 | 段落 | 更新内容 |
|---------|------|------|----------|
| session-status.md | `## 阶段完成记录` | 阶段 06（进化教练）行 | 状态：⏳ → ✅，填入完成时间 |
| session-status.md | `## 产出物追踪表` | evolution-proposal.md 行 | 状态：⏳ → ✅，填入完成时间 |
| session-status.md | `## PM 阶段完成报告（标准化格式）` | Coach 阶段完成报告 | 进化提案数量、改进模式 |

#### Guardian Agent

| 更新文件 | 章节 | 段落 | 更新内容 |
|---------|------|------|----------|
| session-status.md | `## 阶段完成记录` | 阶段 06（守护者）行 | 状态：⏳ → ✅，填入完成时间 |
| session-status.md | `## 产出物追踪表` | guardian-verification.md 行 | 状态：⏳ → ✅，填入完成时间 |
| session-status.md | `## PM 阶段完成报告（标准化格式）` | Guardian 阶段完成报告 | 验证结果、可合并性评估 |

#### PM Agent（全局进度报告）

| 更新文件 | 章节 | 段落 | 更新内容 |
|---------|------|------|----------|
| session-status.md | `## 阶段完成记录` | 阶段 06（PM 全局报告）行 | 状态：⏳ → ✅，填入完成时间 |
| session-status.md | `## PM 阶段完成报告（标准化格式）` | PM 全局进度报告 | PROJECT_STATUS.md 汇总、版本更新 |

---

## 附录：更新代码模板

### session-status.md 更新模板

```bash
# 更新阶段完成记录
echo "| {阶段} | {Agent} | $(date +"%Y-%m-%d %H:%M") | {完成内容} | ✅ |" >> \
  "$ROOT/.claude/iterations/session-status.md"

# 更新产出物追踪表
sed -i 's/| {产出物} | ⏳ 待创建 |/| {产出物} | ✅ 已创建 |/g' \
  "$ROOT/.claude/iterations/session-status.md"

# 更新自动推进状态
sed -i 's/| {阶段} |.*| 🔄 进行中 |/| {阶段} | {时间} | ✅ |/g' \
  "$ROOT/.claude/iterations/session-status.md"
```

### project.md 更新模板

```bash
# 更新详细文档状态
sed -i 's/| {文档名} | {路径} | ⏳ 待创建 |/| {文档名} | {路径} | ✅ 已创建 |/g' \
  "$ROOT/.claude/context/project.md"

# 更新迭代历史
sed -i 's/| {阶段名} | ⏳ 待开始 |/| {阶段名} | ✅ 已完成 |/g' \
  "$ROOT/.claude/context/project.md"
```

---

## 检查清单

每个阶段结束时，必须确认以下更新已完成：

- [ ] session-status.md `## 阶段完成记录` 已更新（每个 Agent 一行）
- [ ] session-status.md `## 产出物追踪表` 所有产出物已更新
- [ ] session-status.md `## PM 阶段完成报告（标准化格式）` 已更新
- [ ] session-status.md `## 自动推进状态` 已更新
- [ ] project.md `#### 详细文档` 相关文档状态已更新
- [ ] 如有异常，session-status.md `## 异常记录` 已追加