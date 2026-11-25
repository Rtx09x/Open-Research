import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import numpy as np,itertools,json
from frozen_operator import sign_frame,recovery_operator
out=[]
for L in [1,2]:
 n=2**(L+1);nsg=n-2;fixed=[]
 for ell in range(L,0,-1):fixed.append(([np.array([[1.],[0.]]) for i in range(2**ell)],[np.array([[1.],[0.]]) for i in range(2**ell)]))
 K=np.zeros((n*n,n*n))
 for ss in itertools.product([-1.,1.],repeat=2*nsg):
  om=sign_frame(fixed,'v',ss[:nsg]);ps=sign_frame(fixed,'u',ss[nsg:]);R=recovery_operator(fixed,om,ps);Q=np.eye(n*n)-R;K+=Q.T@Q
 K/=2**(2*nsg);w,v=np.linalg.eigh(K);d=dict(L=L,maxeig=w[-1],diag=np.diag(K).reshape(n,n).tolist(),offdiagK_norm=np.linalg.norm(K-np.diag(np.diag(K))));out.append(d);print(d,flush=True)
open('coordinate_operator_results.json','w').write(json.dumps(out,indent=2))
