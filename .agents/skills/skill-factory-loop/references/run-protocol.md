# Skill Factory Run Protocol

## 1. Workspace Structure

Each target skill uses its own workspace:

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

Do not write workspace contents into the target skill unless the contract explicitly requires a resource to be promoted into references, scripts, or assets.

## 2. Minimal evals.json Structure

{
  "skill_name": "<target-skill-name>",
  "contract_path": "contracts/<target-skill-name>.contract.md",
  "evals": [
    {
      "id": "eval-001",
      "type": "end_to_end | should_trigger | should_not_trigger | regression",
      "prompt": "task a real user would ask",
      "expected_output": "expected result description",
      "input_files": [],
      "must_check": [
        "required check item"
      ],
      "should_check": [
        "recommended check item"
      ]
    }
  ]
}

## 3. Minimal eval_metadata.json Structure

{
  "eval_id": "eval-001",
  "eval_name": "short name describing what this eval tests",
  "contract_version": "v0.1",
  "prompt": "real user task",
  "input_files": [],
  "assertions": [
    {
      "id": "must-001",
      "level": "MUST",
      "text": "check item description",
      "check_method": "programmatic | artifact | log | model_rubric | human_review"
    }
  ]
}

## 4. Minimal execution_summary.json Structure

{
  "status": "pass_execution | fail_execution | blocked",
  "skill_path": ".agents/skills/<target-skill-name>",
  "prompt": "executed eval prompt",
  "working_directory": "actual execution directory",
  "outputs": [
    "outputs/<artifact>"
  ],
  "commands_or_steps": [
    "key step or command"
  ],
  "errors": [],
  "observations": [],
  "environment_notes": []
}

## 5. Minimal verifier_verdict.json Structure

{
  "overall": "pass | fail | blocked",
  "must_results": [
    {
      "criterion": "MUST clause",
      "status": "pass | fail | blocked",
      "evidence": "evidence path or summary"
    }
  ],
  "should_results": [
    {
      "criterion": "SHOULD clause",
      "status": "pass | fail | blocked",
      "evidence": "evidence path or summary"
    }
  ],
  "trigger_results": [
    {
      "query": "trigger or non-trigger example",
      "expected": "trigger | not_trigger",
      "actual": "trigger | not_trigger | unclear",
      "evidence": "evidence"
    }
  ],
  "regressions_or_risks": [
    {
      "risk": "risk description",
      "severity": "high | medium | low",
      "evidence": "evidence"
    }
  ],
  "next_patch_brief": "minimal repair brief for skill_developer on failure; empty string on pass."
}

## 6. Minimal iteration_summary.json Structure

{
  "iteration": 1,
  "candidate_skill_path": ".agents/skills/<target-skill-name>",
  "contract_path": "contracts/<target-skill-name>.contract.md",
  "eval_count": 0,
  "passed": 0,
  "failed": 0,
  "blocked": 0,
  "overall": "pass | fail | blocked",
  "main_failures": [],
  "next_action": "ship | patch | ask_user | stop_blocked"
}

## 7. Evidence Gate Rules

Overall pass requires:

- all MUST items pass;
- no high-severity regression;
- executor artifacts exist and can be located;
- verifier verdict is traceable to artifacts, logs, or an explicit rubric;
- relevant evals were rerun from the beginning after changes.

Overall fail must produce:

- minimal failure summary;
- reproducible evidence;
- next developer patch brief.

Overall blocked must explain:

- what is missing;
- why the agent cannot fill the gap itself;
- what the user can provide to continue.
