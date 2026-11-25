# Local verified restricted HSS supplement — 26 October 2026, 02:33 UTC

## Claims and scope

1. `uniformly_mixing_fixed_basis_bound.md`: REAL arbitrary rank k, nested bases prescribed BEFORE both query banks, all child transfer singular values in [delta,sqrt(1-delta^2)]. Exactly 3k forward plus 3k transpose products. Expected squared Frobenius error at most (5+16 delta^-4+32 delta^-8) times the FIXED LINEAR CLASS optimum squared. Constant is independent of k and depth, but diverges as delta tends to zero. Both Haar and explicitly gauged full-complement signed-permutation laws are covered. This permits interlevel channel mixing; it excludes general nearly coordinate transfers uniformly.
2. `complex_scalar_fixed_basis_corollary.md`: arbitrary prescribed COMPLEX SCALAR nested bases, exactly three complex A plus three complex A* products, factor 801 relative to the fixed class. An elementary phase-gauge consequence of the independently audited real scalar theorem, included with its proof dependencies.
3. `scalar_re02_training_reduction.md`: an oracle composition statement ONLY. An independent constant-query learner with ordinary O(L) fixed-class projection quality would finish the scalar target after six new coefficient products. Such a learner is not provided.

All proofs are exact-arithmetic restricted research arguments. Independent advisor analytic audits and exact finite controls are included, separately labeled. This is not a formal verification, peer review, priority/novelty certification, finite-precision theorem, unknown-basis learner, or solution of unrestricted RE-02. The earlier scalar checkpoint files are copied unchanged as proof dependencies. The source fourth-moment lemma is a separate narrower result; the uniformly mixing reconstruction proof uses only second moments and does not need its fourth-moment assumptions.

## Explicit class and decoder

Definitions are in `fixed_basis_bound.md`, section "Explicit class, probes, and decoder". At each fine level U,V are block diagonal with 2k-by-k orthonormal blocks. The class is U H_coarse V^T + diag(D_i), with U_i^T D_i V_i=0 and arbitrary 2k-by-2k root. These coefficient subspaces are Frobenius-orthogonal. For the new theorem replace the square probes by the explicit width-3k full-completion law in its statement. Local tests remain row-orthonormal, hence local pseudoinverses are transposes; coefficient formulas and subtractive carry are unchanged. Root decoding is Y_root Omega_root^T. `test_uniform_mixing_fixed_basis.py` implements and counts actual physical matvec calls.

## Replay in a writable COPY

The frozen files are read-only. Copy this directory elsewhere within the authorized cloud workspace before executing tests, which write JSON results. No network or external service is needed.

Stdlib Python exact control (about two seconds on one CPU):

    python verify_uniform_mixing_two_step_exact.py

It checks k=2 noncommuting rational transfers, both one-bank-conditioned directions, 1024 exact orientation pairs per direction, physical decoder identities, flux and emission, and the two-step lower bound. It is corroboration, not proof for all ranks/depths. Advisor independently audited the analytic proof and replayed this worker code; the replay is not represented as independently written code.

Additional original scalar exact controls (stdlib, seconds):

    python verify_branch_doob_exact.py
    python verify_one_bank_output_signs_exact.py
    python verify_correlated_sector_signs_exact.py
    python verify_anchor_inverse_identity_exact.py

Numerical implementation controls (NumPy and SciPy; constrain BLAS to one thread):

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python test_uniform_mixing_fixed_basis.py
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python test_complex_scalar_gauge.py

Empirical risk factors are NOT used to prove the theorem. Hashes are in SHA256SUMS and manifest.json. Advisor dependency hashes bind the current proof and audits; relative original paths in audit prose are historical provenance, not runtime dependencies.

## Operational provenance

This is a LOCAL-ONLY immutable checkpoint. Repository integration and upload are on hold after earlier packaging denials. No git/push, uploader, public publication, paid compute, Pro call, or user-computer action is performed by this checkpoint. A separate accepted Extra High consultation about scalar unknown-basis learning is still pending and contributes no theorem to this packet.
