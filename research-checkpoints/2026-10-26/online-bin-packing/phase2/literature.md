# Phase-2 literature and provenance note

Checked2026-10-25. Model remains classic deterministic online unit-bin packing with arbitrary item sizes, immediate irrevocable placement, and asymptotic worst-case competition. No advice, repacking, random-order, cardinality, or extra-capacity model is substituted.

## Primary foundations

* [Balogh et al., A New and Improved Algorithm for Online Bin Packing](https://arxiv.org/html/1707.01728): full AH definitions, parameter tables, weight scenarios, and container-count invariants. Source Sections3–5, especially Lemma5, Corollaries6/8, and the proof of Lemma19, are used directly in the saturation theorem. The [ESA2018 record](https://doi.org/10.4230/LIPIcs.ESA.2018.5) is the published conference version.
* [Balogh et al., A New Lower Bound for Classic Online Bin Packing](https://arxiv.org/abs/1807.05554): the published adaptive lower-bound framework. The original t=3 history audit is a restricted-family feasibility result, not an improvement on this universal lower bound.
* [More on Online Cardinality Constrained Bin Packing with Small Cardinality Bounds,2026](https://doi.org/10.1016/j.tcs.2026.115774): a current status anchor that distinguishes the classic problem from its own cardinality variant. It is not treated as a classic-bound improvement.
* [FunSearch](https://doi.org/10.1038/s41586-023-06924-6): empirical heuristic discovery is not the all-input asymptotic proof used here.

The original literature/version audit is preserved unchanged in `../literature.md`, including the later author dissertation's identical old AH rational certificate. Phase2 reads the frozen audited parameters rather than silently changing the source algorithm.

## Narrow priority refresh

Additional targeted searches on2026-10-25 for `"online bin packing" "1.57823"`, `"bin packing" "tiny" "delayed" "Advanced Harmonic"`, and current classic-bound references did not reveal a relevant published matching result. The search returned many different variants and empirical methods; these were not used as proof sources.

Absence from these searches does not establish novelty. The exact rational improvement, delayed-closure modification, and structural saturation theorem should be described as independently checked internal research results pending external priority and human/formal review. The unchanged universal lower endpoint and the algorithm-specific nature of the new tightness statement must remain explicit.
