#!/usr/bin/env python3
"""Independent Fraction-only verification of exported AH proof certificate.
Does not import discovery/pricing/optimization modules. It reconstructs all item
weights from rational algorithm parameters, verifies every affected scenario,
and checks the unchanged published scenario bounds against the new target.
The pricing recursion is size-ordered, not the discovery oracle's integer-scaled
density order, and proves a supplied target rather than optimizing an objective.
"""
from fractions import Fraction as Q
import json,time

def price_bound(items,density,capacity,target):
 # Reduced profit accounts exactly for filling remaining capacity with tiny sand.
 raw=[(j,s,w-density*s) for j,s,w in items if s<capacity and w-density*s>0]
 keep=[]
 for j,s,p in raw:
  if any(s2<=s and p2>=p and (s2<s or p2>p or j2<j) for j2,s2,p2 in raw):continue
  keep.append((j,s,p))
 keep.sort(key=lambda a:a[1],reverse=True)
 suffix=[Q(0)]*(len(keep)+1)
 for i in range(len(keep)-1,-1,-1):suffix[i]=max(suffix[i+1],keep[i][2]/keep[i][1])
 allowance=target-density*capacity;nodes=0;leaves=0
 assert allowance>=0
 def visit(i,left,profit):
  nonlocal nodes,leaves
  nodes+=1
  assert profit<=allowance
  if profit+suffix[i]*left<=allowance:leaves+=1;return
  assert i<len(keep)
  _,size,gain=keep[i]
  # q*size < left, strictly; all omitted space is tiny sand.
  quotient=left/size;maxq=(quotient.numerator-1)//quotient.denominator
  for q in range(maxq+1):visit(i+1,left-q*size,profit+q*gain)
 visit(0,capacity,Q(0))
 return {'nodes':nodes,'pruned_leaves':leaves,'retained_items':len(keep)}

def run(path='ah_exact_certificate.json'):
 d=json.load(open(path));w=Q(d['new_w']);target=Q(d['target']);old=Q(d['published_exact_target']);assert 0<w<1 and target<old
 par={int(j):{'lower':Q(p['lower']),'upper':Q(p['upper']),'containers':[(Q(i),Q(a)) for i,a in p['containers']]} for j,p in d['parameters'].items()}
 assert set(par)==set(range(2,213))
 for j,p in par.items():
  assert 0<=p['lower']<p['upper']<=Q(1,2)
  assert sum(a for i,a in p['containers'])==1 and all(a>0 for i,a in p['containers'])
  if j>2:assert p['upper']==par[j-1]['lower']
 assert par[2]['upper']==Q(1,2) and par[212]['lower']==0 and par[212]['upper']==Q(1,43)
 logs=[]
 for sc in d['scenarios']:
  ell=sc['ell'];x=Q(sc['x']);y=Q(sc['y']);assert x==Q(3,10)+Q(ell-1,4800) and y==x+Q(1,4800)
  items=[(1,Q(1,2),w)];rho=None
  for j,p in sorted(par.items()):
   numerator=Q(0);denominator=Q(0)
   for i,a in p['containers']:
    volume=i if j==212 else i*p['upper']
    if volume>Q(1,2):
     if volume>=1-x:required=Q(1)
     else:assert volume<=1-y;required=w
    else:
     if volume<=x:required=1-w
     else:assert volume>=y;required=Q(1)
    numerator+=a*required;denominator+=a*(i-Q(1,43) if j==212 else i)
   weight=numerator/denominator
   if j==212:rho=weight
   else:items.append((j,p['lower'],weight))
  stored=[(int(j),Q(s),Q(z)) for j,s,z in sc['items']]
  assert stored==items and rho==Q(sc['rho'])
  normal=price_bound(items,rho,Q(1),target)
  huge=price_bound([a for a in items if a[0]>=166],rho,y,target-1)
  logs.append({'ell':ell,'normal':normal,'huge':huge})
 assert sorted(sc['ell'] for sc in d['scenarios'])==list(range(1,161))
 assert all(Q(z)<target for z in d['unchanged_bounds'])
 result={'status':'PASS','scenarios':len(logs),'supplied_target':str(target),'nodes':sum(z[k]['nodes'] for z in logs for k in ['normal','huge']),'strict_improvement':str(old-target),'unchanged_published_bounds':len(d['unchanged_bounds'])}
 print(json.dumps(result,indent=2));json.dump({'summary':result,'checks':logs},open('ah_independent_verification.json','w'),indent=2)
if __name__=='__main__':run()
