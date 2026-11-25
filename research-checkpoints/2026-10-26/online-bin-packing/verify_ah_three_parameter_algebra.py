#!/usr/bin/env python3
"""Independent exact two-pattern floor for the three-transfer certificate family.
Not a lower bound on actual algorithm cost. No discovery imports.
"""
from fractions import Fraction as Q
import json
J=json.load(open('ah_three_parameter_full_certificate.json'));R=Q(J['target'])
P={int(j):{'lo':Q(r['lower']),'hi':Q(r['upper']),'a':{Q(i):Q(a) for i,a in r['containers']}} for j,r in J['parameters'].items()}
changes={j['class']:Q(j['mass']) for j in J['modifications']};assert set(changes)=={167,172,179}
D0=Q(805306368,191010959);a1=Q(48313566,191010959);a6=Q(117899504,191010959);delta=changes[172]
assert P[172]['a'][Q(1)]==a1 and P[172]['a'][Q(6)]==a6+delta
X=1/sum(i*a for i,a in P[172]['a'].items());assert X==1/(D0+4*delta)

def basic(j,w,left,right):
 p=P[j];n=Q(0);d=Q(0)
 for i,a in p['a'].items():
  volume=i if j==212 else i*p['hi']
  if volume>Q(1,2):
   if volume>=1-left:z=Q(1)
   else:assert volume<=1-right;z=w
  else:
   if volume<=left:z=1-w
   else:assert volume>=right;z=Q(1)
  n+=a*z;d+=a*(i-Q(1,43) if j==212 else i)
 return n/d
w0=Q(413913,524288)
final=(Q(1),Q(3,7),Q(1,2));critical=(w0,Q(533,1600),Q(1,3))
C3=1+basic(165,*final)+basic(212,*final)/60+Q(1,4);B3=a6-D0/4
C4=w0+basic(165,*critical)+basic(212,*critical)/60;B4=1-a1*w0
assert (C3,B3)==(Q(142208117299,84557168640),-Q(83427088,191010959))
assert (C4,B4)==(Q(5162815091346603839,3718372403277987840),Q(40073570314217,50072376836096))
assert C3+B3*X==C4+B4*X==R
l3=B4/(B4-B3);l4=-B3/(B4-B3)
assert l3>0 and l4>0 and l3+l4==1
assert l3*B3+l4*B4==0 and l3*C3+l4*C4==R
assert Q(1,2)+Q(1,3)+Q(3,20)<1
for sc in [final,critical]:
 w,left,right=sc;v=w+basic(165,*sc)+basic(172,*sc)+basic(212,*sc)/60;assert v==R
print(json.dumps({'status':'PASS','target':str(R),'dual':[str(l3),str(l4)],'scope':'optimal fixed-published-weight upper certificate inside three-transfer family; not an algorithm-cost lower bound'},indent=2))
