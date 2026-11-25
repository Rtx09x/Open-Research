import itertools,json,time,random
from collections import Counter
import networkx as nx
from audit_connected import decomposition
from audit_bridgeless import leaves
start=time.time();stats=Counter()
for G in nx.graph_atlas_g():
 if len(G)<3 or not nx.is_connected(G) or list(nx.bridges(G)):continue
 E,Q,pieces,M,A=decomposition(G);K,regions=leaves(G);n=len(G);pairs=list(itertools.combinations(range(len(E)),2));full=(1<<len(pairs))-1
 covers=[sum(1<<i for i,(e,f) in enumerate(pairs) if row[e]!=row[f]) for row in M]
 for mask in range(1<<n):
  S={v for v in G if mask>>v&1};allowed=[q for q,(s,t) in enumerate(Q) if s in S and t in S]
  pred=len(S)>=2 if len(K)==1 else all(S&R for R in regions)
  union=0
  for q in allowed:union|=covers[q]
  assert (union==full)==bool(pred),(list(G.edges()),S,regions)
  stats['terminal_sets']+=1
  if pred:
   for c in covers:
    assert any(c&~covers[q]==0 for q in allowed),(list(G.edges()),S,c)
    stats['partition_domination_checks']+=1
   stats['identifying_terminal_sets']+=1
 stats['graphs']+=1
print(json.dumps({'stats':dict(stats),'seconds':time.time()-start}),flush=True)
