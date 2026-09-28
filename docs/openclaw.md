# OpenClaw integration

**Yes, this provider can be used from OpenClaw**, through the separately maintained
[openclaw-hyperspace-sidecar](https://github.com/a-m-a-r-a/openclaw-hyperspace-sidecar).
Installing this Python package alone does not register OpenClaw tools or hooks.

```text
OpenClaw -> scoped TS plugin -> one-shot Python bridge
        -> this provider -> HyperspaceDB SDK -> server
```

The companion includes:

- [Installation and generic configuration](https://github.com/a-m-a-r-a/openclaw-hyperspace-sidecar/blob/main/docs/installation.md)
- [Architecture and exact tool contracts](https://github.com/a-m-a-r-a/openclaw-hyperspace-sidecar/blob/main/docs/architecture.md)
- [Verification, upgrade and rollback](https://github.com/a-m-a-r-a/openclaw-hyperspace-sidecar/blob/main/docs/operations.md)
- [Compatibility](https://github.com/a-m-a-r-a/openclaw-hyperspace-sidecar/blob/main/docs/compatibility.md)
- [Sidecar changelog](https://github.com/a-m-a-r-a/openclaw-hyperspace-sidecar/blob/main/CHANGELOG.md)

It exposes curated store/search/status and a bounded cognitive operation. Optional
prompt recall is scoped to explicitly configured private owner sessions. It is
neither a full Hermes runtime nor an official MCP server and does not expose all
provider admin/graph capabilities.

Because each bridge request creates a new provider session, handles returned by a
previous request cannot authorize a later cognitive request. The companion solves
this by exact-content reacquisition and analysis in one lifecycle; it does **not**
weaken provider capability validation or accept arbitrary IDs.

A working deployment requires an embedding-enabled Lorentz 129D backend, a private
API key, stable HMAC key/ledger/profile scope, and an OpenClaw version supporting
the required tool/hook APIs. Follow the companion's pinned requirements and
verification checklist, not a generic `pip install latest` recipe.
