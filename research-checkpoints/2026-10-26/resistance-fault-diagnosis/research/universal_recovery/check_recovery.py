"""Independent rational test of scalar-pair single-fault recovery."""
from pathlib import Path
from fractions import Fraction as F
import json
import networkx as nx
import sympy as sp

def lap(n, edges, w):
 L=sp.zeros(n)
 for (u,v),c in zip(edges,w):
  c=sp.Rational(c);L[u,u]+=c;L[v,v]+=c;L[u,v]-=c;L[v,u]-=c
 return L

def inverse_metric(L):
 n=L.rows;A=L[:n-1,:n-1].inv();P=sp.zeros(n);P[:n-1,:n-1]=A
 return lambda u,v:P[u,u]+P[v,v]-2*P[u,v]

def recover(L,baseline,oracle,root=0):
 n=L.rows;seen=set()
 def diff(u,v):
  seen.add(tuple(sorted((u,v))))
  return oracle(u,v)-baseline(u,v)
 ds={v:diff(root,v) for v in range(n) if v!=root}
 a=max(ds,key=lambda v:abs(ds[v]));sigma=sp.sign(ds[a]);assert sigma
 D={v:sigma*x for v,x in ds.items()};D[root]=0;anchor=D[a]
 z=sp.zeros(n,1)
 for v in range(n):
  if v==root:continue
  if v==a:z[v]=anchor
  else:z[v]=(anchor+D[v]-sigma*diff(a,v))/2
 b=L*z;support=[i for i in range(n) if b[i]!=0];assert len(support)==2
 u,v=support;assert b[u]==-b[v]
 alpha=sigma*b[u]**2/anchor
 change=-alpha/(1+alpha*baseline(u,v))
 assert len(seen)==2*n-3
 return (u,v),change,len(seen)

rows=[];cases=0;queries=0
for G in nx.graph_atlas_g():
 n=G.number_of_nodes()
 if n<2 or n>6 or not nx.is_connected(G):continue
 edges=sorted(G.edges());w=[sp.Rational(1+(3*u+7*v)%5) for u,v in edges]
 L=lap(n,edges,w);baseline=inverse_metric(L)
 local=0
 for i,e in enumerate(edges):
  for factor in [sp.Rational(1,2),sp.Rational(-1,2)]:
   change=w[i]*factor;wf=w.copy();wf[i]+=change
   oracle=inverse_metric(lap(n,edges,wf))
   for root in {0,n-1}:
    found,got,q=recover(L,baseline,oracle,root)
    assert found==e and got==change,(n,e,found,change,got)
    cases+=1;queries+=q;local+=1
 rows.append({'n':n,'m':len(edges),'cases':local})
result={'graphs':len(rows),'fault_root_cases':cases,'query_total':queries,'query_count_per_case':'2*n-3','exact_arithmetic':'SymPy rational grounded Laplacian inverse; algorithm uses no square roots','graph_records':rows}
p=Path(__file__).with_suffix('.json');p.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='graph_records'}))
