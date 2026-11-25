# Delayed closure, a single optimal overflow threshold, and the all-input bound

## Result

The frozen three-transfer AH algorithm, modified only by delaying tiny-container closure until an arriving tiny item fails to fit, has asymptotic competitive ratio at most

\[
R=\frac{23211234258164394107066141961880719040528132151}
        {14707121654123980930208343329037931077093556224}
=1.5782309281201736\ldots.
\]

The exact 402-scenario certificate is `single_threshold_certificate.json`; `verify_single_thresholds.py` verifies all804 strict knapsacks, admissibility inequalities, interval coverage, and unchanged original analysis weights. It uses only the Python standard library. An independent advisor verifier reconstructs parameters directly from the primary AH paper and passes the same claim without worker or Pro imports.

The algorithm-specific matching lower bound is proved separately in `coupled/SATURATION_THEOREM.md`. It is not needed for this upper proof. No publication-priority claim is made.

## 1. Algorithm and source-proof obligations

Use exactly the parameters in the frozen `../ah_three_parameter_full_certificate.json`. Its SHA-256 is recorded and checked by the new certificate. This fixes every class endpoint and proportion, including the three previously audited transfers. All published u,v,w analysis choices remain unchanged.

For tiny items, maintain at most one open container with advertised capacity A. Insert s if its actual load L satisfies L+s<=A. Otherwise close that container, create the next type using AH's original quota/placement rule, and insert s. The tiny maximum is d=1/43 and every tiny capacity is at least d, so s fits its new container. All non-tiny rules and priorities remain unchanged, including the largest-temporary-singleton selection. Fix deterministic tie-breaking only where the source leaves a tie unspecified.

This is a deterministic online unit-bin algorithm: advertised capacities certify physical feasibility, no item is moved, and no future information is used. The delayed closure is an actual algorithm change; the stronger lemma below is false for the original proactive closure rule. `tiny_lemma_stress.json` includes an exact original-rule counterexample.

The primary-proof audit verifies that delayed closure preserves:

* the fixed-volume positive/negative matching separation;
* the type-quota discrepancies;
* the all-but-one tiny-container load greater than A-d;
* all temporary/declared large-container and largest-temporary selection invariants.

The tiny open/closed flag is used after the algorithm definition only for insertion and the tiny-load lemma, not for matching. The full source-portability argument, retrospective-threshold endpoint repair, and replacement proof of the threshold-class additive bound are recorded in `AUDIT.md` and the advisor's `phase2/packing_portability_audit.md`. Their role is to justify replacing only AH's tiny amortization step while retaining the remainder of its all-input weight proof. In particular, retrospective scenario selection is analysis, not advice supplied to the algorithm.

## 2. A valid aggregate charge for every threshold

Fix one scenario. Tiny type i has proportion alpha_i, capacity A_i, and required container weight r_i in[0,1]. Define

\[
B=\sum_i\alpha_iA_i>d,\qquad b=\sum_i\alpha_i r_i.
\]

For any c in[0,d], let

\[
\rho_c=\frac b{B-c},\qquad
f_c(s)=\rho_c\bigl(s+(s-c)_+\bigr).
\tag{1}
\]

**Overflow lemma.** For every finite tiny-item subsequence, the total required weight of its tiny containers is at most

\[
\sum_s f_c(s)+p\rho_c+p-1,\tag{2}
\]

where p is the number of supported tiny types. This is an input-independent additive constant.

**Proof.** If m containers have been created, write `n_i=alpha_i m+e_i`. The quota rule gives e_i<1 and sum e_i=0; both the positive discrepancy mass and its negative counterpart are at most p-1. Thus the total advertised capacity is at least Bm-(p-1), and total required weight is at most bm+p-1.

Each closed container's unused capacity is less than the size s of the distinct item that failed to fit and triggered its successor. At most one final container is unfinished and its unused capacity is at most1. For total tiny size T,

\[
Bm-(p-1)-T\leq cm+\sum_s(s-c)_++1.
\]

