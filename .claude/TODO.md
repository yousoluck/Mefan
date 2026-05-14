# TODO.md - Mefan 框架开发待办事项

> Last updated: 2026-05-14

---

## ✅ 已完成（Completed）

### C1: 目录结构迁移
- [x] `.mefan/` 已迁移到 `.claude/`
- [x] 所有 `.mefan/` 路径引用已更新为 `.claude/`

### C2: 路径引用更新
- [x] `CLAUDE.md` - 日志命令路径已更新
- [x] `files-create.md` - 所有路径已更新
- [x] `rules/global/logging.md` - 日志命令路径已更新
- [x] `rules/global/evolution-process.md` - 提案路径已更新
- [x] `templates/session-status-template.md` - 路径已更新
- [x] 所有 `commands/mf-upgrade:*.md` - 已重命名
- [x] README.md 更新 - 目录结构说明

---

## 📋 待办（Pending）

### T1: 开源框架集成规划

**目标**：将 Mefan 与 OpenSpec/Gstack/SStack 集成融合，打造完整的 AI 工程化开发栈。

**集成架构**：

```
Mefan (流程引擎)
    ├── 输入层 → OpenSpec/Spec Kit (需求规范)
    ├── 执行层 → Mefan (阶段流程 + Agent 协作)
    └── 输出层 → Gstack/Tabario (SDLC 集成) + SStack (UI 设计认知)
```

**分层职责**：

| 层级 | 框架 | 职责 | 集成接口 |
|------|------|------|----------|
| 需求输入 | OpenSpec | 需求规范编写、验收标准定义 | 阶段1读取 `.md` 文件 |
| 流程引擎 | Mefan | 7阶段执行、Agent编排、门禁控制 | 核心框架 |
| SDLC集成 | Gstack/Tabario | Linear/Jira Issue追踪、PR/MR管理 | 阶段3/4 调用 `gh` CLI |
| UI设计 | SStack | 设计稿认知、设计规范提取 | 阶段2 Architecture 参考 |

**实施步骤**：

1. **Phase 1 - OpenSpec 集成**
   - 研究 OpenSpec 规范格式
   - 在阶段1 (Requirements) 中支持读取 OpenSpec 格式
   - 输出适配器 `.claude/adapters/openspec-loader.md`

2. **Phase 2 - Gstack/Tabario 集成**
   - 研究 Gstack 的 Linear/Issue 追踪 API
   - 在阶段3 (Plan) 中实现 Issue → Task 自动转换
   - 在阶段4 (Implement) 中实现 PR 状态同步
   - 输出适配器 `.claude/adapters/gstack-sync.md`

3. **Phase 3 - SStack 集成**
   - 研究 SStack 的设计稿认知能力
   - 在阶段2 (Arch-QA) 中支持设计稿解析
   - 输出适配器 `.claude/adapters/sstack-design.md`

4. **Phase 4 - 统一接口层**
   - 定义标准适配器接口 `.claude/interfaces/adapter-protocol.md`
   - 实现配置化加载机制

---

## 备注

- 框架文件位于 `.claude/` 目录
- Hooks 和 scripts 位于 `.claude/hooks/`
- 日志文件位于 `../logs/conversation-log.md`