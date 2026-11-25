"""Focused larger access-domination checks using original simple-path supports."""
import sys,itertools,random,json,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
import networkx as nx
from audit_connected import oracle
from audit_bridgeless import leaves
rng=random.Random(944029);stats={'graphs':0,'terminal_sets':0,'domination_checks':0,'max_n':0,'max_m':0};start=time.time()
bases=[nx.complete_graph(4),nx.complete_graph(5),nx.cycle_graph(3),nx.cycle_graph(5),nx.diamond_graph(),nx.complete_bipartite_graph(2,3)]
graphs=[nx.complete_graph(4),nx.complete_graph(5),nx.diamond_graph()]
for trial in range(80):
 G=nx.Graph();G.add_node(0)
 for j in range(rng.randint(2,5)):
  B=rng.choice(bases);root=rng.choice(list(B));at=rng.choice(list(G));off=max(G)+1;mp={root:at}
  for v in B:
   if v!=root:mp[v]=off;off+=1
  G=nx.compose(G,nx.relabel_nodes(B,mp))
 graphs.append(G)
for G in graphs:
 E=list(G.edges());Q=list(itertools.combinations(G,2));O=oracle(G,E,Q);P=list(itertools.combinations(range(len(E)),2))
 covers=[sum(1<<j for j,(e,f) in enumerate(P) if row[e]!=row[f]) for row in O]
 K,regions=leaves(G)
 for trial in range(4):
  if len(K)==1:S=set(rng.sample(list(G),2))
  else:S={rng.choice(list(R)) for R in regions}
  if trial==3:S.update(nx.articulation_points(G))
  allowed=[i for i,(u,v) in enumerate(Q) if u in S and v in S]
  for qi,c in enumerate(covers):
   assert any(c&~covers[j]==0 for j in allowed),(list(G.edges()),S,Q[qi])
   stats['domination_checks']+=1
  stats['terminal_sets']+=1
 stats['graphs']+=1;stats['max_n']=max(stats['max_n'],len(G));stats['max_m']=max(stats['max_m'],len(E))
print(json.dumps({'stats':stats,'seconds':time.time()-start}),flush=True)
