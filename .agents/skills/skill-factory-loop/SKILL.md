---
name: skill-factory-loop
description: Build and verify a Codex skill from a confirmed contract. Use to run a role-isolated loop with $skill-creator, skill_developer, skill_executor, skill_verifier, clean evals, evidence gates, fixes, and final delivery.
---

# Skill Factory Loop

You are the orchestrator for skill-development infrastructure. Your goal is not to personally "make it work in this session" from conversational context, but to build a reproducible development-execution-verification loop so the target skill satisfies the contract.

## Preconditions

A confirmed contract must exist. If there is no contract, first use `contract-maker` to generate one.

The user must explicitly authorize subagents/custom agents.

Any of the following counts as authorization for this round:
- The user explicitly invokes `$skill-factory-loop`.
- The user says "please use skill-factory-loop to take over."
- The contract states that `skill_developer`, `skill_executor`, and `skill_verifier` may be used.
- The starting prompt states that subagents/custom agents may be used this round to complete the development, execution, and verification loop.

If none of the above authorization exists, do not enter the loop; output one sentence asking for user confirmation.

## Core Principles

1. Use Codex's built-in `$skill-creator` to create or update the target skill.
2. Treat the contract as the single source of truth.
3. Separate developer, executor, and verifier roles.
4. After each modification round, rerun evals from clean initial conditions.
5. Judge pass through an evidence gate, not through agent self-report.
6. Do not pollute the target skill with development process.
7. Do not manufacture a pass by lowering the contract, deleting evals, or narrowing trigger scope.

## Basic Flow

Baseline rules:

- For a new skill, the baseline is optional and is not a MUST pass condition.
- If running a without_skill baseline, use one of these methods:
  1. Explicitly forbid reading or invoking the candidate skill in the baseline executor prompt, and record that this is a heuristic baseline.
  2. Temporarily move the candidate skill snapshot out of `.agents/skills`, then restart Codex or open a new session.
  3. Disable the target skill with the custom agent's skills.config if the current Codex environment supports dynamic configuration.
- If you cannot guarantee that the baseline did not use the target skill, mark the baseline as `blocked` or `not_run`; do not use it as improvement evidence.

### 1. Contract Readiness Check

Read the contract and confirm that it contains at least:

- skill goal;
- input definition;
- output definition;
- trigger conditions;
- non-trigger conditions;
- MUST acceptance criteria;
- at least two end-to-end evals, or real examples sufficient to generate evals;
- evidence requirements.

If blocking information is missing, return to the contract-maker phase. If only non-blocking gaps exist, write default assumptions and continue.

### 2. Create Or Update The Target Skill

Have `skill_developer` use `$skill-creator` to create or update the target skill.

Target skill path:

`.agents/skills/<target-skill-name>/`

The developer must follow:

- Keep `SKILL.md` concise.
- Use scripts for deterministic, repeatable, error-prone flows.
- Use references for detailed knowledge.
- Use assets for templates and static resources.
- Make the description clear about trigger conditions and boundaries.
- Do not write development logs, test process, or temporary debug explanations.

### 3. Build The Eval Set

Create the initial eval set from the contract. Include at least:

- should-trigger;
- should-not-trigger;
- end-to-end success path;
- adjacent false-trigger examples;
- known edge cases;
- historical failure examples, if any.

Recommended eval file path:

`skill-factory-workspace/<target-skill-name>/evals/evals.json`

### 4. Clean Execution

For each eval, spawn `skill_executor` and pass:

- candidate skill path;
- eval prompt;
- input fixtures;
- output directory;
- artifact types that must be saved.

The executor can only execute and must not modify the target skill.

Save each eval output under:

`skill-factory-workspace/<target-skill-name>/iteration-<N>/<eval-id>/with_skill/`

When needed, also run a baseline:

- New skill: without_skill.
- Existing skill update: old_skill snapshot.

### 5. Independent Verification

For each eval, spawn `skill_verifier` and pass:

- contract;
- eval metadata;
- executor logs;
- outputs/artifacts;
- baseline output, if any.

The verifier only judges and does not modify files.

### 6. Evidence Gate

Overall pass conditions:

- all MUST items pass;
- no high-severity regression;
- should-trigger and should-not-trigger behavior has no critical error;
- artifacts, logs, and verdicts are sufficient for reproduction;
- verifier overall is pass.

If verification fails:

- collect the verifier's `next_patch_brief`;
- give it to `skill_developer` for repair;
- enter the next iteration;
- rerun the relevant evals from the beginning. If the change affects triggers, input, output, or core workflow, rerun all evals.

### 7. Delivery

On delivery, output:

- skill path;
- contract path;
- eval coverage;
- iteration count;
- final verifier verdict;
- main evidence paths;
- known limitations;
- how the user can invoke the skill;
- how to add new evals or continue iteration later.

## Stop Conditions

Stop and deliver:

- All MUST items pass and the verifier passes.

Stop and report blocked:

- the contract conflicts;
- required user resources are missing;
- the environment cannot run a key test;
- safety or permission requirements cannot be met.

Stop and report not converged:

- the same MUST still fails after multiple repair rounds;
- the verifier judges that changes are becoming overfit;
- new changes keep introducing high-severity regressions.

## Run Protocol

For concrete directories, metadata, and verdict schemas, see:

`references/run-protocol.md`
