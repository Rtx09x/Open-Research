"""Rational k2 check of full physical branch, flux, and a failed naive cone."""
from fractions import Fraction as F
import json,random
from verify_triangular_regression_exact import mul,tr,eye,zero,add,bd

def scale(a,c):return [[c*x for x in r] for r in a]
def norm(a):return sum(x*x for r in a for x in r)
def cat(a,b):return [x+y for x,y in zip(a,b)]
def sub(a,i,j,r,c):return [x[j:j+c] for x in a[i:i+r]]
def orth(n,seed):
 rng=random.Random(seed);q=eye(n)
 for t in range(3*n):
  i,j=rng.sample(range(n),2);c,s=F(3,5),F(4,5)
  oldi,oldj=q[i],q[j];q[i]=[c*x-s*y for x,y in zip(oldi,oldj)];q[j]=[s*x+c*y for x,y in zip(oldi,oldj)]
 return q

def main():
 k,s,d=2,6,4;e=eye(s);F0,G,J=e[:k],e[k:2*k],e[2*k:];P,Q,K=F0,G,J
 OV,OU=orth(4,83),orth(4,91)
 A,B,Ap,Bp=[sub(OV,i,j,k,k) for i,j in [(0,0),(0,k),(k,0),(k,k)]]
 R,T,Rp,Tp=[sub(OU,i,j,k,k) for i,j in [(0,0),(0,k),(k,0),(k,k)]]
 X=[[F(2),F(1)],[F(-1),F(3)]];Z=[[F(1),F(-2)],[F(4),F(0)]]
 Y=[[F((i*7+j*3)%9-4,7) for j in range(d)] for i in range(k)]
 W=[[F((i*3+j*5)%7-2,5) for j in range(k)] for i in range(d)]
 O,H=orth(d,139),orth(d,177)
 Fc=add(mul(A,F0),mul(B,G));Pc=add(mul(R,P),mul(T,Q))
 C=add(mul(Ap,F0),mul(Bp,G))+J;D=add(mul(Rp,P),mul(Tp,Q))+K
 yc=add(mul(X,Fc),mul(mul(Y,O),C));zc=add(mul(tr(Z),Pc),mul(mul(tr(W),H),D))
 yo,hw=mul(Y,O),mul(tr(H),W);yb,yh=sub(yo,0,0,k,k),sub(yo,0,k,k,d-k);wb,wh=hw[:k],hw[k:]
 da=mul(mul(tr(T),yc),tr(F0));dd=mul(mul(tr(T),yc),tr(G));ad=mul(mul(P,tr(zc)),B)
 assert da==mul(tr(T),add(mul(X,A),mul(yb,Ap)))
 assert dd==mul(tr(T),add(mul(X,B),mul(yb,Bp)))
 assert ad==mul(add(mul(tr(R),Z),mul(tr(Rp),wb)),B)
 yn=add(mul(tr(R),yc),mul(ad,G),-1);zn=add(mul(tr(A),zc),mul(tr(da),Q),-1)
 xp=add(mul(mul(tr(R),X),A),mul(mul(tr(R),yb),Ap))
 zp=add(mul(mul(tr(R),Z),A),mul(mul(tr(Rp),wb),A))
 v=add(X,Z,-1)
 yp=add(add(mul(mul(tr(R),v),B),mul(mul(tr(R),yb),Bp)),mul(mul(tr(Rp),wb),B),-1)
 wp=add(add(scale(mul(mul(tr(T),v),A),-1),mul(mul(tr(Tp),wb),A)),mul(mul(tr(T),yb),Ap),-1)
 assert mul(yn,tr(F0))==xp and tr(mul(zn,tr(P)))==zp
 assert mul(yn,tr(G))==yp and tr(mul(zn,tr(Q)))==wp
 yrest,wrest=mul(tr(R),yh),mul(wh,A)
 assert mul(yn,tr(J))==yrest and tr(mul(zn,tr(K)))==wrest
 lam=add(add(mul(mul(tr(T),v),B),mul(mul(tr(T),yb),Bp)),mul(mul(tr(Tp),wb),B),-1)
 before=norm(v)+norm(Y)+norm(W);after=norm(add(xp,zp,-1))+norm(yp)+norm(yrest)+norm(wp)+norm(wrest)
 loss=norm(lam)+norm(mul(tr(T),yh))+norm(mul(wh,B))
 assert before-after==loss
 # Exact second moments suffice for the corner cone counterexample.
 S=[[F(1),F(0)],[F(0),F(0)]];EX=scale(S,F(5,4));EY=scale(S,F(3,4))
 assert add(EY,EX,-1)==scale(S,F(-1,2))
 report=dict(status='EXACT_FRACTION_PASS',k=k,width=s,physical_recursion=True,pointwise_flux_identity=True,flux_loss=str(loss),naive_row_covariance_cone_minimum_defect='-1/2',scope='Algebra control; not a general-k stability theorem')
 print(json.dumps(report,indent=2));open('matrix_branch_flux_exact_results.json','w').write(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
