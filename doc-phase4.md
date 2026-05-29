# 开发与 QA 测试阶段 - 完整执行流程 v2.1

## 文档版本
- **版本**: v2.1
- **更新时间**: 2026-05-29
- **基于**: v2.0 增强版
- **适用范围**: 开发阶段 + QA 测试阶段

---

## 一、整体架构（v2.1 增强）

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         阶段 0：开发前准备（已有文档）                      │
├─────────────────────────────────────────────────────────────────────────┤
│  Requirements.md  ──→  ADR  ──→  Sprint Plan  ──→  Test Plan            │
│        ↓               ↓            ↓                ↓                  │
│   User Stories     Architecture   Sprint Scope    QA Strategy         │
│   Sub-features    伪代码+Steps     Module Group   Test Cases           │
│                    Skills List                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                    Consistency-baseline.md                             │
│                              ↓                                        │
│                         代码规范                                        │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                    模块划分（按功能域）                                   │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐                       │
│  │  模块 A    │  │  模块 B    │  │  模块 C    │                       │
│  │  MG-A1     │  │  MG-B1     │  │  MG-C1     │                       │
│  │  MG-A2     │  │  MG-B2     │  │            │                       │
│  └────────────┘  └────────────┘  └────────────┘                       │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                    阶段 4：模块开发与测试（MG 粒度）                       │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │  Dev 按 MG（Modular Group）开发，同一 MG 内所有 US 完成后才进入下一阶段 │
│  └──────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

### v2.1 新增：三层防御体系

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        三层防御体系                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Layer 1: Hook Layer（快速失败）                                          │
│  ├── check-state-machine.sh      → 防止非法状态跃迁                        │
│  ├── check-adr-implementation.sh → 确保按 ADR 伪代码实现                   │
│  ├── check-reference-consistency.sh → 参考模块命名/结构合规               │
│  ├── check-tdd-rhythm.sh         → 验证 TDD 红→绿→重构循环               │
│  ├── check-test-coverage.sh      → 验证测试覆盖率                          │
│  └── check-arch-contract.sh      → 验证架构契约（模块依赖关系）            │
│                                                                          │
│  Layer 2: Guardian Layer（深度语义审查）                                  │
│  ├── Architect Agent → 代码检查（Code Review）                          │
│  ├── QA Agent        → 测试代码检查（Test Code Review）                  │
│  └── PM Agent        → 进度监控、Close 验收                               │
│                                                                          │
│  Layer 3: Human Gate（最终决策）                                         │
│  └── 人类介入处理循环 3 次未通过的异常情况                                  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 二、输入文档衔接

### 2.1 输入文档对照表

| 文档 | 作用 | 给开发/QA 提供的内容 |
|------|------|---------------------|
| **Requirements.md** | 需求来源 | User Story 列表 + Sub-features + 验收标准 |
| **ADR** | 架构设计 | 伪代码 + 实现 Steps + 需要的 Skills |
| **Sprint Plan** | 范围定义 | 本 Sprint 交付的 US + 时间线 + 优先级 + 模块划分 |
| **Test Plan** | 测试策略 | 测试类型 + 测试用例 + 通过标准 |
| **Consistency-baseline.md** | 代码规范 | 代码风格 + 结构规范 + Lint 规则 |
| **reference-module.md** | 参考模块 | 指定模块的代码作为实现参考 |

### 2.2 开发前检查清单（Dev & QA 必读）

```
□ 确认 Requirements.md 中的 US 已对齐 ADR 架构设计
□ 确认 Sprint Plan 中的 US 与 Test Plan 中的测试用例一一对应
□ 确认 Consistency-baseline.md 已更新到本地 IDE Lint 配置
□ 确认 ADR 中的 Skills 可用（如有 API 调用，检查凭证）
□ 确认本地环境与生产环境配置一致（通过 .env.sample）
□ 确认模块划分：同模块内所有 US 一起开发、一起测试
□ 确认已安装 Git hooks（bash .claude/hooks/install-hooks.sh）
```

