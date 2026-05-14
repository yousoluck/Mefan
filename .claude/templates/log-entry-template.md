# 日志条目模板
> 文件：`.claude/iterations/{sprint-name}/logs/mefan-log.md`（追加写入）
> 用途：每次记录一行日志，按此格式追加到文件末尾

## 使用说明
- **文件位置**：`iterations/{sprint-name}/logs/mefan-log.md`
- **写入方式**：追加模式，每次写入一行，不覆盖已有内容
- **写入时机**：阶段进入/退出、Human Gate 审批、异常发生、关键决策

## 字段说明

| 字段 | 说明 | 示例 |
|------|------|------|
| 时间戳 | ISO 8601 格式 | 2026-05-14T10:30:00 |
| 阶段 | 0-6 | 4 |
| Agent | PM/Architect/Developer/QA/Guardian/Coach | PM |
| 事件类型 | 阶段进入/阶段退出/Human Gate/异常/决策 | 阶段退出 |
| 描述 | 简要描述 | 进入阶段4 |
| 关联 | 关联的文件/规则/技能 | session-status.md |
| 结果 | 成功/失败/阻塞 | 成功 |

## 示例行
```
| 2026-05-14T10:30:00 | 4 | PM | 阶段进入 | 进入阶段4-迭代实现 | iteration-plan.md | 成功 |
| 2026-05-14T11:45:00 | 4 | Developer | Hook拦截 | check-consistency发现3条违规 | violations.json | 待修复 |
```

## 注意
- 每行一个日志条目
- 不含表头，表头仅在文件首次创建时写入
- 关联字段若无具体文件填 `-`