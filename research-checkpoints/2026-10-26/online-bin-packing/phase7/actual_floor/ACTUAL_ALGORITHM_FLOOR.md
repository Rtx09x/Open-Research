# A seven-size lower bound for the fixed audited Best-Fit/AH algorithm

## Main conclusion

Let BF-AH denote the **fixed phase4 two-coordinate algorithm**: its recorded capacities and proportions, all-prior-advertised-container tiny Best Fit, and unchanged remaining AH rules. Its asymptotic competitive ratio is at least

```
L = 4107392448037194657402218954908536678004115949310575318313228556551
    /2602571515005375788795491740665865407544891224611410110356087898112
  = 1.5782054112079646... .
```

Together with the already independently audited phase4 upper theorem,

```
L <= asymptotic_ratio(BF-AH) <= 1.5782055179987482... .
```

The remaining possible improvement from **analysis alone for this fixed algorithm** is therefore at most

```
244214804051211930109591/2286852816926276513629309223262
= 1.0679078349233566... × 10^-7.
```

This is not the exact ratio of BF-AH, not a lower bound for every online algorithm, and not a narrowing of the published universal lower bound around1.542780906. It is a concrete resource-allocation result: substantial further upper progress requires changing this algorithm, rather than solely improving its weights or coupling analysis. A smaller analysis-only gain remains mathematically possible.

The native source-parameter/count checker passes. Advisor independent literal-parameter arithmetic, source-invariant and final prose audits also PASS, including every incomplete tiny prefix through N=120000 in a separate all-container simulation. The independent audit is `advisor/phase2/packing_actual_algorithm_floor_audit.md`, with its separate checker/JSON. This statement does not use a current solver output, upper-weight duality, or realizability of a fractional offline pattern mixture.

## 1. Seven fixed rational sizes

Fix once and for all

`tau=1/10^9`, `p=997/2100120`, `s=p-6tau`.

For each integer N>=1, present N tiny items of size s, followed by N items of **each** of the following six sizes, in any fixed class-batch order:

| Item | Size | Source class |
|---|---|---|
| huge |1/2+tau|huge|
| large |1/3+tau|165|
| small |1/11+tau|179|
| small |1/37+tau|205|
| small |1/40+tau|208|
| small |1/43+tau|211|

For definiteness, the huge items may arrive last. The lower bound does not require that every negative container eventually be matched.

All seven sizes are positive and lie in their intended classes. The narrowest relevant large-class interval is `(1/3,1067/3200]`, which contains1/3+tau. Also `0<s<1/43`. These are exact rational checks.

The limiting non-tiny endpoints plus p sum to1. The six positive perturbations add6tau, exactly canceled by the tiny item's subtraction. Thus a bin containing one item of each of the seven sizes has total volume **exactly1**.

Offline, N such bins pack the entire input, and its total volume is N. Consequently

`OPT(I_N)=N` exactly.

No perturbation limit is required: this single fixed rational seven-size set works for every N.

## 2. Actual tiny Best-Fit behavior

The two advertised tiny capacities and proportions are

```
A_1=17/60, A_2=1,
alpha_1=13701867480/32568497273,
alpha_2=18866629793/32568497273=beta.
```

At the fixed size s,

`floor(A_1/s)=596`, `floor(A_2/s)=2106`.

Both floor values equal their values at p. In particular, the exact upper bound on a permissible positive tau from the second capacity is `13/617435280`, greater than10^-9. The first capacity and all class intervals also have slack.

As long as the newest tiny container fits another s, Best Fit uses it: every previously completed tiny container has residual below s and cannot fit any later identical item. When the current residual drops below s, the next identical item fits no prior container, so a new quota-selected one is created. This proves the behavior by induction; it does not replace all-container Best Fit by an assumed one-open rule on arbitrary inputs.

Let m be the tiny-container count and n_i its type counts after N tiny items. Every container except possibly the last has exactly k_i identical items, with `k=(596,2106)`. The last may be incomplete. The primary AH type quota gives `n_i=alpha_i m+O(1)`, uniformly in N. Therefore

```
N=596 n_1+2106 n_2+O(1)=K m+O(1),
K=alpha_1*596+alpha_2*2106
 =47899435362138/32568497273.
```

The positive tiny containers are exactly type2, so their number is

`n_2=beta N/K+O(1)`.

The incomplete final container only changes the bounded error; it does not require a completion assumption. Equivalently, one may choose N at the ends of m full tiny containers, where the native finite replay checks the exact counts.

## 3. Positive-container counts for the actual non-tiny suffix

For a small class j let its recorded proportions be alpha_(i,j), and set

```
D_j=sum_i i alpha_(i,j),
b_j=sum_(i upper(j)>1/2) alpha_(i,j),
omega_j=b_j/D_j.
```

These definitions count **advertised positive containers**, not analysis weights.

The creation quota gives `n_(i,j)=alpha_(i,j)n_j+e_i`, with `e_i<1` and `sum_i e_i=0`. If q_j is the number of supported types and gamma_j their largest cardinality, then

