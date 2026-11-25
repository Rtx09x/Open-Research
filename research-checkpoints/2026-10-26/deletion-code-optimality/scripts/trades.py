"""Exhaust all connected supports of replacement trades of radius at most k.
Pure integer exact search, no floating-point/MILP inference. See trade_lemma.md.
"""
import argparse,collections,itertools,json,time,hashlib
from pathlib import Path
from common import vt,descendants
p=argparse.ArgumentParser();p.add_argument('--n',type=int,default=12);p.add_argument('--k',type=int,default=4);p.add_argument('--seconds',type=int,default=240);a=p.parse_args();n=a.n;k=a.k;t0=time.monotonic()
base=vt(n);bset=set(base);owner={y:i for i,x in enumerate(base) for y in descendants(x,n)}
balls={x:sum(1<<y for y in descendants(x,n)) for x in range(1<<n)}
groups=collections.defaultdict(list)
for x in range(1<<n):
 if x not in bset:
  s=tuple(sorted({owner[y] for y in descendants(x,n)}))
  if len(s)<=k:groups[s].append(x)
edges=[sum(1<<i for i in s) for s in groups];incident=collections.defaultdict(list)
for e in edges:
 for i in range(len(base)):
  if e>>i&1:incident[i].append(e)
levels=[set() for _ in range(k+1)]
for e in edges:levels[e.bit_count()].add(e)
records=[];neutral=[];positive=[];checked=0;eligible_tests=0

def bits(s):
 while s:
  q=s&-s;s^=q;yield q.bit_length()-1

def packing(xs,target):
 """Decision DFS. Pairwise deletion-ball disjointness is sufficient and exact."""
 def dfs(cands,chosen):
  if len(chosen)>=target:return chosen
  while len(cands)+len(chosen)>=target:
   x=cands.pop()
   result=dfs([y for y in cands if not( balls[x]&balls[y])],chosen+[x])
   if result:return result
  return None
 return dfs(xs[:],[])

for m in range(1,k+1):
 total=len(levels[m]);digest=hashlib.sha256()
 for si,S in enumerate(sorted(levels[m])):
  ids=list(bits(S));digest.update(S.to_bytes((len(base)+7)//8,'little'))
  xs=[]
  for j in range(1,m+1):
   for sub in itertools.combinations(ids,j):xs.extend(groups.get(sub,()))
  checked+=1
  if len(xs)>=m+1:
   eligible_tests+=1
   witness=packing(xs,m+1)
   if witness:
    positive.append({'removed':[base[i] for i in ids],'added':witness});break
  if len(neutral)<20 and len(xs)>=m:
   witness=packing(xs,m)
   if witness:neutral.append({'removed':[base[i] for i in ids],'added':witness})
  if m<k:
   possible=set(e for i in ids for e in incident[i])
   for e in possible:
    U=S|e;size=U.bit_count()
    if m<size<=k:levels[size].add(U)
  if time.monotonic()-t0>a.seconds:
   out={'complete':False,'n':n,'k':k,'completed_levels':records,'current_size':m,'current_processed':si+1,'current_total':total,'seconds':time.monotonic()-t0,'reason':'time_budget','positive':positive,'neutral_examples':neutral}
   Path(f'evidence/trades_n{n}_k{k}.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));raise SystemExit(2)
 records.append({'removed_count':m,'connected_supports':total,'sha256':digest.hexdigest()})
 print(json.dumps(records[-1]),flush=True)
 if positive:break
out={'complete':not positive,'n':n,'k':k,'connected_supports':records,'checked':checked,'eligible_improvement_tests':eligible_tests,'positive':positive,'neutral_examples':neutral,'seconds':time.monotonic()-t0,'claim':f'No improving trade removing at most {k} words of VT0({n})' if not positive else 'Candidate improving trade: verify independently'}
Path(f'evidence/trades_n{n}_k{k}.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
