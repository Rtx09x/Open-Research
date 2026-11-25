# Matrix-valued branch reduction: closed flux, but not a stability theorem

**Status:** exact algebraic reduction, independently analytically audited PASS
(26 October 2026), with an independently written Fraction physical decoder
and all384 signed-permutation second-moment controls. The worker also has
a separate rational k=2 physical-subtraction control. The scalar
constant-risk theorem remains the only general dense prescribed-basis theorem
with a depth-independent factor proved here. This note does not prove an
arbitrary-k bound or permit substitution of a correlated matrix source.

## Normalized coordinates

Let k>=1, s>=2k, d=s-k. At a parent, the forward observation frame is the
orthonormal row frame [F;G;J], with k,k,d-k rows, and the transpose frame is
[P;Q;K]. The prescribed physical child transfers and their complements form
orthogonal matrices

    O_V=[ A B ; A_perp B_perp ],
    O_U=[ R T ; R_perp T_perp ].

Thus the child's active frames are F_c=A F+B G and P_c=R P+T Q.
The canonical child forward complement is
[A_perp F+B_perp G;J], and likewise on the transpose side. Independently
rotate these full d-dimensional complements by fresh O,H in O(d).
These are the explicit full-completion normalized coordinates; freshness
for a pure inverse source uses the separately established reverse-coordinate
construction, not an assertion about arbitrary physical noisy samples.

Write the child carried samples as

    Y_c=X F_c + Y O [A_perp F+B_perp G;J],
    Z_c=Z^T P_c + W^T H [R_perp P+T_perp Q;K],

where X,Z are k-by-k, Y is k-by-d, W is d-by-k. Partition

    Y O=[Ybar Yhat],       H^T W=[Wbar;What]

at k columns/rows. Local coefficients and next active coordinates are

    da=T^T(X A+Ybar A_perp),
    dd=T^T(X B+Ybar B_perp),
    ad=(R^T Z+R_perp^T Wbar)B,
    X'=R^T X A+R^T Ybar A_perp,
    Z'=R^T Z A+R_perp^T Wbar A.

The next passive coordinates are

    Y'_G=R^T(X-Z)B+R^T Ybar B_perp-R_perp^T Wbar B,
    Y'_J=R^T Yhat,
    W'_Q=-T^T(X-Z)A+T_perp^T Wbar A-T^T Ybar A_perp,
    W'_K=What A.

These follow directly from Y_next=R^T Y_c-ad G and
Z_next=A^T Z_c-da^T Q, with no probabilistic approximation.

## Pointwise flux identity and expected loss

Let D=X-Z and Hflux=||D||_F^2+||Y||_F^2+||W||_F^2. Orthogonally transform

    [ D Ybar ; -Wbar 0 ]

on the left by O_U^T and on the right by O_V. Its three retained blocks
are D',Y'_G,-W'_Q. Its remaining block is

    Lambda=T^T D B+T^T Ybar B_perp-T_perp^T Wbar B.

Consequently, exactly and pointwise,

    Hflux-Hflux'
      =||Lambda||_F^2+||T^T Yhat||_F^2+||What B||_F^2 >=0.       (1)

Both D' and the passive updates depend only on (D,Y,W), not on the common
mode (X+Z)/2. Conditional independent Haar rotations give

    E[Hflux-Hflux' | X,Z,Y,W]
      =||T^T D B||_F^2
       +(1-||B||_F^2/d)||T^T Y||_F^2
       +(1-||T||_F^2/d)||W B||_F^2.                            (2)

For d>=2k the two passive coefficients are at least1/2. The expected local
output cost is

    E[||da||_F^2+||dd||_F^2+||ad||_F^2 | state]
      =||T^T X||_F^2+||R^T Z B||_F^2
       +(k/d)||T^T Y||_F^2+(||T||_F^2/d)||W B||_F^2.           (3)

Thus the passive portion of(3) is bounded by k/(d-k) times the flux loss.
The active portion is not covered by that pointwise comparison.

## The common-mode Doob gate is algebraic, not the remaining difficulty

For a deterministic coefficient source with the valid reverse filtration,
the conditional mean active updates are X->R^T X A,Z->R^T Z A. Every
conditional future output mean is therefore a deterministic linear map of
X,Z alone. A newly revealed Doob difference is a deterministic linear map
of Ybar,Wbar (plus the analogous terminal-root passive component). Its
conditional covariance, and the law of its future predictable variation,
depend only on the flux state (D,Y,W). Resetting the common mode does not
change them. This establishes the structural flux-only part of the scalar
martingale argument for matrix blocks.

It does NOT establish a rank-independent expected complete-output budget
from arbitrary normalized states, nor a dimension-free fourth moment of the
whole matrix-source operator. Those quantitative gates are still open.

## A natural row-covariance cone fails

The direct analogue S_Y >= c E[XX^T], c=(d-k)/k, is not generally invariant.
Take k=2,d=4,c=1, R=I,T=0,R_perp=0,T_perp=I,
A=diag(1,0),B=diag(0,1), A_perp=-B,B_perp=A,
X=diag(1,0),Z=W=0, and YY^T=XX^T. The cone holds with equality. After one
fresh orientation, however,

    E[X'X'^T]=(5/4)diag(1,0),
    E[Y'Y'^T]=(3/4)diag(1,0).

So this particular matrix cone fails even though the exact flux contraction
holds. This all-state example does not refute a more refined reachable cone,
a nonlocal output bound, the scalar theorem, or arbitrary O(k)-query methods.
The missing geometry is on the right of X: a transfer can retain its occupied
column while using an orthogonal column to extract fresh passive noise.
