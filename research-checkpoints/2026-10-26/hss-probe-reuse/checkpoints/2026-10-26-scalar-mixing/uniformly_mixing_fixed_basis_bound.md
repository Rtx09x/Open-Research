# Arbitrary-rank constant-risk reconstruction for uniformly mixing fixed bases

**Status:** complete restricted proof; independent analytic advisor audit PASS
(26 October 2026). Exact finite controls corroborate the local algebra; they
are not a substitute for the all-depth proof.
This permits genuine interlevel channel mixing but assumes uniformly
nondegenerate transfers. It is not arbitrary prescribed bases or full RE02.

## Statement and probe law

Fix real orthonormal nested left/right rank-k bases before any probes. Assume
that every k-by-k child active transfer has singular values in
[delta,sqrt(1-delta²)] for a fixed delta>0 (necessarily delta<=1/sqrt2).
Equivalently, on either bank and either branch, the active block R or A has
operator norm<=rho=sqrt(1-delta²), and its complementary block T or B has
smallest singular value>=delta. Let C_fixed be this prescribed linear class.

Use two independent width-s tree-frame banks with s=3k,d=s-k=2k and the
explicit full-completion construction below. The local coefficient decoder
uses exactly s A-products and s A^T-products and forward root decoding.
Define

    c2=delta^4(1-k/d),
    Bcond=(2/c2)[1+2/(1-rho²)²]
         =4 delta^(-4)+8 delta^(-8)        when d=2k.

Then for every deterministic real A,

    E||R(A)||_F² <=(4+4Bcond)||A||_F²,
    E||A-R(A)||_F² <=(5+4Bcond) min_(B in C_fixed)||A-B||_F².    (1)

Thus the factor is5+16delta^(-4)+32delta^(-8), independent of k and depth.
For example delta=1/2 gives8453 with6k TOTAL products. Constants are crude.
No rank inflation, entry queries, per-level probes or learning oracle is used.

### Explicit complete frames and independence

At a node, write the complete s-row observation frame as [F;G;J], with row
counts k,k,d-k. The two child active frames are obtained by applying the
prescribed orthogonal2k-by2k transfer to [F;G]. For each child independently,
its canonical full passive complement consists of the sibling active frame
followed by J. Rotate this d-row complement by a fresh independent Haar H in
O(d); its first k rows are that child's detail frame and its remaining rows
are its unused complement. At the top, start with the first2k rows of I_s as
the two root active frames and use the other root active frame plus unused
coordinate rows as each canonical complement. The two full banks are independent.

This description also supports the separately stated finite-orientation
variant, but no arbitrary unrelated choice of complement gauges is assumed.

## 1. Conditional pure-source reverse law

Condition on the ENTIRE construction of the opposite bank, including all its
full-complement orientations. A coefficient source matrix M may depend on
this conditioned bank, but not on the injecting bank. Its normalized initial
carry is pure passive: either Y=-M[I_k 0] or W=-[I_k;0]M, with X=Z=0.

Moving to the parent, the child's full orientation is the only newly used
orientation of the injecting bank. In the explicit full-frame coordinates,
the parent's complete physical frame cancels from the sample-subtraction
identities. The normalized update therefore depends only on the incoming
state, the fixed prescribed transfer, this child's independent orientation,
and the conditioned opposite orientation. Inductively the state uses only
already-revealed injecting-bank orientations below the current boundary;
it does not depend on any unrevealed injecting ancestor orientation. This
proves genuine reverse-order freshness after conditioning the entire opposite
bank. The initial M is deterministic under that conditioning.

This is NOT an independence assertion about arbitrary off-model physical
sample arrays. It applies to the specified pure coefficient source, whose
frame-adapted normalization removes the unknown ancestor frames exactly.

## 2. Two-step flux contraction with only one fresh bank

