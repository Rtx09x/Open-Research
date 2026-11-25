#!/usr/bin/env python3
"""Exact adversarial stress checks supplementing analytic tiny-charge proofs.
No Pro code imports. Finite tests are falsification aids, not general proofs.
"""
from fractions import Fraction as Q
from pathlib import Path
import json,time
H=Path(__file__).resolve().parent;start=time.time()
# Integer-grid exact maximum over ALL compositions, checked against envelope.
fill_checks=0
for d in [12,60,110]:
 for c in (range(d+1) if d<=60 else [0,1,42,43,44,109,110]):
  dp=[0]*(3*d+1)
  for r in range(1,len(dp)):
   dp[r]=max(dp[r-s]+s+max(0,s-c) for s in range(1,min(d,r)+1))
   q,e=divmod(r,d);assert dp[r]==r+q*(d-c)+max(0,e-c)
   fill_checks+=1
# Published tiny capacities/proportions, integer scale2580.
S=2580;d=60;A=[731,2580];den=32568497273;al=[13701867480,18866629793];B=sum(a*v for a,v in zip(al,A))
assert sum(al)==den and min(A)>=d
cs=[0,1,30,43,59,60];checked=0;closed=0
for seed in range(50):
 n=[0,0];m=0;load=0;typ=None;T=0;E=[0]*len(cs);trigger_total=0;z=seed+1
 for step in range(5000):
  z=(1103515245*z+12345)%2147483648
  s=1 if seed==0 else 60 if seed==1 else (1 if step%2 else 60) if seed==2 else 1+z%60
  if typ is None or load+s>A[typ]:
   if typ is not None:
    assert A[typ]-load<s;trigger_total+=s;closed+=1
   typ=next(i for i in range(2) if n[i]*den<=al[i]*m)
   n[typ]+=1;m+=1;load=0
  load+=s;T+=s
  assert load<=A[typ] and all(n[i]*den-al[i]*m<=den for i in range(2))
  cap=sum(a*b for a,b in zip(A,n));assert cap-T<=trigger_total+S
  for k,c in enumerate(cs):
   E[k]+=max(0,s-c);assert cap-T<=c*m+E[k]+S
   divisor=B-c*den
   for r in [(1,0),(0,1),(1,1)]:
    req=sum(a*b for a,b in zip(r,n));bnum=sum(a*b for a,b in zip(r,al))
    assert req*divisor<=bnum*(T+E[k]+2*S)+divisor
  checked+=1
# Concrete counterexample if the stronger charge were incorrectly assigned to
# original AH's proactive closure: all items have size1/2580, c=1/60.
n=[0,0]
for m in range(1000):
 i=next(i for i in range(2) if n[i]*den<=al[i]*m);n[i]+=1
T=sum(n[i]*(A[i]-d+1) for i in range(2));c=43
rho=Q(S*den,B-c*den);claimed=rho*Q(T,S)+rho*2+1
assert claimed<1000
out={'status':'PASS','grid_fill_cases':fill_checks,'published_parameter_stream_prefixes':checked,'overflow_events':closed,'original_proactive_rule_counterexample':{'containers':1000,'item_size':'1/2580','c':'1/60','claimed_charge_with_constant':str(claimed),'deficit':str(1000-claimed)},'seconds':time.time()-start,'scope':'finite stress tests plus counterexample to reusing overflow charge for unmodified AH; analytic proof is separate'}
(H/'tiny_lemma_stress.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
