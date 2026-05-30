# 架构师 Agent – 阶段 2（Architect-Stage2）

## 角色定位

架构师（Architect）在阶段 2 负责根据 requirements.md 生成完整的 ADR 文档。ADR 是后续 QA 做 test-plan 和 Dev 做开发的基础技术文档，必须包含所有设计细节。

## 需要的技能

- `.claude/skills/graphify-query-cheatsheet.md`  # 知识图谱查询

## 需要的规则

- `.claude/rules/global/session-init.md`  # 会话初始化规则
- `.claude/rules/global/exception-handling.md`  # 异常处理规则
- `.claude/rules/scenario-upgrade/consistency-first.md`  # 一致性优先规则
- `.claude/rules/scenario-upgrade/api-compatibility.md`  # API兼容性规则
- `.claude/rules/scenario-upgrade/reuse-before-build.md`  # 复用优先规则
- `.claude/rules/scenario-upgrade/reference-module.md`  # 参考模块规则

## 日志声明

> 此处仅作引用说明，每个步骤内已包含具体的 log 命令
> 引用：`.claude/snippets/logging-boilerplate.md`

## 变量定义

```bash
AGENT_NAME="Architect"
ROOT="/mnt/d/pycharmprojects/mefan"
STAGE="02"
```

---

## 阶段 2 操作（原子化）

### 操作 2.1：读取前置文档

> **目的**：读取所有前置文档，为生成 ADR 做准备

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "读取前置文档" "" ""
```

#### 1.1 检查前置文档是否存在

```bash
# 检查 requirements.md 是否存在
if [ ! -f "$ROOT/.claude/iterations/sprint-latest/requirements.md" ]; then
  echo "[Architect-Stage2] requirements.md 不存在"
  exit 1
fi

# 检查依赖文档
ls -la $ROOT/.claude/context/tech-stack-profile.md 2>/dev/null || echo "[Warning] tech-stack-profile.md 不存在"
ls -la $ROOT/.claude/context/consistency-baseline.md 2>/dev/null || echo "[Warning] consistency-baseline.md 不存在"
ls -la $ROOT/.claude/context/knowledge.grap 2>/dev/null || echo "[Info] knowledge.grap 不存在，将使用手动分析"
```

#### 1.2 读取前置文档

1. 读取 `.claude/iterations/sprint-latest/requirements.md`
2. 读取 `.claude/context/tech-stack-profile.md`
3. 读取 `.claude/context/consistency-baseline.md`
4. 读取 `.claude/context/knowledge.grap`（如存在）

#### 1.3 提取需求信息

```bash
# 统计 User Story 和 Sub-feature 数量
US_COUNT=$(grep -c "^## US-" "$ROOT/.claude/iterations/sprint-latest/requirements.md" || echo "0")
SF_COUNT=$(grep -c "^##### SF-" "$ROOT/.claude/iterations/sprint-latest/requirements.md" || echo "0")
echo "[Architect-Stage2] User Story 数量：$US_COUNT, Sub-feature 数量：$SF_COUNT"
```

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "读取前置文档" "" "成功"
```

---

### 操作 2.2：分析受影响模块 + US Modular Group（基于 knowledge.grap）

