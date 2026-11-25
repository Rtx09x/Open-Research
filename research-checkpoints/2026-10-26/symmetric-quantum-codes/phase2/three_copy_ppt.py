"""PPT strengthening of three-copy SU2 moment extension; numerical results only."""
import sys,time,json
from pathlib import Path
import numpy as np
import sympy as s
from sympy.physics.wigner import wigner_6j
import cvxpy as cp
from scipy import sparse
from three_copy_sdp import build,ROOT
from spin_diagnostics import code19,tensors

def ppt_coefficients(m):
 n=m['n'];j=s.Rational(n,2);nv=m['nv'];J2s=list(range(n%2,3*n+1,2));data={}
 for J2 in J2s:
  J=s.Rational(J2,2);Ls=[L for L in range(n+1)if abs(L-j)<=J<=L+j];Z=np.zeros((len(Ls),len(Ls),nv))
  for row in m['blocks']:
   if row['J2']!=J2:continue
   U,V=row['U'],row['V']
   for k,(a,b)in enumerate(row['pairs']):
    mat=np.outer(U[:,a],U[:,b])
    if a!=b:mat+=mat.T
    if V is not None:
     mm=np.outer(V[:,a],V[:,b]);mat+=mm+(mm.T if a!=b else 0)
    Z[:,:,row['offset']+k]=mat
  data[J2]=(Ls,Z)
 out=[]
 for K2 in J2s:
  K=s.Rational(K2,2);Ls=data[K2][0]
  for parity in [0,1]:
   keep=[L for L in Ls if L%2==parity]
   if not keep:continue
   P=np.zeros((len(keep),len(keep),nv))
   for a,L in enumerate(keep):
    for b,Lp in enumerate(keep[:a+1]):
     for J2,(JJ,Z)in data.items():
      if L not in JJ or Lp not in JJ:continue
      coef=float((-1)**n*wigner_6j(L,j,s.Rational(J2,2),Lp,j,K));P[a,b]+=coef*Z[JJ.index(L),JJ.index(Lp)]
     P[b,a]=P[a,b]
   out.append((K2,parity,P))
  if K2%10==n%2:print('PPT coefficients through K2',K2,flush=True)
 return out

def run(n,known=False):
 st=time.time();m=build(n);coeff=ppt_coefficients(m);x=cp.Variable(m['nv']);cons=[m['E']@x==m['b'],np.array(m['cuts'])@x>=0];mats=[]
 for b in m['blocks']:
  inds={pair:b['offset']+k for k,pair in enumerate(b['pairs'])};X=cp.bmat([[x[inds[(min(i,j),max(i,j))]]for j in range(b['m'])]for i in range(b['m'])]);cons.append(X>>0);mats.append(X)
 ppt=[]
 for K2,parity,P in coeff:
  d=P.shape[0];Y=cp.reshape(sparse.csr_matrix(P.reshape(d*d,-1))@x,(d,d),order='C');cons.append(Y>>0);ppt.append(Y)
 if known:
  C=code19();P=C@C.T;a=np.array([(n+1)/4*sum(abs(np.trace(P@T))**2 for T in sect)for sect in tensors(n)]);cons.append(x[:n+1]==a)
 prob=cp.Problem(cp.Minimize(0),cons);prob.solve(solver='CLARABEL',max_iter=200,tol_gap_abs=1e-9,tol_feas=1e-9,tol_gap_rel=1e-9,verbose=False)
 out={'n':n,'known19_enumerator_fixed':known,'status':prob.status,'elapsed_seconds':time.time()-st,'variables':m['nv'],'PSD_blocks':len(mats),'PPT_blocks':len(ppt),'not_exact_certificate':True}
 if x.value is not None:
  out.update({'equality_error':float(max(abs(m['E']@x.value-m['b']))),'linear_slack':float(min(np.array(m['cuts'])@x.value)),'PSD_min':float(min(np.linalg.eigvalsh(M.value)[0]for M in mats)),'PPT_min':float(min(np.linalg.eigvalsh(M.value)[0]for M in ppt))});np.savez(Path(__file__).with_name(f'three_copy_ppt_n{n}.npz'),x=x.value)
 Path(__file__).with_name(f'three_copy_ppt_n{n}.json').write_text(json.dumps(out,indent=2));print(out,flush=True)
if __name__=='__main__':run(int(sys.argv[1])if len(sys.argv)>1 else 18,known=(len(sys.argv)>1 and sys.argv[1]=='19'))
