#!/usr/bin/env python3
"""Exact saturation-family identities and explicit tiny/offline trace checks.
No Pro or numerical-optimizer imports. Full AH cost lower bound is proved from
source quota invariants, not inferred by extrapolating the finite traces.
"""
from fractions import Fraction as Q
from pathlib import Path
import json,math,time
H=Path(__file__).resolve().parent;start=time.time()
J=json.loads((H.parent/'single_threshold_certificate.json').read_text());R=Q(J['target'])
P={int(j):{'lo':Q(r['lower']),'hi':Q(r['upper']),'a':{Q(i):Q(a) for i,a in r['containers']}} for j,r in J['parameters'].items()}
D=Q(1,43);rp=Q(997,2100120);rq=Q(29,1254)
PP=[165,179,205,208,211];QQ=[165,179,187]
assert Q(1,2)+sum(P[j]['lo'] for j in PP)+rp==1
assert Q(1,2)+sum(P[j]['lo'] for j in QQ)+rq==1
B=sum(i*a for i,a in P[212]['a'].items());b=sum(a for i,a in P[212]['a'].items() if i>Q(1,2))
positive={};negative={};Cs=Q(0)
for j in sorted(set(PP+QQ)):
 mean=sum(i*a for i,a in P[j]['a'].items());beta=sum(a for i,a in P[j]['a'].items() if i*P[j]['hi']>Q(1,2));positive[j]=beta/mean;negative[j]=(1-beta)/mean
 if j!=165:Cs+=(len(P[j]['a'])-1)*(positive[j]*max(P[j]['a'])+1)
Kp=1+sum(positive[j] for j in PP);Kq=1+sum(positive[j] for j in QQ)
c=Q(next(s['c'] for s in J['scenarios'] if s['x']=='3/7' and s['y']=='1/2'));rho=b/(B-c)
Z=B-2*rq+rp;theta=rp/Z
assert Kp+rho*rp==Kq+rho*(2*rq-c)==R
assert Kq+b-Kp==rho*Z
assert (1-theta)*Kp+theta*(Kq+b)==R
assert theta==Q(616945043842439,848239837141104679)
neg=negative[165]+negative[179]+(1-theta)*sum(negative[j] for j in [205,208,211])+theta*negative[187]+(1-b)*theta
assert neg<1
T=Q(1,1000000)
for j in set(PP+QQ):assert P[j]['lo']+T<=P[j]['hi']
assert 0<rp-6*T<rp<c<rq-4*T<rq<D
assert min(P[212]['a'])-2*rq>0 and T<rq-4*T
assert max([P[165]['hi']]+[i*P[j]['hi'] for j in [179,187,205,208,211] for i in P[j]['a'] if i*P[j]['hi']<=Q(1,2)]+[Q(17,60)])+Q(1,2)+T<1
C=Cs+3 # class165 loss<=2, tiny positive count loss<1.

capacities=sorted(P[212]['a']);alpha=[P[212]['a'][a] for a in capacities]
def newtype(n):return next(i for i in range(len(n)) if n[i]*alpha[i].denominator<=alpha[i].numerator*sum(n))
def trace(m,tau):
 p=rp-6*tau;q=rq-4*tau
 scale=math.lcm(p.denominator,q.denominator,tau.denominator,D.denominator,*[a.denominator for a in capacities],*[P[j]['lo'].denominator for j in set(PP+QQ)],2)
 A=[int(a*scale) for a in capacities];pp=int(p*scale);qq=int(q*scale);tt=int(tau*scale);dd=int(D*scale)
 n=[0,0];plan=[]
 for z in range(m):i=newtype(n);n[i]+=1;plan.append(i)
 fills=[A[i]-2*qq+tt for i in plan];F=sum(fills);np=(F+pp-1)//pp;slack=np*pp-F
 assert 0<=slack<pp<scale and min(fills)>0
 # Actual streaming Next Fit simulation with original minimum-index quota.
 actual=[0,0];opened=0;typ=None;load=0;triggers=0;pieces=0;mass=0;bucket=0;remaining=pp
 def put(size):
  nonlocal opened,typ,load,triggers,mass
  assert 0<size<=dd
  if typ is None or load+size>A[typ]:
   if typ is not None:assert A[typ]-load<size;triggers+=1
   typ=newtype(actual);actual[typ]+=1;opened+=1;load=0
  load+=size;mass+=size;assert load<=A[typ]
 for z,(i,filler) in enumerate(zip(plan,fills)):
  put(qq);assert opened==z+1 and typ==i and load==qq
  left=filler
  while left:
   piece=min(left,remaining);put(piece);pieces+=1;left-=piece;remaining-=piece
   assert opened==z+1
   if remaining==0:bucket+=1;remaining=pp
  assert load==A[i]-qq+tt and load<A[i]
 assert opened==m and actual==n and triggers==m-1 and mass==F+m*qq
 assert bucket+(remaining<pp)==np
 N=np+m
 non_tiny=Q(N)*(Q(1,2)+tau+P[165]['lo']+tau+P[179]['lo']+tau)
 non_tiny+=np*sum(P[j]['lo']+tau for j in [205,208,211])+m*(P[187]['lo']+tau)
 total_volume=non_tiny+Q(mass,scale)
 assert total_volume==N-Q(slack,scale) and N-1<total_volume<=N
 # Source quota lemmas imply this bound for actual AH, regardless of matching.
 positive_lower=np*Kp+m*Kq+b*m-C
 limit=Kp+(Kq+b-Kp)*(rp-6*tau)/(Z+3*tau)
 assert R-limit==rho*tau*(6*Z+3*rp)/(Z+3*tau)
 return {'tiny_containers':m,'tau':str(tau),'P_bins':np,'Q_bins':m,'OPT_exact':N,'quota_counts':n,'filler_items':pieces,'overflow_triggers':triggers,'offline_unused_volume':str(Q(slack,scale)),'positive_container_lower_bound':str(positive_lower),'finite_ratio_lower':float(positive_lower/N),'fixed_tau_limiting_ratio':str(limit)}
traces=[trace(m,Q(1,100000000)) for m in [1,10,100,1000]]
out={'status':'PASS','claimed_asymptotic_algorithm_ratio':str(R),'P_residual':str(rp),'Q_residual':str(rq),'B':str(B),'b':str(b),'limiting_Q_fraction':str(theta),'K_P':str(Kp),'K_Q':str(Kq),'count_error_constant':str(C),'negative_container_density':str(neg),'tau_upper':'1/1000000','traces':traces,'seconds':time.time()-start,'scope':'explicit offline and tiny-execution certificates; full AH cost lower bound uses source Lemma5/Corollary6 and small-class quota invariants'}
(H/'saturation_check.json').write_text(json.dumps(out,indent=2));print({k:v for k,v in out.items() if k!='traces'});print('finite traces',[(z['tiny_containers'],z['OPT_exact'],z['finite_ratio_lower']) for z in traces])