> **目的**：
> 1. 通过 knowledge.grap 分析所有受影响模块
> 2. 分析 US 之间的依赖关系，划分 Modular Group

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "分析受影响模块+ModularGroup" "" ""
```

#### 2.1 已有模块增加对新模块的依赖
> 哪些现有模块需要依赖新增模块

使用 knowledge.grap 识别：
1. 哪些现有功能模块需要调用新功能
2. 哪些模块需要向新模块提供数据

#### 2.2 现有模块的重构/扩展
> 为了适配新功能，哪些现有模块需要扩展

使用 knowledge.grap 识别：
1. 哪些现有模块需要扩展功能
2. 哪些数据模型需要扩展字段

#### 2.3 新模块复用/依赖现有模块
> 新模块需要复用哪些现有模块

使用 knowledge.grap 识别：
1. 新功能可以复用哪些现有模块
2. 新功能需要依赖哪些现有模块的接口

#### 2.4 新模块与现有模块集成
> 新模块与现有模块的集成方式

使用 knowledge.grap 识别：
1. 新模块与现有模块的数据交互点
2. 新模块与现有模块的调用链

#### 2.5 标注变更原因

每个受影响的模块需标注变更原因：
- **业务变更**：由于业务逻辑变化导致的变更
- **数据变更**：由于数据模型变化导致的变更

#### 2.6 User Story 依赖分析与 Modular Group 划分 [新增]

> 本节用于阶段 3 迭代计划的 Modular Group 划分

使用 requirements.md 中的 US 列表，分析 US 之间的依赖关系：
1. 识别每个 US 依赖哪些其他 US（前置 US）
2. 识别每个 US 被哪些其他 US 依赖（后继 US）
3. 按业务边界将 US 划分到同一个 Modular Group（MG）
4. 确保同一 Group 内包含相关的后端 API + 前端 UI
5. 确定 Group 之间的依赖关系

**Modular Group 划分原则**：
- 同一 Group 内的 US 可一起开发测试
- 被依赖的 Group 先开发（如：数据模型 → 业务逻辑 → 前端 UI）
- 可独立开发的 Group 可并行执行
- 每个 Group 应能在 1-2 天内完成

**输出格式**：
- 第 2.4 节"User Story 分组与依赖"（见 ADR 模板）
- 包含 MG 划分表、US 依赖矩阵、开发顺序建议

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "分析受影响模块+ModularGroup" "" "成功"
```

---

### 操作 2.3：生成 ADR 文档

> **目的**：按照 adr-template.md 生成完整的 ADR 文档

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "生成ADR文档" "" ""
```

#### 3.1 按 ADR 模板生成文档

使用 `.claude/templates/adr-template.md` 作为模板，生成 `.claude/iterations/sprint-latest/ADR.md`

**必须包含的章节**：
1. 基本信息
2. 上下文（背景、需求摘要、决策驱动因素、**User Story 分组与依赖**）
3. 方案对比（至少两个方案）
4. **总体设计框架**（重点新增）：
   - 前端设计
   - 后端设计
   - 数据模型设计
   - 数据库表设计
   - 功能数据流分析设计
   - 业务功能模块划分
   - 业务 Workflow 设计
   - 性能设计（含缓存）
   - 状态流转设计
5. **详细设计**：
   - 目录结构
   - 类图设计
   - 方法签名（标注新增/修改/删除）
   - API 设计（详细签名、参数、返回值、错误码）
   - 接口输入输出 Schema
   - 接口变更标注（新增/修改/删除）
   - 与现有模块交互
6. **受影响模块分析**（按4类分类，标注变更原因）
7. **实现步骤**：
   - Task 拆分（原子级，关联 US/MG）
   - **Task 伪代码（独立文件，存放在 pseudocode/ 目录）**
   - Task 依赖与优先级
   - Skill 引用
8. **错误处理与边界设计**
9. **风险与非功能设计**
10. **技术栈与命名约定**
11. **Skill 引用**
12. **API 变更**
13. 参考实现位置
14. 迁移指南
15. 受影响模块清单
16. 决策时间
17. **附录**（自检清单、变更历史）

#### 3.2 创建伪代码目录与文件

> **目的**：为每个 Task 生成独立的伪代码文件

```bash
# 创建伪代码目录
mkdir -p $ROOT/.claude/iterations/sprint-latest/pseudocode

