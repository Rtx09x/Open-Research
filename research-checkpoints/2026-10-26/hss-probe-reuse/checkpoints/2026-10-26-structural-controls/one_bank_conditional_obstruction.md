# Coherent phase-return obstruction to a uniform one-bank conditional bound

**Status:** exact restricted construction; independent analytic audit PASS
(26 October 2026). A separately written physical full6D covariance verifier
replayed the finite controls, including nonzero active/passive correlation.
It refutes the proposed stronger conditional pure-source gate, NOT the
unconditional scalar six-query theorem, general approximation existence, or
RE02. No novelty is asserted.

## Statement

Fix scalar rank k=1 and any finite width s=d+1 with d>=2. There is no absolute
constant C (independent of depth and prescribed bases) for

    E_Omega[||V e_ad||² | entire Psi] <= C

uniformly, or with one common almost-sure C over all fixed-basis hierarchies.
Indeed the conditional expected pure-source output can grow at least as the
square root of hierarchy depth. A special coherent opposite bank first
provides a large finite witness; continuity extends it to an open,
positive-Haar-probability set of opposite banks at that fixed depth.

## A rational near-lossless pi rotation

For integer m>=3 set a_j=m-j,b_j=j and

    c_j=(a_j²-b_j²)/(a_j²+b_j²),
    s_j=2a_j b_j/(a_j²+b_j²),       j=0,...,m.

These rational unit-circle points go from(1,0) to(-1,0). Let (r_j,t_j) be
the rotation from point j-1 to point j. Every r_j>0, the product of these
2-by2 rotations is exactly -I, and

    1-r_j = 2m² / [(a_j²+b_j²)(a_(j-1)²+b_(j-1)²)] <=8/m².

Consequently the rational number rho=product_j r_j satisfies
rho>=1-8/m and tends to1. Write q=rho²<1.

## One repeated period

Condition the full transpose-complement orientation at every branch boundary
to be the identity. This is a legitimate deterministic opposite bank, though
it is Haar-null as a single point. Only the independent forward orientations
are averaged. Start with the pure ad source x=z=0,||u||²=1,w=0.

Repeat the following physical transfers:

1. A column swap a=0,b=1 with row r=1,t=0.
2. The m row rotations (r_j,t_j), each with a=1,b=0.

Use the already verified normalized equations. During the row-rotation block,
let h=(x-z,w). The vector h rotates orthogonally by -I on its first two
coordinates, while x is multiplied by rho and u's energy by q. No other
coordinates of h are occupied in this construction.

Immediately before a swap, write

    x=-rho xi,       h=(xi,0,...,0),
    U=E||u||²,       A=E xi².

Initially A=0,U=1. At the swap, the emitted ad coefficient is
-(1+rho)xi. The next injecting component alpha has conditional mean zero and
variance ||u||²/d, irrespective of its dependence on xi. The new x and h are
both -alpha in their first coordinate. The returning u first coordinate is
xi; the remaining u coordinates retain the rotated unused components.
After the m rotations the same state form recurs, and exactly

    U_next=q[(1-1/d)U+A],       A_next=U/d.                 (1)

The swap emits expected energy (1+rho)² A. The row block emits two additional
nonnegative terms

    da cost=(1-q) U/d,
    dd cost=(1-q)[(1-1/d)U+A]/d.                          (2)

These statements do not require xi independent of u. Fresh forward rotation
centering and isotropy suffice. Full moment calculations retain all unused
passive coordinates; dropping them would alter(1).

## Exact infinite sum and finite-depth divergence

Because q<1, the two-state system is strictly substochastic. With U_0=1,A_0=0,

    sum U_i=1/(1-q),       sum A_i=1/[d(1-q)].

Thus, including the unit birth coordinate, its infinite expected output is

    1+2/d+(1+rho)/(d(1-rho)),                             (3)

which tends to infinity with m. This limit is only a convenient calculation;
the counterexample is also explicitly finite.

For m>=64, let C=floor(m/32) and T_i=U_i+A_i. From(1), T_(i+1)>=q T_i, and
q>=1-16/m. Hence T_i>=1/2 for i<=C. Since q>=3/4 and d>=2,
U_i>=3/16 for1<=i<=C. For i>=2, A_i>=3/(16d), while
(1+rho)²>=(15/8)². Each such swap therefore emits more than1/(2d).
Already the first C periods give at least (C-2)/(2d) emitted energy, plus
the unit birth. Taking m periods uses m(m+1) ancestor steps and includes this
lower bound, which diverges as Omega(m/d). A terminal root contributes only
additional nonnegative coefficient energy.

`verify_one_bank_conditional_obstruction.py` constructs these rational
rotations, verifies exact product -I and the rho bound, and evaluates the
finite recurrence with Fraction arithmetic through m=128. Reported integer
lower bounds are certified by exact division, not floating comparisons.
`verify_one_bank_phase_cycle_physical.py` separately retains the full
(x,z,w) covariance and passive energy, matching the cycle and all emitted
costs exactly. Advisor code independently retains the entire six-dimensional
state and averages eight actual forward orientation matrices.

## Haar-null point versus a uniform almost-sure bound

At any fixed finite hierarchy, the conditional expected coefficient energy
is a continuous function of its deterministic opposite-bank orthogonal
orientations: the decoder uses row-frame transposes, and its finite second
moment is a finite polynomial in those frame entries. Therefore a strict
large finite lower bound at the identity orientations persists on an open
neighborhood in the product of orthogonal groups. Haar gives that neighborhood
positive measure. The hypothetical uniform almost-sure C is therefore also
refuted by choosing m and finite depth large enough.

The neighborhood's probability may shrink rapidly with depth. No lower
bound on its probability uniform in depth is asserted, so this gives NO
contradiction to the audited UNCONDITIONAL scalar inverse or reconstruction
bounds. The original correlated anchor averages over this opposite bank too;
its fourth-moment treatment remains valid. A proof for arbitrary matrix
anchors must retain that averaging or use a weaker, appropriately weighted
conditional statement.
