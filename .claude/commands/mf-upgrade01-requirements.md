# /mf-upgrade:01-requirements – 需求澄清与现有系统分析

## 0. 前置条件

> 执行本阶段前，必须满足以下条件：

| 文件 | 路径 | 状态要求 |
|------|------|---------|
| session-status.md | `.claude/iterations/session-status.md` | 已创建 |
| techstack-overall.md | `.claude/iterations/context/techstack-overall.md` | 已存在 |
| tech-stack-profile.md | `.claude/context/tech-stack-profile.md` | 已存在 |
| consistency-baseline.md | `.claude/context/consistency-baseline.md` | 已存在 |
| knowledge-graph.md | `.claude/iterations/context/knowledge-graph.md` | 已存在 |
| feature.md | `.claude/iterations/sprint-latest/feature.md` | 已存在 |

### 路径说明
- 所有输入输出文件均使用完整相对路径，避免歧义
- 路径基准：项目根目录（即 `main.py` 所在目录）

---

## 0. 日志声明

执行本阶段所有步骤时，必须使用 `.claude/hooks/log-event.sh` 记录日志：
- 进入阶段：`bash .claude/hooks/log-event.sh "01" "$AGENT_NAME" "阶段进入" "阶段1开始" "" "成功"`
- 结束阶段：`bash .claude/hooks/log-event.sh "01" "$AGENT_NAME" "阶段退出" "阶段1完成" "" "成功"`
- 产出文件：`bash .claude/hooks/log-event.sh "01" "$AGENT_NAME" "产出物" "生成 <文件>" "<文件>" "成功"`

---

## 1. 规则加载（按需引用）

| 规则/技能 | 用途 | 引用时机 |
|-----------|------|---------|
| `.claude/rules/global/session-init.md` | 阶段初始化三原则 | 步骤 2 开始前 |
| `.claude/rules/scenario-upgrade/consistency-first.md` | 一致性优先规则 | analyst-stage1 内部 |
| `.claude/rules/scenario-upgrade/api-compatibility.md` | API兼容性规则 | analyst-stage1 内部 |
| `.claude/rules/scenario-upgrade/reuse-before-build.md` | 复用优先规则 | analyst-stage1 内部 |

---

## 2. 前置检查

**执行者**：框架自动检查

### 2.1 检查 session-status.md

1. 读取 `.claude/iterations/session-status.md`
2. 确认阶段 0 已完成（状态为 ✅）
3. 若不存在或阶段 0 未完成，报错退出：
   ```
   [自动检查] 阶段 0 未完成或 session-status.md 缺失，请先执行 /mf-upgrade:00-init
   ```

### 2.2 检查 context 文件

1. 确认 `.claude/context/tech-stack-profile.md` 存在
2. 确认 `.claude/context/consistency-baseline.md` 存在
3. 若任一不存在，报错退出：
   ```
   [自动检查] context 文件缺失：tech-stack-profile.md 或 consistency-baseline.md 不存在
   ```

### 2.3 自动检查上一 Agent 产出物

> **机制**：在激活下一个 Agent 前，自动检查上一个 Agent 的产出物是否存在

#### 步骤 1 → 步骤 2 自动检查

**触发时机**：在激活 `pm-stage1.md` 之前

1. 检查 `.claude/iterations/sprint-latest/requirements/upgrade-*.md` 是否存在
2. 若不存在，报错：
   ```
   [自动检查] analyst-stage1 产出物不存在：requirements/upgrade-*.md 未找到
   错误：前置 Agent 未完成工作，请先执行 analyst-stage1
   ```
3. 若存在，继续执行步骤 2

---

## 3. 工作流编排

### 步骤 1：分析师主导需求澄清

- **激活 Agent**：`agents/analyst-stage1.md`
- **职责**：分析师执行完整的需求澄清工作（需求访谈、系统关联分析、命名约定提取、测试影响评估、输出需求文档）
- **引用技能**：`.claude/skills/graphify-query-cheatsheet.md`
- **引用规则**：`.claude/rules/scenario-upgrade/consistency-first.md`、`.claude/rules/scenario-upgrade/api-compatibility.md`、`.claude/rules/scenario-upgrade/reuse-before-build.md`
- **产出物**：`.claude/iterations/sprint-latest/requirements/upgrade-YYYY-MM-DD-title.md`
- **完成后**：更新 session-status.md 中阶段 1 Analyst 完成状态为"✅"

### 步骤 2：PM 执行硬性审查

- **前置检查**：自动检查步骤 1 产出物是否存在
- **激活 Agent**：`agents/pm-stage1.md`
- **职责**：PM 审查分析师产出的需求文档
- **审查清单**：
  - [ ] 冲突拓扑分类完整且有具体模块名
  - [ ] 验收标准全部可测试
  - [ ] 命名约定引用至少 2 个不同文件
  - [ ] 测试影响给出具体文件路径
  - [ ] 需求文档反向引用了 tech-stack-profile.md 和 consistency-baseline.md
  - [ ] 核心冲突已完成升级决策
- **产出物**：更新 session-status.md 中阶段 1 完成状态为"✅"

---

## 4. Human Gate

**审查结果**：
- **全部通过**：提交 `[Human Gate]` 等待人类确认
- **任一未通过**：打回给分析师补充，修正后重新提交审查

---

## 5. 产出物

| 产出物 | 路径 |
|--------|------|
| 需求文档 | `.claude/iterations/sprint-latest/requirements/upgrade-YYYY-MM-DD-title.md` |

---

## 6. 异常处理

| 异常场景 | 处理方式 |
|---------|---------|
| session-status.md 缺失 | 报错退出 |
| context 文件缺失 | 报错退出 |
| 上一 Agent 产出物不存在 | 报错退出，提示前置 Agent 未完成 |
| PM 审查 3 次仍不通过 | 提交 Human Gate |

---

## 关联文档

| 文档 | 路径 |
|------|------|
| 分析师 Agent（阶段1） | `agents/analyst-stage1.md` |
| PM Agent（阶段1） | `agents/pm-stage1.md` |
| graphify 技能 | `.claude/skills/graphify-query-cheatsheet.md` |
| 需求文档模板 | `.claude/templates/requirements-template.md` |