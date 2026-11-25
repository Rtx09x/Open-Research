# Seven-cycle Shannon capacity

**Preprint · November 2026** — [Read the PDF](preprint/seven_cycle_shannon_capacity_obstructions.pdf) · [LaTeX source](preprint/seven_cycle_shannon_capacity_obstructions.tex) · [Build instructions](preprint/BUILD.md)


## Question

How large can zero-error codes become for the seven-cycle confusability graph?

## Results and scope

The project investigates finite constructions and structural barriers for zero-error communication on the seven-cycle graph.

- **Finite-subgroup obstruction:** every finite subgroup or translate in $(\mathbb{R}/\mathbb{Z})^5$ with circular coordinate-max distance at least $2/7$ has at most **367 points**. The proof's cyclic and noncyclic subgroup checks were replayed in the release suite.
- **Physical-code and architecture gates:** the checkpoint records explicit finite code constructions, clique-cover certificates, and exclusions for particular fiber and reservoir constructions. For example, a specified fixed-fiber architecture has at most 135,060 words against its 135,093 target.
- **Reproducible evidence:** all 12 selected C7 checkpoint checks passed, with source, certificates and the upstream licence and notice retained.

These gates constrain the specified alphabets and construction families. They do **not** upper-bound arbitrary $C_7$ codes or resolve the unrestricted Shannon capacity, and the checkpoint does not claim a new overall capacity lower bound.

## Materials

[Finite-subgroup checkpoint](../../research-checkpoints/2026-10-26/seven-cycle-capacity/checkpoints/checkpoint_finite_subgroup_gate_20261026/README.md) · [Track](../../research-checkpoints/2026-10-26/seven-cycle-capacity/)

## Verification and limitations

The unrestricted Shannon capacity remains open; the checkpoint does not establish a new overall capacity bound. Third-party material retains the included upstream licence and notice.

## Reproduce

From the shared checkpoint, run `python run_checkpoint_20261026.py --only c7`.

The research used AI assistance in development and internal checking. The author is responsible for the claims. Prior work and detailed assumptions are cited in the underlying documents.

[Supplementary source packages](archive/source-packages/) preserve additional proofs, certificates and historical work.
