"""Independent larger-graph numeric-exact audit with direct Laplacian responses."""
import networkx as nx
import sympy as S
import random,itertools,json
from functools import lru_cache
rng=random.Random(887213)
def audit(G):
    G=nx.convert_node_labels_to_integers(G);n=len(G);E=list(G.edges());m=len(E);Q=list(itertools.combinations(range(n),2))
    assert nx.is_biconnected(G)
    weights=[S.Rational(rng.randrange(1000,100000)) for _ in E]
    matrix=[[] for _ in Q]
    for f in range(m):
        L=S.zeros(n-1)
        for j,(a,b) in enumerate(E):
            if j==f:continue
            for u,v,sgn in [(a,a,1),(b,b,1),(a,b,-1),(b,a,-1)]:
                if u<n-1 and v<n-1:L[u,v]+=sgn/weights[j]
        K=L.inv()
        for k,(a,b) in enumerate(Q):matrix[k].append(K[a,a]+(K[b,b]-2*K[a,b] if b<n-1 else 0))
    cuts={}
    for a,b in itertools.combinations(range(m),2):
        H=G.copy();H.remove_edges_from([E[a],E[b]])
        if not nx.is_connected(H):cuts[a,b]=next(iter(nx.connected_components(H)))
    for (s,t),row in zip(Q,matrix):
        for a,b in itertools.combinations(range(m),2):
            assert (row[a]==row[b])==((a,b) in cuts and ((s in cuts[a,b])==(t in cuts[a,b])))
    partitions=[]
    for row in matrix:
        groups={}
        for i,x in enumerate(row):groups.setdefault(x,set()).add(i)
        partitions.append(tuple(frozenset(x) for x in groups.values()))
    @lru_cache(None)
    def dp(state):
        if len(state)<=1:return 0
        ans=len(state)
        for parts in partitions:
            children={state&part for part in parts}-{frozenset()}
            if len(children)<=1:continue
            ans=min(ans,1+max(dp(child) for child in children))
        return ans
    kappa=min(max(map(len,p)) for p in partitions)
    A=dp(frozenset(range(m)));assert A==1+(kappa-1).bit_length()
    # Direct fixed-query hitting set on all edge-pairs, including generic-distinct ones.
    universe=set(itertools.combinations(range(m),2))
    covers=[frozenset((a,b) for a,b in universe if row[a]!=row[b]) for row in matrix]
    @lru_cache(None)
    def coverdp(rem):
        if not rem:return 0
        target=min(rem,key=lambda p:sum(p in c for c in covers))
        return 1+min(coverdp(rem-c) for c in covers if target in c)
    N=coverdp(frozenset(universe))
    # Independently enumerate all nontrivial 2-cut vertex shores, pack disjoint ones.
    shores=[]
    for mask in range(1,(1<<n)-1):
        if sum(((mask>>u)&1)!=((mask>>v)&1) for u,v in E)==2:shores.append(mask)
    best=[0]*(1<<n)
    for mask in range(1<<n):
        for shore in shores:
            if not mask&shore:best[mask|shore]=max(best[mask|shore],best[mask]+1)
    nu=max(best);assert N==max(1,(nu+1)//2)
    return dict(n=n,m=m,A=A,N=N,kappa=kappa,nu=nu,two_cuts=len(cuts),edges=E)
Gs=[nx.cycle_graph(i) for i in range(8,13)]
for z in range(12):
    core=nx.complete_graph(4 if z<6 else 5)
    # Subdivide selected edges, retaining biconnectivity and producing long series classes.
    for a,b in list(core.edges()):
        if rng.random()<.55:
            core.remove_edge(a,b);last=a
            for _ in range(rng.randrange(1,3)):
                v=len(core);core.add_edge(last,v);last=v
            core.add_edge(last,b)
    if len(core)<=15:Gs.append(core)
for G in Gs:print(json.dumps(audit(G)),flush=True)
