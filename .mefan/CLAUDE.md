# mefan Harness 宪法
SCENARIO=upgrade
CURRENT_STAGE=0
知识库路径：knowledge/
Skills 路径：skills/
图谱目录：graphify-out/

## 调试与日志
- 日志文件：`iterations/mefan-log.md`
- 所有 Agent 必须按照 `knowledge/global/logging.md` 写入日志。
- 日志命令：`bash .mefan/hooks/log-event.sh <阶段> <Agent> <事件类型> <描述> <关联> <结果>`
EOFCLAUDE
- 日志文件可随时查看，用于排查框架运行问题。