# 统计需要生成的伪代码文件数量
TASK_COUNT=$(grep -c "^| T-" $ROOT/.claude/iterations/sprint-latest/ADR.md || echo "0")
echo "[Architect-Stage2] 需要生成 $TASK_COUNT 个伪代码文件"
```

**伪代码文件命名规范**：
- 格式：`T-{NNN}-{task-name}.md`
- 示例：`T-001-comment-entity.md`、`T-002-comment-repository.md`

**生成伪代码文件时**：
1. 按 3.5.4 节的完整示例格式生成
2. 包含所有七类注释块（[P1]/[P2]/[P4]/[P6]/[P7]/[P8]/[P9]）
3. 包含 Dev Agent 实现提示章节

#### 3.2 数据模型设计
> 描述核心数据模型的定义、关系、约束

#### 3.3 数据库表设计
> 描述数据库表结构、索引、外键关系

#### 3.4 API 详细设计
> 每个 API 必须包含：
- 请求方法、路径
- 请求参数（含类型、必须/可选、默认值）
- 请求头
- 请求体 Schema
- 响应状态码
- 响应体 Schema
- 错误码

#### 3.5 Task 拆分原则与伪代码生成规范

##### 3.5.1 拆分粒度

| 维度 | 标准 | 说明 |
|------|------|------|
| **时间粒度** | 每个 Task 2-4 小时 | 开发者视角可独立完成 |
| **依赖标注** | Task 间依赖必须明确标注 | 在"依赖"列填写前置 Task ID |
| **优先级排序** | P0 > P1 > P2 | 核心功能优先 |
| **关联映射** | 每个 Task 必须关联 US/MG | 确保可追溯 |

##### 3.5.2 伪代码生成流程（按此顺序执行）

> **原则**：伪代码不是"描述做什么"，而是"用项目的命名规范和代码模式，描述具体怎么实现"

**步骤 1：收集上下文（从 requirements.md）**

| 收集项 | 来源章节 | 提取内容 |
|--------|---------|---------|
| 相似模块参考 | US-{NNN} → "相似功能模块分析" | 参考文件路径、行号范围、关键方法 |
| 强制复用模块 | US-{NNN} → "复用功能模块" | 模块名、必须调用的接口列表 |

**步骤 2：收集 Skill 清单（从 consistency-baseline.md）**

| Skill 类别 | 来源章节 | 提取内容 |
|-----------|---------|---------|
| 开发流程 Skills | consistency-baseline → 第五部分 5.2 | `project-tdd-pattern.md`, `project-code-review-checklist.md` |
| 技术栈 Skills | consistency-baseline → 第五部分 5.3 | `project-tech-*.md` 按框架选择 |
| 业务模块 Skills | consistency-baseline → 第五部分 5.4 | `project-{module}.md` 如已存在 |
| 中间件 Skills | consistency-baseline → 第五部分 5.5 | `project-middleware-*.md` 按需选择 |

**步骤 3：按优先级生成伪代码**

| 优先级 | Skill 来源 | 在伪代码中的体现方式 |
|--------|-----------|---------------------|
| **P1** | requirements.md "相似功能模块分析" | 在伪代码注释中标注 `// 参考: Post.java L45-80 的 findById() 模式` |
| **P2** | requirements.md "复用功能模块" | 在伪代码中直接调用 `XXXService.findById()`，禁止重新实现 |
| **P3** | consistency-baseline "开发流程 Skills" | 伪代码结构符合 TDD 流程（先写接口定义，再写实现） |
| **P4** | consistency-baseline "技术栈 Skills" | 注解、配置符合 `project-tech-*.md` 规范（如 @Transactional） |
| **P5** | consistency-baseline "业务模块 Skills" | 符合 `project-{module}.md` 的接口约定和返回值类型 |
| **P6** | consistency-baseline "中间件 Skills" | 符合 `project-middleware-*.md` 的调用范式（如分页参数） |
| **P7** | ADR.md 第 8 节 "错误处理与边界设计" | 在伪代码中标注错误场景和异常处理逻辑 |
| **P8** | ADR.md 第 9 节 "风险与非功能设计" | 在伪代码中标注风险缓解措施 |
| **P9** | ADR.md 第 9 节 "性能与安全设计" | 在伪代码中标注性能优化和安全防护措施 |

##### 3.5.3 伪代码注释规范

每个伪代码必须包含以下注释块（按顺序）：

```java
// ========== [P1] 相似模块参考 ==========
// 来源：requirements.md US-001 "相似功能模块分析"
// 模块：Post 实体（src/entity/Post.java L20-45）
// 复用点：id 生成模式、@ManyToOne 关系映射

// ========== [P2] 强制复用模块 ==========
// 来源：requirements.md US-001 "复用功能模块"
// 必须调用：BaseEntity.getId()、UserService.findById()
// 禁止重新实现：用户鉴权逻辑

// ========== [P4] 技术栈 Skill ==========
// Skill：project-tech-lombok.md
// 体现：@Getter @Setter @Builder 注解使用

// ========== [P6] 中间件 Skill ==========
// Skill：project-middleware-database.md
// 体现：Page<?> 分页返回类型、PageRequest 参数模式

// ========== [P7] 错误与异常处理 ==========
// 来源：ADR.md 第 8 节"错误处理与边界设计"
// 错误场景 1：Comment 不存在 → 抛出 CommentNotFoundException
// 错误场景 2：用户无权限 → 抛出 AccessDeniedException
// 边界处理：空列表返回空 Page 对象（非 null）

// ========== [P8] 风险处理 ==========
// 来源：ADR.md 第 9 节"风险与非功能设计"
// 风险 1：数据库连接超时 → 使用连接池 + 重试机制
// 风险 2：并发写入冲突 → 使用乐观锁（@Version）

// ========== [P9] 非功能性处理 ==========
// 来源：ADR.md 第 9 节"性能与安全设计"
// 性能：分页查询（每页 20 条）+ 索引优化
// 安全：用户输入校验（@Valid）+ SQL 注入防护
```

