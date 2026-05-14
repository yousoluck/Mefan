# 生成人工测试指南
- 触发条件：阶段 5 QA 执行
- 适用 Agent：QA

## 步骤
1. 从 `sprint-status.md` 和 `task-summary/` 提取本次实现的功能清单。
2. 对每个功能，编写至少 3 个测试用例（正常/边界/异常）。
3. 每个用例必须包含：操作步骤（具体可执行）、预期结果（可验证）。
4. 列出受影响的旧模块回归步骤。
5. 明确测试环境搭建方法。
6. 输出到 `templates/manual-test-guide-template.md`。