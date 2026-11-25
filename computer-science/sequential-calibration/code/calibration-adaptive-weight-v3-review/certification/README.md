# Independent verification package

## Result

The adaptive continuation-weight construction in `../theory/ADAPTIVE_Q_THEOREM.md` passed an independent analytic audit and two full-domain arithmetic certificates. Its SPR exponents are `51/5000` and `379/400`; the published transfer theorem gives calibration exponent `20423/30846` (about `0.66209557155`). Read `INDEPENDENT_AUDIT.md` for precise scope. This is internal verification, not external review, comprehensive novelty clearance, an efficient forecaster, or resolution of the matching-rate problem.

## Main artifacts

| Artifact | Verification scope |
|---|---|
| `INDEPENDENT_AUDIT.md` | Legal recursive strategy, full induction and transfer hypotheses |
| `certify_adaptive_bias.py` | 60-digit `mpmath.iv` proof over an exact covering partition |
| `results/adaptive_bias_certificate.json` | 4,988 covering cells, scalar witnesses and interval margins |
| `replay_rational_certificate.py` | Independent standard-library dyadic/rational-power replay |
| `results/rational_replay.json` | All cells passed; 29,972 exact integer root endpoints; 27.10 seconds, 24 MiB |
| `check_rational_policy.py` | Direct whole-cell checks of all inequalities for compiled rational q |
| `results/rational_policy_check.json` | 4,988 closed cells and 14,964 lookup tests passed; 52.73 seconds |
| `check_runtime_lookup.py` | Actual runtime factor function checked at every endpoint and midpoint |
| `results/runtime_lookup_check.json` | 14,964 exact comparisons passed |

The rational-power backend uses 80-bit dyadic endpoints. Floating point supplies only an initial guess for integer root iteration; every returned root is validated by exact integer inequalities. No third-party numerical library is used in either standard-library replay.

## Replay the existing certificate and policy

First check the release manifest. Work in a disposable copy preserving sibling `theory/` and `certification/` directories, because scripts write result JSON files:

```sh
python certification/replay_rational_certificate.py
python certification/check_rational_policy.py
python certification/check_runtime_lookup.py
python theory/adaptive_policy.py
```

The first three use only Python's standard library. The last runs bounded operational tests, not the uniform theorem proof. Runtime varies by machine; measurements above are this run's observed wall times and peak resident memory.

To regenerate rather than replay the outward certificate, use Python with `mpmath==1.3.0`, then regenerate the dependent rational table because its source-certificate hash changes:

```sh
python certification/certify_adaptive_bias.py
python certification/replay_rational_certificate.py
python theory/compile_rational_policy.py
python certification/check_rational_policy.py
python certification/check_runtime_lookup.py
```

## Finite-game controls (not asymptotic evidence)

`solve_masks.py` independently solves every signed board for `n=1..8`, horizons `0..16`, with disjoint bitmasks. It enumerates ALL legal deletion subsets, pointer stopping, reused emptied cells and full-board termination without symmetry pruning. `check_tables.py` uses literal tuples and combinations, checks every Bellman equation, and compares to the lead's independent ternary solver files in `../theory/exact/`.

- 167,280 independent values agree.
- 157,440 Bellman equations and 5,359,392 response evaluations pass.
- At `n=8`, the solver took 0.380 seconds; peak process RSS was 25,488 KiB.
- The independent tuple checker took 0.963 seconds total.
- A minimal dropped-stop counterexample is `--.` with one remaining round: the correct value is two, forced continuation gives one.
- Sign reversal or reflection alone are not symmetries: with two cells and one remaining round, `+.` has value two whereas `-.` and `.+` have value one. The combined reflection/sign reversal is a legal game-tree isomorphism.
- Signed-subboard monotonicity proves all-deletion dominance uniformly; the full-subset solver was implemented before using that lemma. Fixed-point tables extend the finite-n values to later horizons, not to larger n.

`verify_published_parameters.py` separately reproduces the published fixed-bias Appendix A numerical obligations. It is a source control, not the new result or a full independent proof of that paper.

## Integrity

`MANIFEST.json` records hashes and sizes of this verification package and hashes of its audited sibling inputs. Reports contain their own input/script hashes. The immutable release archive maintained by the lead snapshots both sibling directories. Avoid confusing later regenerated timing-bearing JSON with the frozen checked inputs.
