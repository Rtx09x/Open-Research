#!/usr/bin/env python3
"""Independent terminating4F3 construction of SU(2) transform, Fraction only."""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib,time
src=Path(__file__).resolve().parents[2]/'symmetric-quantum-codes'/'phase3'/'scalar_exact_t3.json'

def entry(n,r,k):
 term=F(1);s=term
 for l in range(min(r,k)):
  term*=F((l-r)*(l+r+1)*(l-k)*(l+k+1),(l+1)**2*(l-n)*(l+n+2));s+=term
 return F(2*r+1,n+1)*s

start=time.monotonic();out=[]
for c in json.loads(src.read_text()):
 n=c['n'];m=n+1;d=c['d'];assert c['t']==3 and d==7 and c['K']==2
 M=[[entry(n,r,k) for k in range(m)] for r in range(m)]
 I=[[F(r==k) for k in range(m)] for r in range(m)]
 H=[[2*M[r][k]-I[r][k] for k in range(m)] for r in range(m)]
 E=[I[0],[F(1)]*m]+H[1:d]
 G=I+H[d:]+[[M[r][k]*(-1)**k for k in range(m)] for r in range(m)]
 rhs=[F(1),F(m,2)]+[F(0)]*(d-1)
 y=list(map(F,c['y']));z=list(map(F,c['z']))
 assert len(y)==len(E) and len(z)==len(G) and min(z)>=0
 assert sum(v*w for v,w in zip(rhs,y))==-1
 residual=[sum(y[i]*E[i][k] for i in range(len(E)))-sum(z[i]*G[i][k] for i in range(len(G))) for k in range(m)]
 assert not any(residual)
 # Independent low-rank normalization checks of the transform.
 assert all(v==F(1,m) for v in M[0])
 assert all(M[r][0]==F(2*r+1,m) for r in range(m))
 assert all(sum(M[r][k]*M[k][s] for k in range(m))==F(r==s) for r in [0,1,n] for s in [0,1,n])
 out.append({'n':n,'t':3,'exact_Farkas':'PASS','rhs_dot_y':'-1','positive_dual_terms':sum(v>0 for v in z)})
result={'status':'PASS','matrix_method':'terminating rational4F3, no worker/SymPy imports','certificate_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'results':out,'seconds':time.monotonic()-start,'applicability':'Uses intrinsic LP plus time-reversal cross-enumerator positivity; no nondegeneracy assumption. Novelty separate.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