Use the exact matrix recursion in `matrix_branch_flux_reduction.md`. Let
D=X-Z and Hflux=||D||²+||Y||²+||W||². Condition the transpose bank, and average
only the forward complement orientation. The opposite rotated blocks Wbar,
What are deterministic given the current state and conditioned construction.
Set

    N=R^T D-R_perp^T Wbar,
    Mrow=T^T D-T_perp^T Wbar.

Orthogonality of the row transfer gives

    Hflux=||Y||²+||N||²+||Mrow||²+||What||².               (2)

The exact flux-loss identity and centered isotropy of the forward rotation
imply, with a=delta²(1-k/d),

    E[first loss | state]
      >=a||Y||²+delta²(||Mrow||²+||What||²).              (3)

Indeed the exact first loss is
||Mrow B||²+(1-||B||_F²/d)||T^T Y||²+||What B||².
The next passive forward block satisfies

    Y'_G=N B+R^T Ybar B_perp,

and its cross term is centered. Thus E||Y'||²>=delta²||N||².
At the following boundary the fresh forward rotation again gives expected
loss at least a||Y'||², regardless of the fixed opposite bank. Adding this
to(3) and using(2) yields

    E[Hflux_(l+2) | state_l] <=(1-c2)Hflux_l,
    c2=a delta².                                        (4)

Pointwise Hflux is nonincreasing at every step. Therefore every finite
horizon, INCLUDING its terminal root cut, obeys

    sum_l E Hflux_l <=(2/c2)Hflux_0.                     (5)

There is no need for a nonexistent final second step: pair consecutive cuts
and use pointwise contraction for an unpaired terminal cut.

The transpose-fresh version follows by the exact symmetric calculation:
let N=D A+Ybar A_perp and Mcol=D B+Ybar B_perp. The first loss controls W,
Mcol,Yhat; the next W'_Q=-T^T N+centered noise supplies the missing N term.
The same c2 and(5) hold with the whole forward bank conditioned.

## 3. Common mode, emitted coefficients, and conditional source bound

Let C=(X+Z)/2. Its update is C'=R^T C A+xi, where pointwise

    ||R^T C A||<=rho²||C||,
    ||xi||²<=Hflux/2.

These inequalities need no opposite-bank centering. The elementary l2
convolution bound for this stable recurrence gives

    sum_l ||C_l||²
      <=2||C_0||²/(1-rho^4)
          +[1/(1-rho²)²] sum_l Hflux_l.                 (6)

The emitted coefficient energy is at most
J=||X||²+||Z||²+||Y||²+||W||²<=2||C||²+Hflux POINTWISE.
For da/dd together this is orthogonality of the column transfer applied to
T^T[X,Ybar]. For ad, the map [Z;Wbar]->R^T Z+R_perp^T Wbar is a contraction,
as is right multiplication by B. The forward root decoder is a contraction
at its own terminal cut and is also bounded by that cut's J.

A pure passive source has C_0=0,Hflux_0=||M||². Equations(5)-(6) prove

    E_own[||strict-ancestor/root response||² | other bank]
        <=Bcond||M||².                                 (7)

Including its orthogonal local birth coefficient gives1+Bcond. This bound
is uniform in the conditioned opposite construction and its measurable M.
The uniform-mixing assumption is essential: the separately audited coherent
phase-return example refutes(7) without it.

## 4. Whole matrix wavelet-source input

At any cut let Y=Aq,Z=0, with deterministic spatial matrix A and q a row-
orthonormal k-by-s matrix depending only on the forward bank (possibly a
finer detail frame). Decompose A into its prescribed orthonormal row-wavelet
blocks A_v and the root-active block. At birth v, the output is

    V_(da,v)(A_v q F_v^T) + e_(dd,v)(A_v q G_v^T).

Condition on the complete forward bank. The da source coefficient is now
deterministic, so the transpose-fresh conditional bound(7) applies. Its own
dd coordinate has disjoint coefficient support. Since the two coefficient
squared norms sum to at most||A_v||², the expected birth contribution is
at most(1+Bcond)||A_v||².

