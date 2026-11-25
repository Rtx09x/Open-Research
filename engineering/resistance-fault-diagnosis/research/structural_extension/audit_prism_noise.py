import networkx as nx,itertools,json,sys,random,time
from pathlib import Path
from fractions import Fraction as F
sys.path.insert(0,str(Path(__file__).resolve().parents[2]));from exact_search import responses,inverse
rng=random.Random(20261008)
for n in [6,8,10,12]:
 start=time.time();G=nx.circular_ladder_graph(n//2);E=list(G.edges());m=len(E);c=[1+F(rng.randrange(1,101),1000) for e in E];r=[1/x for x in c]
 Q,M=responses(n,E,resistances=r)
 lap=[[F(0) for _ in range(n-1)] for _ in range(n-1)]
 for (u,v),w in zip(E,c):
  if u<n-1:lap[u][u]+=w
  if v<n-1:lap[v][v]+=w
  if u<n-1 and v<n-1:lap[u][v]-=w;lap[v][u]-=w
 inv=inverse(lap)
 def ent(u,v):return inv[u][v] if u<n-1 and v<n-1 else F(0)
 def intact(q):u,v=q;return ent(u,u)+ent(v,v)-2*ent(u,v)
 base=[intact(q) for q in Q];ix={q:i for i,q in enumerate(Q)};eq=[ix[tuple(sorted(e))] for e in E];tau=[w*base[q] for w,q in zip(c,eq)];slack=[1-z for z in tau]
 assert sum(tau)==n-1
 for q,row in enumerate(M):assert sum(s*(x-base[q])/base[q] for s,x in zip(slack,row))==1
 assert all(len(set(row))==m for row in M)
 margins=[];separators=[]
 for a,b in itertools.combinations(range(m),2):
  candidates=[(abs(M[q][a]-M[q][b])/(M[q][a]+M[q][b]),q) for q in [eq[a],eq[b]]]
  margin,q=max(candidates);assert margin>F(1,100),(n,E[a],E[b],margin)
  margins.append(margin);separators.append(q)
 lower=F(2,99)*(sum(slack)-max(slack));weak=F(2,99)*(m-n)
 out={'n':n,'m':m,'edges':E,'conductances':[str(z) for z in c],'all_pair_queries_generic_distinct':True,'prescribed_exact_query':Q[0],'response_entries':len(Q)*m,'fault_pairs':m*(m-1)//2,'minimum_best_own_endpoint_relative_margin':str(min(margins)),'margin_decimal':float(min(margins)),'energy_identity_queries':len(Q),'Foster_verified':True,'sharp_lower_t_strictly_greater_than':str(lower),'cycle_rank_lower_t_strictly_greater_than':str(weak),'relative_error':'1/100','fixed_endpoint_queries':m,'seconds':time.time()-start}
 print(json.dumps(out),flush=True)
