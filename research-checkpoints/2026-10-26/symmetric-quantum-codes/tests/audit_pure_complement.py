"""Replay pure-subcase affine elimination using stdlib rational hypergeometric M."""
from fractions import Fraction as F
import json
from pathlib import Path
n=18;N=n+1
M=[]
for r in range(N):
 row=[]
 for k in range(N):
  term=F(1);total=term
  for l in range(min(r,k)):
   term*=F((l-r)*(r+1+l)*(l-k)*(k+1+l),(l+1)**2*(l-n)*(n+2+l));total+=term
  row.append(F(2*r+1,N)*total)
 M.append(row)
H=[[2*M[r][k]-(r==k)for k in range(N)]for r in range(N)]
def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
d=json.load(open(Path(__file__).resolve().parents[1]/'pure_complement_elimination.json'));p=list(map(F,d['p']));v=list(map(F,d['v']))
t=[sum(M[a][r]for a in range(3))for r in range(N)];scale=[F(1)]+[4*N*N*t[r]**2 for r in range(1,N)]
assert p[0]==1 and v[0]==0 and sum(p)==F(N,2) and sum(v)==0
assert all(p[r]==v[r]==0 for r in range(1,5))
assert all(dot(H[r],p)==dot(H[r],v)==0 for r in range(1,5))
for x in [p,v]:
 b=[scale[i]*x[i] for i in range(N)]
 assert all(dot(M[r],b)==b[r] for r in range(N))
lower=-p[8]/v[8];upper=-dot(H[8],p)/dot(H[8],v)
assert v[8]>0 and dot(H[8],v)<0 and lower>upper
# Sufficiency of affine parametrization requires full equality rank18.
rows=[[F(r==k) for k in range(N)]for r in [0]]+[[F(1)]*N]+H[1:5]+[[F(r==k)for k in range(N)]for r in range(1,5)]+[[(M[r][k]-(r==k))*scale[k]for k in range(N)]for r in range(N)]
rank=0
for c in range(N):
 pivot=next((i for i in range(rank,len(rows)) if rows[i][c]),None)
 if pivot is None:continue
 rows[rank],rows[pivot]=rows[pivot],rows[rank]
 div=rows[rank][c];rows[rank]=[x/div for x in rows[rank]]
 for i in range(rank+1,len(rows)):
  if rows[i][c]:
   div=rows[i][c];rows[i]=[x-div*y for x,y in zip(rows[i],rows[rank])]
 rank+=1
assert rank==18
out={'exact':True,'method':'stdlib Fraction terminating hypergeometric transform; independent affine and rank verification','equality_rank':rank,'lower':str(lower),'upper':str(upper),'lower_exceeds_upper':True,'scope':'n18,d5,K2 with a1=a2=a3=a4=0 only'}
print(json.dumps(out,indent=2))
