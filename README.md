# Skill Factory

Skill Factory 是一个面向 Codex 的最小 skill 开发基础设施。

它的目标是让用户只需要说明：

- 我能提供什么；
- 我想要什么；
- 输入是什么；
- 输出是什么；
- 验收标准是什么；
- 有哪些方案要求或限制；

之后由 agent 开发设施接管，将目标整理成 contract，创建 skill，执行测试，修复失败，独立验收，并在满足 contract 后交付。

核心原则是：

> 不让同一个 Agent 在同一个上下文里同时扮演开发者、执行者和验收者。  
> Skill 的通过必须来自干净执行、全流程测试和可审计证据，而不是来自“这次会话里看起来跑通了”。

---

## 项目定位

本项目不是重写 Codex 内置的 `$skill-creator`。

Codex 已经提供了成熟的 skill 创建逻辑，包括：

- `SKILL.md`
- `scripts/`
- `references/`
- `assets/`
- skill description 触发
- 渐进披露
- 基础验证

因此，本项目只补充 `$skill-creator` 没有完全覆盖的工程闭环：

- contract 制定；
- developer / executor / verifier 身份隔离；
- clean run；
- eval corpus；
- evidence gate；
- fail → patch → rerun 循环；
- 最终交付报告。

---

## 核心结构

```text
skill_factory/
├── AGENTS.md
├── .gitignore
├── .codex/
│   ├── config.toml
│   └── agents/
│       ├── skill-developer.toml
│       ├── clean-skill-executor.toml
│       └── skill-verifier.toml
└── .agents/
    └── skills/
        ├── contract-maker/
        │   ├── SKILL.md
        │   └── references/
        │       └── contract-template.md
        └── skill-factory-loop/
            ├── SKILL.md
            └── references/
                └── run-protocol.md
```

---

## 主要组件

### 1. `contract-maker`

负责把用户的顶层目标整理成稳定、可执行、可验收的 skill contract。

contract 是后续开发、测试、修复和验收的唯一事实来源。

它会定义：

- skill 目标；
- 用户可提供内容；
- 输入定义；
- 输出定义；
- should-trigger 条件；
- should-not-trigger 条件；
- MUST / SHOULD / COULD 验收标准；
- 方案约束；
- eval 设计；
- 证据要求；
- 完成定义。

contract 默认保存到：

```text
contracts/<skill-name>.contract.md
```

---

### 2. `skill-factory-loop`

负责在 contract 确认后接管后续开发流程。

它会编排：

1. 检查 contract 是否足够开发；
2. 调用 Codex 内置 `$skill-creator` 创建或更新目标 skill；
3. 建立 eval set；
4. 使用 `clean_skill_executor` 从干净环境执行 eval；
5. 使用 `skill_verifier` 独立验收 artifacts、logs 和 verdict；
6. 若失败，将 verifier 的失败摘要交给 `skill_developer` 修复；
7. 修复后重新从头测试；
8. 满足所有 MUST 后交付。

目标 skill 默认保存到：

```text
.agents/skills/<target-skill-name>/
```

运行过程默认保存到：

```text
skill-factory-workspace/<target-skill-name>/
```

---

### 3. `skill_developer`

Codex custom agent。

职责：

- 使用 `$skill-creator` 创建或更新 skill；
- 根据 verifier 的失败报告修复 skill；
- 将确定性、重复性、易错步骤沉淀为 `scripts/`；
- 将详细资料沉淀为 `references/`；
- 将模板和静态资源沉淀为 `assets/`。

禁止：

- 给自己判定通过；
- 修改 verifier verdict；
- 删除 eval 或降低验收标准；
- 将临时 debug 过程写进目标 skill。

---

### 4. `clean_skill_executor`

Codex custom agent。

职责：

- 从干净初始条件执行 eval；
- 像真实用户一样运行候选 skill；
- 保存 outputs、logs、trace 摘要和执行结果；
- 不读取 developer 的修复理由；
- 不修改目标 skill；
- 不判断 contract 是否通过。

每次执行应产生：

```text
execution_summary.json
```

---

### 5. `skill_verifier`

Codex custom agent。

职责：

- 根据 contract、eval metadata、execution summary 和 artifacts 独立验收；
- 判断 MUST / SHOULD / COULD；
- 检查 should-trigger / should-not-trigger；
- 检查是否存在过拟合、误触发、上下文污染或局部修复破坏全流程；
- 输出下一轮 patch brief。

每次验收应产生：

```text
verifier_verdict.json
```

---

## 运行前准备

### 1. 从仓库根目录启动 Codex

必须在 repo root 启动 Codex，确保 Codex 能读取：

```text
AGENTS.md
.agents/skills/
.codex/config.toml
.codex/agents/
```

启动示例：

```bash
cd skill_factory
codex
```

首次使用时，根据 Codex 提示信任当前 project config。

---

### 2. 检查 skills 是否可见

在 Codex 中运行：

```text
/skills
```

应能看到至少两个 repo-scoped skills：

- `contract-maker`
- `skill-factory-loop`

