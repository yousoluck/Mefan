1. 目录结构
   1. 项目根目录/
    ├── .harness/                       # 【框架专属根目录，与 .claude 解耦】
    │   ├── CLAUDE.md                   # 项目宪法（含 SCENARIO 变量）
    │   ├── HARNESS_VERSION.md          # 框架版本
    │   ├── agents/                     # Agent 角色提示词
    │   │   ├── pm.md
    │   │   ├── architect.md
    │   │   ├── analyst.md
    │   │   ├── developer.md
    │   │   ├── qa.md
    │   │   └── guardian.md
    │   ├── commands/                   # Command 入口文件
    │   │   ├── project-upgrade/
    │   │   │   ├── 00-init.md
    │   │   │   ├── 01-requirements.md
    │   │   │   └── ...
    │   │   ├── project-refactor/
    │   │   └── project-new/
    │   ├── knowledge/                  # Rules 和 Skills 统一存储
    │   │   ├── global/                 # 全局通用
    │   │   │   ├── session-init.md
    │   │   │   ├── quality-gates.md
    │   │   │   ├── exception-handling.md
    │   │   │   ├── tech-debt-management.md
    │   │   │   └── harness-version-control.md
    │   │   ├── scenario-upgrade/       # 二次开发场景专用
    │   │   │   ├── consistency-first.md
    │   │   │   ├── api-compatibility.md
    │   │   │   └── reuse-before-build.md
    │   │   └── scenario-refactor/      # 重构专用
    │   │       ├── behavior-freeze.md
    │   │       └── ...
    │   ├── skills/                     # 能力库
    │   │   ├── graphify-query-cheatsheet.md
    │   │   ├── query-third-party-docs.md
    │   │   ├── git-workflow.md
    │   │   └── ...
    │   ├── hooks/                      # 自动化检查脚本
    │   │   ├── check-consistency.py
    │   │   └── ...
    │   ├── templates/                  # 所有产出物的标准模板
    │   │   ├── session-status-template.md
    │   │   ├── tech-stack-profile-template.md
    │   │   ├── consistency-baseline-template.md
    │   │   ├── requirements-template.md
    │   │   ├── adr-template.md
    │   │   ├── test-plan-template.md
    │   │   ├── iteration-plan-template.md
    │   │   ├── sprint-status-template.md
    │   │   ├── task-summary-template.md
    │   │   ├── quality-report-template.md
    │   │   ├── manual-test-guide-template.md
    │   │   ├── bug-log-template.md
    │   │   ├── iteration-retrospective-template.md
    │   │   └── evolution-proposal-template.md
    │   └── settings.json               # Hook 和 MCP 配置
    ├── graphify-out/                   # 知识图谱输出（由 Graphify 生成）
    └── src/                            # 项目业务代码（已有）

2. 
层级	                 文件	               状态
Agent	           agents/pm.md	        ✅ 已加固
                   agents/architect.md	✅ 已加固
                   agents/analyst.md	✅ 已加固
                   agents/developer.md	⬜ 占位
                   agents/qa.md	        ⬜ 占位
                   agents/guardian.md	⬜ 占位
Command	           commands/project-upgrade/00-init.md	✅ 已加固
                   commands/project-upgrade/01-requirements.md	✅ 已加固
                   commands/project-upgrade/02-arch-qa.md	⬜ 未开始
                   commands/project-upgrade/03-plan.md	⬜ 未开始
                   commands/project-upgrade/04-implement.md	⬜ 未开始
                   commands/project-upgrade/05-quality.md	⬜ 未开始
                   commands/project-upgrade/06-retrospect.md	⬜ 未开始
Template	       templates/session-status-template.md	✅
                   templates/tech-stack-profile-template.md	✅
                   templates/consistency-baseline-template.md	✅
                   templates/requirements-template.md	✅ 已加固
                   templates/adr-template.md	✅ 核心占位
                   templates/test-plan-template.md	✅ 核心占位
                   templates/iteration-plan-template.md	✅ 核心占位
                   templates/sprint-status-template.md	✅ 核心占位
                   templates/task-summary-template.md	✅ 核心占位
                   templates/quality-report-template.md	⬜ 未开始
                   templates/manual-test-guide-template.md	⬜ 未开始
                   templates/bug-log-template.md	⬜ 未开始
                   templates/iteration-retrospective-template.md	⬜ 未开始
                   templates/evolution-proposal-template.md	⬜ 未开始
Rule	           knowledge/global/session-init.md	✅
                   knowledge/scenario-upgrade/consistency-first.md	✅
                   knowledge/scenario-upgrade/api-compatibility.md	✅
                   knowledge/scenario-upgrade/reuse-before-build.md	✅
                   knowledge/global/conflict-resolution.md	⬜ 未开始
                   knowledge/global/exception-handling.md	⬜ 未开始
                   knowledge/global/tech-debt-management.md	⬜ 未开始
                   knowledge/global/hook-vs-guardian.md	⬜ 未开始
                   knowledge/global/harness-version-control.md	⬜ 未开始
                   knowledge/global/quality-gates.md	⬜ 未开始
Skill	           skills/graphify-query-cheatsheet.md	✅ 核心
                   skills/git-workflow.md	✅ 占位
                   skills/query-third-party-docs.md	✅ 占位
                   skills/tdd-red-green-refactor.md	⬜ 未开始
                   skills/code-review-checklist.md	⬜ 未开始
                   skills/write-manual-test-guide.md	⬜ 未开始
                   skills/bug-triage-classification.md	⬜ 未开始
                   skills/root-cause-analysis.md	⬜ 未开始
                   Hook	hooks/check-consistency.py	⬜ 占位（待实现）
初始化	           init-mefan-harness.sh	✅ 已提供