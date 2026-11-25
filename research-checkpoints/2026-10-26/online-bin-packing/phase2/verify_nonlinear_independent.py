#!/usr/bin/env python3
"""Independent phase-2 verifier; no Pro or discovery imports.
Reads frozen phase-1 parameters, reconstructs all 402 scenarios and weights,
and verifies nonlinear residual fill using integer-scaled reduced profits.
This differs from Pro's raw-weight dominance/Fraction density or size search.
"""
from fractions import Fraction as Q
from pathlib import Path
import json,math,time,argparse
HERE=Path(__file__).resolve().parent
RNEW=Q(87931323061219230147063794829048504459349,55715094120735551199336133222286481162240)
D=Q(1,43)

def check_price(items,cap,a,b,c,target,offset=0):
 S=math.lcm(cap.denominator,D.denominator,c.denominator,*[s.denominator for j,s,w in items])
 W=math.lcm(a.denominator,b.denominator,target.denominator,*[w.denominator for j,s,w in items])
 C=int(cap*S);dd=int(D*S);cc=int(c*S);aa=int(a*W);bb=int(b*W)
 limit=int((target-offset)*W*S)-aa*C
 raw=[]
 for j,s,w in items:
  size=int(s*S);gain=int(w*W)*S-aa*size
  if 0<size<C and gain>0:raw.append((j,size,gain))
 # A replacement no larger and with at least as much reduced profit leaves
 # at least as much residual hinge charge, since that charge is nondecreasing.
 keep=[t for t in raw if not any(u[1]<=t[1] and u[2]>=t[2] and (u[1]<t[1] or u[2]>t[2] or u[0]<t[0]) for u in raw)]
 keep.sort(key=lambda t:Q(t[2],t[1]),reverse=True)
 def excess(space):
  q,e=divmod(space,dd);return q*(dd-cc)+max(0,e-cc)
 nodes=0;max_seen=-1;path=[]
 def visit(i,space,value):
  nonlocal nodes,max_seen
  nodes+=1;val=value+bb*excess(space);max_seen=max(max_seen,val)
  assert val<=limit,('counterexample',str(Q(aa*C+val,W*S)+offset),path, str(Q(space,S)))
  if i==len(keep):return
  j,size,gain=keep[i]
  upper=max(Q(gain,size),Q(bb*(dd-cc),dd))
  if value*upper.denominator+space*upper.numerator<=limit*upper.denominator:return
  for n in range((space-1)//size,-1,-1):
   if n:path.append((j,n))
   visit(i+1,space-n*size,value+n*gain)
   if n:path.pop()
 visit(0,C,0)
 return {'nodes':nodes,'retained':len(keep),'largest_visited':str(Q(aa*C+max_seen,W*S)+offset)}

def reconstruct(P,sc):
 x,y,w=map(Q,(sc['x'],sc['y'],sc['w']));assert 0<=w<=1
 k=next(j for j,p in P.items() if p['lo']<=x and y<=p['hi']);large=k<=165
 if large:
  u,v=Q(sc['u']),Q(sc['v']);al=P[k]['a'].get(Q(1),Q(0));be=P[k]['a'][Q(2)]
  assert 0<=u<=v<=1 and u*(al+2*be)+w*al>=1 and u*be+v>=1 and v*al+2*u*be+(1-w)*be>=1
 normal=[(1,Q(1,2),w)];huge=[]
 for j,p in sorted(P.items()):
  if j==k and large:
   normal.extend([(j,p['lo'],u),(1000+j,x,v)]);huge.append((j,p['lo'],u));continue
  count=Q(0);charge=Q(0);meanvolume=Q(0)
  for i,al in p['a'].items():
   vol=i if j==212 else i*p['hi'];meanvolume+=al*vol
   if vol>Q(1,2):
    if vol>=1-x:rw=Q(1)
    else:assert vol<=1-y;rw=w
   else:
    if vol<=x:rw=1-w
    else:assert vol>=y;rw=Q(1)
   charge+=al*rw;count+=al*i
  if j==212:
   B=meanvolume;required=charge;continue
  normal.append((j,p['lo'],charge/count))
  if j>=k:huge.append((j,p['lo'],charge/count))
 selected=(x,y) in [(Q(533,1600),Q(1,3)),(Q(3,7),Q(1,2))]
 c=Q(1,60) if selected else D;theta=Q(7,60) if selected else Q(0)
 assert B>D
 a=(1-theta)*required/(B-D)+theta*required/(B-c)
 b=theta*required/(B-c)
 return normal,huge,a,b,c,y

def run(target=RNEW):
 start=time.time();d=json.loads((HERE.parent/'ah_three_parameter_full_certificate.json').read_text())
 P={int(j):{'lo':Q(p['lower']),'hi':Q(p['upper']),'a':{Q(i):Q(a) for i,a in p['containers']}} for j,p in d['parameters'].items()}
 assert set(P)==set(range(2,213));points={Q(0),Q(1,2)}
 for j,p in P.items():
  assert sum(p['a'].values())==1 and all(a>0 for a in p['a'].values())
  points.update([p['lo'],p['hi']])
  for i in p['a']:
   v=i if j==212 else i*p['hi'];assert D<=v<=1;points.update([v,1-v])
 points=sorted(v for v in points if 0<=v<=Q(1,2))
 assert sorted((Q(s['x']),Q(s['y'])) for s in d['scenarios'])==list(zip(points,points[1:]))
 logs=[]
 for sc in d['scenarios']:
  normal,huge,a,b,c,y=reconstruct(P,sc)
  logs.append({'x':sc['x'],'y':sc['y'],'a':str(a),'b':str(b),'c':str(c),'normal':check_price(normal,Q(1),a,b,c,target),'huge':check_price(huge,y,a,b,c,target,1)})
 # Independently exhibit exact unchanged-scenario equality, not just a target.
 sc=next(s for s in d['scenarios'] if Q(s['x'])==Q(49,320) and Q(s['y'])==Q(1,6))
 n,h,a,b,c,y=reconstruct(P,sc);lookup={j:w for j,s,w in n};assert b==0
 witness=3*lookup[167]+lookup[172]+lookup[179]+a/110;assert witness==RNEW
 out={'status':'PASS','target':str(target),'equality_witness':str(witness),'scenarios':len(logs),'knapsacks':2*len(logs),'nodes':sum(q[k]['nodes'] for q in logs for k in ['normal','huge']),'seconds':time.time()-start,'checks':logs}
 (HERE/'independent_nonlinear_check.json').write_text(json.dumps(out,indent=2));print({k:v for k,v in out.items() if k!='checks'})
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--target',default=str(RNEW));run(Q(p.parse_args().target))
