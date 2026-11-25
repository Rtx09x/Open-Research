# Optional explicitly coupled finite-randomness variant

**Status:** explicit construction independently analytically audited by the
advisor; audit passed2026-10-25. The advisor identified the moment condition;
the construction below states the necessary equivariant gauges explicitly.
The main Haar theorem does not rely on this optional variant.

For square width2k, every sibling pair's active frames F_0,F_1 are mutually
orthogonal k-by-2k rows. Therefore the sibling frame is a complete complement:
at child i define

    G_i = H_i F_(1-i),

where H_i is an independent uniform **signed permutation** k-by-k matrix.
Generate each child's two active descendant frames by applying its prescribed
orthogonal physical transfer [V_i,V_i_perp] to [F_i;G_i], and recurse. At the
root the sibling active frames are the two k-row halves of I_(2k). Generate
the row/transpose bank independently, using U in place of V.

This is not the generic algorithm that chooses an arbitrary complement as a
function of F_i alone. The sibling-based complement gauge is retained as
part of the recursion. It makes the orientation relating each child boundary
to its parent **exactly H_i**, independently at all nodes, so the normalized
branch recurrence does not require Haar invariance to change gauges.

Uniform signed permutations satisfy precisely

    E H_i = 0,
    E[H_i^T M H_i] = (tr M/k) I

for every fixed k-by-k M. Their laws are invariant under a central minus sign,
which can be extracted independently. These are the moments used in the
rank-independent covariance induction, frame isotropy, wavelet birth-sign
cancellation and fine-sector decomposition. Thus every displayed argument
of `fixed_basis_bound.md` applies to this explicitly coupled construction.

The random choices are now finite: an independent uniform permutation and
k independent signs per node and per bank. The arithmetic of the given
prescribed bases is unchanged. No assertion is made for signs-only rotations
H_i=+/-I when k>1; those lack isotropic conjugation. Nor is an arbitrary
non-equivariant signed-permutation complement construction covered.

The exact local verifier `verify_matrix_one_bank_bound.py` uses all8 signed
permutations for k=2 and checks512 histories of noncommuting transfers. A
global finite-group enumeration is not needed for the proof, but would be a
useful implementation cross-check of this explicit gauge choice.

Implementation: `finite_tree_frame` in `fixed_basis_algorithm.py` implements
this precise sibling gauge. `test_finite_orientation_variant.py` checks
k=1,2,3 and L=1,...,4 with30 draws each, exact4k callback counts, fixed-class
membership, and exact-model relative residuals about1e-15. Results and log
are `finite_orientation_results.json` and `finite_orientation_run.log`.
These are supplemental numerical controls, not the proof.
