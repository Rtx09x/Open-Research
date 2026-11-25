# Reproducibility and attribution

## Environment and safety of replay

Observed Python: 3.12.14; NumPy 2.3.5; SciPy 1.17.0; SymPy 1.14.0. Exact pins are in `requirements-research.txt`. No dependency installation is needed for standard-library-only checkers. The upstream C7 optional test pin is pytest 8.3.3; it was not installed or observed here.

`run_checks.py` copies each relevant track into a temporary directory, so replay cannot overwrite committed certificates. Each subprocess gets one BLAS thread, a 2 GiB address-space limit, and a 300 CPU-second limit. Checks are sequential by default. Run without Python `-O` because assertions are part of verification. The long deletion checks fail closed on incomplete enumeration; their counts and hashes are compared independently. A timeout is failure, not a certificate.

The suite checks exact certificate algebra, cardinalities, root brackets, finite exhaustive controls, selected source constants, and the independent Gram-map identity. It does not prove all source mathematics, establish publication priority, solve remaining conjectures, or constitute exhaustive formal verification. Recorded original run outputs may contain machine-dependent timings. `integration/verification.json` records integration runs; the original scientific data are preserved unless a portable-path adaptation is explicitly recorded.

## Source and licensing policy

The five folder `literature.md` files and proof notes attribute mathematical sources. The C7 `published/` dependency is an attributed public source snapshot at commit `c753408492dde92a239708986d16c15dbf6c3235`; preserve its Apache-2.0 LICENSE and NOTICE. Upstream Lean provenance is recorded under `published/upstream/`. No new blanket license is granted to original research or preexisting repository content.

No full downloaded paper, HTML reading cache, raw user conversation, internal quota/task ledger, credentials, `.git` history copy, Python cache, or large exploratory operator array is added. The packing audit carries numerical factual tables extracted by its independently authored parser, with exact source-content hash and URL; it does not carry article prose. A hash pins a source copy, not the truth of its theorem or the completeness of a literature search.

## What is frozen

`checkpoint_manifest.json` inventories every integrated file except itself, with SHA-256 and byte length. `verify_manifest.py` recomputes those hashes. `integration/source_adaptations.json` records source-file hashes and portable path/documentation adjustments. Each track's `provenance/original_checkpoint_manifest.*` is an original workspace inventory, **not** a claim that excluded files are bundled; the root manifest is authoritative for this curated snapshot.

The integration starts from remote main commit `3268b983783c3e2001d802af2d68c06bcef00197`, tree `17ccaea7773716c758e263f87f6a27ad97c9df91`. The existing `physical-memory` and `resistance-fault-diagnosis` trees and `.gitignore` are preserved byte-for-byte. Only the root index is revised; new track files are added. Remote tree verification is performed after the leased fast-forward and is reported separately.

## Extra verifier controls

Run `python run_negative_controls.py` to check that four deliberate corruptions are rejected in temporary copies. These controls are not exhaustive security testing. `integration/negative_controls.json` records the passing integration run. Four direct invocations of the upstream Lean/snapshot transcription tests also passed; see `integration/upstream_transcription.json` (not the entire pytest suite).

Additional source-derived numerical audits are bundled in each numerical track's `tests/` directory. The AH audit deliberately uses no dominance pruning and the C7 audit reconstructs the explicit recipe separately from the stored DAG. `integration/AUDIT_FINDINGS.md` records their original audit scope and scientific limitations; any original workspace paths in that historical audit note should be replaced with the portable per-track commands in the current READMEs. The copied original audit manifest is provenance, not the curated inventory.
