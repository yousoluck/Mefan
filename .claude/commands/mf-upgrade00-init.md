# /mf-upgrade:00-init – 会话初始化与上下文建立

> **当前阶段**：阶段 0（会话初始化）
> **主导角色**：项目经理 (PM)
> **辅助角色**：架构师 (Architect)
> **前置条件**：无（首次进入迭代）

---

## 0. 日志声明（自动追加）

执行本阶段所有步骤时，必须使用 `.claude/hooks/log-event.sh` 记录日志：
- 进入阶段：`bash .claude/hooks/log-event.sh "00" "$AGENT_NAME" "阶段进入" "阶段0开始" "" "成功"`
- 结束阶段：`bash .claude/hooks/log-event.sh "00" "$AGENT_NAME" "阶段退出" "阶段0完成" "" "成功"`
- 产出文件：`bash .claude/hooks/log-event.sh "00" "$AGENT_NAME" "产出物" "生成 <文件>" "<文件>" "成功"`
- 异常：`bash .claude/hooks/log-event.sh "00" "$AGENT_NAME" "异常" "<描述>" "" "失败"`

---

## 1. 规则加载（按需引用，非集中声明）

> 以下规则在本步骤执行时**按需读取**，不在阶段开头集中加载。

| 规则/技能 | 用途 | 引用时机 |
|-----------|------|---------|
| `.claude/rules/global/session-init.md` | 阶段初始化三原则 | 步骤 2 开始前 |
| `.claude/skills/graphify-query-cheatsheet.md` | graphify 命令查询方式 | 步骤 3.2 需要执行 graphify 时 |

---

## 2. 环境确认

**执行者**：PM

### 2.1 确认 SCENARIO

读取 `SCENARIO` 变量，确认值为 `upgrade`。若未定义，报错退出。

### 2.2 确定迭代目录

1. 检查是否存在 `iterations/sprint-YYYY-MM-DD/` 目录（YYYY-MM-DD 为当前日期）
2. 若不存在，**报错退出**（要求用户预先创建）
3. 记录本次 iteration 名称（如 `sprint-2026-05-16`）

### 2.3 创建/读取 session-status.md

> **规则**：`session-status.md` 创建在 `iterations/{sprint-name}/session-status.md`

1. 检查 `iterations/{sprint-name}/session-status.md` 是否存在
2. 若不存在，使用 `.claude/templates/session-status-template.md` 生成
3. 若存在，读取并作为当前状态基础
4. 在 session-status.md 中初始化阶段 0 完成记录（状态标记为 ⏳）

---

## 3. 技术栈与一致性基线分析

**执行者**：Architect

### 3.1 技术栈分析

**引用技能**：`.claude/skills/graphify-query-cheatsheet.md`（了解 graphify 用法）

1. 扫描项目根目录依赖文件：`package.json`、`pom.xml`、`requirements.txt`、`build.gradle` 等
2. **若发现依赖文件**：提取前端框架、状态管理、后端框架、数据库、中间件及版本号
3. **若未发现任何依赖文件**：
   - 向用户询问项目类型和技术栈
   - 在输出中标注 **"人工补充"**，逐条记录用户提供的技术栈
4. 输出 `.claude/context/tech-stack-profile.md`，**必须使用** `.claude/templates/tech-stack-profile-template.md`

### 3.2 一致性基线提取

**引用技能**：`.claude/skills/graphify-query-cheatsheet.md`

1. 执行 `graphify query "most common patterns in the project"`
2. 执行 `graphify similar <核心模块>`（若无核心模块，跳过）
3. **若 graphify 查询失败**：
   - 手动扫描 `src/` 下前 5 个高频目录
   - 识别代码组织模式、命名规则、错误处理范式
   - 在输出中标注 **"手动分析"**
4. **强制证据要求**：每条基线必须附带至少 1 条证据（文件路径 + 模式描述 或 graphify 节点名）
5. 输出 `.claude/context/consistency-baseline.md`，**必须使用** `.claude/templates/consistency-baseline-template.md`

### 3.3 依赖全景图（可选）

1. 执行 `graphify dependents <核心模块>`（若 graphify 可用）
2. 将结果摘要**追加到** session-status.md 的"依赖全景图"段
3. 若 graphify 不可用，在 session-status.md 中标注"依赖全景图暂不可用"

---

## 4. PM 校验

**执行者**：PM

PM 在架构师完成步骤 3 后，执行以下校验：

### 4.1 技术栈完整性
- [ ] 是否有前端框架记录？
- [ ] 是否有后端框架记录？
- [ ] 是否列出所有主要直接依赖？
- [ ] 若标注"人工补充"，是否逐条记录并标记清楚？

### 4.2 一致性基线有效性
- [ ] 每条基线是否至少有 1 条证据？
- [ ] 随机抽查 1-2 条证据中的文件路径是否真实存在？
- [ ] 基线条目是否可直接作为阶段 4 开发者的检查标准？

### 4.3 校验结果
- **全部通过**：更新 session-status.md 产出物状态为"✅"
- **未通过**：列出未通过项，通知架构师修正后重新校验

---

## 5. 异常处理

| 异常场景 | 处理方式 |
|---------|---------|
| SCENARIO 未定义 | 报错退出 |
| 迭代目录未创建 | 报错退出 |
| graphify 查询失败 | 标注"手动分析"继续，不报错 |
| PM 校验重试 3 次仍失败 | 提交 Human Gate |

异常需记录到 session-status.md 的"异常记录"章节。

---

## 6. 阶段结束

PM 向用户输出三句话摘要：
- 技术栈组件数量
- 基线条目数 + 证据来源方式（自动/手动）
- 依赖全景图状态

等待 `[Human Gate]` 确认后，进入阶段 1。

---

## 阶段 0 产出物

| 产出物 | 路径 | 状态校验 |
|--------|------|---------|
| tech-stack-profile.md | `.claude/context/` | PM 校验通过后 ✅ |
| consistency-baseline.md | `.claude/context/` | PM 校验通过后 ✅ |
| session-status.md | `iterations/{sprint-name}/` | 阶段结束时 ⏳→✅ |

---

## 关联文档

| 文档 | 路径 |
|------|------|
| session-init 规则 | `.claude/rules/global/session-init.md` |
| graphify 技能 | `.claude/skills/graphify-query-cheatsheet.md` |
| tech-stack 模板 | `.claude/templates/tech-stack-profile-template.md` |
| consistency-baseline 模板 | `.claude/templates/consistency-baseline-template.md` |
| session-status 模板 | `.claude/templates/session-status-template.md` |