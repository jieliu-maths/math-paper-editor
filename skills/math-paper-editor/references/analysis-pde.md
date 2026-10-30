# Analysis and PDE checks

Use only the checks relevant to the paper. These are prompts for actual
derivation, not a checklist whose completion establishes correctness.

- Check dimensions, parameter ranges, endpoints, signs, domains, boundary
  conditions, and the precise notions of weak, strong, or classical solution.
  Verify admissible test functions and approximation arguments.
- Distinguish continuous from compact embeddings, local from global control,
  and critical from subcritical exponents. Weak convergence alone does not
  imply strong convergence. Track common subsequences and nonlinear limits.
- Recompute Hölder exponents, scaling, units, boundary terms, and constants.
  Distinguish a constant for each fixed parameter from one uniform in that
  parameter. State the order of smallness choices and absorption conditions.
- For variational arguments, examine boundedness, coercivity, lower
  semicontinuity, compactness loss, splitting, and nonzero limits. Regularity,
  uniqueness, and maximum principles have their own hypotheses.
- For energy or stability arguments, explain coercivity and the sign of the
  energy derivative separately. Differentiate cutoffs, weights, and moving
  parameters. An unbounded transport term may require integration by parts.
- Orthogonality must remove an identified freedom, and parameter equations
  need an actual nondegeneracy argument. Compare error and dissipation scales
  before choosing a weight; a high algebraic order is not automatically small
  relative to an exponentially small coefficient.
- Close a bootstrap on the same interval with explicit improvement and an
  exclusion of first exit. Do not remove a coupled control if the remaining
  estimate already presupposes it. Integral control does not automatically give
  pointwise decay, and a formal identity needs extension to the claimed class.

Test a disputed inference with the cheapest relevant example. State precisely
what it refutes; failure of one candidate does not refute an entire method.
