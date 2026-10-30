# Deep review

Scope: read the complete synthetic `paper/main.tex`; checked the compactness inference and the final estimate. No source was changed. Compilation was not run, as instructed. This is a reasoned review, not formal verification or independent expert certification.

## Consequential finding: the critical compactness proposition is false

In Proposition `prop:critical`, the claimed compactness of the embedding at the exponent `2^*=2N/(N-2)` is false. Boundedness of the domain does not remove concentration at this endpoint.

Concrete counterexample: choose a nonzero smooth function φ supported in the ball of radius 1/2, and define, for positive integers n,

    u_n(x) = n^((N-2)/2) φ(nx),   x ∈ Ω.

Every u_n belongs to H_0^1(Ω). Change of variables gives

    ‖∇u_n‖_2 = ‖∇φ‖_2,
    ‖u_n‖_2 = n^(-1) ‖φ‖_2,
    ‖u_n‖_(2^*) = ‖φ‖_(2^*) > 0.

Thus the sequence is bounded in H_0^1 and tends strongly to zero in L². Every weakly convergent H_0^1 subsequence consequently has weak limit zero; boundedness and weak sequential compactness then imply that the full sequence converges weakly to zero. Its critical Lebesgue norm stays positive, so it cannot converge strongly to zero in L^(2^*). This directly contradicts the proposition.

Proof consequence: both the proposition and its proof fail as written. A possible corrected statement is strong convergence in L^q(Ω) for 1 ≤ q < 2^*, using the compact subcritical Sobolev embedding and uniqueness of the weak limit. Alternatively the critical conclusion needs additional assumptions excluding concentration; none are supplied. These are proposed repairs, not source edits or accepted theorem changes.

## Other checks

The final L¹ estimate for squares is valid for real-valued functions (and also the displayed algebraic bound for complex squares): factor v_n²−v² and apply Cauchy–Schwarz. L² convergence makes the L² norms bounded, giving the limit claimed.

Minor language issues: “We studies” should be “We study”; “This prove” should be “This proves.” They do not address the mathematical failure.

The exact obstruction is endpoint concentration. The remaining gap is an assumption or a revised exponent that makes the desired compactness statement true. The next mathematical question is whether the intended application requires the critical exponent or only a subcritical one.
