# Four-k-query O(L) approximation with known dense HSS bases

**Status: complete argument; independent advisor algebra/conditioning audit
passed on 2026-10-25.** The bases
are prescribed independently of the probes. This is not unrestricted RE-02,
and no novelty claim is made. The argument reuses the consultation's exact
flux identity and central-sign sector decomposition, then adds a one-bank
matrix-covariance bound and a row-wavelet decomposition. It supersedes the
scalar-only draft `scalar_fixed_basis_bound.md`.

## Statement

Fix arbitrary orthonormal nested row and column bases of dimension k on a
binary HSS hierarchy with N=2^(L+1)k and 2k-coordinate leaves. Let C be the
associated fixed-basis **linear** HSS class. Generate two independent square
2k-column tree frames with independent Haar O(k) complement orientations.
Run the fixed-basis Levitt--Martinsson coefficient decoder, using transposes
as local pseudoinverses.

For every fixed real A, at every carried cut ell>=1,

    E S_ell := E(||Y_ell||_F^2+||Z_ell||_F^2) <=20||A||_F^2.  (1)

Initially E S_0=2||A||_F^2. The output B belongs to C and satisfies

    E||A-B||_F^2 <=(20L+3) min_{H in C}||A-H||_F^2.           (2)

Exactly 2k forward and 2k transpose vector products are queried, independent
of depth. The decoder and probe construction use polynomial arithmetic.
All claims concern exact arithmetic, not finite-precision stability.

### Explicit class, probes, and decoder

At a fine level set U=diag(U_i), V=diag(V_i), with each U_i,V_i having
orthonormal k columns in R^(2k). Recursively the class consists of
`U H_coarse V^T+diag(D_i)`, where H_coarse belongs to the coarser fixed class
and `U_i^T D_i V_i=0`; the root class is all 2k-by-2k matrices. These summands
are mutually Frobenius-orthogonal across nodes and levels.

For the forward probe start from root I_(2k). At node i inherit an active
k-by-2k orthonormal-row frame F_i, choose any orthonormal complement C_i, draw
independent Haar H_i in O(k), and set G_i=H_i C_i. Expand the physical local
frame as `V_i F_i+V_i_perp G_i`. Recurse top-down. Build the transpose probe
independently with U_i. Each local 2k-by-2k probe block is orthogonal, and
E[Omega Omega^T]=E[Psi Psi^T]=I follows inductively by complement centering.

After querying A Omega,A^T Psi, use active/detail coordinates at each node:
`D_da=Y_d F^T`, `D_dd=Y_d G^T`, `D_ad=P Z_d^T`, and `D_aa=0`.
Carry `Y_next=Y_a-diag(D_ad)G` and
`Z_next=Z_a-diag(D_da)^T Q`; the retained tests are F,P. At the root use
`B_root=Y_root Omega_root^T`, then synthesize the nested coefficients upward.
The output can be stored as these HSS factors rather than as a dense matrix.

## A. One-bank pure-detail branch lemma, for arbitrary k

Let only one child on every ancestor step have nonzero samples. Express its
samples in complete orthogonal boundary frames:

    Y_c=X F_c+Y G_c,        Z_c=Z^T P_c+W^T Q_c,

with X,Y,Z,W k-by-k. Keep the entire forward/column bank fixed and randomize
only the transpose/row complement orientations. The child's row frames and
the corresponding column frames have representations

    P_c=R P+T Q,         Q_c=H(R_perp P+T_perp Q),
    F_c=A F+B G,         G_c=O(A_perp F+B_perp G),

where both 2k-by-2k block transfer matrices are orthogonal, H is a fresh Haar
O(k) matrix, and O is fixed after conditioning on the forward bank. The
normalized retained transpose coordinate obeys

    Z_next=R^T Z A+R_perp^T H^T W A.                         (3)

The consultation's exact flux projection gives pointwise contraction of

    J=||X-Z||_F^2+||Y||_F^2+||W||_F^2.                     (4)

Start from a **pure transpose-detail state** X=Y=Z=0, W=W0, where W0 is fixed
independently of the row bank. Set c^2=||W0||_F^2. Thus J_t<=c^2 pointwise.

The decisive matrix invariant is

    E[Z_t Z_t^T] <= (c^2/k) I_k                            (5)

