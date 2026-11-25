"""Fraction-only physical Gram, exact recovery, and all256 sign-gauge control."""
from fractions import Fraction as F
from itertools import product
import json


def dot(a,b):return sum(x*y for x,y in zip(a,b))
def inverse(a):
 n=len(a);x=[list(row)+[F(i==j) for j in range(n)] for i,row in enumerate(a)]
 for i in range(n):
  h=next(h for h in range(i,n) if x[h][i]);x[i],x[h]=x[h],x[i]
  z=x[i][i];x[i]=[v/z for v in x[i]]
  for h in range(n):
   if h!=i:
    z=x[h][i];x[h]=[v-z*w for v,w in zip(x[h],x[i])]
 return [r[n:] for r in x]


def main():
 n=4;supp=[(i,i) for i in range(n)]+[(i,i+1) for i in range(n-1)]+[(i+1,i) for i in range(n-1)]
 om=[[F(1),0,0,0,0],[0,F(1),0,0,0],[F(3,5),0,F(4,5),0,0],[0,F(3,5),0,F(4,5),0]]
 ps=[[F(1),0,0,0,0],[0,F(1),0,0,0],[F(5,13),0,0,0,F(12,13)],[0,F(8,17),0,F(15,17),0]]
 for bank in [om,ps]:
  assert all(dot(r,r)==1 for r in bank)
  assert all(dot(bank[i],bank[i+1])==0 for i in range(n-1))
 raw=[[F(i==a)*dot(om[j],om[b])+F(j==b)*dot(ps[i],ps[a]) for i in range(n) for j in range(n)] for a,b in supp]
 gram=[[r[i*n+j] for i,j in supp] for r in raw];inv=inverse(gram)
 dec=[[sum(inv[a][h]*raw[h][t] for h in range(len(supp))) for t in range(n*n)] for a in range(len(supp))]
 assert all(dec[a][i*n+j]==F(a==b) for a in range(len(supp)) for b,(i,j) in enumerate(supp))
 residual=[F(0) if (i,j) in supp else F(2*i-j+1) for i in range(n) for j in range(n)]
 diagonal=sum(residual[t]**2*sum(row[t]**2 for row in dec) for t in range(n*n))
 total=F(0)
 for signs in product([-1,1],repeat=2*n):
  source=[residual[i*n+j]*signs[i]*signs[n+j] for i in range(n) for j in range(n)]
  total+=sum(dot(row,source)**2 for row in dec)
 assert total/F(2**(2*n))==diagonal
 assert all(sum(raw[a][i*n+j]!=0 for a in range(len(supp)))<=6 for i in range(n) for j in range(n) if (i,j) not in supp)
 result=dict(status='EXACT_FRACTION_PASS',n=n,width=5,coefficient_count=len(supp),sign_gauges=2**(2*n),exact_gauge_average=str(diagonal),scope='Finite algebra control; not the continuous inverse-moment proof')
 print(json.dumps(result,indent=2));open('path_ls_gauge_exact_results.json','w').write(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
