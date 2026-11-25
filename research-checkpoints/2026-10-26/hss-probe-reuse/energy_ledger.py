import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import numpy as np,json,itertools
from scipy.linalg import block_diag
from baseline import make_hss
from frozen_operator import sign_frame

def proj_fixed(A,fixed):
 if not fixed:return A
 us,vs=fixed[0];U=block_diag(*us);V=block_diag(*vs);D=np.zeros_like(A)
 for i,(u,v) in enumerate(zip(us,vs)):
  sl=slice(2*i,2*i+2);a=A[sl,sl];D[sl,sl]=a-u@u.T@a@v@v.T
 return D+U@proj_fixed(U.T@A@V,fixed[1:])@V.T

def ledger(A,fixed,om,ps):
 y=A@om;z=A.T@ps;out=[]
 for us,vs in fixed:
  U=block_diag(*us);V=block_diag(*vs);Ds=[];cross1=0.;cross2=0.;denergy=0
  before=np.linalg.norm(y)**2+np.linalg.norm(z)**2
  for i,(u,v) in enumerate(zip(us,vs)):
   sl=slice(2*i,2*i+2);pu=u@u.T;pv=v@v.T
   d=(np.eye(2)-pu)@y[sl]@om[sl].T+pu@((np.eye(2)-pv)@z[sl]@ps[sl].T).T
   cross1+=float(np.sum((u.T@y[sl])*(u.T@d@om[sl])))
   cross2+=float(np.sum((v.T@z[sl])*(v.T@d.T@ps[sl])))
   Ds.append(d);denergy+=np.linalg.norm(d)**2
  D=block_diag(*Ds);y=U.T@(y-D@om);z=V.T@(z-D.T@ps);om=V.T@om;ps=U.T@ps
  after=np.linalg.norm(y)**2+np.linalg.norm(z)**2
  out.append([before,after,cross1,cross2,denergy])
 return np.array(out)
if __name__=='__main__':
 rng=np.random.default_rng(71);out=[]
 for L,reps in [(1,16),(2,4096),(3,10000),(5,5000)]:
  n=2**(L+1);_,fixed=make_hss(1,L,rng);A=rng.normal(size=(n,n));A-=proj_fixed(A,fixed);A/=np.linalg.norm(A);nsg=n-2
  acc=np.zeros((L,5));acc2=acc.copy();seq=itertools.product([-1.,1.],repeat=2*nsg) if reps==2**(2*nsg) else (rng.choice([-1.,1.],2*nsg) for r in range(reps))
  for ss in seq:
   v=ledger(A,fixed,sign_frame(fixed,'v',ss[:nsg]),sign_frame(fixed,'u',ss[nsg:]));acc+=v;acc2+=v*v
  mean=acc/reps;se=np.sqrt(np.maximum(acc2/reps-mean*mean,0)/reps)
  d=dict(L=L,reps=reps,columns=['before','after','cross_forward','cross_transpose','coefficient_energy'],mean=mean.tolist(),standard_error=se.tolist());out.append(d);print(d,flush=True)
 open('energy_ledger_results.json','w').write(json.dumps(out,indent=2))
