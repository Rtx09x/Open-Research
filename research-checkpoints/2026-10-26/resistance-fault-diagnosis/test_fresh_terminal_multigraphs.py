"""Fresh terminal-ambiguity checks using edge-indexed paths on small multigraphs.
No cactus, augmentation, or planner partition code is used as the reference.
"""
from itertools import combinations, product
from fractions import Fraction as F
from random import Random
from exact_search import responses
import json

def paths(n, edges, s, t):
    adj=[[] for _ in range(n)]
    for i,(u,v) in enumerate(edges):
        adj[u].append((v,i)); adj[v].append((u,i))
    out=[]
    def dfs(v,seen,used):
        if v==t:
            out.append(used); return
        for w,e in adj[v]:
            if w not in seen: dfs(w,seen|{w},used|{e})
    dfs(s,{s},set())
    return out

rng=Random(24071991)
stats={'connected_multigraphs':0,'terminal_sets':0,'edge_pair_comparisons':0,'electrical_response_entries':0}
for n in range(2,5):
    pairs=list(combinations(range(n),2))
    for counts in product(range(3),repeat=len(pairs)):
        edges=[e for e,c in zip(pairs,counts) for _ in range(c)]
        if not edges: continue
        pp={q:paths(n,edges,*q) for q in pairs}
        if any(not p for p in pp.values()): continue
        matrices=[]
        for _ in range(2):
            weights=[F(rng.randint(1,997),rng.randint(1,97)) for e in edges]
            q,matrix=responses(n,edges,resistances=weights)
            matrices.append(dict(zip(q,matrix)))
            stats['electrical_response_entries'] += len(q)*len(edges)
        stats['connected_multigraphs'] += 1
        for size in range(2,n+1):
            for B in combinations(range(n),size):
                qs=list(combinations(B,2))
                pathsB=[p for q in qs for p in pp[q]]
                sig=[tuple(e in p for p in pathsB) for e in range(len(edges))]
                for e,f in combinations(range(len(edges)),2):
                    topology_equal=sig[e]==sig[f]
                    electrical_equal=all(all(mat[q][e]==mat[q][f] for q in qs) for mat in matrices)
                    assert topology_equal==electrical_equal,(n,edges,B,e,f)
                    stats['edge_pair_comparisons']+=1
                stats['terminal_sets']+=1
print(json.dumps(stats,sort_keys=True))
