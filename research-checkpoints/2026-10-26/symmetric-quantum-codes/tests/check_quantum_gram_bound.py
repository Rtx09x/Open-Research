"""Independent rational audit of the n=18 Gram LP dual certificate.
No worker code, optimizer or symbolic-math dependency. Does not prove the
representation-theoretic Gram formula or originality of the lemma.
"""
from fractions import Fraction as Q
from math import factorial as f
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def delta2(a,b,c):
 return Q(f(a+b-c)*f(a-b+c)*f(-a+b+c),f(a+b+c+1))
def sixj_squared(a,b,c,d,e,g):
 lo=max(a+b+c,a+e+g,d+b+g,d+e+c)
 hi=min(a+b+d+e,b+c+e+g,a+c+d+g)
 total=sum((Q((-1)**z*f(z+1),f(z-a-b-c)*f(z-a-e-g)*f(z-d-b-g)*f(z-d-e-c)*f(a+b+d+e-z)*f(b+c+e+g-z)*f(a+c+d+g-z)) for z in range(lo,hi+1)),Q(0))
 return delta2(a,b,c)*delta2(a,e,g)*delta2(d,b,g)*delta2(d,e,c)*total**2
def equal_sixj(n,r,k):
 return Q(f(n-r)*f(r)**2,f(n+r+1))*Q(f(n-k)*f(k)**2,f(n+k+1))*sum((Q((-1)**z*f(z+1),f(z-n-r)**2*f(z-n-k)**2*f(2*n-z)*f(n+r+k-z)**2) for z in range(max(n+r,n+k),min(2*n,n+r+k)+1)),Q(0))
c=json.loads((ROOT/'gram_bound_exact_certificate.json').read_text())
n=18; N=19;d=5
coeff=[]
for r in range(5):
 coeff.append(sum(((2*a+1)*(2*b+1)*sixj_squared(a,b,r,9,9,9) for a in range(3) for b in range(3) if abs(a-b)<=r<=a+b),Q(0)))
assert coeff==list(map(Q,c['c']))
I=[[Q(int(r==k)) for k in range(N)] for r in range(N)]
H=[[2*(-1)**(n+r+k)*(2*r+1)*equal_sixj(n,r,k)-I[r][k] for k in range(N)] for r in range(N)]
A=[I[0],[Q(1)]*N]+H[1:d]; b=[Q(1),Q(N,2)]+[Q(0)]*4; G=I+H[d:]
y=list(map(Q,c['y']));z=list(map(Q,c['z']));obj=[Q(0)]+[v/N for v in coeff[1:]]+[Q(0)]*14
assert obj==list(map(Q,c['variance_objective']))
assert all(t>=0 for t in z)
assert all(sum(A[i][j]*y[i] for i in range(len(y)))-sum(G[i][j]*z[i] for i in range(len(z)))==obj[j] for j in range(N))
upper=sum(bi*yi for bi,yi in zip(b,y))
assert upper==Q(1,722) and upper<Q(1,N*N)
result={'coefficients':[str(x) for x in coeff],'dual_certificate':'exactly verified','upper_bound':str(upper),'strictly_below_singular_threshold':True,'limitations':'Representation identity and scientific novelty require separate audit.'}
(ROOT/'tests/quantum_gram_independent_replay.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
