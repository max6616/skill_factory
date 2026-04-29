---
name: skill-factory-loop
description: 根据已确认 skill contract 自动接管 Codex skill 的创建、测试、修复、验证和交付。Use when the user wants the agent development infrastructure to build a skill from a contract, use Codex $skill-creator, run role-isolated clean evals, fix failures, and iterate until the skill satisfies contract acceptance criteria.
---

# Skill Factory Loop

你是 skill 开发基础设施的编排者。你的目标不是亲自凭会话上下文“把这次跑通”，而是建立一个可复现的开发—执行—验证闭环，让目标 skill 符合 contract。

## 前置条件

必须存在已确认 contract。若没有 contract，先使用 `contract-maker` 生成 contract。

必须有用户对 subagents/custom agents 的显式授权。若当前请求没有明确要求使用 `skill_developer`、`clean_skill_executor`、`skill_verifier` 或等价的子代理隔离流程，先要求用户确认后再进入闭环。

## 核心原则

1. 使用 Codex 内置 `$skill-creator` 创建或更新目标 skill。
2. 将 contract 作为唯一事实来源。
3. 分离 developer、executor、verifier 身份。
4. 每轮修改后，从干净初始条件重新执行 eval。
5. 以 evidence gate 判定通过，而不是以 agent 自述判定通过。
6. 不把开发过程污染到目标 skill。
7. 不通过降低 contract、删除 eval、缩小触发范围来制造通过。

## 基本流程

### 1. Contract readiness check

读取 contract，确认至少包含：

- skill 目标；
- 输入定义；
- 输出定义；
- 触发条件；
- 非触发条件；
- MUST 验收标准；
- 至少 2 个端到端 eval 或足以生成 eval 的真实示例；
- 证据要求。

若缺少阻塞信息，返回 contract-maker 阶段。若只是非阻塞缺口，写入默认假设并继续。

### 2. 创建或更新目标 skill

让 `skill_developer` 使用 `$skill-creator` 创建或更新目标 skill。

目标 skill 路径：

`.agents/skills/<target-skill-name>/`

开发者必须遵守：

- `SKILL.md` 保持简洁；
- scripts 用于确定性、重复性、易错流程；
- references 用于详细知识；
- assets 用于模板与静态资源；
- description 写清何时触发与边界；
- 不写入开发日志、测试过程、临时 debug 解释。

### 3. 建立 eval set

根据 contract 创建初始 eval set。至少包含：

- should-trigger；
- should-not-trigger；
- 端到端成功路径；
- 近邻误触发样例；
- 已知边界情况；
- 如有历史失败样例，必须纳入。

eval 文件建议保存到：

`skill-factory-workspace/<target-skill-name>/evals/evals.json`

### 4. Clean execution

对每个 eval，spawn `clean_skill_executor`，传入：

- 候选 skill 路径；
- eval prompt；
- 输入 fixtures；
- 输出目录；
- 需要保存的 artifacts 类型。

executor 只能执行，不得修改目标 skill。

每个 eval 输出保存到：

`skill-factory-workspace/<target-skill-name>/iteration-<N>/<eval-id>/with_skill/`

必要时同时运行 baseline：

- 新 skill：without_skill；
- 改已有 skill：old_skill snapshot。

### 5. Independent verification

对每个 eval，spawn `skill_verifier`，传入：

- contract；
- eval metadata；
- executor logs；
- outputs/artifacts；
- baseline 输出，如有。

verifier 只判定，不修改。

### 6. Evidence gate

整体通过条件：

- 所有 MUST 均 pass；
- 没有高严重度 regression；
- should-trigger 与 should-not-trigger 没有关键错误；
- artifacts、logs、verdict 足以复现；
- verifier overall 为 pass。

若失败：

- 汇总 verifier 的 `next_patch_brief`；
- 交给 `skill_developer` 修复；
- 进入下一 iteration；
- 重新从头运行相关 eval。若修改影响触发、输入、输出或核心流程，必须重跑全部 eval。

### 7. 交付

交付时输出：

- skill 路径；
- contract 路径；
- eval 覆盖范围；
- iteration 数；
- 最终 verifier verdict；
- 主要证据路径；
- 已知限制；
- 用户如何调用该 skill；
- 后续如何添加新 eval 或继续迭代。

## 停止条件

停止并交付：

- 所有 MUST 通过，verifier pass。

停止并报告 blocked：

- contract 冲突；
- 缺少必要用户资源；
- 环境无法执行关键测试；
- 安全或权限要求无法满足。

停止并报告未收敛：

- 多轮修复后同一 MUST 仍失败；
- verifier 判断修改开始过拟合；
- 新修改持续引入高严重度回归。

## 运行协议

具体目录、metadata、verdict schema 见：

`references/run-protocol.md`
