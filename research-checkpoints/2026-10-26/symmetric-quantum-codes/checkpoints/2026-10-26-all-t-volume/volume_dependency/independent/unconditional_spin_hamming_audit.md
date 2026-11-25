# Independent audit: unconditional intrinsic-spin volume inequality

2026-10-26 00:50 UTC. **Analytic applicability audit PASS**, subject to the
ordinary published recoupling identities and the explicitly cited prior LP
monotonicity theorem. No remaining internally checkable mathematical blocker
identified. This is not a publication-priority or external-review verdict.

Audited worker statement: `symmetric-quantum-codes/phase3/unconditional_spin_hamming_candidate.md`.
For integer K>=2,t>=1, every complex K-dimensional subspace of Sym^n(C²)
detecting ranks0 through2t satisfies n+1>=K(t+1)². This does **not** establish
intrinsic Gram nondegeneracy, the stronger3t²+3t+1 minimum, or exact t3 minimum.

## 1. Kernel and normalization

With Hilbert–Schmidt orthonormal tensors, the normalized covariant channels
Phi_a=(N/(2a+1)) sum_q T_aq (.) T_aq* are unital. Their eigenvalues are
R_a(x)=N M_ax/(2a+1). Kraus multiplication followed by Clebsch–Gordan
orthogonality gives channel-composition coefficients
N(2b+1){a r b;j j j}². They are nonnegative and sum to1 by unitality.
Permutation symmetry of the6j symbol gives detailed balance with weights2a+1.
Evaluating the composition identity at rank1, where
R_1(x)=1−2x(x+1)/[n(n+2)], yields exactly
E[b(b+1)−a(a+1)]=r(r+1)(1−2a(a+1)/[n(n+2)]).

Independent exact6j controls in `check_racah_kernel_moments.py/.json` pass
414 rows, n1 through14, a,r up to5, including integer and half-integer spins.
These finite checks supplement the channel derivation, not replace it.

Squaring L(x)=sum_(a<=t)(2a+1)R_a(x) and using low-rank KL gives
sum_x [K L(x)²−N²c_x] a_x=0 with a_0=1, c_0=m/N,
m=(t+1)² and c_x=0 above2t. All factors N,K and sector dimensions agree.
This uses ordinary intrinsic LP only; no shadow or higher-moment cone.

## 2. Escape inequality

Triangle support forces all rows a<s=max(0,r−t) outside the radius-t set.
Their mass is s². Detailed balance cancels every internal transition.
Subtracting these rows' EXACT drift leaves only the remaining escaping
edges, each with positive Casimir increment at most r(2t+r+1).
The resulting lower bound is exactly worker equation(4).

For r<=t its comparison to q=r(r+1)/(4m) reduces to
4m−1−r(2t+r+1)>0, whose minimum on this interval is t²+7t+3.
For t<=r<=2t my independent substitution is t=s+u,r=2s+u, with s,u>=0.
After clearing the positive denominator
4(s+u)(s+u+1)^4(s+u+2)(4s+3u+1), the numerator has32 strictly positive
monomial coefficients. This is a distinct algebraic representation from
the worker's Bernstein proof. `check_quantum_critical_escape_polynomial.py`
and its JSON record the full exact polynomial. It is positive for t>=1,
including r=t and r=2t. Increasing n only improves the escape bound.

## 3. Lloyd lower bound and all K

The finite hypergeometric sum telescopes as stated. At n0=2m−2 its
consecutive-term ratio is bounded using
(m−u²)/[(2m−1)²−u²]<=1/(4m), u=h+1.
Thus the alternating-series lower bound L(r)/m>=1−q/2 is valid for
1<=r<=2t. Its first omitted term and successive ratios improve with n.
At N=Km−1, K>=2 ensures n>=n0. The constant coefficient is m>0;
each low nonconstant coefficient exceeds Km²q²/4+m(1−q)>0.
Here 0<q<1 throughout. Every higher coefficient is K L(r)²>=0.
Since a_0=1 and a_r>=0, the ordinary LP is infeasible at this length.

## 4. Extending to all shorter lengths: actual source theorem

Manes–Subramanian–Jiang, [arXiv2610.00561v1, §VIII.2 Theorem6](https://arxiv.org/html/2610.00561v1#S8.SS2)
proves ORDINARY LP feasibility at(n,K,d) implies feasibility at(n+1,K,d).
It explicitly distinguishes this from unknown physical-code padding.
There is no parity restriction and no shadow-monotonicity assertion.

I read the full proof. Its explicit T_n is nonnegative, column-stochastic
and lower-triangular, and intertwines M_n with M_(n+1). Source algebraic
identities S359 and S363 pass independent symbolic checks. Independent
Fraction evaluation of T_n against a terminating4F3 construction of M
passes every matrix entry for n0 through24; both spin parities are covered.
See `check_quantum_lp_length_monotonicity.py/.json`,
`manes_monotonicity_symbolic_checks.json`, and extracted source text.

In our normalization transport a to ((n+2)/(n+1))T_n a. This preserves
a0=1, sum a=(n+2)/K, nonnegativity, K M a−a>=0 and the low-rank equality
rows by lower-triangularity. Therefore critical infeasibility propagates
downwards. If n<=2t, detection already contains all End(V), directly
impossible for K>=2; no padding or numerical-table inference is needed.

## Verdict and limits

The all-t, all-integer-K inequality follows from the audited proof and
the stated prior theorem. It permits degenerate codes; proving a packing
inequality is not proving nondegeneracy. The known n7,t1,K2 code is an
equality control: at N=Km the constant term vanishes. Known19 and37 lie
strictly above the bound. Priority must be checked separately against the
intrinsic-code, quantum-metric and spin-code literature; no absence-of-search
argument is an exhaustive novelty claim.
