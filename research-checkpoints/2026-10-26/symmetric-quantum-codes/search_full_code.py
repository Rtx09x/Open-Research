"""Bounded full two-complex-vector search. Near zeros are NOT exact codes."""
import argparse,json,time
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares
from spin_diagnostics import tensors,code19
ROOT=Path(__file__).parent

def hermitian_errors(n,degree=4):
 out=[]
 for r,sect in enumerate(tensors(n)[:degree+1]):
  if r==0:continue
  out.append(sect[r])
  for q in range(1,r+1):
   t=sect[r-q]
   out.extend([(t+t.T)/np.sqrt(2),1j*(t-t.T)/np.sqrt(2)])
 out=np.array(out,dtype=complex)
 assert np.max(abs(out-out.conj().transpose(0,2,1)))<1e-12
 assert np.max(abs(np.einsum('aij,bji->ab',out,out)-np.eye(len(out))))<1e-9
 return out

def pack(C):return np.concatenate([C.real.ravel(),C.imag.ravel()])
def unpack(x,n):return (x[:2*(n+1)]+1j*x[2*(n+1):]).reshape(n+1,2)

def residual_jac(x,n,E,jac=False):
 C=unpack(x,n);u,v=C.T
 out=[np.vdot(u,u).real-1,np.vdot(v,v).real-1,np.vdot(u,v).real,np.vdot(u,v).imag]
 Eu=E@u;Ev=E@v
 uu=np.einsum('i,ai->a',u.conj(),Eu).real;vv=np.einsum('i,ai->a',v.conj(),Ev).real;uv=np.einsum('i,ai->a',u.conj(),Ev)
 out.extend(np.array([uu-vv,2*uv.real,2*uv.imag]).T.ravel())
 if not jac:return np.array(out)
 J=np.zeros((len(out),len(x)));N=n+1
 def put(row,gu,gv):
  # d f = Re <gu,du> + Re <gv,dv>
  gc=np.array([gu,gv]).T;J[row,:2*N]=gc.real.ravel();J[row,2*N:]=gc.imag.ravel()
 z=np.zeros(N,complex)
 put(0,2*u,z);put(1,z,2*v);put(2,v,u);put(3,-1j*v,1j*u)
 for k,(a,b) in enumerate(zip(Eu,Ev)):
  put(4+3*k,2*a,-2*b);put(5+3*k,2*b,2*a);put(6+3*k,-2j*b,2j*a)
 return J

def run(n,starts,seconds):
 E=hermitian_errors(n);rng=np.random.default_rng(20261025);start=time.monotonic();best=1e9;records=[]
 for run in range(starts):
  if time.monotonic()-start>seconds:break
  if n==18 and run<5:
   old=code19();C=(old[:19]*np.sqrt((19-np.arange(19))/19)[:,None]).astype(complex)
   if run:C+=rng.normal(scale=.03*run,size=C.shape)+1j*rng.normal(scale=.03*run,size=C.shape)
  else:C=rng.normal(size=(n+1,2))+1j*rng.normal(size=(n+1,2))
  C=np.linalg.qr(C)[0]
  x=pack(C)
  if run==0:
   from scipy.optimize._numdiff import approx_derivative
   diff=np.max(abs(approx_derivative(lambda y:residual_jac(y,n,E),x)-residual_jac(x,n,E,True)))
   assert diff<1e-6,diff
  r=least_squares(lambda y:residual_jac(y,n,E),x,jac=lambda y:residual_jac(y,n,E,True),max_nfev=1500,ftol=1e-12,xtol=1e-12,gtol=1e-12)
  val=float(np.linalg.norm(r.fun));records.append({'run':run,'norm':val,'nfev':r.nfev,'optimality':r.optimality})
  print(records[-1],flush=True)
  if val<best:
   best=val;np.savez(ROOT/f'full_search_n{n}_best.npz',C=unpack(r.x,n),residual=r.fun)
  (ROOT/f'full_search_n{n}_log.json').write_text(json.dumps({'n':n,'best_norm':best,'records':records,'status':'numerical only; no impossibility follows'},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--n',type=int,default=18);p.add_argument('--starts',type=int,default=12);p.add_argument('--seconds',type=float,default=240);a=p.parse_args();run(a.n,a.starts,a.seconds)
