# Behavioral evaluation

Ten synthetic cases exercise all four modes. tasks.json contains user requests;
gold.json contains the maintainer's reasoning and observable acceptance criteria.
Do not give gold labels or this answer-oriented material to the evaluated model.

| Case | Property |
| --- | --- |
| C01 | Deep-review a critical compactness inference with concrete evidence |
| C02 | Correct subcritical compactness control: avoid a false positive |
| C03 | Distinguish fixed-parameter and uniform constants |
| C04 | Actually rewrite a valid heat proof while protecting its statement |
| C05 | Detect an unjustified integration by parts step |
| C06 | Correct boundary-condition control |
| C07 | Edit only the requested section in a multi-file project |
| C08 | Preserve already clear prose: zero-edit control |
| C09 | Correct English without silently changing mathematical meaning |
| C10 | Separate an elementary fact from an unavailable cited source |

All fixtures were created for this project. They include deliberate false
statements and fictional reference metadata; do not cite them as research.

## Prepare a paired comparison

From the repository root:

~~~sh
python3 tools/evaluate.py prepare --arm skill --out /tmp/mpe-skill-run
python3 tools/evaluate.py prepare --arm baseline --out /tmp/mpe-baseline-run
~~~

Both destinations must be fresh. Each case gets raw paper sources, task.md and
input hashes. The skill arm also gets the exact runtime package. Neither gets
gold labels. Preparation does not call a model. Use --case C07 to select a case.
Do not run evaluations in the installed package or on a real manuscript.

Give each arm the same model/settings, tools and user task. Prefer a fresh
context per case; record whether cases actually share context and their order.
Execute each task and save report.md. For a baseline use general capabilities
without loading the skill. Do not reveal the expected answer or proposed repair.

~~~sh
python3 tools/evaluate.py inspect /tmp/mpe-skill-run
~~~

Inspection reports observed source drift and audit status. It does not judge
mathematical truth. A maintainer must read the actual reasoning, source changes,
protected statements, and snapshots against gold criteria. Score mathematical
findings, false positives, allowed edits, scope, citation honesty, actual
delivery and traceability separately. Do not use exact generated wording as the
mathematical rubric.

## Report honestly

Record release/package hashes, model/settings actually available, prompts,
source hashes, outputs, source changes, build status, assessor and failures.
Keep every trial, including an initial failure and a later repair. Do not call
a second context independent expert review or extrapolate from a small suite.

Tool tests in CI check deterministic invariants. Model tests are separate and
are not automatically rerun by CI. The [initial record](results/v0.1.0.md) includes
both arms' reports and observed sources. Its archived audit root is redacted;
those reference copies are not resumable live records.
