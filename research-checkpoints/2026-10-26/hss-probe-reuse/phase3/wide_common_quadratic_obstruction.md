# Why the wider all-state common-quadratic search fails

**Status:** exact obstruction to a stronger proof ansatz, not to an algorithm.
The model below already grants fresh independent normalized complement
orientations at each step. It does not resolve whether that filtration is
valid for actual feedback data. It explains the previous numerical
`wide_both_bank_potential_search.py` infeasibility without relying on a grid.

In a scalar isolated branch let the normalized active sample coordinates be
x,z and let u,w be the two passive vectors of dimension d=s−1. A general
rotation-invariant quadratic storage has form

    P=A x^2+2C xz+B z^2+U||u||^2+W||w||^2.

Suppose it satisfies, for EVERY input state and EVERY pair of physical
transfer rotations,

    P(state)−E P(next state) >= E(emitted coefficient energy).       (*)

No such quadratic exists, even without requiring P to dominate sample energy.
The two corner transfers below suffice; no continuous angle search is needed.

## Corner1: left active retained, right active/detail swapped

Fresh isotropic complement orientations give

    E x_next^2=||u||^2/d,     z_next=0,
    E||u_next||^2=(x−z)^2+(1−1/d)||u||^2,  w_next=0,
    emitted energy=z^2.

The u-only coefficient in (*) is (U−A)/d, so A<=U. Its active 2x2 matrix is

    [[A−U, C+U], [C+U, B−U−1]].

Positive semidefiniteness forces A>=U, hence A=U, C=−U, and B>=U+1.

## Corner2: right active retained, left active/detail swapped

The roles reverse:

    x_next=0,  E z_next^2=||w||^2/d,
    u_next=0,  E||w_next||^2=(x−z)^2+(1−1/d)||w||^2,
    emitted energy=x^2+||u||^2/d.

The w-only coefficient gives B<=W. The active matrix forces B>=W, so
B=W, C=−W, and A>=W+1. (The extra u emission only imposes another constraint.)
Together C=−U=−W, A=U, B=W contradict both A>=W+1 and B>=U+1.

This kills only a single rotation-invariant, all-state quadratic storage
with one-step emitted-energy decrease. It does NOT kill a multi-step or
nonquadratic storage, a potential on reachable birth states, an expectation
bound with a different filtration, or the actual wider global-LS decoder.
In particular it must not be described as an HSS approximation lower bound.
