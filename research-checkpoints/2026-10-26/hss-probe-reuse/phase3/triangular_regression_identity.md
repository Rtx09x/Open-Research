# Fixed-basis coefficient recovery as a nilpotent two-class regression

**Status:** exact algebraic reduction, not a new robustness theorem or novelty
claim. It reformulates the existing fixed-basis LM coefficient decoder and
isolates where a wider-probe small-gain proof would have to act.

Let U_v,V_v be the globally lifted active bases at a nonroot hierarchy nodev,
and W_v,Z_v its globally lifted left/right detail bases. All W_v together with
the root-active basis form an orthonormal basis of the row coordinates; the
Z_v and root-active basis do the same on the column side. The fixed class is
the orthogonal direct sum of local coefficients

    W_v a_v V_v^T + W_v b_v Z_v^T + U_v c_v Z_v^T,

and the free root core. Define C_F to contain the first two terms at every
node and the root core, and C_T to contain the third terms. Then
C=C_F orthogonal-direct-sum C_T. In left-wavelet row coordinates C_F is a
prescribed independent-row subspace class of per-row dimension2k; C_T is an
independent-column class of per-column dimensionk. This statement concerns
the coefficient subspaces, not a free sparse forest after wavelet rotation.

For known tree probes of widths>=2k let

    F_v=V_v^T Omega, G_v=Z_v^T Omega,
    P_v=U_v^T Psi,   Q_v=W_v^T Psi.

Assume each[F_v;G_v] and[P_v;Q_v] has orthonormal rows, and root active frames
also have orthonormal rows. Define local regressions, directly from the
ORIGINAL queried samples, by

    a_v^0=W_v^T A Omega F_v^T,
    b_v^0=W_v^T A Omega G_v^T,
    c_v^0=P_v (Z_v^T A^T Psi)^T,

and the analogous forward root regression. Write these linear operators as
R_F(A) in C_F and R_T(A) in C_T. R_F is exact on C_F, R_T is exact on C_T.

Their cross-actions strictly move coefficients to ancestors:

* R_F(U_j c_j Z_j^T) can have a nonzero coefficient only at a strict ancestor
  v ofj (or at the root), because W_v^T U_j vanishes otherwise.
* R_T(W_j a_j V_j^T) can have a nonzero coefficient only at a strict ancestor
  v ofj, because Z_v^T V_j vanishes otherwise.
* R_T(W_j b_j Z_j^T)=0 for everyj: different detail columns are orthogonal,
  and atv=j the factor P_j Q_j^T vanishes. The root C_F term also maps tozero.

Consequently on coefficient vectors the combined measurement regression is

    b=(R_F(A),R_T(A)),
    (I+K)x=b,     K(x_F,x_T)=(R_F(x_T),R_T(x_F)).

The cross-operatorK strictly increases level. It is nilpotent, K^(L+1)=0,
with root treated as a terminal level. Thus the exact coefficient decoder is

    x=sum_(m=0)^L (-K)^m b.

Forward substitution in this system is precisely LM's subtract-and-compress
recursion: discarded row details cannot affect later forward row-wavelet
observations, so only earlierad terms need subtracting; transpose-side
observations analogously subtract earlierda terms. Thedd terms never feed
back into the opposite regression. This equivalence holds for arbitraryA,
not just on-model data.

## What this gives, and does not give

It proves deterministic exact recovery from the local orthonormal frames and
identifies an ancestor-directed alternating regression graph. It does not
bound the sum's mean-square norm: the same frame variables enter many edges,
and the raw regressions b also depend on those variables. For the stated
fixed-basis, independent-bank construction, R_F depends only on Omega and
R_T only on Psi, so these two random operators ARE independent. The obstacle
is repeated reuse of each operator and correlation of b with the operators;
independent banks do not make the reused powers K^m independent. Learned
bases could destroy initial operator independence, but are outside this
fixed-basis statement.

For width s>2k, an isolated full-complement orientation has isotropic
projection factor k/(s−k). A complete constant-factor bound would need to
apply that attenuation to a rigorously justified innovation/path decomposition
of this whole nilpotent system. It cannot be obtained by multiplying isolated
one-step expectations or summing purportedly independent feedback amplitudes.
The existing exact square one-bank913/625 example and branch constant5 must
remain regression controls.

Global least squares uses additional unused probe directions which the local
regression R_F/R_T discards; it is a genuinely different decoder. This identity
neither proves nor refutes its expected inverse bound.

Closest row-regression baseline: Gallmeier--Otto, §2,
https://arxiv.org/html/2610.07513v1 , gives an explicit relative regression
moment bound for one prescribed independent-row class. It applies separately
to the row-class abstraction with Gaussian probes, not automatically to the
coupled reused regression above. Its local dimension is not a bound on the
full HSS class's row dimension.

An exact unrelated-left/right rational control is now supplied in
`verify_triangular_regression_exact.py`: N8,k1,L2,width3,22 orthonormal
coefficient atoms. It verifies K^3=0, strict-ancestor support, and equality of
the original-sample finite inverse with the LM recursion using Fraction only.
This is a finite algebra control, not an independent proof for all ranks.
