# Type-resolved residual conservation: mixtures improve the bound, and an exact family floor

## Result and status

Keep **exactly the phase2 Best Fit AH algorithm**, including every class endpoint, container proportion, tiny Best Fit rule, matching priority, and non-tiny rule. Only the upper-bound analysis changes. The new all-input upper bound is

\[
R=\frac{157824873778621055499177374437271627462312087669}
        {100001622932035466916943663859692439386084868096}
=1.578223124297535\ldots.
\]

Worker integer maximization and a separate Fraction target checker pass all402 scenarios /804 strict knapsacks. **Independent primary-derived advisor audit also PASS:** its own Fraction recursion checks all cases, and its independently rebuilt physical pattern constants pass the entire-family dual endpoint test. The source algorithm and all phase2 artifacts remain unchanged. This is a small global **upper-bound** improvement, not a universal lower-bound improvement or a solution of the full packing gap. The true competitive ratio of the Best Fit variant is not proved here.

The new ingredient retains tiny-container type information in the chronological residual-gap lemma. A single certificate from the enlarged family cannot improve the old bound; a convex mixture can. An exact dual further proves that the displayed mixture is optimal over the **entire convex family defined below**, with the algorithm parameters and non-tiny weights fixed. This restricted analysis optimum is not algorithm optimality.

## 1. Type-resolved high-residual conservation

Let d=1/43. Tiny type i has capacity A_i and quota alpha_i. Here the two capacities are17/60 and1, with the unchanged published proportions. Put a_i=A_i-d>0 and B=sum alpha_i A_i.

For a fixed c in[0,d], let h_i count final type-i containers whose remaining capacity is greater than c. Let L_c be the total size of tiny items strictly larger than c, and let m_i and m be the type and total container counts.

The independently audited phase2 chronology lemma says that, except for at most two containers in the union of the h_i, each high-residual type-i container already received more than a_i volume of >c items. Consequently

\[
\sum_i a_i h_i\leq L_c+2a_{\max}.\tag{1}
\]

This is stronger than replacing every a_i by a_min. Also h_i<=m_i and the fixed quota gives `m_i=alpha_i m+e_i`, e_i<1, sum e_i=0.

For any q>=0, define

\[
v_i(q)=(1-qa_i)_+,\qquad
\kappa(q)=\sum_i\alpha_i v_i(q),\qquad
C_h(q)=2qa_{\max}+\sum_i v_i(q).
\]

Termwise `h_i<=q a_i h_i+v_i(q)m_i`. Sum and apply(1) and the quota upper errors to obtain

\[
h:=\sum_i h_i\leq qL_c+\kappa(q)m+C_h(q).\tag{2}
\]

All but the last-created tiny container have final remaining capacity below d. Thus total unused capacity is at most `cm+(d-c)h+1`. Advertised capacity is at least Bm-(p-1), where p is the number of supported types. For total tiny volume T, (2) gives

\[
\mathcal D(c,q)m\leq T+(d-c)qL_c+p+(d-c)C_h(q),\tag{3}
\]

where

\[
\mathcal D(c,q)=B-c-(d-c)\kappa(q)\geq B-d>0.
\]

In a fixed AH scenario let b=sum alpha_i r_i be the required-weight mean. The required tiny-container weight is at most bm+p-1. Hence the item charge

\[
f_{c,q}(s)=\frac b{\mathcal D(c,q)}s
\left[1+(d-c)q\mathbf1_{\{s>c\}}\right]\tag{4}
\]

is valid with input-independent additive constant

\[
\frac b{\mathcal D(c,q)}[p+(d-c)C_h(q)]+p-1.
\]

If b=0 the required weight is zero. At c=d, the extra term vanishes and the original linear tiny charge is recovered. Formula(4) changes no online decisions.

## 2. Mixture validity and conservative exact pricing

Any fixed finite convex combination of valid aggregate inequalities(3)–(4) is valid, with the same convex combination of their additive constants. We never take an unjustified pointwise minimum of valid charges.

For 0<c<d and residual r>0, the exact one-component envelope is

\[
F_{c,q}(r)=\frac b{\mathcal D(c,q)}
\left[r+(d-c)q\min\{r,nd\}\right],\qquad
n=\lceil r/c\rceil-1.
\tag{5}
\]

The strict inequality nc<r is essential because high items have size strictly greater than c. Endpoints: at c=0 all tiny volume is high; at c=d none is high and the extra coefficient is zero. The envelope is increasing and left-continuous, so evaluating it at the strictly larger infimum residual of a non-tiny pattern is safe.

For a mixture we use the **sum of the component envelopes** as an upper bound. We do not claim that one tiny multiset simultaneously maximizes all components for every residual. Exact pricing means exact maximization of this valid upper envelope over all non-tiny patterns. The excess over its linear base density is increasing, and the sum of component maximum densities supplies a safe branch bound.

At the two active patterns below, the residual is less than d and a single tiny item approaching that residual from below simultaneously attains all components' limiting weights. Thus their dual lower certificate is physical, not an artifact of summing incompatible maxima.

## 3. The selected mixture

All scenarios retain the phase2 analysis except(3/7,1/2). In that scenario use

\[
\theta f_{p,1/a_2}+(1-\theta)f_{g,1/a_1},
\]

with

\[
p=997/2100120,\quad g=1/60,\quad
1/a_2=43/42,\quad1/a_1=2580/671,
\]

\[
\theta=\frac{39520943872233333946215}{42253719288965378384366}.
\]

Every published u,v,w and every algorithm parameter remains unchanged. The two active non-tiny patterns are

* P: huge +165+179+205+208+211, with residual p;
* G: huge +165+172, with residual g.

