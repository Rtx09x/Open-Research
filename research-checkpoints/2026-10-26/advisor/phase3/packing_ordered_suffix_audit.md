# Ordered-suffix Best Fit audit

2026-10-26 00:02 UTC. **Analytic, exact arithmetic, and final prose PASS.**

Audited worker note: `online-bin-packing/phase4/ordered_suffix/ORDERED_SUFFIX_THEOREM.md`.
Certificate SHA256: `465170f48decd50fe3be2df0a2b59a62af85db1a2931942f1ed89878c56981f2`.
Independent checker: `check_packing_ordered_suffix.py`; result `packing_ordered_suffix_audit.json`.

## Chronology
The earliest final residual>c container E remains eligible for all later items≤c. At any later container C's creation, no-fit implies gap(E)<birth(C)≤d. Therefore the first≤c item assigned to C, if any, finds C's gap≤gap(E)<birth(C). The earlier load consists entirely of>c items. This witnesses EVERY later-created C, including containers not final-high; applying suffix type quotas is consequently legitimate.

Partition the entire suffix into S (ever takes≤c) and N (never does). S charges its own birth excess. Every N except its last charges the next N's birth excess. These birth targets are injective and disjoint. Only last N is exceptional. Thus sum_suffix(A_i−g)≤L_c+E_g^birth+(Amax−g). Suffix counts differ from alpha_i M by less than p because each is a difference of two prefix quota errors in (−(p−1),1). The note's conservative K_g=p sum_i(A_i−g)+(Amax−g) and C_g=1+K_g/(B−g) are valid.

Immediate-successor no-fit bounds total residual excess above g by E_g+1. Combined advertised-capacity and scenario-weight quota errors yield the displayed additive constant b/(B−c)[p+(g−c)C_g]+p−1. It is independent of input length and the smallest tiny item. No matching-saturation assumption enters the new argument; capacities and all-container eligibility are fixed as in the previously audited Best Fit variant.

## Arithmetic
Independent primary-source parameter/weight parser, with no worker code imports, checked all402 scenario intervals and804 strict knapsacks in43066 Fraction nodes. Both algorithm parameters and every published non-tiny analysis weight are unchanged. Result:

`145158186683463500929311654609983178255750079 / 91975960208053307160010374383175079051657216 = 1.5782187688512288…`.

The strict step envelope uses n*c<r, including zero bonus at c=d. The hinge envelope is separate; summing its maximum with the step maximum is conservative. All lower class endpoints remain strict.

## Scope and stopping certificate
Physical pattern P independently gives exactly the reported R via K_P+b p/(B−p). For c≤g<p, the difference from this floor is b(p−g)(B−2p)/[(B−g)(B−p)]≥0; the other two cutoff regions are immediate. Approaching strict non-tiny endpoints from above makes the residual approach p from below, so c=p's downward value is the correct physical supremum. Every finite convex mixture inherits the floor.

This proves optimality of this specified charge family with fixed non-tiny weights and algorithm parameters, NOT actual algorithm tightness or a universal online-packing lower bound. Earlier phase3 family floors remain valid but are superseded as upper analyses by the genuinely stronger all-suffix invariant. The global packing problem remains open.