---

### 3. 不建议使用过宽权限

不建议在本项目中使用过宽的运行模式，例如：

```bash
codex --yolo
```

原因是本项目依赖身份隔离和权限边界。父会话过宽的 sandbox 或 approval override 可能削弱 verifier 的只读语义。

---

### 4. 不要提交运行产物

以下内容通常不应提交到公开仓库：

```text
skill-factory-workspace/
logs/
tmp/
outputs/
artifacts/
private contracts/
用户输入样例中的敏感文件
```

建议 `.gitignore` 至少忽略：

```gitignore
.DS_Store

skill-factory-workspace/
codex-logs/
.codex-log/
*.log

.venv/
__pycache__/
*.pyc

tmp/
outputs/
artifacts/

contracts/private/
```

---

## 推荐工作流

### 阶段 1：用户提供顶层目标

用户只需要描述：

- 想创建什么 skill；
- 可以提供哪些输入；
- 期望输出是什么；
- 如何判断成功；
- 有哪些限制或偏好。

推荐 prompt：

```text
请使用 contract-maker。我要创建一个新的 Codex skill。

我能提供：
- <文件、文本、示例、偏好、工具、环境>

我想要：
- <skill 最终要帮我稳定完成什么>

输入：
- <输入类型、格式、边界情况>

输出：
- <输出格式、文件、质量标准>

验收标准：
- <MUST / SHOULD / COULD；如果我没有分层，请帮我分层>

方案要求：
- <必须使用或禁止使用的技术、风格、工具、流程>

请先生成 contract 草案。
只问阻塞性问题；非阻塞缺口请写入默认假设。
```

---

### 阶段 2：确认 contract

`contract-maker` 会生成 contract 草案。

用户需要检查：

- 目标是否正确；
- 输入输出是否完整；
- MUST 是否真的必须；
- SHOULD / COULD 是否合理；
- 触发条件是否准确；
- 非触发条件是否覆盖相邻误用；
- 验收标准是否可测试。

确认后，将 contract 保存为：

```text
contracts/<skill-name>.contract.md
```

---

### 阶段 3：交给 skill-factory-loop 接管

推荐 prompt：

```text
请使用 skill-factory-loop 接管后续流程。

contract 路径：
contracts/<skill-name>.contract.md

本轮允许使用 subagents/custom agents：
- skill_developer
- clean_skill_executor
- skill_verifier

要求：
1. 使用 Codex 内置 $skill-creator 创建或更新目标 skill。
2. 使用 developer / executor / verifier 身份隔离执行。
3. 每次修改后，从干净初始条件重新运行相关 eval。
4. 不需要我参与实现细节。
5. 只有 contract 冲突、缺少必要资源、安全权限问题时才询问我。
6. 直到所有 MUST 通过，并给出最终交付报告。
```

---

## Smoke Test

正式开发真实 skill 前，建议先跑一次最小 smoke test。

目标不是创建有价值的 skill，而是确认基础设施链路闭合：

- contract 能生成；
- `$skill-creator` 能创建目标 skill；
- 三个 custom agents 能被使用；
- eval set 能建立；
- executor 能写 `execution_summary.json`；
- verifier 能写 `verifier_verdict.json`；
- 至少能完成一次 fail → patch → rerun；
- 最终能生成交付报告。

推荐 smoke test prompt：

```text
请使用 contract-maker，然后使用 skill-factory-loop 接管。

我要创建一个 toy skill：text-normalizer。

目标：
把用户提供的一段文本转换为规范化输出。

规则：
- 去除首尾空白；
- 连续空格压缩为一个空格；
- 输出 Markdown 代码块；
- 不改变中文标点；
- 如果输入为空，输出 EMPTY_INPUT。

输入：
- 用户直接提供的一段文本。

输出：
- 一个 Markdown 代码块。
- 代码块内是规范化后的文本。
- 空输入时，代码块内输出 EMPTY_INPUT。

MUST：
- 正常输入能规范化；
- 空输入能输出 EMPTY_INPUT；
- 输出必须是 Markdown 代码块；
- 不得依赖本次 session 的临时信息；
- 必须至少包含一个 should-trigger eval 和一个 should-not-trigger eval。

SHOULD：
- skill 的 description 能清楚说明何时使用和何时不使用；
- eval 结果应保存 execution_summary.json 和 verifier_verdict.json。

本轮允许使用 subagents/custom agents：
- skill_developer
- clean_skill_executor
- skill_verifier

请先生成 contract 草案。
contract 确认后，使用 skill-factory-loop 完成创建、测试、修复和交付。
```

---

## 成功交付标准

一个 skill 可以交付，当且仅当：

- contract 中所有 MUST 均通过；
- 没有高严重度 regression；
- should-trigger / should-not-trigger 没有关键错误；
- executor 输出 artifacts 可定位；
- verifier verdict 可追溯到 artifacts、logs 或明确 rubric；
- 修改后已重新从头执行相关 eval；
- 最终报告说明已知限制和使用方法。

最终交付报告至少应包含：

