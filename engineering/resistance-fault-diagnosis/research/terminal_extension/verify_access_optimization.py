from pathlib import Path
from itertools import combinations
import json
ns={}; s=Path(__file__).with_name('verify_terminal_theorem.py').read_text();exec(s[:s.index('for n in range(2,6):')],ns)
comp=ns['comp'];rng=ns['rng'];count=0;sets=0;nontrivial=0

def check(n,edges):
 global count,sets,nontrivial
 if len(comp(n,edges))!=1:return
 if any(len([c for c in comp(n,[e for e in edges if v not in e]) if c!={v}])>1 for v in range(n)):return
 shores=[]
 for e,f in combinations(range(len(edges)),2):
  cc=comp(n,edges,{e,f})
  if len(cc)>1:assert len(cc)==2;shores.append(cc[0])
 signatures={v:tuple(v in shore for shore in shores) for v in range(n)}
 groups={}
 for v,k in signatures.items():groups.setdefault(k,[]).append(v)
 ids={v:i for i,g in enumerate(groups.values()) for v in g};deg=[0]*len(groups)
 for u,v in edges:
  if ids[u]!=ids[v]:deg[ids[u]]+=1;deg[ids[v]]+=1
 required=[set(g) for i,g in enumerate(groups.values()) if deg[i]==2]
 if len(groups)>1:nontrivial+=1;assert len(required)>=2
 for k in range(2,n+1):
  for BB in combinations(range(n),k):
   B=set(BB);valid=all(B&shore and B-set(shore) for shore in shores)
   predicted=all(B&g for g in required)
   assert valid==predicted,(n,edges,B,groups,deg,shores)
   sets+=1
 assert (2 if len(groups)==1 else len(required))==min(k for k in range(2,n+1) if any(all(set(B)&shore and set(B)-set(shore) for shore in shores) for B in combinations(range(n),k)))
 count+=1
for n in range(3,6):
 possible=list(combinations(range(n),2))
 for mask in range(1,1<<len(possible)):check(n,[e for i,e in enumerate(possible) if mask&(1<<i)])
for _ in range(500):
 n=rng.randrange(5,10);check(n,[e for e in combinations(range(n),2) if rng.random()<.42])
out={'biconnected_graphs':count,'terminal_sets_checked':sets,'nontrivial_cactus_quotients':nontrivial,'failures':0};print(json.dumps(out,indent=2));Path(__file__).with_name('access_verification.json').write_text(json.dumps(out,indent=2)+'\n')
