# Phase-twisted uniform gnu construction: independent audit

**Analytic and exact arithmetic PASS, 2026-10-26 03:08 UTC.**
Source `symmetric-quantum-codes/phase3/phase_twisted_gnu_candidate.md`, SHA256
`61cc32b4e1d1d15207d7b8fd5dbbb32fc7780714c49ec7aa68eb39194a12b0a6`.
No novelty, best-known, publication-priority, or full minimum claim is made.

The construction gives a two-dimensional complex subspace of
`Sym^(4t^2+2t)(C^2)` correcting arbitrary t-qubit errors for every integer
t>=10. It has exactly2t+2 nonzero Dicke support rows in the displayed axis.

## Physical KL necessity/sufficiency and normalization

Put g=2t, m=g+1, n=gm. The even and odd binomial distributions
p_i=C(m,i)/2^(m-1) each sum to1; their supports are disjoint. Their chosen
unit phases therefore give two orthonormal codewords.
For the actual g-qubit erasure Kraus maps, the squared Schmidt coefficient
at deleted weight a is

`C(g,a) C(n-g,gi-a)/C(n,gi)`
`= C(g,a) (gi)_a (n-gi)_(g-a)/(n)_g`.

This is a polynomial of degree at most g in i. The alternating binomial
sum of every such polynomial vanishes since m=g+1. Thus every diagonal
entry of the two reduced Gram matrices agrees, with no phase assumption.
For off-diagonal entries, retained-weight equality is gi-a=gj-b.
Because0<=a,b<=g, distinct support nodes can match only when |i-j|=1
and {a,b}={0,g}. Equal logical parities cannot have this match. Each of
the four remaining cross entries is one of the two parity edge sums, or
its conjugate, multiplied by the common positive1/(n)_g ladder factor.
Hence the two specified edge sums vanishing gives the complete physical
g-erasure KL condition. Permutation symmetry gives it on every g-set;
this is equivalent to arbitrary t-error correction. No nondegeneracy,
time reversal, real-code restriction, or numerical residual is used.

## Phase closure and uniform inequalities

The transition graph is a path, not a cycle. Arbitrary unit edge phases
eta_i are realized by zeta_0=1, zeta_(i+1)=zeta_i conjugate(eta_i).
Mirrored amplitudes agree and the noncentral parity cancels pairwise.
For t>=11, the central parity cancels with its two nearest same-parity
neighbors, using e=c+i sqrt(1-c^2), c=a_t/(2a_(t-2)). For t10, two
neighbor pairs use their summed amplitude instead. No compatibility
condition between the two logical directions is omitted.

Independent direct factorial calculation confirms the displayed reduced
amplitude product and ratio. For t>=13, bounding the three binomial-factor
logs by1/t,2/t,1/(t-1), and the product logs by
2(2t-1)/(t^2-4), gives exactly353/572 at13. Each term decreases thereafter;
353/572<2/3<log2. This proves a_t<2a_(t-2) at every larger t.
Exact t11/12 rational comparisons and the two t10 squared comparisons
are sufficient, strictly so. The same family fails for t1..9 because its
central edge exceeds the sum of all others in that parity class.

## Independent finite controls

`check_quantum_phase_gnu_independent.py` imports no worker code and uses
only the standard library. It rebuilds all physical erasure Gram entries
at t10,11,12,13, checks normalization and all diagonal equalities, exact
zero support for all other entries, the four cross-entry factors, and
symbolic path-phase cancellation. It also checks all finite inequalities
and the factorial/product identity. Companion JSON records PASS.
These are controls of the analytic all-t argument, not an extrapolation.

## Dated primary-source comparison, not an exhaustive priority finding

Aydin--Alekseyev--Barg, arXiv2310.05358v3, Construction5.1/Theorem5.3,
gives the explicit uniform bound4t^2+2t+1; the construction here improves
that particular formula by one qubit for t>=10. The original GNU theorem
in Ouyang1302.3247 uses spacing/support parameter at least2t+1 for
arbitrary t errors, giving(2t+1)^2 at unit scaling. Ouyang1604.07925
provides a polynomial qudit family with stated length at least
(2t+1)^2(d-1). The 'shifted GNU' family in2102.02494 shifts Dicke weights;
that name is not evidence of the phase cancellation mechanism here.
A focused search on2026-10-26 did not locate this exact phase-spaced
construction, but it does not establish novelty or best-known status.
Finite-group/numerical families and more general complex code families
must be compared separately.

Primary sources:
- https://arxiv.org/abs/2310.05358v3
- https://par.nsf.gov/servlets/purl/10549462
- https://arxiv.org/abs/1302.3247
- https://arxiv.org/abs/1604.07925
- https://arxiv.org/abs/2102.02494

This does not approach the conjectured leading constant3, prove its
minimum formula, or improve the already established t2/t3 frontier.
