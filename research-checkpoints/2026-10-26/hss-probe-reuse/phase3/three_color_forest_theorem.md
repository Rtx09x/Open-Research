# Six-k-query, factor-two approximation on a known block forest

**Status:** proved below, independently algebra-audited, and exhaustively tested.
The parent forwarded this candidate from a still-running Pro consultation; this
document is an independent derivation, not a claim to originate the idea.
This improves the earlier four-k-query / diameter-factor restricted result by
spending two additional k-column query groups. It does **not** solve RE-02.

## Theorem

Partition N=Mk coordinates into M blocks of size k. Let T be any **known rooted
forest** on the blocks, with parent p(i) or no parent, and depth d(i). Let F_T be
the linear class with arbitrary diagonal blocks and arbitrary blocks in both
orientations of each forest edge; all other blocks vanish. For every fixed real
A, a nonadaptive randomized algorithm uses exactly 3k forward and 3k transpose
vector products and returns B in F_T satisfying

    E B = P_T A,
    E ||A-B||_F^2 <= 2 min_{H in F_T} ||A-H||_F^2.

Here P_T is support masking. The query bound and approximation factor are
independent of M, depth, maximum degree, and number of components. Apart from
the matvecs, construction and decoding take O(M k^2) arithmetic and storage.
The implementation may skip unused query columns, but 6k is a valid uniform
every-execution bound. No symmetry, random-noise, or small-perturbation
assumption is made. Statements are in exact arithmetic.

## Algorithm

Set c(i)=d(i) mod 3. Choose independent Rademacher signs sigma_i and tau_i.
Build N-by-3k probes with block rows

    Omega_i[:, color slot c(i)] = sigma_i I_k,
    Psi_i[:, color slot c(i)]   = tau_i I_k,

and zero entries in other slots. Query Y=A Omega and Z=A^T Psi. Set unsupported
blocks of B to zero and decode

    B_ii       = sigma_i Y_i,c(i),
    B_i,p(i)   = sigma_p(i) Y_i,c(p(i)),    if i is not a root,
    B_p(i),i   = tau_p(i) Z_i,c(p(i))^T,   if i is not a root.

The three formulas write disjoint output blocks. A row's supported blocks are
its diagonal, its unique parent, and its children. Their colors are c(i),
c(i)-1, and c(i)+1 modulo 3. Thus each queried slot used in decoding contains
**exactly one supported target**, regardless of how many children exist.
The transpose formula uses the corresponding statement about columns.

## Exact error identity

Let H=P_T A and E=A-H. Exact recovery on F_T follows directly from the previous
paragraph. For general A the coefficient errors are

    B_ii-H_ii = sum_{j:c(j)=c(i)} sigma_i sigma_j E_ij,

    B_i,p(i)-H_i,p(i)
       = sum_{j:c(j)=c(i)-1} sigma_p(i) sigma_j E_ij,

    B_p(j),j-H_p(j),j
       = sum_{i:c(i)=c(j)-1} tau_p(j) tau_i E_ij.

Supported E blocks are zero, so including them in the displayed sums is
harmless. Within each one of these coefficient errors, squared-norm expansion
and E[sigma_j sigma_l]=delta_jl (or the tau analogue) kill all cross-source
terms. This holds for arbitrary real k-by-k blocks: the cross term is their
Frobenius inner product times the same centered scalar sign product. The
common prefactor sigma_i or sigma_p(i) has square one. Every coefficient has
mean zero because its potential uncentered source is a supported zero block.

Different output blocks are Frobenius-orthogonal, so their errors add
**without needing independence across coefficients**. Also A-H is supported
off the output support. Consequently

    E ||A-B||_F^2 = sum_{(i,j) off support} (1+w_ij) ||E_ij||_F^2,

where

    w_ij = 1[c(j)=c(i)]
         + 1[i is not a root and c(j)=c(i)-1 mod 3]
         + 1[j is not a root and c(i)=c(j)-1 mod 3].

The three cases require color differences 0, -1, +1, respectively, and are
mutually exclusive modulo 3. Therefore w_ij is either zero or one. This proves
the theorem, including same-color diagonal leakage without double counting.
There is no propagated residual subtraction and no tree-flow solve.

The sigma and tau families may in fact be the **same** family: each variance
calculation involves only one family, and cross-output covariance is irrelevant.
Both query directions still count, totaling 6k for an arbitrary nonsymmetric A.

## Immediate consequences and exact scope

* Averaging r independently signed outputs gives exact expected error
  `||E||^2 + (1/r) sum w_ij ||E_ij||^2`, hence factor `1+1/r` with `6kr`
  total queries. There is no log(M) factor for this fixed forest class.
* If A is known symmetric, use the same sign family and reuse Y as Z. The
  bound then needs only 3k forward queries. Optional symmetrization cannot
  increase Frobenius error against symmetric A.
* The factor 2 is sharp for this decoder. On a four-vertex path rooted at an
  endpoint, take A=e_0 e_3^T. Its off-support entry has same-color endpoints,
  and every sign realization produces one unit diagonal error in addition to
  the unit omitted entry. Thus the squared error is exactly 2, whereas the
  fixed-tree optimum is 1.
* The same input is globally rank one, hence is rank-one HSS with optimum
  zero. This is a direct warning that replacing the fixed-tree comparator by
  the full HSS comparator is invalid.
* For the original dyadic representative tree (recursively join consistent
  first-block representatives), every dyadic interval has just one k-block
  incident to all edges leaving it. Its fixed support therefore lies in the
  requested rank-k HSS class. An **arbitrary** forest need not have this HSS
  property on an unrelated prescribed dyadic partition.
* Known independently fixed dense nested bases are not covered by this proof.
  Learning unknown bases from the same probes is a further unresolved issue.

## Verification

Run from this directory:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python verify_three_color_forest.py

The verifier enumerates all 125 labeled rooted forests on four vertices, k=1
and k=2, and all independent forward/transpose sign assignments. Additional
five-vertex paths, stars, disconnected forests, relabelings, and k=3 cases
include exactly supported matrices. All arithmetic in these tests is integer;
the exact total squared errors and exact output means are checked, not merely
Monte Carlo estimates. The decoder itself receives only vector-product
callables, and the test checks exactly 3k calls in each direction on every run.

## Prior art / novelty

The underlying mechanism is **direct star bicoloring**, an established sparse
matrix recovery method. Depth-mod-three is a star coloring of a rooted forest.
Randomly signed coloring is also established. This note verifies the precise
off-support leakage identity and its consequence for this class; it does not
claim either mechanism is new. See `literature_phase2.md` for the comparison.
