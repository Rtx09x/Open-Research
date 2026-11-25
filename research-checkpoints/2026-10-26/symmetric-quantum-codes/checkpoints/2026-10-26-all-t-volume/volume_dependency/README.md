# Internally checked unconditional spin-volume theorem

**Result:** every complex rank-K≥2 code in Sym^n(C²) detecting spin tensors through rank 2t obeys **n+1≥K(t+1)²**. In particular, one logical qubit correcting t arbitrary physical-qubit errors requires n≥2t²+4t+1.

This is an analytic all-t proof, independently audited internally. It is **not** an external-review or publication-priority verdict. It does **not** prove intrinsic nondegeneracy at arbitrary length, the conjectured minimum 3t²+3t+1, or the exact t=3 minimum. The known general upper construction remains 4t²+2t+1.

## Contents and dependencies

- `THEOREM.md`: statement, normalization, analytic proof, all-t polynomial positivity, physical applicability, and explicit published ordinary-LP transport.
- `check_spin_hamming.py`, `racah_coefficients.py`: exact normalization, linearization, symbolic algebra and positive controls. These use SymPy 1.14.0, not an optimizer. Finite tests supplement, not establish by interpolation, the all-t proof.
- `independent/`: separate advisor analytic report, independent exact controls using different formulas/positivity basis, and root's supplemental symbolic check.
- `EQUALITY_COROLLARY.md`: separately audited equality-only purity and Lloyd-root consequences. Not a dependency of the main theorem.
- `provenance/`: exact source version/hash, adaptation notes, and reproduction receipt.
- `MANIFEST.sha256`: frozen-file hashes, excluding itself.

## Reproduce without modifying this frozen directory

Copy this directory to a disposable location. In an existing Python environment with SymPy 1.14.0, run:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
python check_spin_hamming.py
python independent/check_racah_kernel_moments.py
python independent/check_quantum_critical_escape_polynomial.py
python independent/check_quantum_lp_length_monotonicity.py
```

All four scripts terminate with exact assertions. The standard-library-only monotonicity control does not use SymPy. The total bounded replay was measured in `provenance/reproduction.json`. Scripts write their result JSON next to themselves, hence the disposable-copy instruction.

The main proof's non-computational dependency is the all-length ordinary LP monotonicity theorem in Manes–Subramanian–Jiang, arXiv2610.00561v1, Supplement VIII.2. Its proof and normalization have been read and audited; the finite controls do not substitute for that theorem.

This package is local only. No upload, git operation, publication, or external review was performed in freezing it.
