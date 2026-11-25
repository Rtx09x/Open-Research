"""Supplemental checks of the explicit sibling-gauge finite algorithm."""
import json
import numpy as np
from fixed_basis_algorithm import finite_tree_frame, project, reconstruct


def main():
    rng = np.random.default_rng(617280)
    rows = []
    for k in [1,2,3]:
        for L in [1,2,3,4]:
            n=2**(L+1)*k
            fixed=[]
            for ell in range(L,0,-1):
                fixed.append(tuple([np.linalg.qr(rng.normal(size=(2*k,k)))[0]
                                    for _ in range(2**ell)] for _ in range(2)))
            a=rng.normal(size=(n,n));h=project(a,fixed);e=a-h
            ratios=[];calls=[0,0]
            def mv(x):calls[0]+=1;return a@x
            def rmv(x):calls[1]+=1;return a.T@x
            for _ in range(30):
                before=calls.copy();b,_=reconstruct(mv,rmv,fixed,k,rng,finite=True)
                assert [calls[i]-before[i] for i in range(2)]==[2*k,2*k]
                assert np.linalg.norm(b-project(b,fixed))<1e-10
                ratios.append(float(np.linalg.norm(a-b)**2/np.linalg.norm(e)**2))
            exact,_=reconstruct(lambda x:h@x,lambda x:h.T@x,fixed,k,rng,finite=True)
            error=float(np.linalg.norm(h-exact)/np.linalg.norm(h));assert error<1e-12
            row=dict(k=k,L=L,n=n,trials=30,query_count=4*k,mean_error_ratio=float(np.mean(ratios)),exact_model_error=error)
            rows.append(row);print(json.dumps(row),flush=True)
    with open('finite_orientation_results.json','w') as f:json.dump(dict(status='PASS',numerical_only=True,results=rows),f,indent=2)


if __name__=='__main__':main()
