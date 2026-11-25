# Binary single-deletion code optimality

**Global target remains open:** the checked literature interval is 316 ≤ A(12,1) ≤ 320. No 317-word construction or improved global upper bound is claimed.

The exact local result is: every distinct valid code C with |C| ≥ 316 removes at least **10** words from VT0(12). Two independent implementations enumerate all **2,733,456 connected supports** through radius nine, with matching support hashes. See `trade_lemma.md` for completeness and `results.md` for scope. Literature novelty is unconfirmed.

```sh
python scripts/baseline.py 12
python scripts/trades.py --n 12 --k 9 --seconds 280
python scripts/verify_trades_independent.py --n 12 --k 9 --seconds 280
python scripts/small_exact_control.py
```

Run from this folder with one BLAS thread. The first two enumerators require the pinned scientific environment where imported; the independent string/Fraction replay is solver-free. The root `run_checks.py --full` isolates generated outputs and verifies completeness and matching hashes, not merely exit codes. `evidence/` contains the original exact-count checkpoint and a small known neutral-switch control.

`results.md`, `orbit_relaxation.md`, and `spectral_certificate.md` retain the scientific context and unsuccessful global routes. The noncompetitive global dual (rounds to 321), large clique arrays, spectral matrices, experimental logs, and consultation packet are deliberately not part of this lean local-theorem checkpoint. References to those exploratory artifacts in the contextual notes describe the original workspace, not bundled or freshly replayed certificates. No global-optimality or spectral-bound advance is claimed.
