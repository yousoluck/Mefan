# /mf-upgrade:02-arch-qa – 架构设计与测试策略

> **当前阶段**：阶段 2（架构设计与测试策略）
> **前置条件**：阶段 1 已完成，需求文档已产出

---

## 0. 日志声明

执行本阶段所有步骤时，必须使用 `.claude/hooks/log-event.sh` 记录日志：
- 进入阶段：`bash .claude/hooks/log-event.sh "02" "$AGENT_NAME" "阶段进入" "阶段2开始" "" "成功"`
- 结束阶段：`bash .claude/hooks/log-event.sh "02" "$AGENT_NAME" "阶段退出" "阶段2完成" "" "成功"`
- 产出文件：`bash .claude/hooks/log-event.sh "02" "$AGENT_NAME" "产出物" "生成 <文件>" "<文件>" "成功"`

---

## 1. 规则加载（按需引用）

| 规则/技能 | 用途 | 引用时机 |
|-----------|------|---------|
| `.claude/rules/global/session-init.md` | 阶段初始化三原则 | 步骤 2 开始前 |
| `.claude/rules/scenario-upgrade/consistency-first.md` | 一致性优先规则 | architect-stage2 内部 |
| `.claude/rules/scenario-upgrade/api-compatibility.md` | API兼容性规则 | architect-stage2 内部 |
| `.claude/rules/scenario-upgrade/reuse-before-build.md` | 复用优先规则 | architect-stage2 内部 |
| `.claude/rules/scenario-upgrade/reference-module.md` | 参考模块规则 | architect-stage2 内部 |
| `.claude/rules/global/conflict-resolution.md` | 设计冲突升级 | architect-stage2 内部 |

---

## 2. 前置检查

**执行者**：框架自动检查

### 2.1 检查阶段 1 产出物

1. 读取 `.claude/iterations/session-status.md`
2. 确认阶段 1 已完成（状态为 ✅）
3. 若不存在或阶段 1 未完成，报错退出：
   ```
   [自动检查] 阶段 1 未完成或 session-status.md 缺失，请先执行 /mf-upgrade:01-requirements
   ```

### 2.2 检查 context 文件

1. 确认 `.claude/context/tech-stack-profile.md` 存在
2. 确认 `.claude/context/consistency-baseline.md` 存在
3. 若任一不存在，报错退出：
   ```
   [自动检查] context 文件缺失
   ```

### 2.3 自动检查上一 Agent 产出物

#### 步骤 1 → 步骤 2 自动检查

**触发时机**：在激活 `qa-stage2.md` 之前

1. 检查 `.claude/iterations/sprint-latest/adr/upgrade-*.md` 是否存在
2. 若不存在，报错：
   ```
   [自动检查] architect-stage2 产出物不存在：adr/upgrade-*.md 未找到
   错误：前置 Agent 未完成工作，请先执行 architect-stage2
   ```
3. 若存在，继续执行步骤 2

#### 步骤 2 → 步骤 3 自动检查

**触发时机**：在激活 `pm-stage2.md` 之前

1. 检查 `.claude/iterations/sprint-latest/test-plan/upgrade-*.md` 是否存在
2. 若不存在，报错：
   ```
   [自动检查] qa-stage2 产出物不存在：test-plan/upgrade-*.md 未找到
   错误：前置 Agent 未完成工作，请先执行 qa-stage2
   ```
3. 若存在，继续执行步骤 3

---

## 3. 工作流编排

### 步骤 1：架构师主导架构设计与测试策略

- **前置检查**：自动检查阶段 1 产出物
- **激活 Agent**：`agents/architect-stage2.md`
- **职责**：架构师执行完整的架构设计工作（方案对比、详细设计、参考实现定位、一致性合规检查、设计冲突升级、输出 ADR）
- **引用技能**：`.claude/skills/graphify-query-cheatsheet.md`
- **引用规则**：`.claude/rules/scenario-upgrade/consistency-first.md`、`.claude/rules/scenario-upgrade/api-compatibility.md`、`.claude/rules/scenario-upgrade/reference-module.md`
- **产出物**：`.claude/iterations/sprint-latest/adr/upgrade-YYYY-MM-DD-title.md`
- **完成后**：更新 session-status.md 中阶段 2 Architect 完成状态为"✅"

### 步骤 2：QA 主导测试策略设计

- **前置检查**：自动检查步骤 1 产出物（ADR 是否存在）
- **激活 Agent**：`agents/qa-stage2.md`
- **职责**：QA 执行完整的测试策略设计（回归测试范围、新增测试场景、质量门槛设定、人工测试指南标记、输出测试计划）
- **引用规则**：`.claude/rules/global/quality-gates.md`
- **产出物**：`.claude/iterations/sprint-latest/test-plan/upgrade-YYYY-MM-DD-title.md`
- **完成后**：更新 session-status.md 中阶段 2 QA 完成状态为"✅"

### 步骤 3：PM 执行硬性审查

- **前置检查**：自动检查步骤 2 产出物（测试计划是否存在）
- **激活 Agent**：`agents/pm-stage2.md`
- **职责**：PM 审查架构师和 QA 的产出
- **审查清单**：
  - [ ] ADR 是否包含至少两个方案的对比
  - [ ] 详细设计是否给出了目录位置和接口签名
  - [ ] 是否声明了一致性合规状态（遵循/突破并附理由）
  - [ ] 是否提供了至少 2 个参考实现文件路径
  - [ ] 测试计划是否列出具体回归测试文件路径
  - [ ] 质量门槛是否明确（覆盖率、性能基线）
  - [ ] 若有设计冲突，是否已记录并启动升级
- **产出物**：更新 session-status.md 中阶段 2 完成状态为"✅"

---

## 4. Human Gate

**审查结果**：
- **全部通过**：提交 `[Human Gate]` 等待人类确认
- **任一未通过**：打回给相应 Agent 修正，修正后重新提交审查

---

## 5. 产出物

| 产出物 | 路径 |
|--------|------|
| ADR | `.claude/iterations/sprint-latest/adr/upgrade-YYYY-MM-DD-title.md` |
| 测试计划 | `.claude/iterations/sprint-latest/test-plan/upgrade-YYYY-MM-DD-title.md` |

---

## 6. 异常处理

| 异常场景 | 处理方式 |
|---------|---------|
| 前置文档缺失 | 报错退出 |
| 上一 Agent 产出物不存在 | 报错退出，提示前置 Agent 未完成 |
| 设计冲突无法裁决 | 通知 PM，生成《设计冲突裁决申请书》 |
| graphify 不可用 | 标注"手动分析"继续 |
| PM 审查 3 次仍不通过 | 提交 Human Gate |

---

## 关联文档

| 文档 | 路径 |
|------|------|
| 架构师 Agent（阶段2） | `agents/architect-stage2.md` |
| QA Agent（阶段2） | `agents/qa-stage2.md` |
| PM Agent（阶段2） | `agents/pm-stage2.md` |
| graphify 技能 | `.claude/skills/graphify-query-cheatsheet.md` |
| ADR 模板 | `.claude/templates/adr-template.md` |
| 测试计划模板 | `.claude/templates/test-plan-template.md` |