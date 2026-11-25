# Phase-2 verified research package

## Read the strongest result with its precise scope

1. **Symmetric two-error quantum codes:** [full theorem and necessity proof](symmetric-quantum-codes/phase2/theorem_and_necessity.md), [independent applicability report](quantum-independent-audit/INDEPENDENT_APPLICABILITY_REPORT.md), and [hostile applicability audit](advisor/phase2/quantum_hostile_applicability_audit.md). The internally established computer-assisted result is n_min=19 for two-dimensional complex codes whose vectors all lie in Sym^n(C²), correcting arbitrary errors on at most two physical qubits. It does not settle the all-t conjecture or the broader permutation-invariant-projector model. The n≤8 analytic no-cloning argument, separate exact n=9..17 exclusions, new n=18 interval dual, and exact known n=19 existence proof close distinct parts of the chain. The shorter exclusions and n=19 construction are prior art, not new inventions.
2. **Online bin packing:** [Best Fit theorem](online-bin-packing/phase2/best_fit/BEST_FIT_THEOREM.md), [independent audit](advisor/phase2/packing_best_fit_audit.md), and [handoff](online-bin-packing/phase2/HANDOFF.md). The preferred upper bound is exactly `174191383514152461065273968497444592350661 / 110371486054812972793114744355465098952704` (approximately 1.5782281252210837). The [earlier one-open saturation theorem](online-bin-packing/phase2/coupled/SATURATION_THEOREM.md) proves tightness for a different algorithm only. Do not transfer that tightness to Best Fit or interpret it as a universal online lower bound.
3. **HSS with prescribed bases:** [fixed-basis theorem](hss-probe-reuse/phase2/fixed_basis_bound.md) and [independent analytic audit](advisor/phase2/hss_dense_fixed_basis_audit.md). It uses 2k forward plus 2k transpose queries for the (20L+3) expected squared-error guarantee. The [explicit finite-randomness variant](hss-probe-reuse/phase2/finite_orientation_variant.md) and [6k-query, factor-two coordinate-forest theorem](hss-probe-reuse/phase2/three_color_forest_theorem.md) have separate scope. Unknown/adaptively learned bases and the full-HSS comparator remain unresolved. `global_ls_status.md` is an exploratory status note, not a proved extension.

All claims remain subject to external mathematical review and priority assessment. Internal independent audits are not external human peer review. No publication, public release, or outsider contact is part of this package.

## Portable replay

Use Python 3.12 without `-O`. All runners copy artifacts to fresh temporary directories, use one BLAS thread, and impose a 2 GiB address-space and 300 CPU-second per-check limit. They never install dependencies, access the network, or modify committed certificates. The exact packing checkers use only the standard library. The HSS implementation controls need NumPy/SciPy. The primary quantum checker needs only python-flint; the independent verifier additionally needs SymPy.

```sh
# In your own disposable environment, if the required packages are not installed:
python -m pip install -r requirements-phase2.txt
python verify_manifest.py
python run_phase2_checks.py --output integration/phase2/verification_local.json
python run_phase2_checks.py --quantum-only --output integration/phase2/verification_quantum_local.json
python run_phase2_negative_controls.py
```

The independent quantum runner recomputes the KL-stability bounds before using them in the full residual checker, then replays every shorter exact certificate and all fifty known19 reduced-Gram relations. Analytic applicability and the n≤8 argument are proof inputs, not conclusions inferred from numerical controls. `interval_dual_candidate.json` retains its historical filename, but its fixed bytes are the audited witness, SHA-256 `201e1acd2e8616807d98d07038174559cc4480aba1cca8b2d736997e251c7a79`.

[Recorded non-quantum replay](integration/phase2/verification.json), [recorded quantum replay](integration/phase2/verification_quantum.json), and [source adaptations](integration/phase2/source_adaptations.json) distinguish freshly executed integration evidence from original worker output. Supplemental model/control scripts and their original measurements are retained as bug detectors, not additional proof assumptions. Optional numerical quantum controls import CVXPY for helper modules; install `requirements-phase2-controls.txt` only to run those controls. No solver is used by either rigorous witness verifier. With the optional dependencies installed, `python run_phase2_controls.py` regenerates the supplemental model checks in temporary copies, including the known19 moment array needed for the all-cone replay. [Recorded supplemental controls](integration/phase2/supplemental_controls.json) contain the actual integration replay.

## Preservation and curation

The update is based on verified private main `de3ea2ee27e5d14bf49ad1c709aa0bbbf489b433`. Every existing non-index research/paper blob is preserved. Only the root README and cumulative checkpoint inventory are revised. No environment, credential, Python cache, raw consultation packet, full downloaded article, bulky operator array, or unreviewed solver result is included. The quantum `provenance/original_evidence_manifest.json` is the original full workspace inventory, not a claim that omitted solver/array files are bundled. Numerical source facts already present in the phase-1 package replace the advisor's full-HTML dependency for the portable packing replays; this adaptation is explicit and does not claim a new live source fetch.

[The phase-2 manifest](integration/phase2/manifest.json) inventories this update, while `checkpoint_manifest.json` remains the cumulative curated-file inventory checked by `verify_manifest.py`. Both exclude themselves as documented. Historical output timings may differ on replay without changing any mathematical conclusion.
