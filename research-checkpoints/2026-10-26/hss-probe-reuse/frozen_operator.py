"""Worst-direction mean-square test for the frozen dense-basis algorithm."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import numpy as np
from scipy.linalg import block_diag
from baseline import make_hss

def sign_frame(fixed,side,signs):
    x=np.eye(2);p=0
    for us,vs in reversed(fixed):
        bases=us if side=='u' else vs;out=[]
        for i,B in enumerate(bases):
            f=x[i:i+1];w=np.array([[-B[1,0]],[B[0,0]]]);g=signs[p]*np.array([[-f[0,1],f[0,0]]]);p+=1
            out.append(B@f+w@g)
        x=np.vstack(out)
    return x

def recovery_operator(fixed,om,ps):
    n=len(om);E=np.eye(n*n).reshape(n*n,n,n);y=E@om;z=E.transpose(0,2,1)@ps;levels=[]
    for us,vs in fixed:
        m=len(om);U=block_diag(*us);V=block_diag(*vs);D=np.zeros((n*n,m,m))
        for i,(u,v) in enumerate(zip(us,vs)):
            sl=slice(2*i,2*i+2);pu=u@u.T;pv=v@v.T
            D[:,sl,sl]=(np.eye(2)-pu)@y[:,sl,:]@om[sl].T+pu@(((np.eye(2)-pv)@z[:,sl,:]@ps[sl].T).transpose(0,2,1))
        levels.append((U,V,D));y=U.T@(y-D@om);z=V.T@(z-D.transpose(0,2,1)@ps);om=V.T@om;ps=U.T@ps
    B=y@om.T
    for U,V,D in reversed(levels):B=U@B@V.T+D
    return B.reshape(n*n,n*n).T

if __name__=='__main__':
 import itertools,json,time
 rng=np.random.default_rng(1293);out=[]
 for L,reps in [(1,16),(2,4096),(3,500)]:
  n=2**(L+1);H,fixed=make_hss(1,L,rng);nsg=n-2;K=np.zeros((n*n,n*n));Rmean=K.copy()
  signs=itertools.product([-1.,1.],repeat=2*nsg) if reps==2**(2*nsg) else (rng.choice([-1.,1.],2*nsg) for i in range(reps))
  t=__import__('time').time()
  for count,ss in enumerate(signs,1):
   om=sign_frame(fixed,'v',ss[:nsg]);ps=sign_frame(fixed,'u',ss[nsg:]);R=recovery_operator(fixed,om,ps);Q=np.eye(n*n)-R;K+=Q.T@Q;Rmean+=R
  K/=count;Rmean/=count;eig,vec=np.linalg.eigh(K);np.savez(f'frozen_operator_L{L}.npz',K=K,Rmean=Rmean,H=H,top_direction=vec[:,-1].reshape(n,n),eig=eig)
  d=dict(L=L,n=n,reps=count,worst_expected_error=float(eig[-1]),top_eigs=eig[-10:].tolist(),trace=float(np.trace(K)),time=__import__('time').time()-t,exact_H_error=float(np.linalg.norm((np.eye(n*n)-Rmean)@H.ravel())));out.append(d);print(d,flush=True)
 open('frozen_operator_results.json','w').write(json.dumps(out,indent=2))
