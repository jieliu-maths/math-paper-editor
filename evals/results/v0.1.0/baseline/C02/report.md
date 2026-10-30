# Mathematical review

Read all of `paper/main.tex` within its stated scope. All paper sources remain unchanged. Compilation was not run, as instructed. This review supplies reasoning rather than formal correctness certification or independent expert verification.

No consequential mathematical error was found.

The proposition fixes 1 ≤ q < 2N/(N−2) on the unit ball in dimension N ≥ 3. This is the subcritical range of the compact embedding of H_0^1(Ω) into L^q(Ω). A weakly convergent H_0^1 sequence is bounded. Compactness gives an L^q-convergent subsubsequence from every subsequence, and continuity of the embedding identifies each such limit with u (weak convergence can equivalently be tested in distributions). If the full sequence did not converge strongly to u, there would be a subsequence at a fixed positive L^q distance from u, contradicting that subsubsequence conclusion. Thus the full-sequence statement is valid, including q=1. The proof is terse but the inference is standard and justified. It could include this subsequence argument for clarity; no extra mathematical assumption is needed.

For the square estimate, the pointwise factorization and Cauchy–Schwarz give the displayed bound. Strong L² convergence implies boundedness of ‖v_n‖₂, so the product tends to zero. This argument is valid as stated.

Editorial notes only: “We studies” → “We study” and “This prove” → “This proves.” The introductory exponent sentence can also be smoothed. The label `prop:critical` does not match the subcritical content, but labels do not affect the claim and need not be changed.

The theorem target is subcritical strong convergence from weak H_0^1 convergence. The result is supported by compactness on the stated domain; no unresolved mathematical gap was identified in this scope. If the authors later extend the claim to the endpoint exponent, that would require a separate argument addressing concentration.
