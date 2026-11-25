# Depth-independent mean-square inverse for deterministic scalar coefficients

**Status:** complete restricted proof; independent advisor analytic audit PASS
(26 October 2026). This is
NOT a noisy HSS approximation theorem and NOT a global-LS inverse theorem.
The right-hand side below must be fixed independently of the probe banks.

## Theorem

Fix arbitrary real scalar (k=1) dense nested row and column bases. Use two
independent generic width-s tree-frame banks, s>=3. In the orthonormal local
da,dd,ad/root coefficient basis, let T=I+K be the original-sample regression
operator of `triangular_regression_identity.md`, and V=T^−1. Then

    E[V^T V] is diagonal,
    E[V^T V] <= [2+(2d−1)/(d−1)^2] I,   d=s−1.        (1)

Consequently for every deterministic coefficient vector b,

    E||Vb||^2 <= [2+(2d−1)/(d−1)^2]||b||^2,

independently of hierarchy depth and matrix dimension. The constants given
by this proof are5 at width3 and13/4 at width4. They are not claimed sharp.
The statement uses the usual full Haar complement law; the explicit complete-
frame construction below has exactly the same marginal law as the generic
wide detail-frame generator.

## 1. Inverse columns are single-branch passive injections

The cross-regression K strictly moves coefficients to ancestors. A dd source
and a root-core source have no outgoing feedback, so their inverse columns
are exactly coordinate unit vectors.

For a da source of value1 at node j, the source coefficient remains1 and its
contribution to all strict ancestors is exactly the LM recursion started at
that node's compressed active coordinate with samples

    Y_j=0,   Z_j=−Q_j,

where Q_j is the row-bank detail frame. An ad source analogously starts
Y_j=−G_j,Z_j=0. This follows directly by subtracting the source coefficient
from the opposite-bank sample; the own-bank coefficient regression is exact.
Only the single ancestor branch of j is nonzero. No new physical matrix input
or entry access is used in this algebraic identification.

## 2. Explicit full-complement gauge gives genuinely fresh reverse boundaries

For the forward bank, augment each node's active unit row F_v with a complete
d-row orthonormal complement C_v, whose first row G_v is the actual detail.
Suppose a child active is F_child=aF_v+bG_v, a^2+b^2=1. Define

    C_child^0=[−bF_v+aG_v; C_v,unused],
    C_child=H_child C_child^0,

where H_child is an independent HaarO(d). The first row of C_child is uniform
on the sphere in F_child-perp, as required by the original generic probe law.
Construct the row bank independently in exactly the same way. At the two
root children, use fixed inherited active rows e0,e1 and arbitrary complete
orthonormal complements, each randomized by its own independent H.

Now express a live branch's samples in its current full coordinates:
Y=xF+uC and Z=zP+wD. A passive source has fixed normalized coordinates
(x,z,u,w)=(0,0,0,−e0) or(0,0,−e0,0), independent of all H draws.

The exact boundary identity is an orthogonal plane rotation followed by
blockdiag(1,H_child). Therefore the normalized state at a parent depends only
on its child's normalized state, the two H_child draws, and the prescribed
physical transfer coefficients. It does NOT depend on H_parent: the parent's
full frame cancels from the coordinate calculation. Inductively, before
crossing a boundary the normalized state is a function only of strictly
DEEPER H draws; the current H_child draws are independent. This justifies the
fresh-both-bank hypothesis of `wide_reachable_cone.md` for these inverse
columns. It does not assert such freshness for arbitrary carried samples.

## 3. Quantitative column bound

The scalar moment recursion and invariant cone in `wide_reachable_cone.md`
apply. For pure-passive initialization of energy1 they give total expected
emitted coefficient energy at most

    C_d=(2d−1)/(d−1)^2.

The carried energy J never exceeds1 in expectation. Root decoding is a
contraction of the forward sample, so its expected coefficient norm is at
most1. Adding the source coefficient itself proves each inverse column has
expected squared norm at most C_d+2. At a root child the exact expected
terminal contribution is X+U/d, because the other root-active probe direction
is one isotropic direction of the d-dimensional complement; this also gives
an explicit four-moment recurrence for every column's precise expectation.

## 4. Exact orthogonality of distinct inverse columns in expectation

A da source column has deterministic unit entry at its birth and all strict-
ancestor entries linear in its own source detail Q_j. Every subsequent K step
ascends, so that draw never reappears as an ancestor detail. Conditional on
all ancestor frames, Q_j is centered. The analogous ad statement uses G_j.

For columns born at distinct nodes, choose a deeper birth (or either node if
they are in disjoint subtrees). The other column uses only its own birth and
ancestors and never uses this chosen source detail draw. The two columns have
zero overlap at the deeper birth coordinate; their remaining cross inner
product is linear in the chosen centered source detail. Its expectation is
zero. Same-node da and ad columns use independent source details from the two
banks and are likewise orthogonal after averaging. A dd column has no feedback
and its overlap with a strict-descendant column has zero expectation by the
same source-centering argument. Root columns are handled identically.

Thus E[V^T V] is diagonal. Combining this exact cancellation with section3
proves(1).

## Scope boundaries that must not be dropped

* The actual queried RHS b=(R_F(E),R_T(E)) for off-model E depends on these
  same frames and may contain outside-subtree data. Substitution into(1)
  without a new conditional argument is invalid.
* We have bounded E[V^T V], not E[VV^T]. The two are not interchangeable.
  In particular the domination of a global measurement Gram by T^T T does
  not turn(1) into a bound on the globalLS inverse Gram.
* The covariance cone and scalar moment recurrence here are k=1. Arbitrary-k
  matrix transfers require new operator-valued cone inequalities.
* The result is a stable inverse for deterministic coefficient data, not a
  query-efficient unknown-basis learner or a full-HSS comparator guarantee.

## Separate finite-orientation probe-law corollary

The same theorem holds if every H_child in the explicit full-complement
recursion of section2 is instead an independent uniform signed-permutation
matrix of dimension d. At the root children use the same specified full-frame
initialization and independently randomized complements. This is a DIFFERENT
probe law, not a claim that a signed-permutation detail is Haar on the sphere.

The reverse-coordinate induction uses independence of the H variables, not
transitivity of Haar measure. A signed permutation satisfies E H=0 and
E[H^T M H]=(tr M/d)I for every deterministic symmetric M. These identities,
independence between banks, and an independent central sign give precisely
the four quadratic moments, source centering, and terminal-root isotropy
used above. Thus the same cone proof and expected column orthogonality apply.
The conclusion does NOT apply to signed permutations relative to arbitrary
unrelated deterministic complements: the displayed complete-frame recursion
is part of this corollary's hypothesis. Advisor analytic audit also passed
this explicitly coupled variant.

## Reproducible checks

`verify_wide_inverse_branch_exact.py` averages all4096 assignments of the
finite signed-permutation complete-frame orientations on a two-level path.
It matches the exact four-moment recurrence, gives zero same-birth da/ad cross
expectation, and separately checks40 actual N8 dense coefficient-system
inverse columns against the physical branch calculation, using Fraction only.
The finite design is a control of the separately stated full-complement
signed-permutation corollary; the all-depth argument is the proof above.

`test_wide_inverse_coefficient.py` independently constructs the full original-
sample regression inverse for unrelated dense bases at L2,3,4 and widths3,4.
Its1200-draw diagonal estimates agree with the exact recurrence within ordinary
Monte Carlo errors; off-diagonal sample means are small. These numerical data
are corroboration only and are not the proof of(1).
