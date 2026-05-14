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
- [x] 所有 `commands/project-upgrade/*.md` - 路径已更新

---

## 🔄 进行中（In Progress）

### I1: 初始化脚本更新
- [ ] `init.sh` 需要更新为将文件复制到 `.claude/` 而不是 `.mefan/`
- [ ] `init.sh` 中的路径替换逻辑需要从 `.mefan` → `.claude`

---

## 📋 待办（Pending）

### T1: 验证完整性
- [ ] 检查所有更新后的路径对应的文件是否真实存在
- [ ] 运行 `/project-upgrade:auto` 验证框架正常工作

### T2: README.md 更新
- [x] 更新 README.md 中对 `.mefan/` 的引用为 `.claude/`
- [x] 更新目录结构说明

---

## 备注

- 所有文件内的 `.mefan/` 硬编码引用已替换为 `.claude/`
- 框架文件实际位于 `.claude/` 目录
- Hooks 和 scripts 位于 `.claude/hooks/`