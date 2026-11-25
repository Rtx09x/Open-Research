# Exact certificate: carried sketch energy need not decrease monotonically

**Classification:** exact counterexample to one proposed proof shortcut. Not a counterexample to RE-02, the fixed-basis error bound, or the surviving uniform-energy conjecture.

Use the independently fixed-basis orthonormal-frame coefficient decoder from `fixed_basis_unbiasedness.md`, with k=1,L=3,N=16. Set all finest leaf bases U_i=V_i=(1,0)ᵀ. In zero-based physical coordinates, let the only nonzero entries of A be

    A[2,1]=−917/1000, A[4,1]=393/1000, A[6,1]=13/200.

Thus A is rank1 and has squared Frobenius norm999563/1000000. It is orthogonal to the prescribed fixed-basis class because its sole nonzero column is a leaf-detail direction and all its nonzero rows lie outside that leaf. This does not say its full HSS optimum is positive; indeed its full HSS optimum is0.

For each remaining k1 transfer vector use

    u(t)=((1−t²)/(1+t²), 2t/(1+t²))ᵀ,

with complement (−u₂,u₁)ᵀ. The half-angle parameters are:

| Level, finest remaining first | Row U parameters | Column V parameters |
|---|---|---|
| Four local blocks | −15/13, −73/6, −30/13, −54/17 |21/20, −25/14, −16/15,59/6 |
| Two local blocks |41/20,92/19 |93/14,31/4 |

Start both root frames at I₂ and use independent uniform complement signs at all nodes and in both query families.

Let S be the sum of squared norms of the carried forward and transpose product arrays. The finest signs can be integrated analytically. In active/detail coordinates the input is a single offdiagonal ad column, with coefficient vector

    a=(0,−917/1000,393/1000,13/200,0,0,0,0)ᵀ.

Conditional on the coarser frames F,P, its carried data is one degree-one Walsh channel:

    Y=(a−e₀ b)g₀,   Z=0,
    b=P₀Pᵀa,       g₀=(−F₀,₂,F₀,₁).

The omitted finest sign multiplies this whole channel by±1 and therefore does not change any squared-energy difference. All other finest signs disappear. There remain12 independent coarse signs, hence4096 equally likely cases.

Exact rational evaluation gives the following expected change at the **last** nonroot compression step:

    E[S_after−S_before]
    =1332320221605268852341561872186637436659319
      /10388101485192678619556757712323030625000000
    >0.

The decimal is approximately0.128254447985936, but positivity is certified by the integer numerator, not by that decimal.

## Independent reproduction
`rational_potential_counterexample.py` is the discovery/certification implementation. `verify_rational_potential.py` independently reconstructs every rational frame and performs the carried recurrence using only Python lists and `fractions.Fraction`, with no NumPy, SciPy, random draws, or floating-point matrix arithmetic. It reads the explicit parameters in `rational_potential_certificate.json`, checks all4096 cases, and verifies exact equality with the displayed fraction. The independent run completed successfully; see `independent_rational_verification.log`.

This kills the assertion that expected carried energy must decrease at every level. It does **not** kill a uniform upper bound relative to the original input energy: observed energy can decrease and later partially return. That weaker global bound remains open in this work.
