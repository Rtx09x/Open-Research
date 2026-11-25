"""Independent checks: simple-path signatures vs augmented-block cutpairs vs exact electrical responses."""
from fractions import Fraction as F
from itertools import combinations
from random import Random
import json
from pathlib import Path
rng=Random(20261008)
def adj(n,edges):
 a=[[] for _ in range(n)]
 for i,(u,v) in enumerate(edges): a[u].append((v,i));a[v].append((u,i))
 return a
def comp(n,edges,skip=()):
 a=adj(n,edges);out=[];seen=set()
 for root in range(n):
  if root in seen:continue
  c={root};seen.add(root);st=[root]
  while st:
   u=st.pop()
   for v,i in a[u]:
    if i not in skip and v not in seen:seen.add(v);c.add(v);st.append(v)
  out.append(c)
 return out
def paths(n,edges,s,t):
 a=adj(n,edges);out=[]
 def go(u,seen,mask):
  if u==t:out.append(mask);return
  for v,i in a[u]:
   if v not in seen:go(v,seen|{v},mask|(1<<i))
 go(s,{s},0);return out
def block_z(n,edges,B):
 aug=edges+[(n,b) for b in B];a=adj(n+1,aug);disc={};low={};stack=[];blocks=[]
 def dfs(u,parent=-1):
  disc[u]=low[u]=len(disc)
  for v,e in a[u]:
   if e==parent:continue
   if v not in disc:
    stack.append(e);dfs(v,e);low[u]=min(low[u],low[v])
    if low[v]>=disc[u]:
     block=[]
     while True:
      f=stack.pop();block.append(f)
      if f==e:break
     blocks.append(block)
   elif disc[v]<disc[u]:stack.append(e);low[u]=min(low[u],disc[v])
 dfs(n)
 candidates=[b for b in blocks if any(i>=len(edges) for i in b)]
 assert len(candidates)==1
 ids=candidates[0];return aug,ids

def resistance(n,edges,c,deleted,s,t):
 cc=next(x for x in comp(n,edges,{deleted}) if s in x)
 if t not in cc:return None
 vertices=sorted(cc-{t});idx={v:i for i,v in enumerate(vertices)};d=len(vertices)
 M=[[F(0) for _ in range(d+1)] for _ in range(d)];M[idx[s]][-1]=1
 for i,(u,v) in enumerate(edges):
  if i==deleted or u not in cc:continue
  for x,y in ((u,v),(v,u)):
   if x!=t:
    M[idx[x]][idx[x]]+=c[i]
    if y!=t:M[idx[x]][idx[y]]-=c[i]
 for j in range(d):
  k=next(k for k in range(j,d) if M[k][j]);M[j],M[k]=M[k],M[j];z=M[j][j];M[j]=[x/z for x in M[j]]
  for k in range(d):
   if k!=j:
    z=M[k][j]
    if z:M[k]=[a-z*b for a,b in zip(M[k],M[j])]
 return M[idx[s]][-1]

stats={'graphs':0,'terminal_sets':0,'edge_pair_comparisons':0,'electrical_pair_queries':0,'accidental_collisions':0}
def check(n,edges,allB=True,electric=False):
 if len(comp(n,edges))>1:return
 stats['graphs']+=1
 pp={(s,t):paths(n,edges,s,t) for s,t in combinations(range(n),2)}
 bs=[B for k in range(2,n+1) for B in combinations(range(n),k)] if allB else [tuple(sorted(rng.sample(range(n),rng.randrange(2,n+1)))) for _ in range(6)]
 for B in bs:
  p=[mask for st in combinations(B,2) for mask in pp[st]];sig=[tuple(bool(mask&(1<<e)) for mask in p) for e in range(len(edges))]
  aug,H=block_z(n,edges,B);he=[aug[i] for i in H];orig={e for e in H if e<len(edges)};index={e:i for i,e in enumerate(H)}
  base=len(comp(n+1,he))
  for e,f in combinations(range(len(edges)),2):
   predicted=(e not in orig and f not in orig) or (e in orig and f in orig and len(comp(n+1,he,{index[e],index[f]}))>base)
   assert predicted==(sig[e]==sig[f]),(n,edges,B,e,f,predicted)
   stats['edge_pair_comparisons']+=1
  stats['terminal_sets']+=1
 if electric:
  c=[rng.randrange(1,1000000) for _ in edges]
  for (s,t),p in pp.items():
   sig=[tuple(bool(mask&(1<<e)) for mask in p) for e in range(len(edges))]
   rr=[resistance(n,edges,c,e,s,t) for e in range(len(edges))]
   for e,f in combinations(range(len(edges)),2):
    if sig[e]==sig[f]:assert rr[e]==rr[f],('universal mismatch',n,edges,s,t,e,f)
    elif rr[e]==rr[f]:stats['accidental_collisions']+=1
   stats['electrical_pair_queries']+=1
for n in range(2,6):
 potential=list(combinations(range(n),2))
 for mask in range(1,1<<len(potential)):
  edges=[e for i,e in enumerate(potential) if mask&(1<<i)]
  check(n,edges,electric=(n<=4))
for _ in range(120):
 n=rng.randrange(5,9);edges=[e for e in combinations(range(n),2) if rng.random()<0.4]
 check(n,edges,allB=False,electric=True)
print(json.dumps(stats,indent=2))
Path(__file__).with_name('verification.json').write_text(json.dumps(stats,indent=2)+'\n')
