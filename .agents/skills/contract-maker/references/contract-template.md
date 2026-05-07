# Skill Contract: <skill-name>

## 0. Contract Status

Status: draft / confirmed  
Version: v0.1  
Last updated: <date>  
User confirmation method: <conversation / file / explicit approval>

## 1. Skill Goal

This skill should let Codex reliably complete:

<Describe the goal in one to three sentences.>

## 2. User-Provided Content

The user can provide:

- <files, text, examples, target resources, preferences, accounts, APIs, environment, etc.>
- <If none, write "no required user resources">

## 3. Input Definition

Input type:

- <text / file / directory / URL / data table / codebase / other>

Input format:

- <format, fields, paths, naming rules>

Edge cases:

- <empty input, missing fields, multiple files, malformed format, ambiguous input, etc.>

## 4. Output Definition

Must output:

- <file, text, report, code, artifact, structured JSON, etc.>

Output format:

- <format, fields, naming, save location>

Quality standards:

- <accuracy, completeness, consistency, style, performance, readability, etc.>

## 5. Trigger Conditions

should-trigger:

- <Use this skill when the user says this.>
- <Include cases where the skill is semantically needed even if the user does not explicitly mention the skill name.>

## 6. Non-Trigger Conditions

should-not-trigger:

- <Adjacent tasks that should not trigger this skill.>
- <Cases that contain keywords but do not actually need this skill.>

## 7. Acceptance Criteria

### MUST

- <Must be satisfied, otherwise the skill cannot be delivered.>
- <Must be verifiable by evidence.>

### SHOULD

- <Strongly recommended, but minor deviations may be explained in the final note.>

### COULD

- <Optional enhancement.>

## 8. Implementation Requirements And Constraints

Must follow:

- <Required tools, workflows, formats, technologies, or resource organization.>

Forbidden:

- <Forbidden tools, external access, dangerous operations, unacceptable strategies.>

Degrees of freedom:

- High freedom: <parts the agent may decide independently>
- Medium freedom: <parts with preferences but acceptable alternatives>
- Low freedom: <fragile steps that must be followed strictly>

## 9. Eval Design

End-to-end eval:

- id: e2e-001
  prompt: <what a real user would say>
  expected_output: <expected result>
  input_files: <if any>

should-trigger eval:

- <query>
- <query>

should-not-trigger eval:

- <near-miss query>
- <near-miss query>

Historical failure examples:

- <if any>

## 10. Evidence Requirements

Passing must provide:

- execution logs or trace summary;
- output artifact paths;
- automated check or human rubric results;
- verifier verdict;
- if comparing a baseline, a summary of the difference between with-skill and baseline.

## 11. Safety, Privacy, And Permissions

Sensitive data:

- <yes / no / unknown>

External access:

- <allowed / forbidden / requires user confirmation>

High-risk operations:

- <delete, overwrite, publish, network access, paid API calls, etc.>

## 12. Definition Of Done

Deliverable if and only if:

- all MUST items pass;
- there is no high-severity regression;
- artifacts are reproducible;
- verifier gives pass;
- known limitations are written into the delivery note.

## 13. Default Assumptions

- <non-blocking assumption>
- <if the assumption is wrong, the user can revise the contract later>

## 14. Complex / Subjective Quality Contract

If the skill's goal is difficult to fully quantify, add the following:

### 14.1 Quality Dimensions

Break the abstract quality goal into 3-8 assessable dimensions.

### 14.2 Hard Gates

List objective thresholds that must never be violated.

### 14.3 Rubric

Define 0-4 or pass/partial/fail standards for each quality dimension.

### 14.4 Evidence Standard

Define what evidence can support the output and what cannot count as evidence.

### 14.5 Uncertainty Policy

Define what must be output when evidence is insufficient, sources conflict, or materials cannot be accessed.

### 14.6 Seeded Evaluation Strategy

Define how to construct fixtures with known errors or known targets.

### 14.7 Pairwise Baseline Comparison

Define when to use baseline comparison and which dimensions to compare.

### 14.8 Human Review Escape Hatch

Define which cases must be marked for human review rather than forced into automatic pass.
