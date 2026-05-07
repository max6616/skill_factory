# Skill Factory

Skill Factory is a minimal Codex skill-development infrastructure.

Its goal is to let the user only describe:

- what they can provide;
- what they want;
- what the input is;
- what the output is;
- what the acceptance criteria are;
- what implementation requirements or constraints exist;

then let the agent-development infrastructure take over: turn the goal into a contract, create the skill, run tests, fix failures, verify independently, and deliver once the contract is satisfied.

The core principle is:

> Do not let the same Agent act as developer, executor, and verifier in the same context.  
> A Skill passes only through clean execution, end-to-end testing, and auditable evidence, not because "it looked like it worked in this session."

---

## Project Positioning

This project does not reimplement Codex's built-in `$skill-creator`.

Codex already provides mature skill-creation logic, including:

- `SKILL.md`
- `scripts/`
- `references/`
- `assets/`
- skill description triggering
- progressive disclosure
- baseline validation

Therefore, this project only adds the engineering loop that `$skill-creator` does not fully cover:

- contract creation;
- developer / executor / verifier role isolation;
- clean runs;
- eval corpus;
- evidence gate;
- fail -> patch -> rerun loop;
- final delivery report.

---

## Core Structure

```text
skill_factory/
|-- AGENTS.md
|-- .gitignore
|-- .codex/
|   |-- config.toml
|   `-- agents/
|       |-- skill-developer.toml
|       |-- skill-executor.toml
|       `-- skill-verifier.toml
`-- .agents/
    `-- skills/
        |-- contract-maker/
        |   |-- SKILL.md
        |   `-- references/
        |       `-- contract-template.md
        `-- skill-factory-loop/
            |-- SKILL.md
            `-- references/
                `-- run-protocol.md
```

---

## Main Components

### 1. `contract-maker`

Turns the user's top-level goal into a stable, executable, verifiable skill contract.

The contract is the single source of truth for later development, testing, repair, and verification.

It defines:

- skill goal;
- user-provided content;
- input definition;
- output definition;
- should-trigger conditions;
- should-not-trigger conditions;
- MUST / SHOULD / COULD acceptance criteria;
- implementation constraints;
- eval design;
- evidence requirements;
- definition of done.

Contracts are saved by default to:

```text
contracts/<skill-name>.contract.md
```

---

### 2. `skill-factory-loop`

Takes over the development process after the contract is confirmed.

It orchestrates:

1. Check whether the contract is ready for development.
2. Use Codex's built-in `$skill-creator` to create or update the target skill.
3. Build the eval set.
4. Use `skill_executor` to execute evals from a clean environment.
5. Use `skill_verifier` to independently verify artifacts, logs, and verdicts.
6. If verification fails, give the verifier's failure summary to `skill_developer` for repair.
7. After repair, rerun testing from the beginning.
8. Deliver after all MUST criteria pass.

Target skills are saved by default to:

```text
.agents/skills/<target-skill-name>/
```

Run data is saved by default to:

```text
skill-factory-workspace/<target-skill-name>/
```

---

### 3. `skill_developer`

Codex custom agent.

Responsibilities:

- Use `$skill-creator` to create or update the skill.
- Fix the skill based on verifier failure reports.
- Put deterministic, repeatable, error-prone steps into `scripts/`.
- Put detailed reference material into `references/`.
- Put templates and static resources into `assets/`.

Forbidden:

- Decide that its own work passes.
- Modify verifier verdicts.
- Delete evals or lower acceptance standards.
- Write temporary debug process into the target skill.

---

### 4. `skill_executor`

Codex custom agent.

Responsibilities:

- Execute evals from clean initial conditions.
- Run the candidate skill like a real user would.
- Save outputs, logs, trace summaries, and execution results.
- Do not read the developer's fix rationale.
- Do not modify the target skill.
- Do not decide whether the contract passes.

Each execution should produce:

```text
execution_summary.json
```

---

### 5. `skill_verifier`

Codex custom agent.

Responsibilities:

- Independently verify from the contract, eval metadata, execution summary, and artifacts.
- Judge MUST / SHOULD / COULD.
- Check should-trigger / should-not-trigger behavior.
- Check for overfitting, false triggering, context contamination, or local fixes that break the full workflow.
- Output the next patch brief.

Each verification should produce:

```text
verifier_verdict.json
```

---

## Setup Before Running

### 1. Start Codex From The Repository Root

Start Codex from the repo root so Codex can read:

```text
AGENTS.md
.agents/skills/
.codex/config.toml
.codex/agents/
```

Example:

```bash
cd skill_factory
codex
```

On first use, trust the current project config when Codex prompts you.

---

### 2. Check That Skills Are Visible

Run this in Codex:

```text
/skills
```

You should see at least two repo-scoped skills:

- `contract-maker`
- `skill-factory-loop`

---

### 3. Avoid Overly Broad Permissions

Avoid overly broad run modes in this project, for example:

```bash
codex --yolo
```

The reason is that this project relies on role isolation and permission boundaries. An overly broad parent-session sandbox or approval override may weaken the verifier's read-only semantics.

---

### 4. Do Not Commit Run Artifacts

The following content usually should not be committed to a public repository:

```text
skill-factory-workspace/
logs/
tmp/
outputs/
artifacts/
private contracts/
sensitive files from user input examples
```

The `.gitignore` should at least ignore:

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

## Recommended Workflow

### Phase 1: The User Provides The Top-Level Goal

The user only needs to describe:

- what skill they want to create;
- what inputs they can provide;
- what output they expect;
- how success should be judged;
- what constraints or preferences exist.

Recommended prompt:

```text
Please use contract-maker. I want to create a new Codex skill.

