# Current results and exact scope

## Target remains open

No 317-word code and no global upper bound below the published 320 have been obtained. The target is the unrestricted binary, length-12, single-deletion problem.

## Exact local-distance barrier (computed here; novelty unverified)

Let B = VT0(12). Every distinct valid code C with |C| ≥ 316 satisfies

    |B \ C| ≥ 10.

Thus a different 316-word code has symmetric difference at least 20 from B; a 317-word counterexample has symmetric difference at least 21.

This is **not** a proof that 316 is optimal, nor that an improving larger trade is impossible.

### Reproducible evidence

- B has 316 words; two independent deletion checkers verify that its balls partition all 2,048 received words.
- Complete connected blocker-support enumeration, through nine removed baseline words:

| Removed words | Connected supports |
|---:|---:|
| 1 | 0 |
| 2 | 68 |
| 3 | 376 |
| 4 | 1,358 |
| 5 | 5,474 |
| 6 | 23,132 |
| 7 | 102,660 |
| 8 | 463,558 |
| 9 | 2,136,830 |
| **Total** | **2,733,456** |

- `scripts/trades.py`: exact integer packing recursion, no neutral or improving trade, 216.9 seconds.
- `scripts/verify_trades_independent.py`: independently reconstructs string deletion sets and support closure, matches every support hash, and partitions eligible outsiders into at most |S|−1 pairwise-conflicting cliques. All 416,412 nontrivial cover tests passed in 187.3 seconds.
- `trade_lemma.md` proves completeness of the connected-support reduction and its implication for disconnected trades. A second worker audited that reduction.
- Regression control reproduces Sloane's known length-6 neutral switch; this verifies that the search does not reject all switches by construction.

### Why the implication holds

For an outsider x define N(x) = {b in B : D(b) intersects D(x)}. A replacement T for removed S requires N(x) subset S for every x in T. In any improving or neutral replacement, some connected incidence component has nonnegative gain. For its support S, the independent checker supplies a cover of every eligible outsider by at most |S|−1 conflict cliques. An admissible T takes at most one word from each clique, so |T| ≤ |S|−1, contradicting nonnegative gain. Exhaustion covers every such connected support of size at most nine.

## Rigorous but noncompetitive global certificate

All 155,496 maximal conflict cliques yield an integer-checked rational dual upper bound

    32112485464 / 100000000 = 321.12485464,

and therefore the integer bound 321. This is **weaker than the published 320**, not a frontier improvement. The independent checker reconstructs all deletion sets from strings, verifies every clique pair, and checks the dual with Python integers without importing SciPy or the model builder.

## Negative or inconclusive experiments

- Insertion cliques: numerical LP 321.21646453.
- Known fixed-prefix/suffix subcode cuts: no additional decrease.
- All maximal conflict cliques: numerical LP 321.12484237.
- All 4,095 unions of received-word Hamming-weight layers, rounding divisors 2–7: no violated cut at the tested LP solution.
- Odd-walk cuts: four cuts reduce the insertion LP only to 321.21064583.
- Integer orbit-count relaxation: 240-second pilot, 2,056 nodes, upper 321; inconclusive.
- Whole complement/reversal-orbit trades through nine removed orbits: no neutral or improving trade. This is a **symmetry-restricted construction search**, not an unrestricted exclusion. A ten-orbit attempt stopped at the explicit support-count resource cap and is incomplete.

## Next substantive avenue

A sparse spectral/theta-dual pilot used all four character blocks and a proximal bundle optimizer. Its best numerical value was 321.11060523 after 250 iterations—only a small fractional improvement, not the required <320. The candidate was independently checked in the full 4,096-dimensional space, and a weaker rational spectral bound of 321.12 was certified with conservative IEEE backward-error bounds; see `spectral_certificate.md` for assumptions. This still gives only the integer bound 321. No further generic tuning is prioritized. A useful next step needs a stronger mathematical relaxation/cut or a structured trade family; `pro_brief.md` packages that bottleneck for expert input. Any future spectral candidate still needs an exact PSD/eigenvalue upper certificate.
