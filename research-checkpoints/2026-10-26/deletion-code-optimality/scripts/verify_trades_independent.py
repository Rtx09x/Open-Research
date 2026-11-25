"""Independent string-based reconstruction and clique-cover certificate check.
No imports from common.py/trades.py; avoids their packing decision recursion.
"""
import argparse,itertools,collections,json,time,hashlib
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--n',type=int,default=12);p.add_argument('--k',type=int,default=8);p.add_argument('--seconds',type=int,default=240);a=p.parse_args();t0=time.monotonic();n=a.n;k=a.k
words=[''.join(t) for t in itertools.product('01',repeat=n)]
D={s:frozenset(s[:i]+s[i+1:] for i in range(n)) for s in words}
B=[s for s in words if sum(i for i,b in enumerate(s,1) if b=='1')%(n+1)==0]
bset=set(B);owner={}
for i,b in enumerate(B):
 for y in D[b]:assert y not in owner;owner[y]=i
assert len(owner)==2**(n-1)
outs=[];supports=[];inc=collections.defaultdict(set)
for s in words:
 if s in bset:continue
 S=frozenset(owner[y] for y in D[s])
 if len(S)>k:continue
 mask=sum(2**i for i in S);idx=len(outs);outs.append(s);supports.append(mask)
 for i in S:inc[i].add(idx)
levels=[set() for _ in range(k+1)]
for s in supports:levels[s.bit_count()].add(s)

def members(s):
 out=[]
 while s:
  j=(s&-s).bit_length()-1;out.append(j);s-=2**j
 return out

def clique_cover(xs,limit):
 """Exact covering by at most limit pairwise-conflicting cliques.
 These classes bound any compatible selection without reusing packing DFS.
 """
 xs=sorted(xs,key=lambda s:sum(not(D[s]&D[t]) for t in xs),reverse=True)
 bins=[]
 def place(j):
  if j==len(xs):return [v[:] for v in bins]
  s=xs[j]
  for b in bins:
   if all(D[s]&D[t] for t in b):
    b.append(s);r=place(j+1)
    if r is not None:return r
    b.pop()
  if len(bins)<limit:
   bins.append([s]);r=place(j+1)
   if r is not None:return r
   bins.pop()
  return None
 return place(0)

records=[];hard=0;failures=[]
for size in range(1,k+1):
 digest=hashlib.sha256()
 for count,S in enumerate(sorted(levels[size])):
  digest.update(S.to_bytes((len(B)+7)//8,'little'))
  idxs=set()
  for b in members(S):idxs.update(inc[b])
  eligible=[outs[j] for j in idxs if supports[j]&S==supports[j]]
  # A cover into size-1 conflict cliques proves no neutral or positive trade.
  if len(eligible)>=size:
   hard+=1;cover=clique_cover(eligible,size-1)
   if cover is None:
    failures.append({'removed':[B[j] for j in members(S)],'eligible':eligible})
   else:
    assert sorted(s for b in cover for s in b)==sorted(eligible)
    assert len(cover)<size
    for b in cover:
     for s,t in itertools.combinations(b,2):assert D[s]&D[t]
  if size<k:
   for j in idxs:
    U=S|supports[j];z=U.bit_count()
    if size<z<=k:levels[z].add(U)
  if time.monotonic()-t0>a.seconds:
   print('TIMEOUT',size,count);raise SystemExit(2)
 records.append({'removed_count':size,'connected_supports':len(levels[size]),'sha256':digest.hexdigest()})
 print(records[-1],flush=True)
expected=json.load(open(f'evidence/trades_n{n}_k{k}.json'))['connected_supports']
assert records==expected,(records,expected)
out={'n':n,'k':k,'complete':True,'method':'independent string descendants; exact conflict-clique covers, each checked pairwise','support_records':records,'hard_cover_tests':hard,'uncovered_cases':failures,'seconds':time.monotonic()-t0,'no_neutral_or_improving_trade':not failures}
Path(f'evidence/independent_trades_n{n}_k{k}.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
