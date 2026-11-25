# No realization-uniform coercivity for generic wider Haar tree frames

This is an obstruction to a proposed proof condition, **not** a relative-error
lower bound for the randomized algorithm or for global least squares.

Take k=1, N=2^(L+1), and every prescribed active vector (1,0). The fixed class
is the diagonal plus both directions of a known representative tree: the
parent of a nonzero index clears its least significant set bit. Choose the
path

    v_0=0, v_1=2^L, v_2=2^L+2^(L-1), ..., v_(L+1)=2^(L+1)-1.

It has m=L+1 edges. Assign the two probe vectors e_0,e_1 according to the
parity of the index's population count. These are valid square tree frames.
They are also valid wider tree frames of every width s>=2, embedded in the
first two coordinates: at every local step the selected detail is orthogonal
to the active frame. They belong to the support of the generic wider Haar
construction, although any exact realization has probability zero when s>2.
Use the same realization in both banks.

Let B be symmetric, zero except on the m path edges, with

    B[v_(j-1),v_j]=B[v_j,v_(j-1)]=(-1)^j,  j=1,...,m.

B is in the prescribed fixed class. Each interior path vertex sees two
neighbors of the same probe color with opposite coefficients, so its product
row vanishes. Only the two endpoints survive. Consequently,

    ||B||_F^2=2m,
    ||B Omega||_F^2+||B^T Psi||_F^2=4,
    Rayleigh quotient = 2/m = 2/(L+1).

Thus no positive depth-independent c can make the measurement map coercive
for **every** allowed wider Haar-frame realization. By continuity, choosing
L with2/(L+1)<c gives an open neighborhood of frame realizations violating
that c; it has positive probability under the independent Haar-complement
law. This rules out an almost-sure depth-independent coercivity constant
uniform over all L as well.

It does NOT rule out an expected inverse bound, average-case error control,
conditioning on good frames, or a different deterministic frame design. The
size of the bad neighborhood may shrink rapidly with L. The direct three-
color forest design remains uniformly coercive, so this is not a statement
about the known forest class itself being difficult.

`verify_wide_haar_coercivity.py` checks the exact integer path cancellation
and HSS representative-tree edge condition for L=1,...,20 without allocating
an exponentially large dense matrix.
