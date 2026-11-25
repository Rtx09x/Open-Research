# Online bin packing: exact AH parameter refinement

**Audited asymptotic upper certificate:**

`1848920194883516152323541607 / 1171513518439186595284254720 ≈ 1.5782320611603713`.

Three rational container-proportion transfers refine the existing Advanced Harmonic algorithm for classic deterministic one-dimensional online bin packing. Every published analysis u,v,w remains unchanged. This is a modest reparameterization, not a new architecture, a major closure of the gap, or a priority claim. Read `AH_THREE_PARAMETER_REFINEMENT.md` for source-theorem applicability and limitations.

```sh
python verify_ah_source_delta.py
python verify_ah_full.py ah_three_parameter_full_certificate.json ah_three_parameter_full_verification.json
python verify_ah_three_parameter_algebra.py
python tests/audit_ah_three_parameter.py
python tests/audit_ah_two_scenario_floor.py
```

All use standard-library exact Fractions. The complete check covers **402 scenarios and 804 strict knapsack cases**, including the required source balance inequalities. The separate two-scenario floor proves optimality only inside the fixed-published-weight/three-transfer certificate family, not a lower bound on actual algorithm cost.

The independent audit originally parsed the primary paper. The portable replay uses **independently extracted numerical table facts**, not the worker's snapshot, in `tests/source_table_facts.json`. Integration re-executed the original independent parser on the locally cached source before exporting these facts; its source hash and URL are recorded. The full paper is deliberately not redistributed. Replaying these facts is not a fresh network/literature verification.

The earlier one- and two-parameter full-scenario certificate anchors and proofs are preserved. The unchanged-algorithm reanalysis and broad lower-bound experiments remain in the source workspace but are not needed for this lean preferred checkpoint. Source references and the historical reading cutoff are in `literature.md`. Unsuccessful experiments and initial consultation packets are not treated as conclusions.

## Additional independent source-derived audit

`python tests/ah_portable_check.py --track-root .` replays all 402 scenarios with exact integer-lattice pricing and **no one-item dominance pruning** (109,845,241 visited nodes). Its facts come from the separate `extract_ah_primary_facts.py` parser, not the worker/advisor tables. Both the original primary-HTML replay and portable factual-table replay passed; their concise logs are retained. `ah_primary_numerical_facts.json` pins the source hash. A fresh source copy, if independently obtained, can be transcribed with `python tests/extract_ah_primary_facts.py SOURCE.html OUTPUT.json`; no download is performed automatically.