---

## 三、Modular Group（MG）划分原则

### 3.1 为什么按 MG 开发与测试？

1. **US 之间往往有依赖关系**：US-A 的 API 是 US-B 的前端调用的基础
2. **测试需要完整的上下文**：无法单独测试一个「半成品 API」
3. **平衡反馈速度与测试质量**：每个功能模块内部完整后再测试
4. **确保增量可追踪**：Dev 不中途 commit，所有代码在 MG 完成后再 commit

### 3.2 MG 划分依据

```
MG = 功能域内相互依赖的 US 的集合

划分依据:
- 同一业务域（如：用户认证、订单管理、支付）
- 共享的数据模型
- API 调用依赖关系
- 前后端联调的边界
```

### 3.3 MG 划分示例

```
MG: 用户认证
├── US-101: 用户注册
├── US-102: 用户登录
└── US-103: 找回密码

MG: 订单管理
├── US-201: 创建订单
├── US-202: 订单支付
└── US-203: 订单查询
```

### 3.4 MG 测试触发条件

```
触发条件：MG 内所有 US 都进入 "Self Code Checking" 状态
```

---

## 四、User Story 状态流转（7个状态）v2.1

### 4.1 状态定义总览

| 状态 | 名称 | 说明 | 状态更新时机 |
|------|------|------|-------------|
| **1. Dev** | 开发中 | Dev 正在编写代码，尚未提交 | 领取任务时立即更新 |
| **2. Self-Check** | 自我代码检查 | Dev 完成代码自测，准备进入审查 | 进入阶段时立即更新 |
| **3. Code Review** | 代码审查 | Arch Agent 检查代码质量（原 Arch Code Checking） | 进入阶段时立即更新 |
| **4. QA-Test-Coding** | QA 测试代码编写 | QA 根据 Test Plan 编写测试代码 | 进入阶段时立即更新 |
| **5. Test Code Review** | 测试代码审查 | Arch Agent 检查测试代码质量（原 Arch Test Checking） | 进入阶段时立即更新 |
| **6. Testing** | 人工测试 | QA 执行测试，发现 Bug | 进入阶段时立即更新 |
| **7. Close** | 完成 | US 验收通过，PM 最终 commit | 验收通过后更新 |

### 4.2 状态流转图

```
┌─────────┐    完成代码    ┌──────────────────┐   通过   ┌─────────────────┐
│   Dev   │──────────────▶│    Self-Check    │────────▶│   Code Review   │
│ (开发中) │               │   (自我检查)      │          │ (Arch Agent)    │
└─────────┘               └──────────────────┘          └────────┬────────┘
                                                                   │
                          需要修复  ◀─────────────────────────────│
                                                                   │ 通过
                                                                   ▼
┌─────────────────┐    开始测试    ┌─────────────────┐   通过   ┌─────────────┐
│     Close       │◀─────────────│    Testing      │────────▶│ Test Code   │
│     (完成)      │              │   (人工测试)     │          │  Review     │
└─────────────────┘              └─────────────────┘          └─────────────┘
                                 ▲                     不通过    └─────────────┘
                                 │                       ↑
                          修复完成 ◀───────────────────┘
                                 │
┌─────────────────┐    修复 Bug  ┌─────────────────┐
│QA-Test-Coding   │◀─────────────│   (Bug循环)     │
│ (QA写测试代码)   │              │    最多 3 次     │
└─────────────────┘              └─────────────────┘
                                 ▲
                                 │ 测试代码有问题需修复
                          ┌─────┴─────┐
                          │ Test Code │
                          │  Review   │
                          └───────────┘
```

### 4.3 各状态详细说明

