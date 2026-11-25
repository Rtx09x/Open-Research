"""Independent grounded-Laplacian audit; no imports from proposed theorem code."""
import sympy as S
from itertools import combinations
import json

def run(m):
    g=[1/(S.Rational(3)+S.Rational(i+1,m+1)) for i in range(m)]
    C=sum(g); cover=list(zip(range(0,m-1,2),range(1,m,2)))
    if m%2: cover.append((m-2,m-1))
    edges=[(hub,i+2,S.Integer(1) if hub==0 else 1/g[i]-1) for i in range(m) for hub in range(2)]
    queries=list(combinations(range(m+2),2))
    def response(f=None,tau=0):
        L=S.zeros(m+1)
        for k,(a,b,r) in enumerate(edges):
            c=1/(r+(tau if k==f else 0))
            for u,v,sgn in [(a,a,1),(b,b,1),(a,b,-1),(b,a,-1)]:
                if u<m+1 and v<m+1:L[u,v]+=sgn*c
        K=L.inv(); vals={}
        for a,b in queries:
            vals[a,b]=(K[a,a] if a<m+1 else 0)+(K[b,b] if b<m+1 else 0)-(2*K[a,b] if b<m+1 else 0)
        return vals
    base=response(); rays=[]; cases=0
    for f in range(2*m):
        i=f//2; direction=None
        for tau in [S.Rational(1,100),S.Integer(1),S.Integer(123)]:
            y=response(f,tau)
            delta=[y[p+2,q+2]-base[p+2,q+2] for p,q in cover]
            ray=tuple(S.cancel(t/delta[0]) for t in delta)
            if direction is None:direction=ray
            assert ray==direction
            lam=y[0,1]-base[0,1]
            coeff=[]
            for p,q in cover:
                d=g[p]-g[q]
                if i==p:A=d+(1/g[p]-1)*C if f%2==0 else C-d
                elif i==q:A=(1/g[q]-1)*C-d if f%2==0 else C+d
                else:A=d
                coeff.append(A*A)
            assert all(S.cancel(d-lam*a)==0 for d,a in zip(delta,coeff))
            recovered_lam=delta[0]/coeff[0]
            loss=C*C*recovered_lam/(1+C*recovered_lam)
            recovered_tau=loss/(g[i]*(g[i]-loss))
            assert S.cancel(recovered_tau-tau)==0
            cases+=1
        rays.append(direction)
    assert len(set(rays))==2*m
    h=min(g)/3; adversary={q:[] for q in queries}
    for f in range(2*m):
        i=f//2; tau=1/(g[i]-h)-1/g[i]; y=response(f,tau)
        for q in queries:
            if i+2 not in q:adversary[q].append(y[q])
    assert all(len(set(v))==1 for v in adversary.values() if v)
    return dict(m=m,cover=cover,rays=len(set(rays)),positive_magnitude_cases=cases,exact_magnitude_recovery=True,equal_loss_all_external_queries=True)
if __name__=='__main__':
    result=[run(m) for m in range(3,11)]
    print(json.dumps(result,indent=2))
