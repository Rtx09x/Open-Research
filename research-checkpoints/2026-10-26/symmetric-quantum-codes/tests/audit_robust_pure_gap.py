"""Independent short-dual and robust-gap rational replay."""
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
E=[unit(0),[F(1)]*N]+H[1:5]+[unit(r)for r in range(1,5)]+[[(M[r][k]-int(r==k))*scale[k]for k in range(N)]for r in [1,3]]
Q=[unit(r)for r in range(N)]+H[5:];b=[F(1),F(N,2)]+[F(0)]*(len(E)-2)
c=json.loads((ROOT/'pure_complement_short_certificate.json').read_text());y=list(map(F,c['y']));z=list(map(F,c['z']))
assert min(z)>=0 and sum(a*v for a,v in zip(b,y))==-1
assert all(sum(y[i]*E[i][k]for i in range(len(E)))==sum(z[i]*Q[i][k]for i in range(len(Q)))for k in range(N))
cs=list(map(F,['91/285','288199/1187025','33176/237405','10120/142443']))
A=N*max([F(0)]+[a/v for a,v in zip(y[6:10],cs)])
w=max(abs(sum(v*(M[r][k]-int(r==k))for v,r in zip(y[10:],[1,3])))for k in range(N))
nu=F(1,10**8);q=F(1,10**4);bound=A*nu+N*w*(3*N*q+2*N*N*nu)
d=json.loads((ROOT/'robust_pure_gap_certificate.json').read_text());assert A==F(d['A']) and w==F(d['w']) and bound==F(d['rational_upper_at_test']) and bound<1
out={'exact':True,'short_Farkas_identity':True,'analytic_argument':'HS self-adjoint twirl norm; rank-one Q MacWilliams identity; ||R-Q||F²=2N²nu; triangle/Cauchy-Schwarz','A_matches':True,'w_matches':True,'contradiction_bound':str(bound),'necessary_strict_variance_lower_bound':str(nu),'scope':'unrestricted hypothetical n18 code; weak structural bound, not exclusion; novelty unconfirmed'}
Path(__file__).with_name('robust_pure_gap_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
