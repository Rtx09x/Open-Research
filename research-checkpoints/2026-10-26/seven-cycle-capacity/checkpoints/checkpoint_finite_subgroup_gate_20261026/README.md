# Verified finite-subgroup torus construction gate

Every finite subgroup or translate in (R/Z)^5 with circular coordinate-max
minimum distance at least2/7 has at most367 points. This excludes an existing
direct group/lattice construction principle in dimension5, NOT arbitrary
C7^5 independent codes, nonlinear nearpacking completion, nonlinear coset
unions, higher-dimensional codes, or Shannon capacity. No lower-bound gain.
No publication novelty claimed; BPZ2506.14654 credited in the proof.

From this directory, standard-library-only independent replay:

    timeout 285s python advisor/check_c7_circular_range_independent.py
    timeout 285s python advisor/check_c7_abelian_subgroups_independent.py

The first imports the paired independent382 script as text; both are included.
Each replay takes under one minute, one CPU, less than1GiB. They independently
enumerate cyclic and noncyclic groups respectively. The abelian checker also
verifies exact Fourier theta and all-order reduction; its unused P assignment
retains original workspace provenance and performs no read there.

Optional proposer exact checks:

    python physical_iteration/theta_10_over_3_exact.py
    python physical_iteration/finite_subgroup_theta_reduction.py
    timeout 285s python physical_iteration/abelian_torus_gate.py
    timeout 285s python physical_iteration/check_cyclic_multiplier_gate.py

Scripts write their replay JSON next to themselves; for immutable manifest
verification run in a copied directory. No external downloads or solvers needed.