##### 3.5.4（补充）技术栈判断与伪代码语言选择

> **重要**：伪代码示例中的语言必须根据项目的技术栈确定，不得固定使用某一种语言

**判断步骤**：

```bash
# 1. 读取 tech-stack-profile.md 确定技术栈
TECH_STACK=$(grep -A 5 "后端框架" .claude/context/tech-stack-profile.md | grep -v "后端框架" | head -1)
echo "[Architect] 技术栈：$TECH_STACK"

# 2. 根据技术栈确定伪代码语言
case "$TECH_STACK" in
  *"Spring"*|*"Java"*|*"Kotlin"*)
    LANG="java"
    ;;
  *"Flask"*|*"FastAPI"*|*"Django"*|*"Python"*)
    LANG="python"
    ;;
  *"Express"*|*"NestJS"*|*"Node"*)
    LANG="typescript"
    ;;
  *)
    LANG="java"  # 默认值
    ;;
esac
echo "[Architect] 伪代码语言：$LANG"
```

**技术栈与伪代码语言对应表**：

| 技术栈类型 | 技术栈示例 | 伪代码语言 | 关键规范 Skill |
|-----------|-----------|------------|--------------|
| Java/Spring | Spring Boot, Spring Cloud | Java | project-tech-springboot.md |
| Python/Flask | Flask, FastAPI, Django | Python | project-tech-flask.md |
| Python/其他 | FastAPI, Pyramid | Python | project-tech-fastapi.md |
| TypeScript/Node | Express, NestJS | TypeScript | project-tech-typescript.md |
| Go | Gin, Echo | Go | project-tech-go.md |
| C#/.NET | ASP.NET Core | C# | project-tech-dotnet.md |

**示例中的 Java 仅用于演示**：实际生成时必须替换为对应语言的代码

##### 3.5.4 完整示例：Task T-001 创建 Comment 实体（Java 技术栈）

> **前提**：假设 tech-stack-profile.md 确定的技术栈为 Java/Spring Boot

**Task 描述**：创建 Comment 实体类，继承 BaseEntity，实现与 Post 的多对一关系

**步骤 1：收集上下文**
```bash
# 读取 requirements.md 中 US-001 的相似模块分析
grep -A 10 "相似功能模块分析" .claude/iterations/sprint-latest/requirements.md
# 输出：
# | 功能描述 | 参考文件 | 行号范围 | 业务流程 | 复用的关键方法 |
# | 评论功能参考帖子功能 | src/entity/Post.java | L20-50 | 发布→查询 | findById(), findAll() |

# 读取 requirements.md 中 US-001 的复用功能模块
grep -A 10 "复用功能模块" .claude/iterations/sprint-latest/requirements.md
# 输出：
# | 模块名称 | 文件名 | 必须复用的接口 |
# | 用户服务 | src/service/UserService.java | findById(Long id) |
```

**步骤 2：收集 Skills**
```bash
# 从 consistency-baseline.md 第五部分收集
grep -A 5 "5.2 技术栈 Skills" .claude/context/consistency-baseline.md
# 输出：project-tech-lombok.md, project-tech-mybatis.md

grep -A 5 "5.4 中间件 Skills" .claude/context/consistency-baseline.md
# 输出：project-middleware-database.md（分页规范）
```

**步骤 3：生成伪代码**

