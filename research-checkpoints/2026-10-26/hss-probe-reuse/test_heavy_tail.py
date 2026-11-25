import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import numpy as np,json
rng=np.random.default_rng(2219);out=[]
# T's conditional law can be sampled as h G^dagger, with independent h~N(0,I_s).
for s in [3,4,6]:
 for reps in [1000,10000,100000,1000000]:
  G=rng.normal(size=(reps,2,s));h=rng.normal(size=(reps,s))
  Gram=G@G.swapaxes(1,2);rhs=(G@h[...,None])[...,0]
  x=np.linalg.solve(Gram,rhs[...,None])[...,0];z=np.sum(x*x,axis=1)
  d=dict(s=s,reps=reps,mean=float(np.mean(z)),median=float(np.median(z)),p99=float(np.quantile(z,.99)),max=float(np.max(z)),finite_theory=None if s==3 else 2/(s-3));out.append(d);print(d,flush=True)
open('heavy_tail_results.json','w').write(json.dumps(out,indent=2))
