import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import numpy as np,json,itertools
from scipy.linalg import block_diag
from baseline import make_hss
from frozen_operator import sign_frame
from energy_ledger import proj_fixed

def grams(fixed,om,ps):
 n=len(om);E=np.eye(n*n).reshape(n*n,n,n);y=E@om;z=E.transpose(0,2,1)@ps;out=[]
 for us,vs in fixed:
  m=len(om);U=block_diag(*us);V=block_diag(*vs);D=np.zeros((n*n,m,m));cross=np.zeros((n*n,n*n))
  before=y.reshape(n*n,-1)@y.reshape(n*n,-1).T+z.reshape(n*n,-1)@z.reshape(n*n,-1).T
  for i,(u,v) in enumerate(zip(us,vs)):
   sl=slice(2*i,2*i+2);pu=u@u.T;pv=v@v.T
   d=(np.eye(2)-pu)@y[:,sl,:]@om[sl].T+pu@(((np.eye(2)-pv)@z[:,sl,:]@ps[sl].T).transpose(0,2,1));D[:,sl,sl]=d
   a=(u.T@y[:,sl,:]).reshape(n*n,-1);b=(u.T@d@om[sl]).reshape(n*n,-1);cross+=a@b.T
   a=(v.T@z[:,sl,:]).reshape(n*n,-1);b=(v.T@d.transpose(0,2,1)@ps[sl]).reshape(n*n,-1);cross+=a@b.T
  y=U.T@(y-D@om);z=V.T@(z-D.transpose(0,2,1)@ps);om=V.T@om;ps=U.T@ps
  after=y.reshape(n*n,-1)@y.reshape(n*n,-1).T+z.reshape(n*n,-1)@z.reshape(n*n,-1).T
  out.append((after-before,(cross+cross.T)/2,before,after))
 return out
if __name__=='__main__':
 rng=np.random.default_rng(156);out=[]
 for L,reps in [(2,4096),(3,1000)]:
  n=2**(L+1);_,fixed=make_hss(1,L,rng);nsg=n-2;acc=np.zeros((L,4,n*n,n*n))
  P=np.stack([proj_fixed(E,fixed).ravel() for E in np.eye(n*n).reshape(n*n,n,n)],axis=1);Q=np.eye(n*n)-P
  seq=itertools.product([-1.,1.],repeat=2*nsg) if reps==2**(2*nsg) else (rng.choice([-1.,1.],2*nsg) for r in range(reps))
  for ss in seq:acc+=np.array(grams(fixed,sign_frame(fixed,'v',ss[:nsg]),sign_frame(fixed,'u',ss[nsg:])))
  acc/=reps
  for ell in range(L):
   diff,cross,before,after=acc[ell];ev=np.linalg.eigvalsh(Q@diff@Q);cv=np.linalg.eigvalsh(Q@cross@Q);d=dict(L=L,reps=reps,processed_level=ell,diff_eigs_minmax=[float(ev[0]),float(ev[-1])],cross_eigs_minmax=[float(cv[0]),float(cv[-1])],max_after_energy=float(np.linalg.eigvalsh(Q@after@Q)[-1]));out.append(d);print(d,flush=True)
  np.savez(f'potential_operator_L{L}.npz',operators=acc,P=P)
 open('potential_operator_results.json','w').write(json.dumps(out,indent=2))