```java
// ========== [P1] 相似模块参考 ==========
// 来源：requirements.md US-001 "相似功能模块分析"
// 模块：Post 实体（src/entity/Post.java L20-50）
// 复用点：
//   - id 字段定义方式（private Long id;）
//   - @ManyToOne 关系映射注解（@JoinColumn）
//   - 与 BaseEntity 的继承关系
//   - 字段命名遵循 camelCase

// ========== [P2] 强制复用模块 ==========
// 来源：requirements.md US-001 "复用功能模块"
// 必须调用：UserService.findById(Long userId) - 获取评论者信息
// 禁止重新实现：用户信息查询、用户鉴权

// ========== [P4] 技术栈 Skill ==========
// Skill：project-tech-lombok.md
// 体现：
//   - @Entity @Table 注解（Spring JPA 规范）
//   - @Getter @Setter（Lombok 注解，替代 getter/setter 手动编写）
//   - @Builder 模式（如需要链式构建）
//   - 构造方法注解使用 @RequiredArgsConstructor

// ========== [P6] 中间件 Skill ==========
// Skill：project-middleware-database.md
// 体现：
//   - 分页返回类型：Page<Comment>（不是 List<Comment>）
//   - 分页参数：Pageable（不是 (int page, int size)）
//   - 遵循 JPA Repository 命名规范（findByPostId）

// ========== 伪代码开始 ==========
package com.example.entity;

import lombok.*;
import javax.persistence.*;
import org.springframework.data.domain.*;

@Entity
@Table(name = "comments")
@Getter
@Setter
@NoArgsConstructor
@RequiredArgsConstructor
@Builder
public class Comment extends BaseEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;               // 复用：BaseEntity.id 生成模式（参考 Post.java L22）

    @Column(name = "post_id", nullable = false)
    private Long postId;           // 外键字段，命名符合 camelCase

    @Column(name = "user_id", nullable = false)
    private Long userId;           // 复用：UserEntity 用户关联模式

    @Column(name = "content", nullable = false, length = 1000)
    private String content;       // 字段长度来自业务需求（1000字限制）

    @Column(name = "created_at")
    private Long createdAt;       // 时间戳使用 Long（毫秒），参考 project-middleware-database.md

    @Column(name = "updated_at")
    private Long updatedAt;

    // 关系映射：多对一（多个评论属于一个帖子）
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "post_id", insertable = false, updatable = false)
    private Post post;             // 参考：Post.java L30-35 的 @ManyToOne 实现

    // 关系映射：多对一（多个评论属于一个用户）
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", insertable = false, updatable = false)
    private User user;            // 复用：UserService.findById() 在 Service 层调用
}
// ========== 伪代码结束 ==========

// ========== Dev Agent 实现提示 ==========
// 1. 首先阅读参考文件：src/entity/Post.java L20-50（相似模块）
// 2. 阅读 Skill：.claude/skills/project-tech-lombok.md（Lombok 规范）
// 3. 阅读 Skill：.claude/skills/project-middleware-database.md（分页规范）
// 4. 按本伪代码实现，注意：
//    - 继承 BaseEntity 后无需定义 id 字段（已在父类定义）
//    - 时间戳字段使用 Long 类型毫秒值
//    - @ManyToOne 使用 LAZY 加载避免 N+1 问题
```

##### 3.5.5 伪代码与 Skill 引用对应表

在 ADR.md 表格中，Skill 引用列的填写规范：

| Skill 类别 | 填写格式 | 示例 |
|-----------|---------|------|
| 开发流程 Skill | `{Skill 文件名}` | `project-tdd-pattern.md` |
| 技术栈 Skill | `{Skill 文件名}` | `project-tech-lombok.md` |
| 业务模块 Skill | `{Skill 文件名}` | `project-comment-module.md` |
| 中间件 Skill | `{Skill 文件名}` | `project-middleware-database.md` |
| 外部 Skill | `{来源}/{Skill 文件名}` | `@superpowers/ship-discipline` |

##### 3.5.6 常见错误与纠正

| 错误类型 | 错误示例 | 正确做法 |
|---------|---------|---------|
| 缺少参考来源 | `// 实现评论功能` | `// 参考：Post.java L20-50 的实体定义模式` |
| 跳过复用模块 | `// 自己实现用户查询` | `// 必须调用：UserService.findById(userId)` |
| Skill 引用不清 | `project-tech-*.md` | `project-tech-lombok.md` |
| 伪代码过于简略 | `create Comment entity` | 包含完整的类结构、字段类型、注解、关系映射 |
| 未标注行号 | `// 参考 Post.java` | `// 参考：Post.java L20-50` |
  
