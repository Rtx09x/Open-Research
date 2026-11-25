# Deterministic online bin packing

**Preprint · November 2026** — [Read the PDF](preprint/deterministic_online_bin_packing.pdf) · [LaTeX source](preprint/deterministic_online_bin_packing.tex) · [Build instructions](preprint/BUILD.md)


## Question

What performance can a specified deterministic online bin-packing algorithm guarantee against an optimal offline packing?

## Results and scope

For a specified retuned tiny-Best-Fit Advanced Harmonic algorithm, the checkpoint gives the internally checked asymptotic competitive-ratio bracket

$$
1.5782054112079646\ldots\;\leq R\leq\;1.5782055179987482\ldots
$$

The interval is approximately **$1.068\times10^{-7}$ wide**. The lower endpoint comes from an explicit seven-size rational input family with offline optimum exactly $N$; the upper endpoint uses the stated ordered-suffix analysis and pricing certificates. Together they sharply constrain the possible improvement obtainable from analysis alone for this fixed algorithm. Five packing checkpoint checks passed in the release replay.

The lower bound is **algorithm-specific**, not a universal lower bound for every online packing algorithm, and the endpoints do not prove the exact ratio. The published universal gap remains open.

## Materials

[Current checkpoint handoff](../../research-checkpoints/2026-10-26/online-bin-packing/phase7/HANDOFF.md) · [Track](../../research-checkpoints/2026-10-26/online-bin-packing/)

## Verification and limitations

Internally checked; external proof review and publication priority remain open. No solution of the classic universal gap is claimed.

## Reproduce

From the shared checkpoint, run `python run_checkpoint_20261026.py --only packing`; the handoff identifies the proof dependencies.

The research used AI assistance in development and internal checking. The author is responsible for the claims. Prior work and detailed assumptions are cited in the underlying documents.

[Supplementary source packages](archive/source-packages/) preserve additional proofs, certificates and historical work.