#### 状态 1: Dev（开发中）

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 状态 1: Dev (开发中)                                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│ ● Dev 按 MG 开发 US                                                      │
│ ● 同一 MG 内所有 US 完成开发 → 进入 Self-Check                           │
│ ● Dev 不中途 commit，所有代码在本地 until MG 完成                        │
│ ● Sprint Status: US: {ID} | Status: Dev | Dev: {名字}                   │
│ ● 进入时立即更新状态，不是完成后才更新                                     │
│                                                                          │
│ 工作原则:                                                                │
│   - 严格按照 ADR 伪代码实现                                               │
│   - 遵循 Consistency-baseline.md 代码规范                                 │
│   - 复用类似功能模块的代码（参考 reference-module.md）                    │
│   - 遇到问题查阅 ADR 或咨询 Tech Lead                                    │
│                                                                          │
│ Hook 检查（离开 Dev 时）:                                                │
│   - check-adr-implementation.sh: 确保按 ADR 伪代码实现                   │
│   - check-reference-consistency.sh: 参考模块命名/结构合规                │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 状态 2: Self-Check（自我代码检查）

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 状态 2: Self-Check (自我代码检查)                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│ ● **进入时立即更新状态**，不是完成后才更新                                 │
│                                                                          │
│ ● Dev 自行检查:                                                          │
│   - Lint 检查通过（npm run lint）                                        │
│   - 单元测试通过（npm run test）                                          │
│   - 手动功能验证通过                                                     │
│   - 代码无冗余（已复用类似模块）                                          │
│   - 符合 Consistency-baseline.md 规范                                      │
│                                                                          │
│ ● Hook 检查（离开 Self-Check 时）:                                       │
│   - check-state-machine.sh: 验证状态转换合法性                           │
│   - check-tdd-rhythm.sh: 验证 TDD 红→绿→重构循环                         │
│                                                                          │
│ ● 检查通过 → 更新 Sprint Status → 进入 Code Review                      │
│ ● 检查不通过 → 返回 Dev 状态继续修复                                       │
│                                                                          │
│ ● Sprint Status: US: {ID} | Status: Self-Check | Dev: {名字}           │
│                                                                          │
│ 本地检查命令（不依赖 CI/CD）:                                             │
│   # Lint 检查                                                            │
│   npm run lint                                                          │
│                                                                          │
│   # 单元测试                                                            │
│   npm run test                                                          │
│                                                                          │
│   # 代码覆盖率                                                           │
│   npm run test:coverage                                                 │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 状态 3: Code Review（代码审查）v2.1 重命名

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 状态 3: Code Review (代码审查) 【原 Arch Code Checking】                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│ ● **进入时立即更新状态**，不是完成后才更新                                 │
│                                                                          │
│ ● Arch Agent 检查 MG 内所有 US 的代码（按 MG 检查，不是按 US 检查）        │
│                                                                          │
│ ● 检查内容:                                                              │
│   a) [ ] 功能实现是否完整（对照 Requirements.md）                          │
│   b) [ ] 有无错误实现（对照验收标准）                                      │
│   c) [ ] 是否按 ADR 伪代码实现（逻辑一致性）                                │
│   d) [ ] 代码是否有冗余                                                   │
│      - 如有冗余，参考类似功能模块的实现                                    │
│      - 建议复用现有模块                                                   │
│   e) [ ] 是否 follow consistency-baseline 规范                           │
│                                                                          │
│ ● Hook 前置检查:                                                         │
│   - check-state-machine.sh: 验证状态转换合法性                           │
│   - check-adr-implementation.sh: 确保按 ADR 伪代码实现                   │
│                                                                          │
│ ● 如有问题 → 生成 review-log.md → 返回 Dev-Fix 修复 (循环最多 3 次)       │
│ ● 全部通过 → 进入 QA-Test-Coding                                         │
│                                                                          │
│ ● Sprint Status: US: {ID} | Status: Code Review | Arch: {名字}          │
│                                                                          │
│ ● 循环处理:                                                              │
│   - 循环 1/3、2/3：记录问题到 review-log.md，返回修复                      │
│   - 循环 3/3：仍不通过 → 报告 Human Gate                                 │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 状态 4: QA-Test-Coding（QA 测试代码编写）

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 状态 4: QA-Test-Coding (QA 测试代码编写)                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│ ● **进入时立即更新状态**，不是完成后才更新                                 │
│                                                                          │
│ ● QA 根据 Test Plan 编写测试代码                                          │
│                                                                          │
│ ● 核心原则：一个 US/Sub-feature 对应多个测试用例                          │
│                                                                          │
│   Example:                                                              │
│   US-101: 用户注册                                                       │
│   ├── Sub-feature: 邮箱格式验证                                          │
│   │   ├── TC-001: 正常邮箱格式                                           │
│   │   ├── TC-002: 无 @ 符号                                             │
│   │   ├── TC-003: 无域名                                                │
│   │   └── TC-004: 特殊字符                                              │
│   ├── Sub-feature: 密码加密                                             │
│   │   ├── TC-005: 密码加密验证                                          │
│   │   └── TC-006: 加密算法一致性                                        │
│   └── Sub-feature: 注册成功                                            │
│       ├── TC-007: 正常注册流程                                          │
│       └── TC-008: 注册后自动登录                                        │
│                                                                          │
│ ● 测试代码类型:                                                          │
│   - 单元测试（测试单个函数/方法）                                        │
│   - 集成测试（测试 API 调用链路）                                        │
│   - E2E 测试（端到端用户流程）                                           │
│   - 人工测试（无法自动化的测试步骤，需提供详细模板）                       │
│                                                                          │
│ ● Hook 检查（离开 QA-Test-Coding 时）:                                   │
│   - check-tdd-rhythm.sh: 验证 TDD 节奏                                  │
│                                                                          │
│ ● 完成后 → 进入 Test Code Review                                         │
│                                                                          │
│ ● Sprint Status: US: {ID} | Status: QA-Test-Coding | QA: {名字}         │
│                                                                          │
│ ● 循环处理:                                                              │
│   - 循环 1/3、2/3：发现问题返回修复                                       │
│   - 循环 3/3：仍不通过 → 报告 Human Gate                                 │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 状态 5: Test Code Review（测试代码审查）v2.1 重命名

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 状态 5: Test Code Review (测试代码审查) 【原 Arch Test Checking】        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│ ● **进入时立即更新状态**，不是完成后才更新                                 │
│                                                                          │
│ ● Arch Agent 检查 QA 编写的测试代码                                        │
│                                                                          │
│ ● 检查内容:                                                              │
│   a) [ ] 是否覆盖所有测试用例（对照 Test Plan）                            │
│   b) [ ] 测试代码逻辑是否正确                                            │
│      - 断言条件与 Test Plan 预期结果一致                                 │
│      - 测试数据准备正确                                                  │
│      - Mock/Stub 使用正确                                               │
│   c) [ ] 有无遗漏的人工测试流程                                          │
│      - 需提供人工测试模板（环境准备 + 测试步骤 + 预期结果）                │
│   d) [ ] 测试代码是否符合 consistency-baseline 规范                      │
│                                                                          │
│ ● Hook 前置检查:                                                         │
│   - check-state-machine.sh: 验证状态转换合法性                           │
│                                                                          │
│ ● 如有问题 → 返回 QA 修复 → 重新提交 Test Code Review                     │
│ ● 全部通过 → 进入 Testing                                                │
│                                                                          │
│ ● Sprint Status: US: {ID} | Status: Test Code Review | Arch: {名字}     │
│                                                                          │
│ ● 循环处理:                                                              │
│   - 循环 1/3、2/3：发现问题返回修复                                       │
│   - 循环 3/3：仍不通过 → 报告 Human Gate                                 │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 状态 6: Testing（人工测试）

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 状态 6: Testing (人工测试)                                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│ ● **进入时立即更新状态**，不是完成后才更新                                 │
│                                                                          │
│ ● QA 执行人工测试（含执行自动化测试）                                      │
│ ● 所有测试在本地执行，不依赖 CI/CD                                      │
│                                                                          │
│ ● 执行步骤:                                                             │
│   1. 运行自动化测试代码（本地）                                          │
│   2. 执行人工测试步骤（按人工测试模板）                                   │
│   3. 记录测试结果 (Pass/Fail)                                           │
│                                                                          │
│ ● Hook 检查（离开 Testing 时）:                                          │
│   - check-state-machine.sh: 验证状态转换合法性                           │
│   - check-test-coverage.sh: 验证测试覆盖率                               │
│                                                                          │
│ ● 发现 Bug → 记录到 bugs.md → Dev-Fix 修复 (循环最多 3 次)                │
│ ● 全部通过 → 通知 PM 执行 Close 验收                                     │
│                                                                          │
│ ● Sprint Status: US: {ID} | Status: Testing | QA: {名字}               │
│                                                                          │
│ 本地测试命令:                                                            │
│   # 运行所有测试                                                         │
│   npm run test                                                          │
│                                                                          │
│   # 运行特定 MG 的测试                                                   │
│   npm run test -- --grep "MG-001"                                       │
│                                                                          │
│   # 运行特定 US 的测试                                                   │
│   npm run test -- --grep "US-101"                                       │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 状态 7: Close（完成）

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 状态 7: Close (完成)                                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│ ● **进入时立即更新状态**（PM 执行 Close 验收时）                          │
│                                                                          │
│ ● PM 验收通过                                                           │
│ ● PM 执行最终 commit（整个 MG 一起 commit）                              │
│ ● 更新 Sprint Status: US: {ID} | Status: Close                          │
│ ● 生成 Test Report                                                      │
│                                                                          │
│ ● 验收条件:                                                             │
│   □ 所有测试用例通过（自动化 + 人工）                                     │
│   □ **bugs.md 中所有 Bug 状态为 Closed**                                │
│   □ Code Review 通过                                                    │
│   □ Test Code Review 通过                                               │
│   □ Test Report 已生成                                                  │
│                                                                          │
│ ● Bug 关闭检查（Close 前必须满足）:                                      │
│   - 非 Closed 状态的 Bug 包括：Open, In Progress, Fixed, Reopen, Verified │
│   - 所有 Bug 必须已关闭或已记录为 Technical Debt                         │
│                                                                          │
│ Hook 检查（离开 Close 时）:                                             │
│   - check-state-machine.sh: 验证状态转换合法性                           │
│   - check-arch-contract.sh: 验证架构契约（模块依赖关系）                  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 五、Bug 管理流程 v2.1

