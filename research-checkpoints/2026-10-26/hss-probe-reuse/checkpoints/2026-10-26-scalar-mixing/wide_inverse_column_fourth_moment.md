# All-depth fourth moment for a scalar pure-source inverse column

**Status:** complete restricted argument; independent advisor analytic audit
PASS (26 October 2026). Not part of the frozen00:20 addendum. No correlated-noise reconstruction
or unknown-basis theorem is asserted here.

Use prescribed real scalar nested bases, independent full Haar complement
orientations, width s>=3, d=s-1. Let V be the triangular coefficient decoder
inverse from `wide_scalar_inverse_bound.md`. For every deterministic coordinate
unit vector e_j, the conclusion is

    E||V e_j||^4 <= 50000.                         (1)

The constant is deliberately crude and independent of depth and width.
No finite signed-permutation fourth-moment corollary is claimed here.

The proof below uses the already audited reverse-coordinate freshness and
mean-square cone. All expectations refer to the fixed-basis probe law.

## 1. Branch state and a previously established pointwise flux

A da/ad inverse column consists of its unit birth coefficient and one live
ancestor branch. Its initial branch state is pure passive: x=z=0 and either
u=-e_0,w=0 or u=0,w=-e_0. A dd/root inverse column is already a unit vector.

At each upward boundary the independent full-complement rotations are fresh
in normalized coordinates. The state is (x,z,u,w), with U=||u||^2,W=||w||^2.
The distinguished rotated components alpha,beta have independent centered
sphere laws conditional on the incoming state. With r^2+t^2=a^2+b^2=1,

    x'=ra x-rb alpha,       z'=ra z-at beta,
    u'_0=rb(x-z)+ra alpha+bt beta,   u'_rest=r u_rot,rest,
    w'_0=at(z-x)+ar beta+tb alpha,   w'_rest=a w_rot,rest.

The emitted coefficients are

    da=t(a x-b alpha),
    dd=t(b x+a alpha),
    ad=b(r z-t beta).

The flux variables (v=x-z,u,w) evolve without the common mode c=(x+z)/2.
Their squared norm H=v^2+U+W obeys the pointwise identity

    H-H'=(tb v+ta alpha-rb beta)^2
                +t^2(U-alpha^2)+b^2(W-beta^2)>=0.

This is the scalar specialization of the earlier auxiliary flux projection
identity, not a new general contraction. For the pure source, H<=1 pointwise.

The terminal root uses forward root decoding. Its live-row coefficients are
x and one fresh complementary component of u. It is a contraction of Y.
There is no need to use the transpose root estimate in this decoder.

## 2. A uniform mean-square bound from an arbitrary normalized state

For any finite remaining branch and deterministic incoming state, let Z be
the vector of all its emitted coefficients and final root coefficients.
Then

    E||Z||^2 <= 14 (x^2+z^2+U+W).                 (2)

Here is a direct consequence of the previously proved positive four-moment
recursion. A unit pure-passive source has total expected emitted cost<=C_d,
where C_d=(2d-1)/(d-1)^2<=3, and root energy<=1. Its total is<=4.

For an active source x=1,z=0,u=w=0, the first-moment vector is (X,Z,U,W)
=(1,0,0,0), with E[xz]=0. Dominate it componentwise by (1,0,d-1,0), which
belongs to the invariant covariance cone. The recursion and expected cost
have nonnegative coefficients. The dominating vector has energy d, so the
original active source's emitted cost is<=d C_d<=6. For the original source,
E[xz] stays0 and its expected total carried energy is nonincreasing; thus
its root energy is<=1. The same reasoning holds for the z-only source.

The expected output Gram in the two active input coordinates is positive
semidefinite with both diagonal entries<=7, hence operator norm<=14.
Each passive input block is isotropic and has operator norm<=4. Cross terms
between the two passive blocks and between active/passive blocks vanish:
at the first boundary each initial passive block enters linearly through
its own centered fresh orientation, whereas the active-source response is
independent of that first orientation. Subsequent orientations are independent
of it. The two banks are independent. The terminal-root-only case has the
same elementary centering property. This proves(2).

All bounds are uniform over the finite remaining physical transfer sequence.
This is a mean-square bound for normalized states, not a one-step common
quadratic storage inequality (the latter stronger ansatz was disproved).

## 3. Doob differences of the complete output depend only on flux

