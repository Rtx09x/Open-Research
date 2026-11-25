# The certified algorithm is tight: a jointly realizable saturation family

## Statement and scope

Let **D-AH** be the frozen three-transfer Advanced Harmonic algorithm with the delayed tiny-container closure rule defined in `../AUDIT.md`. All non-tiny rules, type quotas, advertised volumes, and priorities are unchanged. Then its asymptotic competitive ratio is exactly

\[
R=\frac{23211234258164394107066141961880719040528132151}
        {14707121654123980930208343329037931077093556224}
 =1.5782309281201736\ldots.
\]

The upper bound is the independently checked all-input theorem in `../SINGLE_THRESHOLD_THEOREM.md`. Here we prove the matching **algorithm-specific** lower bound by actual input sequences. This is not a lower bound for all online algorithms and does not narrow the universal lower bound of the problem. It shows that no improved analysis alone, coupled or separable, can improve the competitive guarantee of this fixed algorithm.

The construction uses only rational item sizes and finite ordinary input sequences. It requires no ability to move items or change the algorithm's information. Its tiny prefix is precomputable from the deterministic quota sequence.

## 1. Two offline patterns and fixed parameters

Write `lower(j)` for the open lower endpoint of class j. Consider two limiting offline patterns:

| Pattern | Non-tiny class lower endpoints, including one huge item | Tiny residual |
|---|---|---|
| P | 1/2, 1/3 (165), 1/11 (179), 1/37 (205), 1/40 (208), 1/43 (211) | p=997/2100120 |
| Q | 1/2, 1/3 (165), 1/11 (179), 1/19 (187) | q=29/1254 |

Each row sums to one after its residual is added. The tiny maximum size is d=1/43. The two tiny types have capacities and proportions

\[
(A_1,A_2)=(17/60,1),\qquad
(\alpha_1,\alpha_2)=
(13701867480,18866629793)/32568497273.
\]

Let

\[
B=\alpha_1 A_1+\alpha_2 A_2
 =22748825579/32568497273,\qquad
b=\alpha_2=18866629793/32568497273.
\]

For a non-tiny class j, define

\[
D_j=\sum_i i\alpha_{ij},\quad
\beta_j=\sum_{i:\,i\,\mathrm{upper}(j)>1/2}\alpha_{ij},\quad
\omega_j=\beta_j/D_j.
\]

For class165 the positive type is type2; its advertised volume remains positive even while it is declared and has only one actual item. The coefficients needed here are

| j | omega_j |
|---|---|
|165|56035901/134217728|
|179|20185282519488238084365473087/225399200947699500932690608128|
|187|120535379/2415919104|
|205|61605937/2415919104|
|208|20486803/872415232|
|211|30706159/1409286144|

Set

\[
K_P=1+\omega_{165}+\omega_{179}+\omega_{205}+\omega_{208}+\omega_{211},
\quad K_Q=1+\omega_{165}+\omega_{179}+\omega_{187},\quad
Z=B-2q+p>0.
\]

Direct rational arithmetic from the parameters, without any weight-dual assumption, gives

\[
K_P+(K_Q+b-K_P)\frac pZ=R.\tag{1}
\]

The limiting fraction of Q bins is

\[
\theta=\frac pZ=
\frac{616945043842439}{848239837141104679}.
\]

It happens to equal the dual multiplier from the upper-bound optimization. Equality (1), not that coincidence, is what the lower bound uses.

## 2. An explicit tiny prefix

Choose any rational `0<tau<=10^-6` and an integer m>=1. Increase every non-tiny size in the two rows by tau. The new residuals are

\[
p_\tau=p-6\tau>0,\qquad q_\tau=q-4\tau\in(0,d).
\]

All these perturbed non-tiny items belong to the claimed classes; in particular the narrow class165 is `(1/3,1067/3200]`, whose width is1/9600. Huge items have size1/2+tau. These facts and all following strict inequalities are checked exactly in `check_saturation.py`.

Generate the first m tiny-container types by the original AH rule: with n_i containers of each type and n total, select the smallest i for which `n_i<=floor(alpha_i n)`. Denote the resulting capacities by A(1),...,A(m).

