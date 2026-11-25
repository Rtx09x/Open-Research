"""Direct small-spin Clebsch-Gordan audit of a proposed crossing formula."""
import json
from pathlib import Path
import sympy as s
from sympy.physics.wigner import clebsch_gordan,wigner_6j

def ms(j):return [j*(-1)+i for i in range(int(2*j+1))]
def E(j,L,Lp,J):
 return s.Matrix((2*L+1)*int(2*j+1),(2*Lp+1)*int(2*j+1),lambda a,b:sum(clebsch_gordan(L,j,J,ms(L)[a//int(2*j+1)],ms(j)[a%int(2*j+1)],M)*clebsch_gordan(Lp,j,J,ms(Lp)[b//int(2*j+1)],ms(j)[b%int(2*j+1)],M)for M in ms(J)))
def cross(j,L,Lp,J,K):
 nj=int(2*j+1);A=E(j,L,Lp,J);B=E(j,Lp,L,K);At=s.zeros(A.rows,A.cols)
 for a in range(A.rows):
  for b in range(A.cols):
   aa,ma=divmod(a,nj);bb,mb=divmod(b,nj);At[a,b]=(-1)**int(2*j-ms(j)[ma]-ms(j)[mb])*A[aa*nj+(nj-1-mb),bb*nj+(nj-1-ma)]
 return s.simplify(s.trace(B*At)/(2*K+1))
rows=[]
for j,L,Lp in [(s.Rational(1,2),0,1),(1,0,1),(1,1,1),(1,1,2),(s.Rational(3,2),1,2)]:
 js=[abs(L-j)+i for i in range(int(2*min(L,j)+1))];ks=[J for J in js if abs(Lp-j)<=J<=Lp+j]
 for J in ks:
  for K in ks:
   direct=cross(j,L,Lp,J,K);pred=s.simplify((-1)**int(2*j)*(2*J+1)*wigner_6j(L,j,J,Lp,j,K));rows.append({'j':str(j),'L':L,'Lp':Lp,'J':str(J),'K':str(K),'direct':str(direct),'predicted':str(pred),'pass':s.simplify(direct-pred)==0})
print(rows);Path(__file__).with_suffix('.json').write_text(json.dumps(rows,indent=2));assert all(r['pass']for r in rows)
