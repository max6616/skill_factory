# Skill Contract: text-normalizer

## 0. Contract 状态

状态：已确认  
版本：v0.1  
最后更新：2026-04-29  
用户确认方式：conversation explicit approval

## 1. Skill 目标

这个 skill 要让 Codex 能够稳定完成：

将用户直接提供的一段文本转换为规范化文本，并以 Markdown fenced code block 输出。规范化规则包括去除首尾空白、将连续半角空格压缩为一个半角空格、保留中文标点不变；空输入时输出 `EMPTY_INPUT`。

## 2. 用户可提供内容

用户可以提供：

- 一段直接出现在对话中的文本。
- 无必需用户资源、文件、账号、外部工具或 API。

## 3. 输入定义

输入类型：

- 文本

输入格式：

- 用户在自然语言请求中直接提供的一段文本。
- 输入可以包含中文、英文、数字、符号、中文标点、半角空格，以及首尾空白字符。

边界情况：

- 输入为空字符串，或仅包含空白字符时，视为空输入。
- 首尾空白应去除。
- 文本内部连续半角空格应压缩为一个半角空格。
- 中文标点，例如 `，。！？；：“”‘’、（）《》`，不得被转换、删除或替换。
- 若输出文本本身包含 triple backticks，必须选择更长的 Markdown fence，保证输出仍是有效代码块。

## 4. 输出定义

必须输出：

- 一个 Markdown fenced code block。

输出格式：

- 输出只包含一个 Markdown code block。
- code block 内是规范化后的文本。
- 空输入时，code block 内必须是 `EMPTY_INPUT`。
- code block 不要求指定语言标识。

质量标准：

- 输出必须可被 Markdown 渲染器识别为代码块。
- code block 内不得包含额外解释、前后缀说明或调试信息。
- 除指定空白规范化外，不改变原文本内容，尤其不改变中文标点。

## 5. 触发条件

should-trigger：

- 用户要求“规范化这段文本”“normalize this text”“整理空格并输出代码块”等文本规范化任务。
- 用户直接提供文本，并要求去除首尾空白、压缩连续空格、或以 Markdown 代码块输出规范化结果。
- 用户显式提到使用 `text-normalizer` skill。

## 6. 非触发条件

should-not-trigger：

- 用户要求翻译、改写、润色、摘要、纠错、扩写、分类、提取关键词或语义分析。
- 用户要求格式化代码、JSON、Markdown 文档、表格或配置文件，而不是普通文本规范化。
- 用户只是在讨论“文本规范化”概念、算法或实现方式，没有要求处理具体输入文本。
- 用户要求改变中文标点、统一全角半角、删除标点或做语言风格调整。

## 7. 验收标准

### MUST

- 正常输入能按规则规范化。
- 空输入能输出 `EMPTY_INPUT`。
- 输出必须是 Markdown fenced code block。
- code block 内不得包含本次 session 的临时信息、开发过程、路径、时间戳或解释性文字。
- 不得依赖本次 session 的临时上下文、临时文件、agent 记忆或未写入 skill 的约定。
- 必须至少包含一个 should-trigger eval。
- 必须至少包含一个 should-not-trigger eval。
- 不得改变中文标点。

### SHOULD

- skill 的 `description` 能清楚说明何时使用和何时不使用。
- eval 结果应保存 `execution_summary.json` 和 `verifier_verdict.json`。
- eval 覆盖正常输入、空输入、中文标点保留、Markdown code block 格式。
- skill 内容应简洁，只包含完成任务所需的程序性知识。

### COULD

- 支持含有 Markdown fence 字符的输入，并自动使用更长 fence 避免破坏代码块。
- 提供一个轻量脚本或检查器验证输出是否为单一 Markdown code block。

## 8. 方案要求与限制

必须遵守：

- 目标 skill 放在 `.agents/skills/text-normalizer/`。
- contract 保存为 `contracts/text-normalizer.contract.md`。
- eval 与运行结果放在 `skill-factory-workspace/text-normalizer/`，按 iteration 分层保存。
- 创建或更新 skill 时优先使用 Codex 内置 `$skill-creator`。
- 开发、执行、验收必须角色隔离：
  - `skill_developer` 只负责创建、修改、修复目标 skill。
  - `clean_skill_executor` 只负责在干净初始条件下执行 eval prompt。
  - `skill_verifier` 只根据 contract、eval metadata、trace、logs、artifacts 和输出验收。

禁止：

- 不得把开发过程、失败日志、临时 debug 结论或修复理由写进目标 skill 的 `SKILL.md`。
- 不得让 developer 自行判定最终通过。
- 不得只重跑失败片段来证明修复通过；修改 skill 后必须从干净初始条件重新运行相关 eval。
- 不得联网、调用外部 API、访问私有资源或依赖用户未提供的文件。

自由度：

- 高自由度：skill 内部说明的组织方式、eval prompt 的具体措辞。
- 中自由度：是否增加轻量自动检查脚本。
- 低自由度：规范化规则、输出 code block 格式、角色隔离、证据要求。

## 9. Eval 设计

端到端 eval：

- id: e2e-001
  prompt: |
    使用 text-normalizer 规范化下面这段文本：

        你好，   世界！  这是   一个  test。
  expected_output: |
    ```
    你好， 世界！ 这是 一个 test。
    ```
  input_files: 无

- id: e2e-002
  prompt: |
    使用 text-normalizer 处理下面的输入：

       
  expected_output: |
    ```
    EMPTY_INPUT
    ```
  input_files: 无

should-trigger eval：

- query: |
    请把这段文本去掉首尾空白、压缩连续空格，并用 Markdown 代码块输出：

       A   B  C，  你好！   
  expected_behavior: 应触发 text-normalizer，并输出单一 Markdown code block，内容为 `A B C， 你好！`。

should-not-trigger eval：

- query: |
    请把“你好，世界！”翻译成英文。
  expected_behavior: 不应触发 text-normalizer，因为这是翻译任务，不是文本规范化任务。

历史失败样例：

- 无。

## 10. 证据要求

通过时必须提供：

- 每个 eval 的输入 prompt、执行方式、输出位置。
- `execution_summary.json`，记录 eval id、触发判定、实际输出、格式检查结果和规范化检查结果。
- `verifier_verdict.json`，记录 verifier 对每个 MUST/SHOULD 项的 pass/fail/blocked 判定。
- 执行日志或 trace 摘要。
- 输出 artifacts 路径。
- 若有失败，提供可复现失败摘要和下一轮修复 brief。

## 11. 安全、隐私与权限

敏感数据：

- 默认无。用户输入文本可能包含任意内容，但 skill 不应持久化除 eval artifacts 外的用户文本。

外部访问：

- 禁止。该 skill 不需要网络、外部 API 或远程服务。

高风险操作：

- 不涉及删除、发布、联网、付费 API、系统配置修改或跨目录写入。

## 12. 完成定义

可以交付当且仅当：

- 所有 MUST 验收项通过。
- 至少一个 should-trigger eval 和至少一个 should-not-trigger eval 已执行并留存证据。
- 正常输入、空输入、中文标点保留、Markdown code block 格式均被 eval 覆盖。
- `execution_summary.json` 和 `verifier_verdict.json` 已保存。
- verifier 给出 pass verdict。
- 已知限制已写入最终交付说明。

## 13. 默认假设

- “连续空格”指连续半角空格 `U+0020`。
- “首尾空白”包括常见前后空白字符，例如半角空格、tab 和换行。
- 不要求进行全角/半角转换。
- 不要求压缩中文标点周围的空格，除非这些空格属于连续半角空格序列。
- 输出 code block 可以不带语言标识。
