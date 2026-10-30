# Math Paper Editor

**Review the argument. Preserve the author's meaning. Trace the revision.**

A Codex skill for LaTeX mathematical manuscripts, starting with analysis and PDE.
Version **0.1.0**.

[简体中文](README.zh-CN.md) · [Evaluation](evals/README.md) ·
[Changes](CHANGELOG.md) · [Contributing](CONTRIBUTING.md) · [MIT](LICENSE)

| Mode | Changes manuscript? | Focus |
| --- | --- | --- |
| review | No | Main argument, consequential gaps, and exposition |
| edit | Within scope | Necessary language corrections; zero changes is valid |
| deep-review | No | Reconstruct key estimates, assumptions, endpoints, and counterexamples |
| rewrite | Within scope | Reorganize existing proofs, simplify auxiliary notation, and explain verifiable steps |

The skill distinguishes errors, missing arguments, unverified citations, and
ambiguities. An ordinary edit cannot silently change a hypothesis, exponent,
convergence mode, or conclusion. Rewriting permits equivalent arguments and
authorized notation changes, not a new theorem or an unproved repair.
It preserves author style, macros, labels, citation keys, and project conventions.

## Install or update

Requirements: **Python 3.10+** for tools, and a Codex environment with skills enabled.
Tools use only Python's standard library. macOS and Linux are CI targets;
Windows and other host adapters are not separately validated. No model, API key,
TeX distribution, proof assistant, or unpublished paper is bundled.

~~~sh
git clone https://github.com/jieliu-maths/math-paper-editor.git
cd math-paper-editor
git checkout v0.1.0
python3 tools/check.py
python3 tools/install.py
python3 tools/install.py --apply
~~~

The first installation command previews; --apply writes. The default destination
is ~/.agents/skills/math-paper-editor; --dest selects an explicit alternative.
Keep one discoverable installation. The skill is available on the next turn;
open a new session if discovery has not refreshed.

Upgrades stop on modified/deleted managed files or collisions, preserve unmanaged
extras, and retain a full old-installation backup outside the discovery directory.
An existing unmanaged copy needs an exact private baseline. See
[installation and maintenance](docs/installation.md).

## Use in a paper project

Type in the Codex conversation, not a terminal:

~~~text
$math-paper-editor review main.tex
$math-paper-editor edit introduction
$math-paper-editor deep-review main.tex
$math-paper-editor rewrite main.tex
~~~

For example: “Rewrite the proof of Lemma 2 for a graduate reader. Preserve its
hypotheses, conclusion, macros, labels, and bibliography. Explain the key estimate,
simplify redundant auxiliary notation, and deliver revised sources, snapshots,
diffs, and the actual build status.”

The manuscript project's instructions and approval boundaries apply. A request
to edit one section permits reading dependencies, not editing other sections.
Reports follow the user's language; manuscript language is preserved by default.

## Traceable revisions

The helper snapshots the actual initial bytes, including existing uncommitted
work. Each replacement checks the last recorded version and refuses observed drift.

| Record | Meaning |
| --- | --- |
| before/ | Original snapshots |
| editor/ and editor.diff | Changes applied through the helper |
| after/ and changes.diff | Final observed source and total difference |
| unattributed.diff | Changes not accounted for by recorded editor operations |
| manifest.json | Hashes, operations, and completion/conflict status |

Records contain manuscript copies and absolute runtime paths: keep them private.
Snapshot and installation tools do not contact a network. AI-host data handling
still depends on that host's settings and policies.

The helper is an optimistic drift check, not an exclusive lock, authorship
certificate, LaTeX semantic checker, or proof checker. Source additions/deletions
need separate accounting in v0.1. See the [editing procedure](skills/math-paper-editor/references/editing.md).

## Test and evaluate

~~~sh
python3 tools/check.py
python3 -m unittest discover -s tests -v
python3 skills/math-paper-editor/scripts/changes.py self-test
~~~

CI runs deterministic tool tests and release checks. A separate suite contains
**10 synthetic behavior cases**, including valid-proof controls, consequential
errors, scoped editing, a no-op, proof rewriting, and unavailable citation evidence.
Preparing cases does not call a model or read a real manuscript.

See [evaluation instructions](evals/README.md) and the
[v0.1.0 record](evals/results/v0.1.0.md). Tool tests and model observations are
reported separately. The small suite does not establish general mathematical
reliability, comparative superiority, or improved research productivity.

## Maintain and integrate

Use an observed failure to create an anonymized minimal case, add an observable
criterion, make a narrow change, compare versions, and publish a tagged release.
This repository is the maintained source; installed directories are versioned
copies. Preserve correct-proof controls and keep paper-specific mechanisms in
conditional references.

The skill works alone or alongside
[AI Research Workflow](https://github.com/jieliu-maths/AI-Research-Workflow).
That project manages evidence and approved research state; this skill edits a
selected manuscript. A manuscript edit cannot approve a claim or its evidence.

MIT licensed, copyright 2026 Jie Liu. The license covers bundled project code,
documents, and synthetic fixtures; it does not license or transfer ownership of
a user's manuscript. External sources and services retain their own terms.
