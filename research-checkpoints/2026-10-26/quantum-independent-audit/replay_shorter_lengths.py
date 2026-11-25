"""Independent rational certificate replay: no optimizer, SymPy, or worker imports.
Checks algebraic certificates only; applicability of constraints needs theorem review.
"""
from fractions import Fraction as Q
from math import factorial as f
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def racah(n,r,k):
    pref=Q(f(n-r)*f(r)**2,f(n+r+1))*Q(f(n-k)*f(k)**2,f(n+k+1))
    s=sum((Q((-1)**z*f(z+1),f(z-n-r)**2*f(z-n-k)**2*f(2*n-z)*f(n+r+k-z)**2) for z in range(max(n+r,n+k),min(2*n,n+r+k)+1)),Q(0))
    return pref*s
results=[]
for c in json.loads((ROOT/'symmetric-quantum-codes/lp_exact_certificates.json').read_text()):
    n,d=c['n'],c['d']; m=n+1
    I=[[Q(int(r==k)) for k in range(m)] for r in range(m)]
    M=[[(-1)**(n+r+k)*(2*r+1)*racah(n,r,k) for k in range(m)] for r in range(m)]
    H=[[2*M[r][k]-I[r][k] for k in range(m)] for r in range(m)]
    A=[I[0],[Q(1)]*m]+H[1:d]; b=[Q(1),Q(m,2)]+[Q(0)]*(d-1)
    G=I+H[d:]; y=list(map(Q,c['y'])); z=list(map(Q,c['z']))
    assert len(y)==len(A) and len(z)==len(G)
    assert all(v>=0 for v in z)
    assert sum(a*v for a,v in zip(b,y))==-1
    assert all(sum(A[i][j]*y[i] for i in range(len(y)))==sum(G[i][j]*z[i] for i in range(len(z))) for j in range(m))
    results.append({'n':n,'d':d,'exact_farkas_valid':True})
print(json.dumps(results,indent=2))
(ROOT/'quantum-independent-audit/shorter_lengths_exact_replay.json').write_text(json.dumps({'scope':'Exact rational algebra only; theorem applicability and novelty separately audited','results':results},indent=2))
