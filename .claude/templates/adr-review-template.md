# ADR Review Template
> 文件名：`.claude/iterations/sprint-latest/reviews/adr-review.md`
> 用途：PM Agent 审核 Architecture Agent 输出的 ADR
> 说明：审核维度详见 `pm-audit-stage2.md` 操作 3

---

## 审核信息

| 字段 | 内容 |
|------|------|
| **ADR 路径** | `.claude/iterations/sprint-latest/ADR.md` |
| **关联需求** | `.claude/iterations/sprint-latest/requirements.md` |
| **审核者** | PM |
| **审核时间** | YYYY-MM-DD HH:mm |
| **审核轮次** | 第 N 次 |

---

## 问题汇总

| 问题ID | 问题描述 | 审核维度 | 严重度 | 负责Agent | 状态 |
|--------|---------|---------|--------|-----------|------|
| P-001 | [具体问题描述] | 维度N | P0/P1/P2 | Architect | Open/Fixed/Closed/Unfixed/CannotFix |

**状态说明**：
- **Open**: 新发现的问题，待修复
- **Fixed**: Architecture Fix Agent 已修复，待 PM 验证
- **Closed**: PM 验证通过，问题已解决
- **Unfixed**: PM 验证不通过，需要重新修复
- **CannotFix**: 无法修复，需要人类介入

---

**总体结论**：
- [ ] **通过** - 所有问题已 Closed，可进入下一阶段
- [ ] **不通过** - 存在 Open/Unfixed 问题，需修复后重新提交

---

## 审核意见

### 需要修复的问题（优先级排序）

1. **[P0] 问题描述**：xxx
   - **问题ID**：P-001
   - **严重度**：P0
   - **负责Agent**：Architect
   - **期望修复方式**：在 ADR.md 第 X 章 X 节补充 xxx 内容，参考 requirements.md US-XXX 的 xxx 要求

2. **[P1] 问题描述**：xxx
   - **问题ID**：P-002
   - **严重度**：P1
   - **负责Agent**：Architect
   - **期望修复方式**：修改 ADR.md 第 X 节的 xxx 部分，确保与 consistency-baseline.md 一致

---

## 修复记录

> 由 Architecture Fix Agent 在每次修复后更新

| 问题ID | 修复时间 | 修复章节 | 修复摘要 | 修复人 | 状态 |
|--------|---------|---------|---------|-------|------|
| P-001 | YYYY-MM-DD HH:mm | 第 5.4 节 | 新增 US-003 的 API 设计 | Architect | Fixed |
| P-002 | YYYY-MM-DD HH:mm | 第 6.3 节 | 补充受影响模块分析 | Architect | Fixed |

---

## 审核历史

| 轮次 | 审核时间 | 问题数量 | 结论 | 备注 |
|------|----------|----------|------|------|
| 第1次 | YYYY-MM-DD HH:mm | Open=5, Fixed=0 | 不通过 | 发现 5 个问题 |
| 第2次 | YYYY-MM-DD HH:mm | Open=0, Fixed=5, Closed=5 | 通过 | 所有问题已修复并验证通过 |
| 第N次 | YYYY-MM-DD HH:mm | Open=X, Fixed=Y, Unfixed=Z | 不通过 | Z 个问题修复未通过验证 |

---

## 附录：常见问题类型参考

### 审核维度分类

| 维度编号 | 维度名称 | 检查要点 |
|---------|---------|---------|
| 维度1 | 功能一致性 | ADR 是否覆盖所有 US，无遗漏 |
| 维度2 | 设计完整性 | 是否有前端/后端/数据模型/API 等完整设计 |
| 维度3 | 受影响模块分析 | 是否正确识别所有受影响的现有模块 |
| 维度4 | 实现可行性 | Task 是否原子化，依赖是否清晰 |
| 维度5 | 错误处理与边界设计 | 是否有错误处理和边界值处理 |
| 维度6 | 风险与非功能设计 | 是否有风险分析和性能设计 |
| 维度7 | 一致性合规 | 是否遵循 consistency-baseline.md |
| 维度8 | 技术栈 | 是否符合 tech-stack-profile.md |

### 严重度定义

| 严重度 | 定义 | 示例 |
|-------|------|------|
| P0 | 阻断性问题，必须修复才能继续 | 缺少核心 US 的设计、API 签名不完整 |
| P1 | 重要问题，影响开发质量 | 缺少错误处理、受影响模块分析不完整 |
| P2 | 建议性问题，优化项 | 命名不规范、注释不完整 |

### CannotFix 场景

| 场景 | 处理方式 |
|------|---------|
| 问题与 requirements.md 冲突 | 转交 BA 修订需求文档 |
| 需要人类决策的技术选型 | 转交人类架构师决策 |
| 业务逻辑调整超出架构范围 | 转交 BA 和业务方确认 |
| 修复会引入更严重问题 | 记录原因，请求人类介入 |