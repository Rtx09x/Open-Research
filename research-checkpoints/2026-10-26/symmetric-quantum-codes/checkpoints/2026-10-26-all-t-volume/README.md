# Local addendum: strict volume bound for rank-two spin codes

**Internally independently audited theorem:** no complex rank-two code detecting spin ranks through2t can attain n+1=2(t+1)² for any integer t≥2. Thus unrestricted symmetric correction of t arbitrary physical-qubit errors requires **n≥2t²+4t+2** for t≥2. The known t=1,n=7 equality case survives.

This does not prove the proposed minimum3t²+3t+1, general intrinsic nondegeneracy, or an exact t3 minimum. External review and publication priority remain unresolved. It is a separate addendum; the original all-K volume package has not been modified.

- `THEOREM.md`: full argument, including the all-t divisibility reduction to13 cases.
- `check_no_perfect_rank_two.py/.json`: exact stdlib arithmetic and modular certificates.
- `independent/`: independently derived checker/result and analytic audit record.
- `volume_dependency/`: exact copy of the previous frozen volume proof, including its separately audited equality Lloyd-root premise and prior-source attribution. Its manifest hash is recorded in `reproduction.json`.

To reproduce without changing frozen files, copy this directory to a temporary location, then run:

```sh
python check_no_perfect_rank_two.py
python independent/check_perfect_spin_codes_independent.py
```

The first script requires only Python's standard library. The second additionally uses SymPy1.14.0. No optimization, floating-point tolerance, network or external data is used. The main analytic dependence on prior ordinary-LP monotonicity is documented in the copied volume theorem.

The exact cubic-depth Newton coefficient forces2t−1|2025. This finite reduction, not numerical sampling, is what makes the statement uniform for arbitrarily large t.

This package remains local under the private-repository packaging hold. No upload, git operation or publication occurred.