The sum may safely include all tiny items instead of only triggers, because each summand is nonnegative. Rearrangement gives `(B-c)m<=T+sum(s-c)_++p`, and multiplying by rho_c proves (2). If b=0 the required weight is zero directly. □

## 3. Exact offline fill envelope

For residual capacity r>=0, write r=kd+e with integer k>=0 and 0<=e<d. Then

\[
G_c(r):=\sup_{\substack{0<s_i\leq d\\\sum_i s_i\leq r}}
\sum_i\bigl(s_i+(s_i-c)_+\bigr)
=r+k(d-c)+(e-c)_+.
\tag{3}
\]

A convex pairwise transfer of mass between two non-endpoint item sizes cannot decrease the objective and makes one item reach0 or d. Repetition leaves k copies of d and at most one remainder e. Thus this vector maximizes the objective for a fixed total r; monotonicity handles total size at most r. Zero remainders are omitted. The same formula handles c=0 or c=d. It is continuous and increasing in r and obeys the safe search bound `G_c(r)<=(2-c/d)r`.

For each non-tiny pattern with constant weight W and infimum residual r, its supremal bin weight is therefore `W+rho_c G_c(r)`. All actual non-tiny sizes are strictly above their class lower endpoint, so only patterns with positive infimum residual are enumerated. The usual AH split between normal bins and bins containing a huge item of weight1 is retained. Continuous residual envelopes handle limiting class endpoints without claiming an unattained boundary pattern is a physical bin.

## 4. Mixtures are never better than one threshold

Set `z=(B-c)^(-1)`. A direct rewrite of (1) gives

\[
f_c(s)=b\max\{s z,\ 1+(2s-B)z\}.\tag{4}
\]

For fixed s this is convex in z. For thresholds c_i with probability weights theta_i, define

\[
z_{\rm eff}=\sum_i\frac{\theta_i}{B-c_i},\qquad
c_{\rm eff}=B-z_{\rm eff}^{-1}\in[0,d].
\]

Jensen's inequality yields the **pointwise** domination

\[
f_{c_{\rm eff}}(s)\leq\sum_i\theta_i f_{c_i}(s)
\quad(0<s\leq d).\tag{5}
\]

The additive constant in (2), `pbz+p-1`, is affine in z too. Each single-threshold aggregate lemma is independently valid; (5) does not invoke the invalid principle that the pointwise minimum of arbitrary valid weight functions is valid. The same argument extends to probability measures on[0,d], since z is bounded there.

For r=kd+e, the corresponding envelope is also convex piecewise affine:

\[
\rho_cG_c(r)=b\max\left\{
k+(r+kd-kB)z,\quad
k+1+(2r-(k+1)B)z
\right\}.\tag{6}
\]

Thus minimizing the largest offline pattern weight over this entire charge family is a one-dimensional convex piecewise-linear minimization. No mixture can improve it.

## 5. Exact discovery and full certification

`exact_threshold_search.py` performs rational row generation. It starts with physical non-tiny patterns, forms the two affine lines (6) for every row, exactly minimizes their upper envelope by rational intersections, and prices all non-tiny patterns at the candidate. A violated pattern is added; otherwise the candidate is certified. The discovery uses `exact_nonlinear_pricing.py` and no floating solver. It reproduces the three final thresholds in4,3,5 rounds, respectively.

The final c values differ from d only in these scenarios:

| Scenario (x,y) | c | Scenario bound, approximately |
|---|---|---|
| (49/320,1/6) | 17247296633919791170832825010809060697177 / 766453998323196903862779518275925184912115 | 1.5782166175185446 |
| (533/1600,1/3) | 6816573536910587603199009980750685989373 / 302853064410090280348279687624368940731775 | 1.5782138214141026 |
| (3/7,1/2) | 6457829887103011780070333 / 302161914769161593191102655 | R |

