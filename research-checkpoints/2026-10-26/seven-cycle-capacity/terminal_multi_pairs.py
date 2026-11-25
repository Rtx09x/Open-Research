#!/usr/bin/env python3
"""Select compatible equal-weight private block pairs and optimize recycled profile."""
import terminal_weighted_gadget as z
import itertools,functools,json,time,math
import numpy as np
start=time.monotonic();pairs=[(r,q) for r,q in z.pairs if z.W[r]==z.W[q]];best_delta=-1;best=None;tested=0
# Stable normalized recurrence: returns log-rate improvement above original500-dimensional code.
def gain(profile,levels=10):
 a,t,s,o,h,v=profile;t/=a;s/=a;o/=a;h/=a;v/=a;g=0
 for k in range(1,levels+1):
  excess=t*(t+2*(s-1));factor=1+excess
  if factor<=0:return -1
  g+=math.log1p(excess)/(500*2**k)
  t,s,o,h,v=2*t*o/factor,s*s/factor,(o*o+(h+v)**2)/factor,(h*o+o*v)/factor,(v*o+o*h)/factor
 return g
for X,transform in z.Xs.items():
 X=list(X);s=sum(z.W[x] for x in X);eligible=[]
 for r,q in pairs:
  if not np.any(z.adj[r,X]&z.adj[q,X]):eligible.append((r,q))
 if not eligible:continue
 vertices=[(r,q,b) for r,q in eligible for b in (0,1)];n=len(vertices);adj=[0]*n;weight=[z.W[r] for r,q,b in vertices]
 for i,(r,q,b) in enumerate(vertices):
  hi,vi=(r,q) if b==0 else(q,r)
  for j,(rr,qq,bb) in enumerate(vertices[:i]):
   hj,vj=(rr,qq) if bb==0 else(qq,rr)
   incompatible=bool(r==rr or len({r,q,rr,qq})<4 or z.adj[hi,hj] or z.adj[vi,vj] or np.any(z.adj[hi,X]&z.adj[vj,X]) or np.any(z.adj[hj,X]&z.adj[vi,X]))
   if incompatible:adj[i]|=1<<j;adj[j]|=1<<i
 @functools.lru_cache(None)
 def solve(mask):
  if not mask:return (0,0)
  ids=[i for i in range(n) if mask>>i&1];v=max(ids,key=lambda i:(adj[i]&mask).bit_count());bit=1<<v
  if not(adj[v]&mask):a,b=solve(mask^bit);return a+weight[v],b|bit
  no=solve(mask^bit);a,b=solve(mask&~(adj[v]|bit));return max(no,(a+weight[v],b|bit))
 t,mask=solve((1<<n)-1);selected=[v for i,v in enumerate(vertices) if mask>>i&1];PH=[r if b==0 else q for r,q,b in selected];PV=[q if b==0 else r for r,q,b in selected];R=[r for r,q,b in selected];B=[r for r in z.R if r not in R]
 nh=np.any(z.adj[np.ix_(PH,X)],axis=0);nv=np.any(z.adj[np.ix_(PV,X)],axis=0);assert not np.any(nh&nv);X0=[x for x,a,b in zip(X,nh,nv) if not(a or b)];XH=[x for x,a in zip(X,nh) if a];XV=[x for x,a in zip(X,nv) if a];o,h,v=[sum(z.W[x] for x in S) for S in (X0,XH,XV)];profile=(z.main,t,s,o,h,v);delta=gain(profile);tested+=1
 if delta>best_delta:
  best_delta=delta;families={'B':B,'N':X0,'A':XV,'D':XH,'O':R,'H':PH,'V':PV}
  # exact finite verification of every family and every mandatory cross separation
  for l,S in families.items():
   assert not np.any(z.adj[np.ix_(S,S)]&~np.eye(len(S),dtype=bool))
   for m in z.bpz.PERP[l]:assert not np.any(z.adj[np.ix_(S,families[m])])
  vector=[sum(z.W[x] for x in families[l]) for l in z.bpz.LABELS]
  best={'selected_pairs':[[z.words[r],z.words[q],b] for r,q,b in selected],'auxiliary_automorphism':transform,'base_dimension':500,'input_vector':z.T['n25'],'families':{l:[z.words[x] for x in S] for l,S in families.items()},'vector':vector,'profile':profile,'screened_log_rate_improvement_10levels':delta,'screened_bound':float(z.nth_root_digits(z.main,500,16))*math.exp(delta),'levels_screened':10}
  open('terminal_recycled_base.json','w').write(json.dumps(best,indent=2)+'\n');print('BEST','pairs',len(selected),'ratios',[x/z.main for x in profile],best['screened_bound'],flush=True)
print('tested',tested,'elapsed',time.monotonic()-start,flush=True)
