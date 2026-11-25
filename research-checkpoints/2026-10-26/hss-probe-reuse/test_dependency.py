import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import numpy as np,json
rng=np.random.default_rng(831);out=[]
for r in [1,2,4,8,16]:
 M=rng.normal(size=(200000,2,r));S=M@M.swapaxes(1,2);lam,U=np.linalg.eigh(S);X=U[:,0,1]**2;W=S[:,0,0]
 cov=float(np.mean((X-X.mean())*(W-W.mean())));pred=float(np.mean(lam[:,1]-lam[:,0])/8)
 d=dict(null_columns=r,sketch_width=r+2,covariance=cov,theory_from_gap=pred,X_variance=float(np.var(X)),expected_X_variance=.125);out.append(d);print(d,flush=True)
open('dependency_results.json','w').write(json.dumps(out,indent=2))