I can provide:
- <files, text, examples, preferences, tools, environment>

I want:
- <what the skill should reliably help me do>

Input:
- <input type, format, edge cases>

Output:
- <output format, files, quality standards>

Acceptance criteria:
- <MUST / SHOULD / COULD; if I did not layer them, please layer them for me>

Implementation requirements:
- <required or forbidden technologies, style, tools, workflow>

Please generate a contract draft first.
Only ask blocking questions; write non-blocking gaps as default assumptions.
```

---

### Phase 2: Confirm The Contract

`contract-maker` generates a contract draft.

The user should check:

- whether the goal is correct;
- whether inputs and outputs are complete;
- whether each MUST is truly mandatory;
- whether SHOULD / COULD items are reasonable;
- whether trigger conditions are accurate;
- whether non-trigger conditions cover adjacent misuse;
- whether acceptance criteria are testable.

After confirmation, save the contract as:

```text
contracts/<skill-name>.contract.md
```

---

### Phase 3: Hand Off To skill-factory-loop

Recommended prompt:

```text
Please use skill-factory-loop to take over the rest of the process.

Contract path:
contracts/<skill-name>.contract.md

This round may use subagents/custom agents:
- skill_developer
- skill_executor
- skill_verifier

Requirements:
1. Use Codex's built-in $skill-creator to create or update the target skill.
2. Use developer / executor / verifier role isolation.
3. After every change, rerun the relevant evals from clean initial conditions.
4. I do not need to participate in implementation details.
5. Ask me only if the contract conflicts, required resources are missing, or there is a safety/permission issue.
6. Continue until all MUST criteria pass and provide a final delivery report.
```

---

## Smoke Test

Before developing a real skill, run a minimal smoke test.

The goal is not to create a valuable skill, but to confirm that the infrastructure loop closes:

- the contract can be generated;
- `$skill-creator` can create the target skill;
- the three custom agents can be used;
- the eval set can be built;
- the executor can write `execution_summary.json`;
- the verifier can write `verifier_verdict.json`;
- at least one fail -> patch -> rerun loop can complete;
- a final delivery report can be generated.

Recommended smoke test prompt:

```text
Please use contract-maker, then use skill-factory-loop to take over.

I want to create a toy skill: text-normalizer.

Goal:
Convert a text snippet provided by the user into normalized output.

Rules:
- Trim leading and trailing whitespace.
- Collapse consecutive spaces into one space.
- Output a Markdown code block.
- Do not change CJK punctuation.
- If the input is empty, output EMPTY_INPUT.

Input:
- A text snippet provided directly by the user.

Output:
- One Markdown code block.
- The code block contains the normalized text.
- For empty input, the code block contains EMPTY_INPUT.

MUST:
- Normal input can be normalized.
- Empty input can output EMPTY_INPUT.
- Output must be a Markdown code block.
- The skill must not depend on temporary information from this session.
- There must be at least one should-trigger eval and one should-not-trigger eval.

SHOULD:
- The skill description should clearly explain when to use it and when not to use it.
- Eval results should save execution_summary.json and verifier_verdict.json.

This round may use subagents/custom agents:
- skill_developer
- skill_executor
- skill_verifier

Please generate a contract draft first.
After the contract is confirmed, use skill-factory-loop to complete creation, testing, repair, and delivery.
```

---

## Successful Delivery Standard

A skill can be delivered if and only if:

- all MUST criteria in the contract pass;
- there is no high-severity regression;
- should-trigger / should-not-trigger behavior has no critical error;
- executor output artifacts can be located;
- verifier verdicts can be traced to artifacts, logs, or an explicit rubric;
- relevant evals have been rerun from the beginning after changes;
- the final report explains known limitations and usage.

The final delivery report must include at least:

```text
skill path
contract path
eval coverage
iteration count
final verifier verdict
main evidence paths
known limitations
how the user can invoke this skill
how to continue iterating later
```

---

## Run Artifact Conventions

Each target skill uses its own workspace:

```text
skill-factory-workspace/<target-skill-name>/
|-- evals/
|   `-- evals.json
|-- baselines/
|   |-- without_skill/
|   `-- old_skill/
|-- iteration-001/
|   |-- eval-001/
|   |   |-- eval_metadata.json
|   |   |-- with_skill/
|   |   |   |-- outputs/
|   |   |   `-- execution_summary.json
|   |   |-- baseline/
|   |   |   |-- outputs/
|   |   |   `-- execution_summary.json
|   |   `-- verifier_verdict.json
|   `-- iteration_summary.json
`-- final_report.md
```

