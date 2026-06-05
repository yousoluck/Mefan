# TEST-MEFAN.md — Mefan 框架自检测试流程

> **状态标记**：本测试套件标记为 **Stage 4 集成测试**（per pytest marker `@pytest.mark.stage4`）
> **来源**：superpowers 集成方案 v2.5.0 Layer 4 — Mefan dogfooding
> **位置**：`/mnt/d/pycharmprojects/Mefan/tests/`

---

## 1. 为什么是 Stage 4 测试，而不是独立测试？

Mefan 是一个 **7 阶段编排框架**：

```
00-init → 01-requirements → 02-arch-qa → 03-plan → 04-implement → 05-quality → 06-retrospect
```

**Stage 4（实现阶段）** 是整个框架最"重活"的阶段，承载：

- **7 状态机**（Dev → Self-Check → Code Review → QA-Test-Coding → Test Code Review → Testing → Close）
- **4 个 Hook**（check-state-machine / check-tdd-rhythm / check-test-coverage / check-adr-implementation）
- **5 个 Agent**（dev-stage4 / dev-fix-stage4 / architect-stage4 / qa-stage4 / pm-stage4）
- **6 个 superpowers Skill 调用点**（TDD / verification / debugging / code-review / receiving-review / finishing-branch）

任何"自检"测试必然要触及：

| 测试关注的对象 | 它的输入依赖 |
|---|---|
| 7 状态机 hook（check-state-machine.sh） | sprint-status.md（**来自 stage 3**） |
| TDD 节奏 hook（check-tdd-rhythm.sh） | git commit history（**来自 stage 4 自身**） |
| 覆盖率 hook（check-test-coverage.sh） | tests/ 目录 + src/ 目录（**来自 stage 4 自身**） |
| ADR 实现 hook（check-adr-implementation.sh） | ADR.md §7 任务列表（**来自 stage 2**） |
| Agent frontmatter（Skill 工具检查） | 22 个 agent 文件（**所有阶段**） |
| Skill 占位符引用（@superpowers/X） | superpowers 插件目录（**框架外部依赖**） |

**结论**：本测试套件 **无法在 stage 4 独立运行** —— 它需要 stage 2 的 ADR 形式 + stage 3 的 sprint-status.md 形式存在。我们通过 **pytest fixtures 模拟前置依赖**（见 §3），让测试可以在 CI/本地任何环境跑通。

因此，标记为 `@pytest.mark.stage4` 是因为：

1. **被测对象在 stage 4**（hooks + state machine + agents 的关键集成点）
2. **依赖前置 stage 2/3 的输出形式**（用 fixture 模拟）
3. **不能在框架未"跑过完整 7 阶段"的情况下证明 stage 4 正确**

---

## 2. 测试模块依赖图

```
                    ┌─────────────────────────────────────┐
                    │  conftest.py (shared fixtures)      │
                    │  - repo_root / agents_dir / hooks   │
                    │  - tmp_sprint / mock_adr            │
                    │  - mock_sprint_status               │
                    │  - mock_consistency_baseline        │
                    └─────────────────────────────────────┘
                                      ▲
                ┌─────────────────────┼─────────────────────┐
                │                     │                     │
        ┌───────┴───────┐    ┌───────┴───────┐    ┌────────┴───────┐    ┌──────────────────┐
        │ test_agent_   │    │ test_skill_   │    │ test_hooks.py  │    │ test_integration │
        │ frontmatter   │    │ references    │    │                │    │ .py (stage4)     │
        │               │    │               │    │                │    │                  │
        │ 零依赖        │    │ 零依赖        │    │ 零依赖         │    │ 依赖 fixtures    │
        │ 仅读 .md      │    │ 仅读 .md +    │    │ 调用 hook      │    │ + 真实 hooks/    │
        │               │    │  glob 检查    │    │ subprocess     │    │ + symlink        │
        └───────────────┘    └───────────────┘    └────────────────┘    └──────────────────┘
              ▼                     ▼                     ▼                       ▼
        ┌──────────────────────────────────────────────────────────────────────────────┐
        │  CI 友好（无 fixture 依赖）        │  Stage 4 集成（需 fixture/symlink）     │
        │  pytest -m "not stage4"            │  pytest -m stage4                       │
        └──────────────────────────────────────────────────────────────────────────────┘
```

### 模块说明

| 模块 | 关注的层 | 依赖 | 失败意味着 |
|---|---|---|---|
| `test_agent_frontmatter.py` | Layer 1 | 零依赖（只读 .md） | 某 agent 的 `tools:` 数组少 `Skill` 工具，无法调 superpowers skill |
| `test_skill_references.py` | Layer 2 | 零依赖 + superpowers 插件存在 | `@superpowers/X` 占位符指向不存在的 skill（如 `tdd-mastery` 不存在） |
| `test_hooks.py` | Layer 3 | 零依赖 + bash 可用 | hook 用了错误路径（`$ROOT/../tests`）静默 no-op |
| `test_integration.py` | Layer 4（端到端） | fixtures + symlink 写 `/mnt/d/...` | 7 状态机无法接受/拒绝某些状态，state machine 损坏 |