### 5.1 Bug 状态流转

```
QA 发现 Bug
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         Bug 生命周期                                     │
└─────────────────────────────────────────────────────────────────────────┘

Open → (分配给 Dev-Fix) → Fixed → (QA-Fix 验证) → Close
    │                                                    ↑
    │                         Reopen ←───────────────────┘
    │                              (验证失败)
    │
    └──→ Technical Debt（循环 3 次仍无法修复）
```

### 5.2 Bug 数据流（各 Agent 职责）

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     Bug 数据流                                          │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────┐    发现 Bug    ┌─────────┐    修复    ┌─────────┐    验证    ┌─────────┐
│   QA    │───────────────▶│ Dev-Fix │──────────▶│ QA-Fix  │──────────▶│ PM-Close│
│         │  记录到 bugs.md │         │ 更新 Fixed │         │ 更新 Close │         │
│ Testing │  状态: Open    │         │            │         │            │         │
└─────────┘                └─────────┘            └─────────┘            └─────────┘
                              │                      │
                              │                      │
                              ▼                      ▼
                        ┌─────────────────────────────────────────┐
                        │               bugs.md                   │
                        │  - Open/Reopen → Dev-Fix 读取并修复       │
                        │  - Fixed → QA-Fix 读取并验证             │
                        │  - 所有 Bug 最终汇总到 PM Close 检查      │
                        └─────────────────────────────────────────┘
