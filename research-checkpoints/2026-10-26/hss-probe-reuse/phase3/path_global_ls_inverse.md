# A depth-uniform expected inverse bound for a coordinate path

**Status:** restricted inverse-moment lemma; advisor analytic audit passed.
This is NOT a relative Frobenius approximation theorem. In particular, the
actual off-model measurement noise depends on the probes; the independent
measurement-noise corollary below does not cover that noise.

## Model and measurement Gram

Take the fixed matrix class supported on the diagonal and both orientations
of the edges of a known path with vertices 0,...,n−1. Use s=4 columns in each
of two independent probe banks, Omega and Psi. Every probe row has norm one.
Start each bank at any fixed orthogonal unit pair; recursively choose row
omega_(i+1) uniformly on the unit sphere in omega_i's orthogonal complement.
The Psi rows follow an independent copy of the same construction.

These are the restrictions of the generic wider orthogonal tree-frame
construction to a coordinate representative path. The path-supported class
is a restriction of that coordinate HSS class, not the whole class: branches
and all other allowed coefficients are absent here.

For M(B)=(B Omega,B^T Psi), let G=M^*M on the orthonormal supported matrix-unit
basis. A diagonal coefficient has Gram diagonal 2 and is orthogonal to every
other coefficient: adjacent probe rows are orthogonal. The directed-edge
coefficients split into two chains in the row/column bipartite observation
graph. Each chain Gram is tridiagonal with diagonal entries2 and off-diagonal
entries c_i. A turn at row i contributes omega_(i−1)^T omega_(i+1), and a
turn at column i contributes the analogous Psi inner product. These alternate
along either chain.

For a single bank, conditional on all rows through i, the distribution of
omega_(i−1)^T omega_(i+1) is the first coordinate of a uniform vector on S^2,
hence uniform on[−1,1] and independent of the conditioning data. Induction
shows the successive turns within each bank are independent. Independence
of the banks therefore makes all c_i in either chain independent uniforms.
The two chains need not be independent for the expectation statement below.

## Lemma

For every path length,

    E G^(−1) <= Catalan I < I

in Loewner order, where Catalan=integral_0^1 atan(t)/t dt is about0.915965.
In particular, the bound is independent of hierarchy depth.
Here every finite tridiagonal chain is positive definite even when |c_i|=1:
its elimination pivots satisfy d_1=2 and d_j=2−c_(j−1)^2/d_(j−1)>1.

For an interior index i, eliminate the left and right subchains. With their
last pivots d_L,d_R>=1, the exact scalar Schur complement gives

    (G^−1)_ii = 1/(2−c_(i−1)^2/d_L−c_i^2/d_R)
               <= 1/[(1−c_(i−1)^2)+(1−c_i^2)].

By a+b>=2sqrt(ab), independence, and an elementary integral,

    E (G^−1)_ii <= 1/2 [E(1−c^2)^(−1/2)]^2
                 = 1/2 [pi/2]^2 = pi^2/8.

The weaker pi^2/8 bound above is already sufficient. For the sharper stated
constant, integrate the exact dominating function:

    integral_0^1 integral_0^1 1/(2−x^2−y^2) dx dy
      = integral_0^(pi/4) log[2 cos^2(theta)/cos(2theta)] dtheta
      = −integral_0^(pi/4) log(tan(theta)) dtheta
      = integral_0^1 atan(t)/t dt = Catalan < 1.

The first equality is polar integration split at theta=pi/4. The second
follows from double-angle substitution in the sine/cosine log integrals;
the third is t=tan(theta) followed by integration by parts. An endpoint
diagonal is bounded by1/(2−c^2), and adding a fictitious independent uniform
second turn only enlarges this bound to the same two-turn integrand. An
isolated coefficient has inverse1/2<Catalan.
For each pair i!=j, conjugating G by an arbitrary diagonal sign matrix
preserves the law of its independent symmetric off-diagonals. Thus E G^−1
has zero off-diagonal entries. Integrability follows from the diagonal bound
and the positive-definite inequality |(G^−1)_ij|<=sqrt((G^−1)_ii(G^−1)_jj).
The diagonal part and both edge chains give the displayed full-class bound.

## Exact distinction from the failed coercivity route

The all-|c|=1 configurations produce eigenvalues tending to zero with path
length, and neighborhoods have positive probability. Therefore this lemma
coexists with failure of realization-uniform coercivity. It concerns an
expectation of the inverse, not a positive lower bound on every realization.

If measurement noise eta is conditionally centered and has covariance at
most sigma^2 I given both banks, least-squares coefficient noise has
conditional covariance at most sigma^2 G^−1. Consequently its unconditional
covariance is at most Catalan sigma^2 I. The actual noise M(E) from a fixed
off-model matrix E is not conditionally centered independent noise and does
not satisfy this hypothesis automatically. Controlling that correlation is
still required for a fixed-comparator relative-error theorem.

`test_path_global_ls_inverse.py` independently constructs physical path
probes, checks the two-chain Gram law, and reports inverse-moment Monte Carlo
controls. Numerical checks corroborate but do not prove the lemma. No novelty
claim is made; this is a narrow diagnostic for the wider global-LS route.
