#!/usr/bin/env python3
"""RED test for sequential-ID fix (Issue#1 Finding 1).

New contract: allocated point IDs must be SMALL, DENSE integers derived from
the ledger counter - NOT uniform uint32 hashes. The hash digest remains as
the logical identity (_hs_digest in metadata); the numeric point ID is just
a storage handle.

Tests:
1. IDs issued for distinct contents stay below 2**24 (16M) - far from the
   server's OOM danger zone.
2. Deterministic dedup: same content twice -> same ID, deduplicated=True.
3. Collision handling: ledger counter + existing-point check still prevents
   overwrites (fake client with pre-existing points).
"""
from __future__ import annotations

import pytest

THRESHOLD = 2 ** 24


class SeqIdClient:
    """Fake client that records inserted IDs; optionally pre-seeds points."""

    def __init__(self, plugin, tmp_path, preexisting_ids=()):
        self.inserted_ids = []
        self.points = {pid: {"id": pid} for pid in preexisting_ids}
        cfg = {
            "collection": "test_memory",
            "host": "127.0.0.1:50051",
            "api_key": "k",
            "ownership_hmac_key": "ok",
            "state_path": str(tmp_path / "ledger.sqlite3"),
            "auto_store": False,
            "trust_mode": "owned_only",
        }

        class Client:
            def __init__(self, outer):
                self.outer = outer

            def health_check(self):
                return "SERVING"

            def get_collection_stats(self, name):
                return {"name": name, "metric": "lorentz", "dimension": 129}

            def vectorize(self, text, metric="", **kwargs):
                return [0.1] * 129

            def insert(self, point_id, **kwargs):
                self.outer.inserted_ids.append(point_id)
                self.outer.points[point_id] = {
                    "id": point_id,
                    "metadata": dict(kwargs.get("metadata") or {}),
                    "payload": (kwargs.get("document") or "").encode(),
                }
                return True

            def get_points(self, ids, collection=""):
                return [
                    dict(self.outer.points[i], id=i)
                    for i in ids if i in self.outer.points
                ]

            def close(self):
                pass

        self._client = Client(self)
        self.provider = plugin.HyperspaceDBMemoryProvider(
            cfg, client_factory=lambda **kwargs: self._client
        )

    def initialize(self):
        self.provider.initialize("seq-id-session")

    def shutdown(self):
        self.provider.shutdown()


def _store(provider: "object", content: str) -> str:
    return provider.handle_tool_call("hyperspace_store", {"content": content})


def test_sequential_ids_stay_small(plugin, tmp_path):
    flaky = SeqIdClient(plugin, tmp_path)
    flaky.initialize()
    for i in range(25):
        out = _store(flaky.provider, f"SEQ_ID_SMALL_{i}: unique content {i}")
        assert '"ok": true' in out or '"ok":true' in out
    assert flaky.inserted_ids, "no inserts happened"
    assert max(flaky.inserted_ids) < THRESHOLD, (
        f"ID too large: {max(flaky.inserted_ids)} >= {THRESHOLD}"
    )
    # dense: max close to count (allow small gaps from probes)
    assert max(flaky.inserted_ids) <= len(flaky.inserted_ids) * 4
    flaky.shutdown()


def test_same_content_reuses_same_point(plugin, tmp_path):
    flaky = SeqIdClient(plugin, tmp_path)
    flaky.initialize()
    out1 = _store(flaky.provider, "SEQ_DEDUP_A: identical content")
    out2 = _store(flaky.provider, "SEQ_DEDUP_A: identical content")
    assert '"ok": true' in out1 or '"ok":true' in out1
    assert '"ok": true' in out2 or '"ok":true' in out2
    # Both writes must resolve to ONE point - no duplicate storage.
    assert len(set(flaky.inserted_ids)) == 1
    flaky.shutdown()


def test_never_overwrites_foreign_points(plugin, tmp_path):
    flaky = SeqIdClient(plugin, tmp_path, preexisting_ids=(1,))
    flaky.initialize()
    out = _store(flaky.provider, "SEQ_FOREIGN_1: first store")
    # must not have written into foreign point 1
    assert all(pid != 1 for pid in flaky.inserted_ids)
    assert '"ok": true' in out or '"ok":true' in out
    flaky.shutdown()
