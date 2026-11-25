"""Exact rational oracle tests. Run with Python + SymPy; no floating point."""
import random
import sympy as S
from itertools import combinations, product


def lap(n, edges):
    L=S.zeros(n)
    for (u,v),w in edges.items():
        L[u,u]+=w; L[v,v]+=w; L[u,v]-=w; L[v,u]-=w
    return L


def components(n,edges):
    todo=set(range(n)); out=[]
    while todo:
        seen={min(todo)}; stack=list(seen)
        while stack:
            u=stack.pop()
            for (a,b),w in edges.items():
                if not w: continue
                v=b if a==u else a if b==u else None
                if v is not None and v not in seen: seen.add(v); stack.append(v)
        todo-=seen; out.append(sorted(seen))
    return out


def pinv_connected(L):
    n=L.rows; J=S.ones(n)/n
    return (L+J).inv()-J


def recover(n,baseline,changed):
    comps=components(n,changed); labels={v:i for i,C in enumerate(comps) for v in C}
    Ps={}
    for i,C in enumerate(comps):
        L=lap(n,changed).extract(C,C); Ps[i]=pinv_connected(L)
    calls={}
    def query(u,v):
        key=tuple(sorted((u,v)))
        if key not in calls:
            if labels[u]!=labels[v]: calls[key]=S.oo
            else:
                C=comps[labels[u]]; P=Ps[labels[u]]; a,b=C.index(u),C.index(v)
                calls[key]=P[a,a]+P[b,b]-2*P[a,b]
        return calls[key]
    unassigned=set(range(n)); discovered=[]; ranks=[]; recovered=S.zeros(n)
    while unassigned:
        root=min(unassigned)
        C=[root]+[v for v in sorted(unassigned-{root}) if query(root,v)!=S.oo]
        unassigned-=set(C); discovered.append(C)
        size=len(C); positions={v:i for i,v in enumerate(C)}
        base_edges={(positions[u],positions[v]):w for (u,v),w in baseline.items() if u in positions and v in positions}
        B=pinv_connected(lap(size,base_edges))
        def br(u,v):
            i,j=positions[u],positions[v]; return B[i,i]+B[j,j]-2*B[i,j]
        V=C[1:]; d=S.Matrix([query(root,v)-br(root,v) for v in V])
        nonzero=[x for x in d if x!=0]; sign=S.sign(nonzero[0]) if nonzero else 1
        diag=sign*d; H=S.zeros(size-1); residual=diag.copy(); count=0
        while any(x!=0 for x in residual):
            assert all(x>=0 for x in residual), 'monotonicity violated'
            a=next(i for i,x in enumerate(residual) if x>0); av=V[a]
            col=[]
            for i,v in enumerate(V):
                dav=0 if v==av else sign*(query(av,v)-br(av,v))
                col.append((diag[a]+diag[i]-dav)/2)
            h=S.Matrix(col)-H[:,a]; H+=h*h.T/residual[a]
            residual=diag-S.Matrix([H[i,i] for i in range(size-1)]); count+=1
        ranks.append(count)
        rooted=S.zeros(size)
        for i in range(size-1):
            for j in range(size-1): rooted[i+1,j+1]=H[i,j]
        J=S.eye(size)-S.ones(size)/size
        P=B+sign*J*rooted*J
        rec=(P+S.ones(size)/size).inv()-S.ones(size)/size
        for i,u in enumerate(C):
            for j,v in enumerate(C): recovered[u,v]=rec[i,j]
    assert recovered==lap(n,changed)
    m=len(comps)+sum(ranks)
    assert len(calls)<=m*n-m*(m+1)//2
    k=sum(baseline.get(e,0)!=changed.get(e,0) for e in set(baseline)|set(changed))
    assert m-1<=k
    if len(comps)==1:
        r=ranks[0]; assert len(calls)==(r+1)*(n-1)-r*(r+1)//2
    return len(calls),ranks,len(comps),k


def main():
    rng=random.Random(8675309); cases=[]
    for n in range(1,9):
        for trial in range(20):
            edges={(v-1,v):S.Rational(rng.randrange(1,5),rng.randrange(1,4)) for v in range(1,n)}
            for e in combinations(range(n),2):
                if rng.random()<.35: edges.setdefault(e,S.Rational(rng.randrange(1,5),rng.randrange(1,4)))
            for direction in (-1,1):
                changed=edges.copy()
                for e in edges:
                    if rng.random()<.45:
                        changed[e]*=rng.choice([S.Rational(0),S.Rational(1,3),S.Rational(2,3)]) if direction<0 else rng.choice([S.Rational(4,3),S.Rational(2),S.Rational(3)])
                cases.append(recover(n,edges,changed))
    # Cyclic support: all triangle edges change but response rank only two.
    tri={e:S.Rational(1) for e in combinations(range(3),2)}
    assert recover(3,tri,{e:S.Rational(1,2) for e in tri})[1]==[2]
    # Rank-one complete bridge deletion and the all-isolated endpoint.
    for n in range(2,10):
        path={(i,i+1):S.Rational(1) for i in range(n-1)}
        deleted=path.copy(); deleted[(n//2-1,n//2)]=0
        assert recover(n,path,deleted)[0]<=2*n-3
        assert recover(n,path,{e:S.Rational(0) for e in path})[0]==n*(n-1)//2
    # Mixed-direction counterexample: all root-star changes vanish, graph changed.
    mixed={(0,1):S.Rational(12,13),(0,2):S.Rational(12,13),(1,2):S.Rational(20,13)}
    P0=pinv_connected(lap(3,tri)); P1=pinv_connected(lap(3,mixed))
    dr=lambda u,v: (P1[u,u]+P1[v,v]-2*P1[u,v])-(P0[u,u]+P0[v,v]-2*P0[u,v])
    assert dr(0,1)==dr(0,2)==0 and dr(1,2)==-S.Rational(1,6)
    exhaustive=0; disconnected=0
    E=list(combinations(range(4),2)); base={e:S.Rational(1) for e in E}
    for weights in product((S.Rational(0),S.Rational(1,2),S.Rational(1)),repeat=len(E)):
        _,_,c,_=recover(4,base,dict(zip(E,weights)))
        exhaustive+=1; disconnected+=c>1
    print(f'PASS exhaustive K4 conductances {{0,1/2,1}}: {exhaustive} cases; {disconnected} disconnected.')
    for n in range(2,8):
        base={(i,i+1):S.Rational(1) for i in range(n-1)}
        changed={e:base.get(e,0)+S.Rational(1,2) for e in combinations(range(n),2)}
        recover(n,base,changed)
    print('PASS six new-edge increase cases.')
    print(f'PASS: {len(cases)} randomized rational cases; cyclic support; bridge deletions; all-isolated graphs; mixed-polarity counterexample.')
    print(f'Random cases include {sum(c>1 for _,_,c,_ in cases)} disconnected graphs.')

if __name__=='__main__': main()
