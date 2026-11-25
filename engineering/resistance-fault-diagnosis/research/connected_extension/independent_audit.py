"""Independent adversarial family audit: path supports and physical endpoint realizations."""
import sys,random,itertools,json,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
import networkx as nx
from exact_search import adaptive,nonadaptive
from audit_connected import decomposition,oracle
from audit_bridgeless import leaves,pairing_cover
rng=random.Random(104982);count=0;paircomp=0;fixed=0;maxn=0;maxm=0;start=time.time()
bases=[nx.cycle_graph(k) for k in range(3,8)]+[nx.complete_graph(4),nx.complete_bipartite_graph(2,3),nx.diamond_graph()]
for trial in range(160):
 G=nx.Graph();G.add_node(0)
 for j in range(rng.randint(2,5)):
  B=rng.choice(bases if trial%2 else bases+[nx.path_graph(2),nx.path_graph(3)])
  # Attach at random local vertex rather than always vertex zero.
  root=rng.choice(list(B));at=rng.choice(list(G));off=max(G)+1;mp={root:at}
  for v in B:
   if v!=root:mp[v]=off;off+=1
  G=nx.compose(G,nx.relabel_nodes(B,mp))
 E,Q,P,M,A=decomposition(G);O=oracle(G,E,Q)
 for r,s in zip(M,O):
  for e,f in itertools.combinations(range(len(E)),2):
   assert (r[e]==r[f])==(s[e]==s[f]),(trial,list(G.edges()),e,f)
   paircomp+=1
 aa,_,_=adaptive(O);assert aa==A,(trial,E,aa,A)
 if not list(nx.bridges(G)):
  C,regions=leaves(G);D=len(regions);k=max(1,(D+1)//2)
  if D:
   # Deliberately choose diverse physical representatives, not minimal IDs.
   reps=[rng.choice(list(r)) for r in regions];qix={frozenset(q):i for i,q in enumerate(Q)}
   ok=False
   for attempt in range(10000):
    xs=reps+([rng.choice(reps)] if D%2 else []);rng.shuffle(xs);pairs=list(zip(xs[::2],xs[1::2]))
    if any(a==b for a,b in pairs):continue
    qs=[qix[frozenset(p)] for p in pairs]
    if len({tuple(O[q][e] for q in qs) for e in range(len(E))})==len(E):ok=True;break
   assert ok,(trial,E,regions,reps)
  if len(Q)<=55 and k<=3:
   N,_=nonadaptive(O);assert N==k,(trial,E,N,k);fixed+=1
 count+=1;maxn=max(maxn,len(G));maxm=max(maxm,len(E))
 if count%10==0:print(json.dumps({'count':count,'pair_comparisons':paircomp,'exact_fixed':fixed,'max_n':maxn,'max_m':maxm,'seconds':time.time()-start}),flush=True)
