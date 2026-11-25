"""Linear third-order KL constraints via the local operator Casimir."""
import numpy as np
import sympy as s
from sympy.physics.wigner import wigner_6j

def kl_lift(m,rmax=4,details=False):
 n=m['n'];j=s.Rational(n,2);nv=m['nv'];data={};J2all=list(range(n%2,3*n+1,2))
 for J2 in J2all:
  J=s.Rational(J2,2);Ls=[L for L in range(n+1)if abs(L-j)<=J<=L+j];d=len(Ls);F=np.array([[float((-1)**n*s.sqrt((2*L+1)*(2*K+1))*wigner_6j(j,j,L,j,J,K))for K in Ls]for L in Ls]);D=np.diag([(-1)**(n-L)for L in Ls]);F13=D@F@D;Z=np.zeros((d,d,nv))
  for row in m['blocks']:
   if row['J2']!=J2:continue
   U,V=row['U'],row['V']
   for k,(a,b)in enumerate(row['pairs']):
    M=np.outer(U[:,a],U[:,b]);M=M+(M.T if a!=b else 0)
    if V is not None:
     M2=np.outer(V[:,a],V[:,b]);M+=M2+(M2.T if a!=b else 0)
    Z[:,:,row['offset']+k]=M
  W=np.einsum('ab,bcv->acv',2*F13-np.eye(d),Z)/np.sqrt(J2+1);data[J2]=(Ls,W)
 equations=[];errs=[];groups=[]
 for L in range(n+1):
  for Lp in range(L,min(n,L+rmax)+1):
   Js=[J2 for J2 in J2all if L in data[J2][0]and Lp in data[J2][0]]
   if not Js:continue
   C=np.zeros((len(Js),len(Js)))
   for a,K2 in enumerate(Js):
    for b,J2 in enumerate(Js):
     if abs(K2-J2)<=2:C[a,b]=float(3*s.sqrt((K2+1)*(J2+1))*(-1)**(L+Lp)*wigner_6j(j,s.Rational(K2,2),L,s.Rational(J2,2),j,1)*wigner_6j(j,s.Rational(K2,2),Lp,s.Rational(J2,2),j,1))
   Cas=n*(n+2)/2*np.eye(len(Js))-n*(n+1)*(n+2)/6*C;e,V=np.linalg.eigh(Cas);expected=np.array([r*(r+1)for r in range(abs(L-Lp),min(L+Lp,n)+1)])
   assert len(e)==len(expected);errs.append(np.max(abs(e-expected)));assert max(abs(e-expected))<1e-9
   W=np.array([data[J2][1][data[J2][0].index(L),data[J2][0].index(Lp)]for J2 in Js]);eq=V[:,e<rmax*(rmax+1)+.5].T@W
   groups.append({'L':L,'Lp':Lp,'Js':Js,'Vlow':V[:,e<rmax*(rmax+1)+.5],'start':len(equations),'stop':len(equations)+len(eq)});equations.extend(eq)
 E=np.array(equations);U,sv,Vh=np.linalg.svd(E,full_matrices=False);rank=sum(sv>1e-9);meta={'raw_rows':len(E),'rank':int(rank),'singular_values':sv.tolist(),'casimir_eigen_error':float(max(errs))};return (Vh[:rank],meta,E,groups)if details else (Vh[:rank],meta)
