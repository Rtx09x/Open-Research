"""Independent optimized all-complement dual and robust-gap rational replay."""
from fractions import Fraction as F
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];N=19;n=18
M=[]
for r in range(N):
 row=[]
 for k in range(N):
  term=F(1);total=term
  for j in range(min(r,k)):
   term*=F((j-r)*(r+1+j)*(j-k)*(k+1+j),(j+1)**2*(j-n)*(n+2+j));total+=term
  row.append(F(2*r+1,N)*total)
 M.append(row)
unit=lambda r:[F(r==k)for k in range(N)]
H=[[2*M[r][k]-int(r==k)for k in range(N)]for r in range(N)]
t=[sum(M[a][r]for a in range(3))for r in range(N)];scale=[F(1)]+[4*N*N*t[r]**2 for r in range(1,N)]
E=[unit(0),[F(1)]*N]+H[1:5]+[unit(r)for r in range(1,5)]+[[(M[r][k]-int(r==k))*scale[k]for k in range(N)]for r in range(N)]
Q=[unit(r)for r in range(N)]+H[5:];b=[F(1),F(N,2)]+[F(0)]*(len(E)-2)
c=json.loads((ROOT/'optimized_robust_gap_certificate.json').read_text());y=list(map(F,c['y']));z=list(map(F,c['z']))
assert len(y)==len(E)==29 and len(z)==len(Q)==33
assert min(z)>=0 and sum(a*v for a,v in zip(b,y))==-1
assert all(sum(y[i]*E[i][k]for i in range(len(E)))==sum(z[i]*Q[i][k]for i in range(len(Q)))for k in range(N))
cs=list(map(F,['91/285','288199/1187025','33176/237405','10120/142443']))
A=N*max([F(0)]+[a/v for a,v in zip(y[6:10],cs)])
w=max(abs(sum(v*(M[r][k]-int(r==k))for v,r in zip(y[10:],range(N))))for k in range(N))
assert 0<=A<=F(c['A']) and 0<=w<=F(c['w'])
q=F(c['q']);nu=q*q;assert nu==F(c['strict_variance_lower_bound'])
bound=F(c['A'])*nu+N*F(c['w'])*(3*N*q+2*N*N*nu)
assert bound==F(c['rational_bound']) and bound<1
out={'exact':True,'all_complement_Farkas_identity':True,'dual_rows':29,'nonnegative_inequalities':33,'analytic_argument':'Previously audited HS self-adjoint twirl norm argument; conservative 2sqrt(2)<=3','constant_bounds_verified':True,'contradiction_bound':str(bound),'necessary_strict_variance_lower_bound':str(nu),'scope':'unrestricted hypothetical n18 code; structural lower bound, not exclusion; novelty unconfirmed'}
Path(__file__).with_name('optimized_robust_gap_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