For each t from1 to m, present:

1. One tiny item of size q_tau.
2. Tiny filler items of total size
   \[
   F_t=A(t)-2q_\tau+\tau>0.
   \]

The filler splitting is specified below; every filler item is at most p_tau<d. After this group, the current container's load is

\[
q_\tau+F_t=A(t)-q_\tau+\tau<A(t).
\]

Every filler prefix fits the container. If another q_tau arrives, the total would be A(t)+tau>A(t), so it closes this container and starts the next quota-selected type. The new item fits that type. Thus this is an exact causal execution with m tiny containers, one q_tau per container, and m-1 overflow events. The last container simply remains open when tiny arrivals end.

Let `F=sum_t F_t` and define

\[
n_P=\lceil F/p_\tau\rceil,\qquad N=n_P+m.
\]

To split the fillers, take the common refinement of the consecutive online filler segments of lengths F_t and consecutive offline budgets of lengths p_tau. Each positive refinement interval is one filler item. Intervals never exceed p_tau. There are at most m+n_P-1 such items. Each F_t receives exactly its prescribed load; each P budget is filled exactly except possibly the last. No approximation or divisibility assumption is needed.

This construction is fully determined before the input begins. The type selection depends only on past type counts, not on hidden matching choices.

## 3. Complete the input; prove OPT exactly

After the tiny prefix, present the following numbers of non-tiny items, each of size `lower(j)+tau`:

* N items each of classes165 and179;
* n_P items each of classes205,208,211;
* m items of class187;
* N huge items of size1/2+tau.

For definiteness, present small classes in increasing item-size order, then class165, then huge items. The positive-container lower bound below in fact does not depend on this suffix order or matching choices.

Offline, use n_P bins of pattern P and m bins of pattern Q. Each Q receives one q_tau item; each P receives one refinement budget of filler. All bins fit. Let

\[
\sigma=n_Pp_\tau-F,\qquad0\leq\sigma<p_\tau<1.
\]

Every Q and all but possibly the last P are full, so the total input volume is N-sigma>N-1. Consequently volume gives OPT>=N, while the displayed packing gives OPT<=N. Therefore

\[
\operatorname{OPT}=N.\tag{2}
\]

The last P may also be full when sigma=0; the same argument applies.

## 4. Actual online cost from container conservation

AH never puts two advertised positive containers into one bin. Hence its actual number of bins is at least its number of positive containers. This avoids any assumption about whether negative containers are matched, or about which retrospective weight scenario applies.

For each small class j, let zeta_j be its number of supported types and gamma_j the largest supported type. The quota rule, as in the proof of source Lemma19, gives

\[
n_{ij}=\alpha_{ij}n_j+e_i,\qquad e_i<1,\quad\sum_i e_i=0.
\]

The total positive discrepancy and the absolute total negative discrepancy are at most zeta_j-1. Since a type-i container has at most i actual items (possibly fewer while open),

\[
N_j\leq\sum_i i n_{ij}
\leq D_jn_j+\gamma_j(\zeta_j-1).
\]

Its positive-container count is therefore at least

\[
\beta_jn_j-(\zeta_j-1)
\geq\omega_jN_j-(\zeta_j-1)(\omega_j\gamma_j+1).\tag{3}
\]

**Class165 is large, not small.** Source Lemma5 and Corollary6 give
`n_2<=alpha_2 n` and `n_2>=alpha_2 n-2`. Also
`N_165<=n_1+2n_2<= (1+alpha_2)n`. Thus its positive-container count is at least

\[
\omega_{165}N_{165}-2.\tag{4}
\]

This is also the lower half of source Corollary8. It includes temporary/declared transformations and does not require all type2 containers to be full.

The tiny quota gives at least bm-1 positive tiny containers. Each huge item is its own positive container. Summing (3)–(4) over the construction gives

\[
\operatorname{D\!\!-\!AH}\geq
n_PK_P+m(K_Q+b)-C,\tag{5}
\]

where the following fixed input-independent constant is sufficient:

\[
C=3+\sum_{j\in\{179,187,205,208,211\}}
(\zeta_j-1)(\omega_j\gamma_j+1)
=\frac{1413539207612313536008874798413}
       {112699600473849750466345304064}.
\]

Neither (3) nor (5) assumes container fullness. Neither invokes the tiny weight lemma or the upper-bound LP.

## 5. Arbitrarily large near-tight instances

Tiny quota discrepancies are bounded, so
`sum_t A(t)=Bm+O(1)` uniformly in m. At fixed tau,

\[
\frac{n_P}{m}\longrightarrow
\frac{B-2q_\tau+\tau}{p_\tau}.
\]

Using (2) and (5), then letting m grow,

\[
\liminf_{m\to\infty}\frac{\operatorname{D\!\!-\!AH}}{\operatorname{OPT}}
\geq K_P+(K_Q+b-K_P)\frac{p-6\tau}{Z+3\tau}.
\]

As rational tau decreases to0, the right side tends to R by (1). More explicitly, for the positive rational `rho=b/(B-c_*)` at the certified final-scenario threshold c_*, the identities

\[
K_Q+b-K_P=\rho Z,\qquad K_P+\rho p=R
\]

give a fixed-tau deficit exactly

\[
R-\left[K_P+(K_Q+b-K_P)\frac{p-6\tau}{Z+3\tau}\right]
=\rho\tau\frac{6Z+3p}{Z+3\tau}\longrightarrow0.
\]

For every epsilon>0, first choose rational tau sufficiently small, then m arbitrarily large. This produces arbitrarily large OPT with ratio at least R-epsilon, so no additive competitive constant can evade the lower bound. A diagonal choice tau_k->0 and sufficiently large m_k gives an explicit sequence of finite instances. One need not claim that these instances are successive prefixes of a single run.

## 6. Verification and interpretation

`python phase2/coupled/check_saturation.py` checks all exact pattern sums, class memberships, positive coefficients, the ratio identity, the fixed-tau deficit, and explicit tiny/refinement executions for m=1,10,100,1000 at tau=10^-8. The largest has OPT=1,374,639, with999 overflow events and1,374,638 filler items. The trace checker uses integers after exact scaling; it does not simulate the entire AH implementation. The all-input quota argument above supplies the online lower bound, not extrapolation from those traces.

The advisor independently parsed the primary AH parameters, verified the limiting conservation identities and class165 source invariants, and reviewed the common-refinement/ceil construction. Independent artifacts are `advisor/phase2/packing_saturation_algebra.json` and its subsequent audit note.

This construction answers the requested global-correlation challenge negatively for the current algorithm: the active offline patterns, tiny overflow loads, and online type proportions are compatible. A better bound requires an algorithm change (or discovery of an error in the independently checked theorem), rather than a stronger accounting of the same execution.

## 7. A narrow architecture-level corollary

The lower bound remains valid if the deterministic matching priorities or tiny type-selection order are changed, **provided** that all of the following remain true:

* the same tiny capacities and limiting proportions have input-independent bounded count discrepancy;
* there is one open tiny container, and it is filled until the next tiny item fails to fit before a new container is selected;
* each bin still has at most one advertised positive container;
* the stated non-tiny positive-count lower invariants remain valid.

Indeed, after a q_tau item starts a selected container, a deterministic adversary can infer its capacity and generate the requisite filler total. One global p_tau budget counter implements the common refinement as items are generated. Bounded capacity discrepancy still gives `sum A(t)=Bm+O(1)`. Everything after that is unchanged. For each deterministic algorithm this adaptive description unrolls into a fixed finite input sequence, so it grants no information or resource to the online algorithm.

This corollary does not cover randomized choices, multiple simultaneously available tiny containers, changed quotas/capacities, or matching changes that invalidate the positive-count premises. It specifically prevents mistaking a tie-break or quota-order adjustment for an escape from the obstruction.

Primary source for algorithm invariants and numbering: [Balogh et al., A New and Improved Algorithm for Online Bin Packing, Sections3 and5](https://arxiv.org/html/1707.01728).
