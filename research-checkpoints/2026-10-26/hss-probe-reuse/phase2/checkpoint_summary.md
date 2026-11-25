# Phase-two checkpoint: independently audited restricted theorem

## Main result

For arbitrary rank parameter k and **independently prescribed dense nested
bases**, there is a four-k-query decoder with

    E||A-B||_F^2 <= (20L+3) min_{H in C_fixed}||A-H||_F^2.

Both directions count:2k forward plus2k transpose products. The output lies
in the exact fixed-basis rank-k HSS class. The proof uses square local frames
with full HaarO(k) complement orientations, not signs-only for generalk.

`fixed_basis_bound.md` gives the complete argument and explicit algorithm.
The advisor independently audited the algebra, the one-bank conditioning,
wavelet cross-term cancellation, anchor/dd sectors, rank-independent matrix
covariance and final coefficient ledger; the audit passed. This is an internal
independent check, not external peer review. Novelty remains unestablished.

The new steps after the supplied Pro consultation are:
1. A sharp one-bank pure-detail transport bound5, using pointwise flux
   contraction and `E[ZZ^T] <= ||W0||_F^2 I/k` from Haar conjugation.
2. Arbitrary one-bank-independent input bound5 by orthogonal row wavelets and
   their distinct central birth signs.
3. Opposite-bank conditioning for the correlated ad/da anchor correction and
   dd sources; Hilbert-space triangle gives sector bound20.
4. The consultation's exact sign-sector separation then gives uniform carried
   energy20, without assuming any monotone-energy shortcut. Orthogonal output
   coefficient spaces yield the O(L) approximation bound.

## Additional verified results

* The Pro six-k / factor-two coordinate-tree candidate was independently
  derived and extended to arbitrary forests. Exhaustive integer tests cover
  all125 rooted four-vertex forests,274 total cases and88,576 executions.
  `three_color_forest_theorem.md` states the exact leakage identity.
* Rational N=8 wavelet certificate: the true fixed class has dimension22 but
  its transformed coordinate envelope has30 entries and a triangle. Dense
  nested bases do not become free forest support under naive wavelets.
* The completed Pro Gaussian-innovation obstruction, flux/isolated-branch
  proofs and sector identity passed a separate algebra/conditioning audit;
  all supplied exact verifiers were source-inspected and replayed.

## Failed shortcuts retained, not hidden

* Nonbacktracking three-column frames plus the old decoder have an explicit
  coordinate family with squared error L+2 against fixed optimum1.
* Even coordinate-correct three-color frames do not reproduce the successful
  direct decoder when fed through the old subtractive LM recovery: factor3
  already occurs at L=2.
* One-bank constant-one contraction passed shallow exhaustive tests but fails
  exactly at L=4:1 becomes913/625 for every transpose-sign realization. It was
  replaced by the sharp bound5. Rational gains2.37003,...,4.96338 confirm
  bounded transient gain rather than growth without bound.

## Reproducibility

Exact standard-library tests:

    python verify_one_bank_counterexample.py
    python verify_matrix_one_bank_bound.py
    python verify_one_bank_sharpness.py
    python wavelet_support_obstruction.py

Exact integer forest test:

    OPENBLAS_NUM_THREADS=1 python verify_three_color_forest.py

Supplemental numerical implementation:

    OPENBLAS_NUM_THREADS=1 python test_fixed_basis_algorithm.py

It tests k=1,2,3 and L=1,...,4,25 trials each, verifies4k individually counted
queries, class membership, and exact-model recovery to about1e-15. Observed
mean fixed-class error ratios are about2.48--3.42; those experiments are not
the proof. Haar QR generation includes the required diagonal-sign correction.

## What remains open

This is **not RE-02**. The bases must be available before these specialized
probes are queried. Unknown-basis learning from reused Gaussian data, a full-
HSS comparator, and avoiding an O(L^2) product of separate guarantees remain.
The sharper uniform-energy constant2 also remains unproved, but is unnecessary
for the restricted O(L) theorem. The existing two-color coordinate example
shows linear-depth error can occur for this square-frame coefficient decoder.

All phase-two writes are confined to this folder; frozen initial artifacts
and the supplied Pro archive were not modified. No Pro call, user-computer
operation, upload, publication, repository modification or push was performed
by this worker. One unnecessary read-only `git status` invocation returned no
output; no further git commands will be used.

## Optional finite-randomness construction

`finite_orientation_variant.md` gives a sibling-gauged signed-permutation
version with the same4k/(20L+3) guarantee; advisor analytic audit passed.
`test_finite_orientation_variant.py` verifies its implementation numerically
for k<=3,L<=4, with exact callback counts and on-model residuals around1e-15.
