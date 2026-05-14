# /project-upgrade:auto – 自动推进全流程
## 0. 日志声明（自动追加
执行本阶段所有步骤时，必须使用 `.mefan/hooks/log-event.sh` 记录日志。
- 进入阶段时：`bash .mefan/hooks/log-event.sh <阶段> <Agent> "阶段进入" "进入阶段X" "" "成功"`
- 结束阶段时：`bash .mefan/hooks/log-event.sh <阶段> <Agent> "阶段退出" "阶段X完成" "" "成功"`
- 在 Human Gate 前后记录审批事件

## 1. 角色激活
- **执行 Agent**：PM (`.claude/agents/pm.md`)，负责判断当前阶段、拉起对应 Command、断点续跑。

## 2. 前置输入（必须读取）
- `.mefan/iterations/{sprint-name}/session-status.md`（阶段状态 + US 状态 + 产出物追踪）
- `.mefan/iterations/{sprint-name}/sprint-status.md`（task 进度）
- `.mefan/iterations/mefan-log.md`（用于确认断点）

**执行前检查**：
1. 确认 `session-status.md` 存在，若不存在，报错退出。
2. 确认 `sprint-status.md` 存在（阶段 3 才创建）。

## 3. 执行流程

### 3.1 断点检查
读取 `.mefan/iterations/{sprint-name}/session-status.md`：

1. **读取 `## 自动推进状态`**：
   - 当前阶段：N
   - 已完成阶段：[0, 1, 2, ...]
   - 阻塞标记：{无 / 原因}

2. **若存在阻塞标记**：
   - 输出阻塞原因
   - 等待人类决策：重试 / 回退 / 跳过
   - 人类决策后清除阻塞标记，继续

3. **初始化**：若 `## 自动推进状态` 不存在，初始化为阶段 0。

### 3.2 阶段完成条件判断

**auto 用 session-status + sprint-status 共同判断**：

| 阶段 | 完成条件 | 判断依据 |
|------|---------|---------|
| 00-03 | 阶段产出物存在 | session-status 产出物追踪表 |
| **04** | **所有 task 都是 Done** | **sprint-status 任务看板** |
| 05 | 质量报告产出 | session-status 产出物追踪表 |
| 06 | 迭代总结产出 | session-status 产出物追踪表 |

**阶段 4 特殊判断**：
```
读取 sprint-status.md 的任务看板
统计状态为 Done 的 task 数
若 Done task 数 == 总 task 数 → 阶段 4 完成
否则 → 阶段 4 未完成，阻塞标记："阶段4进行中：X/N task 完成"
```

### 3.3 推进循环
从当前阶段开始，按序执行：

1. **检查当前阶段是否已完成**：
   - 阶段 0-3, 5-6：检查 session-status 产出物追踪表
   - 阶段 4：检查 sprint-status 所有 task 是否 Done
   - 若已完成，跳过，进入下一阶段

2. **执行前置条件验证**：
   - 阶段 N 的前置输入必须是阶段 N-1 的产出物
   - 验证这些产出物在 session-status 中标记为 ✅

3. **拉起对应 Command**：
   - 阶段 0：触发 `/project-upgrade:00-init`
   - 阶段 1：触发 `/project-upgrade:01-requirements`
   - 阶段 2：触发 `/project-upgrade:02-arch-qa`
   - 阶段 3：触发 `/project-upgrade:03-plan`
   - 阶段 4：触发 `/project-upgrade:04-implement`
   - 阶段 5：触发 `/project-upgrade:05-quality`
   - 阶段 6：触发 `/project-upgrade:06-retrospect`

4. **等待阶段完成 + PM 报告**：
   - 若阶段内包含 `[Human Gate]`，PM 等待用户 `APPROVED` 或 `继续`
   - 用户确认后，执行 3.4 更新状态

5. **进入下一阶段**

### 3.4 更新状态
**执行者**：PM

1. **更新 session-status.md**：
   - `## 自动推进状态`：当前阶段+1，已完成列表追加当前阶段
   - `## 阶段完成记录`：标记阶段 N 为 ✅
   - `## 产出物追踪表`：标记阶段 N 产出物为 ✅
   - `## PM 阶段完成报告`：按标准化格式填写

2. **更新 sprint-status.md**（若阶段 4 完成）：
   - 确认所有 task 都是 Done
   - 更新 User Story 进度汇总

3. **记录日志**：`bash .mefan/hooks/log-event.sh auto PM "阶段完成" "阶段N完成" "" "成功"`

### 3.5 异常处理
- 若阶段执行失败：
  1. 在 session-status 的 `## 自动推进状态` 记录 `阻塞标记：阶段N失败`
  2. 输出失败摘要
  3. 等待人类决策：重试 / 回退 / 跳过
- 若连续失败 3 次，终止自动流程，建议手动介入

## 4. 产出物
- 所有阶段的正常产出物
- 更新的 `session-status.md`（阶段状态 + PM 报告）
- 更新的 `sprint-status.md`（task 进度 + US 汇总）