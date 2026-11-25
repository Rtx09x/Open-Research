# Symmetric quantum error correction

## Question

How few physical qubits can support a two-dimensional quantum code entirely within the permutation-symmetric subspace, correcting up to t arbitrary physical-qubit errors?

## Results and scope

The October checkpoint reports an internally checked computer-assisted exclusion at n=18 for t=2 and a known construction at n=19. For t=3 it reports 35 ≤ n ≤ 37; the exact minimum and the proposed general formula remain open. These statements are restricted to the specified symmetric-subspace model.

## Materials

[Project checkpoint](../../research-checkpoints/2026-10-26/symmetric-quantum-codes/) · [Independent verifier materials](../../research-checkpoints/2026-10-26/quantum-independent-audit/) · [General bound and assumptions](../../research-checkpoints/2026-10-26/symmetric-quantum-codes/checkpoints/2026-10-26-all-t-volume/THEOREM.md)

## Verification and limitations

The proof and computer-assisted certificates have internal audits. Independent human review, novelty and priority are not established; the general minimum formula is not proved.

## Reproduce

From the shared checkpoint, run `python run_checkpoint_20261026.py --only quantum`; follow the quantum track for other certificates and dependency requirements.

The research used AI assistance in development and internal checking. The author is responsible for the claims. Prior work and detailed assumptions are cited in the underlying documents.

[Supplementary source packages](archive/source-packages/) preserve additional proofs, certificates and historical work.
