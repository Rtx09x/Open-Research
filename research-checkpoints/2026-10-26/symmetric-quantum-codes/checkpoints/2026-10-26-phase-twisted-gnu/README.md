# Internally audited phase-twisted gnu construction

For every integer t>=10, an explicit algebraic complex rank-two symmetric code correcting t arbitrary physical-qubit errors exists at **n=4t²+2t**. This is one below the stated explicit Aydin–Alekseyev–Barg4t²+2t+1 formula, not a claim of globally best-known parameters, priority, external acceptance, or the conjectured leading coefficient3.

`THEOREM.md` gives the full all-t argument and direct physical erasure proof. Both logical states, all phases and their path compatibility are explicit. `independent/` contains a separate physical/binomial checker and analytic/source audit. The stronger gap2t−1 candidate is NOT included.

Copy this directory to a disposable location, then run with ordinary Python:

```sh
python check_phase_twisted_gnu.py
python independent/check_quantum_phase_gnu_independent.py
```

Only the standard library is used. No solver, floating-point tolerance, network, or external data is required. Scripts write result JSON next to themselves. Finite controls supplement the analytic uniform inequality rather than extrapolating it.

The independent checker was adapted only to read its pinned source from `provenance/audited_source.md`; this exact original source matches the hash in the independent audit. The final theorem adds the audit status and independently supplied direct physical proof. See `provenance/reproduction.json` and `MANIFEST.sha256`.

This package was frozen locally; no upload, git operation, external publication, or paid compute occurred in its creation.
