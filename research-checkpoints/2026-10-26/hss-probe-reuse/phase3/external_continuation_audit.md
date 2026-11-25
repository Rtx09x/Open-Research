# Independent audit of the external HSS continuation

Audit date:2026-10-25 UTC. The retrieved note labels its local date26October.
Source: authorized existing ChatGPT consultation, final response visible at
[private consultation identifier omitted] .
The downloaded note and21-file archive are retained unchanged under
`external_continuation/`. The initial Library searches did not resolve them;
a simpler exact-title-prefix search did. No new model message was submitted.

## 1. Exact greedy learner obstruction: PASS

For L>=3, N=2^(L+1), let

    x=sum_{j=0}^{L-1} e_(2^j), w=e_(2^L), z=e_(3*2^(L-1)),
    A=xw^T+(3/2)e_0 z^T.

The exponents are essential: signal rows are1,2,4,...,not0,2,4,....
All entries lie in the root left-to-right off-diagonal block. Its two singular
values are sqrt(L),3/2, so every rank-one HSS approximation has squared error
at least9/4. The globally rank-one xw^T attains that lower bound.

At each exact greedy round, the first2-row block has disjoint column supports
and row energies9/4,1; it uniquely chooses the noise row. Every other live row
block has rank1 and is retained. The signal and noise column locations stay
in different2-column blocks until the final round, when the noise column
uniquely wins. Diagonal blocks are zero, so diagonal correction does not alter
this induction. Each level loses exactly one orthogonal unit signal, and the
output is exactly the noise term. Thus greedy error squared=L and the supplied
weighted ledger=10L^2+13L. Its ratio to L*OPT^2 is(40L+52)/9, unbounded.

The Kronecker extension A tensor I_k is valid: competing eigenvalues9/4 and1
have multiplicityk with a strict gap, so the selected projector is unique.
OPT^2=9k/4, every born residual has energyk, and greedy error=kL. Within-block
basis gauges do not change this argument. This is a learner-specific exact-
entry lower family, not a query lower bound and not a lower bound for all
polynomial-time learners. Literature novelty remains unestablished.

New independent code `verify_greedy_bridge_independent.py` computes sparse
row/column covariance decisions using Fraction, rather than importing the
consultation's choices. It passes L3,...,12. The proof is the induction above,
not the finite range of checks.

## 2. Actual fresh coefficient risk: PASS, scalar canonical completion

For k=1 and the specified e0 completions at zero-data blocks, let sigma be the
forward sign on the signal column w, and tau_j the row-detail birth sign of
signal row2^j. Along the relevant left and right chains,

    Omega_w=sigma e0^T,    Psi_(2^j)=tau_j e1^T.

The tau_j are independent. A single source emits a unit D_da coefficient at
its birth; its remaining transpose sample travels to the final right-column
compression. The latter emits D_ad=tau_j and then the root emits−sigma tau_j.
All other coefficients vanish. For the full sum of sources this gives the
stronger **pointwise** identity

    coefficient energy = L+2(sum_j tau_j)^2.

Therefore expected coefficient energy=3L. The signal is orthogonal to the
learned fixed class, which contains the perturbation exactly, so expected full
error=4L. The ledger10L^2+13L is overly pessimistic here: its failure does NOT
falsify the desired O(L) risk of this two-pass construction on this family.

`verify_greedy_coefficient_identity.py` is a separate physical2-by-2 block
integer decoder, using the independently computed bases. It verifies the
pointwise identity on80 sign realizations at eachL3,...,10. These sampled exact
integer controls are not an exhaustive sign proof. After source inspection,
the supplied Walsh verifier was separately replayed forL3,...,8; all exact
moments passed. Those replays are identified as supplied-code replays, not an
independent implementation.

The external executive summary should not be read as an arbitrary-k4L claim:
its detailed coefficient proposition is explicitly k=1. The arbitrary-k
extension above applies to the greedy loss/weighted obstruction. No stronger
coefficient identity is assumed here.

## 3. Other claims: algebraically correct, scoped

* Risk operator K_C=(I−P_C)(I+E R_C^*R_C)(I−P_C) gives exactly conditional
  expected squared error. PSD Young inequality and the audited fixed-basis
  theorem reduce the full target to E_train <H*,K_C H*> <=C L OPT^2.
  This is a precise sufficient condition, not a proved learning theorem.
* Two candidates independent of12 new Gaussian validation vectors can be
  selected with expected squared error at mostsqrt(21/5) times the better
  candidate. The inverse-chi-square second moment is9/5 and ordinary second
  moment is7/6, giving the displayed constant by Cauchy--Schwarz. The two
  candidates need not be independent of each other, only of the validation
  bank. This standard-style selection tool does not construct a good learner.
* The counterexample itself has global rank2k and can be exactly recovered
  from4k supported two-sided products, then optimally rank-k truncated. This
  demonstrates scope, not robust recovery on arbitrary inputs.

## 4. Follow-on completion test and next target

Zero-data SVD completions do affect the learned fixed class, even though they
leave the greedy approximation/loss unchanged. Exploratory coordinate choices
(all0,all1,alternating levels,different bank choices) throughL7 did not produce
superlinear actual risk. They are not a proof of completion independence.

The next substantive target is the learner-aware signal covariance condition,
first for the precisely specified exact-entry greedy learner (a restricted
analysis lemma), then for a genuinely O(k)-query reused-sketch learner. The
former does not itself satisfy the query model. A useful falsification target
is an explicit A=H*+E with OPT=||E||^2 known and actual expected fresh coefficient
risk growing faster than L*OPT, not merely a large weighted upper bound.

In parallel, wider global least squares remains unproved. Its proposed
realization-uniform coercivity condition is exactly refuted by the separate
2/(L+1) path family; an expected inverse theorem needs new analysis.

## 5. Immediate exact corollaries of the audited construction

The amplitude3/2 is not essential. Any rationala with1<a<sqrt(L) gives the
same greedy projectors, born losses and coefficient-risk law, while OPT^2=a^2.
Consequently the worst-case greedy approximation ratio at depthL>=2 has
supremum at leastL (let a decrease to1). This matches the known2L upper bound
in its depth dependence, without a claim of sharp leading constant. It is a
corollary of the external construction, not a separate algorithm lower bound.

For the canonical scalar coefficient decoder the exact random squared error is

    2L+2T^2,  T=sum_(j=0)^(L-1) tau_j,

independently ofa in that range. Its expectation is4L and variance is
8L(L−1), using E T^4=3L^2−2L. Thus the finite-sign controls' empirical means
should not be mistaken for exact expectations. Some realizations have
quadratic error, but their contribution still yields the exact linear mean.
