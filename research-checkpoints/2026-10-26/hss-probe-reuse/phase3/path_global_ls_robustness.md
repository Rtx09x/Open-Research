# Generic wider global LS: a correlated-noise bound for a scalar path

**Status:** restricted theorem; independent advisor analytic audit passed.
Not RE02, not a new best path/forest algorithm. The established three-color
forest decoder already has a stronger6-query/factor2 guarantee. This result
instead closes the actual off-model noise correlation for a different,
generic Markov-frame global least-squares decoder.

## Theorem and algorithm

Let C be the real matrix class supported on the diagonal and both directions
of a known path on n vertices. In each independent probe bank of width5,
choose a Haar orthonormal initial pair, then choose each succeeding row
uniformly on the unit sphere perpendicular to its predecessor. (For n=1 use
a uniform unit row.) Query A Omega and A^T Psi: exactly10 scalar matvecs.
Return the unique least-squares minimizer over C of

    ||(A−B)Omega||_F^2 + ||(A−B)^T Psi||_F^2.

Then in exact arithmetic

    E||A−B||_F^2 <= 85 min_{H in C}||A−H||_F^2.

The comparator is the fixed support class only. No rank-learning assertion
or implementation-complexity improvement is claimed.

## 1. Measurement Gram and its inverse-square diagonal

On the supported matrix-unit coefficient basis, G=M^*M splits into isolated
diagonal-coefficient entries2 and two tridiagonal directed-edge chains with
diagonal2. Along either chain the off-diagonals c_i are iid first coordinates
of a uniform vector on S^3. This follows by conditioning sequentially on the
preceding Markov probe rows; forward and transpose turns alternate. See the
full scalar path Gram derivation in `path_global_ls_inverse.md`.

The moments needed here are

    rho=E c^2=1/4,
    a=E(1−c^2)^−1=2,
    b=E[c^2/(1−c^2)]=1.

For example c^2 has Beta(1/2,3/2) law, so its beta-integrals give these values.
Every finite chain is positive definite. Its left and right elimination
pivots d=2−c^2/d_prev are greater than1. Scalar Schur complementation yields

    (G^−1)_jj <= 1/[(1−c_(j−1)^2)+(1−c_j^2)].

If j is an endpoint, introduce one fictitious independent turn with the same
law: subtracting its nonnegative square in the denominator only enlarges
the bound. The chain with a single coefficient has inverse1/2 and can be
handled separately.

Left elimination of column j gives, for i<j,

    |(G^−1)_ij|
       = product_(t=i)^(j−1) (|c_t|/d_t) · (G^−1)_jj
       <= product_(t=i)^(j−1)|c_t| · (G^−1)_jj.

Right elimination gives the corresponding formula for i>j. Squaring the
diagonal bound and using (u+v)^2>=4uv gives

    E[(G^−1)_jj^2] <= a^2/4 = 1.

For distance r=|i−j|>=1, the product contains one neighbor turn of j and r−1
other turns. They are independent. The same bound consequently gives

    E[(G^−1)_ij^2] <= (ab/4)rho^(r−1)
                            = (1/2)(1/4)^(r−1).

Summing both sides of j proves the uniform inverse-square diagonal bound

    E[(G^−2)_jj] = sum_i E[(G^−1)_ij^2] <= 7/3.       (1)

This argument does NOT assume independence between an inverse and its RHS.
It bounds the entire relevant inverse column before a noise RHS is inserted.

## 2. A single off-support matrix unit, including its correlated RHS

Let E=e_i e_j^T be off support. Its queried samples have only forward row i
and transpose row j nonzero. Thus b=M^*M(E) is supported on at most six
coefficient coordinates: the diagonal and up to two path-edge variables in
row i, and the diagonal and up to two path-edge variables in column j.
These two sets are disjoint because (i,j) is not a supported coefficient.
Each b_alpha is an inner product of two unit probe rows, so |b_alpha|<=1.
The coefficient vector returned by LS is x=G^−1 b. Pointwise, even though b
and G are correlated,

    ||x||^2 <= p sum_(alpha in supp b) |b_alpha|^2 ||G^−1 e_alpha||^2
            <= 6 sum_(alpha in supp b) ||G^−1 e_alpha||^2,

where p<=6. Using (1) on at most six columns yields E||x||^2<=84.
The output is supported in C whereas E is orthogonal to C; hence the total
expected squared error on this unit input is at most85.

## 3. Exact sign-gauge diagonalization, not a triangle bound over entries

The joint law of the rows of a Markov bank is invariant under arbitrary
independent sign flips of its physical rows. The initial Haar orthonormal
pair has this symmetry, and the transition kernel depends only on the
preceding row's orthogonal complement, which is unchanged by its sign.
The forward and transpose banks are independent. Consequently the probe
law is invariant under (Omega,Psi)->(D_c Omega,D_r Psi) for any two diagonal
sign matrices D_c,D_r.

The support class is invariant under B->D_r B D_c. Least squares is equivariant:

    R_(D_c Omega,D_r Psi)(D_r A D_c)
       = D_r R_(Omega,Psi)(A) D_c.

Thus Q(A)=E||R(A)||^2 is a quadratic form invariant under independent row and
column signs. Its cross coefficient between distinct physical matrix units
must vanish: a row or column sign distinguishes the two units. This step is
why summing the unit-input bound does NOT incur the number of matrix entries.

For arbitrary E orthogonal to C,

    E||R(E)||^2 = sum_(off support i,j) E_ij^2 E||R(e_i e_j^T)||^2
                <=84||E||_F^2.

The decoder is linear and exact on C because G is positive definite. Writing
A=P_C A+E, the residual E is orthogonal to the reconstructed supported error.
This proves the displayed factor85 theorem.

## Boundaries of a lift to the actual HSS problem

* A branching tree has clique interactions among all edges incident at a
  high-degree vertex; its Gram is not the tridiagonal chain used in (1).
* In a dense nested-basis class, a physical matrix unit can excite many tied
  hierarchical coefficients; the six-coordinate RHS support bound is false.
* Independent physical row/column sign flips generally do not preserve dense
  prescribed nested bases. The exact gauge diagonalization in section3
  therefore cannot be imported into the dense model.
* None of these observations is an impossibility result for wider dense
  global LS. A tied-tree matrix-valued resolvent/noise argument would be a
  materially new step. The path calculation only demonstrates that the
  correlated off-model RHS can be handled without pointwise coercivity.


## Reproducibility

`verify_path_ls_gauge_exact.py` is a Fraction-only N4,width5 control with
unrelated rational banks. It verifies physical Gram construction, exact
on-model inversion, the six-coordinate RHS bound, and the entire256-element
row/column sign average exactly. It is not a substitute for the continuous
inverse-moment argument. `test_path_global_ls_robustness.py` gives additional
200-draw numerical checks for n=4,8,16,32; empirical unit-input error factors
are about1.30--1.43 and on-model errors below7e-16. These are diagnostics, not
proof constants or claims about the worst full HSS input.
