# Binary single-deletion codes

## Question

What is the maximum size of a binary length-12 code correcting a single deletion?

## Results and scope

The archived global interval remains 316–320. The checkpoint reports two normalized size-320 root-case exclusions, not a global upper bound of 319. Other artifacts document partial structural and local-barrier results.

## Materials

[Root-case exclusions](../../research-checkpoints/2026-10-26/deletion-code-optimality/checkpoints/root-exclusions-2026-10-26/README.md) · [Track](../../research-checkpoints/2026-10-26/deletion-code-optimality/)

## Verification and limitations

These are conditional finite exclusions, not a solution of the full optimization problem. Claimed finite certificates remain subject to independent verification.

## Reproduce

From the shared checkpoint, run `python run_checkpoint_20261026.py --only deletion`. It reconstructs archived assets in a temporary copy and may take substantial time.

The research used AI assistance in development and internal checking. The author is responsible for the claims. Prior work and detailed assumptions are cited in the underlying documents.

[Supplementary source packages](archive/source-packages/) preserve additional proofs, certificates and historical work.
