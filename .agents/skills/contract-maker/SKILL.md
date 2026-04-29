---
name: contract-maker
description: 将用户关于新建或改进 agent skill 的顶层目标转化为完整、可执行、可验收的 skill contract。Use when the user wants to create, update, outsource, evaluate, or self-iterate a skill and needs to define inputs, outputs, acceptance criteria, constraints, trigger conditions, non-trigger conditions, examples, evals, or delivery requirements before development begins.
---

# Contract Maker

你的任务是把用户的顶层意图转化为一个稳定的 skill contract。contract 是后续 skill 开发、执行、验证和交付的唯一事实来源。

## 工作目标

让用户只需要说明“我能提供什么、我想要什么、验收标准是什么”，而不需要参与后续实现细节。你负责把模糊目标转化为清晰、可测试、可泛化的 contract。

## 信息收集原则

优先从用户已提供的信息中提取 contract，不要重复询问已经明确的信息。

只在存在阻塞性缺口时提问。阻塞性缺口包括：输入来源不明、输出格式不明、验收标准冲突、必须依赖用户私有资源但资源未提供、存在安全或权限风险。

如果缺口不阻塞开发，写入“默认假设”并继续。不要为了追求完美 contract 而让用户陷入实现讨论。

## contract 必须覆盖

1. Skill 目标：这个 skill 要稳定完成什么任务。
2. 用户可提供内容：文件、文本、示例、偏好、环境、账号或外部工具。
3. 输入定义：输入类型、格式、路径、边界情况。
4. 输出定义：输出文件、格式、命名、质量标准、可接受变体。
5. 触发条件：用户怎样表达时应该使用该 skill。
6. 非触发条件：哪些相邻任务不应使用该 skill。
7. 验收标准：按 MUST / SHOULD / COULD 分层。
8. 方案要求：必须使用或禁止使用的技术、工具、流程、资源组织方式。
9. 测试策略：端到端 eval、should-trigger、should-not-trigger、历史失败样例。
10. 证据要求：什么 artifacts、logs、checks 能证明通过。
11. 安全与权限：外部访问、隐私、敏感数据、不可执行操作。
12. 完成定义：什么情况下可以交付，什么情况下必须继续迭代。

## 输出要求

生成 contract 时，使用 `references/contract-template.md` 的结构。

contract 应写成可以被另一个 Codex 实例直接执行的工程文件，而不是对话摘要。

contract 中不要包含冗长解释、开发过程、模型猜测或用户情绪描述。只保留对后续开发和验收有约束力的信息。

## 推荐产物路径

将最终 contract 保存为：

`contracts/<skill-name>.contract.md`

如果用户还未确认 contract，先输出“contract 草案”。用户确认后，标记为“已确认 contract”。

## 完成标准

当 contract 已经足以让 skill-factory-loop 接管后续开发、测试、修复和交付时，明确写出：

“contract 已准备好，可交给 skill-factory-loop 接管。”
