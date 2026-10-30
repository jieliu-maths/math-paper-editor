# Integration by parts review

Read `paper/main.tex` in full. All sources are unchanged. Compilation was not run, as instructed. The following is direct reasoning, not formal verification or independent expert certification.

The lemma `lem:parts` is false for the stated class of all real C²([0,1]) functions. Integration by parts gives

    ∫₀¹ u u″ dx = u(1)u′(1) − u(0)u′(0) − ∫₀¹ |u′|² dx.

The proof omits the endpoint term, and the hypotheses impose no condition making it vanish. For the explicit admissible function u(x)=x, the asserted left side is zero and the asserted right side is −1. The missing boundary term is 1, which restores equality.

A correct unconditional identity retains the boundary term. To preserve the claimed boundary-free identity instead, one must add assumptions that imply u(1)u′(1)=u(0)u′(0), for example homogeneous Dirichlet values at both endpoints, homogeneous Neumann values, or matching periodic values and derivatives. No such assumption is present. These are possible author decisions, not edits applied here.

The target was a universal boundary-free integration by parts identity. The counterexample disproves it as stated; any energy argument that uses it must account for the boundary flux or add appropriate boundary conditions. The remaining question is which boundary conditions the intended application supplies.
