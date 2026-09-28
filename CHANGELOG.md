# Fork changelog

This records **a-m-a-r-a fork changes**, not a reconstruction of upstream history.
The upstream MIT license and attribution are preserved.

## 2026-09-29 — OpenClaw integration documentation

- Added this changelog, fork purpose/difference guide and OpenClaw integration page.
- Linked the separately maintained OpenClaw sidecar and its install/update/rollback
  instructions. No claim that installing this provider alone installs OpenClaw tools.
- Corrected the README CI badge/link to refer to this fork, not upstream results.
- No Python behavior change in this documentation update.
- Follow-up CI on `610fee5`: [successful run](https://github.com/a-m-a-r-a/hermes-hyperspacedb-provider/actions/runs/36493877210),
  including Python 3.11/3.12 unit/contracts, packaging, Hermes discovery, SDK
  import matrix and upstream Hermes canary. An initial release-hygiene failure
  from duplicated upstream attribution was corrected by linking the canonical README.

## 2026-09-28 — Cognitive diagnostics (`7e59e33`)

Based on upstream `1b7ce96` (package version 2.8.1).

### Added

- `hyperspace_geometry(operation="analyze_thought_stability")`: 3–16 ordered
  capabilities, consecutive hyperbolic distances, mean log step ratio and bounded
  trend classification. Zero/unresolved steps yield `indeterminate`, not high trust.
- `hyperspace_geometry(operation="analyze_geometry")`: exact finite-sample
  four-point Gromov delta, diameter and normalized delta; 4–16 capabilities.
- `_cognitive.py` and [semantics/limitations](docs/cognitive.md).
- 15 cognitive tests: analytic trends/delta, ordering, invalid input, missing
  points, backend failure, bounded sampling and absence of database writes.

### Changed

- Geometry vector validation rejects boolean components; regression coverage
  includes boolean output from momentum.
- Existing `hyperspace_geometry` schema extended without adding an eleventh tool.

### Preserved / deliberately not implemented

- Existing momentum and relation summaries, session/profile/collection capability
  scope, Lorentz 129D contract, HMAC provenance and SDK deadlines.
- `trust_score` remains unavailable: upstream skill and SDK semantics disagree.
- No claimed Lyapunov exponent, calibrated confidence, hallucination detector,
  full official MCP parity, automatic runtime migration or raw-vector exposure.

### Verification

Initial SDK 3.1.3 run: 201 passed / 1 packaging skip before build. SDK 3.1.7:
202 passed, then an additional boolean-output regression passed. Wheel and sdist
built. These were local tests; GitHub Actions had not been verified at publication.
The follow-up complete suite includes that regression (203 tests).

### Install identity

The fork retained the upstream package version `2.8.1`; it is **not** uniquely
identified by that number. Pin commit `7e59e333622f4e6debe6acb9af44ef5f31f4c3d2`
or a reviewed descendant. Do not assume upstream PyPI contains these additions.
