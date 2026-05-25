---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: fc9fc5bb71a3e8546844e16b1a1e74c3
    PropagateID: fc9fc5bb71a3e8546844e16b1a1e74c3
    ReservedCode1: 3043021f7f2d598baa3c7cb19d15c79686847c8511eeb218610bdfbbdaf3b347363e77022002ab282782d6c2f44d557b146aff1caee14288d4719802dbab8d693036b8de6d
    ReservedCode2: 304502206bf350308056c39ffc36af09e33c5e8a35ec4201646ea85f7abeabdb387b239e0221009e5605418b8436f942ba8a94096353266048fc2f543231d9ceff0f9b189d47e9
---

# User Story 文档模板

> 文件路径：`.claude/iterations/sprint-latest/requirements/user-stories/us-{ID}.md`
> 更新时机：Analyst-Stage1 完成 User Story 拆分后创建并填写
> **粒度**：独立可验收的用户故事，满足 INVEST 原则

---

## 基本信息

| 字段 | 内容 | 说明 |
|------|------|------|
| **US ID** | | 格式：US-{NNN} |
| **标题** | | 简洁描述用户目标 |
| **所属迭代** | | sprint-latest |
| **创建时间** | | |
| **Analyst** | | |
| **状态** | ⏳ To Do / 🔍 In Progress / ✅ Done | |

---

## 用户故事描述

### 1. 用户角色

> 描述与该 User Story 相关的用户角色

| 角色 | 描述 | 优先级 |
|------|------|--------|
| | | P0/P1/P2 |

### 2. 用户目标

> **格式**：`作为 {角色}，我想 {功能}，以便 {价值}`

```markdown
作为 [角色]，我想 [功能]，以便 [价值]。
```

### 3. 业务价值

> 描述该 User Story 对业务的价值

| 价值类型 | 描述 |
|---------|------|
| **用户价值** | |
| **业务价值** | |
| **技术价值** | |

### 4. 验收标准（Acceptance Criteria）

> 每个 User Story 必须有至少 2 个可验证的验收标准
> **格式**：输入-输出断言

| AC ID | 验收标准 | 测试方法 |
|-------|---------|---------|
| AC-1 | 输入 [X]，预期输出 [Y] | 手动/自动 |
| AC-2 | 输入 [A]，预期输出 [B] | 手动/自动 |

---

## 需求详情

### 5. 涉及的功能（From feature.md）

| 功能ID | 功能名称 | 说明 |
|--------|---------|------|
| FEATURE-001 | | 来自 feature.md 的功能要点 |

### 6. 涉及的系统模块

> 描述该 User Story 涉及的系统模块

| 模块类型 | 模块名称 | 文件路径/说明 |
|---------|---------|--------------|
| **接口模块** | | API 路径、请求/响应格式 |
| **逻辑模块** | | 业务规则、处理逻辑 |
| **数据模块** | | 数据库表、缓存结构 |

### 7. 依赖关系

#### 7.1 前置依赖

| 依赖类型 | 依赖项 | 说明 |
|---------|-------|------|
| **User Story** | US-XXX | 必须先完成 |
| **Sub-feature** | SF-XXX | 必须先完成 |
| **外部系统** | | 如有 |

#### 7.2 被依赖关系

| 依赖方 | 依赖项 | 说明 |
|-------|-------|------|
| US-XXX | 该 US 的输出 | |

---

## 子功能拆分（Sub-features）

> 该 User Story 拆分的子功能模块

| SF ID | 子功能名称 | 类型 | 优先级 | 状态 |
|-------|----------|------|--------|------|
| SF-001-1 | | frontend/backend/api/db | P0/P1/P2 | ⏳ |

### Sub-feature 详情引用

- `../sub-features/sf-001-1.md` - {子功能名称}
- `../sub-features/sf-001-2.md` - {子功能名称}

---

## 一致性要求

> 引用 consistency-baseline.md 和项目专属 Skills

### 8. 命名规范

| 规范类型 | 要求 | 引用 |
|---------|------|------|
| **Action 命名** | | 引用 consistency-baseline.md |
| **组件命名** | | 引用项目专属 Skill |
| **API 路径风格** | | 引用一致性约定 |

### 9. 代码模式

| 模式类型 | 引用 | 说明 |
|---------|------|------|
| **服务模式** | skills/project-service-pattern.md | |
| **DTO 模式** | skills/project-dto-pattern.md | |
| **错误处理** | skills/project-error-handling.md | |

---

## 测试要求

### 10. 现有测试影响

> 评估该 User Story 对现有测试的影响

| 测试文件 | 测试用例数 | 受影响用例 | 影响程度 |
|---------|-----------|-----------|---------|
| | | | |

### 11. 新增测试计划

| 类型 | 用例数 | 说明 |
|------|--------|------|
| **单元测试** | | |
| **集成测试** | | |
| **回归测试** | | |

### 12. 测试覆盖风险

| 风险等级 | 说明 | 处理方式 |
|---------|------|---------|
| 🟢 低 | | |
| 🟡 中 | | 需要补充测试 |
| 🔴 高 | 无现有测试覆盖 | 必须补充 |

---

## 冲突分析

### 13. 与其他 User Story 的冲突

> 识别与该 User Story 存在冲突的其他 User Story

| 冲突类型 | 涉及 US | 冲突描述 | 处理方式 |
|---------|--------|---------|---------|
| **核心冲突** | US-XXX | | |
| **边缘冲突** | US-YYY | | |

---

## 备注

### 14. 待确认事项

| 序号 | 问题 | 状态 | 回答 |
|------|------|------|------|
| 1 | | 待确认 | |

### 15. 备注

| 备注项 | 内容 |
|--------|------|
| 澄清轮次 | |
| 参与人员 | |
| 遗留问题 | |

---

## 变更记录

| 日期 | 修改人 | 修改内容 | 版本 |
|------|--------|---------|------|
| | | | v1.0 |

---

## 关联文档

| 文档类型 | 文档名称 | 路径 |
|---------|---------|------|
| 功能需求文档 | feature.md | `../../feature.md` |
| 需求主文档 | upgrade-*.md | `../upgrade-*.md` |
| 子功能文档 | sf-*.md | `../sub-features/` |
| 项目上下文 | project.md | `.claude/context/project.md` |
| 技术栈 | tech-stack-profile.md | `.claude/context/tech-stack-profile.md` |
| 一致性基线 | consistency-baseline.md | `.claude/context/consistency-baseline.md` |