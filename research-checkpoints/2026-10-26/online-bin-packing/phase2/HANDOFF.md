# Phase-2 handoff

## Preferred result

**Newest global upper bound:** tiny Best Fit across all previous advertised tiny containers, keeping the same frozen parameters and non-tiny AH rules, has competitive ratio at most

`174191383514152461065273968497444592350661 / 110371486054812972793114744355465098952704 ≈1.5782281252210837`.

The new residual-gap lemma and its discontinuous step-weight envelope, source-proof portability, and all402/804 exact knapsacks independently pass. See `best_fit/BEST_FIT_THEOREM.md`. No lower-bound tightness or threshold-optimality is claimed for this successor. It is a genuine architectural change, not another retuning of the exhausted one-open charge.

### Preserved earlier exact-ratio result

The delayed-tiny-closure version of the frozen three-transfer AH algorithm has exact algorithm-specific asymptotic competitive ratio

`23211234258164394107066141961880719040528132151 / 14707121654123980930208343329037931077093556224 ≈1.5782309281201736`.

* Upper direction: an all-input overflow theorem, exact nonlinear tiny fill, and all402 scenario /804 strict-knapsack certificates.
* Lower direction: a finite rational input family jointly realizing the two active offline patterns and the online quota proportions, with exactOPT=N and a direct positive-container cost count.
* Independent advisor audits cover both directions. This is not a universal lower-bound improvement. The global classic lower endpoint remains the published approximately1.54278090647.
* Publication priority, peer review, and formal proof-assistant verification remain unresolved.

## Minimal preferred verification files

For the newest Best Fit result, add these files to the one-open source/provenance bundle below:

```
phase2/best_fit/BEST_FIT_THEOREM.md
phase2/best_fit/best_fit_certificate.json
phase2/best_fit/verify_step_independent.py
phase2/best_fit/independent_step_verification.json
```

The Best Fit verifier imports only the previously audited `weights` reconstruction from `phase2/verify_single_thresholds.py`; it does not import its pricing routine or any Best Fit discovery code. For exact maximization reproduction add `best_fit/check_all_cases.py`, `best_fit/step_pricing.py`, `phase2/verify_nonlinear_independent.py`, and `phase2/exact_nonlinear_pricing.py`. All use the standard library.

Keep these relative paths intact:

```
ah_three_parameter_full_certificate.json       # frozen phase-1 dependency
phase2/single_threshold_certificate.json       # full exact new certificate
phase2/verify_single_thresholds.py              # stdlib all-case checker
phase2/SINGLE_THRESHOLD_THEOREM.md
phase2/AUDIT.md
phase2/coupled/SATURATION_THEOREM.md
phase2/coupled/check_saturation.py
phase2/coupled/saturation_check.json
```

For exact discovery reproducibility also include:

```
phase2/exact_nonlinear_pricing.py
phase2/exact_threshold_search.py
phase2/exact_threshold_search.json
```

The preferred discovery and verification path needs no NumPy/SciPy, network, optimizer service, Pro access, or source HTML parser. The frozen certificate hash and complete parameter/scenario equality checks prevent accidental parameter drift. A separate advisor source parser establishes provenance against the primary paper rather than trusting the frozen snapshot alone.

`manifest.json` inventories phase-2 proof/code/certificate artifacts and their hashes; it deliberately excludes itself, Python caches, and copied Pro replay files. Output JSON files contain measured timings, so rerunning a checker may change its output hash without changing any mathematical content.

## Reproduction

From `online-bin-packing/`:

```sh
ulimit -v 1048576
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
timeout 290 python phase2/exact_threshold_search.py
timeout 290 python phase2/verify_single_thresholds.py
timeout 290 python phase2/coupled/check_saturation.py
timeout 290 python phase2/best_fit/check_all_cases.py
timeout 290 python phase2/best_fit/verify_step_independent.py
timeout 290 python phase2/best_fit/stress_gap_lemma.py
```

Typical runtimes are under3 seconds per command. One CPU and less than1 GiB suffice. Every script was read before execution; no job used external or paid compute. Phase-1 files were not modified.

## Evidence layers and independent audit locations

| Claim | Worker evidence | Independent advisor evidence |
|---|---|---|
| Delayed closure preserves source proof | `AUDIT.md`, direct source inspection | `advisor/phase2/packing_portability_audit.md` |
| Overflow lemma and fill formula | `SINGLE_THRESHOLD_THEOREM.md`;250,000 prefix and13,758 fill tests | Same portability audit and threshold-family audit |
| Full upper fraction | `verify_single_thresholds.py`, `single_threshold_verification.json` | `advisor/phase2/check_packing_single_thresholds.py`, `packing_single_threshold_audit.json` |
| Continuum threshold optimum | Exact affine duals, full pricing, Jensen collapse | Independent exact dual and Jensen checks |
| Actual fixed-algorithm tightness | `coupled/SATURATION_THEOREM.md`, exact tiny/refinement traces | `advisor/phase2/packing_saturation_audit.md`, `packing_saturation_algebra.json` |
| New Best Fit upper bound | `best_fit/BEST_FIT_THEOREM.md`, `best_fit/verify_step_independent.py` | `advisor/phase2/check_packing_best_fit.py`, `packing_best_fit_audit.json`, source/lemma audit note |
| Original t=3 history is causal | `AUDIT.md` section4; inspected/replayed Pro lower files | Restricted source/offline argument reviewed in audit coordination |

The finite saturation trace does **not** run every AH rule. The all-input source quota invariants analytically supply the online-cost lower bound. No conclusion is extrapolated from sampled ratios.

## Proven stopping boundaries

1. Mixtures of the static overflow charges are pointwise dominated by one effective threshold.
2. Exact duals certify each of the three optimized scenarios over the whole continuous threshold range, not only a grid.
3. Under explicit universal quota-neutral linear-load-plus-one-trigger assumptions, the undominated local charges reduce to this hinge family.
4. More strongly, actual saturation inputs show that no stronger analysis of the **same algorithm** can lower its true ratio.
5. The saturation obstruction also survives deterministic tiny type reordering or matching changes that preserve fixed capacities/proportions, bounded quotas, one-open delayed closure, and the positive-container invariants.

## Structural continuation and next unresolved target

Tiny Best Fit across all previously created advertised tiny containers changes the insertion architecture rather than its analysis. The small fillers in the saturation input can refill old overflow holes. `coupled/probe_tiny_best_fit.py` first confirmed the mechanism:1,000 source tiny containers reduce to967, and positive tiny containers579 to560. The subsequent chronological high-residual lemma closes an all-input proof, producing the preferred bound above after all-case and independent audits.

Freeze this new structural successor rather than extend an unbounded tuning chain. Its actual tightness is open. The step certificate uses the conservative minimum capacity A_min to bound the number of high-gap containers; an eventual type-resolved conservation theorem would be a principled further target, but no such improvement is claimed here. The whole Best Fit parameter/threshold family is not certified optimal.

The external consultation already owns the separate lower-bound branch marking B placements into exactly-two-A bins. This worker did not duplicate that work. No additional Pro request is authorized or needed for the present verified package.

## Integration guidance

Prefer the newest Best Fit upper fraction above, with its distinct algorithm definition and explicit novelty/review caveats. Preserve the one-open exact-ratio theorem as a separate stronger statement about an earlier, different algorithm. Keep phase1 as a historical independently checked anchor too. Do not transfer one-open tightness to Best Fit, or present either algorithm-specific result as the optimal online ratio. Parent owns repository integration and user-facing updates; this worker made no git commit or push.
