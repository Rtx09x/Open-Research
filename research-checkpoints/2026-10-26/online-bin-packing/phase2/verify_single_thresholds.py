#!/usr/bin/env python3
"""Fraction-only all-case/continuous-family certificate checker.
No optimizer or Pro imports. Raw-weight size frontier and SIZE-order target
search are different from the integer reduced-profit maximization discovery.
"""
from fractions import Fraction as Q
from pathlib import Path
import json,time,hashlib
H=Path(__file__).resolve().parent;D=Q(1,43)
def G(r,c):
 q,e=divmod(r,D);return r+q*(D-c)+max(Q(0),e-c)
def pricing(items,cap,rho,c,target,offset):
 frontier=[];largest=-Q(1)
 for j,s,w in sorted(items,key=lambda t:(t[1],-t[2],t[0])):
  if w<=largest:continue
  largest=w
  if s<cap and w>rho*s:frontier.append((j,s,w))
 frontier.sort(key=lambda t:t[1],reverse=True)
 suffix=[rho*(2-c/D)]*(len(frontier)+1)
 for i in range(len(frontier)-1,-1,-1):suffix[i]=max(suffix[i+1],frontier[i][2]/frontier[i][1])
 nodes=0
 def visit(i,room,value):
  nonlocal nodes
  nodes+=1;assert offset+value+rho*G(room,c)<=target
  if i==len(frontier) or offset+value+room*suffix[i]<=target:return
  j,s,w=frontier[i];n=0
  while n*s<room:visit(i+1,room-n*s,value+n*w);n+=1
 visit(0,cap,Q(0));return nodes

def weights(P,s):
 x,y,w,c=map(Q,[s['x'],s['y'],s['w'],s['c']]);assert 0<=w<=1 and 0<=c<=D
 k=next(j for j,r in P.items() if r['lo']<=x and y<=r['hi']);big=k<=165
 if big:
  u,v=Q(s['u']),Q(s['v']);al=P[k]['alpha'].get(Q(1),Q(0));be=P[k]['alpha'][Q(2)]
  assert 0<=u<=v<=1 and u*(al+2*be)+w*al>=1 and u*be+v>=1 and v*al+2*u*be+(1-w)*be>=1
 N=[(1,Q(1,2),w)];HUGE=[];B=b=None
 for j,r in sorted(P.items()):
  if big and j==k:
   N.extend([(j,r['lo'],u),(1000+j,x,v)]);HUGE.append((j,r['lo'],u));continue
  charge=mean=Q(0)
  for i,al in r['alpha'].items():
   vol=i if j==212 else i*r['hi']
   if vol>Q(1,2):
    if vol>=1-x:rw=Q(1)
    else:assert vol<=1-y;rw=w
   else:
    if vol<=x:rw=1-w
    else:assert vol>=y;rw=Q(1)
   charge+=al*rw;mean+=al*i
  if j==212:B=mean;b=charge
  else:
   N.append((j,r['lo'],charge/mean))
   if j>=k:HUGE.append((j,r['lo'],charge/mean))
 assert B>D
 return N,HUGE,B,b,c,y

def run():
 start=time.time();J=json.loads((H/'single_threshold_certificate.json').read_text());frozen=H.parent/'ah_three_parameter_full_certificate.json';F=json.loads(frozen.read_text())
 assert hashlib.sha256(frozen.read_bytes()).hexdigest()==J['frozen_parameter_certificate_sha256']
 assert J['parameters']==F['parameters'];R=Q(J['target']);assert R<Q(J['pro_target'])<Q(F['target'])
 P={int(j):{'lo':Q(r['lower']),'hi':Q(r['upper']),'alpha':{Q(i):Q(a) for i,a in r['containers']}} for j,r in J['parameters'].items()}
 V={Q(0),Q(1,2)}
 for j,r in P.items():
  assert sum(r['alpha'].values())==1 and all(v>0 for v in r['alpha'].values());V.update([r['lo'],r['hi']])
  for i in r['alpha']:
   v=i if j==212 else i*r['hi'];assert D<=v<=1;V.update([v,1-v])
 V=sorted(v for v in V if 0<=v<=Q(1,2));intervals=[];logs=[];duals=[]
 ref={(s['x'],s['y']):s for s in F['scenarios']}
 for s in J['scenarios']:
  intervals.append((Q(s['x']),Q(s['y'])))
  assert all(s.get(k)==ref[(s['x'],s['y'])].get(k) for k in ['u','v','w'])
  N,HUGE,B,b,c,y=weights(P,s);target=Q(s.get('target',J['target']));assert target<=R
  counts=[pricing(N,Q(1),b/(B-c),c,target,0),pricing(HUGE,y,b/(B-c),c,target,1)]
  logs.append({'x':s['x'],'y':s['y'],'c':s['c'],'target':str(target),'nodes':counts})
  if 'dual_patterns' in s:
   rows=s['dual_patterns'];assert sum(Q(t['lambda_weight']) for t in rows)==1 and all(Q(t['lambda_weight'])>=0 for t in rows)
   parsed=[]
   for row in rows:
    huge=row['huge'];look={j:(sz,w) for j,sz,w in (HUGE if huge else N)};cap=y if huge else Q(1)
    residual=cap-sum(look[j][0]*n for j,n in row['pattern']);assert residual>0 and residual==Q(row['residual'])
    const=int(huge)+sum(look[j][1]*n for j,n in row['pattern']);assert const==Q(row['constant'])
    parsed.append((Q(row['lambda_weight']),residual,const))
   breaks={Q(0),D}|{r%D for l,r,a in parsed}
   def dualvalue(z):return sum(l*(a+b/(B-z)*G(r,z)) for l,r,a in parsed)
   assert all(dualvalue(z)>=target for z in breaks) and dualvalue(c)==target
   # Pointwise Jensen reduction verified at all breakpoints of the item-size
   # piecewise-linear functions; between them the difference is affine.
   mix=[(Q(z),Q(t)) for z,t in s['dominated_mixture']];assert sum(t for z,t in mix)==1
   assert sum(t/(B-z) for z,t in mix)==1/(B-c)
   for size in {Q(0),D,c}|{z for z,t in mix}:
    f=lambda z:b/(B-z)*(size+max(Q(0),size-z))
    assert f(c)<=sum(t*f(z) for z,t in mix)
   duals.append({'x':s['x'],'y':s['y'],'target':str(target),'continuous_c_breakpoints':len(breaks)})
 assert sorted(intervals)==list(zip(V,V[1:])) and len(logs)==402 and len(duals)==3
 out={'status':'PASS','target':str(R),'target_decimal':float(R),'improvement_over_Pro':str(Q(J['pro_target'])-R),'scenarios':len(logs),'knapsacks':2*len(logs),'continuous_family_optimum_certificates':duals,'nodes':sum(sum(z['nodes']) for z in logs),'seconds':time.time()-start,'checks':logs}
 (H/'single_threshold_verification.json').write_text(json.dumps(out,indent=2));print({k:v for k,v in out.items() if k!='checks'})
if __name__=='__main__':run()
