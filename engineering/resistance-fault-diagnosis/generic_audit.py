"""Exhaustive small-topology check of generic response-identity criterion."""
from itertools import combinations
from exact_search import responses
import random,json,time

def support(n,E,deleted,s,t):
    adj=[[] for _ in range(n)]
    for i,(u,v) in enumerate(E):
        if i!=deleted:adj[u].append((v,i));adj[v].append((u,i))
    mask=0;found=False
    def walk(u,seen,used):
        nonlocal mask,found
        if u==t:mask|=used;found=True;return
        for v,e in adj[u]:
            if not (seen>>v&1):walk(v,seen|(1<<v),used|(1<<e))
    walk(s,1<<s,0)
    return mask if found else None

def main(n):
    allE=list(combinations(range(n),2));count=0;comparisons=0;start=time.time()
    rng=random.Random(20261008+n)
    for gm in range(1,1<<len(allE)):
        E=[e for i,e in enumerate(allE) if gm>>i&1]
        if any(support(n,E,-1,0,v) is None for v in range(1,n)):continue
        if len(E)<2:continue
        Q=list(combinations(range(n),2))
        S=[[support(n,E,f,*q) for f in range(len(E))] for q in Q]
        matrices=[responses(n,E,resistances=[rng.randint(1,997) for e in E])[1] for _ in range(3)]
        for qi,q in enumerate(Q):
            for e,f in combinations(range(len(E)),2):
                a,b=S[qi][e],S[qi][f]
                predicted=(a is None and b is None) if a is None or b is None else not((b>>e&1) or(a>>f&1))
                observed=all(M[qi][e]==M[qi][f] for M in matrices)
                assert predicted==observed,(n,E,q,e,f,predicted,observed)
                comparisons+=1
        count+=1
    return {'vertices':n,'connected_labeled_graphs':count,'fault_pair_query_comparisons':comparisons,'positive_integer_weightings_each':3,'seconds':time.time()-start,'qualification':'Finite corroboration, not a proof of generic identity or novelty.'}

if __name__=='__main__':
    for n in [3,4,5]:print(json.dumps(main(n)),flush=True)
