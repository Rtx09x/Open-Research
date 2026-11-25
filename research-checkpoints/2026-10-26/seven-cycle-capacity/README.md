# Seven-cycle capacity: finite terminal recycling checkpoint

**Exact finite lower bound: Θ(C7) ≥ 3.258832624232849476**, dimension **768,000**.

This is a small strict improvement over the reproduced August 2026 construction (3.258832620353266309…). It is not the exact capacity, a new universal combining theorem, or a certified priority claim. It uses the existing BPZ seven-family composition theorem and the cited input representation.

Read `result_proof.md`. The explicit base is `terminal_recycled_base.json`; the 12-node DAG, full exact integer cardinality, and rational root bracket are in `optimized_recycle_certificate.json`. The simpler dimension-128,000 and 2402-word macro-code anchors are retained.

```sh
python verify_base.py
python replay_wrapper.py
python verify_weighted_terminal_independent.py
python verify_recycled_certificate.py
python verify_recycled_certificate.py optimized_recycle_certificate.json
python tests/audit_c7_optimized.py
```

All primary checkers use the standard library. The independent DAG audit uses exact rational logarithm enclosures with explicit remainders, a different root-bracket route from the worker's giant-integer-power check. It also independently replays the base and simpler certificate. Finite arithmetic does not replace the inherited mathematical theorem and is not a full Lean formalization.

The attributed `published/` source snapshot is pinned to commit `c753408492dde92a239708986d16c15dbf6c3235`. Its Apache-2.0 LICENSE and NOTICE are retained. Only generated caches and the inactive nested CI workflow are excluded; bundled source files are unmodified. Source provenance and the upstream pinned Lean files are retained. Optional pytest tests require the upstream `published/requirements.txt`; pytest was not installed in the integration environment and that entire test suite was not rerun.

## Additional independent construction audit

`python tests/c7_portable_check.py --track-root .` independently reads K4a from the literal Lean snapshot, rebuilds the recycled families and explicit recursion, and checks both integer root brackets. It first recomputes the five inherited finite certificates using the upstream implementation. `tests/c7_fresh_check.log` records the passing original run (the portable copy changes path handling only). This is not an independent proof of the entire inherited construction theorem.
