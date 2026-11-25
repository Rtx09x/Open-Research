# A reachable covariance cone for a wider scalar pure-passive branch

**Status:** the abstract moment/cone algebra has passed an independent advisor
audit. The connection to deterministic inverse columns has now also passed
independent analytic audit; see `wide_scalar_inverse_bound.md`. This is NOT a relative-error theorem for the
probe-correlated off-model RHS, and it is not a globalLS theorem.

## Exact scalar boundary model

Use width s=d+1 with d>1. In each bank maintain an active unit row and a full
orthonormal d-row complement. Normalize a single live branch's sample pair
as Y=x F+u C and Z=z P+w D, where u,w are d-vectors. At an upward boundary,
the prescribed physical transfers have coefficients(r,t) and(a,b), with
r^2+t^2=a^2+b^2=1. The two full complement orientations at this boundary are
independent HaarO(d), independent of the incoming normalized state.

Write p=t^2,q=b^2. If E[xz]=0 initially it stays zero. Let
X=E x^2,Z=E z^2,U=E||u||^2,W=E||w||^2. Averaging the exact subtract/compress
map gives

    X'=(1−p)(1−q)X + (1−p)q U/d,
    Z'=(1−p)(1−q)Z + (1−q)p W/d,
    U'=(1−p)q(X+Z)+(1−p)(1−q/d)U+pq W/d,
    W'=(1−q)p(X+Z)+(1−q)(1−p/d)W+pq U/d.

The expected emitted da,dd,ad coefficient energy at this boundary is

    e=pX+pU/d+q(1−p)Z+pqW/d.                         (1)

These formulas require only the first two isotropic moments of the full
complement orientations, not their entire continuous distribution.

## Invariant cone and total-emission bound

For pure-passive initialization, X=Z=0 and only u or w is present. The cone

    (d−1)X<=U,   (d−1)Z<=W                             (2)

holds initially and is invariant. In fact

 U'−(d−1)X'=(1−p)[(1−q)(U−(d−1)X)+q(X+Z)]+pqW/d >=0,

with the symmetric formula for W'−(d−1)Z'. Set J=X+Z+U+W. The exact flux loss is

    J−J'=pq(X+Z)+p(1−q/d)U+q(1−p/d)W.

By(2), the cost(1) is at most

    [(2d−1)/(d−1)^2] (J−J').

For example, bound pX by pU/(d−1), and q(1−p)Z by q(1−p)W/(d−1); compare with
J−J'>=(d−1)(pU+qW)/d. Summing gives

    sum_boundary E(emitted coefficient energy)
      <= C_d J_initial,   C_d=(2d−1)/(d−1)^2.          (3)

At width3 this constant is3; at width4 it is5/4. A terminal root decoded from
one forward orthonormal test contributes at most E||Y||^2=X+U<=J_initial.
There is no contradiction with the exact no-common-quadratic obstruction:
(3) uses the reachable cone, not a one-step inequality for every sample state.

## A precise proposed bridge to actual coefficient inverse columns

For scalar fixed bases, augment the generic wide frame construction with an
unused full orthonormal complement at each node. If a parent has full frame
[F;G;C_unused], a child active is aF+bG. A canonical child complement is
[−bF+aG;C_unused]. Multiply it by an independent HaarO(d) matrix H_child to
obtain the child's full complement; its first row is the actual detail test.
This has the same marginal law as choosing a uniform detail in active-perp.

For a single deterministic coefficient-source column in (I+K)^−1, the source
da/ad coefficient injects a pure passive sample into the opposite bank.
In these normalized full-complement coordinates, the starting amplitude is
fixed. The branch state before crossing an ancestor boundary is a function
only of the deeper relative H variables, while that boundary's H is sampled
independently. This explicit equivariant construction is intended to justify
the fresh-boundary hypothesis above; it must be checked against the actual
ancestor-triangular regression/physical decoder, not simply asserted for an
arbitrary carried noisy sample. A dd or root source has no outgoing feedback.

If this bridge holds, an individual deterministic scalar inverse column has
mean squared norm at most C_d+2 (its initial coefficient, the emissions, and
root output). A further birth-sign argument would be needed to upgrade this
to an expected operator bound for every deterministic coefficient RHS. That
upgrade is being tested, not included as an established theorem here.

The actual raw RHS from an off-model E is probe-dependent and may contain
outside-subtree frame data. Neither(3) nor the closed-subtree gauge lemma
makes it independent of the inverse. That is a separate unresolved step.

`verify_wide_reachable_cone.py` checks the physical one-step moments with
exact signed-permutation averages and the cone/telescoping identities with
Fraction arithmetic. `test_wide_inverse_coefficient.py` tests the separate
inverse-column/operator hypothesis numerically; those data are not a proof.
