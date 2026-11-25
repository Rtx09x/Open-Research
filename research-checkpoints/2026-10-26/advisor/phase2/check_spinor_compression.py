"""Independent Schwinger normalization and positive controls.
Analytic identities are proved in spinor_compression.md. Random/known19 checks
are floating-point controls, not certificates of infeasibility or exact code KL.
"""
from pathlib import Path
from fractions import Fraction as F
import json,math
import numpy as np
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent

def spin(n):
 a=np.zeros((n,n+1),complex);b=a.copy()
 for w in range(n+1):
  if w:a[w-1,w]=math.sqrt(w)
  if w<n:b[w,w]=math.sqrt(n-w)
 plus=a.conj().T@b;minus=plus.conj().T
 J=np.array([(plus+minus)/2,(plus-minus)/(2j),(a.conj().T@a-b.conj().T@b)/2])
 assert np.linalg.norm(a@a.conj().T+b@b.conj().T-(n+1)*np.eye(n))<1e-12
 return a,b,J

def control(n,W,q=None):
 a,b,J=spin(n);j=n/2;m=W.shape[1];A=np.array([W.conj().T@x@W for x in J]);plus=A[0]+1j*A[1];minus=plus.conj().T
 H=j*np.eye(m)-A[2];Hp=j*np.eye(m)+A[2];T=np.block([[H,minus],[plus,Hp]])
 factor=np.hstack([b@W,a@W]);factor_error=np.linalg.norm(T-factor.conj().T@factor)
 schur=Hp-plus@np.linalg.solve(H,minus);eig=np.linalg.eigvalsh(T);seig=np.linalg.eigvalsh(schur)
 out={'n':n,'W_dimension':m,'T_factor_error':factor_error,'T_positive_eigenvalues':eig[eig>1e-8].tolist(),'T_rank_numeric':int(sum(eig>1e-8)),'T_min_eigenvalue':float(eig.min()),'Schur_positive_eigenvalues':seig[seig>1e-8].tolist(),'Schur_norm':float(np.linalg.norm(schur))}
 assert factor_error<1e-10 and eig.min()>-1e-10 and seig.min()>-1e-9
 if q is not None:
  gamma=np.real(np.array([q.conj()@x@q for x in J]));g=np.linalg.norm(gamma)
  expected=np.r_[np.zeros(n),np.ones(n-2)*(n+1),j+1-g,j+1+g]
  out['spectrum_formula_error']=float(np.linalg.norm(np.sort(expected)-eig));assert out['spectrum_formula_error']<1e-9
  R=j*(j+1)*np.eye(m)-sum(x@x for x in A);V=np.column_stack([W.conj().T@x@q for x in J]);K=V.conj().T@V
  forced=np.zeros((3,3),complex)
  for i in range(3):
   for k in range(3):
    eps=0 if i==k else (1 if(i,k)in[(0,1),(1,2),(2,0)]else-1)
    ell=3-i-k if i!=k else 0
    forced[i,k]=((n+1)*j*(j+1)/3*(i==k)-np.trace(A[i]@A[k])-gamma[i]*gamma[k])/2+(1j*eps*gamma[ell]/2 if eps else 0)
  out['forced_K_error']=float(np.linalg.norm(forced-K));assert out['forced_K_error']<1e-9
  out['R_K_trace_power_errors']=[float(abs(np.trace(np.linalg.matrix_power(R,p))-np.trace(np.linalg.matrix_power(K,p))))for p in [1,2,3]]
  assert max(out['R_K_trace_power_errors'])<1e-7
  assert out['T_rank_numeric']==n and out['Schur_norm']<1e-9
 return out

# Exact rational coherent-state control for every n through24.
for n in range(1,25):
 for w in range(n):
  rhs=F(w*(n-w+1),n-w+1) if w else F(0)
  assert rhs==w
 assert [F(n-r)+(r+1 if r<n-1 else 0)for r in range(n)]==[F(n+1)]*(n-1)+[F(1)]

# Generic complex codim1, no reality/time-reversal assumption.
rng=np.random.default_rng(8227);q=rng.normal(size=19)+1j*rng.normal(size=19);q/=np.linalg.norm(q)
_,_,vh=np.linalg.svd(q.conj()[None,:],full_matrices=True);W=vh.conj().T[:,1:]
out={'exact_coherent_controls_n1_to24':True,'random_n18':control(18,W,q)}

# Known19 code from the already exact-certified rational-root center, rebuilt
# using elementary degree<=2 spin products, no worker imports/tensor library.
d=json.loads((ROOT/'symmetric-quantum-codes/code19_root_certificate.json').read_text());co=np.array([1]+[float(F(x))for x in d['center']]);v=np.zeros(20);v[::2]=co*np.sqrt([math.comb(19,w)for w in range(0,20,2)]);v/=np.linalg.norm(v);C=np.column_stack([v,v[::-1]])
_,_,J=spin(19);ops=[np.eye(20),*J]
for i in range(3):
 for k in range(i,3):ops.append((J[i]@J[k]+J[k]@J[i])/2)
images=np.hstack([E@C for E in ops]);u,sv,_=np.linalg.svd(images,full_matrices=False);assert sum(sv>1e-9)==18
out['known19']=control(19,u[:,:18]);assert out['known19']['T_rank_numeric']==19 and len(out['known19']['Schur_positive_eigenvalues'])==1
out['scope']='analytic Schwinger theorem plus exact coherent controls; generic and known19 numerical controls only; no n18 exclusion'
(HERE/'spinor_controls.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