```text
skill 路径
contract 路径
eval 覆盖范围
iteration 数
最终 verifier verdict
主要证据路径
已知限制
用户如何调用该 skill
后续如何继续迭代
```

---

## 运行产物约定

每个目标 skill 使用独立工作区：

```text
skill-factory-workspace/<target-skill-name>/
├── evals/
│   └── evals.json
├── baselines/
│   ├── without_skill/
│   └── old_skill/
├── iteration-001/
│   ├── eval-001/
│   │   ├── eval_metadata.json
│   │   ├── with_skill/
│   │   │   ├── outputs/
│   │   │   └── execution_summary.json
│   │   ├── baseline/
│   │   │   ├── outputs/
│   │   │   └── execution_summary.json
│   │   └── verifier_verdict.json
│   └── iteration_summary.json
└── final_report.md
```

这些运行产物默认是开发过程证据，不是目标 skill 的一部分。

不要把运行日志、失败记录、临时假设或 debug 过程写进目标 skill 的 `SKILL.md`。

---

## Baseline 规则

baseline 用于比较“没有新 skill”或“旧 skill”的表现。

新 skill：

```text
baseline = without_skill
```

更新已有 skill：

```text
baseline = old_skill snapshot
```

注意：

如果无法保证 baseline 真的没有调用候选 skill，则 baseline 只能标记为 heuristic、not_run 或 blocked，不能作为强改进证据。

---

## 当前边界

当前版本是最小起点基础设施。

它依赖：

- Codex repo-scoped skills；
- Codex custom agents；
- `$skill-creator`；
- protocol-level evidence gate。

当前版本暂不包含完整 deterministic controller。

也就是说，流程控制仍主要由 `skill-factory-loop` 的协议和 Codex agent 执行能力完成，而不是由独立脚本强制状态转移。

如果 smoke test 中出现以下问题，应考虑新增脚本控制器：

- loop 跳过 verifier；
- executor 没有写 artifacts；
- verifier 只给自然语言判断，没有 JSON verdict；
- 失败后 developer 修了局部但没有重跑 eval；
- agent 修改 eval 或降低标准来让自己通过；
- 多轮后状态混乱，无法判断当前 iteration。

未来可新增：

```text
scripts/run_iteration.py
scripts/validate_skill_factory.py
scripts/collect_evidence.py
```

---

## 设计原则

### 1. Contract 是唯一事实来源

开发过程中的解释、猜测、临时 debug 结论、局部修复理由，都不能替代 contract。

### 2. Skill 不应携带开发上下文

目标 skill 只应包含执行者需要的程序性知识、必要引用、脚本和资源。

不应包含：

- 本轮失败日志；
- developer 的思考过程；
- 临时 workaround；
- 只适用于当前 session 的路径或文件名；
- 为某个 eval 硬编码的补丁。

### 3. 开发、执行、验收必须分离

同一个 agent 同时开发、执行、验收，容易产生：

- 上下文污染；
- 确认偏差；
- 临时补丁化；
- 局部通过但全流程破坏。

### 4. 通过必须有证据

不得用：

```text
我认为完成了
看起来没问题
应该可以
我已经测试过
```

作为通过依据。

通过必须来自：

- artifacts；
- logs；
- trace summary；
- checks；
- verifier verdict；
- contract criteria mapping。

### 5. 每次修复后重新从头测试

不允许只重跑失败片段并声称通过。

若修改影响：

- 触发条件；
- 输入处理；
- 输出格式；
- 核心流程；
- scripts；
- references；
- description；

则必须重新运行相关 eval。必要时重跑全部 eval。

---

## 推荐正式开发启动模板

```text
请使用 contract-maker 创建 contract，然后在我确认后使用 skill-factory-loop 接管。

我要创建的 skill：
<一句话目标>

我能提供：
- <文件、文本、样例、偏好、工具、环境>

输入：
- <输入类型、格式、边界情况>

输出：
- <输出格式、文件、质量标准>

验收标准：
MUST:
- <必须满足的条件>

SHOULD:
- <强烈建议满足的条件>

COULD:
- <可选增强>

方案要求：
- <必须使用 / 禁止使用 / 偏好>

触发条件：
- <用户怎样表达时应触发>

非触发条件：
- <哪些相邻任务不应触发>

本轮允许使用 subagents/custom agents：
- skill_developer
- clean_skill_executor
- skill_verifier

请先生成 contract 草案。
只问阻塞性问题；非阻塞缺口请写入默认假设。
```

---

## 项目状态

当前项目状态：

```text
alpha / smoke-test-first
```

推荐顺序：

1. 先跑 toy skill smoke test；
2. 确认 contract → skill → eval → execution summary → verifier verdict → final report 链路闭合；
3. 再进入第一个真实 skill 开发；
4. 若流程不稳定，再补 deterministic controller。

---

## 一句话总结

Skill Factory 的目标不是让 Agent 更忙，而是让 skill 开发从“会话里的临时修补”升级为：

> contract 驱动、身份隔离、干净执行、证据验收、可复现迭代的工程循环。