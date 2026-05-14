# 日志与调试规则
- type: constraint
- severity: error

## 日志文件
- 路径：`iterations/mefan-log.md`
- 格式：每条日志一个 Markdown 表格行，追加写入，禁止覆盖。

## 必须记录日志的时机
1. 进入/退出阶段
2. 加载每条 Rule 或 Skill 时
3. 开始/完成原子步骤
4. 生成正式文档
5. 任何异常或阻断
6. Human Gate 提交/通过
格式：bash .claude/hooks/log-event.sh <阶段> <Agent> <事件类型> <描述> <关联> <结果>