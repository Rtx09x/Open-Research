# Three-class rational refinement of Advanced Harmonic

**Status:** complete exact proof certificate and independent primary-source audit passed. This is the frozen final result of the bounded parameter-refinement experiment. Publication priority is not claimed.

## The result

For classic deterministic one-dimensional online bin packing with unit bins and irrevocable online placement, the Advanced Harmonic (AH) algorithm of [Balogh, Békési, Dósa, Epstein and Levin](https://arxiv.org/html/1707.01728), with the three rational changes below, has asymptotic competitive ratio at most

\[
R_* = \frac{1848920194883516152323541607}{1171513518439186595284254720}
     \approx 1.5782320611603713.
\]

The original exact AH certificate is

`R0=10060574276093395247/6374352691333693440 ≈1.5782895555451986`.

The exact improvement is

`R0−R*=52970480514705773020251207803/921315719333166392502587007959040 ≈ 5.74943848272e-05`.

This is a modest numerical refinement of an established algorithm family. It is not a new algorithmic architecture, not a major closure of the known gap, and not a priority claim. The comparison is against the **exact** old certificate, not merely its rounded 1.57829 label.

## Exactly what changes

All class boundaries, container types, online rules, and all other proportions remain published. Make these transfers between existing positive container proportions:

| Class | Item interval | Container-proportion transfer |
|---|---|---|
| 167 | (1/4,271/960] | type 1 → type 3, κ=`101/1000000` |
| 172 | (3/20,1/6] | type 2 → type 6, δ=`203907985616802938880/661406035963546729717373` |
| 179 | (1/11,1/10] | type 10 → type 2, η=`56254421499138925905512741470208/47449963408280619234481631165243337` |

The transfers are approximately κ=0.000101, δ=0.0003082947153933, and η=0.0011855524737733. A transfer subtracts that value from the source type's proportion and adds it to the destination type's proportion. These are deterministic floor-tracked container proportions, not randomized selection probabilities. The complete resulting rational parameters are in `ah_three_parameter_full_certificate.json`.

Every analysis weight **u,v,w remains exactly the published value**, including `w=413913/524288` for the 160 scenarios in (3/10,1/3]. The final result needs no analysis-weight reoptimization.

## Proof reduction and applicability

1. The source AH algorithm permits fixed nonnegative container proportions summing to one. All changed values remain positive, and only already-supported small-class types are changed. Container volumes and the scenario partition are therefore unchanged.
2. The source's large-threshold balance inequalities involve only u,v,w and the proportions of that large threshold class. The three altered classes are small, so these hypotheses remain valid. The exact verifier nevertheless checks all balance, range, and order conditions.
3. For every scenario, reconstruct the source §4.3 item weights and tiny-item density from the modified rational parameters. Theorem 24 gives `ALG(I) ≤ W(I)+C`, where C is independent of the input.
4. As in source §4.4, bound each offline bin by two strict-infimum knapsacks: a bin without a weight-one huge item, or a weight-one huge item plus a smaller-capacity knapsack. All non-tiny infimum representatives must have total size **strictly** below the relevant capacity. Remaining space is filled with tiny sand.
5. Exact pricing proves every bin's weight is at most R*. Hence `W(I) ≤ R*·OPT(I)`, and therefore `ALG(I) ≤ R*·OPT(I)+C` for all inputs. Taking OPT to infinity proves the asymptotic bound. No finite-benchmark extrapolation is involved.

The model has no advice, lookahead, repacking, extra capacity, cardinality constraint, or random-order assumption. The new constants are fixed rational algorithm parameters, not input-dependent information.

### Endpoint convention

For endpoint clarity we choose the analysis threshold `t=1−a` strictly between `max(0,1−p)` and `min(1/2,n)`, avoiding the finite breakpoint set, where `p,n` are the smallest unmatched positive and negative container volumes (defaults 1 and 1/2). Lemma 3 makes this interval nonempty. Every unmatched positive has volume above `a`, and every unmatched negative has volume above `t`; the proof of Theorem 24 therefore applies unchanged. This selects an interior scenario and removes endpoint ambiguity without altering AH or its parameters.

See [the independently source-checked endpoint clarification](AH_ENDPOINT_CONVENTION.md) for the full argument and source anchors. This is an analytical convention clarification, not a parameter or certificate change; it is not formally verified.

## Complete exact computation and independent audit

The certificate contains **all 402 consecutive scenario intervals**. `verify_ah_full.py` reconstructs the entire endpoint set from class boundaries and container volumes/complements and checks exact coverage. It does not trust a scenario count or any published numerical per-scenario maximum.

For all scenarios it reconstructs weights and proves both strict knapsack bounds with Fraction-only target search. It also checks the 492 large-threshold balance inequalities (three for each of 164 such scenarios), plus range/order conditions. The worker proof search uses size order; discovery uses a different integer-scaled density-order maximization oracle.

```sh
python verify_ah_full.py ah_three_parameter_full_certificate.json ah_three_parameter_full_verification.json
python verify_ah_three_parameter_algebra.py
```

Worker terminal status: **PASS**, 402 intervals, 804 strict knapsack cases, 25,252 search nodes, approximately 6 seconds on one CPU; standard-library Python only.

The advisor independently parsed the primary HTML and checked the three exact source-parameter differences, every unchanged u,v,w, all 402 intervals, and all knapsack/validity conditions. Its separate Fraction DFS, with no worker imports, passed in 22,779 nodes (about 2 seconds). Advisor artifacts: `audit_ah_three_parameter.py`, `ah_three_parameter_audit.json`. The separate analytic floor was also independently derived from source parameters and checked in `audit_ah_two_scenario_floor.py`.

## Why this bounded search stops here

Let `D0=805306368/191010959` be class 172's original mean item count per container, and set `x=1/(D0+4δ)`. The same physical infimum-size pattern, one item each at 1/2,1/3,3/20 with sand 1/60, has these weights in two scenarios:

```
Final large threshold:
L−(x) = 142208117299/84557168640
        − (83427088/191010959)·x

Last critical small threshold:
L+(x) = 5162815091346603839/3718372403277987840
        + (40073570314217/50072376836096)·x
```

The selected δ makes both equal R*. Positive rational multipliers

```
λ− = 40073570314217/61943480870889
λ+ = 21869910556672/61943480870889
```

sum to one and cancel x, so `λ−L−+λ+L+=R*` for every x. Thus no further adjustment of the **same three transfers, while keeping the published analysis weights and all other parameters fixed**, can improve this weight certificate. This is a genuine restricted analysis floor, **not** a lower bound on the modified algorithm's actual competitive ratio and **not** an unrestricted optimum for AH or online bin packing.

The source-based algebra, active pattern values, intersection, and positive dual identity are checked by `verify_ah_three_parameter_algebra.py` and independently by the advisor. This floor gives a principled stopping point for the bounded experiment instead of an unbounded coordinate search.

## What is and is not settled

- **Settled internally:** exact parameters, source-theorem applicability, complete rational pricing, independent reconstruction, and the restricted fixed-weight analysis floor.
- **Unsettled:** publication priority and any broader optimality. Literature/version checks found no matching refinement; this does not prove novelty. See `literature.md`.
- **Next mathematical route, not executed here:** change the critical scenario's analysis weight or a parameter outside these three transfer directions, then rebuild and certify all affected cases. The exact floor explains why simply continuing these same coordinates cannot help.
- No public posting, external outreach, paid computation, user-computer activity, or git operations occurred. Downloaded papers are reading caches, excluded from the minimal integration manifest.

Earlier audited anchors remain in the original research workspace (the one- and two-class full-scenario anchors are also bundled here): unchanged AH reanalysis at 1.5782893074261488; one-class refinement at 1.5782796641658323; two-class refinement at 1.578244990835865. None is silently overwritten by the stronger result.
