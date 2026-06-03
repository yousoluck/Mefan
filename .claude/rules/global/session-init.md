# 会话初始化规则
- type: constraint
- severity: error

1. 必须首先确认 CLaUDE.md 中的 SCENARIO 变量。
2. 必须检查 graphify-out/graph.json 是否存在，如不存在则执行 `/graphify .` 生成图谱；如已存在则执行 `/graphify . --update` 更新图谱。
3. 必须检查或创建 `session-status.md`。
