# Maintaining math-paper-editor

This contains a reusable editing skill and synthetic evaluation fixtures, not
a mathematical research project. Maintain skills/math-paper-editor; update
installed copies with the installer after testing.

Run python3 tools/check.py, python3 -m unittest discover -s tests -v, and the
helper's self-test. Use temporary test directories. Preserve mode/scope
boundaries and distinguish tool consistency from mathematical correctness.

Add demonstrated failures as small licensed/synthetic cases. Do not publish
real papers, audit copies, installation state/backups, local absolute paths or
credentials. Keep gold labels out of prepared model workspaces. Record failures
and evaluation limitations.
