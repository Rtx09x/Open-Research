# Disjoint-successor conservation and the optimal two-cutoff mixture

## Result and scope

For the **unchanged phase2 tiny-Best-Fit AH algorithm**, the exact all-input asymptotic upper bound is

\[
R=\frac{17309229457317341044853136044527531250227952497}
{10967548450040323523815819160873924866844131328}
=1.5782222924443705\ldots.
\]

Worker integer maximization and a separate Fraction recursion pass all 402 scenarios / 804 strict knapsacks. The new chronology lemma has an independent advisor analytic PASS. **Independent primary-derived advisor arithmetic and full prose audit also PASS**: its own parser and Fraction recursion check all402/804 cases, all30 endpoint inequalities, physical-row equality, chronology, strict thresholds and the additive constant. The advisor imports no worker or Pro code. See `advisor/phase2/check_packing_successor_mixture.py` and `packing_successor_mixture_audit.json`. This document proves an all-input upper bound and an exact optimum within a specified analysis family, **not actual algorithm tightness, optimality of online bin packing, or a solution of the classic packing gap**. The published universal lower endpoint is unchanged. Publication priority and external human/formal review are unestablished.

All advertised capacities, proportions, matching priorities, non-tiny handling and published u,v,w are unchanged. Only the final scenario's tiny charge changes. Earlier phase1, phase2 and phase3 step-mixture certificates are preserved.

## 1. Chronology with no double-charged creation item

Let tiny item sizes lie in (0,d], d=1/43, and advertised capacities be A_1=17/60 and A_2=1. Their proportions are alpha_i; write B=sum_i alpha_i A_i, m_i for their creation counts, m=sum_i m_i and p=2. The unchanged quota rule gives `m_i=alpha_i*m+e_i`, `e_i<1`, and `sum e_i=0`.

Every arriving tiny item searches **all prior advertised tiny containers** and enters a fitting one with least residual advertised capacity. A new container is created only if none fits. Capacities never change. Physical matching remains safe because it uses these fixed advertised volumes.

Fix 0<=c<=g<=d. Let H_c be the containers with final residual greater than c, h_i their type counts, and h=sum_i h_i. Define

\[
L_c=\sum_s s1_{s>c},\qquad E_g=\sum_s(s-g)_+,
\qquad a_i(g)=A_i-g>0.
\]

The stronger conservation inequality is

\[
\boxed{\sum_i a_i(g)h_i\le L_c+E_g+2a_{\max}(g).}\tag{1}
\]

Partition H_c into S, whose containers ever receive an item <=c, and N, whose containers never do.

**S containers.** Exclude the earliest-created H_c if it belongs to S. Every remaining C in S has an earlier final-H_c container E. At C's creation, E did not fit C's creation item s_C, so E's residual was strictly below s_C. It subsequently only decreases. At the first <=c item assigned to C, E still has residual >c and is a feasible alternative. Best Fit implies that C's pre-insertion residual is at most E's, hence <s_C. All earlier contents of C exceed c, so

`A_C-g <= L_c(C)+(s_C-g)_+`.

Charge C to its **own** creation item.

**N containers.** Order N by creation time and exclude its last member, if any. For any remaining C, take the creation item s_nextN of the **next member of N**, not necessarily the next container overall. C already existed at that event; creation implies that no old container fitted s_nextN. Thus C's final residual is <s_nextN. All of C's contents exceed c, giving

`A_C-g <= L_c(C)+(s_nextN-g)_+`.

The successor map on N is injective. Its birth-item targets belong to N, whereas all S-own targets belong to S. Thus **no creation item is charged twice**. There are at most two exceptions, contributing at most2 a_max(g). Sum the inequalities and use that creation items are a subset of all items to prove(1). The final S/N classification is an ex-post proof device; it gives the online algorithm no future information.

Also, each container except the last-created has final residual less than the creation-item size of its immediate successor. This assignment is injective; the last residual is at most1. Hence, for final residuals r_C,

\[
\sum_C(r_C-g)_+\le E_g+1.\tag{2}
\]

The elementary inequality `r<=c+(g-c)1_(r>c)+(r-g)_+` then bounds total unused capacity U by

\[
U\le cm+(g-c)h+E_g+1.\tag{3}
\]

These arguments include strict comparisons explicitly and apply to every finite input prefix. No smallest item, exact threshold item, open-container flag or lookahead is assumed.

## 2. Valid two-cutoff item weights and additive constants

For q>=0 define

\[
v_i=(1-q(A_i-g))_+,\quad
\kappa_g(q)=\sum_i\alpha_i v_i,\quad
C_h=2q(A_{\max}-g)+\sum_i v_i.
\]

Termwise `h_i<=q(A_i-g)h_i+v_i m_i`. Equation(1) and the quota upper errors yield

\[
h\le qL_c+qE_g+\kappa_g(q)m+C_h.
\]

