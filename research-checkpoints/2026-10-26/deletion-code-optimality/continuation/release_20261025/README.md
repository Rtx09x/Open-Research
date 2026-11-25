# Frozen exact global deletion-code checkpoint

Binary length12, one deletion. This package proves

`A(12,1) <= 320497437108/10^9 = 320.497437108`, hence integer upper320.

The integer interval remains316–320. This is NOT a319 bound, NOT a proof of
VT optimality, and NOT a317-word construction. Generic CG inequalities are
classical. Priority of these concrete deletion applications is unverified.

The dual uses578 word cliques,52 rank-one CG rows, and exact internal-orbit
bounds. It does not assume complement/reversal invariance of a code. The
exact verifier checks the geometry and1056 integer coverage constraints.

Independent exact primal certificate: the finite all-clique/current-CG LP
(with the direct cardinality cap omitted) has optimum in
`[320.497435475376,320.497437108]`. A scaled rational point has objective
exactly320 and also satisfies the known cardinality cap. This proves only
that this finite continuous cut list cannot certify319. It does not cover
future cuts or the original-word partial-integrality branch model.

## Isolated replay

Only Python standard library; no NumPy, SciPy, network, solver, or original
workspace files are needed. Do not run Python with -O.

```
python -I -S scripts/verify_cg_hierarchy.py evidence/best_dual.json
python -I -S scripts/verify_fractional_root.py
python -I -S scripts/negative_controls.py
```

The primal checker independently rebuilds insertion incidence and enumerates
all155496 maximal word cliques. It checks786 finite proof nodes and invokes
the dual verifier to justify the cardinality cap. Expected runtime~3s.

An independent advisor used literal insertion, explicit four-way group
transport on4096 words, and separately checked the exact global dual.
No discovery scripts or live branch files are included in this package.
