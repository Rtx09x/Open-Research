# Structure and Uncertainty in Resistance-Based Fault Diagnosis

The core of the resistance-diagnosis research track: the current paper, its complete source, and reproducible checks of its stated claims. All other studies and historical material are excluded.

- [Reviewed manuscript, 37 pages](manuscript/structure_uncertainty_fault_diagnosis.pdf)
- [Complete LaTeX source](manuscript/structure_uncertainty_fault_diagnosis.tex), with inline bibliography and no external figures
- [Opposite leaf-pairing construction proof](research/planner/OPPOSITE_PAIRING_PROOF.md)

Author: Rudra Tiwari, University of Delhi, India. The manuscript is the reviewed 16 October 2026 version, preserved byte-for-byte. Review and verification involved AI assistance; “reviewed” does not mean independent human peer review, publication acceptance, or certified novelty.

## Results and limits

For a known positively weighted network, the paper studies diagnosis from scalar pair-resistance measurements. It proves restricted-terminal ambiguity, connected-graph adaptive recurrence, bridgeless fixed-design/access formulas, explicit adaptive-versus-fixed gaps, universal single finite-change recovery, and severity/noise-dependent bounds. The full assumptions and analytic proofs are in the manuscript.

Generic exact deletion, unknown finite conductance change, severity intervals, and bounded adversarial noise are different models. The connected-graph recurrence is exponential in the number of blocks plus bridges. Finite-change recovery assumes one change preserving connectivity. Unknown topology, component uncertainty, drifting faults, and general multiple-fault recovery are not claimed. Finite tests are corroboration, not substitutes for analytic proofs or an originality review.

## Essential code

- `exact_search.py` and `verify.py`: exact response/search and independently formulated certificate checks, with adversarial regressions.
- `research/planner/` and `research/connected_planner/`: topology-based planners and tests.
- `research/terminal_extension/`, `research/access_optimality_extension/`, `research/connected_extension/`, and `research/structural_extension/`: current terminal, access, topology and prism audits.
- `research/universal_recovery/`, `research/new_theorem_audit/`, and `research/realistic_fault_extension/`: exact single-change, parallel-path and severity checks.
- `explicit_gap.py`, `precision_tradeoff.py`, `weighted_noise_lower.py`, `research/noise_extension/`, and `research/clique_noise_extension/`: explicit-family and bounded-noise evidence.

`generic_audit.py` is retained as a required dependency of the biconnected audit. All retained scientific algorithms are unchanged; `run_checks.py` selects only evidence for the main paper. Tests generate their own data, so no historical result dumps or large certificate archives are needed.

## Build

From this directory, with configured TeX Live and the AMS, geometry, booktabs, hyperref and microtype packages:

    bash scripts/build_pdf.sh

Three LaTeX passes produce the main PDF. The supplied reviewed PDF is included, so reading the paper does not require TeX.

## Verify

Use Python 3.12 or newer, excluding 3.14.1 under the pinned NetworkX requirements. In a disposable copy:

    python -m venv .venv
    . .venv/bin/activate
    python -m pip install -r requirements.txt
    python run_checks.py
    python run_checks.py --full --output verification-results.json

The default runs 12 core checks; `--full` adds 19 exhaustive or extended audit runs (30 distinct entry points overall, with the explicit-family checker run at two size ranges). Keep assertions enabled: do not use `python -O`. Programs may generate adjacent JSON results. Generated results and Python caches are intentionally not tracked.

## Fresh core validation, 23 October 2026

All 12 core checks and all 19 extended audit runs passed in a disposable copy with SymPy 1.14.0 and NetworkX 3.7. The main manuscript rebuilt successfully to 37 pages with no unresolved references or citations. Temporary TeX format/font-map configuration was needed for the container, not for the source. The committed PDF remains the original reviewed file. These are finite exact/combinatorial checks, not a full formal proof or independent human replication.

## Deliberately excluded

Gaussian and joint-uncertainty supplements, multiple/mixed/structured-fault studies, nominated-tree and compositional studies, exploratory/historical manuscripts, partial Lean packages, duplicate exports, and old verification logs are outside this two-paper core. They do not strengthen the main manuscript by implication. No full proof-assistant formalization is claimed. The original complete workspace is preserved separately as the backup.
