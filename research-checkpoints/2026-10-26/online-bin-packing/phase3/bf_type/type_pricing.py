"""Exact step pricing for the type-resolved high-gap conservation inequality."""
from fractions import Fraction as Q
import math
D=Q(1,43)

def coefficients(P,B,b,c,q):
    kappa=sum(alpha*max(Q(0),1-q*(A-D)) for A,alpha in P[212]['a'].items())
    denominator=B-c-(D-c)*kappa
    assert denominator>0
    rho=b/denominator;extra=rho*(D-c)*q
    return rho,extra,kappa

def price(items,cap,P,B,b,c,q,offset):
    assert 0<c<=D
    rho,extra,kappa=coefficients(P,B,b,c,q)
    S=math.lcm(cap.denominator,D.denominator,c.denominator,*[s.denominator for j,s,w in items])
    W=math.lcm(rho.denominator,extra.denominator,*[w.denominator for j,s,w in items])
    C=int(cap*S);dd=int(D*S);cc=int(c*S);aa=int(rho*W);ee=int(extra*W)
    raw=[]
    for j,s,w in items:
        size=int(s*S);gain=int(w*W)*S-aa*size
        if 0<size<C and gain>0:raw.append((j,size,gain))
    keep=[t for t in raw if not any(u[1]<=t[1] and u[2]>=t[2] and(u[1]<t[1] or u[2]>t[2] or u[0]<t[0]) for u in raw)]
    keep.sort(key=lambda t:Q(t[2],t[1]),reverse=True)
    def bonus(r):return 0 if c==D else ee*min(r,dd*((r-1)//cc))
    best=bonus(C);bestpat=[];nodes=0;path=[]
    def visit(i,space,value):
        nonlocal best,bestpat,nodes
        nodes+=1;v=value+bonus(space)
        if v>best:best=v;bestpat=path.copy()
        if i==len(keep):return
        j,size,gain=keep[i];bound=max(Q(gain,size),Q(ee))
        if value*bound.denominator+space*bound.numerator<=best*bound.denominator:return
        for n in range((space-1)//size,-1,-1):
            if n:path.append((j,n))
            visit(i+1,space-n*size,value+n*gain)
            if n:path.pop()
    visit(0,C,0)
    return Q(aa*C+best,W*S)+offset,tuple(sorted(bestpat)),nodes
