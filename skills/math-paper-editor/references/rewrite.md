# Authorized proof and exposition restructuring

The default reader knows the field but has not worked on this project. Follow
the user's requested audience and language. Clarity means the reader can
reconstruct the argument, not that the text has the fewest symbols or pages.

Map the exact main statement, load-bearing estimates, external inputs, and
parameter choices before choosing the exposition. Separate established
identities, assumptions, conditional steps, and inherited unverified inputs.
Look for redundant decompositions or aliases, but keep constructions with a
real mathematical role. Renaming is not a simplification of the proof.

Explain a construction's purpose before introducing its machinery. In the
introduction, state the problem, verified relation to nearby work, difficulty,
and proof mechanism. Define objects when needed instead of front-loading all
auxiliary operators. Retain enough of a technical lemma in the main text for a
reader to identify its hypotheses and how it is used.

Maintain a compact old/new notation map internally. Check objects, signs,
normalizations, parameter dependence, and downstream uses. Same-looking symbols
in a reference can denote different objects. Distinctions such as exact versus
approximate or fixed versus varying must survive. Delete an auxiliary alias
only when expansion improves understanding and preserves its mathematical role.

For each key estimate, give the load-bearing computation at least once:
pairing, integration by parts, boundary term, exponent matching, and absorption
as applicable. “Standard” cannot replace a step the intended reader cannot
recover. Choose constants in their actual dependency order. Reordering must not
move a conclusion's regularity or convergence into its own premises.

Only add details that follow from stated assumptions or a verified equivalent
argument. A new hypothesis, new theorem, or unresolved load-bearing lemma needs
the relevant authorization; report the gap and continue independent work.
Keep an unclosed manuscript explicitly a working draft.

For related PDE mechanisms, consult analysis-pde.md. Do not require a particular
energy, modulation, flux, or bootstrap architecture in every manuscript.
Motivation and concise exposition may be inspired by good mathematical writing;
do not imitate named authors or promise their style as a quality guarantee.

Follow editing.md for snapshots, guarded writes, and isolated builds. Reread
the resulting main argument and the full diff. Check definition order, all
notation changes, preserved theorem scope, and inputs not reverified. Deliver
the actual revision; inspect every page if delivering a PDF. No fixed amount
of shortening or number of renamed symbols is an acceptance criterion.