Advertised capacity is at least Bm-(p-1). With T the total tiny volume, equation(3) gives

\[
\mathcal D(c,g,q)m\le
T+(g-c)qL_c+[1+(g-c)q]E_g+p+(g-c)C_h,\tag{4}
\]

where

\[
\mathcal D=B-c-(g-c)\kappa_g(q)\ge B-g>0.
\]

Let b be the original scenario's alpha-average required tiny-container weight. The quota argument bounds aggregate required tiny-container weight by bm+(p-1). Put rho=b/mathcal D. The valid nonnegative item charge is

\[
f_{c,g,q}(s)=\rho\left[s+(g-c)q\,s1_{s>c}
+[1+(g-c)q](s-g)_+\right].\tag{5}
\]

Its aggregate sum bounds required tiny-container weight, up to the input-independent additive constant

\[
\rho[p+(g-c)C_h]+p-1.\tag{6}
\]

For b=0 the charge is zero. Convex mixtures of finitely many valid charges remain valid, with the constants mixed as well. Since the algorithm and the finitely many scenario intervals are unchanged, these constants preserve the all-input asymptotic theorem.

At g=d the excess vanishes and (5) is exactly the earlier type-resolved step family. At c=g it is `b/(B-c)[s+(s-c)_+]`, the earlier overflow hinge. The new disjoint-successor information is strictly stronger than the previously tested factor-two excess estimate.

The original AH matching and temporary/declared-large-container proofs are unchanged: they depend on advertised volumes, creation events and original type changes, not tiny eligibility flags. The all-prior-container Best Fit decoder's applicability was independently checked in phase2. The only new proof obligation here is the displayed tiny charge.

## 3. Exact conservative pricing, including strict thresholds

For a formal residual r>0 left after non-tiny lower-endpoint sizes, actual tiny volume is strictly less than r. The supremum of volume in tiny items strictly greater than c is

\[
S_c(r)=\min\{r,d(\lceil r/c\rceil-1)\}\quad(0<c<d),
\]

with S_0(r)=r and S_d(r)=0. The condition is **nc<r**, not nc<=r; the downward threshold value at r=c must be retained.

Write r=nd+u with n=floor(r/d) and0<=u<d. Concentrating mass into size-d items gives the exact excess supremum

\[
H_g(r)=n(d-g)+\max(0,u-g).
\]

A valid envelope for a single charge is

\[
F_{c,g,q}(r)=\rho\{r+(g-c)qS_c(r)+[1+(g-c)q]H_g(r)\}.\tag{7}
\]

For mixtures, sum these envelopes. The separate maxima need not be simultaneously attainable for every r; their sum is intentionally a conservative upper bound. Exact knapsack pricing therefore proves an upper bound even when it overestimates the best tiny partition.

`successor_cutoff/pricing.py` uses exact common-denominator integer arithmetic and strict non-tiny total sizes. It removes the linear tiny-density term, applies monotone residual-envelope dominance, and bounds remaining reduced profit by the maximum of non-tiny reduced-profit density and tiny bonus density. The hinge-density factor is (d-g)/d. `verify_independent.py` imports neither that oracle nor its optimizer; it uses Fraction arithmetic, a different size-ordered frontier and target-based recursion. Both cover all402 scenarios /804 cases, including the special huge-item case.

## 4. Selected three-charge mixture and exact full bound

Only the scenario (x,y)=(3/7,1/2) changes. Put p_0=997/2100120. The three components (c,g,q) are

1. `(p_0,1/60,60/59)`;
2. `(p_0,29/1254,1254/1225)`;
3. `(p_0,29/1254,12540/3263)`.

Their positive weights are, respectively,

```
1814089728233975698222416793549469703167 /
6864854906992031222261373930296964022272

33557708367518006482756014246314236261079177977195 /
48154593549543570133439478104115676207783990001664

8977085537304660166459832645657079620254096550615 /
230963698691329345640015274610480743292889877970944
```

They sum exactly to1. Every other scenario embeds its previous step charge with g=d. The exact global maximum is R above. Certificate `successor_mixture_certificate.json` has SHA256

`48d1e32cefcb5f2c999de480684332a4c2b2b411c4912ffb7e8754ea9f56d64d`.

All parameters and u,v,w are compared exactly to the preserved source certificate. The worker integer oracle visits67,640 nodes; the separate Fraction checker visits30,122. Neither relies on a numerical solver's status. SciPy was used only to discover a candidate LP basis; all its coefficients, positive primal/dual solutions, inequalities and final knapsacks are reconstructed exactly. Replaying the certificate does not need SciPy.

## 5. The entire continuous mixture family is now optimized

This section concerns all finite convex mixtures of (5), with `0<=c<=g<=d`, `q>=0`, the current algorithm parameters and non-tiny weights fixed. It is **not** a lower bound on actual algorithm performance.

Three physical bin patterns attain R in the selected mixture:

