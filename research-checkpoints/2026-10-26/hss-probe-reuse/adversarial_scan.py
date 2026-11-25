import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import json,numpy as np
from baseline import reused_hss,make_hss
rng=np.random.default_rng(8011);out=[]
for L in [2,3,4,5,6,7]:
 k=1;n=2**(L+1);H,fixed=make_hss(k,L,rng);H/=np.linalg.norm(H)
 vectors=[]
 # Leaf checkerboard, alternating dyadic, representative spikes, and random.
 for typ in ['leaf_checker','dyadic_checker','corner','identity_cross','random']:
  E=np.zeros((n,n))
  if typ=='leaf_checker':
   u=np.tile([1.,-1.],n//2);v=rng.choice([-1.,1.],n);E=np.outer(u,v)
  elif typ=='dyadic_checker':
   for width in [2**q for q in range(2,L+2)]:
    for start in range(0,n,width):
     q=width//2;u=np.r_[np.ones(q//2),-np.ones(q//2)];E[start:start+q,start+q:start+width]+=np.outer(u,u)/width
  elif typ=='corner':E[n//2-1,n-1]=1.
  elif typ=='identity_cross':E[:n//2,n//2:]=np.eye(n//2);E[n//2:,:n//2]=np.eye(n//2)
  else:E=rng.normal(size=(n,n))
  E/=np.linalg.norm(E)
  for eps in [1e-6,.1,10.]:
   A=H+eps*E
   for s in [4,6,10]:
    ratios=[]
    for rep in range(30):
     B,_=reused_hss(lambda x:A@x,lambda x:A.T@x,n,k,L,s,rng)
     ratios.append(float(np.linalg.norm(A-B)**2/eps**2))
    d=dict(L=L,n=n,type=typ,eps=eps,s=s,mean=float(np.mean(ratios)),p90=float(np.quantile(ratios,.9)),maximum=max(ratios));out.append(d);print(d,flush=True)
 open('adversarial_checkpoint.json','w').write(json.dumps(out,indent=2))
open('adversarial_results.json','w').write(json.dumps(out,indent=2))
