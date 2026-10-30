# Contributing

Motivate a narrow change with an observed failure. Include a synthetic or
appropriately licensed minimal example, requested mode/scope, observable
acceptance criterion, and actual result. Never post unpublished manuscripts,
audit snapshots, private source paths, tokens, or confidential reviews.
Anonymize before filing an issue.

For tool changes, add a regression and run:

~~~sh
python3 tools/check.py
python3 -m unittest discover -s tests -v
python3 skills/math-paper-editor/scripts/changes.py self-test
~~~

For behavior changes, compare relevant cases on old/new versions using the same
model/settings and task. Keep valid-proof controls. Record available model
metadata, source fingerprints, tasks, outputs, changes, build status, assessor,
failures and limits. Do not replace a failed trial silently or grade a preferred
sentence. See evals/README.md.

Keep common boundaries in SKILL.md and conditional details in references.
Preserve standalone use and default skill discovery. Self-review or another
session with the same model is not independent expert verification.
Contribute only materials you have the right to release under MIT.

Release: update VERSION/CHANGELOG; run checks/tests; publish an honest evaluation
record; verify GitHub CI; create tag/release; install that revision.
Keep local installation state and backups out of Git.
