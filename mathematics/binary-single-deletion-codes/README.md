# Binary single-deletion codes

## Question

What is the maximum size of a binary length-12 code correcting a single deletion?

## Results and scope

The research combines exhaustive local analysis, structural necessities and exact certificates for binary length-12 single-deletion codes:

- **Radius-nine barrier:** every distinct valid code of size at least 316 removes at least **10** words from the reference $VT_0(12)$ code. Two implementations enumerate **2,733,456 connected supports** through radius nine with matching support hashes.
- **Checksum structure:** every code of size at least 317 requires at least seven checksum classes, under the stated checksum definition.
- **Size-320 exclusions:** exact certificates exclude normalized root words 5 and 11 in two of 13 receiver-root cases, under the stated normalization. The archived root-case replay passed in the release run.

The global interval remains **316–320**. These local and conditional results are substantial constraints on possible improvements, but they neither construct a 317-word code nor establish a global upper bound of 319.

## Materials

[Root-case exclusions](../../research-checkpoints/2026-10-26/deletion-code-optimality/checkpoints/root-exclusions-2026-10-26/README.md) · [Track](../../research-checkpoints/2026-10-26/deletion-code-optimality/)

## Verification and limitations

These are conditional finite exclusions, not a solution of the full optimization problem. The released certificates have passed internal replay and remain subject to independent expert verification.

## Reproduce

From the shared checkpoint, run `python run_checkpoint_20261026.py --only deletion`. It reconstructs archived assets in a temporary copy and may take substantial time.

The research used AI assistance in development and internal checking. The author is responsible for the claims. Prior work and detailed assumptions are cited in the underlying documents.

[Supplementary source packages](archive/source-packages/) preserve additional proofs, certificates and historical work.
