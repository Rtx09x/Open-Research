# Permutation-invariant two-error quantum codes

**The unrestricted 18-qubit case remains open. No 19-qubit-minimum theorem is claimed.**

- `proved_reduction.md`: audited nondegeneracy reduction and restricted pure/4-anticoherent and time-reversal exclusions.
- `generator_reformulation.md`: exact equivalence to a 128-real-variable compressed-generator system, not an infeasibility proof.
- Exact necessary syndrome-variance interval: **1/102400 < ν ≤ 1/722**. This does not exclude the remaining case.
- `literature.md`: n ≤ 17 exclusion is already prior work (Okada 2025); certificates here reproduce rather than discover it. The known 19-qubit construction is a positive control.

## Independent exact replays

Run from this folder:

```sh
python tests/check_quantum_farkas.py
python tests/check_quantum_gram_bound.py
python tests/audit_code19.py
python tests/audit_pure_complement.py
python tests/audit_time_reversal.py
python tests/audit_optimized_robust_gap.py
python tests/audit_gram_map_exact.py
```

All but the final spin-matrix trace audit use the standard library; that audit uses SymPy. The two `check_quantum_*` programs use explicit Racah factorial sums and rational arithmetic. The separate Gram-map checker uses exact matrices/direct traces rather than 6j symbols. Certificate generators (`certify_*.py`, `code19_exact.py`, `optimize_robust_gap.py`) use the pinned numerical/symbolic environment; run them only in a disposable copy because they write outputs.

`generator_model.py` and reconstruction controls are numerical implementation checks, not proofs that the 128-variable system is infeasible. `full_search_n18_log.json` is a negative search log; neither unsuccessful optimization nor its omitted NPZ candidate proves nonexistence. Mathematical applicability remains tied to the arguments in the proof notes. Novelty of the reductions is unconfirmed.
