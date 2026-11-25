# Uniformly mixing deterministic matrix-source moments — analytic audit

2026-10-26 02:00 UTC. **PASS for the restricted source theorem**, conditional
on the explicitly gauged pure-source reverse-coordinate construction already
audited in the matrix branch reduction. No correlated-source substitution.

Audited `hss-probe-reuse/phase2/uniformly_mixing_matrix_source_moments.md`.
With d>=2k, minimum singular values of T,B at least delta>0, set
rho²=1-delta², c=min(delta^4,(1-k/d)delta²), and
Bdelta=[1+k/(2d(1-rho^4))]/c. The exact flux identity gives
E H_next <=(1-c)H. Independent centered Haar complements give
E||C_next||² <=rho^4||C||²+(k/(4d))H.
Summing these inequalities, including the final root state, gives
sum E J <=2||C0||²/(1-rho^4)+Bdelta H0.
Local emitted energy and terminal root energy are bounded by J at their
respective cuts. Thus the displayed all-state output estimate has no missing
root or endpoint term. For a pure passive matrix source H0=||M||²,C0=0;
adding its own orthogonal birth coefficient proves the stated second moment.

The real O(d) scalar fourth-moment formula was independently checked by SVD
and the diagonal-entry moments. The comparison with three times the squared
variance follows from tr((AA^T)^2)>=(tr AA^T)^2/d. Coordinatewise Cauchy
proves its Hilbert-valued version. Two independent centrally symmetric Haar
linear images retain the same fourth-moment constant by expansion. This
argument does NOT automatically apply to the finite signed-permutation
second-moment variant.

For the complete ancestor/root output, the already audited block recursion
makes future mean responses deterministic linear maps of X,Z, and Doob
increments linear maps of the fresh passive rotations. Their predictable
variation depends on (D,Y,W) alone. Resetting common C=0 therefore preserves
future variation; the all-state estimate bounds its inclusive conditional
tail by Bdelta H. Pointwise flux contraction supplies H<=||M||². Consequently
E Avar²<=2 Bdelta²||M||^4. The dimension-free Hilbert martingale fourth bound
from the scalar proof yields ancestor fourth moment<=242 Bdelta²||M||^4.
Orthogonal birth support then gives total fourth moment
[1+2Bdelta+242 Bdelta²]||M||^4.

Constants are uniform in k and depth for fixed delta (and d>=2k). Weak-mixing
or coordinate transfers are excluded. M must be deterministic before both
banks. This is not a fourth moment of the whole source operator norm, a
conditional opposite-bank theorem, a correlated matrix-anchor estimate, or
an arbitrary-rank fixed-basis reconstruction theorem. The full unrestricted
rank-k robustness problem remains open.