in the positive-semidefinite order. It is true initially. Centering of H kills
the cross term in (3), and Haar conjugation isotropizes the noise term. Since
A A^T<=I and ||W A||_F^2<=||W||_F^2<=c^2,

    E[Z_next Z_next^T]
      = R^T E[Z A A^T Z^T] R
        + (E||W A||_F^2/k) R_perp^T R_perp
      <= (c^2/k)(R^T R+R_perp^T R_perp)
      = (c^2/k)I.

This proves (5) by induction, with no commutativity requirement on transfer
blocks. In particular E||Z_t||_F^2<=c^2. Writing C_t=X_t-Z_t and using (4),

    E S_t = E[J_t+2||Z_t||_F^2+2<C_t,Z_t>]
          <=c^2+2c^2+2 sqrt(E||C_t||_F^2 E||Z_t||_F^2)
          <=5c^2.                                         (6)

Exchange query banks for the analogous statement starting from a pure
forward-detail state Y=Y0, X=Z=W=0, with only forward orientations randomized.

### Conditioning justification

The initialization is explicitly **frame-adapted**: a pure detail state means
physical samples W0^T Q_c (or Y0 G_c), not a fixed physical array independent
of its own bank. Its normalized amplitude is independent of the randomized
bank. Along a single ancestor branch, choose each complement gauge using the
fixed transfer completion shown above. Independent Haar orientations in these
gauges have the same conditional tree-frame law. The normalized recurrence
then uses fresh H at each step; its current state depends only on earlier
branch orientations. Conditioning on the opposite complete bank merely fixes
O and does not change this independence. No source outside the branch enters.

This is different from applying a branch lemma to arbitrary contaminated
global samples whose amplitudes already depend on ancestor orientations.

## B. Arbitrary one-bank-independent input

Fix the complete forward tree frame. Let Y0 be any array independent of the
transpose bank and set Z0=0. Then the same carry recursion satisfies

    E_Psi S_cut <=5||Y0||_F^2                              (7)

at every cut. To prove this, decompose the **spatial row coordinates** of Y0
in the fixed orthogonal left hierarchical-wavelet basis: k detail coordinates
per nonroot node and 2k root-active coordinates. Let H_v be the k-by-2k sample
coefficient of a detail block v.

A single such input component has zero row-detail samples at every finer
node. Until its birth node v is compressed, it therefore creates no transpose
data and only undergoes orthogonal active restrictions. At v its carry is

    Y_v=0,        Z_v=-(H_v F_v^T)^T Q_v.

Its normalized state is the pure transpose-detail state of Section A, with
W0=-H_v F_v^T and ||W0||_F^2<=||H_v||_F^2. Equation (6) bounds every subsequent
ancestor energy by 5||H_v||_F^2.

The contributions of different wavelet blocks are orthogonal **in expected
output sample energy**. Extract an independent central Rademacher sign tau_v
from the Haar complement at v. After its emission, the entire contribution
from v is tau_v times a function of ancestor orientations only: the remaining
coarser decoder does not use tau_v. For two distinct blocks, take the deeper
one if they are nested; if disjoint, take either. Its own sign is absent from
the other contribution and kills the cross term. This also separates emitted
details from un-emitted coarser details and from root-active data. Un-emitted
details remain orthogonal in their spatial row coordinates; root-active data
carry without loss. Summing their input squared norms proves (7).

The argument works for block wavelets, since their central signs multiply the
whole k-by-2k source. It does not require entrywise sign independence. The
symmetric independent-bank statement follows by exchanging roles.

## C. Bound each exact fine-sign sector

At a fine level, transform A into active/detail coordinates and write its
blocks A_aa,A_ad,A_da,A_dd. Diagonal k-by-k blocks of ad,da,dd have zero effect
on the subsequent carry: their contributions cancel exactly by local frame
orthogonality. Only aa and the off-diagonal parts need be considered.

Write G_j=sigma_j Gbar_j and Q_i=tau_i Qbar_i. The fine-sign characters of the
carried data are 1 for aa, sigma_j for ad column j, tau_i for da row i, and
sigma_j tau_i for an off-diagonal dd block (i,j). All subsequent linear carry
maps depend on coarser frames only, not on these signs. Therefore distinct
sectors are orthogonal in expected energy. The following bounds are for each
**whole** ad-column/da-row sector, not for isolated entries whose cross terms
would otherwise be uncontrolled.

### C1. An ad block-column

Let A_j=A_ad[:,j] have zero jth block and let J_j inject one block. Its carry is

    Y=(A_j-J_j B_j)G_j,       Z=0,       B_j=P_j P^T A_j.    (8)

