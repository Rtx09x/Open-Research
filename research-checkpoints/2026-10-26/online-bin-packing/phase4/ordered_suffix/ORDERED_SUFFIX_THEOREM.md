# Earliest-high ordered suffixes replace minimum capacity by mean capacity

## Result and status

For the **unchanged phase2 tiny-Best-Fit AH algorithm**, the new exact all-input upper bound is

\[
R_4=\frac{145158186683463500929311654609983178255750079}
{91975960208053307160010374383175079051657216}
=1.5782187688512288\ldots.
\]

The new chronological proof below has independent advisor analytic PASS. Full worker integer pricing and a separate Fraction recursion pass all402 scenarios /804 strict knapsacks. **Independent primary-derived advisor arithmetic and final prose audit also PASS**: its own source parser and Fraction recursion check all402/804 cases and the physical P floor, without worker imports. See `advisor/phase2/check_packing_ordered_suffix.py`, `packing_ordered_suffix_audit.json`, and `packing_ordered_suffix_audit.md`. This is a small upper improvement, not full-gap closure or a universal lower-bound improvement. Actual Best Fit tightness and external publication priority remain unproved.

All phase2 and phase3 artifacts remain immutable. No algorithm parameter, type quota, matching priority or published non-tiny weight u,v,w changes. The new information is **ordering**: every container after one persistent witness, not merely the final-high subset, must pay large-item load. This is outside the families just ruled out by the phase4 epoch/global-birth barrier.

## 1. Source invariants and notation

Tiny sizes satisfy0<s<=d, d=1/43. Advertised capacities are A_1=17/60 and A_2=1, with unchanged proportions alpha_i. Put B=sum alpha_i A_i, p=2, and let m_i,m count created tiny containers. The source quota gives `m_i=alpha_i*m+e_i`, with `-(p-1)<e_i<1` and `sum e_i=0` at every prefix.

On each tiny item, the decoder searches **all existing advertised tiny containers** and chooses a fitting one with smallest residual capacity. It creates a container only if none fits. Capacities never change. Fixed-volume matching remains safe; the previously audited source matching and temporary/declared-large proofs apply unchanged.

Fix0<=c<=g<=d. Let H_c be the containers with final residual>c and h their count. Let `L_c=sum s*1_(s>c)` and `E_g^birth=sum_birth(s-g)_+`; write E_g for the same sum over all tiny items.

## 2. A witness controls the entire later creation suffix

If H_c is empty the desired h bound is immediate. Otherwise let E be its **earliest-created** member. Take the creation suffix T consisting of every container created strictly after E, and let M_i,M be its type/total counts. Every member of H_c other than E lies in T, so h<=M+1. Importantly, T may also contain many containers that are not final-high.

E's residual remains>c throughout the future because residuals only decrease. At the creation of any C in T, no prior container fits C's birth item s_C. In particular E's residual at that moment is strictly below s_C<=d.

Partition **all of T** into S, containers that ever receive an item<=c, and N, containers that never do.

### S: own-birth targets

At the first<=c item assigned to C in S, E is still an eligible alternative. Best Fit gives C's residual immediately before insertion at most E's current residual, which is strictly below s_C. All earlier contents of C exceed c. Therefore

`A_C-g <= L_c(C)+(s_C-g)_+`.

Charge this term to C's own birth item. There is **no earliest-S exception**: E lies outside T and witnesses every member of S. The weak tie comparison is sufficient because E's residual is strictly below s_C.

### N: successor-within-N targets

Order N by creation time. For every N member C except the last, the birth item of its next N member was rejected by every old container, including C. C's final residual is therefore below that birth size. All of C's contents exceed c, hence

`A_C-g <= L_c(C)+(s_nextN-g)_+`.

Charge it to that next-N birth. These targets are injective and all belong to N, disjoint from the S-own targets. Only the last N member, if any, is exceptional and costs at most Amax-g.

Summing over **all suffix containers** gives the key inequality

\[
\sum_i(A_i-g)M_i\le L_c+E_g^{birth}+A_{\max}-g.
\tag{1}
\]

This improves the previous proof's inequality on only the h_i high containers. Applying quotas to all M_i is now legitimate; applying them directly to h_i would not be.

## 3. Explicit discrepancy and weight constants

Each suffix type count is a difference of two prefix counts. Thus

`M_i=alpha_i*M+delta_i`, with `-p<delta_i<p`.

Put a_i=A_i-g and `K_g=p*sum_i a_i+a_max`. Since all a_i>0, equation(1) implies

`(B-g)M<=L_c+E_g^birth+K_g`.

Hence, using h<=M+1 and E_g^birth<=E_g,

\[
h\le\frac{L_c+E_g}{B-g}+C_g,
\qquad C_g=1+\frac{K_g}{B-g}.
\tag{2}
\]

Every quantity in C_g depends only on the fixed parameters and cutoffs, not the input length or smallest item. For g=d, E_d=0, giving the particularly simple `h<=L_c/(B-d)+O(1)` with **mean** capacity B rather than A_min.

The usual immediate-successor injection bounds final excess residual by `sum_C(residual_C-g)_+<=E_g+1`; only the last-created container is exceptional. Consequently unused capacity U satisfies

`U<=c*m+(g-c)h+E_g+1`.

Advertised capacity is at least Bm-(p-1). Combining this with(2), total tiny volume T, and writing `k=(g-c)/(B-g)`, gives

\[
(B-c)m\le T+kL_c+(1+k)E_g+p+(g-c)C_g.
\tag{3}
\]

