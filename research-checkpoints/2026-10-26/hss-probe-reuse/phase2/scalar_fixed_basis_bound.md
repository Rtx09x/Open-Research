# A scalar dense fixed-basis O(L) bound from one-bank transport

**Superseded by `fixed_basis_bound.md`, which supplies the rank-independent
Haar covariance extension.** Retained as a scalar derivation checkpoint.
**Status: derived proof for independent audit.** This is a restricted k=1
theorem, not unrestricted RE-02. It uses prescribed, independently fixed dense
nested bases and four total matvecs. No claim for general k is made here.
The local flux identity and the fine sign-sector decomposition are reused
from the Pro consultation and were independently algebra-audited.

## Main claims

Use the fixed-basis LM coefficient decoder with square two-column tree frames
in each bank, independently randomized by complement signs. For every fixed
real A and every carried cut ell,

    E (||Y_ell||_F^2 + ||Z_ell||_F^2) <= 20 ||A||_F^2.       (U)

At the initial cut the stronger identity `E S_0=2||A||_F^2` holds.
Consequently, with L nonroot compression levels and fixed-basis linear class C,
the output B lies in C, has HSS rank at most one, and satisfies

    E ||A-B||_F^2 <= (20 L + 3) min_{H in C} ||A-H||_F^2.    (H)

The query count is two forward plus two transpose matvecs, independently of
depth. Constants are deliberately loose. The comparator is the fixed linear
class, not the best unknown-basis rank-one HSS matrix.

## Lemma 1: one random bank, one pure-detail branch, factor five

Normalize an isolated child's samples in its two complete boundary frames:

    Y_c=x F_c+y G_c,        Z_c=z P_c+w Q_c.

Let the column/forward bank be completely fixed; randomize only the row/
transpose complement orientations. Start with `x=y=z=0,w=c`. Row and column
transfer coefficients satisfy `r^2+t^2=a^2+b^2=1`. The scalar branch updates
from the consultation imply

    z_next = r a z - t a tau w,

up to immaterial complement-sign conventions, where tau is the fresh row-bank
sign attaching this child to its parent. Column signs are fixed. The exact
flux energy

    J=(x-z)^2+y^2+w^2

contracts **pointwise** on a single live branch. Thus `J_t<=c^2` at every
ancestor, in particular `w_t^2<=(c^2)` and `(x_t-z_t)^2<=c^2`.
Conditionally centered independent tau gives

    E z_next^2 = a^2 (r^2 E z^2 + t^2 E w^2) <= c^2

by induction from z_0=0. Therefore

    E S_t = E[J_t + 2 z_t^2 + 2(x_t-z_t)z_t]
          <= c^2 + 2c^2 + 2 sqrt(E(x_t-z_t)^2 E z_t^2)
          <= 5c^2.                                         (B)

Freshness is valid because normalized branch states depend only on previous
row-bank signs along that branch, whereas the next row sign is independent;
the other bank is fixed. A pure boundary-detail source has no outside-source
dependence that would violate this statement. Exchanging banks gives the same
bound for a pure forward-detail source with only forward signs averaged.

The number five cannot be improved for this one-bank statement. A first row
swap / column identity maps a pure w=1 source to a pure retained z=1 source
(up to sign). Follow it by m row identities and fixed column rotations through
delta=pi/m, with consistent forward orientation. If a=cos(delta), then

    S_m = 1 + 2 a^(2m) + 2 a^m -> 5.

Thus the failure of the sharper constant-one guess is **bounded transient
gain**, not growth without bound in depth. This sharpness concerns arbitrary
one-bank sample transport, not a sharp constant in (U) or (H).

## Lemma 2: one-bank-independent arbitrary input, factor five

Fix the entire forward tree frame. Start the fixed-basis carry recursion with
any Y0 independent of the transpose bank and Z0=0. Then at every cut

    E_Psi S_cut <= 5 ||Y0||_F^2.                             (T)

Decompose the rows of Y0 in the orthonormal **left hierarchical wavelet basis**:
one detail coordinate for every nonroot node and two final root actives. Each
row coefficient is a two-entry sample vector h_v. This is a spatial row-basis
decomposition; the forward test realization remains fixed.

For a single detail component at node v, every finer row compression sees zero
row-detail data, hence creates no transpose data or coefficient correction.
When v is compressed, Y_active=0 and Y_detail=h_v. The carry emits

    Y_v=0,       Z_v=-(h_v F_v^T) Q_v.

Its normalized state is precisely a pure transpose-detail source with
`c=-(h_v F_v^T)` and `c^2<=||h_v||^2`. Lemma 1 bounds all later branch energies
by `5||h_v||^2`. Before its emission, the component is simply carried through
orthogonal active row restrictions, with unchanged norm.

