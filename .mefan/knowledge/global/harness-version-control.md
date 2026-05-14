# 框架版本管理
- type: constraint
- severity: error

## 版本文件
- 根目录 `HARNESS_VERSION.md` 记录当前框架版本。
- 格式：`v<MAJOR>.<MINOR>.<PATCH>`

## 版本递增规则
- MAJOR：框架核心流程或角色发生结构性变化。
- MINOR：新增场景、新增阶段、新增 Rule/Skill。
- PATCH：修正现有文件、加固指令、修复框架缺陷。

## 更新时机
- 阶段 6 结束时，PM 必须评估是否需递增版本。
- 若合并了进化提案，至少递增 PATCH。