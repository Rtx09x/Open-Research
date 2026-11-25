# Two-class rational refinement of Advanced Harmonic

**Status:** complete exact certificate and independent primary-source audit passed. The cleaner certificate retaining every published analysis weight has passed both the worker and advisor full checkers, including comparison of every u,v,w to primary tables. Numerical/publication priority is not claimed.

## Main statement

For classic deterministic one-dimensional online bin packing, use the Advanced Harmonic algorithm of [Balogh, Békési, Dósa, Epstein and Levin](https://arxiv.org/html/1707.01728), with exactly these two changes to its container proportions:

1. In class 172, `(3/20,1/6]`, transfer
   `δ=3808504450168569987072/8656947158519818292585777`
   (approximately 0.0004399362015766024) from type 2 to type 6.
2. In class 179, `(1/11,1/10]`, transfer
   `η=1021176854624523671529586688/1182117257922550741242537316731`
   (approximately 0.000863854112424631) from type 10 to type 2.

Every other algorithm parameter, class boundary, and supported container type is unchanged. All affected proportions remain positive and sum to one. The resulting asymptotic competitive ratio is at most

\[
R=288133180542317449599574241/182565559983001943628840960
  \approx 1.5782449908358649.
\]

Its reduction from the source's **exact** rational certificate is

`6398395900211954902386288349/143575398468552184531916653854720 ≈ 4.45647093336e-05`.

This is a modest quantitative refinement of an existing algorithm family, not a new packing principle and not a significant closure of the lower/upper gap. It improves the actual rational certificate, rather than merely adding decimal places to the rounded 1.57829.

## Applicability and infinite-input guarantee

The AH proof permits fixed rational nonnegative container proportions summing to one in each class. Both transfers are between already-supported small-class types. Hence all class endpoints, container volumes, and the complete 402-interval scenario partition remain unchanged. For large-threshold scenarios, the sufficient inequalities involve only u,v,w and the two proportions of that large threshold class; neither altered small class enters those validity constraints.

The clean final certificate keeps **every analysis u,v,w equal to its published value**, including `w=413913/524288` on (3/10,1/3]. No optimization of the analysis weights is required for this final statement. All validity inequalities are checked directly regardless.

For each scenario, the proof uses the source's item-weight and tiny-density formulas, then checks both strict-infimum knapsack cases. The unchanged general AH weight theorem gives `ALG(I) ≤ weight(I)+C` for an input-independent constant C. The certificates establish `weight(I) ≤ R·OPT(I)` for every input. Therefore `ALG(I) ≤ R·OPT(I)+C`, giving the global asymptotic statement as OPT grows. There is no empirical-to-infinite extrapolation, advice, lookahead, repacking, or altered bin capacity.

## Exact three-pattern derivation

Let `D172` and `D179` be the original mean item counts per container of the respective classes, and put

`x=1/(D172+4δ)`, `y=1/(D179−8η)`.

Three explicit infimum-size offline patterns have affine weights:

1. In a w=0 scenario: three class-167 items, one class-172 item, one class-179 item, and sand; sizes `3·(1/4)+3/20+1/11`, leaving sand 1/110.
2. In the final large-threshold scenario: one huge item and one item each of classes 165,179,205,208,211, with sand.
3. In the same final scenario: one huge item, one class-165 item, one class-172 item, with sand 1/60.

Their respective affine weights are

```
L1 = 124762873764239/104019410288640 + x + y
L2 = 481297903308151/298261319516160 − y/4
L3 = 142208117299/84557168640 − (83427088/191010959)·x
```

Solving `L1=L2=L3` gives the two transfers above and R. This is not just a heuristic fit of active patterns: complete exact pricing verifies that every other pattern in every scenario is below R.

There is also an exact lower certificate for the best **weight bound within this fixed two-parameter, fixed-published-weights family**. The positive multipliers

```
λ1 =  83427088/608146399
λ2 = 333708352/608146399
λ3 = 191010959/608146399
```

sum to one and cancel both x and y coefficients, yielding `λ1·L1+λ2·L2+λ3·L3=R`. Thus no parameter choice inside this restricted certificate family can reduce the maximum of these three pattern weights below R. This is **not** an optimality claim for all AH parameters, all weight analyses, or the true competitive ratio of the modified algorithm.

## Reproducibility

Primary exact artifact: `ah_two_parameter_published_weights_certificate.json`. It contains the complete rational algorithm parameters, explicit parameter modifications, and all 402 scenario records. The verifier reconstructs the scenario set independently and checks exact coverage rather than trusting a list count.

```sh
python verify_ah_full.py ah_two_parameter_published_weights_certificate.json ah_two_parameter_published_weights_verification.json
```

Terminal worker result: **PASS**, all 402 scenarios, 24,615 Fraction-only target-pricing nodes, about 6 seconds on one CPU. It checks the source's 492 large-threshold feasibility inequalities and 804 strict knapsack cases. Its recursion is size-ordered, unlike the density-ordered integer-scaled discovery oracle.

The separate advisor implementation reparses the primary HTML, checks the exact parameter differences, reconstructs all item weights, and uses its own Fraction DFS with no worker-module imports. Its audit of the exact unchanged-weight certificate passed all 402 intervals and 804 strict knapsacks (22,179 nodes, approximately 2 seconds), after checking every u,v,w against the primary tables.

Supporting derivation: `ah_three_face_balance.py`, `ah_three_face_result.json`. The standalone `verify_ah_three_face_algebra.py` checks the active pattern values, parameter changes, exact intersection, and positive dual identity. The advisor also independently derived the affine constants from primary parameters, checked strict pattern feasibility, and verified the exact intersection and dual. This restricted optimality fact is not needed for the global upper guarantee. The intermediate two-parameter certificate with a rebalanced but unnecessary critical weight is preserved as `ah_two_parameter_full_certificate.json`. The simpler one-parameter and unchanged-algorithm audited results are preserved separately, not overwritten.

## Source-table discrepancy and priority

The complete all-scenario checker does not trust printed numerical scenario maxima. It directly recomputes the w=0 group, for which one quoted source group figure is below the conservative pricing value we reconstruct. This is safely below the overall published bound and does not affect the result here, which certifies every case directly. We do not need to claim an error in the paper.

Current literature checks and source/version details are in `literature.md`. Searches found no matching refinement, but absence of a search result cannot establish priority. No public posting or author outreach has been performed.