`verify_single_thresholds.py` is separate from discovery: it uses a Fraction-only size-ordered target search rather than discovery's integer-scaled reduced-profit maximization. It checks the exact frozen parameter hash, positive normalized proportions, every breakpoint interval, all unchanged u,v,w, and the three large-threshold feasibility inequalities. It then checks both strict knapsacks for each of402 scenarios. Empty patterns cover tiny-only residuals. Its dominance and density pruning are upper bounds, not heuristic pruning. The result is PASS with29,899 nodes.

For every optimized scenario the certificate includes a probability distribution on active patterns. The weighted pattern objective is a lower bound on the maximum pattern objective for every c. Between residual remainders the weighted expression is affine in z, so checking c=0,d and the finitely many residual remainders certifies its lower bound throughout the continuum. Equality at c_* proves that the reported threshold is globally optimal **within this per-scenario charge family with the fixed non-tiny weights and algorithm parameters**. All-pattern pricing supplies the other direction; optimizing only the active lines would not suffice.

The independent advisor reconstruction uses the primary HTML parameter tables and its own reduced-profit Fraction recursion:402 intervals,804 knapsacks,23,037 nodes, approximately2.84 seconds, PASS. It checks the continuous-c duals and effective thresholds too. The worker verification artifacts and advisor audit agree on the exact fraction R.

## 6. A precisely scoped characterization of local trigger charges

The hinge family also exhausts the undominated certificates of the following **restricted universal local form**. This is not a characterization of arbitrary online analyses.

Assume a common scalar rho>=0, a nonnegative type-independent trigger charge g(s), and constants a_i with `sum alpha_i a_i=0`. Require the local inequality

\[
\rho L+g(s)\geq r_i-a_i
\tag{7}
\]

uniformly for every type and every feasible overflow load L approaching A_i-s from above. This uniform requirement is important: restricting (7) to an uncharacterized reachable subset would be a different claim.

Taking the limiting load and maximizing over types shows

\[
g(s)\geq\max\{0,\max_i(r_i-a_i-\rho A_i)+\rho s\}
\geq[b-\rho B+\rho s]_+.
\tag{8}
\]

The second inequality follows because a maximum is at least its alpha-weighted average. Choosing
`a_i=r_i-rho A_i-(b-rho B)` balances all intercepts and attains (8), while preserving quota neutrality. Summing these constants over actual container counts contributes only O(1) by the quota discrepancies; this need not be the same constant as in (2).

For b>0, rho<b/B leaves a positive per-item charge as s tends to zero, causing unbounded one-bin pricing. For `rho in[b/B,b/(B-d)]`, set c=B-b/rho to obtain exactly(1). For rho>b/(B-d), the optimized hinge has c>d and is simply rho s on(0,d]; it is dominated by the c=d endpoint. If b=0, zero charge is optimal directly.

Hence the single-threshold search is complete for universal quota-neutral **linear-load plus one-trigger** certificates. It does not cover history-dependent potentials, type-dependent trigger charges, state-restricted inequalities, or arbitrary coupled accounting. Those exclusions are explicit rather than presumed impossible. The separate actual saturation construction happens to rule out any better bound for the current fixed algorithm, by a stronger and entirely different argument.

## 7. Reproduction and limits

From the parent algorithm directory, with a one-CPU, one-GiB resource envelope:

```sh
ulimit -v 1048576
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
timeout 290 python phase2/exact_threshold_search.py
timeout 290 python phase2/verify_single_thresholds.py
timeout 290 python phase2/coupled/check_saturation.py
```

The first two commands reproduce the exact upper proof certificate and the restricted continuous-threshold optima. The third checks arithmetic and finite executions in the separate tightness construction. Finite trace tests are not a replacement for its quantified proof.

Primary foundations: [AH algorithm and proof](https://arxiv.org/html/1707.01728); [published ESA version](https://doi.org/10.4230/LIPIcs.ESA.2018.5). The newly claimed rational bound, algorithm modification, and structural theorems still warrant independent human/formal review and a publication-priority search. Internal exact verification is not peer review.
