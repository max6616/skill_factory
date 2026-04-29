# Skill Factory 工作约定

本仓库用于把用户提供的顶层 skill 目标转化为可复现、可测试、可交付的 Codex skill。

## 核心原则

始终把已确认的 contract 视为唯一事实来源。开发过程中的解释、猜测、临时 debug 结论、局部修复理由，都不能替代 contract。

创建或更新 skill 时，优先使用 Codex 内置 `$skill-creator`。不要自行重写 skill-creator 的脚手架、命名、frontmatter、资源目录和基础验证逻辑；只在 contract、测试闭环、身份隔离和证据门层面补充编排。

不要把开发过程、测试记录、失败日志、临时假设写进目标 skill 的 `SKILL.md`。目标 skill 只应包含另一个 Codex 实例完成任务所需的核心程序性知识、必要引用、脚本和资源。

任何候选 skill 的通过，都必须建立在从用户入口开始的全流程测试上。修改 skill 后，不允许只重跑失败片段；必须从干净初始条件重新运行相关 eval，必要时重跑全部 eval。

## 用户参与边界

用户只需要提供：目标、输入、输出、验收标准、约束、偏好、示例和必要资源。

contract 确认后，除非缺少必要外部资源、存在安全/权限问题、或 contract 本身互相矛盾，不要再要求用户参与实现细节决策。

## 角色隔离

开发、执行、验收必须分离：

- `skill_developer`：只负责创建、修改、修复目标 skill，不允许给自己判定通过。
- `clean_skill_executor`：只负责在干净初始条件下执行 eval prompt，不读取 developer 的修复理由，不修改目标 skill。
- `skill_verifier`：只根据 contract、eval metadata、trace、logs、artifacts 和输出进行验收，不继承实现者假设，不修改目标 skill。

## 证据门

不得用“我认为完成了”“看起来没问题”作为交付依据。通过必须至少包含：

- contract 中所有 MUST 验收项的判定；
- 每个 eval 的输入、执行方式、输出位置；
- 相关命令、脚本或检查结果；
- verifier 的 pass/fail/blocked verdict；
- 若有失败，给出可复现失败摘要和下一轮修复 brief。

## 产物约定

目标 skill 放在 `.agents/skills/<target-skill-name>/`。

contract 放在 `contracts/<target-skill-name>.contract.md`。

eval 与运行结果放在 `skill-factory-workspace/<target-skill-name>/`，按 iteration 分层保存。

最终交付时必须报告：

- skill 路径；
- contract 路径；
- eval 覆盖范围；
- 最终 verdict；
- 已知限制；
- 用户如何安装、调用和继续迭代。
