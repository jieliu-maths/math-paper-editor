# Rewrite delivery

Revised source: `paper/main.tex` (actual edits applied). The proof is rewritten for a graduate reader; the statement and all other source text are retained. Compilation was not run, as instructed. Verification below is a source and mathematical reasoning check, not formal correctness certification or independent expert verification.

The proof replaces A, Z, P, M₂ and K₀ by a single local quantity E(t), explicitly defined as the squared L² norm. It now shows differentiation under the integral, substitution of the heat equation, integration by parts with the zero boundary value, application of the assumed Poincaré inequality, and the integrating-factor argument. Taking square roots recovers the norm decay rate e^(−μt), while the squared energy decays at e^(−2μt). The zero initial energy case requires no division.

Preserved: the existing preamble, the macro `\Om`, every existing label (`eq:poincare-input`, `lem:heat-decay`, `eq:heat-conclusion`), the smooth real-valued solution hypothesis, the domain and boundary assumptions, the time interval, the given constant μ, and the exact stated conclusion. The proof uses the assumed inequality directly and does not assume μ is optimal.

The mathematical target and result remain the stated heat-flow L² decay estimate. The energy argument closes that estimate under the original smoothness assumptions; no further gap was identified within this scope. Extending the proof to weaker solution classes would require a separate justification of the energy identity and is outside this rewrite.
