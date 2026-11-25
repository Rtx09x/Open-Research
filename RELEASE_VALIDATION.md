# Founding collection: release validation

Validation run: 25 November 2026. Research statements remain subject to their stated model assumptions, analytic proof review and prior-work comparison. An internally reproduced certificate is not independent human review, peer review, or a priority determination.

## Files and navigation

- The ten project README pages and the five domain indexes were checked for local link targets.
- All supplementary ZIP archives passed ZIP integrity tests; their released SHA-256 manifests were checked.
- The frozen 26 October research checkpoint was reconstructed from the source repository; all 1,056 transferred source files matched their Git blob identifiers. Its `verify_manifest.py` passed for all 956 files covered by that manifest. Two original-paper trees and the manifest itself have separately preserved source identities.
- The calibration package's `verify_manifest.py` passed all 144 manifest/audit records. Both frozen manifests also passed from a fresh checkout of the staged release. `.gitattributes` preserves byte-exact line endings in these packages.
- The quantum A2 package's `verify_package.py` passed its packaging, syntax and receipt checks; this is not a replay of all its scientific claims.

## Executable checks

Runs used Python 3.12.14; where applicable: NumPy 2.3.5, SciPy 1.17.0, SymPy 1.14.0, NetworkX 3.7 and python-flint 0.9.0. Assertions were enabled.

- Physical state machines: the original `scripts/verify.sh` completed successfully in a disposable copy.
- Resistance-based fault diagnosis: `python run_checks.py --full` passed all 31 core and extended runs in a disposable copy.
- Symmetric quantum codes: `run_checkpoint_20261026.py --only quantum` passed 8 checks. The separate `quantum-independent-audit/verify_full_certificate_independent.py` also returned PASS using exact arithmetic and outward-rounded 256-bit Arb intervals. This is a certificate arithmetic replay and does not independently establish every analytic hypothesis or novelty.
- Sequential calibration: the package manifest and `certification/replay_rational_certificate.py` passed; the latter checked 4,988 coverage boxes. The uniform induction and its v3 repair still require external analytic scrutiny.
- Online packing: `run_checkpoint_20261026.py --only packing` passed 5 checks for the specified algorithm.
- Hierarchical matrix recovery: `run_checkpoint_20261026.py --only hss` passed 12 checks for the scoped constructions and controls.
- Single-deletion codes: `run_checkpoint_20261026.py --only deletion` passed the archive replay, including its stated root-case controls.
- Seven-cycle capacity: `run_checkpoint_20261026.py --only c7` passed 12 checks for the recorded finite gates.
- Sparse conductance recovery: `test_exact_recovery.py` passed its exhaustive and randomized controls. The composition addendum's `test_exact.py` passed its graph and recovery checks.
- Quantum-channel capacity: both standalone obstruction checkers passed. Their conclusions apply only to the models stated in the notes.

The checks do not cover every theorem, every supplementary archive or every claim in all ten projects. No complete proof-assistant formalization, comprehensive literature search or independent expert review is asserted.
