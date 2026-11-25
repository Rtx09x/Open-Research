"""Solver-free exact maximum-code control at small n via coloring branch-and-bound."""
import argparse,itertools,json,time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--n',type=int,default=6);p.add_argument('--seconds',type=int,default=30);a=p.parse_args();n=a.n;t=time.monotonic()
words=[''.join(z) for z in itertools.product('01',repeat=n)];D=[set(s[:i]+s[i+1:] for i in range(n)) for s in words];N=len(words);adj=[0]*N
for i in range(N):
 for j in range(i):
  if not D[i]&D[j]:adj[i]|=1<<j;adj[j]|=1<<i
best=[];nodes=0

def colors(P):
 order=[];bound=[];color=0
 while P:
  color+=1;Q=P
  while Q:
   v=(Q&-Q).bit_length()-1;q=1<<v;P^=q;Q^=q;order.append(v);bound.append(color);Q&=~adj[v]
 return order,bound

def search(P,R):
 global best,nodes
 nodes+=1
 if nodes%10000==0 and time.monotonic()-t>a.seconds:raise TimeoutError
 vs,bs=colors(P)
 for i in range(len(vs)-1,-1,-1):
  if len(R)+bs[i]<=len(best):return
  v=vs[i];Q=P&adj[v]
  if Q:search(Q,R+[v])
  elif len(R)+1>len(best):best=R+[v]
  P^=1<<v
complete=True
try:search((1<<N)-1,[])
except TimeoutError:complete=False
for i,j in itertools.combinations(best,2):assert not D[i]&D[j]
vt=[s for s in words if sum(i for i,x in enumerate(s,1) if x=='1')%(n+1)==0]
out={'n':n,'complete':complete,'maximum_code_size':len(best) if complete else None,'incumbent_size':len(best),'vt_size':len(vt),'witness':[words[i] for i in best],'search_nodes':nodes,'seconds':time.monotonic()-t,'method':'exact maximum clique on compatibility graph; each coloring class is an upper-bound conflict clique'}
Path(f'evidence/small_exact_control_n{n}.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
