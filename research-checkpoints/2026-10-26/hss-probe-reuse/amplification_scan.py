import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import json,numpy as np
from baseline import reused_hss,make_hss
rng=np.random.default_rng(35711);out=[]
for L in range(2,8):
 k=1;n=2**(L+1);H,fixed=make_hss(k,L,rng);H/=np.linalg.norm(H);E=rng.normal(size=(n,n));E/=np.linalg.norm(E)
 for s in [4,5,6]:
  for mode in ['fixed','adaptive']:
   ratios=[]
   for rep in range(100):
    A=E if mode=='fixed' else H+1e-6*E
    B,_=reused_hss(lambda x:A@x,lambda x:A.T@x,n,k,L,s,rng,fixed=fixed if mode=='fixed' else None)
    ratios.append(float(np.linalg.norm(A-B)**2/(1 if mode=='fixed' else 1e-12)))
   d=dict(L=L,n=n,s=s,mode=mode,mean=float(np.mean(ratios)),median=float(np.median(ratios)),p90=float(np.quantile(ratios,.9)),maximum=max(ratios));out.append(d);print(d,flush=True)
 open('amplification_checkpoint.json','w').write(json.dumps(out,indent=2))
open('amplification_results.json','w').write(json.dumps(out,indent=2))
