# Rational spectral upper certificate — infrastructure control only

The matrix certificate proves the bound **321.12**, hence only the integer bound 321. This is weaker than the published 320 and is not claimed as a new frontier result.

## Exact mathematical matrix

`evidence/spectral_rational_n12.npz` specifies an exact rational symmetric matrix M: diagonal entries 1; every nonedge entry 1; each listed conflict edge {i,j} has entry 1−w_ij, where w_ij is an integer divided by 10^6. The verifier reconstructs deletion sets from strings and checks **every** modified edge actually joins two deletion-confusable words. It assumes no symmetry of a code.

If C is any valid code, its normalized indicator v satisfies vᵀMv=|C|, since every matrix entry within C is 1. Thus |C|≤λ_max(M). It is enough to certify H=(32112/100)I−M positive semidefinite.

## A posteriori check, not trust in Cholesky success

The verifier computes floating matrices L and R as approximate Cholesky factor and inverse. These outputs are then treated as exact binary-valued matrices; their construction algorithms need not be mathematically trusted. The checks use conservative classical IEEE-754 dot-product error bounds and outward-rounded scalar bounds.

Let γ_k = kε/(1−kε), using ε=2^−52 (twice the usual unit roundoff, deliberately conservative). Positive row/column sums are bounded upward using γ_n. Matrix-product errors are bounded by γ_(2n), accounting for at most n products and n additions in each classical dot product. Scalar endpoints are rounded outward with `nextafter`.

The code checks finite magnitudes and nonzero entry ranges, excludes overflow/underflow in the verification products, and explicitly bounds rational-to-binary input conversion. It assumes standard IEEE-754 arithmetic and a classical BLAS dot-product error model; it is **not a formal proof-assistant kernel**. Strassen-like multiplication or a nonconforming BLAS would require a different operation bound.

For p=1,∞, establish rigorous upper bounds η_p≥||I−RL||_p<1. Then

    ||L⁻¹||_p ≤ ||R||_p / (1−η_p),

because L⁻¹=(RL)⁻¹R. Hence

    σ_min(L)^2 ≥ 1 / (upper(||L⁻¹||_1) · upper(||L⁻¹||_∞)).

Separately bound ||H−LLᵀ||_∞, including input conversion and product/subtraction rounding. The exact residual is symmetric, so its spectral norm is at most its infinity norm. A strict positive difference between the preceding lower and upper bounds proves H positive definite.

## Recorded margins

- Inverse residual bounds: η_1 ≤ 7.20×10^−8; η_∞ ≤ 3.12×10^−7.
- σ_min(L)^2 lower bound: 3.7503×10^−5.
- Factorization-residual norm upper bound: 4.6263×10^−7.
- Certified positive-definiteness margin: greater than 3.7040×10^−5.

See the JSON for full digits. The resulting certificate is comfortably positive, rather than relying on a nearly canceled eigenvalue sign.

## Replay

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python scripts/certify_spectral.py --verify-only
```

Observed runtime 7.4 seconds and peak RSS about 620 MiB. The rational edge list is the durable candidate; dense L/R need not be stored because the verifier regenerates and checks them a posteriori. An independent dense 4,096-dimensional eigenvalue calculation also matches the symmetry-block numerical search, but that agreement alone is not the proof.
