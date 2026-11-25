# Single-threshold tiny charges and the exact successor bound

## Independent arithmetic audit
`check_packing_single_thresholds.py` reparses the primary AH source through the advisor's frozen parser, verifies the same three container-proportion transfers and all published analysis weights, and independently prices all402 scenarios/804 strict knapsacks. Its reduced-profit-density recursion differs from the worker's raw-weight-size recursion. All checks passed with23,037 nodes in2.84seconds. Three exact continuous-threshold duals also pass.

The delayed-tiny AH variant therefore has the candidate rigorously audited asymptotic upper ratio

    23211234258164394107066141961880719040528132151
    /14707121654123980930208343329037931077093556224
    =1.5782309281201736... .

Algorithm/theorem portability is audited separately in `packing_portability_audit.md`; this does not apply to unchanged proactive tiny closure. Literature priority remains unestablished.

## Mixtures reduce to one threshold
Let d be the maximum tiny size, B the average advertised capacity, and b the average required container weight. For c∈[0,d], the valid charge is

    f_c(s)=b/(B−c) [s+(s−c)_+].

Set z=(B−c)^−1. Then exactly

    f_c(s)=b max{sz,1+(2s−B)z}.

This is convex in z for every s. Hence a convex mixture of thresholds is pointwise at least the single threshold with z_eff=Σtheta_i z_i. Its c_eff=B−1/z_eff remains in[0,d]. The earlier additive quota constant is affine in z, so this substitution does not worsen that constant either.

For each non-tiny pattern the extremal tiny fill consists of q items of size d and a remainder e, giving G_c(r)=r+q(d−c)+(e−c)_+. Each pattern's total is convex piecewise linear in z. The maximum over all patterns is therefore a one-dimensional convex piecewise-linear objective. The supplied two-pattern duals prove the three relevant minima over the whole continuous c interval, not merely a tested grid. This is optimality in this charge family with other parameters/weights fixed, not algorithm optimality.

## Broader local-certificate classification (analytic audit)
Assume a universal local certificate of the form

    rho L+g(s) >= r_i−a_i

for every type-i overflow L+s>A_i, with rho≥0, g(s)≥0 type-independent, and quota-neutral constants Σalpha_i a_i=0. Assume it must hold uniformly as L decreases to A_i−s. Then

    g(s)>=max_i(r_i−a_i−rho A_i+rho s)_+
         >=(b−rho B+rho s)_+.

Equality in the last lower bound is attainable by choosing

    a_i=r_i−rho A_i−(b−rho B).

Thus the least item charge within this local form is rho s+(b−rho B+rho s)_+. For b>0, rho<b/B gives a positive limiting charge as s tends to0 and unbounded single-bin pricing. For rho>b/(B−d), the hinge is inactive on[0,d] and its linear charge is dominated by the endpoint c=d. The remaining rho correspond exactly to c=B−b/rho in[0,d]. The case b=0 is trivial zero charge and should be separated.

Bounded deterministic quota discrepancy makes Σn_i a_i an additive constant; it need not equal the earlier proof's particular constant, which is immaterial asymptotically. This classification does not cover type-dependent load slopes, history-dependent charges, correlations between successive overflow events, or a certificate imposed only on a narrower characterized reachable-state set. Those are concrete ways to leave the exhausted local family.
