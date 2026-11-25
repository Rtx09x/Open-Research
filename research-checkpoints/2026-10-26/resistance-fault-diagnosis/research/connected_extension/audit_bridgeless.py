import sys,itertools,json,random,time
from collections import Counter
from pathlib import Path
import networkx as nx
from audit_connected import decomposition,oracle
from exact_search import adaptive,nonadaptive

def leaves(G):
 arts=set(nx.articulation_points(G)); C=nx.MultiGraph();representatives={};regions=[]
 for bi,es in enumerate(nx.biconnected_component_edges(G)):
  B=G.edge_subgraph(es).copy();assert nx.is_biconnected(B)
  cuts=[]
  for e,f in itertools.combinations(list(B.edges()),2):
   H=B.copy();H.remove_edges_from([e,f])
   if not nx.is_connected(H):cuts.append(set(nx.node_connected_component(H,next(iter(B)))))
  groups={}
  for v in B:groups.setdefault(tuple(v in S for S in cuts),[]).append(v)
  comp={};
  for i,vs in enumerate(groups.values()):
   z=(bi,i);C.add_node(z);representatives[z]=set(vs)
   for v in vs:comp[v]=z
  for u,v in B.edges():
   if comp[u]!=comp[v]:C.add_edge(comp[u],comp[v])
  for v in set(B)&arts:
   a=('a',v);C.add_edge(comp[v],a);C.add_edge(comp[v],a)
 for z in C:
  if C.degree(z)==2:
   assert z in representatives
   R=representatives[z]-arts;assert R
   regions.append(R)
 return C,regions

def pairing_cover(xs):
 # Enumerate all edge covers of k=ceil(L/2) using leaf representatives.
 if len(xs)%2:
  for v in xs:
   for pairs in pairing_cover(xs+[v]):
    if all(a!=b for a,b in pairs):yield pairs
  return
 if not xs:yield [];return
 x=xs[0]
 for i in range(1,len(xs)):
  for rest in pairing_cover(xs[1:i]+xs[i+1:]):yield [(x,xs[i])]+rest

def check(G,exact=True):
 E,Q,pieces,M,A=decomposition(G);C,regions=leaves(G);L=len(regions);pred=max(1,(L+1)//2)
 if exact:
  N,qs=nonadaptive(M);assert N==pred,(list(G.edges()),L,N,pred)
 if L:
  reps=[min(R) for R in regions];qix={frozenset(q):i for i,q in enumerate(Q)}
  found=None
  for pairs in pairing_cover(reps):
   inds=[qix[frozenset(q)] for q in pairs]
   if len({tuple(M[q][e] for q in inds) for e in range(len(E))})==len(E):found=pairs;break
  assert found is not None,(list(G.edges()),regions)
 # all blocks three-edge-connected iff auxiliary cactus has only artificial edges
 special=all(nx.edge_connectivity(G.edge_subgraph([E[e] for e in p]))>=3 for p in pieces)
 if special:assert A==pred,(list(G.edges()),A,pred)
 return {'L':L,'N':pred,'A':A,'special':special}

if __name__=='__main__':
 start=time.time();stats=Counter();rng=random.Random(7610);large=[]
 for G in nx.graph_atlas_g():
  if len(G)<3 or not nx.is_connected(G) or list(nx.bridges(G)):continue
  res=check(G);stats['atlas_graphs']+=1;stats['three_edge_block_graphs']+=res['special']
 bases=[nx.cycle_graph(3),nx.cycle_graph(4),nx.complete_graph(4),nx.complete_bipartite_graph(2,3),nx.diamond_graph()]
 for trial in range(100):
  G=nx.Graph();G.add_node(0)
  for k in range(rng.randrange(2,5)):
   B=rng.choice(bases);attach=rng.choice(list(G));mapping={0:attach};off=max(G)+1
   for v in list(B)[1:]:mapping[v]=off;off+=1
   G=nx.compose(G,nx.relabel_nodes(B,mapping))
  C,regions=leaves(G)
  if len(regions)>9:continue
  res=check(G,False);stats['larger_graphs']+=1
  if len(large)<15:large.append({'n':len(G),'m':G.number_of_edges(),**res})
 print(json.dumps({'stats':dict(stats),'seconds':time.time()-start,'larger_examples':large}),flush=True)
