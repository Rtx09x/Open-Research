# HSS reused-probe research checkpoint

**The full RE-02 problem remains unresolved.** The results below have distinct scopes:

- `minimal_sketch_obstruction.md`: at s=3, k=1, the specified reused-Gaussian implementation has infinite expected squared error on a 4×4 input with optimal HSS error 2. This does not exclude larger constant oversampling.
- `tree_flow_theorem.md`: known block-tree support (a strict HSS subclass), 4k queries, and a sharp (2L+2) error factor relative to that subclass's own optimum.
- `actual_dependency_witness.md`: positive compressed-core/test covariance for all finite s≥3; failure of naive independence, not failure of the desired theorem.
- `fixed_basis_unbiasedness.md`: unbiased projection for independently fixed dense nested bases; variance is still unproved.
- `rational_potential_counterexample.md`: an exact rational counterexample to a proposed monotone-energy proof route, not an HSS impossibility theorem.

## Reproduce

```sh
python verify_rational_potential.py
python verify_results.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python exact_tree_test.py
```

The first command is an independent standard-library exact 4096-sign replay. The second checks consistency of stored experiments and must not be mistaken for recomputing them. The last exhausts small finite-sign tree controls; it uses NumPy integer-valued arrays. The root test runner also regenerates the small exact tree controls.

Other included scripts reproduce small dense experiments and document failed routes; `baseline_results.json` and other numerical summaries are not expectation theorems. `variance_reduction_target.md` states the remaining sufficient lemma and records a failed stronger shortcut. Source links are in `literature.md`. Large operator arrays, NPZ checkpoints, downloaded articles/upstream reference implementation, work logs, and consultation packets are excluded. Novelty is not established.
