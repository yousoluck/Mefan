# mefan Harness 宪法
SCENARIO=upgrade
CURRENT_STAGE=0
知识库路径：.claude/rules/
Skills 路径：.claude/skills/
图谱目录：graphify-out/

## 对话日志（强制执行）
> ⚠️ **每次对话结束时，AI 必须自动执行日志记录，无需用户提醒**

- **日志文件**：`../logs/conversation-log.md`
- **执行时机**：对话结束时（即 AI 回复用户后）
- **执行命令**：
  ```bash
  bash .claude/hooks/conversation-log.sh "assistant" "<用户输入>" "<AI回复摘要>" "<执行的操作>"
  ```
- **记录内容**：时间戳、用户输入、AI回复摘要、执行的操作

## 调试与日志
- 框架运行日志：`iterations/mefan-log.md`
- 所有 Agent 必须按照 `.claude/rules/global/logging.md` 写入日志。
- 日志命令：`bash .claude/hooks/log-event.sh <阶段> <Agent> <事件类型> <描述> <关联> <结果>`
EOFCLAUDE
- 日志文件可随时查看，用于排查框架运行问题。
