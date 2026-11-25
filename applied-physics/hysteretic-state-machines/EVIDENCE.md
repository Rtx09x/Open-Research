# Core evidence

All mathematical arguments and complete hypotheses are in `paper/main.tex`. The retained exact checks cover:

| Claim or check | Retained evidence |
|---|---|
| Unary realizability, reset and two-stage merge constructions | `repro/generalizations/src/memory.py`, `check_run.py` |
| Adjacent-layer capacity and decimal interaction-order separation | `repro/original/src/verify.py`, its exact input certificates and capacity witnesses |
| All-period constructions and 1,000 states on 13 switches | `repro/generalizations/src/cycle_operations.py`, `check_run.py`, composition inputs and `build_compositions.py` |
| Interaction-free maps and exact reset support/source-incidence laws | `repro/audit/src/resources.py` |
| Sparse pairwise realizability and structural bounds | `repro/audit/src/sparse.py`, `structural_bounds.py` |
| Seven-state interaction-order/support separation | `repro/audit/src/seven_state_separation.py`, the affine witness and manuscript proof |
| Exact small-map classifications, including minimality of the seven-state separation | `repro/audit/src/verify_stored.py`, `encoding_search.py`, `synthesis.py`, `affine_minima_through6.json`, `unary_seven_extension.json` |
| Global positive span, invalid dynamics and certificate corruption rejection | `repro/audit/src/validate_model.py`, `test_audit.py`, negative-span fixture; other regression suites |

The runner executes generators before checkers that consume their outputs. It does not require the historical ZIP archives or optional numerical solvers. Discovery paths still present in reusable library modules are not invoked by the exact checker.

## Fresh core validation, 23 October 2026

Validation was performed in a disposable copy; the committed input fixtures and original research directory were not overwritten.

- All 15 retained scientific programs passed.
- The manuscript rebuilt successfully to 22 pages with LaTeX/BibTeX and no unresolved references or citations. The saved final PDF was not replaced. The container required temporary format/font-map configuration; a normal configured TeX Live installation can use the supplied build script directly.
- Unit/regression suites passed 9 + 20 + 49 = 78 tests.
- Exact certificate replay verified 690 retained/generated copies representing 688 distinct certified systems.
- All 326 retained finite unary types were reclassified with exhaustive lower-dimensional coverage.
- The explicit 1,000-state counter, cycle compositions, reset/resource constructions, seven-state geometry and nominal decimal reset checks passed.
- The final manuscript PDF, LaTeX source and all copied scientific files match the original reviewed files byte for byte. Only the lean runner and these navigation/evidence documents were newly written.

Counts are specific to this lean fixture set. They need not equal the larger archive's counts because redundant certificates and historical experiments are excluded. Passing finite checks does not establish independent human review, a full proof-assistant formalization, or originality.

## Why the 21 JSON inputs remain

- Original (8): six discovered cycle witnesses, one complete exact decimal lower-bound certificate set, and one nominal-reset regression expectation. These are input evidence, not raw run logs.
- Generalizations (6): four finite-spectrum witness sets and two composition-ingredient sets. The composition, 1,000-counter parameters and event trace are regenerated from these inputs and are not committed.
- Audit (7): two complete finite-classification certificate sets, three rational feasible witnesses, one independently enumerated decimal dual-certificate set, and one deliberately invalid negative-span model. The lean runner checks them without a numerical solver or archive extraction.

Reconstructing discovered witnesses or infeasibility certificates requires a separate search/solver, whereas validating them is exact and dependency-free. Regenerable reports, model outputs, build products and logs are omitted.
