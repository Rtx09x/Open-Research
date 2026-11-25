# Dense wavelet envelopes require depth-growing star colors

**Status:** exact obstruction to a particular free-envelope coloring route.
Not a lower bound for arbitrary fixed-basis algorithms or unrestricted RE02.

Take scalar dense nested bases with nonzero active and detail transfer entries
at every level, for example the rational rotations(3/5,4/5) on the row side
and(5/13,12/13) on the column side. Apply the separate global orthogonal
hierarchical wavelet transforms to rows and columns.

Consider a single nested branch: its L detail wavelets and its ONE root-active
wavelet on that side. The other root active has disjoint support and is NOT
included. There are t=L+1 coordinates in each bank. The free coordinate
support envelope of the transformed fixed class contains ALL t-by-t positions
on these two coordinate sets:

* Each detail-detail diagonal coordinate belongs to the local dd atom.
* For a fine detail and any coarser detail/root active, the fine da atom
  W_v V_v^T has a nonzero entry there. Its active column V_v has nonzero
  expansion coefficients in every ancestor detail and its root active,
  products of the nonzero transfer entries.
* The fine ad atom provides the reverse ordered coordinates independently
  on the row side.
* The root core supplies the root-active diagonal coordinate.

Thus the bipartite envelope graph contains K_(L+1,L+1). This statement is
about the union of nonzero coordinates of the class's atoms, not independent
freedom of those entries: the coefficients are tied.

A star coloring of K_(t,t) needs at least t+1 colors. Proper coloring separates
the two parts' color sets. If both parts contain a repeated color, two vertices
of each repeated color induce a bichromatic K2,2 and hence a forbidden P4.
At least one part must therefore use t distinct colors, and the other needs
at least one additional color. Consequently a direct star-coloring recovery
of this free envelope needs at least L+2 colors; the coordinate12k/factor3
argument cannot remain depth-independent through this naive transformation.

Projection of an envelope approximation back to the known tied class is
possible and restores its rank/basis constraints (with a controlled relative
error factor), but does not remove the depth-growing probing count. For
example if an envelope estimator has squared error<=c OPT_C^2, orthogonal
projection back to C gives error<=(1+c)OPT_C^2. The issue is query count, not
that projection itself is unavailable.

`verify_dense_envelope_clique.py` gives a Fraction-only certificate for
L=1,...,6 with unrelated rational row/column rotations, checking every needed
ancestor overlap and wavelet orthogonality. The all-depth argument above is
the proof; finite checks only guard against indexing mistakes.
