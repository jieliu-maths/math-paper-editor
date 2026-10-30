# Traceable editing

First inspect Git status and relevant existing diffs, when Git is used. Keep
the existing index and other people's changes. Never automatically commit,
stash, reset, or restore a manuscript. For each source you may edit, capture
its current bytes, including existing uncommitted changes.

Choose a fresh output directory under the project's existing review-artifact
convention, otherwise `.math-paper-editor/<unique-run>/`. These local records
contain manuscript copies and absolute runtime paths; do not publish them.
Replace `SKILL` below with this installed skill directory, `PAPER` with the
paper root, and `RUN` with the unique output directory.

```sh
python3 SKILL/scripts/changes.py begin --root PAPER --out RUN -- main.tex sections/introduction.tex
```

The helper accepts existing UTF-8 text sources. It preserves bytes, including
line endings, but does not parse LaTeX or establish equivalence. If snapshots
cannot be saved, continue read-only work and explain why writing is blocked.
Adding a source file or expanding scope requires authorization and a snapshot
before editing it; begin another record for additional existing files.

Prepare a full replacement in `RUN/candidates/` or another explicit staging
location, never by first overwriting the manuscript. Make a small coherent edit
and apply it through the helper:

```sh
python3 SKILL/scripts/changes.py apply RUN --file main.tex --replacement RUN/candidates/main.tex
python3 SKILL/scripts/changes.py check RUN
```

`apply` checks the current source against the last recorded version and refuses
observed drift. On conflict, reread the file, preserve the concurrent edit,
and start a new snapshot/candidate from the merged version. Do not overwrite it
or change the recorded hash to force acceptance. It is an optimistic check,
not an exclusive lock: another process can still write during filesystem
operations. Coordinate concurrent editing when possible.

Before/after builds use the project's known entry and isolated output paths.
Preserve the original PDF. Do not install TeX, enable shell escape, or execute
unknown build scripts without authorization. Clearly separate old failures,
new failures, and checks not run. At most three focused repair attempts are
normally enough before reporting a build obstruction. Keep mathematical
findings separate from build results.

Self-review the complete diff. Preserve `edit` mode's mathematical meaning and
scope. For `rewrite`, check notation mappings, definitions, dependency order,
constant choices, and theorem scope. Remove your own unsupported equivalent
rewrites while preserving other changes.

```sh
python3 SKILL/scripts/changes.py finish RUN
```

The record contains:

- `before/`: original snapshots;
- `editor/` and `editor.diff`: versions applied through this helper;
- `after/` and `changes.diff`: the source observed at finalization;
- `unattributed.diff`: differences between the recorded editor version and the
  final observed source; these must not be attributed to AI;
- `manifest.json`: hashes, operations, and `complete` or `conflicted` status.

Exit code 2 means observed drift/conflict. The snapshots and differences are
preserved, but the edit is not a cleanly attributed completion. Direct source
editing outside `apply` is preserved as unattributed change, not silently
claimed as an editor operation. Finalization seals the record; repeating it
with unchanged sources is idempotent, and later source changes require a new
record. The helper never automatically restores a manuscript.

Source additions/deletions are outside this helper's v0.1 scope: list and
preserve them separately if the user authorizes them. Never report an incomplete
record as a complete audit trail. Deliver accessible paths and explain any
conflict. Restore only on user request after checking for later changes.
