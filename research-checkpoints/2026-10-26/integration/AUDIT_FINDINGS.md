# Independent skeptical audit of two numerical refinements

Date: 2026-10-25. Scope: C7 recycled-label lower bound and three-transfer Advanced Harmonic upper bound only. This is internal review, not external peer review or a priority claim. No worker/advisor files were changed.

## C7: finite refinement survives checks; inherited realization remains explicit

The claimed lower bound `3.258832624232849476` follows from a valid finite-label substitution, conditional on the inherited 125-dimensional seven-family realization. The entire new four-coordinate family rule and ordinary binary substitutions were checked afresh, not inferred from a stored PASS result. Physical Cartesian blocks are separated; the construction does **not** require a private *physical vertex* neighbor in the original graph. Overlap between non-required-separated labels (notably O=V) is permissible. Distinct blocks within each output family are separated and therefore disjoint, so exact cardinalities add.

`c7_fresh_check.py` independently reads the literal K4a list from the upstream Lean source, builds the two recycled pairs and coordinate-swapped auxiliary code, checks all relevant finite separations, and follows the stated recurrence directly rather than evaluating the stored DAG. It checks the exact final vectors, the 128000- and 768000-dimensional integer root brackets, and `Mopt > M8^6 > Mpublished^1536`. It also reruns the five upstream finite certificates and compares the resulting n25 input vector. The run passed in 85.6 seconds, 751856 KiB peak RSS, one CPU.

**Limit:** the upstream heterogeneous construction was replayed using the published implementation and read as a theorem dependency, not independently formalized or re-proved end to end. This is stronger than trusting the worker's vector hash but not independent foundational certification of Tandon's theorem. The new extension itself needs only elementary Cartesian-product separation plus the eleven relations in [Definition 5 / Proposition 1](https://arxiv.org/html/2608.30273v1#S4.SS1).

## AH: an actual admissible deterministic algorithm, plus an endpoint clarification

The three transferred quantities are **container proportions**, not random probabilities. The source algorithm's floor-tracking mechanism realizes fixed proportions deterministically, and all destination/source types were already supported. No new container size, class boundary, online information, or lookahead is introduced. Feasibility and item-weight constraints are the relevant bridge to [Theorem 24](https://arxiv.org/html/1707.01728#Thmtheorem24), not empirical benchmark behavior.

The expected complete check is all consecutive breakpoints induced by class boundaries and supported container volumes/complements, both offline-bin cases for each interval, and all large threshold-class inequalities. Strict infimum-size knapsacks are correct: allowing equality at capacity can add physically unrealizable patterns; dropping genuine subcapacity patterns would be unsound. Tiny-only and huge-plus-tiny bins must remain covered.

A source endpoint-convention ambiguity was found: the `(x,y]` convention and static weight at positive volume `1−y` disagree at `a=1−y`. This is **not a counterexample to the numerical bound**. An explicit interior analysis threshold in the strict unmatched-container gap repairs it without changing AH. See `AH_ENDPOINT_CONVENTION.md` for a complete lemma, source anchors, and suggested proof paragraph. This clarification is not supplied by a scenario-count check alone.

Fresh numerical checker `ah_fresh_check.py` and result `ah_fresh_check.log` **PASS** all 402 scenarios, 804 strict knapsacks and 492 large-class inequalities at the claimed exact rational target. It has no worker/advisor imports, parses primary HTML independently, reconstructs scenarios and source weights, uses interior threshold comparisons, and target-prices with exact integer lattices. It deliberately performs **no one-item dominance deletion**, reducing a common-mode risk shared by prior checkers. It visited 109,845,241 nodes in 98.98 seconds and 17292 KiB peak RSS on one CPU.

## Literature / priority assessment

Fresh searches were by mathematical framework, named algorithm, author/title, repository, model and refinements, not only proposed decimals. The examined [Tandon primary preprint](https://arxiv.org/abs/2608.30273), [author repository](https://github.com/tandonravi/C7-Shannon-Capacity-Heterogeneous-Recursion), and [current BPZ repository](https://github.com/spectra-research/shannon-capacity-lean) retain the earlier numerical bounds; the latter advertises 3.258827985920007. No matching recycling refinement was located.

For packing, the [ESA 2018 primary publication](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESA.2018.5) is the source AH result. A later author-primary [WADS 2025 paper](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.WADS.2025.26) still gives the classical interval [1.54278,1.57829]. Smaller numbers from [parallel/k-copy packing](https://arxiv.org/abs/1910.03249), stochastic input models, advice, absolute ratios, multidimensional packing, and heuristic benchmark papers do not answer the same question. No subsequent matching three-transfer refinement was found.

**Conclusion:** both claims survived this independent audit as correct finite/numerical refinements subject to their stated inherited theorem dependencies and the explicit AH endpoint clarification. They are potentially new *numerical bounds within established frameworks*, not resolutions of the open problems. The local mathematical checks cannot establish that no unpublished, unindexed, or later primary source has the same bound. Avoid “first,” “record,” “breakthrough,” and unconditional priority language until external review and a broader priority check.

## Portable reproduction packet

The frozen `*_fresh_check.py` scripts document the original audit runs and paths. For integration, use:

```sh
python c7_portable_check.py --track-root /path/to/seven-cycle-capacity
python ah_portable_check.py --track-root /path/to/online-bin-packing
```

`ah_primary_numerical_facts.json` contains only independently extracted source numerical data and provenance, not paper prose. It was produced by `extract_ah_primary_facts.py PRIMARY.html OUTPUT.json`; its SHA256 is `99a00d0648429fd93d0c56c79c4351cf7a3dff967a104f70b0e75979c8af3dad`. The portable AH checker defaults to this JSON beside it, or accepts `--facts`. Its full replay passed the same 109,845,241 nodes, 402 scenarios and 804 cases in 94.77 seconds (13056 KiB peak RSS), recorded in `ah_portable_check.log`. This second run checks the extraction/replay route, not a second independent mathematical method. The original first run directly parsed the primary HTML.

The portable C7 checker differs from its passing original only by argparse/import/path selection, and was syntax checked; no duplicate full replay was performed. It needs the existing `published/` source/certificate subtree. Both checkers enforce one-CPU affinity, 2 GiB address-space and finite CPU limits on Linux. External 295-second wall timeouts were used for the original runs.
