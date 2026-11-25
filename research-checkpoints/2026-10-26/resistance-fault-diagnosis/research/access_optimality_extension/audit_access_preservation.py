"""Independent exhaustive generic partition/optimization audit. No theorem formula is used
in either optimizer. Cactus tests use abstract cut partitions, not electrical partitions
of an articulated physical cactus. Install the dependencies listed in requirements.txt before running.
"""
from itertools import combinations
from functools import lru_cache
from pathlib import Path
import json,time
import networkx as nx

START=time.time()
stats={'biconnected_graphs':0,'biconnected_terminal_sets':0,'cactus_models':0,'cactus_terminal_sets':0,'query_dominance_checks':0,'optimizer_pairs':0}

def optimizers(rows,m):
    # rows are partitions encoded by tuples of hypothesis bitsets.
    rows=tuple(sorted(set(rows)))
    @lru_cache(None)
    def depth(S):
        if S.bit_count()<=1:return 0
        splits={tuple(sorted(b&S for b in row if b&S)) for row in rows}
        splits.discard((S,))
        return min((1+max(depth(b) for b in split) for split in splits),default=m+1)
    A=depth((1<<m)-1)
    pairs=list(combinations(range(m),2)); full=(1<<len(pairs))-1
    covers=[]
    for row in rows:
        covers.append(sum(1<<i for i,(a,b) in enumerate(pairs) if not any(block>>a&1 and block>>b&1 for block in row)))
    covers=tuple(set(covers))
    # Exact set cover by memoized uncovered-pair recursion, unrelated to augmentation.
    @lru_cache(None)
    def cover(U):
        if not U:return 0
        bit=U&-U
        return 1+min(cover(U&~c) for c in covers if c&bit)
    return A,cover(full)

def check(G,cactus=False):
    n=len(G); E=list(G.edges(keys=True)) if G.is_multigraph() else list(G.edges()); m=len(E)
    queries=list(combinations(range(n),2)); pairs=list(combinations(range(m),2)); shores={}
    for a,b in pairs:
        H=G.copy();H.remove_edges_from([E[a],E[b]])
        cs=list(nx.connected_components(H))
        if len(cs)>1:
            assert len(cs)==2
            shores[a,b]=cs[0]
    covers=[];rows=[]
    for s,t in queries:
        crossing=frozenset(p for p,S in shores.items() if (s in S)!=(t in S));covers.append(crossing)
        # Edges in different series classes have distinct formal labels.
        parent=list(range(m))
        def root(i):
            while parent[i]!=i:i=parent[i]
            return i
        for (a,b),S in shores.items():
            if (s in S)==(t in S):parent[root(a)]=root(b)
        blocks={}
        for i in range(m):blocks[root(i)]=blocks.get(root(i),0)|(1<<i)
        rows.append(tuple(sorted(blocks.values())))
    unrestricted=optimizers(rows,m)
    for mask in range(1<<n):
        B={i for i in range(n) if mask>>i&1}
        if len(B)<2 or not all(B&S and B-S for S in shores.values()):continue
        ids=[i for i,(s,t) in enumerate(queries) if s in B and t in B]
        for i,C in enumerate(covers):
            dominators=[j for j in ids if C<=covers[j]]
            assert dominators,(E,B,queries[i])
            # Separately verify partition refinement rather than assume cut implication.
            assert any(all(any(block&old==block for old in rows[i]) for block in rows[j]) for j in dominators)
            stats['query_dominance_checks']+=1
        assert optimizers([rows[i] for i in ids],m)==unrestricted,(E,B,unrestricted)
        stats['optimizer_pairs']+=1
        stats['cactus_terminal_sets' if cactus else 'biconnected_terminal_sets']+=1
    stats['cactus_models' if cactus else 'biconnected_graphs']+=1

for G in nx.graph_atlas_g():
    if len(G)>=3 and nx.is_biconnected(G):check(G)
    if len(G)>=3 and nx.is_connected(G) and not list(nx.bridges(G)) and all(len(c)==G.subgraph(c).number_of_edges() for c in nx.biconnected_components(G)):
        check(G,True)
# Hand-built cactus chains, bouquets, mixed attachments; includes parallel 2-cycles.
for lengths,anchors in [([2,2,2],[0,1,2]),([3,3,3],[0,1,3]),([3,3,3],[0,0,0]),([4,3,2],[0,2,4]),([2,4,3],[0,1,3]),([4,4],[0,2]),([5,3],[0,2])]:
    G=nx.MultiGraph();G.add_node(0);nextv=1
    for ell,anchor in zip(lengths,anchors):
        assert anchor in G
        nodes=[anchor]+list(range(nextv,nextv+ell-1));nextv+=ell-1
        G.add_edges_from(zip(nodes,nodes[1:]+nodes[:1]))
    check(G,True)
stats.update(failures=0,seconds=time.time()-START)
print(json.dumps(stats,indent=2));Path(__file__).with_name('audit_results.json').write_text(json.dumps(stats,indent=2)+'\n')
