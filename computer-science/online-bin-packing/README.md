# Deterministic online bin packing

## Question

What performance can a specified deterministic online bin-packing algorithm guarantee against an optimal offline packing?

## Results and scope

The October checkpoint reports an algorithm-specific asymptotic ratio bracket 1.5782054112079646… ≤ R ≤ 1.5782055179987482…. The lower endpoint concerns a particular algorithm and input construction, not a universal lower bound for all online algorithms.

## Materials

[Current checkpoint handoff](../../research-checkpoints/2026-10-26/online-bin-packing/phase7/HANDOFF.md) · [Track](../../research-checkpoints/2026-10-26/online-bin-packing/)

## Verification and limitations

Internally checked; external proof review and publication priority remain open. No solution of the classic universal gap is claimed.

## Reproduce

From the shared checkpoint, run `python run_checkpoint_20261026.py --only packing`; the handoff identifies the proof dependencies.

The research used AI assistance in development and internal checking. The author is responsible for the claims. Prior work and detailed assumptions are cited in the underlying documents.

[Supplementary source packages](archive/source-packages/) preserve additional proofs, certificates and historical work.
