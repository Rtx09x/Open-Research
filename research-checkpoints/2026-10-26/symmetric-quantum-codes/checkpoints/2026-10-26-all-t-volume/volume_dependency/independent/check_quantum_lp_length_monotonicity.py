"""Independent Fraction controls of Manes et al.2610.00561v1 §VIII.2.
These controls supplement the all-n source algebra, not replace its proof.
"""
from fractions import Fraction as F
from math import factorial as fac
from pathlib import Path
import json,time,hashlib
start=time.monotonic()
def M(n):
 out=[]
 for r in range(n+1):
  row=[]
  for k in range(n+1):
   a=s=F(1)
   for l in range(min(r,k)):
    a*=F((l-r)*(l+r+1)*(l-k)*(l+k+1),(l+1)**2*(l-n)*(l+n+2));s+=a
   row.append(F(2*r+1,n+1)*s)
  out.append(row)
 return out
def T(n):
 return [[F(0) if l<k else F((n+1-k)*(n+2*k+2),(n+2)*(n+k+2)) if l==k else F((2*l+1)*(n+2+2*k*(k+1))*fac(n-k)*fac(n+k+1),(n+2)*fac(n+1-l)*fac(n+l+2)) for k in range(n+1)] for l in range(n+2)]
results=[]
A=M(0)
for n in range(25):
 B=M(n+1);C=T(n)
 assert all(v>=0 for row in C for v in row)
 assert all(sum(row[k] for row in C)==1 for k in range(n+1))
 assert C[0][0]==F(n+1,n+2) and all(C[0][k]==0 for k in range(1,n+1))
 assert all(sum(B[i][j]*C[j][k] for j in range(n+2))==sum(C[i][j]*A[j][k] for j in range(n+1)) for i in range(n+2) for k in range(n+1))
 results.append(n);A=B
out={'passed':True,'length_steps_checked':results,'includes_both_spin_parities':True,'ordinary_LP_only':True,'source':'https://arxiv.org/html/2610.00561v1#S8.SS2','normalization':'For a0=1,sum a=(n+1)/K use a_prime=((n+2)/(n+1))*T_n*a; low-rank equalities preserved by lower-triangularity. No physical-code padding and no shadow transport asserted.','seconds':time.monotonic()-start}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
