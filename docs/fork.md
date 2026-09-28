# Why this fork exists

Upstream: [antydizajn/hermes-hyperspacedb-provider](https://github.com/antydizajn/hermes-hyperspacedb-provider).
Base: `1b7ce96`, upstream 2.8.1. This fork adds bounded cognitive geometry while
keeping upstream ownership, ledger and fail-closed behavior. It does not claim to
be the upstream project or a complete implementation of the official Hyperspace MCP.

| Capability | Upstream base | Fork |
| --- | --- | --- |
| Owned memory / HMAC / SQLite ledger | Existing | Preserved |
| Momentum / relation | Existing | Preserved, validation tightened |
| Ordered step-distance trend | Not exposed here | Added |
| Finite-sample Gromov delta | Not exposed here | Added |
| Calibrated truth score | Unavailable | Still unavailable |
| OpenClaw plugin and bridge | Not part of provider | Separate companion repository |

See [changelog](../CHANGELOG.md) for implementation details and verification, and
[cognitive semantics](cognitive.md) before interpreting output. Provider changes
are framework-independent; host-specific bindings should not accumulate here.

## Repository boundary and maintenance

- **This repo:** Python provider, geometry, capability validation, provider tests.
- **[OpenClaw sidecar](https://github.com/a-m-a-r-a/openclaw-hyperspace-sidecar):**
  TypeScript plugin, Python lifecycle bridge, host/session authorization, install
  examples and operations guide.
- **HyperspaceDB:** SDK/server embedding and storage behavior. This fork cannot
  repair a missing embedding feature or a misprovisioned backend tenant.

Upstream updates should be reviewed and merged explicitly, followed by provider
unit/contract tests and sidecar write/readback/cognitive tests. The sidecar pins a
reviewed provider commit, not a moving branch. No automatic upstream sync or
upstream pull request is claimed. Consult the actual Actions runs; a badge is not
a substitute for release-specific evidence.

Changes that belong in the general provider can be proposed upstream separately;
OpenClaw-only authorization and hooks remain in the companion. This is a maintenance
boundary, not a promise that upstream has accepted this fork's changes.