Reveal independent orientations in the valid reverse-coordinate order. Let
Z denote the complete strict-ancestor/root output vector, padded with zeros
for all other coefficient coordinates. Its Doob martingale is M_i=E[Z|F_i].
For a pure passive source, M_0=0. The deterministic unit birth coefficient
is not included in Z.

At every stage, the conditional expected *future* coefficient vector depends
linearly only on the current x,z. It has no dependence on u,w: the first
unrevealed orientation centers each passive block, and all later mean active
updates are x->ra x,z->ra z. The corresponding two future-response vectors
are deterministic functions of the prescribed remaining transfers.

Consequently, the newly revealed martingale difference has the form

    Delta_i=alpha_i h_i+beta_i g_i,                (3)

where h_i,g_i are deterministic coefficient vectors (including the current
emission and the changed conditional future mean). At the root this is just
one complementary component times a fixed root-coordinate unit vector.
In particular

    a_i=E[||Delta_i||^2|F_(i-1)]
       =(U_i||h_i||^2+W_i||g_i||^2)/d             (4)

depends only on the current flux state and deterministic future transfers,
not on the common mode c_i. The law of the entire future sequence of a_i
also depends only on the flux state, because the flux recursion is closed.

This statement concerns a Doob martingale of a deterministic coefficient
source. It is not a freshness assertion for an arbitrary queried physical
off-model right-hand side.

## 4. Uniform second moment of the predictable variation

Let A=sum_i a_i. Given any pre-step history, reset the common mode to zero
while preserving (v,u,w), namely x=v/2,z=-v/2. This does NOT change the law
of any future a_i. The reset state's ordinary energy is
J=U+W+v^2/2<=H. By(2) and the Doob variance identity,

    E[sum_(j>=i) a_j | F_(i-1)] <=14 H_i<=14.     (5)

This includes the current predictable term. It follows that EA<=14 and

    EA^2
      =2 sum_i E[a_i sum_(j>=i) a_j]-sum_i E a_i^2
      <=28 EA <=2*14^2.                          (6)

The conditional expectation in(5), not an independence assumption, justifies
the multiplication by the predictable a_i. Resetting c is valid only because
the full future variation law is flux-only as established in section3.

## 5. Dimension-free Hilbert martingale fourth moment

For independent centered sphere components,
E alpha^4<=3(E alpha^2)^2 and similarly for beta. Expanding the norm in(3),
and using <h,g>^2<=||h||^2||g||^2, gives conditionally

    E||Delta_i||^4 <=3 a_i^2.

The difference is conditionally centrally symmetric, so both odd terms in
the fourth-power expansion vanish. Thus, with W=max_i ||M_i||,

    E||Z||^4 <=6 E[W^2 A]+3 EA^2.

The elementary Doob L4 bound is (EW^4)^(1/4)<=4/3 (E||Z||^4)^(1/4).
For completeness it follows by stopping at first crossing of lambda:
lambda P(W>=lambda)<=E[||Z|| 1_(W>=lambda)]. Integrating 4lambda^2 and
using Holder gives EW^4<=4/3 E[||Z|| W^3], hence the stated inequality.

Let X=(E||Z||^4)^(1/2), B=(EA^2)^(1/2). Cauchy–Schwarz now yields

    X^2 <= (32/3) X B+3 B^2.

The positive root is less than11 B, so E||Z||^4<=121 EA^2<=242*14^2=47432.
The unit birth coefficient has disjoint support. Its full inverse-column
fourth norm therefore satisfies

    E||V e_j||^4 =1+2E||Z||^2+E||Z||^4
                 <=1+2*4+47432=47441<50000.

This proves(1). Independent audit specifically checked the Doob filtration,
flux-only future variation law, common-mode reset, and uniform-state14 bound.
`verify_branch_doob_exact.py` additionally checks512 finite full-frame paths
using Fraction arithmetic, including the conditional future mean, exact Doob
differences, common-mode invariance, and variance identity. It is a finite
algebra control, not a replacement for the all-depth Haar proof.

## What this would and would not settle

Together with the separately proved E|P_j Psi^T a|^4<=3||a||^4, Cauchy–Schwarz
would bound a SINGLE correlated anchor product by sqrt(150000)||a||^2,
without pretending the two factors are independent. It would not by itself
control the sum and cross terms of all anchor contributions, establish a
generalk theorem, prove constant global-LS risk, learn unknown bases, or solve
RE02. Those remain separate research obligations.
