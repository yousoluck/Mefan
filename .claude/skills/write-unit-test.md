# 编写单元测试
- 触发条件：阶段 4 QA 执行 QA-Test-Coding 时需要编写测试代码
- 适用 Agent：QA

## 输入
- `test-plan.md`（获取测试用例 + 预期结果）
- `ADR.md`（了解功能实现细节）
- `sprint-status.md`（获取当前 MG/US 范围）
- `consistency-baseline.md`（了解测试代码规范）

## 输出
- `tests/US-XXX/*.test.js`（自动化测试代码）
- `tests/US-XXX/manual-test/TC-M001.md`（人工测试模板）

## 测试目录结构

```
tests/                              # 测试根目录（与 .claude 平级）
├── US-101/                         # 按 US 分目录
│   ├── user-registration.test.js  # 自动化测试代码
│   └── manual-test/               # 人工测试模板目录
│       ├── TC-M001.md             # TC-M001 人工测试模板
│       └── TC-M002.md             # TC-M002 人工测试模板
├── US-102/
│   ├── user-login.test.js
│   └── manual-test/
│       └── TC-M101.md
└── ...
```

**命名规范**：
- 测试文件：`{功能简述}.test.js`（kebab-case）
- 人工测试模板：`TC-M{NNN}.md`（如 TC-M001, TC-M002）

## 操作步骤

### 1. 确定测试范围

1. 读取 `sprint-status.md`，确定当前 MG 内所有 US
2. 读取 `test-plan.md`，获取每个 US 的测试用例列表
3. 确认每个 Sub-feature 都有对应的测试用例

### 2. 编写自动化测试代码

对每个测试用例，编写对应的测试代码：

```javascript
// Test File: tests/US-101/user-registration.test.js

/**
 * ============================================================================
 * US-101: 用户注册
 * ============================================================================
 *
 * 测试用例覆盖说明:
 * - TC-001 ~ TC-004: 邮箱格式验证
 * - TC-005 ~ TC-006: 密码加密
 * - TC-007 ~ TC-008: 注册成功流程
 *
 * 参考文档:
 * - Test Plan: test-plan.md（US-101）
 * - ADR: ADR.md（伪代码）
 * ============================================================================
 */

const request = require('supertest');
const app = require('../../src/app');

describe('US-101: 用户注册', () => {

  describe('Sub-feature: 邮箱格式验证', () => {
    // TC-001: 正常邮箱格式
    test('TC-001: 正常邮箱格式应注册成功', async () => {
      const response = await request(app)
        .post('/api/register')
        .send({
          email: 'test@example.com',
          password: 'ValidPassword123'
        });

      expect(response.status).toBe(201);
      expect(response.data.success).toBe(true);
    });

    // TC-002: 无 @ 符号
    test('TC-002: 无 @ 符号应返回错误', async () => {
      const response = await request(app)
        .post('/api/register')
        .send({
          email: 'testexample.com',
          password: 'ValidPassword123'
        });

      expect(response.status).toBe(400);
      expect(response.data.error).toContain('invalid email');
    });
    // ... 其他 TC
  });

  describe('Sub-feature: 密码加密', () => {
    // TC-005: 密码加密验证
    test('TC-005: 密码应被加密存储', async () => {
      // ...
    });
    // ... 其他 TC
  });
});
```

### 3. 编写人工测试模板

对无法自动化的测试用例，编写人工测试模板：

```markdown
## Manual Test Plan - US-101: 用户注册

### 基本信息
- **US ID**: US-101
- **US 标题**: 用户注册
- **测试类型**: 人工测试
- **测试人员**: {QA名字}
- **测试时间**: {YYYY-MM-DD}

---

### 环境准备

| 步骤 | 操作 | 预期结果 | 实际结果 | 状态 |
|------|------|----------|----------|------|
| 1 | 打开测试环境 URL: http://localhost:3000 | 页面正常显示 | | |
| 2 | 清除浏览器缓存和 Cookie | 缓存已清除 | | |
| 3 | 准备测试邮箱: test-manual@example.com | 邮箱可用 | | |
| 4 | 确保数据库测试数据已清理 | 数据已清理 | | |
| 5 | 打开 DevTools > Console | Console 面板打开 | | |

---

### 功能测试

#### TC-M001: 正常注册流程
| 步骤 | 操作 | 预期结果 | 实际结果 | 状态 |
|------|------|----------|----------|------|
| 1 | 点击"注册"按钮 | 显示注册表单 | | |
| 2 | 输入有效邮箱: test-manual@example.com | 邮箱格式验证通过 | | |
| 3 | 输入密码: TestPass123 | 显示密码强度: 强 | | |
| 4 | 确认密码: TestPass123 | 显示密码一致 | | |
| 5 | 点击"注册"按钮 | 显示加载中 | | |
| 6 | 等待响应 | 注册成功提示 | | |
| 7 | 页面跳转 | 跳转到首页，显示用户信息 | | |
| 8 | 检查 Cookie | 存在 session cookie | | |

---

### 测试结果汇总

| 分类 | 用例数 | 通过 | 失败 | 通过率 |
|------|--------|------|------|--------|
| 功能测试 | 1 | | | |
| **总计** | **1** | | | |
```

### 4. 完成检查清单

- [ ] 所有 Test Plan 中的测试用例都有对应测试代码
- [ ] 一个 US/Sub-feature 对应多个测试用例
- [ ] 测试代码逻辑与 Test Plan 预期结果一致
- [ ] 无法自动化的用例都有人工测试模板
- [ ] 测试代码符合 consistency-baseline.md 规范
- [ ] 测试文件命名规范：`tests/{US-ID}/{功能}.test.js`
- [ ] 人工测试模板命名规范：`tests/{US-ID}/manual-test/TC-M{NNN}.md`

## 禁止事项

- 禁止遗漏任何 Test Plan 中的测试用例
- 禁止一个测试文件覆盖多个 US（一个 US 一个测试文件）
- 禁止硬编码测试数据（使用变量或常量）
- 禁止不清理测试副作用（每个测试后清理数据）