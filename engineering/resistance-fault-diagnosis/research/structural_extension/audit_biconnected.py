import sys,itertools,random,json,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
import networkx as nx
from generic_audit import support
from exact_search import responses,adaptive,nonadaptive
rng=random.Random(20261008)
t0=time.time();stats={'graphs':0,'identity_comparisons':0,'rational_entries':0,'exact_optimizations':0};examples=[]
for G in nx.graph_atlas_g():
 n=len(G)
 if n<3 or not nx.is_biconnected(G):continue
 E=list(G.edges());m=len(E);Q=list(itertools.combinations(G,2));P=list(itertools.combinations(range(m),2));cuts={}
 for a,b in P:
  H=G.copy();H.remove_edges_from([E[a],E[b]])
  comps=list(nx.connected_components(H))
  if len(comps)>1:
   assert len(comps)==2
   cuts[a,b]=set(comps[0])
 # Matrix of structural equivalence, independent simple-path rational identity criterion.
 mat=[]
 for s,t in Q:
  su=[support(n,E,f,s,t) for f in range(m)]
  labels=list(range(m))
  def root(x):
   while labels[x]!=x:x=labels[x]
   return x
  for a,b in P:
   equal=not((su[b]>>a&1) or(su[a]>>b&1))
   predicted=(a,b) in cuts and ((s in cuts[a,b])==(t in cuts[a,b]))
   assert equal==predicted,(E,(s,t),a,b)
   if equal:labels[root(a)]=root(b)
   stats['identity_comparisons']+=1
  mat.append([root(a) for a in range(m)])
 kappa=min(max(row.count(z) for z in set(row)) for row in mat)
 ap=1+(kappa-1).bit_length()
 ao,_,_=adaptive(mat);assert ao==ap,(E,ap,ao)
 no,nq=nonadaptive(mat)
 # independent max disjoint two-cut shores via subset-packing DP
 shores=[]
 for mask in range(1,(1<<n)-1):
  if sum(((mask>>u)&1)!=((mask>>v)&1) for u,v in E)==2:shores.append(mask)
 dp=[0]*(1<<n)
 for mask in range(1<<n):
  for shore in shores:
   if not mask&shore:dp[mask|shore]=max(dp[mask|shore],dp[mask]+1)
 nu=max(dp);np=max(1,(nu+1)//2)
 assert no==np,(E,no,np,nu)
 # Check augmenting selected query multiedges directly by all cuts.
 assert all(sum(((mask>>u)&1)!=((mask>>v)&1) for u,v in E)+sum(((mask>>Q[q][0])&1)!=((mask>>Q[q][1])&1) for q in nq)>=3 for mask in range(1,(1<<n)-1))
 if n<=6:
  _,rm=responses(n,E,resistances=[rng.randrange(1,10**6) for _ in E])
  assert all((row[a]==row[b])==(rr[a]==rr[b]) for row,rr in zip(mat,rm) for a,b in P)
  stats['rational_entries']+=len(Q)*m
 stats['graphs']+=1;stats['exact_optimizations']+=1
 if len(examples)<20 and no>ao:examples.append({'edges':E,'A':ao,'N':no,'kappa':kappa,'nu':nu})
 if stats['graphs']%50==0:print(json.dumps({'progress':stats,'seconds':time.time()-t0}),flush=True)
print(json.dumps({'final':stats,'seconds':time.time()-t0,'gap_examples':examples}),flush=True)