---

## 3. Pytest Fixture 树

定义在 `conftest.py`：

```
Fixture                          Scope        用途
─────────────────────────────────────────────────────────────────────────────────
repo_root                        session      项目根 `/mnt/d/pycharmprojects/Mefan`
agents_dir                       session      `.claude/agents/`
hooks_dir                        session      `.claude/hooks/`
skills_dir                       session      `.claude/skills/`
superpowers_dir                  session      superpowers 插件目录
                                              `/home/amdin/.claude/plugins/cache/...`
tmp_sprint                       function     模拟 `iterations/sprint-latest/`
                                              （含 reviews/、task-summary/ 空目录）
mock_adr                         function     最小 ADR.md（§2.4 MG 表、§5 API、§7 伪代码）
mock_sprint_status               function     最小 sprint-status.md（任务看板 + 状态机表）
mock_consistency_baseline        function     最小一致性基线（命名约定）
```

session-scope fixture 仅初始化一次，function-scope fixture 每个测试函数都重新构造。

---

## 4. 三种跑测模式

### 模式 A：零依赖快测（CI 默认）

```bash
cd /mnt/d/pycharmprojects/Mefan
pytest tests/test_agent_frontmatter.py \
       tests/test_skill_references.py \
       tests/test_hooks.py \
       -v
```

**适用场景**：
- CI/CD 流水线（每 PR 触发）
- 本地快速验证
- 改完 agent frontmatter 后回归

**期望耗时**：< 10 秒（纯文件读取，无 subprocess）

**通过条件**：
- ✅ 所有 22 个 agent 的 frontmatter 合法
- ✅ 所有 stage 4/5/6 agent 的 `tools` 包含 `Skill`
- ✅ 所有 `@superpowers/X` 占位符指向已安装的 v5.1.0 skill
- ✅ 3 个 hook 不再使用 `$ROOT/../tests` 错误路径

### 模式 B：Stage 4 集成测（本地深度验证）

```bash
pytest tests/test_integration.py -v -m stage4
```

**适用场景**：
- 阶段 4 hook 修改后
- 7 状态机逻辑变更后
- 在本机有 `/mnt/d/pycharmprojects/Mefan` 写权限时

**期望耗时**：~30-60 秒（涉及 symlink + 7 次 bash subprocess）

**通过条件**：
- ✅ check-state-machine.sh 接受 7 个合法状态（参数化测试）
- ✅ check-state-machine.sh 拒绝非法状态（如 `TotallyNotAState`）
- ✅ 静态分析：脚本声明完整的 7 状态转换表

**注意事项**：
- 该测试会临时创建 symlink `/mnt/d/pycharmprojects/Mefan/.claude/iterations/sprint-latest → tmp_path`
- 测试结束后会自动清理（finally 块）
- 如果原有 sprint-latest 是目录而非 symlink，会先 rename 备份后再恢复
- CI 跑不了（CI 没有 `/mnt/d/...` 路径），只能本地跑

### 模式 C：全测（发布前完整验证）

```bash
pytest tests/ -v
```

**适用场景**：
- 框架版本发布前（v2.5.0、v2.6.0 ...）
- evolution proposal 合并到主干前
- 任何"我改了 hook 或 agent 或 skill"的场景

**期望耗时**：~1-2 分钟

**通过条件**：模式 A + 模式 B 全部通过

---

## 5. 测试目标

### 短期目标（v2.5.0 集成 superpowers）

| 目标 | 衡量指标 | 测试模块 |
|---|---|---|
| Agent 解锁 Skill 工具 | 12 个 stage 4/5/6 agent 的 `tools` 包含 `Skill` | test_agent_frontmatter.py |
| 占位符真实化 | 6 个 `@superpowers/X` 占位符指向 v5.1.0 真实 skill | test_skill_references.py |
| Hook 复活 | 3 个 hook 不再 silent no-op | test_hooks.py |
| 7 状态机不退化 | 状态机能接受 7 个合法状态、拒绝非法状态 | test_integration.py |

### 长期目标（持续 dogfooding）

| 目标 | 触发时机 |
|---|---|
| 每个 PR 触发零依赖快测 | 集成 CI 后自动 |
| 每个 agent 修改回归 frontmatter 测试 | 触及 `.claude/agents/*.md` 的提交 |
| 每个 hook 修改触发 hook 测试 | 触及 `.claude/hooks/*.sh` 的提交 |
| 每个版本发布前跑 stage 4 集成测 | repo-maintainer 在 v2.x.x 发布前 |

---

## 6. 测试运行的 RED → GREEN 历程

