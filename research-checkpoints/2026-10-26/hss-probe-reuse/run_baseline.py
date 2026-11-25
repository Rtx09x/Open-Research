import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import json,time,numpy as np
from baseline import reused_hss,make_hss,hss_rank_check
rng=np.random.default_rng(2538);result=[]
for k in [1,2]:
 for L in [1,2,3,4,5]:
  n=2**(L+1)*k;H,fixed=make_hss(k,L,rng)
  for noise in [0.,1e-5,.1]:
   E=rng.normal(size=(n,n));E*=noise*np.linalg.norm(H)/np.linalg.norm(E)
   A=H+E
   for mode in ['reuse','fixed']:
    ratios=[];rels=[];ranks=[]
    for trial in range(20):
     B,meta=reused_hss(lambda x:A@x,lambda x:A.T@x,n,k,L,6*k,rng,fixed=fixed if mode=='fixed' else None)
     err=np.linalg.norm(B-A)**2
     ratios.append(float(err/max(np.linalg.norm(E)**2,1e-300)));rels.append(float(np.sqrt(err)/np.linalg.norm(A)))
     if trial==0:ranks.append(hss_rank_check(B,k,L))
    result.append(dict(k=k,L=L,n=n,mode=mode,noise=noise,mean_ratio=np.mean(ratios) if noise else None,max_ratio=max(ratios) if noise else None,mean_relerr=np.mean(rels),rank_tail=max(ranks),queries=meta['queries']))
    print(result[-1],flush=True)
open('baseline_results.json','w').write(json.dumps(result,indent=2))
