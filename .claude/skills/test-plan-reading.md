# Test Plan 阅读指南
- 触发条件：QA-Test-Coding / Test Code Review / Testing 阶段开始时
- 适用 Agent：qa-stage4, qa-fix-stage4

## 输入
- `.claude/iterations/sprint-latest/test-plan.md`

## 输出
- 对当前 MG / Task 应执行测试项的完整理解
- 自动化 vs 人工测试划分

## 阅读步骤

### 1. 总览章节
- 读取 § 1 测试策略总览，理解本次迭代的测试重点
- 确认 P0 关键路径的覆盖要求
- 标记需人工探索性测试的模块

### 2. 自动化测试清单
- 读取 § 3 自动化测试用例，提取待执行列表
- 对照 git diff 确认每个用例的代码已就绪
- 标记需 QA-Test-Coding 补写的缺失用例

### 3. 人工测试指南
- 读取 § 4 人工测试用例，识别需手动执行的场景
- 准备测试数据和操作步骤
- 标记环境依赖（数据库、Mock 服务、第三方 API）

## 关联文档

| 文档 | 用途 |
|------|------|
| `.claude/iterations/sprint-latest/ADR.md` | 理解 API 设计与错误码 |
| `.claude/iterations/sprint-latest/requirements/*.md` | 理解 User Story 与 AC |
| `.claude/iterations/sprint-latest/sprint-status.md` | 确认当前 MG 状态 |

## 禁止事项
- 禁止跳过 § 1 测试策略总览直接执行
- 禁止未对照 § 3 自动化测试清单就开始补写
