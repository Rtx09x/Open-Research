# Calibration research: clarified v3 review package

## What this says

An internally checked adaptive-weight proof gives a candidate worst-case expected classical marginal calibration guarantee

    O(T^(20423/30846)) = O(T^0.6620955715489852...).

This is a modest asymptotic improvement over the inspected printed upper exponent .662942288, not a practical performance promise. The new mechanism varies the continuation-bias magnitude with observed count ratios, rather than merely retuning the published fixed-shift parameters. The clean certificate has an enormous constant/threshold (`F=10^10`). The full optimal calibration rate remains open.

**Important correction:** a hostile AI-assisted review found a real gap in the original proof interface: a legal global history can revisit a child that previously became locally full. The supplied 19-round example reproduces this exactly. Version 3 explicitly proves a stronger deletion-augmented local-trace induction. The algorithm, numerical obligations, policy, constants and exponent are unchanged. This correction is documented, not concealed.

## Reading order

1. `theory/ADAPTIVE_Q_THEOREM.md`: clarified theorem, complete analytic proof and numerical obligations.
2. `theory/ERRATUM_v2_to_v3.md`: original defect, concrete witness and repair.
3. `theory/EXTERNAL_ERASURE_INDUCTION.md`: precise local semantics and recursive projection.
4. `phase2/certification/EXTERNAL_ERASURE_AUDIT.md`: independent audit of that repair.
5. `certification/INDEPENDENT_AUDIT.md`: original algebra/transfer audit, read **with** the repair above; its older surrounding-history wording is not the complete induction interface.
6. `SOURCES.md` and `theory/NOVELTY_AUDIT.md`: primary-source versions and limits of the comparison.

The small `theory/phase2/v3_draft/` duplicate preserves the exact file paths referenced by the signed scientific audit. The canonical reading copy is `theory/ADAPTIVE_Q_THEOREM.md`.

## What is—and is not—verified

The analytic induction, full trigger-domain certificate and exact rational implementation have independent internal checks. Two different arithmetic implementations passed; 4,988 cells cover the entire continuous domain. Finite-game solvers agree on 167,280 state/horizon values, and the local-erasure semantic tests pass. These finite tests are controls, not substitutes for the uniform proof.

This is **not external human peer review, proof-assistant formalization, comprehensive priority clearance, an efficient forecaster, a matching minimax theorem, or evidence of useful finite-horizon speed**. The published SPR-to-calibration transfer theorem is invoked with checked hypotheses, not reproved here. The external AI review did not inspect the original exact-rational table or the native standard-library backend; those checks are internal.

## Verify and replay

Python 3.10 or newer is sufficient for the standard-library replays. First verify the package hashes:

```sh
python verify_manifest.py
```

Then work in a **disposable copy** of the extracted package, since verification scripts write result files:

```sh
python certification/replay_rational_certificate.py
python certification/check_rational_policy.py
python certification/check_runtime_lookup.py
python certification/check_tables.py
python theory/adaptive_policy.py
python theory/check_19_round_interface.py
python phase2/certification/check_augmented_projection.py
python phase2/certification/replay_hostile_transcript.py
```

The exact arithmetic replays take roughly a minute or two on an ordinary CPU in the observed environment; no GPU, network, paid service or external account is needed. `certification/README.md` explains optional certificate regeneration using `mpmath==1.3.0`. Regeneration changes timing-bearing JSON and dependent hashes, so do not confuse a regenerated run with the supplied frozen inputs.

Full downloaded third-party works, browser traces, prompts, account details and routine workflow logs are intentionally omitted. This is a review package, not a public publication or priority registration.