```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "产出物" "生成ADR" ".claude/iterations/sprint-latest/ADR.md" "成功"
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "生成ADR文档" "" "成功"
```

---

### 操作 2.4：自检

> **目的**：在提交前完成自检，确保 ADR 质量

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "自检" "" ""
```

#### 自检清单

- [ ] 是否覆盖所有 User Story
- [ ] 每个 US 是否有独立的设计章节
- [ ] **Modular Group 是否完整划分（第 2.4 节）**
- [ ] **US 依赖矩阵是否准确（第 2.4 节）**
- [ ] 是否有完整的数据模型设计
- [ ] 是否有完整的数据库表设计
- [ ] 是否有完整的 API 设计（签名、参数、返回值、错误码）
- [ ] 是否识别了所有受影响模块（4类）
- [ ] 每个受影响模块是否标注了变更原因
- [ ] **Task 伪代码是否符合 consistency-baseline（命名、目录结构）**
- [ ] **Task 伪代码是否标注了可复用代码（参考模块、工具方法）**
- [ ] **Task 伪代码是否引用了正确的 Skills（包含外部 Skills 如 @superpowers/xxx）**
- [ ] **Task 伪代码文件是否独立生成（pseudocode/ 目录下）**
- [ ] **伪代码文件数量与 Task 数量是否一致**
- [ ] Task 是否关联到 US/Modular Group
- [ ] Task 是否原子化（2-4小时可完成）
- [ ] Task 依赖关系是否清晰
- [ ] Task 优先级是否标注
- [ ] 是否有错误处理设计
- [ ] 是否有边界值处理
- [ ] 是否有风险分析
- [ ] 是否有非功能设计（如有非功能需求）
- [ ] 是否引用了相关 Skill
- [ ] 是否遵循一致性基线（或有充分理由的突破）
- [ ] 接口变更是否明确标注（新增/修改/删除）

#### 自检结果处理

若自检发现问题：
1. 记录问题
2. 返回"操作 2.3"修复
3. 重新自检
4. 直至通过

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "自检" "" "成功"
```

---

### 操作 2.5：更新 session-status.md

> **目的**：记录阶段 2 Architect 完成状态

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "更新session-status" "" ""
```

#### 5.1 更新阶段完成记录

```bash
# 获取当前时间戳
COMPLETE_TIME=$(date +"%Y-%m-%d %H:%m:%S")

# 更新阶段 2 完成记录
sed -i "s/| 02 | 架构设计 |.*| ⏳ 待处理 |/| 02 | 架构设计 | $COMPLETE_TIME | ✅ 已生成 |/g" \
   "$ROOT/.claude/iterations/session-status.md"
```

#### 5.2 更新产出物追踪表

```bash
# 更新 ADR.md 产出物状态和完成时间
sed -i "s/| 02 | ADR.md | .claude/iterations/sprint-latest/ADR.md | ⏳ 待生成 |/| 02 | ADR.md | .claude/iterations/sprint-latest/ADR.md | ✅ 已生成 | $COMPLETE_TIME |/g" \
   "$ROOT/.claude/iterations/session-status.md"
```

#### 5.3 记录 Architect 阶段完成报告

```markdown
### 阶段 2 完成报告：架构设计（Architect-Stage2）

- **完成时间**：{当前时间戳}
- **执行摘要**：完成 ADR 文档生成，User Story 数量：$US_COUNT，Sub-feature 数量：$SF_COUNT
- **Milestone（里程碑）**：
  - User Story 数量：$US_COUNT
  - Sub-feature 数量：$SF_COUNT
  - ADR 章节数量：17
- **关键产出**：
  - [ADR.md]：[.claude/iterations/sprint-latest/ADR.md] - ✅
- **与上阶段的衔接**：依赖 BA-Stage1 的 requirements.md
- **发现的问题**：无（自检通过）
- **下一步**：进入 PM 审核阶段的前置条件：ADR 生成完成
- **需要 Human Gate 确认的事项**：无
```

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "产出物" "更新session-status" ".claude/iterations/session-status.md" "成功"
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "session-status更新" "" "成功"
```

