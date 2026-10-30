# Rewrite delivery

Delivered actual revised source: [paper/main.tex](paper/main.tex). No definite error found within the checked scope. Read the full manuscript and checked the energy identity, Poincaré input, integrating factor, and square-root passage. The theorem's hypotheses, rate e^(−μt), all labels, macro definitions, and preamble remain unchanged.

The proof now shows differentiation, substitution of the heat equation, integration by parts with vanishing Dirichlet boundary term, application of the assumed Poincaré inequality, and integration of the differential inequality. Smoothness supplies the differentiations and the boundary condition makes each time slice admissible. Taking square roots avoids division by the norm at its zeroes.

Authorized auxiliary-notation simplification: retain A(t) as the squared L² norm; expand P(t) to the gradient integral; replace M₂(t) by its identical value A(t), K₀ by the already defined μ, and Z(t) by taking square roots at the end. These aliases had no downstream use outside the proof. No theorem or hypothesis was added. The Poincaré inequality remains an explicit assumed input; its optimality is neither needed nor claimed.

Only the proof changed. The complete diff was self-reviewed against the source and the notation mapping above. This was one editor's check, not independent expert verification or formal certification. No bibliography or external novelty claim is present; no network or primary-source lookup was performed. Compilation was not run, as instructed; no PDF was generated or inspected.

Traceability: [audit/before/main.tex](audit/before/main.tex) preserves the input; [audit/changes.diff](audit/changes.diff) is the final diff; [audit/manifest.json](audit/manifest.json) records the guarded application. Check and finish reported no conflicts and complete status. There was no Git repository, so no index or existing Git changes were altered.
