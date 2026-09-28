# Cognitive diagnostics

This fork extends the existing `hyperspace_geometry` tool without adding another
schema to the agent context. It operates on the configured, verified Lorentz 129D
collection at curvature 1, converting to the Poincare 128D ball for computation.
No additional server RPC, automatic write, runtime switch or raw-vector disclosure
is introduced. Existing SDK deadline/error handling and session capability scope
remain in force. Existing geometry recovery may re-vectorize stored content on
the configured backend when the stored vector is invalid.

## Operations

- `analyze_thought_stability`: 3–16 unique session handles, in caller-defined order.
  Returns consecutive hyperbolic distances, log ratios, their mean, and
  `contracting`, `neutral`, `expanding`, or `indeterminate`.
  Distances at or below 1e-12 are numerically unresolved; no fabricated score is
  returned. Neutral tolerance is 1e-6 on the mean log ratio.
- `predict_momentum`: existing two-handle SDK Koopman extrapolation, steps in
  (0, 4]. Returns dimension and radius only, not a predicted statement or vector.
- `analyze_geometry`: 4–16 handles. Exact four-point Gromov delta on the finite
  sample, diameter and delta/diameter (null for a zero-diameter sample).
  At most 1,820 quadruples; no random sampling or collection migration suggestion.
- `trust_score`: explicitly unavailable, not a synthetic probability.
- `predict_relation`: existing two-handle tangent-vector norm summary.

Example after obtaining handles through retrieval:

```json
{"operation":"analyze_thought_stability","handles":["<first>","<second>","<third>"]}
```

Use an explicit sequence of observations, short decision summaries or hypotheses.
Do not collect hidden reasoning traces. Search rank is not chronological order.
The provider does not infer timestamps or reorder the input.

## Interpretation and upstream differences

This is **not** a drop-in implementation of the upstream MCP result contract.
No `lyapunov_exponent`, `is_stable`, attractor ID, truth probability or automatic
permission gate is claimed. A mean log step ratio is a geometric proxy: it can
telescope to endpoint step lengths, so inspect the returned individual distances
and ratios for intermediate excursions. A contracting path can still be wrong;
a changing topic can expand without error. A finite sample cannot establish
stability of a dynamical system. Delta is measured under the existing hyperbolic
metric, not evidence that this is the best embedding metric.

Reviewed upstream source: YARlabs/hyperspace-db commit
`c226b5496aa5ae2bd95ddaf9aa4f799fac25c8b1`, especially
`sdks/python/hyperspace/client.py`, `sdks/python/hyperspace/math.py`, and
`integrations/hyperspacedb-skills/skills/hyperspacedb-cognitive/SKILL.md`.
The skill describes a 0–1 composite trust score, but the Python implementation
returns a signed energy trend and uses 0 or 1 fallbacks for missing data/errors.
These incompatible semantics are not exposed as calibrated trust here.

References:
- https://github.com/YARlabs/hyperspace-db
- https://yar.ink/docs/hyperspacedb/api-reference/connection
- Original provider attribution: see the repository README.

## Verification scope

Analytic geodesic fixtures cover contracting, expanding, neutral and repeated
points. Tests cover exact delta, input order independent of backend order,
missing points, backend timeout, invalid arguments, bounds and read-only behavior.
Tests use synthetic points; no production collection is read or modified.