Split the right side into two linear sources.

* Conditional on the entire forward bank, A_j G_j is independent of the
  transpose bank, and ||A_j G_j||_F=||A_j||_F. Apply (7): its energy at any
  later cut is at most 5||A_j||_F^2 in expectation.
* Conditional on the entire transpose bank, B_j is deterministic. The second
  source is a **single pure forward-detail boundary source** at j, with
  normalized amplitude -B_j. Apply the bank-exchanged (6), not (7), averaging
  the forward bank. Its energy is at most 5||B_j||_F^2. Moreover,

      E||B_j||_F^2 <=E||P^T A_j||_F^2=||A_j||_F^2,

  since P_j has operator norm one and E[P P^T]=I for tree frames.

The triangle inequality in the Hilbert space of random sample pairs gives

    E S_sector <=(sqrt(5)+sqrt(5))^2||A_j||_F^2
               =20||A_j||_F^2.                             (9)

This handles the correlated anchor correction by conditioning on the
**opposite** bank; it never declares B_j independent of its own bank.
The da-row argument is the transpose-symmetric version.

### C2. An off-diagonal dd block

For M=A_dd[i,j], i!=j, the carry is the sum of

    Y_j=-(P_j Q_i^T M)G_j,       Z=0,
    Z_i=-(F_i G_j^T M^T)Q_i,     Y=0.                       (10)

For the first source fix the transpose bank and apply pure-forward-detail
bound (6); for the second fix the forward bank and apply its transpose
version. Their amplitudes have Frobenius norm at most ||M||_F, because the
frame products have operator norm at most one. Each costs at most5||M||_F^2;
the same Hilbert-space triangle inequality gives20||M||_F^2 for their sum.

Fine central signs removed in the sector decomposition may be reintroduced:
each multiplies a whole source and leaves its squared energy unchanged.
Thus the complete boundary-detail frame law needed in (6) is legitimate.

### C3. Recursive aa sector

Its carry is precisely A_aa F,A_aa^T P, the original consistent two-bank data
on the coarser fixed hierarchy. At the initial coarse cut the expected energy
is2||A_aa||_F^2; later cuts satisfy (1) by induction. Sector energies add and
their input squared norms sum to at most||A||_F^2. Taking the maximum constant
20, not a sum of constants across levels, proves (1) for **all** A.

## D. Approximation guarantee

The decoder is linear, exact on C, and outputs an element of C. Put E=A-P_C A.
The lifted local discrepancy spaces and the root core are mutually
Frobenius-orthogonal. Therefore

    ||A-B||_F^2=||E||_F^2+||R(E)||_F^2.

At every nonroot level the local discrepancy energy is at most the incoming
sample energy: dda and ddd together use exactly the forward-detail energy
because [F_i;G_i] is square orthogonal, and dad uses at most the transpose-
detail energy. The first incoming cut costs2||E||_F^2 in expectation. The
remaining L-1 local cuts and the root core each cost at most20||E||_F^2 by (1).
Specifically the root decoder is `B_root=Y_root Omega_root^T`, with square
orthogonal Omega_root, so its Frobenius norm equals||Y_root||_F and is at most
the square root of S_root. No ill-conditioned root inverse is used.
Thus E||R(E)||_F^2<=(2+20L)||E||_F^2, proving (2).

## Scope and remaining questions

This would close the known-dense-basis coefficient robustness gap with a
nonsharp absolute constant, but **not** the original unknown-basis problem.
The prescribed bases must be available before the specialized probes are
generated; they cannot be learned from the same prequeried bank and then
declared independent. No constant-factor fixed-basis approximation is proved:
the final coefficient errors are still summed over L levels. Multiplying this
O(L) guarantee by an O(L) basis-selection guarantee gives O(L^2), not RE-02.

The rank-independent covariance argument requires genuine Haar isotropy (or
a correctly coupled isotropic complement law), not merely independent central
signs times arbitrary fixed k-by-k rotations. Central signs alone suffice for
the sector/wavelet orthogonality, not for matrix invariant (5).

Conditional use after a separate training transcript is valid only with fresh
independent reconstruction frames. Training queries must be added to4k, and
the theorem compares to the resulting fixed class. See
`common_optimum_target.md` for a birth-level weighted oracle bound and the
remaining common-OPT question; no unproved learned-basis guarantee is hidden.