Let b be the scenario's alpha-average required tiny-container weight. The original quota argument bounds total required tiny-container weight by bm+(p-1). Thus the valid charge is

\[
f_{c,g}(s)=\frac{b}{B-c}\left[s+k s1_{s>c}+(1+k)(s-g)_+\right].
\tag{4}
\]

Its input-independent additive constant is

\[
\frac{b}{B-c}\,[p+(g-c)C_g]+p-1.
\tag{5}
\]

The denominators are positive because B>d. If b=0 the charge is zero. Finite convex mixtures remain valid with the constants mixed. There are finitely many unchanged scenario intervals, so these constants preserve the asymptotic all-input proof.

The charge simplifies to

\[
\boxed{
f_{c,g}(s)=
\begin{cases}
bs/(B-c),&s\le c,\\
b[s+(s-g)_+]/(B-g),&s>c.
\end{cases}}
\tag{6}
\]

At c=g this is the old overflow hinge. At g=d it is a step whose high-item density is the fixed value b/(B-d).

## 4. Relation to the older family

For identical c,g, the new charge pointwise dominates both old successor q endpoints. At the old lower endpoint q=1/(1-g), large-s weights are identical, while the old low-s density exceeds the new one by a positive multiple of `(g-c)(1-B)`. At the old upper endpoint q=1/(A_min-g), low-s weights are identical, while the old high-s coefficient exceeds the new one by a positive multiple of `(g-c)(B-A_min)`.

This explains why the phase3 analysis-family floor does not apply: its old columns are weakened by the **all-suffix quota conservation**, not merely retuned. Likewise the phase4 global-birth barrier did not retain this ordered suffix.

## 5. Exact pricing and the selected charge

Use the same strictly correct conservative envelopes as before. For a residual r after strict non-tiny class lower endpoints,

`S_c(r)=min(r,d*(ceil(r/c)-1))` for0<c<d, with S_0(r)=r and S_d(r)=0.

The count condition is nc<r, not nc<=r. For r=nd+u,0<=u<d,

`H_g(r)=n(d-g)+max(0,u-g)`.

The valid tiny upper envelope is `rho*r+rho*k*S_c(r)+b/(B-g)*H_g(r)`, rho=b/(B-c). It sums separate maxima conservatively. The exact integer knapsack oracle and separate Fraction target checker retain strict non-tiny capacities, dominance and fractional-density bounds.

In the final scenario(3/7,1/2), choose the simple rationals

`c=997/2100120`, `g=11/500`.

For every other scenario keep its previous cutoff c and set g=d. All published u,v,w and algorithm parameters are identical to the immutable phase3 source. Full pricing yields R_4 exactly. Worker integer search:67,765 nodes; independent worker Fraction search:30,215 nodes.

Stable certificate: `ordered_suffix_certificate.json`, SHA256

`465170f48decd50fe3be2df0a2b59a62af85db1a2931942f1ed89878c56981f2`.

The source certificate's SHA, parameter equality, all scenario endpoints, every u,v,w, and both knapsack forms are checked explicitly. This is not an inference from a few active patterns.

## 6. A single physical pattern proves the whole-family optimum

Let P be the physical pattern with non-tiny types `(1,165,179,205,208,211)`, formal residual

`r_P=997/2100120`,

and non-tiny weight

`K_P=3039661924025609862963147485/1926488896988884623356329984`.

All class sizes can approach their lower endpoints strictly, leaving one tiny item tending to r_P from below. Thus the single-item charge is a physically attainable supremum, including the downward value at c=r_P.

For **every**0<=c<=g<=d, the tiny weight is at least `b*r_P/(B-r_P)`:

- If c>=r_P, equation(6) gives `b*r_P/(B-c)>=b*r_P/(B-r_P)`.
- If c<r_P<=g, it gives `b*r_P/(B-g)>=b*r_P/(B-r_P)`.
- If c<=g<r_P, subtracting the proposed minimum gives

`b*(r_P-g)*(B-2*r_P)/[(B-g)(B-r_P)]>=0`,

because the exact parameters satisfy B>2r_P.

Mixtures preserve this lower bound. Our selected charge has c=r_P, so it attains equality on P; full all-pattern pricing shows no larger value. Consequently

`R_4=K_P+b*r_P/(B-r_P)`

is the exact optimum over the **entire finite convex ordered-suffix two-cutoff charge family** with fixed non-tiny weights and algorithm parameters. This is a principled stopping certificate, not actual algorithm tightness.

An initial floating basis finder exposed a degenerate face: P alone is dual-active. Rather than trying to force a numerical basis certificate, `refine.py` computes the displayed exact floor directly and selects g=11/500 within the rational interval allowed by the other diagnostic rows. The complete knapsack oracle then verifies that choice. No solver is required for reproduction or proof.

## 7. Reproduction and remaining scope

From `online-bin-packing/`, with `PYTHONDONTWRITEBYTECODE=1`, one CPU,1GiB and290-second job limits:

```sh
python phase4/ordered_suffix/refine.py
python phase4/ordered_suffix/check_all.py
python phase4/ordered_suffix/verify_independent.py
python phase4/ordered_suffix/verify_floor.py
```

Each verification is standard-library exact arithmetic and takes seconds. The classic universal lower endpoint remains unchanged; the full packing gap is open. Further cutoff tuning in this family cannot help. Actual realization of P under the full algorithm's container/matching constraints, or a new invariant beyond mean suffix load, remains a separate question.