| Pattern types | Tiny residual | Non-tiny weight constant |
|---|---|---|
| P:1,165,179,205,208,211 |997/2100120|3039661924025609862963147485/1926488896988884623356329984|
| G:1,165,172 |1/60|8724615875584559265456187/5578635802091364739448832|
| Q:1,165,179,187 |29/1254|350934298064558974481767473469/225399200947699500932690608128|

Every residual is below d. Increase all non-tiny sizes a sufficiently small amount above their class lower endpoints and use **one tiny item** tending to the displayed residual from below. This simultaneously realizes the step and excess suprema of every mixture component, including equality cutoffs. Thus these are physical supremum rows, not artifacts of a loose envelope.

The exact positive dual weights, in P,G,Q order, are

\[
(435637141840686929,\ 2137549740104520,\ 150268380653160)
/437924959961444609.
\]

Let V(c,g,q) be the corresponding weighted average of the three physical pattern weights. We prove V>=R everywhere by a finite endpoint reduction.

### 5.1 Reduce q to its two type endpoints

Write a=17/60. For q<1/(1-g), both terms of kappa are positive and

`mathcal D=(B-g)[1+(g-c)q]`.

For s>c, the charge is `b[s+(s-g)_+]/(B-g)`, independent of q; for s<=c it decreases with q. Hence q=1/(1-g) pointwise dominates the entire lower q range. For q>1/(a-g), kappa=0 and the charge is nondecreasing in q, so q=1/(a-g) dominates. Between these endpoints, kappa is affine in q; both the numerator of V and its positive denominator are affine in q. A fractional-linear function is monotone or constant on such an interval, so its minimum is at an endpoint.

### 5.2 Reduce c to0, g, or a physical residual

Fix g and either q endpoint. Between physical residuals, V has an affine numerator and a common positive affine denominator in c. Its minimum occurs at interval endpoints. At c=s, the indicator `s>c` drops, causing a downward jump; therefore a left-limit endpoint cannot beat the actual threshold value. It suffices to use `c in {0,g,p_0,1/60,29/1254}`, restricted to c<=g.

### 5.3 Reduce g to0, d, or a physical residual

For fixed c equal to0 or a residual, the endpoint formulas simplify exactly to

\[
f_{c,g,1/(1-g)}(s)=
\begin{cases}
\dfrac{bs(1-g)}{(1-c)(B-g)},&s\le c,\\
\dfrac{b[s+(s-g)_+]}{B-g},&s>c;
\end{cases}
\]

\[
f_{c,g,1/(a-g)}(s)=
\begin{cases}
\dfrac{bs}{B-c},&s\le c,\\
\dfrac{b(a-c)[s+(s-g)_+]}{(B-c)(a-g)},&s>c.
\end{cases}
\]

On every g interval between physical residuals, each weighted average has a common positive affine denominator and an affine numerator. The hinge terms are continuous at their breakpoints. Thus the minimum occurs at g endpoints. On the diagonal c=g, both q choices reduce to the same hinge `b[s+(s-g)_+]/(B-g)`, with the same endpoint property.

Consequently it suffices to test

`g in {0,p_0,1/60,29/1254,d}`,
`c in the same set with c<=g`,
`q in {1/(1-g),1/(a-g)}`.

There are30 distinct parameter triples. `verify_family.py` independently rebuilds all three physical rows, recomputes the positive dual and checks **all30 exact inequalities V>=R**. Each selected mixture component attains equality. There are four dual-flat endpoints: both q endpoints at(c=p_0,g=1/60), and both at(c=p_0,g=29/1254); the selected primal uses three of them. No uniqueness is asserted. Therefore every finite mixture in this entire continuous family has some physical pattern of weight at least R. The complete all-pattern upper certificate attains R, closing both directions.

This is a principled stopping certificate for this charge family. More parameter sweeps within it cannot improve the bound. A future gain must use a stronger chronological invariant, non-tiny/global matching information, a genuinely different charging family, or an algorithm change. The actual worst-case ratio of the Best Fit algorithm remains unknown.

## 6. Reproduction and audit boundary

From `online-bin-packing/`:

```sh
ulimit -v 1048576
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
timeout 290 python phase3/successor_mixture/check_all.py
timeout 290 python phase3/successor_mixture/verify_independent.py
timeout 290 python phase3/successor_mixture/verify_family.py
```

These are standard-library verification jobs taking seconds. Optional discovery is `optimize.py` and additionally needs SciPy; its floating output is not accepted as a proof. The primary AH framework is [arXiv1707.01728](https://arxiv.org/html/1707.01728). The source-portability audit and unchanged algorithm are preserved in phase2. The lower-fork obstruction elsewhere in phase3 is a separate restricted result and must not be confused with this global upper bound.

Finite falsification controls also pass: all4^9 synthetic size sequences and an explicit longer mixed S/N history check the birth-target injection. These are supplementary tests, not a substitute for the universal chronology proof.
