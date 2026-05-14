# Hook 与守护者边界定义
- type: guideline
- severity: warning

## Hook 定义
- 自动化脚本，由 Claude Code 的 `PostToolUse` 事件触发。
- 执行固定规则检查（命名、风格、diff 大小、API 签名）。
- 输出 `violations.json`，无推理能力。

## 守护者定义
- 具有 AI 推理能力的 Agent。
- 读取 `violations.json` + 完整代码 + 需求/设计文档。
- 执行深度语义审查，输出 APPROVED/REJECTED/CONDITIONAL。

## 交互合约
- Hook 发现违规 → 开发者修复 → 修复后 Hook 重跑通过。
- 任务完成 → 守护者审查 → 若 REJECTED，开发者修复 → 重新提交 CR。
- Hook 的失败不会直接合并阻断，但会触发开发者修复循环；守护者的 REJECTED 直接阻断任务完成。