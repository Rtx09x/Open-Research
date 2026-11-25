# Symmetric quantum error correction

## Question

How few physical qubits can support a two-dimensional quantum code entirely within the permutation-symmetric subspace, correcting up to t arbitrary physical-qubit errors?

## Results and scope

The work studies two-dimensional complex codes **inside the fully symmetric $n$-qubit subspace**, correcting arbitrary errors on at most $t$ physical qubits. Its strongest internally checked results include:

- **Two-error minimum:** $n_{\min}(2)=19$ in this model. The central new exclusion is a computer-assisted certificate ruling out $n=18$; the 19-qubit construction was already known. The full minimum also uses shorter-length exclusions and the known construction, as documented in the proof package.
- **Three errors:** $35\leq n_{\min}(3)\leq37$, combining certificates excluding 33 and 34 with an exact existence certificate at 37. Whether 35 or 36 works remains open.
- **General lower bound:** for rank-two codes and $t\geq2$, the archived volume theorem and equality exclusion yield $n\geq2t^2+4t+2$. The proposed exact formula $3t^2+3t+1$ remains a conjecture.
- **Explicit higher-radius constructions:** the checkpoint also supplies a phase-twisted construction with $n=4t^2+2t$ for $t\geq10$, under the stated construction hypotheses.

These are scoped results, not bounds for arbitrary quantum codes outside the symmetric subspace. The independent internal arithmetic verifier for the 18-qubit certificate passed a fresh 256-bit interval replay; the general-bound checkpoint replay also passed. The analytic applicability argument and priority still need independent expert scrutiny.

## Materials

[Two-error theorem and proof](../../research-checkpoints/2026-10-26/symmetric-quantum-codes/phase2/theorem_and_necessity.md) · [Three-error bracket](../../research-checkpoints/2026-10-26/symmetric-quantum-codes/phase3/t3_verified_bracket.md) · [Independent verifier materials](../../research-checkpoints/2026-10-26/quantum-independent-audit/) · [General bound and assumptions](../../research-checkpoints/2026-10-26/symmetric-quantum-codes/checkpoints/2026-10-26-all-t-volume/THEOREM.md)

## Verification and limitations

The proof and computer-assisted certificates have internal audits. Independent human review, novelty and priority are not established; the general minimum formula is not proved.

## Reproduce

From the shared checkpoint, run `python run_checkpoint_20261026.py --only quantum`; follow the quantum track for other certificates and dependency requirements.

The research used AI assistance in development and internal checking. The author is responsible for the claims. Prior work and detailed assumptions are cited in the underlying documents.

[Supplementary source packages](archive/source-packages/) preserve additional proofs, certificates and historical work.
