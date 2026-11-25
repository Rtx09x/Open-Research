# Internally verified three-error bracket:35≤n_min(3)≤37

Here n_min(3) is the least n admitting a two-dimensional **complex** code contained in Sym^n(C²) that corrects every error acting on at most three physical qubits. The all-t formula3t²+3t+1 remains open. In particular this package does not claim minimum37.

## Lower bound35

- n≤12: a distance7 code corrects erasure of any six subsystems. If n≤12, partition the physical qubits into two sets of size at most six. Each complementary set would recover the logical qubit, contradicting no-cloning. Equivalently use the quantum Singleton bound.
- Every n13,…,32: `scalar_exact_t3.json` supplies exact rational Farkas identities in established intrinsic/shadow enumerator constraints. The advisor independently rebuilt their coefficients by terminating rational4F3 and replayed every identity.
- n33: `general_dual_n33_t3.json` supplies a finite, full-spin three-copy Z/PPT/lifted-KL witness. `check_general_dual.py 33 3` computes exact rational Gram PSD factors and outward-rounded Arb enclosures of factorial-Racah coefficients. The exact affine constant is−169973/6250000000 and the residual budget is289/100000000, giving strictupper−303821/12500000000<0. All complex symmetric rank-two codes satisfy the constraints; taking real parts is a relaxation, not a restriction to real codewords. The advisor independently reconstructed the coefficients through exact SymPy6j→Arb and separately checked all516 used low-rank eigenvectors with local-Casimir residual bounds. Terminal audit PASS.

- n34: `general_dual_n34_t3.json`, full SHA25604ca5f383f77f8168d3989cb2b67a13ae51a82648518ec75d0f6407c1fb392ba, supplies a second certificate in the identical unrestricted three-copy family. The checker `check_general_dual_tight.py 34 3` changes only the uniform residual tolerance from10^−8 to10^−9 compared with the n33 checker. Exact constant−2785623/2000000000000 plus exact budget119/400000000 gives strictupper−2190623/2000000000000<0. The independent advisor's exact SymPy6j→Arb full-space audit PASS includes535 separately checked local-Casimir KL eigenvectors. Integer-spin applicability is the same previously audited model; there are no new constraints or ansatz assumptions.

## Upper bound37

Let q0=1 and let(q1,…,q18) be the unique root in the rational box defined by `code37_root_certificate.json`. Its eighteen quadratic equations, rational center, radius10^−50, exact inverse-Jacobian residual and Hessian bound certify existence by contraction; no floating residual is used as proof. Define

    |0_L> proportional to Σ_(i=0)^18 sqrt(C(37,2i)) q_i |D_(2i)^37>,
    |1_L> = reversed Dicke amplitudes of |0_L>.

Their supports have opposite parity, and their common nonzero norm is finite. Every one of the98 six-qubit reduced-Gram KL polynomials is an exact linear combination of the defining quadratics, recorded in `code37_kl_reduction.json`. Thus this rank-two symmetric code detects all products of two weight≤3 errors and corrects all three-qubit errors. The advisor's independent stdlib Fraction/AST replay verifies the root certificate and all98 identities.

## Scope and antecedents

Numerical37 candidates predate this calculation: Visnevskyi's2025 thesis and Bond et al arXiv2603.10981v1 must be acknowledged. AAB arXiv2310.05358v3 supplies the sufficient parity/reversal construction framework and a general explicit upper bound4t²+2t+1. Okada arXiv2502.14165v1 supplies the scalar intrinsic LP antecedent. Projector/marginal/PPT hierarchies have earlier antecedents including Yu et al2021/2022. The present claims are computer-assisted and internally independently checked, not externally reviewed or accepted. Priority remains unconfirmed.

The remaining open lengths for the three-error minimum are35 and36. No n35/n36 numerical SDP output is used in this proof.
