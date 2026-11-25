"""Depth-three expected potential forms; fine signs integrated, coarse signs enumerated.
Bounded job: checkpoints every64 patterns, exits after230 seconds for resume.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import numpy as np,time,json
from scipy.linalg import block_diag
from baseline import make_hss
from frozen_operator import sign_frame
from energy_ledger import proj_fixed
rng=np.random.default_rng(156);make_hss(1,2,rng);_,fixed=make_hss(1,3,rng);n=16;m=8;B=n*n;C=1+2*m+m*m;ns=m-2;total=2**(2*ns)
W=lambda u:np.array([[-u[1,0]],[u[0,0]]]);UU=block_diag(*[np.hstack([u,W(u)]) for u in fixed[0][0]]);VV=block_diag(*[np.hstack([v,W(v)]) for v in fixed[0][1]])
E=np.eye(B).reshape(B,n,n);A=UU.T@E@VV;aa=A[:,::2,::2];ad=A[:,::2,1::2];da=A[:,1::2,::2];dd=A[:,1::2,1::2]
Pfix=np.stack([proj_fixed(e,fixed).ravel() for e in E],axis=1);Qfix=np.eye(B)-Pfix

def one(F,P):
 g=np.column_stack([-F[:,1],F[:,0]]);q=np.column_stack([-P[:,1],P[:,0]]);y=np.zeros((B,C,m,2));z=y.copy();y[:,0]=aa@F;z[:,0]=aa.transpose(0,2,1)@P;p=1
 for i in range(m):
  col=ad[:,:,i].copy();b=(col@P)@P[i];col[:,i]-=b;y[:,p]=col[:,:,None]*g[i];p+=1
 for i in range(m):
  row=da[:,i,:].copy();b=(row@F)@F[i];row[:,i]-=b;z[:,p]=row[:,:,None]*q[i];p+=1
 for i in range(m):
  for j in range(m):
   y[:,p,i,:]=-dd[:,j,i,None]*(P[i]@q[j])*g[i];z[:,p,j,:]=-dd[:,j,i,None]*(F[j]@g[i])*q[j];p+=1
 y=y.reshape(B*C,m,2);z=z.reshape(B*C,m,2);om=F;ps=P;out=[]
 for us,vs in fixed[1:]:
  mm=len(om);U=block_diag(*us);V=block_diag(*vs);D=np.zeros((B*C,mm,mm));cross=np.zeros((B,B));yf=y.reshape(B,-1);zf=z.reshape(B,-1);before=yf@yf.T+zf@zf.T
  for i,(u,v) in enumerate(zip(us,vs)):
   sl=slice(2*i,2*i+2);pu=u@u.T;pv=v@v.T;d=(np.eye(2)-pu)@y[:,sl]@om[sl].T+pu@(((np.eye(2)-pv)@z[:,sl]@ps[sl].T).transpose(0,2,1));D[:,sl,sl]=d
   a=(u.T@y[:,sl]).reshape(B,-1);b=(u.T@d@om[sl]).reshape(B,-1);cross+=a@b.T
   a=(v.T@z[:,sl]).reshape(B,-1);b=(v.T@d.transpose(0,2,1)@ps[sl]).reshape(B,-1);cross+=a@b.T
  y=U.T@(y-D@om);z=V.T@(z-D.transpose(0,2,1)@ps);om=V.T@om;ps=U.T@ps;yf=y.reshape(B,-1);zf=z.reshape(B,-1);after=yf@yf.T+zf@zf.T;out.append([after-before,(cross+cross.T)/2,before,after])
 return np.array(out)
path='exact_conditional_checkpoint.npz'
if os.path.exists(path):x=np.load(path);start=int(x['count']);acc=x['acc']
else:start=0;acc=np.zeros((2,4,B,B))
t=time.time()
for count in range(start,total):
 ss=np.array([1. if count&(1<<b) else -1. for b in range(2*ns)]);F=sign_frame(fixed[1:],'v',ss[:ns]);P=sign_frame(fixed[1:],'u',ss[ns:]);acc+=one(F,P)
 if (count+1)%64==0:
  np.savez(path,count=count+1,acc=acc);print('checkpoint',count+1,'elapsed',time.time()-t,flush=True)
  if time.time()-t>230:break
if count+1==total:
 ops=acc/total;out=[]
 for j in range(2):
  ev,vec=np.linalg.eigh(Qfix@ops[j,0]@Qfix);cv,cvec=np.linalg.eigh(Qfix@ops[j,1]@Qfix);out.append(dict(coarse_level=j,difference_extrema=[float(ev[0]),float(ev[-1])],cross_extrema=[float(cv[0]),float(cv[-1])],max_after=float(np.linalg.eigvalsh(Qfix@ops[j,3]@Qfix)[-1])));print(out[-1],flush=True)
  np.save(f'exact_cross_witness_{j}.npy',cvec[:,0].reshape(n,n))
 np.savez('exact_conditional_operator_results.npz',operators=ops,P=Pfix);open('exact_conditional_operator_results.json','w').write(json.dumps(out,indent=2))
