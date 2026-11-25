# Research checkpoint — 26 October 2026

**All five selected main targets remain open.** This is a bounded snapshot of exact intermediate theorems and certificates, with internal independent mathematical/arithmetic audits. External expert review, priority and novelty remain unresolved. Later candidates and newly completed follow-on packets are outside this cutoff.

## Results and exact scope

### Symmetric quantum codes

- [General all-K volume theorem](symmetric-quantum-codes/checkpoints/2026-10-26-all-t-volume/volume_dependency/THEOREM.md): complex K-dimensional symmetric codes correcting arbitrary errors on at most t physical qubits satisfy `n+1 ≥ K(t+1)²`, K≥2,t≥1. Its dependence on established ordinary-LP monotonicity and primary sources is stated explicitly.
- [Rank-two equality exclusion](symmetric-quantum-codes/checkpoints/2026-10-26-all-t-volume/THEOREM.md): for every t≥2, `n ≥ 2t²+4t+2`. The uniform divisibility reduction `2t−1 | 2025` reduces the equality question to finitely many exact arithmetic cases, separately independently reconstructed.
- [Phase-twisted gnu construction](symmetric-quantum-codes/checkpoints/2026-10-26-phase-twisted-gnu/THEOREM.md): explicit algebraic complex codes of length `4t²+2t` for every integer t≥10. This is one below the stated AAB `4t²+2t+1` formula only; it is **not a global best-known or priority claim**.
- Earlier exact [t=2 minimum19](symmetric-quantum-codes/phase2/theorem_and_necessity.md) and [t=3 bracket35–37](symmetric-quantum-codes/phase3/t3_verified_bracket.md) remain intact. The separate n33/n34 implementations were both rerun in isolated portable copies. General all-t optimality and lengths35/36 for t3 remain open. Auxiliary collective-operator counting is not silently substituted for physical-error applicability.

### Online bin packing

The [actual-floor theorem and handoff](online-bin-packing/phase7/HANDOFF.md) give a fixed-algorithm lower ratio1.5782054112079646… against the independently checked [retuned upper1.5782055179987482…](online-bin-packing/phase4/retune_two/TWO_COORDINATE_THEOREM.md). Exactly two small-class proportions are retuned relative to the ordered-suffix anchor; this is not merely a new proof of the older configuration. The seven rational input sizes force the lower count through explicit quota/positive-container invariants. All402 scenarios/804 strict upper knapsacks are replayed independently. The floor applies only to the specified algorithm and stated invariant-preserving architecture, not all online packing. The pending independent type-role chronology is excluded.

### Deletion codes

The [seven-class theorem](deletion-code-optimality/phase2/README.md), [exact global fractional dual](deletion-code-optimality/continuation/release_20261025/README.md), [fractional26-coordinate barrier](deletion-code-optimality/continuation/barrier26_release_20261025/README.md), and [two complete root-case exclusions](deletion-code-optimality/checkpoints/root-exclusions-2026-10-26/README.md) are included. Root5/root11 exclude only normalized size320 codes containing those words under the stated constants/normalization. Two of13 receiver-root choices are closed, not every branch. The global integer interval stays316–320. Fractional points of mass320 or320.21514469 are **not codes**.

### Seven-cycle capacity

The [earlier physical proof package](seven-cycle-capacity/phase3/VERIFIED_PHYSICAL_RESULTS.md) and frozen [fiber](seven-cycle-capacity/checkpoints/checkpoint_fiber_gate_20261026/README.md), [reservoir](seven-cycle-capacity/checkpoints/checkpoint_reservoir_gates_20261026/README.md), [multi-reservoir](seven-cycle-capacity/checkpoints/checkpoint_multireservoir_gate_20261026/README.md), [Hall-diagnosis](seven-cycle-capacity/checkpoints/checkpoint_multireservoir_diagnosis_20261026/README.md), and [finite-subgroup](seven-cycle-capacity/checkpoints/checkpoint_finite_subgroup_gate_20261026/README.md) gates exclude only their stated finite alphabets or constructions. The subgroup bound≤367 concerns finite subgroup/translates in `(R/Z)^5` at circular coordinate-max distance≥2/7, not arbitrary codes or Shannon capacity. No lower-bound gain is claimed. The changed-base replay remains worse; it does not replace the prior lower bound. The expensive construction replay is not repeated here.

### HSS probe reuse

The [scalar/mixing packet](hss-probe-reuse/checkpoints/2026-10-26-scalar-mixing/README.md) proves six products/factor801 for prescribed real scalar bases, with a separate complex scalar phase-gauge corollary. For arbitrary real rank k, the6k-product factor `5+16δ⁻⁴+32δ⁻⁸` requires every live child-transfer singular value in `[δ,sqrt(1−δ²)]`; bases are fixed before both query banks. It is not arbitrary-transfer or learned-basis recovery. The [structural controls](hss-probe-reuse/checkpoints/2026-10-26-structural-controls/README.md) include a conditional-source obstruction and a channel-separable corollary; the obstruction does not refute the unconditional scalar theorem. Full RE02 remains open. Earlier restricted phase3 reductions are preserved; simpler known decoders supersede some of their algorithmic bounds.

## Reproduction

```sh
python -m pip install -r requirements-phase3.txt
python verify_manifest.py
python run_phase3_checks.py
python run_phase3_negative_controls.py
python run_phase3_checks.py --only quantum --slow
python run_checkpoint_20261026.py
```

Assertions must remain enabled. Pinned dependencies are NumPy2.3.5, SciPy1.17.0, SymPy1.14.0 and python-flint0.9.0; many exact checks need only stdlib. The portable runners use fresh writable temporary copies, one CPU/BLAS thread, a2GiB address-space ceiling and bounded runtimes, without network or discovery solvers. Analytic applicability is in the theorem/audit prose; finite numerical implementation controls are not represented as proofs. Recorded results are in `integration/phase3/` and `integration/2026-10-26/`.

Large immutable proof data are stored once as hash-bound parts. The standalone seven-class helper reassembles its exact original ZIP. `materialize_replay_assets.py` reconstructs the C7 reservoir data and solid root5/root11 archive in a disposable copy; `run_checkpoint_20261026.py` calls it automatically. The latter archive saves88MB of repeated exact model expansions in2.79MB and binds all296 members. No live branch/frontier or raw solver search state is included. Deliberately corrupted certificates, missing support, wrong signs/coverage/numerators/geometry and changed archive parts must be rejected.

## Preservation and provenance

The parent is private main `5ed65add96d4290ea8cc1bc772f408850bb01c14`. All its paper/proof blobs are preserved; only the readable root index and cumulative hash manifest are changed. New manifests bind selected frozen bytes. Original frozen README/manifest mentions of a local-only hold describe freeze-time provenance, not the status of this later authorized checkpoint; they are not proof assumptions. Source-path-only verifier adaptations and the portable source-derived packing-table loader are documented in integration provenance. The original primary-derived packing audit is retained; portable replay does not claim to reparse article HTML.

No private account data, browser transcripts/screenshots, credentials, operational coordination ledgers, environments/caches, live exploratory arrays or raw paper copies are included. The [previously delivered PDF](reports/2026-10-25-2207/README.md) remains unchanged as a dated22:03 report delivered22:07 on25October, not the current status.