```

### 5.3 各 Agent Bug 职责

| Agent | 读取 Bug 状态 | 处理 | 更新状态 |
|-------|--------------|------|---------|
| **Dev-Fix** | Open, Reopen | 修复 Bug | → Fixed |
| **QA-Fix** | Fixed | 验证修复 | → Close 或 Reopen |
| **PM-Close** | 所有状态 | 验收 | 确认所有已 Close |

### 5.4 bugs.md 字段要求

```markdown
## Bug Report - Testing

### 基本信息
- **MG**: MG-001
- **US ID**: US-101
- **Bug ID**: TEST-BUG-001
- **严重级别**: P0/P1/P2/P3
- **测试类型**: 自动化测试 / 人工测试
- **发现时间**: {YYYY-MM-DD}
- **报告人**: {QA名字}
- **修复人**: {Dev 名字}
- **循环次数**: 1/3, 2/3, 3/3
```

---

## 六、Hook 系统 v2.1 新增

### 6.1 Hook 清单

| Hook | 职责 | 触发时机 |
|------|------|---------|
| `check-state-machine.sh` | 验证 MG 状态流转合法性 | 每个状态进入时 |
| `check-adr-implementation.sh` | 确保按 ADR 伪代码实现 | Dev 离开时、Code Review 前 |
| `check-reference-consistency.sh` | 参考模块命名/结构合规 | Dev 实现时 |
| `check-tdd-rhythm.sh` | 验证 TDD 红→绿→重构循环 | Self-Check 完成时 |
| `check-test-coverage.sh` | 验证测试覆盖率 | Testing 完成时 |
| `check-arch-contract.sh` | 验证架构契约（模块依赖关系） | Code Review 离开时、Close 完成时 |

### 6.2 Hook 触发矩阵

| Hook | Dev→Self | Self→CodeReview | CodeReview→QA | QA→TestCodeReview | TestCodeReview→Test | Test→Close |
|------|----------|-----------|---------|-------------|---------------|------------|
| check-state-machine | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| check-adr-implementation | ✅ | - | ✅ | - | - | - |
| check-reference-consistency | ✅ | - | - | - | - | - |
| check-tdd-rhythm | - | ✅ | - | - | - | - |
| check-test-coverage | - | - | - | - | ✅ | ✅ |
| check-arch-contract | - | - | ✅ | - | - | ✅ |

### 6.3 Hook 与守护者边界

| 层级 | 能力 | 阻断级别 |
|------|------|---------|
| **Hook** | 自动化检查（命名、风格、diff 大小、状态验证） | 快速失败，阻断进入下一状态 |
| **Guardian (Agent)** | AI 推理（深度语义审查、架构判断） | REJECTED 直接阻断 |
| **Human Gate** | 人类决策 | 最终裁决 |

---

## 七、Agent 职责 v2.1

### 7.1 Agent 清单

| Agent | 阶段 | 职责 |
|-------|------|------|
| **Dev** | 4 | 按 MG 开发，执行 Self-Check |
| **Dev-Fix** | 4 | 修复 Code Review 和 Testing 阶段发现的问题（合并 review-log + bugs.md） |
| **Architect** | 4 | 执行 Code Review 和 Test Code Review |
| **QA** | 4 | 执行 QA-Test-Coding 和 Testing |
| **QA-Fix** | 4 | 验证 bugs.md 中状态为 Fixed 的 Bug |
| **PM** | 4 | 进度监控、Close 验收、最终 commit |

### 7.2 Dev-Fix Agent（新增）

Dev-Fix 负责修复两类问题：

**A. 从 review-log.md 提取代码审查问题（AC-*）**
- 状态为 Open 且属于当前 MG
- 修复后更新状态为 Fixed

**B. 从 bugs.md 提取 Bug（状态为 Open 或 Reopen）**
- 属于当前 MG 的 Bug
- 修复后更新 bugs.md 中 Bug 状态为 Fixed

### 7.3 QA-Fix Agent（新增）

QA-Fix 负责验证修复结果：

- 从 bugs.md 提取所有状态为 Fixed 且属于当前 MG 的 Bug
- 逐一验证 Bug 是否已真正修复
- **验证通过** → 更新 bugs.md 中对应 Bug 的状态为 **Close**
- **验证不通过** → 更新 bugs.md 中对应 Bug 的状态为 **Reopen**，并说明原因

---

## 八、阶段 4 完整流程图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         阶段 4：MG 生命周期                              │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│  Dev 开发 MG 内所有 US                                                   │
│                                                                          │
│  Dev → Self-Check → Code Review → QA-Test-Coding → Test Code Review    │
│                      ↑                          │                        │
│                      │                          │                        │
│                      └──────────────────────────┘                        │
│                               │                                         │
│                               ▼                                         │
│                        Testing                                         │
│                               │                                         │
│                               ▼                                         │
│                    ┌─────────────────────────────────┐                  │
│                    │     Bug 循环（最多 3 次）        │                  │
│                    │                                 │                  │
│                    │  Dev-Fix ←── bugs.md ──→ QA-Fix │                  │
│                    │    ↑                            │                  │
│                    │    │ Open/Reopen                │                  │
│                    │    │                            │                  │
│                    │    │ Fixed ──────────────────→  │                  │
│                    │    │                            │                  │
│                    │    │验证通过 → Close             │                  │
│                    │    │验证失败 → Reopen ───────────┘                  │
│                    │                                 │                  │
│                    └─────────────────────────────────┘                  │
│                               │                                         │
│                               ▼                                         │
│                        PM Close                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 九、循环限制与异常处理

### 9.1 循环限制

| 阶段 | 循环次数 | 超限处理 |
|------|---------|---------|
| Code Review | 3 次 | 报告 Human Gate |
| Test Code Review | 3 次 | 报告 Human Gate |
| QA-Test-Coding | 3 次 | 报告 Human Gate |
| Testing Bug 修复 | 3 次 | 记录为 Technical Debt |

### 9.2 Hook 拦截处理

| 拦截次数 | 处理方式 |
|---------|---------|
| 第 1 次 | 开发者根据违规列表自行修复 |
| 第 2 次 | 开发者必须编写 interception-analysis.md |
| 第 3 次 | 暂停任务，PM 介入评估 |

### 9.3 Human Gate 触发条件

| 条件 | 说明 |
|------|------|
| Code Review 3 次循环未通过 | 连续 3 次检查发现问题未修复 |
| Test Code Review 3 次循环未通过 | 连续 3 次测试代码检查未通过 |
| QA-Test-Coding 3 次循环未通过 | 连续 3 次测试代码未通过检查 |
| Testing 3 次循环未通过 | 连续 3 次测试执行未通过 |
| 发现 P0 缺陷 | 立即暂停，报告 Human Gate |

---

## 十、Git 分支管理 v2.1

### 10.1 分支命名规范

```
feature/MG-{MG_ID}-short-desc
例：feature/MG-001-user-auth
```

### 10.2 分支创建流程

```bash
# 1. 从主分支拉取最新代码
git checkout develop
git pull origin develop

