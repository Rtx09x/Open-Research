"""Independent exact pair-twirl/enumerator normalization controls."""
from fractions import Fraction as F
from math import factorial as f
from pathlib import Path
import json,time
start=time.time();out=[]
def mac(n,L,r):
 total=F(0)
 for k in range(min(L,r)+1):total+=(-1)**k*F(f(L+k)*f(r+k)*f(n-k)*f(n+1),f(L-k)*f(r-k)*f(k)**2*f(n)*f(n+k+1))
 return F(2*L+1,n+1)*total
for n in (2,3,6,18,19):
 # Diagonal tensor sectors are normalized discrete orthogonal polynomials.
 polynomials=[]
 for r in range(n+1):
  v=[F(w**r)for w in range(n+1)]
  for p in polynomials:
   coeff=sum(a*b for a,b in zip(v,p))/sum(a*a for a in p)
   v=[a-coeff*b for a,b in zip(v,p)]
  polynomials.append(v)
 a=[F(n+1,4)*(p[-1]+p[-2])**2/sum(x*x for x in p)for p in polynomials]
 assert a[0]==1 and sum(a)==F(n+1,2)
 t=[F(4,n+1)*sum((-1)**r*mac(n,L,r)*a[r]for r in range(n+1))for L in range(n+1)]
 # Direct Clebsch-Gordan highest-weight calculation for P=|n><n|+|n-1><n-1|.
 expected=[F(0)]*(n+1);expected[n]=2+F(n,2*n-1);expected[n-1]=1;expected[n-2]=F(n-1,2*n-1)
 assert t==expected and sum(t)==4 and sum((-1)**(n-L)*t[L]for L in range(n+1))==2
 out.append({'n':n,'nonzero_pair_spin_weights':[[L,str(v)]for L,v in enumerate(t)if v]})
report={'status':'PASS','controls':out,'seconds':time.time()-start,'scope':'pair-spin transform normalization for exact rank2 noncode projectors; not a three-copy SDP feasibility result'}
Path(__file__).with_name('three_copy_pair_map_checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
