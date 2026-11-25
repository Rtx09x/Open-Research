"""Adversarial direct-CG controls for arbitrary complex rank-two projectors.
No KL imposed. In particular these controls are NOT time-reversal invariant.
Direct full-Hilbert twirl/PT is compared to recoupling and reduced real maps.
"""
import sys,time,json
from pathlib import Path
from functools import lru_cache
import numpy as np
import sympy as s
from sympy.physics.wigner import clebsch_gordan,wigner_6j
BASE=Path(__file__).resolve().parents[1]/'symmetric-quantum-codes'/'phase2';sys.path.insert(0,str(BASE))
from three_copy_sdp import build
from three_copy_ppt import ppt_coefficients
@lru_cache(None)
def cg(j1,j2,J):
 a=[-j1+i for i in range(int(2*j1+1))];b=[-j2+i for i in range(int(2*j2+1))];c=[-J+i for i in range(int(2*J+1))]
 return np.array([[float(clebsch_gordan(j1,j2,J,m,n,M)) if m+n==M else 0. for M in c]for m in a for n in b])
def run(n,seed):
 st=time.time();N=n+1;j=s.Rational(n,2);D=N**3;rng=np.random.default_rng(seed)
 C,_=np.linalg.qr(rng.standard_normal((N,2))+1j*rng.standard_normal((N,2)));P=C@C.conj().T;Q=np.eye(N)-P
 T=np.zeros((N,N));
 for a in range(N):T[a,N-1-a]=(-1)**(n-a)
 tr_violation=np.linalg.norm(P-T@P.conj()@T.T)
 pair={L:cg(j,j,s.Integer(L)) for L in range(N)};U={};Ls={}
 for J2 in range(n%2,3*n+1,2):
  J=s.Rational(J2,2);Ls[J2]=[L for L in range(N)if abs(L-j)<=J<=L+j]
  U[J2]=[np.kron(pair[L],np.eye(N))@cg(s.Integer(L),j,J) for L in Ls[J2]]
 def blocks(A):
  return {J2:np.array([[np.trace(u.T@A@v)/(J2+1) for v in UU]for u in UU]) for J2,UU in U.items()}
 def matrix(B):
  out=np.zeros((D,D),complex)
  for J2,UU in U.items():
   for a,u in enumerate(UU):
    for b,v in enumerate(UU):out+=B[J2][a,b]*(u@v.T)
  return out
 def pt3(A):
  B=A.reshape((N,)*6).transpose(0,1,5,3,4,2).reshape(D,D);R=np.kron(np.eye(N*N),T);return R@B@R.T
 def crossing(B):
  out={}
  for K2,ls in Ls.items():
   K=s.Rational(K2,2);A=np.zeros((len(ls),len(ls)),complex)
   for a,L in enumerate(ls):
    for b,Lp in enumerate(ls):
     for J2,js in Ls.items():
      if L in js and Lp in js:A[a,b]+=float((-1)**n*(J2+1)*wigner_6j(L,j,s.Rational(J2,2),Lp,j,K))*B[J2][js.index(L),js.index(Lp)]
   out[K2]=A
  return out
 Zb=blocks(np.kron(np.kron(P,P),P));Z=matrix(Zb);PT=pt3(Z);PTb=blocks(PT);pred=crossing(Zb)
 complex_cross_error=max(np.max(abs(pred[J]-PTb[J])) for J in U)
 gauge={J:np.diag([(-1)**L for L in ls])for J,ls in Ls.items()};m=build(n);x=np.zeros(m['nv']);reconstruction_error=0
 for J,ls in Ls.items():
  S=gauge[J]@Zb[J].real@gauge[J]*(J+1);R=np.zeros_like(S)
  for b in m['blocks']:
   if b['J2']!=J:continue
   B,V=b['U'],b['V'];X=B.T@S@B
   for k,(a,c)in enumerate(b['pairs']):x[b['offset']+k]=X[a,c]
   R+=B@X@B.T+(V@X@V.T if V is not None else 0)
  reconstruction_error=max(reconstruction_error,float(np.max(abs(S-R))))
 coef=ppt_coefficients(m);reduced_pt_error=0
 for J,parity,A in coef:
  keep=[k for k,L in enumerate(Ls[J])if L%2==parity];R=np.einsum('abv,v->ab',A,x);B=gauge[J]@PTb[J].real@gauge[J];reduced_pt_error=max(reduced_pt_error,float(np.max(abs(R-B[np.ix_(keep,keep)]))))
 # Check that PT generically does NOT commute with Swap23: only Swap12 symmetry survives.
 swap23=np.eye(D).reshape((N,)*6).transpose(0,2,1,3,4,5).reshape(D,D)
 pt_s3_failure=np.linalg.norm(PT@swap23-swap23@PT)
 pair_weights={L:np.trace(pair[L].T@np.kron(P,P)@pair[L]).real for L in range(N)}
 errors={};mins={}
 for tag,A,B,Cc in [('PPP',P,P,P),('PPQ',P,P,Q),('PQQ',P,Q,Q),('QQQ',Q,Q,Q)]:
  direct=blocks(np.kron(np.kron(A,B),Cc));predicted={}
  for J2,ls in Ls.items():
   J=s.Rational(J2,2);d=len(ls);F=np.array([[float((-1)**n*s.sqrt((2*L+1)*(2*K+1))*wigner_6j(j,j,L,j,J,K))for K in ls]for L in ls]);D12=np.diag([(-1)**(n-L)for L in ls]);F13=D12@F@D12
   Dpair=np.diag([pair_weights[L]/(2*L+1)for L in ls]);ZZ=gauge[J2]@Zb[J2]@gauge[J2];Y13=F@Dpair@F;Y23=F13@Dpair@F13
   val={'PPP':ZZ,'PPQ':Dpair-ZZ,'PQQ':2/N*np.eye(d)-Dpair-Y13+ZZ,'QQQ':(1-6/N)*np.eye(d)+Dpair+Y13+Y23-ZZ}[tag]
   predicted[J2]=gauge[J2]@val@gauge[J2]
  errors[tag]=max(float(np.max(abs(direct[J]-predicted[J]))) for J in U)
  directPT=blocks(pt3(matrix(direct)));predPT=crossing(predicted)
  errors['PT_'+tag]=max(float(np.max(abs(directPT[J]-predPT[J])))for J in U)
  mins[tag]=min(float(np.linalg.eigvalsh(A)[0])for A in direct.values());mins['PT_'+tag]=min(float(np.linalg.eigvalsh(A)[0])for A in directPT.values())
 out=dict(n=n,seed=seed,time_reversal_violation=float(tr_violation),imaginary_moment_size=max(float(np.max(abs(B.imag)))for B in Zb.values()),complex_crossing_error=float(complex_cross_error),real_S3_reconstruction_error=reconstruction_error,reduced_PPT_error=reduced_pt_error,PT_Swap23_commutator=float(pt_s3_failure),mixed_formula_errors=errors,cone_minima=mins,seconds=time.time()-st)
 assert tr_violation>0.1 and complex_cross_error<1e-10 and reconstruction_error<1e-10 and reduced_pt_error<1e-10 and max(errors.values())<1e-10 and min(mins.values())>-1e-10
 return out
if __name__=='__main__':
 start=time.time();rows=[]
 for n in [2,3,4,5,6]:
  row=run(n,1937+n);rows.append(row);print(json.dumps(row),flush=True)
  Path(__file__).with_suffix('.json').write_text(json.dumps(dict(status='PASS',rows=rows,total_seconds=time.time()-start),indent=2)+'\n')
