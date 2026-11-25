# Local-only structural diagnosis and exact tests

The280 remaining clique-cover gap is NOT a constructive280-word gain. The
fixed-pairing Hall set has4272 core words/3992 compatible cliques but5248 real
Z neighbors. Forcing this core set and optimizing admissibleT(Z) gives exact
maximum133828, well below134753. Scope is this fixed seed/pairing only.

Run these standard-library checks sequentially from this directory:

    timeout 285s python physical_iteration/verify_hall_shadow_seed.py
    timeout 285s python advisor/check_c7_attachment_hall_independent.py
    timeout 285s python advisor/check_c7_hall_seed_independent.py

The advisor base reconstruction differs from its preserved original only in
the workspace-root path. The Hall checker must precede the advisor seed checker.

A new construction criterion and bounded supplied-reservoir tester are included:

    timeout 285s python physical_iteration/reservoir_escape_gate.py --output diagnostic_control.json.gz

This no-argument run is a known negative control, not another reservoir search.
A supplied independent rectangle recipe reaches135093 exactly when its
unfiltered Hall surplus against Z is at least340. No such new reservoir has
been found. Other combinations are not excluded, fullC7 capacity stays open,
and the global lower bound is unchanged. See the structural diagnosis document.

Local frozen packet only; no upload/git/publication. LICENSE/NOTICE retained.
