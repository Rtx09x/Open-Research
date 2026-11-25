# Quantum channel capacity

## Question

Can quantum information be transmitted at positive rate for the stated qubit depolarizing-channel noise level?

## Results and scope

For the qubit depolarizing channel with total nonidentity Pauli error probability $p=0.205$, the work develops an exact obstruction to a particular stabilizer-shield route toward quantum communication.

The proof treats full $[[m,2]]$ stabilizer encoding subspaces and **arbitrary CPTP receiver decoders**, including the specified erasure-flag and postselection behavior. It derives a quantitative distance obstruction to the target shield and supplies an additional random-stabilizer result. The accompanying exact checker verifies finite-block inequalities, including the stated $m=4096$ and $m=8192$ cases. A separate checker verifies a squeezed-state obstruction in its own noise setting.

Both standalone checkers passed in the release replay. The result rules out the stated architecture under its hypotheses; it does not establish zero channel capacity or positive quantum capacity at $p=0.205$.

## Materials

[Stabilizer-shield obstruction](paper/stabilizer_shield_obstruction_205.md) · [Checkers](code/)

## Verification and limitations

Architecture-specific negative results do not bound arbitrary quantum codes; private-information calculations do not by themselves prove a quantum-capacity result. Independent review is outstanding.

## Reproduce

From `code/`, run `python shield_stabilizer_obstruction_checker.py` and `python verify_squeezed_obstruction_stdlib.py` with assertions enabled. Consult the proof note for hypotheses.

The research used AI assistance in development and internal checking. The author is responsible for the claims. Prior work and detailed assumptions are cited in the underlying documents.
