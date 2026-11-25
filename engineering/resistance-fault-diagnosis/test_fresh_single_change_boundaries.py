"""Independent exact rational boundary tests of two-anchor reconstruction.
Includes changes spanning 24 orders and near-deletion of bridges.
"""
import sympy as S
from itertools import combinations
from random import Random
import json
rng=Random(993022)
cases=0
for n in range(2,8):
    pairs=list(combinations(range(n),2))
    graphs=[[(i,i+1) for i in range(n-1)],pairs]
    if n>=3:graphs.append([(i,(i+1)%n) for i in range(n)])
    for edges in graphs:
        weights=[S.Rational(rng.randint(1,23),rng.randint(1,17)) for _ in edges]
        def lap(ws):
            L=S.zeros(n)
            for (u,v),c in zip(edges,ws):
                L[u,u]+=c;L[v,v]+=c;L[u,v]-=c;L[v,u]-=c
            return L
        def resistance(L):
            P=L[:n-1,:n-1].inv();return lambda u,v:(P[u,u] if u<n-1 else 0)+(P[v,v] if v<n-1 else 0)-(2*P[u,v] if max(u,v)<n-1 else 0)
        L=lap(weights);R=resistance(L)
        for e in sorted(set((0,len(edges)//2,len(edges)-1))):
            for ratio in (S.Rational(1,10**12),S.Integer(10**12),-1+S.Rational(1,10**12),-S.Rational(1,2)):
                ws=weights[:];delta=ws[e]*ratio;ws[e]+=delta;Rp=resistance(lap(ws))
                for root in sorted(set((0,n-1))):
                    inc={v:Rp(root,v)-R(root,v) for v in range(n)}
                    anchor=max(range(n),key=lambda v:abs(inc[v]));sigma=S.sign(inc[anchor]);D=abs(inc[anchor])
                    assert D>0
                    z=S.zeros(n,1);z[anchor]=D
                    for v in range(n):
                        if v not in (root,anchor):z[v]=sigma*(inc[anchor]+inc[v]-(Rp(anchor,v)-R(anchor,v)))/2
                    support=L*z;found={v for v in range(n) if support[v]!=0}
                    assert found==set(edges[e])
                    t=next(x for x in support if x!=0);gamma=sigma*t*t/D
                    recovered=-gamma/(1+gamma*R(*edges[e]))
                    assert recovered==delta
                    cases+=1
print(json.dumps({'exact_boundary_reconstructions':cases,'max_change_scale':'1e12','min_change_scale':'1e-12','bridge_surviving_fraction':'1e-12','status':'PASS'}))
