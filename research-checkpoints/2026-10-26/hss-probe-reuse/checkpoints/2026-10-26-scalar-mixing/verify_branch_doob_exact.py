"""Independent Fraction check of Doob innovations and common-mode invariance.
Finite d2 signed-permutation controls; analytic target uses Haar moments.
"""
from fractions import Fraction as F
from itertools import permutations,product
import json


def dot(a,b):return sum(x*y for x,y in zip(a,b))
def orientations(u):
 return [[u[p[i]]*sg[i] for i in range(2)] for p in permutations(range(2)) for sg in product([-1,1],repeat=2)]
def scale(a,v):return [a*x for x in v]
def add(x,y):return [a+b for a,b in zip(x,y)]
def mean(rows):return [sum(v)/len(rows) for v in zip(*rows)]
def step(state,ur,wr):
 x,z,u,w=state;r,t,a,b=F(3,5),F(4,5),F(5,13),F(12,13)
 alpha,beta=ur[0],wr[0]
 out=[t*(a*x-b*alpha),t*(b*x+a*alpha),b*(r*z-t*beta)]
 xp,zp=r*a*x-r*b*alpha,r*a*z-a*t*beta
 up=[r*b*(x-z)+r*a*alpha+b*t*beta,r*ur[1]]
 wp=[a*t*(z-x)+a*r*beta+t*b*alpha,a*wr[1]]
 return out,(xp,zp,up,wp)


def main():
 state=(F(3,8),F(-2,9),[F(1,2),F(1,3)],[F(2,5),F(-1,7)])
 x,z,u,w=state;r,t,a,b=F(3,5),F(4,5),F(5,13),F(12,13)
 h=[-t*b,t*a,F(0),-r*b,F(0)];g=[F(0),F(0),-b*t,F(0),F(0)]
 a0=(dot(u,u)*dot(h,h)+dot(w,w)*dot(g,g))/2
 groups=[];allrows=[];A=[];quadratic_variations=[]
 shifted=(x+F(7,11),z+F(7,11),u,w)
 for ur in orientations(u):
  for wr in orientations(w):
   out,nxt=step(state,ur,wr);xp,zp,up,wp=nxt
   rows=[out+[xp,v[0]] for v in orientations(up)]
   cond=mean(rows);groups.append((ur,wr,cond,rows,nxt));allrows+=rows
   _,ns=step(shifted,ur,wr)
   assert ns[2:]==nxt[2:] and ns[0]-ns[1]==xp-zp
   a1=dot(up,up)/2;assert a1==dot(ns[2],ns[2])/2
   A.append(a0+a1)
 m0=mean(allrows)
 assert m0==[t*a*x,t*b*x,b*r*z,r*a*x,F(0)]
 for ur,wr,cond,rows,nxt in groups:
  delta=[v-m for v,m in zip(cond,m0)]
  assert delta==add(scale(ur[0],h),scale(wr[0],g))
  rootd=[[v-m for v,m in zip(row,cond)] for row in rows]
  assert all(q[:4]==[F(0)]*4 for q in rootd)
  assert sum(dot(q,q) for q in rootd)/8==dot(nxt[2],nxt[2])/2
  quadratic_variations.extend([dot(delta,delta)+dot(q,q) for q in rootd])
 variance=sum(dot([v-m for v,m in zip(row,m0)],[v-m for v,m in zip(row,m0)]) for row in allrows)/len(allrows)
 assert variance==sum(A)/len(A)==sum(quadratic_variations)/len(quadratic_variations)
 report=dict(status='EXACT_FRACTION_PASS',d=2,boundary_assignments=64,root_assignments=8,
  total_paths=len(allrows),future_mean_passive_independent=True,
  doob_difference_linear_distinguished_components=True,
  predictable_variation_flux_only=True,variance_identity=True,
  scope='Finite algebra control; all-depth Haar theorem is analytic')
 print(json.dumps(report,indent=2));open('branch_doob_exact_results.json','w').write(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
