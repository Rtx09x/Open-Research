# Research

A private working repository of precise models, proofs, and reproducible research checkpoints. A checked finite certificate is not a solution of an entire open problem, an independent human peer review, or a certification of novelty.

## Current checkpoint — 26 October 2026

**All five main research targets remain open.** The repository contains rigorous intermediate finite results, restricted theorems, exact certificates and documented obstructions—not a claim that the broader problems are solved. See [the dated status and replay guide](CHECKPOINT_2026-10-26.md).

| Track | Checked intermediate result | Unresolved boundary |
|---|---|---|
| [Quantum codes](symmetric-quantum-codes/checkpoints/2026-10-26-all-t-volume/THEOREM.md) | General volume bound `n+1 ≥ K(t+1)²`; for rank2 and t≥2, `n ≥ 2t²+4t+2`. Explicit complex construction `n=4t²+2t` for t≥10. Finite t2 minimum19 and t3 bracket35–37 retained | General minimum formula and exact t3 minimum still open; construction comparison is only against the stated AAB formula, not a best-known/priority claim |
| [Online packing](online-bin-packing/phase7/HANDOFF.md) | Specified retuned algorithm has actual ratio bracket **1.5782054112079646… to 1.5782055179987482…** | Lower endpoint is algorithm/architecture-specific, not a universal online lower bound; classic gap open |
| [Deletion codes](deletion-code-optimality/checkpoints/root-exclusions-2026-10-26/README.md) | Seven-checksum-class necessity and two exact normalized root-case exclusions | Global optimum remains **316–320**; no global319 proof or size320 code |
| [Seven-cycle capacity](seven-cycle-capacity/checkpoints/checkpoint_finite_subgroup_gate_20261026/README.md) | Exact physical closures and several restricted architecture/group obstructions | **No capacity improvement**; unrestricted capacity remains open |
| [HSS recovery](hss-probe-reuse/checkpoints/2026-10-26-scalar-mixing/uniformly_mixing_fixed_basis_bound.md) | Prescribed scalar bases:6queries/factor801; prescribed uniformly-mixing real rank-k bases:6kqueries/depth-independent constant | Unknown-basis full RE02 and unrestricted-transfer arbitrary-rank constant recovery remain open |

These are internally audited computer-assisted results, **not external peer review, acceptance, exhaustive novelty or publication-priority certification**. Prior papers and proof files remain unchanged. Dated older statuses below are historical, and later live experiments are excluded from this snapshot.

## Phase-3 checkpoint — historical, 25 October 2026

Start with [PHASE3.md](PHASE3.md), the scoped results and isolated replay guide.

| Track | Internally verified checkpoint | Still open / limitation |
|---|---|---|
| [Symmetric quantum codes](symmetric-quantum-codes/phase3/t3_verified_bracket.md) | **35 ≤ n_min(3) ≤ 37**, with exact existence at 37 and independent n33/n34 exclusions; earlier t=2 minimum 19 retained | **General all-t goal remains open and prioritized**; minimum 37 is not proved |
| [Online bin packing](online-bin-packing/phase3/HANDOFF.md) | Same tiny-Best-Fit algorithm, stronger all-input asymptotic upper ratio **≤1.5782222924443705** | Optimized finite-mixture analysis family only; classic gap and actual algorithm tightness open |
| [Deletion codes](deletion-code-optimality/phase2/README.md) | Every length-12 code of size ≥317 needs ≥7 checksum classes; exact global fractional dual and a selected-integrality obstruction | Integer interval remains **316–320**; fractional witnesses are not codes |
| [Seven-cycle capacity](seven-cycle-capacity/phase3/VERIFIED_PHYSICAL_RESULTS.md) | Exact finite closures/classification and a valid non-automorphic 367-word seed | **No capacity improvement**; changed-base replay is worse |
| [HSS probe reuse](hss-probe-reuse/phase3/REPLAY.md) | Audited restricted reductions, path/forest and coordinate-probing lemmas | **Full RE02 open**; some constructions are superseded by simpler known decoders |

All verification here is internal computer-assisted research, not external expert review, acceptance, priority certification or full formalization. The [dated 22:07 report](reports/2026-10-25-2207/README.md) is a historical snapshot, not the later quantum status. All prior proof and paper files are preserved; only this index and the cumulative hash manifest are updated.

## Phase-2 results — historical checkpoint, 25 October 2026

See [the phase-2 reading and reproduction guide](PHASE2.md) for proof scope, exact certificates, independent internal audits, and the replay commands.

