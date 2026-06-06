# Test Code Review 审查清单
- 触发条件：阶段 4 QA-Test-Coding 完成后，由架构师执行 Test Code Review
- 适用 Agent：architect-stage4

## 输入
- QA 提交的测试代码（单元测试 + 集成测试）
- 关联的 ADR § 5.4 API 设计 + § 12 测试策略
- 开发者提交的 production code（git diff）

## 输出
- Test Code Review 结果：APPROVED / REJECTED / CONDITIONAL
- 驳回清单（如有）
- 建议项清单（如有）

## 审查步骤

### 1. 测试覆盖完整性
- [ ] 是否覆盖所有 Gherkin AC 场景？
- [ ] 边界条件（空值、边界值、异常）是否有测试？
- [ ] 集成测试是否覆盖模块间调用关系？

### 2. 测试质量
- [ ] 测试是否独立（无状态泄漏、顺序依赖）？
- [ ] 断言是否精确（不只用 `assertTrue`，应有具体期望值）？
- [ ] Mock/Stub 是否合理（不过度 mock、不欠 mock）？

### 3. 可维护性
- [ ] 测试命名是否清晰描述场景？
- [ ] 是否有重复 setup 可提取到 fixture？
- [ ] 测试运行时间是否可接受？

## 审查结果定义

| 结果 | 条件 |
|------|------|
| **APPROVED** | 所有检查项通过 |
| **CONDITIONAL** | 有建议项，QA 可选择采纳 |
| **REJECTED** | 有阻塞项，QA 必须修复后重新提交 |

## 禁止事项
- 禁止要求与 ADR § 12 测试策略冲突的修改
- 禁止要求覆盖 ADR 未声明的非功能性需求
