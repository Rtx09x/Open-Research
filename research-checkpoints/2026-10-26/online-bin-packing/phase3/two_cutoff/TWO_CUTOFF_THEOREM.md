# Two chronological cutoffs: charging actual overflow excess

## Result and current audit status

For the **unchanged phase2 tiny-Best-Fit AH algorithm**, the new all-input upper-bound candidate is

\[
R_2=\frac{70368019988469330838302270297132169299133207549971124303}
{44586883299218624616767998086450472130823929645605322752}
=1.5782224452926163\ldots.
\]

The new chronological inequality below has an independent advisor analytic PASS. Worker exact integer pricing and a separate Fraction recursion each PASS all402 scenarios /804 strict knapsacks. Independent source-derived advisor arithmetic audit also PASS: `advisor/phase2/check_packing_two_cutoff.py` and `packing_two_cutoff_audit.json`. This factor-two intermediate is superseded by the stronger disjoint-successor theorem in `../successor_mixture/SUCCESSOR_MIXTURE_THEOREM.md`. This is a small improvement over the fully audited step-mixture bound1.578223124297535; it does not solve the classic packing gap, prove actual Best Fit tightness, or improve its universal lower endpoint. No claim of optimality over this larger charge family is made.

The type-step mixture certificate and all phase1/phase2 files are preserved unchanged. All algorithm parameters, type quotas, matching priorities and non-tiny analysis weights u,v,w remain unchanged. Only the final scenario's tiny charge changes.

## 1. A size-sensitive chronology lemma

Let tiny item sizes be in(0,d], with d=1/43. Advertised tiny capacities are A_i in{17/60,1}; their creation proportions are alpha_i. Let m_i be the type counts, m their sum, p the number of supported types, and B=sum alpha_i A_i. The original quota rule gives m_i=alpha_i m+e_i, e_i<1 and sum e_i=0. The tiny decoder chooses, among **all existing fitting advertised containers**, one with least remaining advertised capacity; it creates a container only when none fits. Advertised capacities never change.

Fix 0<=c<=g<=d. Let H_c be the containers with final residual greater than c, and h_i their type counts. Write

\[
L_c=\sum_s s\,1_{s>c},\qquad E_g=\sum_s(s-g)_+,
\qquad a_i(g)=A_i-g>0.
\]

We claim

\[
\sum_i a_i(g)h_i\le L_c+2E_g+2a_{\max}(g).\tag{1}
\]

Exclude at most the earliest-created member of H_c and the last-created container overall. Consider any remaining C in H_c.

**If C ever receives an item of size at most c:** let s_C be its creation-item size and consider its first <=c item. An earlier final-H_c container E existed when C was created. No existing container fitted s_C, so E's residual was strictly below s_C then, and only decreased. At the first <=c insertion into C, E still has residual greater than c, so it is a feasible alternative. Best Fit therefore makes C's residual immediately before this insertion at most E's residual, hence strictly below s_C. All preceding items in C exceed c. Thus their total volume is greater than A_C-s_C, and

`A_C-g <= L_c(C)+(s_C-g)_+`.

**If C never receives an item of size at most c:** C is not last-created. At the creation of its immediate successor in creation order, with size s_next, no existing container fits. Hence C's residual at that time, and therefore its final residual, is strictly below s_next. All its items exceed c, so

`A_C-g <= L_c(C)+(s_next-g)_+`.

Each creation item is charged at most twice: once for its own container in the first case and once for its immediate predecessor in the second case. The <=2 omitted containers contribute at most2 a_max(g). Summing proves(1). This argument uses only already observed placement and creation events, not lookahead or item relocation; final H_c is an analysis device.

Separately, if r_C is C's final residual, then every C other than the last-created has r_C<s_next. The successor assignment is injective, and the last residual is at most1. Therefore

\[
\sum_C(r_C-g)_+\le E_g+1.\tag{2}
\]

For every nonnegative r,

`r <= c+(g-c)1_(r>c)+(r-g)_+`.

Thus total unused advertised capacity U satisfies

\[
U\le cm+(g-c)h+E_g+1,\qquad h=\sum_i h_i.\tag{3}
\]

The strict comparisons in the proof imply the weak inequalities stated; no equality endpoint or missing smallest item is assumed.

## 2. Type conservation and the valid item charge

For q>=0 put

\[
v_i=(1-q(A_i-g))_+,\quad \kappa_g(q)=\sum_i\alpha_i v_i,
\quad C_h=2q(A_{\max}-g)+\sum_i v_i.
\]

As in the type-step theorem, `h_i<=q(A_i-g)h_i+v_i m_i`. Equation(1) and the quota upper errors give

\[
h\le qL_c+2qE_g+\kappa_g(q)m+C_h.\tag{4}
\]

Total advertised capacity is at least Bm-(p-1). With T the total tiny-item volume, equations(3) and(4) imply

