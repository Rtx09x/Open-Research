# Rational moment export and two universal endpoint kernels

## Exact independent replay
`check_rational_moment_export.py` uses only Python's standard library and exact Gaussian-rational sparse matrices. It imports no worker code. It reconstructs the spin9 generators in the monomial basis, verifies the weighted adjoint for metric diag(1/binom(18,w)), checks su(2) and Casimir90, rebuilds all36 rank0–5 harmonic basis matrices, verifies orthogonality/norms, and checks all324 exported product expansions. All passed in0.92seconds. The source certificate SHA256 and explicit endpoint kernel bases are in `rational_moment_export_checks.json`.

B0=I rather than I/sqrt19 is a harmless invertible error-basis change; set ℓ(I)=I2 accordingly. Low ranks1–4 carry24 real scalar moments and rank5 carries11 arbitrary Hermitian2×2 moments (44 real). Neither reality nor parity of the code is assumed.

With M=I_spin⊗(G⊗I_logical)>0 and H=Ttilde, T is congruence-normalized H and Tbar=M^−1 H is similar to T. S=T(19I−T)≥0 is equivalent to the two linear endpoint LMIs H≥0 and19M−H≥0. Alternatively use the Hermitian quadratic form19H−HM^−1H≥0, not a Loewner inequality on non-Hermitian Tbar.

## Creation-side counterpart of the annihilation factor
For V18→V17, annihilation gives

    T=[bW,aW]†[bW,aW].

For V18→V19, creation gives aa†=10I+Jz, bb†=10I−Jz, ab†=J_− and ba†=J_+. Hence

    19I−T=[a†W,−b†W]†[a†W,−b†W].

Each list of18 operators (two spinor components times9 degree≤2 errors) spans precisely12 rectangular operators: irreducible ranks1/2,3/2,5/2 have dimensions2+4+6. Therefore each has six coefficient syzygies, becoming12 after the logical doubling. This is independent of the moment values.

The independent checker constructs both syzygy spaces from exact derivative/multiplication matrices; sector-wide normalization factors do not alter their kernels. It checks rank12 for each list, six independent syzygies per endpoint, and combined coefficient-kernel rank12. It further checks all36 cross-kernel orthogonality identities as exact19×19 physical operator equations.

## Common nontrivial block has dimension12
Let U,V denote the logically doubled endpoint kernel matrices. Then

    HU=0, (19M−H)V=0, U†MV=0.

The last identity also follows by subtracting U†HV=0 from19U†MV. G>0 makes U,V disjoint and their M-Gram matrices invertible. Their M-orthogonal projectors are

    P0=U(U†MU)^−1U†M,
    P19=V(V†MV)^−1V†M.

The complement P=I−P0−P19 has rank12. Tbar acts as0 on U,19 on V, and preserves this complement. Thus the36-dimensional spectral problem reduces to one12-dimensional nontrivial block, in addition to12 automatic zeros and12 automatic nineteens. Its complement metric depends only on the24 low scalar moments; all rank5 logical moments enter the remaining block.

For a genuine code, this block's spectrum is

    0 (six times),19 (four times),10±|gamma|,

with the coherent endpoint multiplicity merging as usual. Its trace is96. The full orientation polynomial still uses the original physical spinor factors; do not silently replace the inserted Pauli matrices by arbitrary12×12 matrices without transporting their action through the projections.

This is an exact matrix-size reduction and algebraic audit, not an infeasibility proof. The68 variables equal the real Grassmann dimension of a complex2-plane in19 dimensions; the reformulation alone is not a parameter-count breakthrough.
