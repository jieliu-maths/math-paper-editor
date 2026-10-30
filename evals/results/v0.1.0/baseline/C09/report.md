# Conservative editing delivery

Edited `paper/main.tex` only to replace “This prove the assertion.” with “This proves the assertion.” All mathematical statements and the mathematical argument are unchanged, including the word “strongly” in both the lemma and its proof. Labels and preamble are preserved. Compilation was not run, as instructed.

## Separate mathematical concern

The lemma `lem:hilbert` is false in the stated infinite-dimensional space. Let e_n denote the sequence in ℓ²(ℕ) whose nth coordinate is 1 and all other coordinates are zero. Then ‖e_n‖₂=1 for every n, so the sequence is bounded. For distinct m and n,

    ‖e_n − e_m‖₂ = √2.

No subsequence is Cauchy in norm, so no subsequence can converge strongly. This is a direct counterexample to the lemma.

Weak sequential compactness of bounded subsets in this Hilbert space gives weakly convergent subsequences, not strongly convergent ones. In this example e_n converges weakly to zero, since for every fixed vector y in ℓ² its nth coordinate tends to zero, while its norm remains 1. Thus the proof's use of “strongly” is consequential, not an English correction.

A potential author-approved repair is to replace the conclusion with weak subsequential convergence, or to add a genuine norm-compactness assumption. Neither repair was applied because the task expressly requires the mathematical statements and argument to remain unchanged.

The mathematical target of strong subsequential convergence remains disproved as written. The exact obstruction is failure of norm compactness of the bounded unit vectors. The next mathematical question is whether the application needs weak convergence only or has extra compactness structure. The counterexample and editorial check are reasoned evidence, not formal verification or independent expert certification.
