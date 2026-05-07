---
name: contract-maker
description: "Create a verifiable skill contract from a user's high-level goal. Use when defining a new or updated Codex skill: inputs, outputs, trigger rules, non-trigger cases, acceptance criteria, evals, evidence, constraints, and delivery requirements."
---

# Contract Maker

Your task is to turn the user's top-level intent into a stable skill contract. The contract is the single source of truth for later skill development, execution, verification, and delivery.

## Working Goal

Let the user only explain "what I can provide, what I want, and what the acceptance criteria are" without participating in later implementation details. You are responsible for turning a fuzzy goal into a clear, testable, generalizable contract.

## Information-Gathering Principles

Prefer extracting the contract from information the user has already provided. Do not ask again for information that is already clear.

Ask questions only for blocking gaps. Blocking gaps include unclear input source, unclear output format, conflicting acceptance criteria, required dependence on missing private user resources, or safety/permission risks.

If a gap does not block development, write it into "Default Assumptions" and continue. Do not drag the user into implementation discussion just to make a perfect contract.

## The Contract Must Cover

1. Skill goal: what task the skill should reliably complete.
2. User-provided content: files, text, examples, preferences, environment, accounts, or external tools.
3. Input definition: input type, format, path, and edge cases.
4. Output definition: output files, format, naming, quality standards, and acceptable variants.
5. Trigger conditions: how the user should express a request for this skill to be used.
6. Non-trigger conditions: which adjacent tasks should not use this skill.
7. Acceptance criteria: layered as MUST / SHOULD / COULD.
8. Implementation requirements: required or forbidden technologies, tools, workflows, and resource organization.
9. Testing strategy: end-to-end evals, should-trigger, should-not-trigger, and historical failure examples.
10. Evidence requirements: what artifacts, logs, and checks can prove pass.
11. Safety and permissions: external access, privacy, sensitive data, and forbidden operations.
12. Definition of done: when the skill can be delivered and when iteration must continue.

## Output Requirements

When generating a contract, use the structure in `references/contract-template.md`.

The contract should be an engineering file another Codex instance can execute directly, not a conversation summary.

Do not include verbose explanations, development process, model guesses, or descriptions of user emotions in the contract. Keep only information that constrains later development and verification.

## Recommended Artifact Path

Save the final contract as:

`contracts/<skill-name>.contract.md`

If the user has not confirmed the contract yet, output a "contract draft" first. After user confirmation, mark it as a "confirmed contract."

## Completion Standard

When the contract is sufficient for skill-factory-loop to take over development, testing, repair, and delivery, explicitly write:

"The contract is ready to hand off to skill-factory-loop."
