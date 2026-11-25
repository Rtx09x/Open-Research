#!/usr/bin/env python3
"""Exact analytic three-face certificate; no discovery code imports.
Scope: restricted two-parameter family with published analysis weights fixed.
This lower bound on certificate quality is NOT a lower bound on algorithm cost.
"""
from fractions import Fraction as Q
import json
p=json.load(open('ah_two_parameter_published_weights_certificate.json'));R=Q(p['target'])
P={int(j):{'lo':Q(r['lower']),'hi':Q(r['upper']),'a':{Q(i):Q(v) for i,v in r['containers']}} for j,r in p['parameters'].items()}
changes={d['class']:Q(d['mass']) for d in p['modifications']};delta=changes[172];eta=changes[179]
base172={Q(1):Q(48313566,191010959),Q(2):Q(24797889,191010959),Q(6):Q(117899504,191010959)}
base179={Q(2):Q(8723245,23755812),Q(10):Q(15032567,23755812)}
assert P[172]['a']=={i:a+delta*(int(i==6)-int(i==2)) for i,a in base172.items()}
assert P[179]['a']=={i:a+eta*(int(i==2)-int(i==10)) for i,a in base179.items()}
D172=sum(i*a for i,a in base172.items());D179=sum(i*a for i,a in base179.items())
x=1/(D172+4*delta);y=1/(D179-8*eta)
lines=[(Q(124762873764239,104019410288640),Q(1),Q(1)),(Q(481297903308151,298261319516160),Q(0),-Q(1,4)),(Q(142208117299,84557168640),-Q(83427088,191010959),Q(0))]
assert base172[6]-D172/4==lines[2][1]
assert base179[10]-D179/8==lines[1][2]
lam=[Q(83427088,608146399),Q(333708352,608146399),Q(191010959,608146399)]
assert all(t>0 for t in lam) and sum(lam)==1
assert sum(t*b for t,(a,b,c) in zip(lam,lines))==0
assert sum(t*c for t,(a,b,c) in zip(lam,lines))==0
assert sum(t*a for t,(a,b,c) in zip(lam,lines))==R
assert all(a+b*x+c*y==R for a,b,c in lines)

def weight(j,w,left,right):
 if j==1:return w
 r=P[j];n=Q(0);den=Q(0)
 for i,a in r['a'].items():
  vol=i if j==212 else i*r['hi']
  if vol>Q(1,2):
   if vol>=1-left:z=Q(1)
   else:assert vol<=1-right;z=w
  else:
   if vol<=left:z=1-w
   else:assert vol>=right;z=Q(1)
  n+=a*z;den+=a*(i-Q(1,43) if j==212 else i)
 return n/den
patterns=[[(167,3),(172,1),(179,1)],[(1,1),(165,1),(179,1),(205,1),(208,1),(211,1)],[(1,1),(165,1),(172,1)]]
for idx,pattern in enumerate(patterns):
 w,left,right=(Q(0),Q(49,320),Q(1,6)) if idx==0 else (Q(1),Q(3,7),Q(1,2))
 used=sum(n*(Q(1,2) if j==1 else P[j]['lo']) for j,n in pattern);assert used<1
 value=sum(n*weight(j,w,left,right) for j,n in pattern)+weight(212,w,left,right)*(1-used)
 assert value==R
print(json.dumps({'status':'PASS','target':str(R),'dual':list(map(str,lam)),'scope':'restricted certificate-family optimum, not lower bound on algorithm cost'},indent=2))
