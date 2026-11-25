# Why the naive dense-basis wavelet-to-forest reduction fails

**Status:** exact obstruction to a particular reduction, not an impossibility
result for fixed-basis approximation or RE-02.

## What the coordinate change does preserve

For known orthogonal hierarchical row/column transforms Q_U,Q_V, set
`A_tilde=Q_U^T A Q_V`. One forward product by A_tilde costs one forward product
by A, and one transpose product costs one transpose product by A. Frobenius
norms and the optimum over the **exactly transformed** fixed-basis linear
class are preserved. Unrelated row and column bases pose no issue for these
facts. The failed step is identifying that transformed class with free
coefficients on a forest support.

## Exact depth-two example

Take k=1,N=8,L=2. Finest active vectors are the first coordinate in each of
the four two-coordinate leaves. At the next level use left active vectors
`(3/5,4/5)` and right active vectors `(5/13,12/13)`, separately on the two
parent nodes. The local detail is `(-s,c)` for an active vector `(c,s)`.

Order the final wavelet coordinates as four leaf details, two parent details,
and two root actives. These are orthonormal separately on the left and right.
The physical local coefficient atom `e_0 e_1^T` belongs to the exact fixed
HSS subspace. Its wavelet transform has two entries:

    A_tilde[4,0] = -4/5,     A_tilde[6,0] = 3/5.

They are tied to a **single** free coefficient. The complete fixed class has
22 orthonormal coefficient atoms (three per each of six nonroot nodes, plus
four root coefficients), while the union of nonzero wavelet coordinates
across those atoms has 30 positions. A diagonal-plus-bidirectional forest
on eight scalar coordinates has at most `8+2(8-1)=22` positions.

Therefore this specific hierarchical wavelet transform cannot convert the
class to such a forest support, even after coordinate permutation. Its
coordinate envelope also contains the triangle on vertices `{0,4,6}`.
Treating all 30 envelope coordinates as independently variable enlarges the
class: the isolated atom `e_4 e_0^T` has exact squared distance `9/25` from
the true transformed class.

`wavelet_support_obstruction.py` independently constructs all 22 orthonormal
atoms with standard-library rational arithmetic, transforms them, and checks
all assertions exactly. The unrelated left/right rotations are deliberate.
The argument does not exclude some entirely different global pair of
orthogonal transforms; it only refutes this naive wavelet identification.

## General structural reason

A local active vector is a combination of its parent's active and detail
vectors. Recursing expresses it in all ancestor detail spaces plus its root
active space. Thus a local active-detail coefficient becomes several
ancestor-descendant entries whose amplitudes obey transfer-matrix ties.
For generic nonzero scalar transfer coefficients, a root-to-leaf chain gives
a clique in the coordinate support envelope: the leaf detail, all ancestor
details, and the root active are pairwise connected. Its size grows with L.
Consequently the free envelope has degeneracy growing at least linearly in
L; direct forest coloring and constant-degree sparse approximation cannot
simply be applied to this enlarged support with depth-independent queries.

This does **not** prove that enlarging the support destroys all approximation
guarantees. If an unbiased support estimator has variance at most C times
the envelope residual, orthogonally projecting it back into the exact fixed
class gives error at most `(1+C)` times the true fixed-class optimum. The
projection needs no additional matvecs. What is lost in the naive route is
the constant-query forest structure, not the possibility of such a projected
comparison. A successful method must exploit the coefficient ties or some
other structure rather than ignore them.
