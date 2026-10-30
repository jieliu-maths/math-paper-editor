# Review depth and continuation

For a short passage, a concise response is sufficient. For a long manuscript,
keep a small coverage record in the agreed review-output directory, or in the
conversation if saving a report was not requested. Read-only modes may write an
independent report when requested; they may not insert manuscript comments.

Track only what helps resume the mathematical check:

| Item | Location | Read | Checked | Inputs | Finding / remaining question |
| --- | --- | --- | --- | --- | --- |
| Main result | theorem label | yes/no | reconstructed / partial / not checked | lemma labels, source versions | precise gap or scoped conclusion |

Reading is not verification. A dependency copied from an earlier report is an
inherited input until rechecked. Record the source version or file fingerprint
used for a saved report so later changes do not silently inherit its conclusions.
Do not turn the record into a second authoritative research-state ledger.

Prioritize the main theorem, load-bearing lemmas, and the assumptions they need.
Record open dependencies rather than repeatedly claiming whole-paper coverage.
For each consequential external theorem, identify the exact source/version and
the matching hypotheses. If the source is unavailable, mark it unverified;
absence of access is not evidence that the citation is false.

`deep-review` reconstructs crucial estimates and examines relevant endpoints,
scaling tests, counterexamples, and selection of constants or subsequences.
Do not treat a list of things to check as a completed check. A correct argument
is an important control: do not manufacture defects to fill a report.

Useful finding format:

> [M1] Missing argument / major — theorem or equation label — exact inference
> not yet justified — proof consequence — smallest useful repair question.

Use the final source's line numbers together with stable labels when edits move
lines. Keep minor language feedback subordinate to consequential mathematics.
