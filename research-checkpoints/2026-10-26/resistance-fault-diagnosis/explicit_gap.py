"""Closed-form, bounded-resistance, linear adaptivity-gap construction.

Hubs0,1; peripheral i+2 has resistances a_i=1 and b_i=2+(i+1)/(m+1).
Uses circuit reduction rather than a Laplacian inverse/determinant.
"""
from fractions import Fraction as F
from itertools import combinations
import json,sys,time

def response(m,q,e):
    h,i=divmod(e,m);a=[F(1)]*m;b=[2+F(j+1,m+1) for j in range(m)]
    L=[a[j]+b[j] for j in range(m)]
    R=1/sum(1/L[j] for j in range(m) if j!=i)
    z=[a[j]*b[j]/L[j] for j in range(m)]
    alpha=[a[j]/L[j] for j in range(m)];beta=[b[j]/L[j] for j in range(m)]
    u,v=sorted(q)
    if (u,v)==(0,1):return R
    if u<2:
        k=v-2
        if k==i:
            # h is failed hub connection; remaining edge goes to1-h.
            return (b[i] if h==0 else a[i])+(R if u==h else 0)
        return z[k]+(alpha[k] if u==0 else beta[k])**2*R
    j,k=u-2,v-2
    if i==j:return (b[j] if h==0 else a[j])+z[k]+(beta[k] if h==0 else alpha[k])**2*R
    if i==k:return (b[k] if h==0 else a[k])+z[j]+(beta[j] if h==0 else alpha[j])**2*R
    return z[j]+z[k]+(alpha[j]-alpha[k])**2*R

def cover(m):
    qs=[(2+i,3+i) for i in range(0,m-1,2)]
    if m%2:qs.append((2,m+1))
    return qs

def check(m,full=False):
    assert m>=3
    qs=cover(m)
    values=[[response(m,q,e) for e in range(2*m)] for q in qs]
    assert len(set(zip(*values)))==2*m
    first=[response(m,(0,1),i) for i in range(m)]
    assert len(set(first))==m
    for i in range(m):assert response(m,(0,2+i),i)!=response(m,(0,2+i),m+i)
    # Combinatorial property used in the static upper proof.
    if m>=6:
        for i,j in combinations(range(m),2):assert any(i+2 not in q and j+2 not in q for q in qs)
    first_margin=min(abs(x-y) for x,y in combinations(first,2))
    adaptive_second=min(abs(response(m,(0,2+i),i)-response(m,(0,2+i),m+i)) for i in range(m))
    static_margin=min(max(abs(row[i]-row[j]) for row in values) for i,j in combinations(range(2*m),2))
    adaptive_lower=F(9,16*(m+1)*(m-1)**2)
    static_lower=F(9*(m-2)**2,256*(m+1)*(m-1)**2)
    assert first_margin>adaptive_lower and static_margin>static_lower
    for q in qs:
        p,r=q[0]-2,q[1]-2
        inside=[]
        for i in (p,r):
            hi=response(m,q,i);lo=response(m,q,m+i)
            assert hi>F(8,3) and F(5,3)<lo<F(71,36)
            inside.extend([hi,lo])
        assert len(set(inside))==4
        for i in range(m):
            if i not in (p,r):assert response(m,q,i)<F(109,72)
    if full:
        from exact_search import responses
        E=[(h,2+i) for h in range(2) for i in range(m)]
        Q,M=responses(m+2,E,resistances=[F(1)]*m+[2+F(i+1,m+1) for i in range(m)])
        assert all(M[k][e]==response(m,q,e) for k,q in enumerate(Q) for e in range(2*m))
    return {'m':m,'faults':2*m,'adaptive_exact':2,'nonadaptive_exact':len(qs),'first_margin':str(first_margin),'second_margin':str(adaptive_second),'static_margin':str(static_margin),'proved_adaptive_margin_lower':str(adaptive_lower),'proved_static_margin_lower':str(static_lower),'all_pairs_laplacian_crosscheck':full}

if __name__=='__main__':
    for m in map(int,sys.argv[1:]):print(json.dumps(check(m,full=m<=12)),flush=True)
