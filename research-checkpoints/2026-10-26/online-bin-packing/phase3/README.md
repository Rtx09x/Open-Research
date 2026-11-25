# Phase3: a killed lower fork and an improved upper analysis

## Preferred upper bound

For the **unchanged phase2 tiny Best Fit AH algorithm**:

`17309229457317341044853136044527531250227952497 / 10967548450040323523815819160873924866844131328 ≈1.5782222924443705`.

Worker and independently primary-derived advisor checks pass all402 scenarios /804 exact knapsacks. A disjoint-successor chronological conservation theorem gives valid two-cutoff item charges. An exact positive three-pattern dual proves optimality within the **entire convex two-cutoff charge family**, not actual algorithm tightness or optimality of online bin packing.

Read `successor_mixture/SUCCESSOR_MIXTURE_THEOREM.md`. Stable full certificate: `successor_mixture/successor_mixture_certificate.json`, SHA256 `48d1e32cefcb5f2c999de480684332a4c2b2b411c4912ffb7e8754ea9f56d64d`.

The earlier independently audited step-mixture bound1.578223124297535 is preserved in `bf_type/`. The intermediate two-cutoff and single-successor candidates are retained for provenance, not presented as the preferred result.

## Lower-bound structural obstruction

The proposed shared marked-B history followed by D≈4/7 or E≈5/14 then above-half C is defeated on the exact nine-state prefix by every paired/quartet fraction in a surviving interval. The simple choice f=1/5 puts every E in fresh pairs and survives all branch-prefix lengths up to the proposed E cap. The obstruction is robust to either sign of small B/E perturbations.

Read `lower_shared/SHARED_FORK_OBSTRUCTION.md`. This is a restricted-family survival theorem, not a global online algorithm or a universal lower-bound improvement.

## Reproduce without changing frozen earlier folders

```sh
ulimit -v 1048576
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
timeout 290 python phase3/lower_shared/verify_shared_fork.py
timeout 290 python phase3/successor_mixture/check_all.py
timeout 290 python phase3/successor_mixture/verify_independent.py
timeout 290 python phase3/successor_mixture/verify_family.py
```

Run from `online-bin-packing/`. Standard library only; each job takes seconds. Phase1 and phase2 are preserved. Earlier fixed-algorithm tightness belongs to the one-open algorithm, not the later Best Fit variant. The classic global gap remains open, and publication priority/external human or formal review remain unestablished.

The next concrete target outside the optimized family is `NEXT_STRUCTURAL_TARGET.md`: terminal creation epochs, their type quotas and birth-item counts. The current package is a completed checkpoint, not a claim to have solved the full gap.
