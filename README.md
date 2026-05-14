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
    │   │   │   ├── 02-arch-qa.md
    │   │   │   ├── 03-plan.md
    │   │   │   ├── 04-implement.md
    │   │   │   ├── 05-quality.md
    │   │   │   ├── 06-retrospect.md
    │   │   │   └── auto.md
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
    │   │   ├── tdd-red-green-refactor.md
    │   │   ├── code-review-checklist.md
    │   │   ├── write-manual-test-guide.md
    │   │   ├── ug-triage-classification.md
    │   │   ├── root-cause-analysis.md
    │   │   └── pattern-extraction-from-logs.md
    │   ├── hooks/                      # 自动化检查脚本
    │   │   ├── check-consistency.py
    │   │   └── log-event.sh
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
    │   ├── settings.json                      # Hook/MCP 配置
    │   ├── context/                           # 全局技术上下文（跨迭代共享）
    │   │   ├── tech-stack-profile.md
    │   │   └── consistency-baseline.md
    │   ├── iterations/                        # 迭代总目录
    │   │   ├── mefan-log.md                   # 全局日志
    │   │   ├── sprint-2026-05-14/             # 单个迭代
    │   │   │   ├── session-status.md
    │   │   │   ├── requirements/
    │   │   │   │   └── upgrade-2026-05-14-xxx.md
    │   │   │   ├── adr/
    │   │   │   │   └── upgrade-2026-05-14-xxx.md
    │   │   │   ├── test-plan/
    │   │   │   │   └── upgrade-2026-05-14-xxx.md
    │   │   │   ├── sprint-status.md
    │   │   │   ├── iteration-plan.md
    │   │   │   ├── task-summary/
    │   │   │   │   ├── T001.md
    │   │   │   │   └── ...
    │   │   │   ├── test-results/
    │   │   │   │   ├── regression-2026-05-14.log
    │   │   │   │   ├── manual-test-guide.md
    │   │   │   │   └── unit-T001.log
    │   │   │   ├── bug-log/
    │   │   │   │   ├── auto-2026-05-14.md
    │   │   │   │   └── manual-2026-05-14.md
    │   │   │   └── retrospective.md
    │   │   └── sprint-2026-05-28/
    │   │       └── ...
    │   ├── evolution-proposals/               # 进化提案
    │   │   └── upgrade-2026-05-14.md
    │   └── reports/                           # 人类可读报告
    │       └── PROJECT_STATUS.md
    └── graphify-out/                          # 知识图谱（由工具生成，非框架文件）

2.
层级	                 文件	               状态
Agent	           agents/pm.md	        ✅ 已加固
                   agents/architect.md	✅ 已加固
                   agents/analyst.md	✅ 已加固
                   agents/developer.md	✅ 已加固
                   agents/qa.md	        ✅ 已加固
                   agents/guardian.md	✅ 已加固
                   agents/coach.md	    ✅ 已加固
Command	           commands/project-upgrade/00-init.md	✅ 已加固
                   commands/project-upgrade/01-requirements.md	✅ 已加固
                   commands/project-upgrade/02-arch-qa.md	✅ 已加固
                   commands/project-upgrade/03-plan.md	✅ 已加固
                   commands/project-upgrade/04-implement.md	✅ 已加固
                   commands/project-upgrade/05-quality.md	✅ 已加固
                   commands/project-upgrade/06-retrospect.md	✅ 已加固
                   commands/project-upgrade/auto.md	✅ 已加固
Template	       templates/session-status-template.md	✅
                   templates/tech-stack-profile-template.md	✅
                   templates/consistency-baseline-template.md	✅
                   templates/requirements-template.md	✅ 已加固
                   templates/adr-template.md	✅ 已加固
                   templates/test-plan-template.md	✅ 已加固
                   templates/iteration-plan-template.md	✅ 已加固
                   templates/sprint-status-template.md	✅ 已加固
                   templates/task-summary-template.md	✅ 已加固
                   templates/quality-report-template.md	✅ 已加固
                   templates/manual-test-guide-template.md	✅ 已加固
                   templates/bug-log-template.md	✅ 已加固
                   templates/iteration-retrospective-template.md	✅ 已加固
                   templates/evolution-proposal-template.md	✅ 已加固
                   templates/log-entry-template.md	✅ 已加固
                   templates/project-status-template.md	✅ 已加固
Rule	           knowledge/global/session-init.md	✅
                   knowledge/scenario-upgrade/consistency-first.md	✅
                   knowledge/scenario-upgrade/api-compatibility.md	✅
                   knowledge/scenario-upgrade/reuse-before-build.md	✅
                   knowledge/global/conflict-resolution.md	✅ 已加固
                   knowledge/global/exception-handling.md	✅ 已加固
                   knowledge/global/tech-debt-management.md	✅ 已加固
                   knowledge/global/hook-vs-guardian.md	✅ 已加固
                   knowledge/global/harness-version-control.md	✅ 已加固
                   knowledge/global/quality-gates.md	✅ 已加固
                   knowledge/global/logging.md	✅ 已加固
Skill	           skills/graphify-query-cheatsheet.md	✅ 核心
                   skills/git-workflow.md	✅ 已加固
                   skills/query-third-party-docs.md	✅ 已加固
                   skills/tdd-red-green-refactor.md	✅ 已加固
                   skills/code-review-checklist.md	✅ 已加固
                   skills/write-manual-test-guide.md	✅ 已加固
                   skills/ug-triage-classification.md	✅ 已加固
                   skills/root-cause-analysis.md	✅ 已加固
                   skills/pattern-extraction-from-logs.md	✅ 已加固
Hook	           hooks/check-consistency.py	✅ 已提供
                   hooks/log-event.sh	✅ 已提供
初始化	           init-mefan-harness.sh	✅ 已提供