# Uniformly mixing arbitrary-rank prescribed-basis reconstruction — audit

2026-10-26 02:19 UTC. **Independent analytic PASS for the restricted theorem.**
Audited `hss-probe-reuse/phase2/uniformly_mixing_fixed_basis_bound.md`; numerical
or finite controls are corroboration, not the proof of all depths/ranks.

## Precise scope

The real orthonormal rank-k nested row/column bases are prescribed before
probing. Every child active transfer has singular values in
[delta,sqrt(1-delta²)], with fixed0<delta<=1/sqrt2. Use the explicit complete
sibling/unused-coordinate complement gauge and two independent width3k
banks. The theorem is relative to the linear fixed-basis class, not to
unrestricted HSS OPT. It uses3k A products plus3k A^T products.

The audited factor is

    E||A-R(A)||² <= [5+16delta^(-4)+32delta^(-8)] OPT_fixed².

It is independent of k and depth but diverges as delta goes to zero. Genuine
interlevel channel mixing is allowed; coordinate and nearly singular
transfers are not uniformly covered. The full arbitrary-basis problem and
unknown-basis learning remain open.

## Conditional source gate

Fix the complete opposite bank. In the explicit normalized pure-source
recursion, a source matrix measurable only in that bank is deterministic,
and the next own-bank child orientation is independent of the incoming
normalized state: parent frames cancel from the exact physical update.
This reverse-coordinate induction is specific to pure coefficient sources,
not an assumption of freshness for arbitrary noisy sample arrays.

With d=2k, a=delta²(1-k/d), and c2=a delta², orthogonality gives
H=||Y||²+||N||²+||Mrow||²+||What||². The first expected loss is at least
a||Y||²+delta²(||Mrow||²+||What||²). The next forward-passive energy has
expectation at least delta²||N||², so the following loss supplies the missing
term. The symmetric conditional calculation holds in the other direction.
Hence two-step conditional flux contraction has factor1-c2. Pairing finite
cuts and retaining a possible last cut gives sum E H<=2H0/c2, including root.

Common C=(X+Z)/2 has a deterministic contraction factor rho² and forcing
norm²<=H/2. The finite l2 convolution inequality, plus pointwise local
emission<=J and terminal root<=J, yields conditional pure-source ancestor
budget Bcond||M||², where Bcond=4delta^(-4)+8delta^(-8). No opposite-bank
centering, Haar fourth moment, or matrix-source operator norm is used.

## Reconstruction bridge

For a forward-bank-dependent row-orthonormal q and deterministic spatial A,
wavelet birth coefficients are A_v q F_v^T and A_v q G_v^T; their squared
norms sum to at most||A_v||². Condition the entire forward bank and use the
transpose-fresh source bound. Distinct births have zero total-output cross
terms by the deeper source's own independent centered opposite detail sign.
Only the CHOSEN deeper source's own birth support is disjoint from the other
output; an ancestor birth can overlap the descendant's strict-ancestor
response, and that overlap is killed by the descendant's sign. This precision
was requested in the prose and does not change the proof.

The correlated ad anchor B_j=P_j P^T A_j is measurable in the transpose bank.
The forward-fresh conditional source theorem therefore applies directly;
E||B_j||²<=||A_j||² by contraction and frame isotropy. No unjustified random-
source substitution is needed. The da case is symmetric. Off-diagonal dd
blocks split into two opposite-bank-measurable contracted sources. Squared-
triangle estimates give carry constants2+4Bcond and4Bcond, respectively.

Finest independent central signs separate whole ad columns, da rows and dd
blocks into distinct Walsh characters. Fine coefficient support is orthogonal
to all coarser output, vanishes for aa input, and has expectation at most twice
the non-aa energy. The aa sector is the identical coarser problem. Induction
therefore takes a maximum, not a depth sum, giving operator constant4+4Bcond.
Exactness on the fixed class, linearity and orthogonal residual decomposition
give the displayed relative constant5+4Bcond.

## Finite randomness

Independent uniform signed permutations of the FULL complements in the
explicit gauge have all properties used here: orthogonality, centering,
conjugation isotropy and central signs. The same proof therefore applies to
that separate finite probe law. No assertion is made that arbitrary sparse
complement gauges have the Haar distribution or that they inherit Haar
fourth moments. The earlier unbounded one-bank conditional phase-return
example violates the uniform-mixing hypothesis and is consistent with this
restricted result.
