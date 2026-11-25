# Phase 3: verified results, boundaries and reproduction

This private checkpoint preserves all earlier papers and proof artifacts. It records internally audited computer-assisted results, not human external peer review, acceptance, exhaustive novelty certification or proof-assistant formalization. Dates identify frozen snapshots; they are not priority claims.

## Read the useful results first

- **Quantum:** [standalone three-error theorem](symmetric-quantum-codes/phase3/t3_verified_bracket.md): **35 ≤ n_min(3) ≤ 37** for complex rank-two codes contained in Sym^n(C²) correcting arbitrary three-qubit errors. Exact 37 existence uses a rational contraction certificate and all 98 reduced KL polynomial identities. Scalar exact exclusions cover n=13–32; no-cloning covers n≤12. Independent n33 and n34 audits reconstruct exact 6j coefficients and check all 516 and 535 used KL eigenvectors, respectively. The t=2 minimum 19 is retained as an intermediate solved case. **Minimum 37 and the general all-t formula remain open and prioritized.** No n35/n36 solver output is used. Read the [priority report](symmetric-quantum-codes/phase3/priority/PRIORITY_REPORT.md), [citation addendum](symmetric-quantum-codes/phase3/priority/CITATION_ADDENDUM.md) and [auxiliary-operator clarification](symmetric-quantum-codes/phase3/terminology_clarification.md).
- **Packing:** [handoff/theorem](online-bin-packing/phase3/HANDOFF.md): the unchanged tiny-Best-Fit algorithm has all-input asymptotic ratio at most `17309229457317341044853136044527531250227952497 / 10967548450040323523815819160873924866844131328` ≈ **1.5782222924443705**. Exact checks cover all 402 scenarios / 804 strict knapsacks. The positive dual proves optimality only in the specified continuous finite-mixture analysis family, not actual algorithm tightness or a solution of the classic lower/upper gap. The separate shared-history lower-bound fork is an obstruction, not a universal lower improvement.
- **Deletion:** [seven-class theorem](deletion-code-optimality/phase2/README.md) proves any length-12 one-deletion code of size ≥317 uses ≥7 VT checksum classes. The complete 868 exact certificates cover 1,716 supports. [Global exact dual](deletion-code-optimality/continuation/release_20261025/README.md) is 320.497437108, with finite-LP bracket [320.497435475376, 320.497437108]; the integer upper stays 320. An exact capped fractional size-320 point is not a code. The [26-selected-coordinate barrier](deletion-code-optimality/continuation/barrier26_release_20261025/README.md) gives fractional mass 320.21514469 with those 26 coordinates integral: that finite relaxation cannot prove 319. This is neither a 320-word code nor a global bound improvement. The actual integer interval remains **316–320**.
- **C7:** [physical results](seven-cycle-capacity/phase3/VERIFIED_PHYSICAL_RESULTS.md) prove the 243-state one-word-exchange closure, restricted alphabet capacities, the complete 486 maximum-code classification on the second boundary, and validity/non-automorphism of a new 367-word seed. The changed-base replay is **worse**, about 3.25882526526239; it does not replace the previous lower bound. The earlier reversed q-overlap intuition is explicitly corrected: larger q helps the neutral-mass term in the displayed recursion. **No new capacity bound** is claimed.
- **HSS:** [replay guide](hss-probe-reuse/phase3/REPLAY.md) and theorem notes record known-dense-basis 4k/(20L+3), finite randomness, exact triangular/path reductions, forest weights, and the audited 12k/factor-3 coordinate star-probing corollary. The path 10-query/factor-85 result is algorithmically superseded by a 6k/factor-2 forest decoder; the coordinate corollary uses standard published star-coloring/probing. The dense-envelope clique is an obstruction. **Full RE02 remains open.**

## Reproduce without discovery solvers or network access

Use Python 3.12, assertions enabled, in a disposable checkout:

```sh
python -m pip install -r requirements-phase3.txt
python verify_manifest.py
python run_phase3_checks.py --output integration/phase3/verification_local.json
python run_phase3_checks.py --only quantum --slow --output integration/phase3/quantum_local.json
```

The first suite includes exact arithmetic and separately labelled finite numerical implementation controls. `--slow` additionally runs both separate full-space n33/n34 SymPy/Arb implementations (each roughly 15 minutes in the observed environment). The runner copies inputs to a fresh writable temporary repository for each command, uses one CPU/BLAS thread, imposes a 2 GiB memory ceiling and bounded CPU/wall time, and makes no network requests. The recorded integration JSON files show commands actually executed; analytic applicability remains in the theorem and audit documents. Optional discovery scripts are not required to check the claims.

The large deletion certificate ZIP is stored as 47 hash-bound byte-for-byte parts no larger than 256 KiB. `replay_k6.py` verifies every part and the full original ZIP hash before temporary extraction, with no external files. Negative controls cover missing certificate completeness, dual signs/coverage/numerators, CG divisors/clique geometry, the fractional obstruction, and additional track-specific corruptions.

C7's expensive changed-base construction is **not rerun** by the portable suite. Its frozen logs and ledger are retained; the new exact component, validity and classification checks are replayed. No claim of a fresh heavy replay is made.

## Provenance and curation

Original approved manifests are retained under per-track `provenance/`; current curated manifests bind the portable files. Only hardcoded deployment paths, private operational prose and index references were adjusted. Mathematical witnesses retain their approved hashes. Source-derived packing weights were already present in the preserved repository; its advisor replay uses those factual tables rather than bundling a raw article copy. Raw papers, screenshots, browser sessions, operational prompts, credentials, environments, caches, discovery arrays and live branch trees are excluded.

The [22:07 PDF](reports/2026-10-25-2207/README.md) is the exact previously delivered snapshot, not a current three-error status report. Earlier candidate-status fields inside immutable certificate artifacts are historical; terminal theorem/audit documents and hash-bound replay reports supersede only their verification status, not their bytes.
