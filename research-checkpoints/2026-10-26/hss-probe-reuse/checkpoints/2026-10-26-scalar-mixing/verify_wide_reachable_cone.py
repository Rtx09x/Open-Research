"""Exact full-orientation moment controls and reachable-cone telescoping."""
from fractions import Fraction as F
from itertools import permutations,product
import random,json


def dot(x,y):return sum(a*b for a,b in zip(x,y))
def orientations(v):
 for p in permutations(range(len(v))):
  for signs in product([-1,1],repeat=len(v)):yield [v[p[i]]*signs[i] for i in range(len(v))]
def step(X,Z,U,W,p,q,d):
 return ((1-p)*(1-q)*X+(1-p)*q*U/d,
 (1-p)*(1-q)*Z+(1-q)*p*W/d,
 (1-p)*q*(X+Z)+(1-p)*(1-q/d)*U+p*q*W/d,
 (1-q)*p*(X+Z)+(1-q)*(1-p/d)*W+p*q*U/d)
def cost(X,Z,U,W,p,q,d):return p*X+p*U/d+q*(1-p)*Z+p*q*W/d


def physical(d,r,t,a,b,x,z,u,w):
 fc=[a,b]+[F(0)]*(d-1);pc=[r,t]+[F(0)]*(d-1)
 c=[[-b,a]+[F(0)]*(d-1)]+[[F(j==i) for j in range(d+1)] for i in range(2,d+1)]
 h=[[-t,r]+[F(0)]*(d-1)]+[[F(j==i) for j in range(d+1)] for i in range(2,d+1)]
 sums=[F(0)]*6;count=0
 for uu in orientations(u):
  y=[x*fc[j]+sum(uu[i]*c[i][j] for i in range(d)) for j in range(d+1)]
  for ww in orientations(w):
   zz=[z*pc[j]+sum(ww[i]*h[i][j] for i in range(d)) for j in range(d+1)]
   da,dd,ad=t*y[0],t*y[1],b*zz[0]
   yn=[r*yy-ad*F(j==1) for j,yy in enumerate(y)];zn=[a*vv-da*F(j==1) for j,vv in enumerate(zz)]
   vals=[yn[0]**2,zn[0]**2,dot(yn,yn)-yn[0]**2,dot(zn,zn)-zn[0]**2,yn[0]*zn[0],da**2+dd**2+ad**2]
   sums=[v+w for v,w in zip(sums,vals)];count+=1
 return [v/count for v in sums],count


def main():
 controls=[]
 for d in [2,3]:
  for r,t,a,b in [(F(3,5),F(4,5),F(5,13),F(12,13)),(F(1),F(0),F(0),F(1)),(F(0),F(1),F(1),F(0))]:
   x,z=F(1),F(0);u=[F(i+1) for i in range(d)];w=[F(2*i-1) for i in range(d)];p,q=t*t,b*b
   got,n=physical(d,r,t,a,b,x,z,u,w);v=(x*x,z*z,dot(u,u),dot(w,w));expected=list(step(*v,p,q,d))+[F(0),cost(*v,p,q,d)]
   assert got==expected;controls.append(dict(d=d,p=str(p),q=str(q),exact_orientation_pairs=n))
 rng=random.Random(8934);cones=[]
 for d in range(2,7):
  C=F(2*d-1,(d-1)**2)
  for bank in ['U','W']:
   v=(F(0),F(0),F(bank=='U'),F(bank=='W'));total=F(0)
   for ell in range(120):
    p=rng.choice([F(0),F(1),F(9,25),F(25,169)]);q=rng.choice([F(0),F(1),F(9,25),F(25,169)])
    nv=step(*v,p,q,d);e=cost(*v,p,q,d);assert e<=C*(sum(v)-sum(nv));assert (d-1)*nv[0]<=nv[2] and (d-1)*nv[1]<=nv[3];total+=e;v=nv
   assert total<=C;cones.append(dict(d=d,initial=bank,depth=120,total_energy_float=float(total),bound=str(C)))
 report=dict(status='EXACT_FRACTION_PASS_ABSTRACT_BRANCH',physical_moment_controls=controls,reachable_cones=cones,scope='Actual inverse-column boundary bridge remains separately checked')
 print(json.dumps(report,indent=2));open('wide_reachable_cone_results.json','w').write(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
