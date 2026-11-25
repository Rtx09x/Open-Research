# Hierarchical matrix recovery

## Question

Can a useful hierarchical semiseparable approximation be recovered from a small number of matrix-vector products?

## Results and scope

The October checkpoint reports a depth-independent expected-error bound for prescribed real nested bases satisfying a uniform-mixing condition, with 6k total products. The factor depends on the mixing parameter.

## Materials

[Uniform-mixing theorem](../../research-checkpoints/2026-10-26/hss-probe-reuse/checkpoints/2026-10-26-scalar-mixing/uniformly_mixing_fixed_basis_bound.md) · [Track](../../research-checkpoints/2026-10-26/hss-probe-reuse/)

## Verification and limitations

The fixed-basis hypotheses matter: the result does not learn arbitrary unknown bases or solve the unrestricted RE-02 problem. Internal checks do not establish independent peer review.

## Reproduce

From the shared checkpoint, run `python run_checkpoint_20261026.py --only hss`.

The research used AI assistance in development and internal checking. The author is responsible for the claims. Prior work and detailed assumptions are cited in the underlying documents.

[Supplementary source packages](archive/source-packages/) preserve additional proofs, certificates and historical work.
