# Skill Factory Run Protocol

## 1. 工作区结构

每个目标 skill 使用独立工作区：

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

不要把该工作区内容写入目标 skill，除非 contract 明确要求把某个资源沉淀为 references、scripts 或 assets。

## 2. evals.json 最小结构

{
  "skill_name": "<target-skill-name>",
  "contract_path": "contracts/<target-skill-name>.contract.md",
  "evals": [
    {
      "id": "eval-001",
      "type": "end_to_end | should_trigger | should_not_trigger | regression",
      "prompt": "真实用户会提出的任务",
      "expected_output": "期望结果描述",
      "input_files": [],
      "must_check": [
        "必须满足的检查项"
      ],
      "should_check": [
        "建议满足的检查项"
      ]
    }
  ]
}

## 3. eval_metadata.json 最小结构

{
  "eval_id": "eval-001",
  "eval_name": "短名称，描述它在测什么",
  "contract_version": "v0.1",
  "prompt": "真实用户任务",
  "input_files": [],
  "assertions": [
    {
      "id": "must-001",
      "level": "MUST",
      "text": "检查项说明",
      "check_method": "programmatic | artifact | log | model_rubric | human_review"
    }
  ]
}

## 4. execution_summary.json 最小结构

{
  "status": "pass_execution | fail_execution | blocked",
  "skill_path": ".agents/skills/<target-skill-name>",
  "prompt": "执行的 eval prompt",
  "working_directory": "实际执行目录",
  "outputs": [
    "outputs/<artifact>"
  ],
  "commands_or_steps": [
    "关键步骤或命令"
  ],
  "errors": [],
  "observations": [],
  "environment_notes": []
}

## 5. verifier_verdict.json 最小结构

{
  "overall": "pass | fail | blocked",
  "must_results": [
    {
      "criterion": "MUST 条款",
      "status": "pass | fail | blocked",
      "evidence": "证据路径或摘要"
    }
  ],
  "should_results": [
    {
      "criterion": "SHOULD 条款",
      "status": "pass | fail | blocked",
      "evidence": "证据路径或摘要"
    }
  ],
  "trigger_results": [
    {
      "query": "触发或非触发样例",
      "expected": "trigger | not_trigger",
      "actual": "trigger | not_trigger | unclear",
      "evidence": "证据"
    }
  ],
  "regressions_or_risks": [
    {
      "risk": "风险描述",
      "severity": "high | medium | low",
      "evidence": "证据"
    }
  ],
  "next_patch_brief": "失败时给 skill_developer 的最小修复 brief；通过时为空字符串。"
}

## 6. iteration_summary.json 最小结构

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

## 7. 证据门规则

整体 pass 必须满足：

- 所有 MUST pass；
- no high severity regression；
- executor 产物存在且可定位；
- verifier verdict 可追溯到 artifacts、logs 或明确 rubric；
- 修改后重新从头执行相关 eval。

整体 fail 必须产生：

- 最小失败摘要；
- 可复现证据；
- 下一轮 developer patch brief。

整体 blocked 必须说明：

- 缺少什么；
- 为什么 agent 无法自行补足；
- 用户提供什么后可以继续。
