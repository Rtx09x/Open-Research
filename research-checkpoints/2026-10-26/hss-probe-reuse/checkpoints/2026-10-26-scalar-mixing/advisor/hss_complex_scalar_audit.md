# Complex scalar fixed-basis extension — independent analytic audit

2026-10-26 01:54 UTC. **PASS**, conditional on the already audited real scalar theorem.

Audited `hss-probe-reuse/phase2/complex_scalar_fixed_basis_corollary.md`.
On a tree each scalar active basis has a unique parent, so choosing child phases
eta_i = eta_parent b_i/|b_i| makes the rephased transfer
conj(eta_i) b_i eta_parent real nonnegative. Zero transfers permit arbitrary
phases. Continuing to the physical coordinate vectors produces diagonal
unitaries separately for the row and column hierarchy; there is no cycle
consistency condition. Arbitrary complex coupling coefficients absorb all
active-basis phase choices. This is an exact unitary equivalence of the tied
fixed classes, not a coordinate-envelope relaxation.

After transformation, the real-probe reconstruction map is complex-linear:
apply it to real and imaginary parts and add. Orthogonal projection, residual,
and squared Frobenius norm split in the same way. Consequently the real
800 operator bound and 801 relative-error bound transfer without loss.
For real tests, conjugating Atilde* psi gives Atilde^T psi, so the real
transpose formulas use the available adjoint oracle legitimately. Three
complex A products and three complex A* products suffice, including known
unitary pre/postprocessing. This is not a count of six real-only oracle calls.
The same argument transfers unbiasedness and independent averaging.

Scope remains prescribed-before-probes scalar nested bases, arbitrary complex
input, and complex matvec units. No arbitrary-rank or unknown-basis theorem,
new complex-Haar moment claim, or numerical-stability guarantee is implied.
