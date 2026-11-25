# Failed dense extension: parent-plane nonbacktracking frames

**Scope:** the frame proposal and the fixed-basis LM coefficient decoder below.
This does not invalidate the direct three-color forest theorem, and it does
not obstruct all constant-query fixed-basis algorithms or RE-02.

## Proposal and first tests

With three probe columns and k=1, retain the parent's orthonormal two-frame
plane. A child's new detail frame is an independently signed unit vector
orthogonal to that **entire** parent plane. Its active vector lies in that
plane. This preserves local row isometry and complement centering.

`nonbacktracking_frames.py` forms the complete linear reconstruction operator
and its expected error Gram matrix. Exhaustive sign averaging gives worst
error eigenvalue 2 at L=1, 3.67706136869 for one dense L=2 instance, and exactly
4 for coordinate L=2 bases. The L=3 dense result is only a Monte Carlo check.
Thus even the factor-two forest result does not transfer automatically.

## Explicit coordinate family showing depth growth

For the dyadic representative tree on N=2^(L+1) scalar blocks, a nonzero
vertex's graph parent clears its least significant set bit. Take L=2t and

    a=(4^t-1)/3,       b=a+4^t,       A=e_a e_b^T.

Both endpoints are odd and distinct, so A lies off the tree support; its
fixed-tree optimum is exactly one.

The parent-plane construction produces signed coordinate probes. Their color
recurrence is independent of the signs. On indices whose odd binary bit
positions are all zero, the color is `popcount(index) mod 2`, using only colors
zero and one. To see this, start with plane {0,1}. Processing a bit pair `0b`
first keeps the active color and temporarily uses color 2 as the detail;
the next bit returns the plane to {0,1}, toggling the active color exactly
when b=1. The highest root bit gives the initial color.

All vertices on the unique path from a through zero to b have this property.
Clearing one set bit toggles the color, so the entire path is bichromatic.
It has `popcount(a)+popcount(b)=t+(t+1)=L+1` edges.

On coordinate bases the LM recursion eliminates the scalar leaf of each
finest pair, then repeats on the representative tree. In a two-color
component, its child-parent and parent-child coefficient equations are
exactly signed tree-divergence leaf elimination. The off-support unit block
acts as a virtual edge between a and b. The unique flow sends unit-magnitude
coefficients along all L+1 path edges; the third-color channels do not alter
this component. All sign factors have magnitude one. Consequently

    ||A-B||_F^2 = 1 + (L+1) = L+2

for every sign realization, while the fixed-class optimum is one. This rules
out a depth-independent error constant for this proposed construction and
decoder. It does **not** rule out its O(L) error guarantee.

`nonbacktracking_coordinate_test.py` checks the scalar recurrences in exact
integer arithmetic, using the orthogonal coefficient energy ledger rather
than materializing the output. It exhausts all 4096 sign assignments at L=2;
at L=4,6,8,10, twenty independent assignments per depth give errors 6,8,10,12,
respectively, and coefficient ledgers `[2,0,...,2,0,root 1]`. Those larger
finite tests support, but do not replace, the path argument above.

The basic failure is combinatorial: this coloring follows the hierarchy's
successive planes, not depth modulo three in the representative forest. The
successful direct forest scheme uses the latter and has no bichromatic
four-vertex path.