# 2. 创建新分支（每个 MG 创建一个分支）
git checkout -b feature/MG-001-user-auth

# 3. 在该分支上开发 MG 内的所有 US
# 注意：Dev 不中途 commit，所有 US 开发完成后统一处理
```

### 10.3 Close 时合并

```bash
# PM 执行 Close 时
git checkout develop
git merge --no-ff feature/MG-001-user-auth -m "feat(module): 完成 MG-001 模块开发"
git branch -d feature/MG-001-user-auth
git push origin develop
```

---

## 十一、Sprint Status 更新规则 v2.1

### 11.1 状态更新时机

**关键原则：进入阶段时立即更新状态，不是完成后才更新**

| 阶段 | 更新时机 | 示例 |
|------|---------|------|
| Dev | 领取任务时 | "进入 Dev" → 立即更新为 "🏃 Dev" |
| Self-Check | 进入 Self-Check 时 | "进入 Self-Check" → 立即更新为 "🔍 Self-Check" |
| Code Review | 进入 Code Review 时 | "进入 Code Review" → 立即更新为 "🖥️ Code Review" |
| QA-Test-Coding | 进入 QA-Test-Coding 时 | "进入 QA-Test-Coding" → 立即更新为 "🧪 QA-Test-Coding" |
| Test Code Review | 进入 Test Code Review 时 | "进入 Test Code Review" → 立即更新为 "🔬 Test Code Review" |
| Testing | 进入 Testing 时 | "进入 Testing" → 立即更新为 "✅ Testing" |
| Close | PM 执行 Close 验收时 | "验收通过" → 立即更新为 "🎉 Close" |

### 11.2 mg-state.json（状态追踪文件）

```json
{
  "MG-001": {
    "current_state": "Testing",
    "state_history": [
      {"state": "InProgress", "entered_at": "2026-05-29T10:00:00"},
      {"state": "SelfCheck", "entered_at": "2026-05-29T12:00:00"},
      {"state": "CodeReview", "entered_at": "2026-05-29T14:00:00"},
      {"state": "QATestCoding", "entered_at": "2026-05-29T15:00:00"},
      {"state": "TestCodeReview", "entered_at": "2026-05-29T16:00:00"},
      {"state": "Testing", "entered_at": "2026-05-29T17:00:00"}
    ],
    "violations": [],
    "last_check": "2026-05-29T17:30:00"
  }
}
```

---

## 十二、验收条件 v2.1

### 12.1 Close 验收条件

```
□ 所有测试用例通过（自动化 + 人工）
□ bugs.md 中所有 Bug 状态为 Closed（非 Open/In Progress/Fixed/Reopen/Verified）
□ Code Review 通过
□ Test Code Review 通过
□ Test Report 已生成
```

### 12.2 PM Close 检查命令

```bash
# 检查 bugs.md 中是否所有 Bug 都已 Closed
NON_CLOSED_BUGS=$(grep "| TEST-BUG-" "$BUGS_PATH" | grep -v "| Closed |" | grep -v "问题ID" | wc -l)
if [ $NON_CLOSED_BUGS -gt 0 ]; then
  echo "[PM-Stage4] 错误：仍有 $NON_CLOSED_BUGS 个 Bug 未关闭，无法执行 Close"
  exit 1