Different detail components are orthogonal **in expectation** at each cut.
For a component already emitted at v, its entire later contribution is
`tau_v` times a function of ancestor signs: the remaining coarser decoder
does not use tau_v. A coarser component has not used tau_v at all; a component
in a disjoint subtree also does not use it. For an ancestor/descendant pair,
average the finer component's own sign. Thus every cross term between
distinct emitted components, or emitted and un-emitted components, vanishes.
The un-emitted components remain mutually orthogonal in their spatial row
coordinates. Root-active components carry without loss and do not depend on
any row-bank signs. Summing the squared row coefficients proves (T).

This argument also proves the symmetric statement with query banks exchanged.
It is stronger than the isolated-branch estimate alone and uses the particular
independent-bank initialization. It does not claim one-step monotonicity.

## Lemma 3: bound every fine sign sector by twenty

At a fine level write A in active/detail coordinates as aa,ad,da,dd. The block
diagonals of ad,da,dd make **zero** contribution to the subsequent carry, by
local frame orthogonality. They can therefore be omitted when proving (U).
Use the consultation's exact central-sign sector expansion for the remaining
blocks. Distinct sectors are orthogonal in expected carried energy.

### One ad column j

Let a=A_ad[:,j] with a_j=0. Its carried pair is

    Y=(a-e_j b)G_j,       Z=0,       b=P_j P^T a.

Split it into the direct term and the anchor correction.

* **Direct term:** conditional on the complete forward bank, `a G_j` is
  independent of the transpose bank. Lemma 2 bounds its energy at any later
  cut by `5||a||^2`.
* **Anchor term:** conditional on the complete transpose bank, b is a fixed
  scalar. The data `-e_j b G_j,0` are a single **pure forward-detail boundary
  source**. Apply the bank-exchanged Lemma 1, averaging the forward bank, to
  get at most `5b^2`. Moreover,

      E b^2 <= E ||P^T a||^2 = ||a||^2,

  because P_j has unit norm and the tree frame is isotropic: E[P P^T]=I.

The triangle inequality in the Hilbert space of random carried arrays yields
`E S <= (sqrt(5)+sqrt(5))^2 ||a||^2 = 20||a||^2`.
This swaps conditioning rather than incorrectly pretending the anchor
amplitude is independent of its own bank. The da-row bound is symmetric.

### One off-diagonal dd block (i,j)

For scalar M=A_dd[i,j], the carried pair is the sum of two sources:

    Y_j=-(P_j Q_i^T) M G_j,       Z_i=-(F_i G_j^T) M Q_i.

For the first, condition on the transpose bank and use the pure forward-detail
branch estimate; for the second, condition on the forward bank and exchange
banks. Each expected energy is at most `5 M^2`, since the displayed inner
products of unit frames have magnitude at most one. The same Hilbert-space
triangle inequality gives `20 M^2` for their sum.

The fine central signs can be retained or integrated first. A removed sign
multiplies an entire source and has no effect on its squared energy; it may
be reintroduced when invoking the boundary-detail branch law.

### The aa sector and induction

The aa carried pair is exactly `A_aa F,A_aa^T P`, the original problem on a
smaller fixed hierarchy. At the initial coarse cut its expected energy is
`2||A_aa||^2`; at later cuts apply induction. The orthogonal sector energies
add, and their input squared norms sum to at most `||A||^2`. Taking the maximum
sector constant, rather than summing constants over levels, proves (U).

## From uniform carried energy to approximation error

The decoder is linear and exact on C. For E=A-P_C A, output coefficients lie
in C and the lifted local discrepancy spaces and the root core are mutually
Frobenius-orthogonal. Hence

    ||A-B||^2 = ||E||^2 + ||R(E)||^2.

At each nonroot level, the squared norm of its discrepancy coefficient is at
most the incoming carried energy: dda and ddd partition the forward detail
sample energy, and dad uses at most the transpose detail energy. The first
incoming cut has expected energy `2||E||^2`; the other L-1 cuts and the root
core each cost at most `20||E||^2`. Thus

    E||R(E)||^2 <= (2+20L)||E||^2,

which proves (H). All random variables are finite polynomials in bounded frame
entries, so expectation and conditioning manipulations have no tail issue.

## Limitations requiring explicit retention

* k=1 is essential in the current branch second-moment induction. For matrix
  blocks, scalar convexity of `r^2 Ez^2+t^2 Ew^2` does not immediately survive
  noncommuting transfer blocks. No rank-independent general-k extension is
  claimed.
* Bases must be prescribed independently before the four probes are generated.
  The unknown-basis HSS optimum and reused-sketch learning barrier remain.
* Combining this O(L) fixed-basis factor with an O(L) basis-selection factor
  would still give O(L^2), not the requested unrestricted RE-02 theorem.