```
N <= sum_i i n_(i,j) <= D_j n_j+gamma_j(q_j-1),
positive_j >= b_j n_j-(q_j-1)
           >= omega_j N-(q_j-1)(omega_j gamma_j+1).
```

The first inequality allows incomplete containers. Matching does not change their advertised signs or cardinality targets. The modified class179 proportions remain positive and supported on the same types2,10, so the same quota argument applies.

**Class165 is large, not small.** Its temporary/declared transformations require the source large-class invariants rather than the preceding small-class formula. The primary AH bounds give `n_2>=alpha_2 n-2`, `n_2<=alpha_2 n`, and `N<=n_1+2n_2<=(1+alpha_2)n`. Hence its positive type2 count is at least

`[alpha_2/(1+alpha_2)]N-2 = (56035901/134217728)N-2`.

This is the lower half of the source large-class count conclusion already independently audited in the earlier saturation theorem. No scenario weight is substituted for it.

Every huge item creates its own positive container, contributing N. Summing the exact positive rates yields

```
K_P = 1+omega_165+omega_179+omega_205+omega_208+omega_211
    =4629362226716989759188631892637569797799391977917968977
     /2934040051782717193271004450452948397602065646874525696.
```

The exact rates are reconstructed directly from the frozen parameter table in `verify_actual_floor.py`; it imports no upper-weight reconstruction or pricing code.

## 4. Actual bins and the asymptotic lower bound

The unchanged AH matching architecture never puts two advertised positive containers into one bin. Thus the actual online bin count is at least its total positive-container count, regardless of how many negative containers remain unmatched. The tiny modification does not change advertised capacities or matching signs.

Combining the preceding counts gives an input-independent constant C such that

`BF-AH(I_N) >= N K_P+beta N/K-C`.

Since `OPT(I_N)=N` and N is arbitrarily large, no asymptotic additive competitive constant can avoid

`asymptotic_ratio(BF-AH) >= K_P+beta/K=L`.

For an explicit sufficient constant, let

`C_non=2+sum_(j=179,205,208,211)(q_j-1)(omega_j gamma_j+1)`.

The tiny quota errors satisfy `N<=K m+1510` and `n_2>=beta m-1`. Therefore

`C=C_non+1510 beta/K+1`

is sufficient even for arbitrary N and an incomplete last tiny container. The exact checker records C_non and exact finite-instance lower bounds.

The identity `K_P+beta p/(B-p)=upper_anchor` is checked only to express the small remaining window. The proof of L was derived from actual container counts first; it does not infer a lower bound by reversing the upper-weight analysis.

## 5. A fixed-capacity architecture corollary

The same lower bound holds more broadly for every deterministic packing policy satisfying all of these explicit hypotheses:

1. Every tiny item is assigned to a container whose advertised capacity is one of the same A_1,A_2, and its contents do not exceed that capacity.
2. The counts of those two tiny types retain the same proportions with input-independent bounded discrepancy.
3. The non-tiny items retain the positive-container lower-count invariants used in section3, and each huge item is a positive container.
4. No bin contains two advertised positive containers; the tiny positive type is still exactly type2.

Indeed, identical items of size s imply **solely by capacity**

`N<=596 n_1+2106 n_2=K m+O(1)`.

The quota then implies at least `beta N/K-O(1)` positive tiny containers. Sections3–4 finish the identical lower bound. Best Fit, a single open container, a particular type order, and the absence of premature openings are not needed for this lower inequality. Multiple open containers or a different decoder do not escape it if all four hypotheses remain true.

This is not a statement about arbitrary bin-packing policies. A policy that changes capacities, proportions, cross-class container accounting, or the positive-bin invariant falls outside it. In particular, an interlaced-grid or altered matching proposal must identify precisely which hypothesis it changes before being treated as an escape route.

A proportion change is itself enough to leave these hypotheses; the corollary does **not** prove that a wholly new algorithmic framework is mathematically necessary. It does prove that fixed-parameter reanalysis and decoder-only changes preserving the hypotheses cannot produce a larger gain. Avoiding further blind coordinate sweeps is a research-allocation decision, not an impossibility theorem about all other parameters.

## 6. Reproduction, audits, and limits

With bytecode disabled and the usual1CPU/1GiB/290-second limits, run

`python phase7/actual_floor/verify_actual_floor.py`.

It checks every size/class/floor relation, positive-container rate, exact OPT packing, and ratio identity. Native integer-scaled all-container Best Fit replays297658 tiny arrivals over four traces, including128 containers in the largest trace. Separate closed-form quota counts give rigorous finite lower bounds for much larger explicit N without pretending to simulate their billions of items. The all-length induction above supplies the proof.

This floor applies to the fixed phase4 parameterized algorithm and to later phase5/6/7 **analyses of the same algorithm**. It does not constrain a changed capacity policy, changed type proportions, a changed non-tiny strategy, or arbitrary online algorithms. The earlier one-open saturation theorem concerns a different algorithm and is not being transferred here.

No new best upper bound, global lower-bound improvement, algorithm optimality, publication priority or full-gap solution is claimed.
