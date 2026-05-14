# Git 工作流
- 触发条件：阶段 4 开发者创建分支、提交代码时
- 适用 Agent：开发者

## 输入
- 当前任务 ID（如 T001）
- 任务短描述（来自 iteration-plan.md）

## 输出
- Git 特性分支名：`feature/<task-id>-<short-desc>`
- Commit message 格式：`[<task-id>] <type>: <description>`

## 操作步骤

### 1. 创建特性分支
```bash
git checkout -b feature/<task-id>-<short-desc>
```
例如：`git checkout -b feature/T001-user-login`

### 2. 提交 Commit 格式
```bash
git add <files>
git commit -m "[<task-id>] <type>: <description>"
```

**type 类型**：
| type | 使用场景 |
|------|---------|
| feat | 新功能 |
| fix | Bug 修复 |
| docs | 文档变更 |
| refactor | 重构（无行为改变） |
| test | 测试相关 |
| chore | 构建/工具/依赖 |

**示例**：
```bash
git commit -m "[T001] feat: 实现用户登录 API"
git commit -m "[T002] fix: 修复会话超时验证问题"
```

### 3. 推送分支
```bash
git push -u origin feature/<task-id>-<short-desc>
```

### 4. 创建 PR/MR（可选）
根据项目流程，使用 `gh pr create` 或手动在 GitHub/GitLab 创建 Pull Request。

## 禁止事项
- 禁止直接在 main/master 分支提交
- 禁止提交包含密钥或敏感信息的代码
- 禁止提交未通过 Hook 检查的代码