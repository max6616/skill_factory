# Skill Contract: text-normalizer

## 0. Contract Status

Status: confirmed  
Version: v0.1  
Last updated: 2026-04-29  
User confirmation method: conversation explicit approval

## 1. Skill Goal

This skill should let Codex reliably complete the following task:

Convert a text snippet provided directly by the user into normalized text and output it as a Markdown fenced code block. Normalization rules include trimming leading and trailing whitespace, collapsing consecutive half-width spaces into one half-width space, preserving CJK punctuation unchanged, and outputting `EMPTY_INPUT` for empty input.

## 2. User-Provided Content

The user may provide:

- A text snippet directly in the conversation.
- No required user resources, files, accounts, external tools, or APIs.

## 3. Input Definition

Input type:

- Text

Input format:

- A text snippet provided directly by the user in a natural-language request.
- Input may contain CJK text, English, numbers, symbols, CJK punctuation, half-width spaces, and leading or trailing whitespace characters.

Edge cases:

- Treat an empty string, or a string containing only whitespace, as empty input.
- Remove leading and trailing whitespace.
- Collapse consecutive internal half-width spaces into a single half-width space.
- CJK punctuation, such as `，。！？；：“”‘’、（）《》`, must not be converted, deleted, or replaced.
- If the output text itself contains triple backticks, choose a longer Markdown fence so the output remains a valid code block.

## 4. Output Definition

Must output:

- One Markdown fenced code block.

Output format:

- The output contains only one Markdown code block.
- The code block contains the normalized text.
- For empty input, the code block content must be `EMPTY_INPUT`.
- The code block does not need a language identifier.

Quality standards:

- The output must be recognizable as a code block by Markdown renderers.
- The code block must not contain extra explanations, prefixes, suffixes, or debug information.
- Except for the specified whitespace normalization, do not change the original text content, especially CJK punctuation.

## 5. Trigger Conditions

should-trigger:

- The user asks for a text-normalization task, such as "normalize this text", "clean up spacing and output a code block", or equivalent wording.
- The user directly provides text and asks to trim leading/trailing whitespace, collapse consecutive spaces, or output the normalized result as a Markdown code block.
- The user explicitly mentions using the `text-normalizer` skill.

## 6. Non-Trigger Conditions

should-not-trigger:

- The user asks for translation, rewriting, polishing, summarization, correction, expansion, classification, keyword extraction, or semantic analysis.
- The user asks to format code, JSON, Markdown documents, tables, or config files rather than normalize plain text.
- The user is only discussing the concept, algorithm, or implementation of "text normalization" and is not asking to process concrete input text.
- The user asks to change CJK punctuation, normalize full-width/half-width characters, delete punctuation, or adjust writing style.

## 7. Acceptance Criteria

### MUST

- Normal input can be normalized according to the rules.
- Empty input can output `EMPTY_INPUT`.
- Output must be a Markdown fenced code block.
- The code block must not contain temporary information from the current session, development process details, paths, timestamps, or explanatory text.
- The skill must not rely on temporary context from the current session, temporary files, agent memory, or conventions not written into the skill.
- There must be at least one should-trigger eval.
- There must be at least one should-not-trigger eval.
- CJK punctuation must not be changed.

### SHOULD

- The skill `description` clearly explains when to use it and when not to use it.
- Eval results should save `execution_summary.json` and `verifier_verdict.json`.
- Evals cover normal input, empty input, CJK punctuation preservation, and Markdown code block format.
- The skill content should be concise and contain only the procedural knowledge needed to complete the task.

### COULD

- Support input containing Markdown fence characters by automatically using a longer fence to avoid breaking the code block.
- Provide a lightweight script or checker to verify that the output is a single Markdown code block.

## 8. Implementation Requirements And Constraints

Must follow:

- Place the target skill in `.agents/skills/text-normalizer/`.
- Save the contract as `contracts/text-normalizer.contract.md`.
- Save evals and run results in `skill-factory-workspace/text-normalizer/`, layered by iteration.
- Prefer Codex's built-in `$skill-creator` when creating or updating the skill.
- Development, execution, and verification must be role-isolated:
  - `skill_developer` only creates, modifies, and fixes the target skill.
  - `skill_executor` only executes eval prompts from clean initial conditions.
  - `skill_verifier` verifies only from the contract, eval metadata, trace, logs, artifacts, and outputs.

Forbidden:

- Do not write the development process, failure logs, temporary debug conclusions, or fix rationales into the target skill's `SKILL.md`.
- Do not let the developer decide final pass status.
- Do not prove a fix by rerunning only the failed fragment; after changing the skill, rerun the relevant eval from clean initial conditions.
- Do not access the network, call external APIs, access private resources, or depend on files the user did not provide.

Degrees of freedom:

- High freedom: organization of the skill's internal instructions and exact wording of eval prompts.
- Medium freedom: whether to add a lightweight automated checking script.
- Low freedom: normalization rules, output code block format, role isolation, and evidence requirements.

## 9. Eval Design

End-to-end eval:

- id: e2e-001
  prompt: |
    Use text-normalizer to normalize the following text:

        Hello，   world！  This   is  a   test。
  expected_output: |
    ```
    Hello， world！ This is a test。
    ```
  input_files: none

- id: e2e-002
  prompt: |
    Use text-normalizer to process the following input:

       
  expected_output: |
    ```
    EMPTY_INPUT
    ```
  input_files: none

should-trigger eval:

- query: |
    Trim leading and trailing whitespace, collapse consecutive spaces, and output this text as a Markdown code block:

       A   B  C，  hello！   
  expected_behavior: Should trigger text-normalizer and output a single Markdown code block containing `A B C， hello！`.

should-not-trigger eval:

- query: |
    Translate 'Hello， world！' into Spanish.
  expected_behavior: Should not trigger text-normalizer because this is a translation task, not a text-normalization task.

Historical failure examples:

- None.

## 10. Evidence Requirements

Passing must provide:

- Each eval's input prompt, execution method, and output location.
- `execution_summary.json`, recording eval id, trigger decision, actual output, format check result, and normalization check result.
- `verifier_verdict.json`, recording the verifier's pass/fail/blocked verdict for each MUST/SHOULD item.
- Execution logs or trace summary.
- Output artifact paths.
- For any failure, a reproducible failure summary and the next repair brief.

## 11. Safety, Privacy, And Permissions

Sensitive data:

- None by default. User input text may contain arbitrary content, but the skill should not persist user text except as eval artifacts.

External access:

- Forbidden. This skill does not need network access, external APIs, or remote services.

High-risk operations:

- No deletion, publishing, network access, paid APIs, system configuration changes, or cross-directory writes are involved.

## 12. Definition Of Done

Deliverable if and only if:

- All MUST acceptance items pass.
- At least one should-trigger eval and at least one should-not-trigger eval have been executed and evidence has been retained.
- Normal input, empty input, CJK punctuation preservation, and Markdown code block format are all covered by evals.
- `execution_summary.json` and `verifier_verdict.json` have been saved.
- The verifier gives a pass verdict.
- Known limitations are written into the final delivery note.

## 13. Default Assumptions

- "Consecutive spaces" means consecutive half-width spaces, `U+0020`.
- "Leading/trailing whitespace" includes common leading and trailing whitespace characters such as half-width spaces, tabs, and newlines.
- Full-width/half-width conversion is not required.
- Spaces around CJK punctuation do not need to be compressed unless those spaces are part of a consecutive half-width space sequence.
- The output code block may omit a language identifier.
