# Review of parameter dependence

Read the entire synthetic `paper/main.tex`. Paper source unchanged. Compilation was not run, as instructed. This is a reasoning-based review, not formal or independent expert verification.

The lemma `lem:uniform` is false: its proof establishes a constant for each fixed parameter, not one finite constant uniform over 0 < ε ≤ 1.

Indeed, for any two distinct points of [0,1],

    |f_ε(x) − f_ε(y)| / |x − y| = 1/ε.

In particular x=1 and y=0 force C ≥ 1/ε for every admissible ε. Taking ε=1/n would require C ≥ n for every positive integer n, impossible for finite C. The constant supplied by the mean value theorem is optimal and diverges as ε tends to zero. The last sentence of the proof therefore reverses the essential quantifiers without justification.

Two possible repairs, neither applied here: state that for each fixed ε the function is Lipschitz with optimal constant C_ε=1/ε; or restrict the parameter to ε₀ ≤ ε ≤ 1 for a specified ε₀>0, allowing the uniform constant C=1/ε₀. The original full parameter range cannot support its claimed uniform conclusion.

The target was a uniform Lipschitz bound. The exact result is failure of that bound through the explicit difference quotient above. Consequently this lemma cannot support a uniform regularity argument or a limit passage requiring equicontinuity with this modulus. The next mathematical question is whether the intended application permits a lower cutoff on ε or a parameter-dependent bound.
