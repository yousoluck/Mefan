# 日志格式片段（所有 Agent 复用）

> 本文件为共享片段，所有 Agent 在执行任何原子步骤前后必须调用日志。
> 在 Agent 文件的 ## 日志声明 部分引用：`!.claude/snippets/logging-boilerplate.md`

## 日志命令格式

执行任何原子步骤前后，必须调用日志：

```bash
# 步骤开始
bash $ROOT/hooks/log-event.sh "<阶段>" "$AGENT_NAME" "步骤开始" "<描述>" "" ""

# 步骤完成
bash $ROOT/hooks/log-event.sh "<阶段>" "$AGENT_NAME" "步骤完成" "<描述>" "" "成功"

# 加载规则/技能时
bash $ROOT/hooks/log-event.sh "<阶段>" "$AGENT_NAME" "规则加载" "加载 <文件名>" "<文件名>" "成功"

# 产出文件时
bash $ROOT/hooks/log-event.sh "<阶段>" "$AGENT_NAME" "产出物" "生成 <文件路径>" "<文件路径>" "成功"

# 异常时
bash $ROOT/hooks/log-event.sh "<阶段>" "$AGENT_NAME" "异常" "<描述>" "" "失败"
```

## 占位符说明

| 占位符 | 含义 | 示例 |
|--------|------|------|
| `<阶段>` | 当前阶段编号（两位数） | `00`, `01`, `02` |
| `$AGENT_NAME` | Agent 名称（固定值） | `PM`, `Architect`, `DEV` |
| `<描述>` | 操作的简要描述 | `session-status初始化`, `技术栈分析` |
| `<文件名>` | 加载的规则/技能文件名 | `graphify-query-cheatsheet.md` |
| `<文件路径>` | 生成的产出物完整路径 | `.claude/context/tech-stack-profile.md` |

## 变量定义

在每个 Agent 文件开头应定义：

```markdown
## 变量定义
AGENT_NAME="PM"  # 或 "Architect", "DEV" 等
ROOT="/mnt/d/pycharmprojects/Mefan"
```

## 使用方式

在 Agent 文件中引用：

```markdown
## 日志声明
> 引用：!.claude/snippets/logging-boilerplate.md

## 变量定义
AGENT_NAME="PM"
ROOT="/mnt/d/pycharmprojects/Mefan"

## 操作步骤
### PM-操作-1：环境确认
1. bash $ROOT/hooks/log-event.sh "00" "$AGENT_NAME" "步骤开始" "环境确认" "" ""
2. [执行具体操作]
3. bash $ROOT/hooks/log-event.sh "00" "$AGENT_NAME" "步骤完成" "环境确认" "" "成功"
```