"""Reproducible supplemental numerical tests of the known-basis theorem."""
import json
import time
import numpy as np
from fixed_basis_algorithm import reconstruct, project


def main():
    rng = np.random.default_rng(20261025)
    rows = []
    start = time.monotonic()
    for k in [1, 2, 3]:
        for L in [1, 2, 3, 4]:
            n = 2**(L+1)*k
            fixed = []
            for ell in range(L, 0, -1):
                us = [np.linalg.qr(rng.normal(size=(2*k, k)))[0] for _ in range(2**ell)]
                vs = [np.linalg.qr(rng.normal(size=(2*k, k)))[0] for _ in range(2**ell)]
                fixed.append((us, vs))
            h = project(rng.normal(size=(n, n)), fixed)
            raw = rng.normal(size=(n, n))
            e = raw-project(raw, fixed)
            e /= np.linalg.norm(e)
            assert np.linalg.norm(project(e, fixed)) < 1e-12
            a = h+0.01*e
            optimum = float(np.linalg.norm(a-project(a, fixed))**2)
            queries = [0, 0]

            def mv(x):
                queries[0] += 1
                return a@x

            def rmv(x):
                queries[1] += 1
                return a.T@x

            errors = []
            residual_energies = []
            for rep in range(25):
                old = queries.copy()
                b, _ = reconstruct(mv, rmv, fixed, k, rng)
                assert [queries[i]-old[i] for i in range(2)] == [2*k, 2*k]
                errors.append(float(np.linalg.norm(a-b)**2/optimum))
                assert np.linalg.norm(b-project(b, fixed)) < 1e-10
                _, energies = reconstruct(lambda x:e@x, lambda x:e.T@x, fixed, k, rng)
                residual_energies.append(energies)
            exact, _ = reconstruct(lambda x:h@x, lambda x:h.T@x, fixed, k, rng)
            exact_error = float(np.linalg.norm(h-exact)/np.linalg.norm(h))
            assert exact_error < 1e-12
            row = dict(k=k,L=L,n=n,trials=25,queries_each_execution=4*k,
                       mean_error_ratio=float(np.mean(errors)),
                       max_error_ratio=float(max(errors)), theorem_mean_bound=20*L+3,
                       mean_residual_cut_energies=np.mean(residual_energies,axis=0).tolist(),
                       exact_model_relative_error=exact_error)
            rows.append(row)
            print(json.dumps(row),flush=True)
            with open('fixed_basis_algorithm_results.json','w') as f:
                json.dump(dict(status='PASS',supplemental_numerical_tests=True,
                               elapsed_seconds=time.monotonic()-start,results=rows),f,indent=2)


if __name__=='__main__':main()
