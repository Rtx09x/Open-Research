# The sharp one-bank constant-one shortcut is false, but gain is bounded

At k=1,L=4,N=32, fix all bases to (1,0), except U_0=(0,1) at the eight-node
level and V_0=(3/5,4/5) at both the four-node and two-node levels. Fix all
forward complement signs to +1, and let transpose signs be independent.
Take Y0 zero except physical row1 equals Omega row0; take Z0=0. Initial energy
is one and is independent of the transpose bank.

The exact carried energies are `[1,1,1,913/625]` for every transpose-sign
realization. The independent standard-library full-recursion verifier
`verify_one_bank_counterexample.py` checks all16 active branch-sign cases;
the other26 signs belong to identically zero subtrees, accounting for all2^30
outcomes. A separate floating-point full-operator implementation agrees.

This refutes constant one and one-bank monotonicity, **not** all uniform
constants. The later theorem `fixed_basis_bound.md` proves a sharp uniform
constant five for arbitrary-k Haar one-bank transport. Exact rational branch
examples in `verify_one_bank_sharpness.py` attain2.37003,3.21409,4.45879,
4.85575,4.96338 as the chosen path grows. Their limit is five, not infinity.

Neither the sharp-one failure nor sharp-five transport is itself a statement
about the unknown-basis HSS optimum. The complete fixed-basis proof handles
the actual correlated sectors separately.