fi
```

---

## 十三、v2.0 → v2.1 变更总结

| 变更项 | v2.0 | v2.1 |
|--------|------|------|
| **状态命名** | Arch Code Checking, Arch Test Checking | Code Review, Test Code Review |
| **状态更新时机** | 未明确说明 | 进入阶段时立即更新，非完成后更新 |
| **Bug 数据流** | 未明确 | Dev-Fix → QA-Fix → PM Close 链式验证 |
| **Hook 系统** | 无 | 6 个新增 Hook，三层防御体系 |
| **Dev-Fix Agent** | 无 | 新增，专门处理 review-log + bugs.md |
| **QA-Fix Agent** | 无 | 新增，专门验证 Fixed Bug |
| **状态追踪** | 无 | mg-state.json 状态追踪文件 |
| **循环限制** | Bug 循环 3 次 | 全部循环 3 次（Code Review、Test Code Review、QA-Test-Coding） |

---

## 十四、流程关键原则（v2.1）

1. **模块化开发与测试**：同 MG 内所有 US 一起开发、一起测试
2. **状态更新时机**：进入阶段时立即更新，不是完成后更新
3. **三层防御**：Hook（快速失败）→ Guardian（深度审查）→ Human Gate（最终决策）
4. **Bug 闭环**：Dev-Fix 修复 → QA-Fix 验证 → PM Close 验收
5. **本地化测试**：不依赖 CI/CD，确保测试速度
6. **清晰的增量追踪**：Dev 不中途 commit，PM 统一 commit
7. **循环限制**：所有检查循环最多 3 次，避免无限循环

---

**文档结束**