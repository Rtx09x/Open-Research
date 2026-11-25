#!/usr/bin/env python3
"""Compile the certified continuous q rule to a finite exact rational policy.
This is a proof-strengthening construction, not parameter optimization.
Every accepted box gets a rational q above its rigorous q* upper enclosure.
Inherited-minus feasibility follows algebraically from q>=q*, plus budgets
are independently rechecked for that constant rational q on the whole box.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib,json,time
from mpmath import iv
iv.dps=70
I=iv.mpf
a,b,rho,k,d,p,p0,q0,qmax=map(I,['.0102','.9475','.0097','.6','14.8','.856','.85599','.9019','.76'])
H=2**a;U=H*k**b
here=Path(__file__).parent
source=here.parent/'certification/results/adaptive_bias_certificate.json'
certificate=json.loads(source.read_text())


def point_q(x):return I(x.numerator)/x.denominator

def endpoint_exact(mpf):
 sign,man,exp,bc=mpf
 return (-1 if sign else 1)*Q(man)*(Q(2)**exp)

start=time.monotonic();rows=[];min_plus=None;min_total=None
for leaf in certificate['partition']:
 lo,hi=Q(leaf['lo']),Q(leaf['hi'])
 x=I([point_q(lo).a,point_q(hi).b])
 z,r=(x,rho) if leaf['segment']==1 else (d*x,x)
 S=(z+1+r+k)**b;B=p*z**b+r**b;P=p*z**b+1;A=P+r**b
 den=p0*S-B;assert den>0
 raw=U/den
 upper=max(Q(1,2),endpoint_exact(raw._mpi_[1]))
 scale=2**48
 numerator=-((-upper.numerator*scale)//upper.denominator)
 qrat=Q(numerator,scale);qi=point_q(qrat)
 assert qrat>=upper and qi<=qmax
 # qrat>=q*(point) gives the completed-minus budget by construction.
 plus=p0*S-P-qi*U;total=q0*S-A-qi*U
 assert plus>0 and total>0
 min_plus=plus.a if min_plus is None else min(min_plus,plus.a)
 min_total=total.a if min_total is None else min(min_total,total.a)
 rows.append({'segment':leaf['segment'],'lo':str(lo),'hi':str(hi),'q':str(qrat)})
# Recheck full closed-domain coverage with exact rational arithmetic.
for segment,lo,hi in [(1,Q(0),Q('14.8')*Q('.0097')),(2,Q('.0097'),Q(1))]:
 part=sorted((Q(x['lo']),Q(x['hi'])) for x in rows if x['segment']==segment)
 assert part[0][0]==lo and part[-1][1]==hi
 assert all(l[1]==r[0] for l,r in zip(part,part[1:]))
out={'status':'certified rational step policy for same induction constants','source_certificate_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'iv_precision':iv.dps,'rows':rows,'n_rows':len(rows),'minimum_certified_plus_margin':str(min_plus),'minimum_certified_total_margin':str(min_total),'seconds':time.monotonic()-start,'runtime_rule':'At trigger let z=tau/h. If z<=delta*rho use segment1 x=z; otherwise use segment2 x=z/delta. Choose the first row of that segment whose closed interval contains x. q is its exact rational; update weight multiplicatively using exact rational arithmetic.'}
(here/'rational_q_policy.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
