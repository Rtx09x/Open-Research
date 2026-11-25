# Phase 2: independent checks of Pro suggestions

Frozen initial artifacts in the parent folder are not modified.

## Main independently audited restricted theorem

`fixed_basis_bound.md` proves that **4k total queries** give expected squared
error at most **(20L+3) times the best approximation with independently known
dense nested bases**, for every k. The proof establishes a uniform carried-
energy bound20, using a sharp one-bank transport constant5, block-wavelet
sign orthogonality, and the consultation's exact sign sectors. The advisor's
independent algebra/conditioning audit passed. This is not full RE-02; unknown
bases and the full-HSS comparator remain unresolved. Novelty is unestablished.

`fixed_basis_algorithm.py` is a black-box implementation with genuine Haar
complements; its test checks exact query counts, fixed-class membership and
exact-model recovery numerically. `verify_matrix_one_bank_bound.py` checks the
noncommuting k=2 covariance invariant in exact rational arithmetic.
An explicitly sibling-gauged finite signed-permutation construction is also
audited; see `finite_orientation_variant.md` and its numerical callback test.

## Coordinate-forest improvement

`three_color_forest_theorem.md` proves that **6k total queries** give expected
squared error **at most 2 times the best known block-forest support error**.
This is depth-independent and supersedes the earlier 4k / diameter-factor
tradeoff if a constant two extra k-column query groups are permitted.

The exact expected error is a sum of off-support block energies with weights
1 or 2. Parent/child/diagonal leakage cases are disjoint modulo three.

`three_color_forest.py` is a black-box implementation;
`verify_three_color_forest.py` and its JSON/log provide exhaustive integer tests.
The theorem was independently algebra-audited by the advisor. Novelty is not
claimed: direct star bicoloring and signed probing both have prior art.

## Scope and unresolved work

The comparator is the best matrix on a **known coordinate forest support**,
not the best rank-k HSS matrix. A rank-one counterexample explicitly prevents
that reinterpretation. Dense fixed nested bases and unknown adaptive bases
remain distinct problems. `wavelet_support_obstruction.md` exactly refutes the
naive transformation of dense nested bases into free forest coordinates.

## Scoped failed shortcuts and consultation audit

`pro_audit.md` records the completed consultation's Gaussian-innovation,
flux, branch and sector audits; the supplied exact verifiers were inspected
and replayed without modifying their archive. `nonbacktracking_obstruction.md`
and `ordered_frame_failure.md` document two failed three-column extensions.

The constant-one independent-bank transport guess passed shallow tests but
failed at L=4 with exact energy913/625 from initial1. It was then replaced by
the proved sharp constant5, not abandoned. See `one_bank_counterexample.md`,
`verify_one_bank_counterexample.py`, and `verify_one_bank_sharpness.py`.

## Correction to a frozen initial note

The final paragraph of `../fixed_basis_unbiasedness.md` is stale: positivity of
its cross term is **refuted**, not merely unproved. The weaker monotone carried
energy claim is also refuted by the exact rational certificate and independent
verifier in the parent folder. The unbiasedness theorem remains valid, and the
sharp uniform-energy constant2 remains unproved; the depth-independent
constant20 is now proved for prescribed bases. This correction is
recorded here rather than editing the frozen original.
