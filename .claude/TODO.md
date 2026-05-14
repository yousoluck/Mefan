# TODO.md - Mefan 框架开发待办事项

> Last updated: 2026-05-14

---

## 需求（Requirements）

### R1: Claude Code 配置迁移（init.sh 功能）

- **描述**：Mefan 项目完工后，由 init.sh 脚本将 `.mefan` 框架文件迁移到 `.claude` 目录，以匹配 Claude Code 工具的目录结构。
- **前置条件**：Mefan 框架开发完成，所有功能测试通过
- **执行者**：init.sh 脚本
- **要求**：
  1. 迁移时保持文件路径一致性
  2. 所有文件内对特定路径的引用（如 `.mefan/rules/` → `.claude/rules/`）必须同步更新
  3. 迁移完成后，`.mefan` 目录可以保留作为备份，或由 init.sh 清理

---

## 待办任务（Tasks）

### T1: init.sh 迁移脚本开发

- [ ] 编写 init.sh 脚本，实现以下功能：
  - [ ] 创建 `.claude/` 目录结构（agents/、commands/、rules/、skills/、templates/）
  - [ ] 从 `.mefan/` 复制框架文件到 `.claude/`
  - [ ] 扫描所有文件，替换路径引用（.mefan/rules/ → .claude/rules/）
  - [ ] 验证迁移后文件完整性

### T2: 路径引用一致性检查

- [ ] 检查所有文件中是否有对 `.mefan/` 的硬编码引用
- [ ] 确认 init.sh 会处理这些引用

---

## 备注

- 当前开发在 `.mefan/` 目录下进行
- `.claude/` 目录已删除，等 init.sh 完工后由脚本重建
- 所有文件中的路径引用必须使用相对路径或占位符，便于迁移时替换