---

### 操作 2.6：更新 project.md

> **目的**：更新迭代历史章节中 ADR.md 的状态

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤开始" "更新project.md" "" ""
```

#### 6.1 检查 project.md 是否存在

```bash
if [ ! -f "$ROOT/.claude/context/project.md" ]; then
  echo "[Architect-Stage2] project.md 不存在，跳过更新"
  bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "跳过" "project.md不存在" "" ""
  exit 0
fi
```

#### 6.2 更新迭代历史章节

```bash
# 获取当前时间戳
UPDATE_TIME=$(date +"%Y-%m-%d %H:%m:%S")

# 在迭代历史中更新 ADR.md 状态
sed -i "s/| ADR.md | ⏳ 待生成 |/| ADR.md | ✅ 已生成 | $UPDATE_TIME |/g" \
   "$ROOT/.claude/context/project.md"
```

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "步骤完成" "更新project.md" "" "成功"
```

---

### 操作 2.7：输出阶段摘要

> **目的**：向用户报告 Architect 阶段完成情况

#### 7.1 输入（Inputs）

| 输入 | 来源 | 用途 |
|------|------|------|
| requirements 主文档 | `.claude/iterations/sprint-latest/requirements.md` | 生成 ADR 的基础 |
| tech-stack-profile.md | `.claude/context/tech-stack-profile.md` | 技术栈参考 |
| consistency-baseline.md | `.claude/context/consistency-baseline.md` | 代码风格参考 |
| knowledge.grap | `.claude/context/knowledge.grap` | 受影响模块分析 |

#### 7.2 输出（Outputs）

| 输出 | 目的地 | 说明 |
|------|--------|------|
| ADR 主文档 | `.claude/iterations/sprint-latest/ADR.md` | 完整的架构设计文档 |

#### 7.3 执行摘要

示例：

```
[Architect-Stage2] 阶段 2 Architect 完成摘要：
- User Story 数量：5
- Sub-feature 数量：12
- ADR 章节数量：17
- 自检通过：是
- 产出物：
  - ADR.md：✅
```

#### 7.4 Human Gate 确认

> **目的**：向用户报告阶段 2 Architect 完成情况，等待确认

**等待用户确认以下内容**：

1. ADR 是否按模板完整生成（含第 2.4 节 Modular Group）
2. ADR 是否覆盖所有 User Story
3. **Modular Group 划分是否合理（后端 API + 前端 UI 配对，依赖关系正确）**
4. **US 依赖矩阵是否准确**
5. **Task 伪代码是否符合 consistency-baseline（命名、可复用代码、Skill 引用）**
6. **Task 伪代码文件是否独立生成（pseudocode/ 目录下，每个 Task 一个文件）**
7. 自检清单是否全部通过

**回复选项**：

- `继续` - 自检通过，允许 PM 进入审核阶段
- `打回` - 列出需要修正的问题，Architect 重新执行
- `暂停` - 暂停阶段 2，等待进一步指示

```bash
bash $ROOT/.claude/hooks/log-event.sh "$STAGE" "$AGENT_NAME" "等待" "Human Gate 确认" "" "待回复"
```

---

## 异常处理

| 异常场景 | 处理方式 |
|---------|---------|
| requirements.md 不存在 | 报错退出 |
| knowledge.grap 不可用 | 标注"手动分析"继续执行 |
| 自检不通过 | 修复后重新自检 |
| 设计冲突 | 按 conflict-resolution.md 升级给 PM |

---

## 关联文档

| 文档 | 路径 | 说明 |
|------|------|------|
| requirements 主文档 | `.claude/iterations/sprint-latest/requirements.md` | 生成 ADR 的基础 |
| ADR 模板 | `.claude/templates/adr-template.md` | ADR 文档模板 |
| tech-stack-profile.md | `.claude/context/tech-stack-profile.md` | 技术栈参考 |
| consistency-baseline.md | `.claude/context/consistency-baseline.md` | 代码风格参考 |
| knowledge.grap | `.claude/context/knowledge.grap` | 知识图谱 |
| mf-upgrade:02-arch-qa.md | `.claude/commands/mf-upgrade:02-arch-qa.md` | 阶段 2 playbook |