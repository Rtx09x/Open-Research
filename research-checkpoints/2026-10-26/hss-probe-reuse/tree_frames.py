"""Tree-adapted orthonormal-row probes for fixed nested bases (experimental)."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import numpy as np
from baseline import nullifier,reused_hss,make_hss

def frame(n,s,rng):return np.linalg.qr(rng.normal(size=(s,n)))[0].T

def tree_frame(fixed,side,k,s,rng):
    tests=frame(2*k,s,rng)
    for us,vs in reversed(fixed):
        bases=us if side=='u' else vs
        out=[]
        for i,B in enumerate(bases):
            active=tests[k*i:k*(i+1)]
            Q=np.linalg.qr(B,mode='complete')[0][:,k:]
            ambient=nullifier(active).T
            extra=frame(k,s-k,rng)@ambient
            out.append(B@active+Q@extra)
        tests=np.vstack(out)
    return tests

if __name__=='__main__':
 import json
 rng=np.random.default_rng(7214);out=[]
 for L in [1,2,3,4,5,6,7]:
  k=1;n=2**(L+1)*k;H,fixed=make_hss(k,L,rng)
  E=rng.normal(size=(n,n));E/=np.linalg.norm(E)
  for s in [2*k,4*k,6*k]:
   errors=[];norms=[];exact=[]
   for rep in range(50):
    om=tree_frame(fixed,'v',k,s,rng);ps=tree_frame(fixed,'u',k,s,rng)
    B,_=reused_hss(lambda x:E@x,lambda x:E.T@x,n,k,L,s,rng,fixed=fixed,sketches=(om,ps))
    errors.append(np.linalg.norm(E-B)**2);norms.append(np.linalg.norm(B)**2)
    if rep==0:
     C,_=reused_hss(lambda x:H@x,lambda x:H.T@x,n,k,L,s,rng,fixed=fixed,sketches=(om,ps));exact.append(np.linalg.norm(C-H)/np.linalg.norm(H))
   d=dict(L=L,n=n,s=s,meanerr=np.mean(errors),maxerr=max(errors),mean_reconstruction_norm2=np.mean(norms),exact_error=max(exact));out.append(d);print(d,flush=True)
 open('tree_frame_results.json','w').write(json.dumps(out,indent=2))
