# A structural successor: tiny Best Fit and a residual-gap charge

## Status and precise algorithm change

**Worker and independent advisor analytic/source/pricing audits PASS.** The advisor independently reconstructed primary parameters and checked all402 scenarios /804 strict knapsacks with its own Fraction recursion, without worker or Pro imports. The earlier one-open theorem and its matching tightness remain separate frozen anchors. This note concerns a different algorithm, **BF-AH**.

Keep the frozen three-transfer parameters and every non-tiny AH rule. For a tiny item s, inspect **all previously created tiny containers**, including containers that the one-open algorithm would have closed. Among those whose remaining advertised capacity is at least s, choose one with the smallest such remaining capacity; break equal residuals by creation order. If none fits, create the next quota-selected type by the original minimum-index rule, use the original AH matching/placement procedure, and insert s.

Advertised volumes never change. Refilling a tiny container cannot overflow its bin because its actual load remains at most that advertised volume and matching respects the sum of advertised volumes. No item moves, no future input is used, and no extra capacity is supplied. The number of eligible tiny containers is not artificially bounded; the classic online model permits this memory/state.

The candidate certified bound is

\[
R_{BF}=\frac{174191383514152461065273968497444592350661}
               {110371486054812972793114744355465098952704}
=1.5782281252210837\ldots.
\]

No matching lower bound for BF-AH is claimed. In particular, the earlier one-open saturation construction does not apply to it.

## 1. Basic source invariants

Tiny type counts retain the original quota discrepancy. Matching and all non-tiny container transitions see the same fixed advertised volume at creation; additional insertions into existing tiny containers change no advertised volume, bin association, or other class's type counts.

Immediately before each new tiny container is created, every older tiny container has remaining capacity less than the arriving item, hence less than or equal to d=1/43. Afterwards its remaining capacity can only decrease. Thus, at every time, all tiny containers except possibly the most recently created have load greater than A_i-d. This replaces the original one-open proof of exactly the same numerical load invariant. Source proofs that use that invariant still apply; no claim that there is only one eligible tiny container is made.

The source-portability audit must additionally confirm that the original open/closed eligibility flag is not needed elsewhere. The earlier independent audit located its uses only in insertion and the load lemma. Largest-temporary-singleton and threshold-class arguments depend on advertised volumes and creation operations, which remain unchanged.

## 2. The high-residual lemma

Fix 0<=c<=d and a finite input. Let H be the tiny containers with **final remaining capacity greater than c**. Let L_{>c} be the total volume of tiny items strictly larger than c, and let A_min be the smallest supported tiny capacity. Here A_min=17/60>d.

**Lemma.** Except for at most two containers in H, each type-i container in H contains more than A_i-d total volume of items strictly larger than c. Consequently

\[
|H|\leq \frac{L_{>c}}{A_{\min}-d}+2.\tag{1}
\]

**Proof.** Exclude the earliest-created member of H and, if necessary, the most recently created tiny container overall. Consider another container C in H and an earlier member E of H. E's remaining capacity is always at least its final remaining capacity, which is greater than c. At the moment C was created, E failed to fit C's first item, so E's remaining capacity was less than that item's size and hence at most d. It remains strictly below d thereafter.

If C ever receives an item s<=c, consider its first such item. E is an available fit at that moment. Best Fit therefore selects C only if C's remaining capacity before insertion is at most E's, hence strictly less than d. C already has load greater than A_i-d, and all previously inserted items in C are larger than c by definition of the first small item.

If C never receives an item at most c, all its load consists of items larger than c. Since C is not the last-created container overall, the creation of a later container forced C's remaining capacity below d; its final load is therefore greater than A_i-d. This proves the claim. The relevant item sets belong to distinct containers, so summing gives (1). □

This is a chronological statement about the real Best Fit execution, not a relaxation of offline patterns. It fails to follow for a one-open policy because E would not remain available.

## 3. All-input step charge

In a fixed AH scenario, let p be the number of supported tiny types,

\[
B=\sum_i\alpha_i A_i,\qquad b=\sum_i\alpha_i r_i,
\qquad a=A_{\min}-d>0.
\]

For m tiny containers, total tiny size T, and total remaining capacity U, quota discrepancies give `sum A_i n_i>=Bm-(p-1)`. Every container except possibly the most recent has remaining capacity less than d. Splitting by H therefore gives

\[
U\leq cm+(d-c)|H|+1.
\]

Using (1),

\[
(B-c)m\leq T+\frac{d-c}{a}L_{>c}+p+2(d-c).\tag{2}
\]