按 superpowers TDD 铁律，本测试套件**先编写，后实现**：

### RED 阶段（baseline，本 plan 的 Step 1）

```bash
$ pytest tests/test_agent_frontmatter.py -v
======================== FAILED ============================
FAILED test_stage45_agent_has_skill_tool[dev-stage4]
       AssertionError: dev-stage4.md frontmatter is missing `Skill` in tools.
FAILED test_stage45_agent_has_skill_tool[architect-stage4]
       ...
FAILED test_stage45_agent_has_skill_tool[qa-stage4]
       ...
[12 tests failed, 0 passed]
```

```bash
$ pytest tests/test_skill_references.py -v
======================== FAILED ============================
FAILED test_all_superpowers_placeholders_resolve
       AssertionError: Broken `@superpowers/X` references:
         - dev-stage4.md: @tdd-mastery
         - architect-stage4.md: @code-review, @cupid-clean-code
         - qa-stage4.md: @test-automation
         - qa-stage5.md: @test-execution
[1 test failed]
```

```bash
$ pytest tests/test_hooks.py -v
======================== FAILED ============================
FAILED test_hook_uses_correct_tests_path[check-tdd-rhythm.sh]
       AssertionError: uses wrong path $ROOT/../tests
FAILED test_hook_uses_correct_tests_path[check-test-coverage.sh]
       ...
FAILED test_hook_uses_correct_tests_path[check-adr-implementation.sh]
       ...
[3 tests failed]
```

### GREEN 阶段（按 plan Step 2-9 修复后）

修复后期望：

```bash
$ pytest tests/ -v
======================== PASSED ============================
test_agent_has_valid_yaml_frontmatter      [22 PASSED]
test_agent_tools_are_known                  [22 PASSED]
test_stage45_agent_has_skill_tool           [12 PASSED]
test_stage0123_agent_has_skill_tool_rec.    [9 PASSED]
test_all_superpowers_placeholders_resolve   [1 PASSED]
test_no_raw_at_superpowers_in_agents        [1 PASSED]
test_stage45_agent_uses_at_least_one_skill  [12 PASSED]
test_hook_uses_correct_tests_path           [3 PASSED]
test_state_machine_script_exists            [1 PASSED]
test_state_machine_no_sprint_status_rc      [1 PASSED]
test_hook_warns_when_dirs_missing           [3 PASSED]
test_state_machine_accepts_each_of_7        [7 PASSED]  (stage4)
test_state_machine_static_check             [1 PASSED]  (stage4)
test_state_machine_rejects_invalid_state    [1 PASSED]  (stage4)
======================== 96 PASSED ========================
```

---

## 7. 与 mefan 流程的关系

本测试**完全独立于框架运行时**：

- 不参与 stage 0-6 编排
- 不被 PM agent 调用
- 不被 hook 触发
- 不出现在 sprint-status.md 看板
- **只在 CI 或开发者手动跑**

它是 **mefan 框架的元测试（meta-test）** —— 测试框架本身的完整性，不测试框架"产出物"的质量。

---

## 8. 维护责任

| 触发 | 谁负责更新测试 |
|---|---|
| 新增 agent 文件 | senior-developer 在 PR 中同步更新 `STAGE45_AGENTS_REQUIRING_SKILL` |
| 新增 superpowers skill 到 mefan | senior-developer 在 PR 中同步更新 placeholder 白名单 |
| 修改 hook 脚本 | qa-engineer 在改完后跑全测 |
| 修改 7 状态机 | architect 同步更新 `SEVEN_STATES` |
| superpowers 升级到 v5.2.0 | senior-developer 在升级 PR 中跑全测 |

---

## 9. 已知限制

1. **test_integration.py 需要 `/mnt/d/...` 路径**：CI 跑不了，仅本地跑
2. **未模拟 7 状态机的完整流转**：只测了"接受合法/拒绝非法"，未端到端跑 Dev → Close
3. **未测试 superpowers Skill 调用的运行时行为**：只验证 `tools: [..., Skill]` 声明，不验证 Claude Code 真的能 dispatch
4. **未覆盖 stage 0-3 的 agent 调用点**：那些是 P2 优先级，待后续完善

---

## 10. 跑测速查

```bash
# 最快（仅 frontmatter + 占位符）
pytest tests/test_agent_frontmatter.py tests/test_skill_references.py -v

# CI 默认（零依赖 + hook 静态分析）
pytest tests/ -v -m "not stage4"

# 本地 stage 4 深度
pytest tests/ -v -m stage4

# 全测
pytest tests/ -v

# 单个 agent
pytest tests/test_agent_frontmatter.py -v -k "dev-stage4"

# 查看 marker
pytest tests/ --markers
```

---

*最后更新：2026-06-05*
*关联：`.claude/plans.md`（superpowers 集成方案）*
*维护者：repo-maintainer + senior-developer*
