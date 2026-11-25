# Sequential calibration

**Preprint · November 2026** — [Read the PDF](preprint/adaptive_weight_sequential_calibration.pdf) · [LaTeX source](preprint/adaptive_weight_sequential_calibration.tex) · [Build instructions](preprint/BUILD.md)


## Question

What expected calibration error can be guaranteed in the classical adversarial binary forecasting setting?

## Results and scope

The v3 adaptive-weight package presents an internally checked **candidate asymptotic calibration bound**

$$
\mathbb{E}[\mathrm{CalErr}(T)]=O\!\left(T^{20423/30846}\right)
=O\!\left(T^{0.6620955715489852\ldots}\right).
$$

The mechanism adapts continuation weights to observed count ratios in the sign-preservation-with-reuse game, then invokes the stated transfer to classical marginal calibration. The exponent improves on the **inspected historical printed comparator** of 0.662942288; that comparison is not a claim about the current literature frontier.

The exact-arithmetic replay checked **4,988 cells** covering the stated trigger domain; the package also reports 167,280 finite state/horizon controls. A real gap in the earlier v2 induction was identified, with a 19-round counterexample. The v3 package documents a stronger deletion-augmented induction and the erratum. Those numerical checks are evidence for the numerical obligations, not a substitute for independent scrutiny of the repaired analytic argument.

## Materials

[Start here](code/calibration-adaptive-weight-v3-review/START_HERE.md) · [Theorem](code/calibration-adaptive-weight-v3-review/theory/ADAPTIVE_Q_THEOREM.md) · [Erratum](code/calibration-adaptive-weight-v3-review/theory/ERRATUM_v2_to_v3.md)

## Verification and limitations

The v3 argument and arithmetic were internally checked, but the analytic repair requires independent scrutiny. The result has enormous constants and is not a practical finite-horizon performance guarantee or a proof of an optimal exponent.

## Reproduce

From `code/calibration-adaptive-weight-v3-review`, run `python verify_manifest.py`; the start guide lists exact-arithmetic replays and their scope.

The research used AI assistance in development and internal checking. The author is responsible for the claims. Prior work and detailed assumptions are cited in the underlying documents.
