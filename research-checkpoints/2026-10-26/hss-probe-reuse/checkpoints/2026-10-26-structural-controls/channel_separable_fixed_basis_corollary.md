# Direct-sum corollary for channel-separable rank-k bases

**Status:** elementary direct-sum corollary of the audited scalar constant-risk
theorem; separate independent analytic advisor audit PASS (26 October 2026). This is a strict subclass, not arbitrary dense
rank-k nested bases. It is not part of the frozen00:20 addendum.

Suppose known orthogonal row/column coordinate changes decompose the physical
spaces into k channels, each with n coordinates. At every tree node, each
active scalar channel is a linear combination of only the two child actives
of that same channel. Different channels may have different scalar transfer
angles, and row/column channel bases need not agree. There is no mixing
between channels as one passes between levels. Leaf coordinates can be
interleaved to give the usual 2k-sized leaves.

Under the resulting known row/column permutations/orthogonal transforms,
the prescribed fixed class is the orthogonal direct sum of k^2 scalar classes
C_ab: row hierarchy from channel a and column hierarchy from channel b. Its
off-diagonal row/column ranks are at most k, and its coupling blocks remain
arbitrary k-by-k matrices.

For each column channel b, draw its three scalar forward probes and extend
them by zero outside that channel. The resulting3k matvecs with A provide
all forward sketches of all k^2 blocks A_ab simultaneously. For each row
channel a, do the analogous three transpose probes; another3k matvecs provide
all transpose sketches. Apply the scalar decoder separately to each block.
No physical entry queries or separate products per channel pair are needed.

The scalar801 bound and Frobenius orthogonality across block channels
give immediately

    E||A-Bhat||_F^2<=801 min_(B in C_fixed)||A-B||_F^2,

with6k TOTAL forward-plus-transpose products. Correlations across block
decoders sharing one bank are irrelevant because their output supports are
orthogonal. Known pre/post orthogonal changes preserve product counts and
the Frobenius comparator.

This does not diagonalize arbitrary dense nested bases. Local CS decompositions
may diagonalize one parent transfer, but the induced channel gauges generally
mix at the next level. Simultaneous no-mixing channel structure is an explicit
hypothesis, not an automatic consequence of orthonormal nested bases.
