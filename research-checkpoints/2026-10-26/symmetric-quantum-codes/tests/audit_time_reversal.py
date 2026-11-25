"""Exact independent hypergeometric replay of restricted parity certificate."""
from fractions import Fraction as F
import json
from pathlib import Path
n=18;N=n+1
M=[]
for r in range(N):
 row=[]
 for k in range(N):
  term=F(1); total=term
  for ell in range(min(r,k)):
   term*=F((ell-r)*(r+1+ell)*(ell-k)*(k+1+ell),(ell+1)**2*(ell-n)*(n+2+ell)); total+=term
  row.append(F(2*r+1,N)*total)
 M.append(row)
H=[[2*M[r][k]-int(r==k) for k in range(N)] for r in range(N)]
unit=lambda r:[F(r==k)for k in range(N)]
E=[unit(0),[F(1)]*N]+H[1:5]+[unit(r) for r in range(1,N,2)]
b=[F(1),F(N,2)]+[F(0)]*(len(E)-2)
Q=[unit(r)for r in range(N)]+H[5:]
d=json.load(open(Path(__file__).resolve().parents[1]/'time_reversal_certificate.json'));y=list(map(F,d['y']));z=list(map(F,d['z']))
assert len(y)==len(E) and len(z)==len(Q) and min(z)>=0
assert all(sum(y[i]*E[i][k]for i in range(len(E)))==sum(z[i]*Q[i][k]for i in range(len(Q))) for k in range(N))
assert sum(x*v for x,v in zip(b,y))==-1
odd_min=1/max(y[6:]);overlap_max=2-F(8,19)*odd_min
out={'exact':True,'method':'stdlib Fraction terminating hypergeometric transform','scope':'time-reversal-invariant code projector only; NOT real-Dicke amplitudes','necessary_weighted_odd_moment_lower_bound':'1','odd_moment_sum_lower_bound':str(odd_min),'time_reversal_overlap_upper_bound':str(overlap_max)}
Path(__file__).with_name('time_reversal_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
