"""Independent simple-path oracle versus block partitions and healthy-spine minimax."""
import sys,itertools,json,time,random
from pathlib import Path
from functools import lru_cache
from collections import Counter
import networkx as nx
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from exact_search import adaptive,nonadaptive,responses


def decomposition(G):
 E=list(G.edges()); index={frozenset(e):i for i,e in enumerate(E)}
 pieces=[list(index[frozenset(e)] for e in es) for es in nx.biconnected_component_edges(G)]
 masks=[sum(1<<e for e in p) for p in pieces]
 Q=list(itertools.combinations(G,2)); matrix=[]; healthy=[]; costs=[]; hits=[]
 for s,t in Q:
  path=nx.shortest_path(G,s,t); pe={index[frozenset(e)] for e in zip(path,path[1:])}
  row=[('healthy',)]*len(E); touched=0
  for bi,p in enumerate(pieces):
   if not pe.intersection(p):continue
   touched|=1<<bi
   if len(p)==1:row[p[0]]=('infinity',);continue
   V={v for e in p for v in E[e]}; gates=[v for v in path if v in V];a,b=gates[0],gates[-1]
   B=G.edge_subgraph([E[e] for e in p]).copy(); uf=nx.utils.UnionFind(p)
   for e,f in itertools.combinations(p,2):
    H=B.copy();H.remove_edges_from([E[e],E[f]])
    if not nx.is_connected(H) and nx.has_path(H,a,b):uf.union(e,f)
   for e in p:row[e]=('block',bi,uf[e])
  matrix.append(row);healthy.append(sum(1<<e for e,z in enumerate(row) if z==('healthy',)));hits.append(touched)
 @lru_cache(None)
 def spine(state):
  active=sum(masks[i] for i in range(len(pieces)) if state>>i&1)
  if active.bit_count()<=1:return 0
  best=len(E)
  for qi,row in enumerate(matrix):
   nxt=state&~hits[qi]
   if nxt==state:continue
   counts=Counter(row[e] for e in range(len(E)) if active>>e&1 and row[e]!=('healthy',))
   r=max(counts.values());tail=(r-1).bit_length()
   best=min(best,1+max(tail,spine(nxt)))
  return best
 return E,Q,pieces,matrix,spine((1<<len(pieces))-1)

def oracle(G,E,Q):
 index={frozenset(e):i for i,e in enumerate(E)};mat=[]
 for s,t in Q:
  sig=[0]*len(E)
  for pi,path in enumerate(nx.all_simple_paths(G,s,t)):
   for e in zip(path,path[1:]):sig[index[frozenset(e)]]|=1<<pi
  mat.append(sig)
 return mat

def fixed_criterion(G,E,Q,pieces,chosen):
 # Block local partition refinement plus distinct bridge path-incidence signatures.
 bridges=[p[0] for p in pieces if len(p)==1]
 signatures={e:tuple(not nx.has_path(nx.restricted_view(G,[],[E[e]]),*Q[q]) for q in chosen) for e in bridges}
 if len(set(signatures.values()))<len(bridges):return False
 for p in pieces:
  if len(p)==1:continue
  B=G.edge_subgraph([E[e] for e in p]).copy();H=nx.MultiGraph(B);activated=False
  for qi in chosen:
   path=nx.shortest_path(G,*Q[qi]);vs=[v for v in path if v in B]
   if len(vs)>=2:H.add_edge(vs[0],vs[-1]);activated=True
  if not activated:return False
  V=list(B)
  if any(sum(1 for u,v in H.edges() if (u in S)!=(v in S))<3 for k in range(1,len(V)) for S in map(set,itertools.combinations(V,k))):return False
 return True

if __name__=='__main__':
 start=time.time();stats=Counter();rng=random.Random(81793);examples=[]
 for G in nx.graph_atlas_g():
  n=len(G)
  if n<2 or not nx.is_connected(G):continue
  E,Q,pieces,M,sp=decomposition(G);O=oracle(G,E,Q)
  for row,oracle_row in zip(M,O):
   for e,f in itertools.combinations(range(len(E)),2):
    assert (row[e]==row[f])==(oracle_row[e]==oracle_row[f]),(E,e,f)
    stats['partition_comparisons']+=1
  a,_,_=adaptive(O);assert a==sp,(E,a,sp);stats['adaptive_optimizations']+=1
  no,nq=nonadaptive(O);assert fixed_criterion(G,E,Q,pieces,nq),(E,nq)
  # All fixed sets through size 3 on order <=5, plus random candidate sets.
  sets=[tuple(q for q in range(len(Q)) if rng.randrange(2)) for _ in range(10)]
  if n<=5:sets.extend(S for k in range(4) for S in itertools.combinations(range(len(Q)),k))
  for S in sets:
   truth=len({tuple(O[q][e] for q in S) for e in range(len(E))})==len(E)
   assert fixed_criterion(G,E,Q,pieces,S)==truth,(E,S,truth)
   stats['fixed_design_checks']+=1
  if n<=5:
   _,R=responses(n,E,resistances=[rng.randrange(1,1000000) for _ in E])
   for row,rr in zip(M,R):
    for e,f in itertools.combinations(range(len(E)),2):assert (row[e]==row[f])==(rr[e]==rr[f])
   stats['rational_entries']+=len(Q)*len(E)
  if len(examples)<15 and len(pieces)>1 and a<no:examples.append({'edges':E,'A':a,'N':no,'pieces':pieces})
  stats['graphs']+=1
  if stats['graphs']%100==0:print(json.dumps({'progress':dict(stats),'seconds':time.time()-start}),flush=True)
 print(json.dumps({'final':dict(stats),'seconds':time.time()-start,'gap_examples':examples}),flush=True)
