# mefan Harness 宪法
SCENARIO=upgrade
CURRENT_STAGE=0
ROOT=/mnt/d/pycharmprojects/Mefan
知识库路径：.claude/rules/
Skills 路径：.claude/skills/
图谱目录：graphify-out/

## 对话日志（强制执行）
> ⚠️ **每次对话结束时，AI 必须显式执行日志记录，无需用户提醒**

- **日志文件**：`../logs/conversation-log.md`
- **执行时机**：对话结束时（即 AI 回复用户后）
- **执行命令**：
  ```bash
  bash /mnt/d/pycharmprojects/Mefan/.claude/hooks/conversation-log.sh "assistant" "<用户输入>" "<AI回复摘要>" "<执行的操作>"
  ```
- **记录内容**：时间戳、用户输入、AI回复摘要、执行的操作

## Agent 激活规则
> 当 Command 文件激活 Agent 时，必须遵循以下规则：

### 自动加载机制
当激活 `agents/<role>-stage<N>.md` 时：
1. **读取 Agent 文件声明**：打开对应的 Agent 文件
2. **加载声明的 Rules**：按 `## 需要的规则` section 引用加载
3. **加载声明的 Skills**：按 `## 需要的技能` section 引用加载
4. **按需引用**：不在阶段开头集中声明，在具体操作步骤中按需引用

### Agent 文件结构要求
每个 Agent 文件必须包含：
```markdown
## 需要的技能
- `.claude/skills/xxx.md`

## 需要的规则
- `.claude/rules/xxx.md`
```

### 示例
激活 `agents/pm-stage6.md` 时：
1. 读取 `agents/pm-stage6.md`
2. 发现声明 `.claude/rules/global/harness-version-control.md` → 加载该规则
3. 发现声明 `.claude/rules/global/tech-debt-management.md` → 加载该规则
4. 按 Agent 文件内的操作步骤执行

## 调试与日志
- 框架运行日志：`iterations/mefan-log.md`
- 所有 Agent 必须按照 `.claude/rules/global/logging.md` 写入日志。
- 日志命令：`bash .claude/hooks/log-event.sh <阶段> <Agent> <事件类型> <描述> <关联> <结果>`
EOFCLAUDE
- 日志文件可随时查看，用于排查框架运行问题。
