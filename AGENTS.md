# Skill Factory Working Agreement

This repository turns a user's top-level skill goal into a reproducible, testable, deliverable Codex skill.

## Core Principles

Always treat the confirmed contract as the single source of truth. Explanations, guesses, temporary debug conclusions, and local fix rationales from development cannot replace the contract.

When creating or updating a skill, prefer Codex's built-in `$skill-creator`. Do not reimplement skill-creator's scaffolding, naming, frontmatter, resource directories, or baseline validation logic; only add orchestration around contracts, test loops, role isolation, and evidence gates.

Do not write the development process, test records, failure logs, or temporary assumptions into the target skill's `SKILL.md`. The target skill should contain only the core procedural knowledge, necessary references, scripts, and resources another Codex instance needs to complete the task.

Every candidate skill must be accepted based on end-to-end testing from the user entry point. After changing a skill, do not rerun only the failed fragment; rerun the relevant eval from clean initial conditions, and rerun all evals when necessary.

## User Participation Boundary

The user only needs to provide the goal, inputs, outputs, acceptance criteria, constraints, preferences, examples, and necessary resources.

After the contract is confirmed, do not ask the user to participate in implementation-detail decisions unless a required external resource is missing, there is a safety or permission issue, or the contract contradicts itself.

## Role Isolation

Development, execution, and verification must be separated:

- `skill_developer`: only creates, modifies, and fixes the target skill; it must not decide that its own work passes.
- `skill_executor`: only executes eval prompts from clean initial conditions; it must not read the developer's fix rationale or modify the target skill.
- `skill_verifier`: verifies only from the contract, eval metadata, trace, logs, artifacts, and outputs; it must not inherit implementer assumptions or modify the target skill.

## Evidence Gate

Do not use "I think it is done" or "it looks fine" as delivery evidence. Passing requires at least:

- a verdict for every MUST acceptance item in the contract;
- each eval's input, execution method, and output location;
- relevant commands, scripts, or check results;
- the verifier's pass/fail/blocked verdict;
- for any failure, a reproducible failure summary and the next repair brief.

## Artifact Conventions

Place the target skill in `.agents/skills/<target-skill-name>/`.

Place the contract in `contracts/<target-skill-name>.contract.md`.

Place evals and run results in `skill-factory-workspace/<target-skill-name>/`, layered by iteration.

The final delivery report must include:

- skill path;
- contract path;
- eval coverage;
- final verdict;
- known limitations;
- how the user can install, invoke, and continue iterating on the skill.
