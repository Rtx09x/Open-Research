"""Exact conservative pricing for disjoint-successor two-cutoff chronology charges.

Envelope sums the separate maxima of the step and overflow-excess terms.
It is an upper bound, not an assertion that both maxima are jointly attained.
"""
from fractions import Fraction as Q
import math
D=Q(1,43)

def coefficients(P,B,b,c,g,q):
    assert 0<=c<=g<=D and q>=0
    kappa=sum(alpha*max(Q(0),1-q*(A-g)) for A,alpha in P[212]['a'].items())
    denominator=B-c-(g-c)*kappa
    assert denominator>=B-g>0
    rho=b/denominator
    return rho,rho*(g-c)*q,rho*(1+(g-c)*q)

def terms(P,B,b,mix):
    return [(c,g,*(weight*t for t in coefficients(P,B,b,c,g,q))) for c,g,q,weight in mix if weight]

def step(r,c):
    if c==0:return r
    if c==D:return Q(0)
    z=r/c;n=-(-z.numerator//z.denominator)-1
    return min(r,n*D)

def hinge(r,g):
    n=r//D;return n*(D-g)+max(Q(0),r-n*D-g)

def envelope(P,B,b,r,mix):
    return sum(rho*r+extra*step(r,c)+excess*hinge(r,g) for c,g,rho,extra,excess in terms(P,B,b,mix))

def price(items,cap,P,B,b,mix,offset):
    ts=terms(P,B,b,mix);rho=sum(z[2] for z in ts)
    S=math.lcm(cap.denominator,D.denominator,*[v.denominator for z in ts for v in z[:2]],*[s.denominator for j,s,w in items])
    W=math.lcm(rho.denominator,*[v.denominator for z in ts for v in z[3:]],*[w.denominator for j,s,w in items])
    C=int(cap*S);dd=int(D*S);aa=int(rho*W)
    TS=[(int(c*S),int(extra*W)) for c,g,r,extra,e in ts if extra and c<D]
    HS=[(int(g*S),int(e*W)) for c,g,r,extra,e in ts if e and g<D]
    raw=[]
    for j,s,w in items:
        size=int(s*S);gain=int(w*W)*S-aa*size
        if 0<size<C and gain>0:raw.append((j,size,gain))
    keep=[t for t in raw if not any(u[1]<=t[1] and u[2]>=t[2] and(u[1]<t[1] or u[2]>t[2] or u[0]<t[0]) for u in raw)]
    keep.sort(key=lambda t:Q(t[2],t[1]),reverse=True)
    def bonus(r):
        n,rem=divmod(r,dd)
        return sum(e*(r if not c else min(r,dd*((r-1)//c))) for c,e in TS)+sum(e*(n*(dd-g)+max(0,rem-g)) for g,e in HS)
    density=sum(e for c,e in TS)+sum(Q(e*(dd-g),dd) for g,e in HS)
    best=bonus(C);bestpat=[];nodes=0;path=[]
    def visit(i,space,value):
        nonlocal best,bestpat,nodes
        nodes+=1;v=value+bonus(space)
        if v>best:best=v;bestpat=path.copy()
        if i==len(keep):return
        j,size,gain=keep[i];bound=max(Q(gain,size),density)
        if value*bound.denominator+space*bound.numerator<=best*bound.denominator:return
        for n in range((space-1)//size,-1,-1):
            if n:path.append((j,n))
            visit(i+1,space-n*size,value+n*gain)
            if n:path.pop()
    visit(0,C,0)
    return Q(aa*C+best,W*S)+offset,tuple(sorted(bestpat)),nodes
