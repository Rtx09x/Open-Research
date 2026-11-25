# Deterministic online bin packing: literature and scope

Checked 2026-10-25. Target: classic one-dimensional unit-capacity bins, arbitrary rational item sizes, irrevocable deterministic online placement, asymptotic competitive ratio. No lookahead, advice, repacking, cardinality restriction, or random-order hypothesis.

- Balogh, Békési, Dósa, Epstein, Levin, *A new lower bound for classic online bin packing*, arXiv:1807.05554 (2018; subsequently published). https://arxiv.org/abs/1807.05554 . Exact lower bound `(1363-sqrt(1387369))/120 = 1.5427809064729...`. Uses geometric tiny batches, an adaptively separated approximately 1/7 batch, and three alternative suffixes. The paper explicitly says its one-weight optimization is tight and reports small-template mathematical-program checks. It supplies an analytic certificate, so reproducing it does not require an unavailable solver artifact.
- Balogh et al., *A new and improved algorithm for online bin packing*, https://arxiv.org/abs/1707.01728 . Advanced Harmonic gives the upper endpoint 1.57829.
- Epstein and Levin, WADS 2025, *Lower Bounds for Several Standard Bin Packing Algorithms in the Random Order Model*. https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.WADS.2025.26 . Its introduction independently reports the same classic interval; its actual new results concern a different model.
- *More on online cardinality constrained bin packing with small cardinality bounds* (2026), https://doi.org/10.1016/j.tcs.2026.115774 . Explicitly distinguishes classic BP and still cites `[1.54278,1.57829]`. Its improved cardinality bounds do not improve classic BP.
- FunSearch, https://doi.org/10.1038/s41586-023-06924-6 . Empirical heuristic improvement is not an asymptotic worst-case certificate.

Searches for 2025–2026 classic deterministic improvements did not reveal a later global bound. This is a literature check, not a completeness guarantee.

## Reuse rather than reinvention
The starting point is the published adaptive prefix and virtual-bin method, not heuristic benchmarking. New tests add complement branches to this exact architecture. Retuning the published **lower-bound** scalar weight cannot beat that published lower bound. The upper-bound analysis weight is a different optimization and does admit the tiny exact tightening documented in `AH_REANALYSIS.md`. Any result from a restricted adversary relaxation is labeled as such.

## AH exact-bound and publication-version audit

- Primary full version: [arXiv 1707.01728](https://arxiv.org/abs/1707.01728), submission history checked 2026-10-25: only v1 (6 July 2017). Its original exact critical-scenario bound is `10060574276093395247/6374352691333693440`, with `w=413913/524288`.
- [ESA 2018 publisher record](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESA.2018.5) and [author’s University of Haifa publication record](https://cris.haifa.ac.il/en/publications/a-new-and-improved-algorithm-for-online-bin-packing/) identify the conference contribution. No separate journal revision of this upper-bound paper was found in targeted title searches. Do not confuse the Algorithmica 2021 **lower-bound** paper with a revision of AH.
- József Békési, *Contribution to a Class of Combinatorial Optimization Problems*, [DSc dissertation, 2022](https://real-d.mtak.hu/1496/7/dc_2018_22_doktori_mu%20%285%29.pdf), printed page 14, repeats precisely the same `w` and exact rational certificate. This author-primary later source helps rule out a simple arXiv/publication mismatch.
- Searches for the proposed decimal prefixes `1.578289307`, `1.57828930`, `1.5782894`, and exact new numerator found no relevant result. These searches are not a proof of novelty; all priority claims remain withheld.

- For the final two-class refinement, additional searches for `"bin packing" "1.578245"`, `"bin packing" "1.57824"`, and `"Advanced Harmonic" "1.5782"` returned no relevant matching result on 2026-10-25. This does not establish priority; the final claim remains an independently checked internal research result.