These run artifacts are development evidence by default, not part of the target skill.

Do not write run logs, failure records, temporary assumptions, or debug process into the target skill's `SKILL.md`.

---

## Baseline Rules

The baseline is used to compare behavior "without the new skill" or with the "old skill."

New skill:

```text
baseline = without_skill
```

Updating an existing skill:

```text
baseline = old_skill snapshot
```

Note:

If you cannot guarantee that the baseline truly did not call the candidate skill, mark the baseline only as heuristic, not_run, or blocked. Do not use it as strong improvement evidence.

---

## Current Boundaries

The current version is a minimal starting infrastructure.

It depends on:

- Codex repo-scoped skills;
- Codex custom agents;
- `$skill-creator`;
- a protocol-level evidence gate.

The current version does not yet include a complete deterministic controller.

In other words, process control is still mostly handled by the `skill-factory-loop` protocol and Codex agent execution capability, rather than by an independent script that enforces state transitions.

If the smoke test shows any of the following issues, consider adding a script controller:

- the loop skips the verifier;
- the executor does not write artifacts;
- the verifier gives only a natural-language judgment and no JSON verdict;
- after failure, the developer fixes a local fragment but does not rerun evals;
- an agent modifies evals or lowers standards to make itself pass;
- after multiple rounds, state is confused and the current iteration cannot be identified.

Possible future additions:

```text
scripts/run_iteration.py
scripts/validate_skill_factory.py
scripts/collect_evidence.py
```

---

## Design Principles

### 1. The Contract Is The Single Source Of Truth

Explanations, guesses, temporary debug conclusions, and local fix rationales from development cannot replace the contract.

### 2. The Skill Should Not Carry Development Context

The target skill should contain only the procedural knowledge, necessary references, scripts, and resources the executor needs.

It should not include:

- failure logs from this round;
- the developer's reasoning process;
- temporary workarounds;
- paths or filenames that apply only to the current session;
- patches hardcoded for a specific eval.

### 3. Development, Execution, And Verification Must Be Separated

When the same agent develops, executes, and verifies, it can easily create:

- context contamination;
- confirmation bias;
- temporary patching;
- local pass with full-workflow breakage.

### 4. Passing Requires Evidence

Do not use:

```text
I think it is done
It looks fine
It should work
I already tested it
```

as passing evidence.

Passing must come from:

- artifacts;
- logs;
- trace summaries;
- checks;
- verifier verdicts;
- contract criteria mapping.

### 5. Retest From The Beginning After Every Fix

Do not rerun only the failed fragment and claim it passes.

If a change affects:

- trigger conditions;
- input handling;
- output format;
- core workflow;
- scripts;
- references;
- description;

then rerun the relevant evals. Rerun all evals when necessary.

---

## Recommended Formal Development Start Template

```text
Please use contract-maker to create a contract, then use skill-factory-loop after I confirm it.

The skill I want to create:
<one-sentence goal>

I can provide:
- <files, text, examples, preferences, tools, environment>

Input:
- <input type, format, edge cases>

Output:
- <output format, files, quality standards>

Acceptance criteria:
MUST:
- <mandatory conditions>

SHOULD:
- <strongly recommended conditions>

COULD:
- <optional enhancements>

Implementation requirements:
- <required / forbidden / preferred>

Trigger conditions:
- <how the user should express the request for the skill to trigger>

Non-trigger conditions:
- <which adjacent tasks should not trigger the skill>

This round may use subagents/custom agents:
- skill_developer
- skill_executor
- skill_verifier

Please generate a contract draft first.
Only ask blocking questions; write non-blocking gaps as default assumptions.
```

---

## Project Status

Current project status:

```text
alpha / smoke-test-first
```

Recommended order:

1. Run the toy skill smoke test first.
2. Confirm that the contract -> skill -> eval -> execution summary -> verifier verdict -> final report loop closes.
3. Then move into the first real skill development.
4. If the process is unstable, add the deterministic controller.

---

## One-Sentence Summary

Skill Factory's goal is not to make the Agent busier, but to upgrade skill development from "temporary patching inside a session" into:

> a contract-driven, role-isolated, cleanly executed, evidence-verified, reproducible iteration loop.
