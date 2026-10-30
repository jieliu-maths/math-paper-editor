# Review

[M1] Confirmed error, major — `lem:parts`, lines 6–12. Integration by parts for the stated class gives ∫₀¹u u″=[u u′]₀¹−∫₀¹|u′|². The manuscript drops the boundary term without a boundary condition. For the admissible function u(x)=x, the asserted left side is 0 and the asserted right side is −1; the omitted boundary term equals 1. Thus the lemma as stated is false, not merely underexplained.

The minimal mathematical repair question is which boundary behavior is intended. Homogeneous Dirichlet values, homogeneous Neumann derivatives, or the direct requirement [u u′]₀¹=0 suffice, but none is presently assumed. Alternatively include the boundary term in the identity for arbitrary C² functions. Each option changes the statement; no source was edited.

Coverage: read all of the standalone `paper/main.tex` and reconstructed the entire integration by parts argument and a concrete counterexample. The C² regularity and real-valued assumption suffice for the full identity. There are no included sources or external references to verify.

All sources remain unchanged. Compilation was not run, as instructed. No network or external verification was performed. This scoped review does not claim formal correctness or independent expert verification.

Source SHA-256: da18910bc7dcfbf01adb1bbfe539cf5c7c502c7f6ef95f8909c74764e94448ea
