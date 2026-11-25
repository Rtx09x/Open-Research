# Phase 2: structural tiny-container improvements with exact certificates

**Preferred global upper bound:** tiny Best Fit across all previously created advertised tiny containers, with the frozen three-transfer parameters and unchanged non-tiny AH, has competitive ratio at most

`174191383514152461065273968497444592350661 / 110371486054812972793114744355465098952704 ≈1.5782281252210837`.

Its new chronological residual-gap lemma, source-proof portability, and all402/804 exact pricing cases independently pass. See `best_fit/BEST_FIT_THEOREM.md`. No actual-ratio tightness or threshold-optimality is claimed for this successor.

## Preserved one-open anchor

The fixed three-transfer AH variant with delayed tiny-container closure has exact asymptotic ratio

`23211234258164394107066141961880719040528132151 / 14707121654123980930208343329037931077093556224 ≈1.5782309281201736`.

Both directions have separate proofs and independent advisor audits. This is an algorithm-specific exact ratio and a global **upper-bound** improvement; it does not improve the universal lower bound or solve the full gap. Publication priority and external human/formal review are unestablished.

## Read first

1. `best_fit/BEST_FIT_THEOREM.md`: the preferred new algorithm, residual-gap proof, discontinuous step charge, and exact all-case upper bound.
2. `SINGLE_THRESHOLD_THEOREM.md`: one-open upper bound; mixtures collapse to a single threshold; exact continuum optimization; scoped local-certificate characterization.
3. `coupled/SATURATION_THEOREM.md`: one-open finite rational construction, exact OPT, source-quota online cost lower bound, and actual tightness.
4. `AUDIT.md`: preceding Pro hypotheses, original-rule counterexample, and restricted causal t=3 history.
5. `HANDOFF.md`: dependencies, entrypoints, evidence layers, and remaining targets.

## Reproduce

Run from this folder's parent directory:

```sh
ulimit -v 1048576
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
timeout 290 python phase2/exact_threshold_search.py
timeout 290 python phase2/verify_single_thresholds.py
timeout 290 python phase2/coupled/check_saturation.py
timeout 290 python phase2/best_fit/check_all_cases.py
timeout 290 python phase2/best_fit/verify_step_independent.py
```

All use the standard library. Each upper verifier checks402 intervals and804 exact strict knapsacks. The saturation checker is a tiny-prefix/refinement execution checker for the one-open algorithm, not a complete AH simulator; its full online-cost argument is analytic.

Initial frozen phase-1 files are unchanged. This phase changes no proportions relative to that snapshot. All new writes are confined to `phase2/`. Pro replay artifacts and the initial numerical discovery script are retained for provenance but are not needed for the preferred exact reproduction.
