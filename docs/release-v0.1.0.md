First public release of **Math Paper Editor**, a Codex skill for scoped LaTeX
mathematical manuscript review and revision, starting with analysis and PDE.

- Four modes: review, edit, deep-review and rewrite.
- Author-controlled mathematical scope, conditional domain guidance, and
  English/Chinese documentation.
- Byte-preserving snapshots, optimistic guarded edits, separate editor/observed/
  unattributed diffs, and sealed audit records.
- Versioned installation with legacy-adoption checks and complete backups.
- MIT license; synthetic fixtures only.

Validation: **38 deterministic tests**, release checks, helper self-test and
official skill-format validation passed. GitHub CI covers macOS/Linux with
Python 3.10/3.12.

The initial model evaluation ran 10 cases in each of two isolated sessions
(skill and unaided baseline). Both met the case criteria; **no mathematical
accuracy improvement was demonstrated**. Four skill writing cases produced
clean audit records. See the [full evaluation record](https://github.com/jieliu-maths/math-paper-editor/blob/v0.1.0/evals/results/v0.1.0.md)
for raw reports, changes and limitations.

Compilation, workflow consistency and fluent prose do not certify proof truth.
The installed skill is available on the next turn; use a new session if discovery
has not refreshed.
