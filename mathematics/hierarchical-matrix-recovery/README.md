# Hierarchical matrix recovery

## Question

Can a useful hierarchical semiseparable approximation be recovered from a small number of matrix-vector products?

## Results and scope

The project develops matrix-vector-product recovery guarantees for hierarchical semiseparable approximations under explicitly prescribed nested bases.

- **Uniformly mixing rank-$k$ bases:** with $6k$ total forward and transpose products, the stated reconstruction achieves expected squared Frobenius error at most $5+16\delta^{-4}+32\delta^{-8}$ times the best approximation in the prescribed class. The factor is independent of hierarchy depth and assumes the stated uniform transfer singular-value bounds.
- **Scalar prescribed bases:** the checkpoint also records a depth-independent factor **801** with six products under its stated scalar assumptions.
- **Earlier fixed-basis result:** a separate theorem uses $4k$ total products and gives an expected squared-error factor $20L+3$ for hierarchy depth $L$, under the prescribed-basis model.

The checkpoint's 12 HSS checks passed in the release replay. These are fixed-basis results: the general problem of learning arbitrary unknown nested directions and achieving the full RE-02 target remains open.

## Materials

[Uniform-mixing theorem](../../research-checkpoints/2026-10-26/hss-probe-reuse/checkpoints/2026-10-26-scalar-mixing/uniformly_mixing_fixed_basis_bound.md) · [Track](../../research-checkpoints/2026-10-26/hss-probe-reuse/)

## Verification and limitations

The fixed-basis hypotheses matter: the result does not learn arbitrary unknown bases or solve the unrestricted RE-02 problem. Internal checks do not establish independent peer review.

## Reproduce

From the shared checkpoint, run `python run_checkpoint_20261026.py --only hss`.

The research used AI assistance in development and internal checking. The author is responsible for the claims. Prior work and detailed assumptions are cited in the underlying documents.

[Supplementary source packages](archive/source-packages/) preserve additional proofs, certificates and historical work.
