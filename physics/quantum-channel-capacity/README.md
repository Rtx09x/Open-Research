# Quantum channel capacity

## Question

Can quantum information be transmitted at positive rate for the stated qubit depolarizing-channel noise level?

## Results and scope

The archived research includes an exact obstruction for a specified stabilizer-shield architecture and a separate squeezed-obstruction checker. It does not establish positive quantum capacity at p = 0.205, where p denotes total nonidentity Pauli error probability.

## Materials

[Stabilizer-shield obstruction](paper/stabilizer_shield_obstruction_205.md) · [Checkers](code/)

## Verification and limitations

Architecture-specific negative results do not bound arbitrary quantum codes; private-information calculations do not by themselves prove a quantum-capacity result. Independent review is outstanding.

## Reproduce

From `code/`, run `python shield_stabilizer_obstruction_checker.py` and `python verify_squeezed_obstruction_stdlib.py` with assertions enabled. Consult the proof note for hypotheses.

The research used AI assistance in development and internal checking. The author is responsible for the claims. Prior work and detailed assumptions are cited in the underlying documents.
