# Deep review

Coverage: read all of `paper/main.tex`; reconstructed Proposition `prop:critical` and the final quadratic estimate. No external references or included sources are used. The main proposed mechanism is compactness of a Sobolev embedding.

[M1] Confirmed error, major — `prop:critical`, lines 14–21. The embedding at the critical exponent is continuous but not compact, and the proposition is false. Here is a counterexample satisfying its exact domain and boundary conditions. Fix a nonzero smooth function φ with compact support in the unit ball. For integers n≥1 define u_n(x)=n^((N−2)/2)φ(nx). Each u_n belongs to H_0^1(Ω). Change of variables gives

- ∥∇u_n∥₂²=∥∇φ∥₂²;
- ∥u_n∥₂²=n⁻²∥φ∥₂²→0;
- ∥u_n∥_(2*)^(2*)=∥φ∥_(2*)^(2*)>0.

Thus u_n is bounded in H_0^1 and converges weakly there to zero: every weakly convergent subsequence has zero limit by its strong L² convergence, and boundedness plus weak subsequence compactness then establishes the full weak limit. Equivalently, the weak gradient limit is identified distributionally. Its critical norm stays positive, so it does not converge strongly in L^(2*). Concentration at the origin is the obstruction. Merely repairing the proof's wording cannot repair the theorem. A possible substantive revision is to assert strong convergence in L^q for 1≤q<2*, using subcritical compactness, or add a justified no-concentration hypothesis. Either changes the mathematical statement and requires author choice; neither was applied.

The final estimate, lines 24–30, checks out under its stated strong L² assumption: factor the difference of squares, apply Cauchy–Schwarz and the triangle inequality, and use boundedness of a norm-convergent sequence. This does not rescue the preceding critical assertion.

Minor prose: “We studies”→“We study”; “This prove”→“This proves.” Sources remain entirely unchanged, including these phrases, as required by deep-review mode.

Compilation was not run, as instructed. No network or external-reference verification was performed. This is a scoped editorial mathematical check, not formal certification or independent expert verification.

Source SHA-256: e969999bec7c6be8696aede0260ed4a6c918df1eb81128baa753e0ff5c73d42f
