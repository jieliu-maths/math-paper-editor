# Integration by parts review

Read `paper/main.tex` in full; all sources remain unchanged. Compilation was not run, as instructed. This review is based on the explicit calculation below and is not formal or independent expert verification.

No mathematical issue was found in the stated lemma. For a real C²([0,1]) function, integration by parts is justified and yields

    ∫₀¹ u u″ dx = [u u′]₀¹ − ∫₀¹ (u′)² dx.

The given assumptions u(0)=u(1)=0 eliminate both endpoint contributions. Since u is real, (u′)²=|u′|², giving exactly the displayed conclusion. No condition on the boundary derivatives is necessary. Smoothness is stronger than needed but fully sufficient.

The one-sentence proof is adequate for this elementary statement; writing the boundary term explicitly would make the role of the endpoint assumptions clearer, but is an optional exposition improvement rather than a missing mathematical hypothesis.

The target identity follows under the exact hypotheses provided. No mathematical gap remains in this scope, and no follow-up mathematical repair is required.
