# Graphify 查询速查表
- 触发条件：阶段 0、2、4 需要分析代码结构或依赖关系时
- 适用 Agent：架构师、开发者、PM

## 输入
- 查询类型（dependents/similar/query）
- 目标模块名或文件名（可选）

## 输出
- Graphify 分析结果（文本/结构化数据）
- 用于生成 consistency-baseline.md、分析模块依赖

## 查询命令

### 1. 依赖分析
```bash
graphify dependents <module-name>
```
**用途**：查看某模块被哪些模块依赖
**场景**：修改前评估影响范围

### 2. 相似代码查找
```bash
graphify similar <file-path>
```
**用途**：查找与目标文件类似的代码模式
**场景**：复用现有实现、设计新模块

### 3. 模式查询
```bash
graphify query "<自然语言描述>"
```
**用途**：用自然语言查询代码库中的模式
**示例**：
- `graphify query "most common patterns in the project"`
- `graphify query "error handling patterns"`

### 4. 项目结构更新
```bash
graphify update
```
**用途**：更新项目图谱（首次或代码大幅变更后）
**场景**：阶段 0 初始化、项目规模变更后

## 输出格式说明
- `dependents` 返回模块依赖树
- `similar` 返回相似文件列表（含相似度分数）
- `query` 返回匹配结果列表

## 异常处理
- 若 graphify 未安装：标注"图谱待安装"，跳过此步，用手动分析替代
- 若查询超时：重试一次，若仍失败，标注"查询超时 + graphify 可用时补充"