For distinct births, choose the deeper birth if nested, or either if disjoint.
Its overlapping strict-ancestor output is linear in its own centered opposite-
bank detail sign; the other birth avoids that draw. The chosen deeper source's own birth supports cannot overlap the other output; every overlap lies
in that deeper source's strict-ancestor response and therefore carries its own
centered sign. The amplitudes depend only on the forward bank.
Thus cross-birth TOTAL coefficient inner products vanish. Root-active terms
are covered by the same cancellation and an orthonormal contraction. Hence

    E||output(Aq,0)||² <=(1+Bcond)||A||².                 (8)

The transpose-input version is identical; forward-only root decoding merely
omits the transpose-only root contribution.

## 5. Correlated anchors and the maximum-sector induction

At a fine cut, a whole off-diagonal ad block column A_j (with its diagonal
block zero) has carry

    Y=(A_j-E_j B_j)G_j, Z=0,       B_j=P_j P^T A_j.

Its first source is bounded by(8). Its anchor is the strict-ancestor ad inverse
response with source B_j, which depends only on the transpose bank. Apply(7)
conditionally, then use the pointwise contraction by P_j and frame isotropy:
E||B_j||²<=E||P^T A_j||²=||A_j||². The two-term squared-norm inequality gives
coarser output at most(2+4Bcond)||A_j||². The da block row is symmetric.

An off-diagonal dd block M has two source amplitudes P_j Q_i^T M and
M G_j F_i^T. Each is measurable in its opposite bank and has norm<=||M||.
Applying(7) separately and the two-term inequality gives coarser cost at
most4Bcond||M||². Diagonal local coefficient blocks have zero carry.

Condition on the coarser frames and extract independent finest central signs.
The complete carried aa, ad-column j, da-row i and dd-block(i,j) sectors have
characters1,sigma_j,tau_i,sigma_j tau_i. Their TOTAL coarser output energies
are orthogonal after this sign average. Norm estimates above are then averaged
under the original full law, not under an altered conditional-source law.
The aa sector is exactly the same consistent problem on the coarser hierarchy.

Fine coefficients have Frobenius-orthogonal support from coarser coefficients;
they vanish for aa input. Their total expected energy is at most twice the
non-aa input energy, using local row-orthonormal projection and global frame
isotropy. Therefore induction takes the MAXIMUM of the coarser constant and
4+4Bcond, not a sum over levels. The root-only base is a contraction. This
proves the first inequality(1). Linearity, range in C_fixed, exactness on it,
and the orthogonal residual identity give the second inequality(1).

## Scope and finite randomness

All banks are generated only after the prescribed bases are available.
Conditioning never covers bases learned from those banks. The theorem does
not construct a query-efficient unknown-basis learner, compare to unrestricted
rank-k HSS OPT, or control floating-point error. Constants diverge as delta
approaches0; this proof does not bridge the general near-coordinate regime.

Every step uses only orthogonality, mean-zero complement orientations, exact
conjugation isotropy, independent banks, and independent central signs. Thus
independent uniform signed-permutation full-complement orientations in the
EXPLICIT sibling/unused-row gauge above give the same theorem. This is a
separate finite probe law, not an assertion that an arbitrary signed-permutation
complement generator has the Haar law. No Haar fourth moment is used here.

## Reproducible controls

`verify_uniform_mixing_two_step_exact.py` uses Fraction arithmetic for k2,s6,
noncommuting rational transfer gauges with delta3/5, a fixed arbitrary
opposite bank, and32-by32 fresh-orientation pairs in each conditional
direction. It separately verifies the design moments, actual physical
sample-subtraction identities, pointwise emission/flux inequalities, and
exact two-step contraction. Runtime was about2seconds on one CPU.

`test_uniform_mixing_fixed_basis.py` implements and counts the actual3k
forward+3k transpose products for k1--4,L1--4,N<=128. Haar and explicitly
gauged signed-permutation laws pass numerical exact-on-class and output-class
checks. Empirical error factors near2.2 are not used as proof.
