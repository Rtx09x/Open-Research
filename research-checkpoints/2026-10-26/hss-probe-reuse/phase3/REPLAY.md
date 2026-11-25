# Minimal replay

Use a fresh writable working directory; scripts write JSON/log outputs to the
current directory. Keep this source bundle read-only. Set B to its absolute path.

    mkdir -p /tmp/hss-checkpoint-replay && cd /tmp/hss-checkpoint-replay
    export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
    python "$B/verify_triangular_regression_exact.py"
    python "$B/verify_path_ls_gauge_exact.py"
    python "$B/verify_dense_envelope_clique.py"
    python "$B/verify_matrix_one_bank_bound.py"
    python "$B/verify_wide_haar_coercivity.py"

These exact controls use Python standard-library Fraction/integer arithmetic.
The following additional integer/block tests require NumPy (no large compute):

    python "$B/coordinate_observation_forest.py"
    python "$B/coordinate_star_probing.py"
    python "$B/verify_three_color_forest.py"

Main numerical implementation checks require NumPy and SciPy:

    python "$B/test_fixed_basis_algorithm.py"
    python "$B/test_finite_orientation_variant.py"

Optional numerical path controls require NumPy:

    python "$B/test_path_global_ls_inverse.py"
    python "$B/test_path_global_ls_robustness.py"

All controls are small single-CPU jobs; none is the all-depth proof. The proof
files and their exact scope remain primary. Coordinate observation-forest
replay imports the included independent greedy verifier only for the final
corroborating family check, not for its exhaustive arbitrary-basis checks.
