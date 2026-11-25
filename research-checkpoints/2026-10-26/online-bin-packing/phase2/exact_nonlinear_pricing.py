"""Exact standard-library nonlinear pricing extracted from the authored phase-2 oracle."""
from fractions import Fraction as Q
import math
D=Q(1,43)

def tiny_parameters(P,s):
 x,y,w=Q(s['x']),Q(s['y']),Q(s['w']);B=b=Q(0)
 for v,a in P[212]['a'].items():
  B+=v*a
  rw=(Q(1) if v>=1-x else w) if v>Q(1,2) else (1-w if v<=x else Q(1))
  b+=a*rw
 return B,b

def price(items,cap,B,b,mix,offset):
 terms=[(c,z*b/(B-c)) for c,z in mix if z and c<D]
 a=sum(z*b/(B-c) for c,z in mix)
 S=math.lcm(cap.denominator,D.denominator,*[c.denominator for c,z in terms],*[s.denominator for j,s,w in items])
 W=math.lcm(a.denominator,*[z.denominator for c,z in terms],*[w.denominator for j,s,w in items])
 C=int(cap*S);dd=int(D*S);aa=int(a*W);T=[(int(c*S),int(z*W)) for c,z in terms]
 raw=[]
 for j,s,w in items:
  size=int(s*S);g=int(w*W)*S-aa*size
  if 0<size<C and g>0:raw.append((j,size,g))
 keep=[t for t in raw if not any(u[1]<=t[1] and u[2]>=t[2] and(u[1]<t[1] or u[2]>t[2] or u[0]<t[0]) for u in raw)]
 keep.sort(key=lambda t:Q(t[2],t[1]),reverse=True)
 def hinge(space):
  q,e=divmod(space,dd);return sum(z*(q*(dd-c)+max(0,e-c)) for c,z in T)
 extra_density=sum(Q(z*(dd-c),dd) for c,z in T);best=hinge(C);bestpat=[];nodes=0;path=[]
 def visit(i,space,value):
  nonlocal best,bestpat,nodes
  nodes+=1;v=value+hinge(space)
  if v>best:best=v;bestpat=path.copy()
  if i==len(keep):return
  j,size,gain=keep[i];bound=max(Q(gain,size),extra_density)
  if value*bound.denominator+space*bound.numerator<=best*bound.denominator:return
  for n in range((space-1)//size,-1,-1):
   if n:path.append((j,n))
   visit(i+1,space-n*size,value+n*gain)
   if n:path.pop()
 visit(0,C,0)
 return Q(aa*C+best,W*S)+offset,tuple(sorted(bestpat)),nodes