| Track | Internally verified result | Boundary |
|---|---|---|
| [Symmetric quantum codes](symmetric-quantum-codes/phase2/theorem_and_necessity.md) | **Minimum n=19** for a two-dimensional complex code inside the fully symmetric n-qubit subspace correcting arbitrary errors on at most two physical qubits; computer-assisted proof | Not arbitrary permutation-invariant projectors outside that subspace; general all-t conjecture remains open |
| [Online bin packing](online-bin-packing/phase2/best_fit/BEST_FIT_THEOREM.md) | Tiny Best Fit structural successor: asymptotic competitive ratio **≤1.5782281252210837**; previous one-open algorithm has a separately proved exact algorithm-specific ratio | No universal lower-bound improvement or optimality/tightness claim for Best Fit |
| [HSS probe reuse](hss-probe-reuse/phase2/fixed_basis_bound.md) | **4k total queries**, expected squared error **≤(20L+3)** times the best approximation with independently prescribed dense nested bases | Not the unknown/adaptive-basis full RE-02 target |

These are internally audited research results, **not external peer review, publication acceptance, exhaustive novelty certification, or proof-assistant formalization**. Earlier checkpoint files are retained unchanged as historical artifacts; the phase-2 documents supersede their status statements only where explicitly indicated. The existing papers and the other two research checkpoints are unchanged.

## Initial checkpoints — historical, 25 October 2026

| Folder | Established checkpoint | Still unresolved |
|---|---|---|
| [Deletion-code optimality](deletion-code-optimality/) | Exact radius-nine local barrier around VT0(12): every different code of size at least 316 removes at least 10 baseline words | Global length-12 optimum; the checked literature interval remains 316–320 |
| [Symmetric quantum codes](symmetric-quantum-codes/) | Nondegeneracy reduction, restricted subcase exclusions, exact necessary variance bounds, and a generator reformulation | Unrestricted 18-qubit two-error code existence; no proof that 19 is minimal |
| [HSS probe reuse](hss-probe-reuse/) | Minimal-sketch obstruction, known-tree-support theorem, fixed-basis unbiasedness, and an exact counterexample to a proposed proof potential | Full RE-02 and general reused-probe variance bound |
| [Seven-cycle capacity](seven-cycle-capacity/) | Exact finite construction: **Θ(C7) ≥ 3.258832624232849476** in dimension 768,000 | Exact Shannon capacity and priority of this small refinement |
| [Online bin packing](online-bin-packing/) | Three-parameter Advanced Harmonic refinement: asymptotic ratio **≤ 1.5782320611603713** | Broader algorithmic optimality and publication priority |

The two numerical improvements are relative to the cited, reproduced constructions/certificates, not assertions of an exhaustive literature frontier. Each depends on the mathematical assumptions and source theorems explained in its proof. The other tracks contain scoped reductions or obstructions only. Initial expert-consultation packets are not conclusions and are not bundled as evidence.

### Reproduce

Run in a disposable checkout with Python 3.12. The principal independent rational checkers use the standard library; the full suite additionally uses the observed pinned scientific dependencies:

```sh
python -m pip install -r requirements-research.txt
python run_checks.py --full --output integration/verification_local.json
python verify_manifest.py
```

The runner executes each check in a fresh temporary track copy, sets one BLAS thread, applies a 2 GiB address-space ceiling and a 300 CPU-second per-check limit, and never downloads data or uses the network. It is sequential by default. `--full` includes both independent radius-nine exhaustive deletion enumerations; omit it for the shorter certificate/control suite. Python assertions must remain enabled. See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for audit boundaries and source/licensing details. [The recorded integration replay](integration/verification.json) is evidence of the commands actually run, not a claim of complete formal verification.

## Existing papers — preserved unchanged

- [Physical memory](physical-memory/README.md): **Physical Resource Complexity of Hysteretic State Machines: Realizability, Optimal Memory, and Interaction Tradeoffs.** The resource cost of implementing prescribed transitions with interacting binary switching elements.
- [Resistance-based fault diagnosis](resistance-fault-diagnosis/README.md): **Structure and Uncertainty in Resistance-Based Fault Diagnosis.** The scalar-measurement cost of identifying faults under topology, terminal-access, severity and error constraints.

### Reading and reproduction of the existing papers

Start with a track README and its linked current PDF. Each track includes the complete LaTeX source and required dependencies, analytic proofs in the manuscript, and a focused executable check suite. Follow the track README to build and test in a disposable copy. Exact computational evidence and finite numerical checks do not replace the stated analytic proofs.

The current manuscripts are the reviewed 16 October 2026 versions: 22 pages for physical memory and 37 pages for fault diagnosis. They are preserved byte-for-byte. Author: Rudra Tiwari, University of Delhi, India. The work involved AI assistance; “reviewed” does not mean independent human peer review, publication acceptance, exhaustive novelty certification, or full proof-assistant formalization. No new license is granted by this repository.

### Scope of the existing-paper core

Within these two existing paper folders, only the two current manuscripts, their compilation dependencies, essential current-claim proof/code/tests and required exact input fixtures are included. Historical drafts, exploratory branches, separate supplement papers, duplicate exports, archived workspaces, old result logs, build intermediates and formalization fragments are excluded. The original complete workspace is preserved separately as the backup.

Proved statements, finite evidence, conjectures and unresolved questions must remain clearly distinguished. Model assumptions and limitations belong with every claim. New research tracks should follow the same structure rather than accumulating unrelated drafts in an existing track.
