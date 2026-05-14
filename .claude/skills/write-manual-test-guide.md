# 生成人工测试指南
- 触发条件：阶段 5 QA 需要生成人工测试用例
- 适用 Agent：QA

## 输入
- `sprint-status.md`（获取任务完成状态）
- `task-summary/` 目录（获取本次实现的功能清单）
- `iteration-plan.md`（获取原始计划）
- 需求文档 `.claude/iterations/{sprint-name}/requirements/*.md`

## 输出
- `.claude/iterations/{sprint-name}/test-results/manual-test-guide.md`
- 必须使用 `.claude/templates/manual-test-guide-template.md`

## 操作步骤

### 1. 提取功能清单
1. 读取 sprint-status.md 中所有 Done 状态的任务
2. 读取对应 task-summary/*.md
3. 列出本次实现的所有功能及对应文件路径

### 2. 编写测试用例
对每个功能，编写至少 3 个测试用例：

| 用例类型 | 说明 |
|---------|------|
| 正常 | 典型操作路径，预期正常响应 |
| 边界 | 临界值、空输入、最大值等 |
| 异常 | 错误输入、异常条件、错误处理 |

**每个用例必须包含**：
- 操作步骤（具体可执行）
- 预期结果（可验证）
- 测试数据（具体值）

### 3. 列出受影响模块回归测试
识别本次变更可能影响的老模块
为每个模块编写回归测试步骤

### 4. 说明测试环境搭建
- 依赖服务/数据库
- 配置要求
- 启动步骤

### 5. 输出到模板
按 `.claude/templates/manual-test-guide-template.md` 格式输出

## 禁止事项
- 禁止遗漏任何已实现功能
- 禁止使用模糊的步骤描述（如"输入正确数据"）
- 禁止跳过异常路径测试用例