Their exact non-tiny weights are stored in `type_mixture_certificate.json`. `optimize_fixed_mixture.py` forms their affine lines in theta and checks the proposed intersection by exact all-pattern pricing. It closes in the first pricing round after endpoint initialization. `check_all_mixture.py` then reprices every scenario; no unchanged printed bound is assumed. The global maximum is R, and all other scenarios are below1.578171.

`verify_mixture_independent.py` uses a separate Fraction-only size-ordered target recursion, verifies exact parameter/source hashes and unchanged analysis weights, reconstructs every interval and admissibility inequality, checks all804 knapsacks, and validates the active physical patterns and positive dual. Worker results:67,632 maximization nodes and30,087 target-verification nodes.

The advisor independently reparsed primary AH parameters, imported no worker or Pro code, and passed all402/804 cases in42,934 Fraction nodes (approximately2.47seconds). Its certificate binding is SHA256`63445fa665054757e516df709ff57bad35a525b9c172f7f93bed9badf66b461d`. Independent files: `advisor/phase2/check_packing_type_mixture.py` and `packing_type_mixture_audit.json`. The eight endpoint dual inequalities and their continuous-family applicability were independently checked too.

## 4. Why every single type-resolved charge hits the old floor

This explains why the mixture is a structural improvement rather than merely a better scalar setting.

For any q>=0,

\[
1-\kappa(q)=\sum_i\alpha_i\min\{qa_i,1\}
\leq q(B-d).
\]

Therefore the density on items above c is at least b/(B-d). The small-item density is at least b/(B-c), since kappa>=0.

In the final scenario, if c<g, pattern G can have one tiny item approaching g from below and still above c. Its weight is at least

`K_G+b*g/(B-d)=1.5782320611603713...`,

the earlier frozen three-transfer analysis value. If c>=g, pattern P's residual p is below c, and its weight is at least

`K_P+b*p/(B-c)>=K_P+b*p/(B-g)=1.5782281252210837...`.

The latter bound is attained by the phase2 single charge(c=g,q=1/a1), whose full all-case certificate already passes. Thus enlarging the *single-charge* family to all type-resolved(c,q) cannot improve the phase2 bound. Mixtures strictly improve it.

## 5. Exact optimum over all convex mixtures of this family

The following reduction and eight rational endpoint inequalities prove a stronger stopping result than optimality of the chosen pair alone.

### Restrict q without loss

For q<=1/a2, both types are unsaturated and

`kappa=1-q(B-d)`.

The high-item density stays b/(B-d), while the low-item density decreases as q increases. Thus q=1/a2 pointwise dominates every smaller q. For q>=1/a1, kappa=0; the low-item density is fixed and the high-item density increases with q. Thus q=1/a1 dominates every larger q.

It suffices to consider q in[1/a2,1/a1]. In this interval kappa(q)=alpha1(1-q a1) is affine. For each fixed c, a positive weighted sum of P and G's charges has a common denominator affine in q and a numerator affine in q, plus a constant. Such a fractional-linear function has no strict interior minimum unless constant, so its minimum occurs at a q endpoint.

### Restrict c for the two-pattern dual

Both p and g are below d. For either pattern its one-tiny-item contribution is the low density times its residual when c is at least that residual, and the high density otherwise. At either fixed q endpoint, the weighted sum is fractional-linear in c on each interval cut by0,p,g,d. At c=p or c=g, the relevant contribution jumps downward (strict high means s>c). The value at the endpoint is therefore no greater than its left limit. Consequently checking c=0,p,g,d bounds the dual from below throughout[0,d].

### The exact positive dual

Use pattern multipliers

\[
\lambda_P=\frac{1849075774172128637213}{1920623604043880835653},\qquad
\lambda_G=\frac{71547829871752198440}{1920623604043880835653}.
\]

They are positive and sum to one. `verify_family_optimum.py` checks exactly that

`lambda_P W_P(c,q)+lambda_G W_G(c,q)>=R`

at all eight pairs `c in{0,p,g,d}`, `q in{1/a2,1/a1}`. Equality holds precisely at the two components selected in Section3. The reductions above extend the inequality to every c,q. Integrating or summing it over any valid convex mixture proves that at least one of the two physical pattern weights is at least R. Our all-pattern upper certificate attains R, closing both directions.

This certifies the optimum of the **entire convex family of type-resolved step charges(4)** with fixed non-tiny weights and algorithm parameters. It does not characterize all history-dependent potentials, stronger residual invariants, other algorithms, or the actual worst-case ratio of the current Best Fit algorithm.

## 6. Reproduction and scope

From `online-bin-packing/`, without writing Python caches into the frozen phase2 folder:

```sh
ulimit -v 1048576
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
timeout 290 python phase3/bf_type/optimize_fixed_mixture.py
timeout 290 python phase3/bf_type/check_all_mixture.py
timeout 290 python phase3/bf_type/verify_mixture_independent.py
timeout 290 python phase3/bf_type/verify_family_optimum.py
```

All use exact standard-library fractions and bounded jobs; no numerical solver or external computation is needed. Discovery, verification, global-family dual, and source-proof applicability are separate evidence layers. The independently audited phase2 Best Fit chronology/source proof is reused unchanged; only its new type-resolved algebra and weights require extension.

The global lower endpoint remains the published approximately1.54278090647. Publication priority and independent external human/formal review remain unestablished. The new lower-fork obstruction elsewhere in phase3 is a restricted survival result and must not be confused with this all-input upper theorem.

Primary source for the unchanged algorithm/weight framework: [AH, arXiv1707.01728](https://arxiv.org/html/1707.01728).
