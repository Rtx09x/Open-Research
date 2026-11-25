"""Numerical phase-gauge and complex matvec-count control, not proof."""
import numpy as np,json
from scipy.linalg import block_diag
from global_ls_probe import frames
from fixed_basis_algorithm import project

def gauge(fixed,side):
 phases=np.ones(2,dtype=complex)
 for pair in reversed(fixed):
  phases=np.concatenate([eta*np.where(abs(b[:,0])>0,b[:,0]/np.where(abs(b[:,0])>0,abs(b[:,0]),1),1) for eta,b in zip(phases,pair[side])])
 return phases

def cproject(A,fixed):
 if not fixed:return A.copy()
 us,vs=fixed[0];U,V=block_diag(*us),block_diag(*vs);D=np.zeros_like(A)
 for i,(u,v) in enumerate(zip(us,vs)):
  sl=slice(2*i,2*i+2);b=A[sl,sl];D[sl,sl]=b-u@(u.conj().T@b@v)@v.conj().T
 return D+U@cproject(U.conj().T@A@V,fixed[1:])@V.conj().T

def reconstruct(A,real,du,dv,rng):
 om,ps=frames(real,'v',1,3,rng),frames(real,'u',1,3,rng);counts=[0,0]
 def mv(v):counts[0]+=1;return du.conj()*(A@(dv*v))
 def amv(v):counts[1]+=1;return dv.conj()*(A.conj().T@(du*v))
 Y=np.column_stack([mv(om[:,i]) for i in range(3)])
 Z=np.conj(np.column_stack([amv(ps[:,i]) for i in range(3)]));levels=[]
 for us,vs in real:
  U,V=block_diag(*us),block_diag(*vs);D=np.zeros((len(om),len(om)),complex)
  for i,(u,v) in enumerate(zip(us,vs)):
   sl=slice(2*i,2*i+2);pu,pv=u@u.T,v@v.T
   D[sl,sl]=(np.eye(2)-pu)@Y[sl]@om[sl].T+pu@((np.eye(2)-pv)@Z[sl]@ps[sl].T).T
  levels.append((U,V,D));Y,Z=U.T@(Y-D@om),V.T@(Z-D.T@ps);om,ps=V.T@om,U.T@ps
 B=Y@om.T
 for U,V,D in reversed(levels):B=U@B@V.T+D
 assert counts==[3,3]
 return du[:,None]*B*dv.conj()[None,:]

def main():
 rng=np.random.default_rng(465421);rows=[]
 for L in [1,2,3,4]:
  n=2**(L+1);fixed=[]
  for ell in range(L,0,-1):
   pair=[]
   for side in range(2):
    bank=[]
    for i in range(2**ell):
     b=rng.normal(size=(2,1))+1j*rng.normal(size=(2,1));bank.append(b/np.linalg.norm(b))
    pair.append(bank)
   fixed.append(tuple(pair))
  real=[tuple([abs(b) for b in bank] for bank in pair) for pair in fixed]
  du,dv=gauge(fixed,0),gauge(fixed,1);A=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n));H=cproject(A,fixed)
  At=du.conj()[:,None]*A*dv[None,:];Hp=du[:,None]*project(At,real)*dv.conj()[None,:]
  assert np.linalg.norm(H-Hp)<1e-10
  B=reconstruct(H,real,du,dv,rng);assert np.linalg.norm(B-H)<1e-9
  B=reconstruct(A,real,du,dv,rng);assert np.linalg.norm(B-cproject(B,fixed))<1e-9
  rows.append(dict(L=L,n=n,complex_forward_calls=3,complex_adjoint_calls=3,projection_gauge_defect=float(np.linalg.norm(H-Hp)),exact_on_class_defect=float(np.linalg.norm(reconstruct(H,real,du,dv,rng)-H))))
 report=dict(status='NUMERICAL_IMPLEMENTATION_CONTROL_PASS',checks=rows,scope='Phase gauge and complex query implementation only; analytic corollary separate')
 print(json.dumps(report,indent=2));open('complex_scalar_gauge_results.json','w').write(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
