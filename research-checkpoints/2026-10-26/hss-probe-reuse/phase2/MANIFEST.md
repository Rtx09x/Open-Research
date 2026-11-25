# Integration manifest

Main theorem/proof: `fixed_basis_bound.md`.
Main overview: `checkpoint_summary.md`, `README.md`, `research_log.md`.
Primary-literature scope: `literature_phase2.md`; Pro audit: `pro_audit.md`.

Core implementation and tests:
* `fixed_basis_algorithm.py`, `test_fixed_basis_algorithm.py`, associated JSON/log.
* `verify_matrix_one_bank_bound.py`, exact covariance JSON/log.
* `verify_one_bank_sharpness.py`, exact gain JSON/log.
* `verify_one_bank_counterexample.py`, certificate JSON/log and explanation.
* `three_color_forest.py`, verifier, theorem, exact results/log.
* `wavelet_support_obstruction.py`, explanation and exact JSON/log.

Useful failed-route controls: nonbacktracking and ordered-frame scripts,
explanations, JSON/logs; one-bank transport/cross experiments and corrected
`current_sector_bottleneck.md`. The scalar-only proof draft is superseded by
the arbitrary-k theorem and is labeled accordingly.

Large `.npz` operators are optional diagnostic caches, not necessary to replay
the exact core tests. Do not treat supplementary floating-point spectra as
exact certificates. No downloaded primary papers or upstream code need be
copied from the frozen initial folder for these phase-two proofs.

Optional audited finite-randomness construction:
`finite_orientation_variant.md`, `finite_tree_frame` in the main implementation,
`test_finite_orientation_variant.py`, `finite_orientation_results.json`/log.

Exploratory only: `global_ls_probe.py`, `ordered_global_ls_probe.py`, their
JSON/logs, and `global_ls_status.md`. These test a different decoder and are
not part of the proved fixed-basis theorem.