\[
\mathcal D(c,g,q)m
\le T+(g-c)qL_c+[1+2(g-c)q]E_g+p+(g-c)C_h,\tag{5}
\]

where

\[
\mathcal D=B-c-(g-c)\kappa_g(q)\ge B-g>0.
\]

Let b be the original scenario's alpha-average required tiny-container weight. The original quota argument bounds the total required tiny-container weight by bm+(p-1). Thus, with rho=b/mathcal D, the nonnegative item charge

\[
f_{c,g,q}(s)=\rho\big[s+(g-c)q\,s1_{s>c}
+(1+2(g-c)q)(s-g)_+\big]\tag{6}
\]

satisfies the aggregate required-weight bound with input-independent additive constant

\[
\rho\,[p+(g-c)C_h]+p-1.\tag{7}
\]

The case b=0 is covered by zero charge. Finite convex mixtures remain valid by mixing inequalities and constants. The source matching, temporary/declared-large-container, and quota arguments are unchanged; their applicability to the all-open tiny Best Fit decoder was independently audited in phase2.

**Controls.** If g=d then E_d=0 and(6) reduces exactly to the previously audited type-resolved step charge. If c=g then(6) reduces to `b/(B-c)[s+(s-c)_+]`, the previously audited delayed-overflow hinge. The new information is the two different cutoffs, not retuning within the already optimized step family.

## 3. Exact conservative bin pricing

For tiny total volume strictly below a residual r, the supremum of total volume in items strictly greater than c is

\[
S_c(r)=\min\{r,d(\lceil r/c\rceil-1)\}\quad(0<c<d).
\]

Use S_0(r)=r and S_d(r)=0. The integer condition is **nc<r**, not nc<=r. Non-tiny class lower endpoints are strict, so a bin containing those items has strictly less than their formal residual available. This is essential at r=c.

For the excess functional, writing r=nd+u, n=floor(r/d),0<=u<d, the supremum is

\[
H_g(r)=n(d-g)+\max(0,u-g).
\]

This follows by merging mass into maximum-size d items; it is continuous at multiples of d. A valid upper envelope for(6) is

\[
F(r)=\rho\{r+(g-c)q S_c(r)+[1+2(g-c)q]H_g(r)\}.\tag{8}
\]

We intentionally sum separate maxima. They need not be jointly attained for every residual; this makes the pricing conservative, never invalid. Convex mixtures similarly sum these envelopes. For the active P and Q residuals below d, one tiny item approaching the residual does attain both terms simultaneously, but no global optimality claim relies on that observation.

The integer oracle `pricing.py` removes the linear rho*r part, uses monotonic residual-envelope dominance, and bounds remaining reduced profits by the maximum of the non-tiny reduced-profit density and the tiny bonus density. The hinge density bound is `(d-g)/d`; the step density bound is1. Strict non-tiny total sizes are enforced by `(space-1)//size` on the exact common-denominator grid. The separate Fraction verifier uses a different size-ordered recursion and target bounds.

## 4. Selected charge and finite refinement

In the final scenario(x,y)=(3/7,1/2), use a single charge with

\[
c=997/2100120,\quad g=10709750143/500000000000,
\quad q=1/(1-g).
\]

All other scenarios use their prior audited type-step charges, embedded with g=d. All published u,v,w and all algorithm parameters are identical to the previous certificate.

A bounded fourteen-point exploration first exposed the new face. A finite rational bisection then located the crossing of the existing P pattern(1,165,179,205,208,211), residual997/2100120, and Q pattern(1,165,179,187), residual29/1254. The selected g is one of the two adjacent rationals on the10^12 denominator grid. Crucially, the **complete pattern oracle** then certified every pattern, not only these two rows. Full402-scenario pricing showed no other limiting scenario. The final rational R_2 above is the exact certified maximum at this selected rational g, not a rounded optimization estimate.

Artifacts:

- `refined_candidate.json`: selected rational, bracketing evidence, two diagnostic rows and complete critical-scenario oracle.
- `two_cutoff_certificate.json`: stable all-scenario artifact, SHA256 `8e2765c85417a2ff737cac9dcf2ad44713f3e57070345c47e5ef3783f9578773`.
- `independent_verification.json`: separate Fraction PASS,30,122 nodes.
- `explore.py`, `refine.py`, `check_all.py`, `verify_independent.py`: standard-library reproducibility.

Run with `PYTHONDONTWRITEBYTECODE=1`,1CPU,1GiB and a290-second timeout per job from `online-bin-packing/`. Individual runs take seconds. The current certificate's status text records that independent advisor arithmetic audit was pending when generated; later audit status belongs in this theorem/checkpoint, without silently changing the hashed artifact.

The global packing gap remains open. This result is analysis of the unchanged Best Fit variant; the earlier one-open saturation input does not establish a matching lower bound for it. Further improvement must be proved, not inferred from the positive difference between earlier envelopes.
