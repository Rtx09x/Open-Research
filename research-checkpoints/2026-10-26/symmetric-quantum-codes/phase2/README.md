# Phase 2: boundary reductions and a three-copy exclusion certificate

**Current status:** the rigorous interval dual certificate excludes n=18. Two independently implemented arithmetic verifiers, separate unrestricted-complex applicability audits, and the full n≤17 / n=19 chain pass. The selected t=2 minimum-19 target is internally established by a computer-assisted proof; external mathematical review and publication-priority checking remain outstanding. No all-t claim is made.

Start with:
- `theorem_and_necessity.md`: precise minimum-19 theorem statement, full unrestricted necessity proof, and exact primary references.
- `certificate_readme.md`: finite witness, strict rational contradiction, and reproduction.
- `check_interval_dual.py` + `interval_dual_candidate.json`: standalone verifier and234KB witness. Only stdlib and python-flint are needed; no solver/model import.
- `three_copy_relaxation.md`: why each SDP condition is necessary for unrestricted complex rank-two codes.
- `three_copy_known19_direct.py/json`: actual known19 three-copy twirl control.
- `research_log.md`: chronology and failed relaxations, kept distinct from proof evidence.

The earlier analytic route is preserved in `spinor_equivalence.md`, `rational_formulation.md`, and exact coefficient/control scripts. Its68 moments match the real dimension of Gr_C(2,19); the benefit is the spectrahedral/invariant structure, not a reduction below the original code manifold dimension.

The initial audited checkpoint in the parent directory has not been overwritten. No Pro/external-AI consultation was used in this phase. The private `.venv` was installed from official PyPI with explicit parent approval; exclude it from repository artifacts. Solver results alone are not proofs.
