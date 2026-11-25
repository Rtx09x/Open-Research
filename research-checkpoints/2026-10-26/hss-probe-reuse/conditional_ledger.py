"""Integrate finest complement signs analytically, enumerate only coarse signs."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import numpy as np,itertools,json
from scipy.linalg import block_diag
from baseline import make_hss
from frozen_operator import sign_frame
from energy_ledger import proj_fixed

def channels(A,fixed,F,P):
 us,vs=fixed[0];W=lambda u:np.array([[-u[1,0]],[u[0,0]]]);UU=block_diag(*[np.hstack([u,W(u)]) for u in us]);VV=block_diag(*[np.hstack([v,W(v)]) for v in vs]);C=UU.T@A@VV
 aa=C[::2,::2];ad=C[::2,1::2];da=C[1::2,::2];dd=C[1::2,1::2];m=len(F);g=np.column_stack([-F[:,1],F[:,0]]);q=np.column_stack([-P[:,1],P[:,0]])
 Y=np.zeros((1+2*m+m*m,m,2));Z=Y.copy();Y[0]=aa@F;Z[0]=aa.T@P;p=1
 for i in range(m):
  b=P[i]@(P.T@ad[:,i]);a=ad[:,i].copy();a[i]-=b;Y[p]=a[:,None]*g[i];p+=1
 for i in range(m):
  b=(da[i]@F)@F[i];a=da[i].copy();a[i]-=b;Z[p]=a[:,None]*q[i];p+=1
 for i in range(m):
  for j in range(m):
   Y[p,i]=-(P[i]@q[j])*dd[j,i]*g[i];Z[p,j]=-(F[j]@g[i])*dd[j,i]*q[j];p+=1
 return Y,Z

def batchledger(y,z,fixed,om,ps):
 out=[];nchannels=len(y)
 for us,vs in fixed:
  m=len(om);U=block_diag(*us);V=block_diag(*vs);D=np.zeros((nchannels,m,m));cross=0.
  before=np.linalg.norm(y)**2+np.linalg.norm(z)**2
  for i,(u,v) in enumerate(zip(us,vs)):
   sl=slice(2*i,2*i+2);pu=u@u.T;pv=v@v.T
   d=(np.eye(2)-pu)@y[:,sl,:]@om[sl].T+pu@(((np.eye(2)-pv)@z[:,sl,:]@ps[sl].T).transpose(0,2,1));D[:,sl,sl]=d
   cross+=np.sum((u.T@y[:,sl,:])*(u.T@d@om[sl]))+np.sum((v.T@z[:,sl,:])*(v.T@d.transpose(0,2,1)@ps[sl]))
  y=U.T@(y-D@om);z=V.T@(z-D.transpose(0,2,1)@ps);om=V.T@om;ps=U.T@ps
  out.append([before,np.linalg.norm(y)**2+np.linalg.norm(z)**2,cross])
 return np.array(out)
if __name__=='__main__':
 rng=np.random.default_rng(156);_,_=make_hss(1,2,rng);_,fixed=make_hss(1,3,rng);a=np.load('potential_operator_L3.npz');ops=a['operators'];Q=np.eye(256)-a['P'];out=[]
 for target in [0,1,2]:
  val,vec=np.linalg.eigh(Q@ops[target,1]@Q);E=vec[:,0].reshape(16,16);E-=proj_fixed(E,fixed);E/=np.linalg.norm(E);acc=np.zeros((2,3));m=8;ns=m-2
  for ss in itertools.product([-1.,1.],repeat=2*ns):
   F=sign_frame(fixed[1:],'v',ss[:ns]);P=sign_frame(fixed[1:],'u',ss[ns:]);Y,Z=channels(E,fixed,F,P);acc+=batchledger(Y,Z,fixed[1:],F,P)
  acc/=2**(2*ns);d=dict(target=target,monte_carlo_min_eigenvalue=float(val[0]),exact_sign_mean=acc.tolist(),columns=['before','after','cross_sum']);out.append(d);print(d,flush=True)
 open('conditional_ledger_results.json','w').write(json.dumps(out,indent=2))