Total required tiny-container weight is at most bm+p-1. Define

\[
\rho=\frac b{B-c},\qquad k=\frac{d-c}{A_{\min}-d},\qquad
f_c(s)=\rho s\bigl(1+k\mathbf1_{\{s>c\}}\bigr).
\tag{3}
\]

Then every finite input satisfies

\[
\sum_i r_i n_i\leq\sum_s f_c(s)
+\rho[p+2(d-c)]+p-1.\tag{4}
\]

The constant is input-independent. If b=0, required weight is zero directly. For c=d, this reduces to the familiar linear tiny charge. No tiny-type parameter is changed.

## 4. Exact pricing at the discontinuity

For 0<c<d and residual r>0, let n be the largest nonnegative integer satisfying **n c<r**, equivalently `n=ceil(r/c)-1`. The maximum volume assignable to items strictly larger than c is

\[
V_c(r)=\min\{r,nd\}.\tag{5}
\]

Indeed, there can be at most n such items, each at most d. If r<=nd, use n items of size r/n (when n>0); their sizes are strictly greater than c and at most d. If r>nd, use n items of size d and split the remaining volume into items at most c. The remainder is at most c because r<=(n+1)c and d>=c. When n=0, use only small items. Thus the exact envelope is

\[
F_c(r)=\rho\,[r+kV_c(r)].\tag{6}
\]

At r=nc it is incorrect to allow n large items: each would need size strictly above c. Formula (5) deliberately uses the strict inequality. The envelope is left-continuous at these points, with possible upward jumps immediately to their right. A non-tiny pattern has actual residual strictly below its infimum residual r, so evaluating (6) at r is a valid upper bound and equals the limiting supremum. Continuous-hinge pricing must not be reused here.

The endpoints are handled separately: at c=d no tiny item is larger than c, so V=0 and F_c(r)=rho r; at c=0 all tiny items are larger than c, so V=r and F_c(r)=rho(1+k)r. The certified choices use only c>0.

The envelope is increasing, and its excess over rho r is increasing. A safe density upper bound is rho(1+k). These facts justify the exact dominance and branch bounds used by both checkers.

## 5. Fixed rational thresholds and all402 scenarios

Use c=d except:

* c=3/200 for scenario(49/320,1/6);
* c=1/60 for scenarios(533/1600,1/3) and(3/7,1/2).

The latter value is a physical residual breakpoint of the pattern huge+class165+class172; it is not a fitted decimal. These are a bounded set of simple choices, not a claimed optimization over every threshold or new algorithm parameter.

`check_all_cases.py` reconstructs all scenarios and exactly maximizes both strict knapsacks using integer-scaled reduced profits and (5). `verify_step_independent.py` instead uses Fraction-only size-ordered target search, independently reconstructed weights, checks interval coverage and all admissibility constraints, verifies unchanged parameters/u/v/w, and replays every maximizing pattern. Both use only the standard library.

The bottleneck pattern is huge+165+179+205+208+211 with tiny residual997/2100120. It is below c, so its tiny charge is purely linear. The same exact supremum appears in the normal and huge-separated cases of scenario(3/7,1/2). No original per-scenario printed bound is reused without pricing.

Results: worker integer maximization67,462 nodes; separate worker Fraction target29,963 nodes; independent primary-derived advisor verifier23,108 nodes. All pass the same exact fraction. Independent files are `advisor/phase2/check_packing_best_fit.py` and `packing_best_fit_audit.json`, accompanied by the source/lemma audit note.

`stress_gap_lemma.py` additionally tests25,000 exact tiny arrivals,2,500 high-gap/capacity-charge checks, and6,114 exact envelope constructions, including sizes exactly at either side of the strict threshold. These tests supplement the proof; they are not its justification.

## 6. Reproduction and limitations

From `online-bin-packing/`:

```sh
ulimit -v 1048576
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
timeout 290 python phase2/best_fit/check_all_cases.py
timeout 290 python phase2/best_fit/verify_step_independent.py
```

The previous one-open algorithm and its exact tightness are retained independently. This step-charge lemma is not a contradiction: Best Fit keeps earlier holes available and violates the one-open hypothesis of that lower-bound architecture.

Exact pricing alone is not an algorithm theorem; it must be combined with the chronological lemma, source-proof portability, and the ordinary AH all-input charging theorem. Independent advisor audit and external human/formal review are distinguished. No optimality or publication priority is asserted.

Primary source for unchanged AH machinery: [Balogh et al., A New and Improved Algorithm for Online Bin Packing](https://arxiv.org/html/1707.01728).
