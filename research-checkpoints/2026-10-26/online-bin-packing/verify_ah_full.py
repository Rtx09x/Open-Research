#!/usr/bin/env python3
"""Complete AH certificate verifier. No discovery/parameter-search imports.
Reconstructs scenario partition and weights; checks exact source validity
inequalities for large threshold classes; proves both strict knapsack bounds.
Uses the separate Fraction-only target-pricing verifier, not discovery oracle.
"""
from fractions import Fraction as Q
from verify_ah_independent import price_bound
import json,sys,time

def run(path='ah_variant_full_certificate.json',output='ah_variant_full_verification.json'):
 start=time.time();d=json.load(open(path));target=Q(d['target']);old=Q(d['published_exact_target']);assert target<old
 P={int(j):{'lo':Q(p['lower']),'hi':Q(p['upper']),'alpha':{Q(i):Q(a) for i,a in p['containers']}} for j,p in d['parameters'].items()}
 assert set(P)==set(range(2,213));V={Q(0),Q(1,2)}
 for j,p in P.items():
  assert 0<=p['lo']<p['hi']<=Q(1,2)
  assert sum(p['alpha'].values())==1 and all(v>0 for v in p['alpha'].values())
  if j>2:assert p['hi']==P[j-1]['lo']
  V.update([p['lo'],p['hi']])
  for i,a in p['alpha'].items():
   volume=i if j==212 else i*p['hi'];assert 0<volume<=1;V.update([volume,1-volume])
   if j!=212:assert i.denominator==1
 assert P[2]['hi']==Q(1,2) and P[212]['lo']==0 and P[212]['hi']==Q(1,43)
 V=sorted(v for v in V if 0<=v<=Q(1,2));intervals=[];log=[]
 for sc in d['scenarios']:
  x,y,w=Q(sc['x']),Q(sc['y']),Q(sc['w']);assert 0<=w<=1;intervals.append((x,y))
  k=next(j for j,p in P.items() if p['lo']<=x and y<=p['hi'])
  large=k<=165
  if large:
   u,v=Q(sc['u']),Q(sc['v']);a=P[k]['alpha'].get(Q(1),Q(0));b=P[k]['alpha'].get(Q(2),Q(0))
   assert a+b==1 and 0<=u<=v<=1
   assert u*(a+2*b)+w*a>=1
   assert u*b+v>=1
   assert v*a+2*u*b+(1-w)*b>=1
  normal=[(1,Q(1,2),w)];heavy=[];rho=None
  for j,p in sorted(P.items()):
   if large and j==k:
    normal.extend([(j,p['lo'],u),(1000+j,x,v)]);heavy.append((j,p['lo'],u));continue
   numerator=Q(0);denominator=Q(0)
   for i,a in p['alpha'].items():
    volume=i if j==212 else i*p['hi']
    if volume>Q(1,2):
     if volume>=1-x:weight=Q(1)
     else:assert volume<=1-y;weight=w
    else:
     if volume<=x:weight=1-w
     else:assert volume>=y;weight=Q(1)
    numerator+=a*weight;denominator+=a*(i-Q(1,43) if j==212 else i)
   weight=numerator/denominator
   if j==212:rho=weight
   else:
    normal.append((j,p['lo'],weight))
    if j>=k:heavy.append((j,p['lo'],weight))
  assert 0<=rho<=2
  a=price_bound(normal,rho,Q(1),target);b=price_bound(heavy,rho,y,target-1)
  log.append({'name':sc['name'],'x':str(x),'y':str(y),'normal':a,'huge':b})
 assert sorted(intervals)==list(zip(V,V[1:]))
 result={'status':'PASS','all_scenarios':len(intervals),'target':str(target),'target_decimal':float(target),'improvement_over_published':str(old-target),'nodes':sum(q[t]['nodes'] for q in log for t in ['normal','huge']),'seconds':time.time()-start,'certificate':path}
 print(json.dumps(result,indent=2));json.dump({'summary':result,'checks':log},open(output,'w'),indent=2)
if __name__=='__main__':run(*sys.argv[1:])
