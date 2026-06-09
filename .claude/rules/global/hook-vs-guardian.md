# Hook 与守护者边界定义
- type: guideline
- severity: warning

> **当前实现注**（2026-06-06）：本规则定义的"Hook 输出 `violations.json`"契约**未在当前实现中落地**。6 个 hook（`check-adr-implementation.sh` / `check-tdd-rhythm.sh` / `check-test-coverage.sh` / `check-incremental.sh` / `check-reference-consistency.sh` / `check-consistency.py` / `check-diff-size.py`）**全部只 echo 到 stdout + 追加到 `iterations/mefan-log.md`**，**没有任何 hook 写 `violations.json`**。`coach-stage6.md` 操作 1 已改用 `grep mefan-log.md` 解析（详见 superpowers-integration.md §J H5）。`violations.json` 保留为长期目标。

## Hook 定义
- 自动化脚本，由 Claude Code 的 `PostToolUse` 事件触发。
- 执行固定规则检查（命名、风格、diff 大小、API 签名）。
- **当前**：输出到 stdout + 追加到 `iterations/mefan-log.md`。
- **长期目标**：输出 `violations.json`（结构化 NDJSON），无推理能力。

## 守护者定义
- 具有 AI 推理能力的 Agent。
- 读取 `iterations/mefan-log.md`（或未来的 `violations.json`）+ 完整代码 + 需求/设计文档。
- 执行深度语义审查，输出 APPROVED/REJECTED/CONDITIONAL。

## 交互合约
- Hook 发现违规 → 开发者修复 → 修复后 Hook 重跑通过。
- 任务完成 → 守护者审查 → 若 REJECTED，开发者修复 → 重新提交 CR。
- Hook 的失败不会直接合并阻断，但会触发开发者修复循环；守护者的 REJECTED 直接阻断任务完成。