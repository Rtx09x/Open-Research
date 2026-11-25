# Sequential calibration

## Question

What expected calibration error can be guaranteed in the classical adversarial binary forecasting setting?

## Results and scope

The v3 adaptive-weight package presents a candidate bound O(T^(20423/30846)) using the stated sign-preservation-with-reuse transfer. Version 2 had a documented gap; v3 gives a proposed stronger induction and retains the counterexample and erratum.

## Materials

[Start here](code/calibration-adaptive-weight-v3-review/START_HERE.md) · [Theorem](code/calibration-adaptive-weight-v3-review/theory/ADAPTIVE_Q_THEOREM.md) · [Erratum](code/calibration-adaptive-weight-v3-review/theory/ERRATUM_v2_to_v3.md)

## Verification and limitations

The v3 argument and arithmetic were internally checked, but the analytic repair requires independent scrutiny. The result has enormous constants and is not a practical finite-horizon performance guarantee or a proof of an optimal exponent.

## Reproduce

From `code/calibration-adaptive-weight-v3-review`, run `python verify_manifest.py`; the start guide lists exact-arithmetic replays and their scope.

The research used AI assistance in development and internal checking. The author is responsible for the claims. Prior work and detailed assumptions are cited in the underlying documents.
