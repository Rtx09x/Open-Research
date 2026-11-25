"""Exact maximization of a valid convex sum of step-fill upper envelopes."""
from fractions import Fraction as Q
import math
from type_pricing import coefficients,D

def components(P,B,b,mix):
    return [(c,weight*coefficients(P,B,b,c,q)[0],weight*coefficients(P,B,b,c,q)[1]) for c,q,weight in mix if weight]

def fill(r,c):
    if c==D:return Q(0)
    z=r/c;n=-(-z.numerator//z.denominator)-1
    return min(r,n*D)

def envelope(P,B,b,r,mix):
    return sum(rho*r+extra*fill(r,c) for c,rho,extra in components(P,B,b,mix))

def price(items,cap,P,B,b,mix,offset):
    terms=components(P,B,b,mix);rho=sum(r for c,r,e in terms)
    S=math.lcm(cap.denominator,D.denominator,*[c.denominator for c,r,e in terms],*[s.denominator for j,s,w in items])
    W=math.lcm(rho.denominator,*[e.denominator for c,r,e in terms],*[w.denominator for j,s,w in items])
    C=int(cap*S);dd=int(D*S);aa=int(rho*W)
    TS=[(int(c*S),int(e*W)) for c,r,e in terms if c<D]
    raw=[]
    for j,s,w in items:
        size=int(s*S);gain=int(w*W)*S-aa*size
        if 0<size<C and gain>0:raw.append((j,size,gain))
    keep=[t for t in raw if not any(u[1]<=t[1] and u[2]>=t[2] and(u[1]<t[1] or u[2]>t[2] or u[0]<t[0]) for u in raw)]
    keep.sort(key=lambda t:Q(t[2],t[1]),reverse=True)
    def bonus(r):return sum(e*min(r,dd*((r-1)//c)) for c,e in TS)
    density=sum(e for c,e in TS);best=bonus(C);bestpat=[];nodes=0;path=[]
    def visit(i,space,value):
        nonlocal best,bestpat,nodes
        nodes+=1;v=value+bonus(space)
        if v>best:best=v;bestpat=path.copy()
        if i==len(keep):return
        j,size,gain=keep[i];bound=max(Q(gain,size),Q(density))
        if value*bound.denominator+space*bound.numerator<=best*bound.denominator:return
        for n in range((space-1)//size,-1,-1):
            if n:path.append((j,n))
            visit(i+1,space-n*size,value+n*gain)
            if n:path.pop()
    visit(0,C,0)
    return Q(aa*C+best,W*S)+offset,tuple(sorted(bestpat)),nodes
