#!/usr/bin/env python3
"""Independent fixed-algorithm floor arithmetic; no worker imports or weights."""
from fractions import Fraction as Q
from pathlib import Path
import json, hashlib

ROOT=Path(__file__).resolve().parents[2]
source=ROOT/'online-bin-packing/phase4/retune_two/retuned_certificate.json'
claim=ROOT/'online-bin-packing/phase7/actual_floor/actual_floor_certificate.json'
j=json.loads(source.read_text()); c=json.loads(claim.read_text())
# Literal parameter inputs, separately compared with frozen algorithm table.
rows={165:(Q(1,3),Q(1067,3200),{1:Q(22145926,78181827),2:Q(56035901,78181827)}),
179:(Q(1,11),Q(1,10),{2:Q(27927345544998943473172174410059889328771995680602116851,75741405378444607696070020526291572299375191317598061148),10:Q(47814059833445664222897846116231682970603195636995944297,75741405378444607696070020526291572299375191317598061148)}),
205:(Q(1,37),Q(1,36),{10:Q(99052686,407082371),36:Q(308029685,407082371)}),
208:(Q(1,40),Q(1,39),{11:Q(73429915,298784748),39:Q(225354833,298784748)}),
211:(Q(1,43),Q(1,42),{11:Q(119627466,457395215),42:Q(337767749,457395215)})}
alpha=Q(13701867480,32568497273); beta=1-alpha
capacities=(Q(17,60),Q(1)); proportions=(alpha,beta)
p=Q(997,2100120); tau=Q(1,10**9); s=p-6*tau
assert 0<s<p<Q(1,43)
assert Q(1,2)+tau+sum(lo+tau for lo,hi,a in rows.values())+s==1
rates={}; error=Q(2)
for label,(lo,hi,a) in rows.items():
    r=j['parameters'][str(label)]
    assert Q(r['lower'])==lo and Q(r['upper'])==hi
    assert {int(k):Q(v) for k,v in r['containers']}==a
    assert sum(a.values())==1 and all(v>0 for v in a.values())
    assert lo<lo+tau<=hi
    if label==165:
        # Source Lemma5 + Corollary6: n2>=alpha2*n-2,
        # N<=n+n2<=(1+alpha2)*n, irrespective of incomplete declared pairs.
        rates[label]=a[2]/(1+a[2])
        assert rates[label]==Q(56035901,134217728)
    else:
        mean=sum(k*v for k,v in a.items())
        positive=sum(v for k,v in a.items() if k*hi>Q(1,2))
        rates[label]=positive/mean
        error+=(len(a)-1)*(rates[label]*max(a)+1)
    assert rates[label]==Q(c['positive_container_rates'][str(label)])
tiny=j['parameters']['212']
assert dict((Q(k),Q(v)) for k,v in tiny['containers'])==dict(zip(capacities,proportions))
slots=tuple(a//s for a in capacities)
assert slots==(596,2106)==tuple(a//p for a in capacities)
K=sum(v*k for v,k in zip(proportions,slots))
Kp=1+sum(rates.values()); lower=Kp+beta/K; upper=Q(j['target'])
assert lower==Q(c['actual_algorithm_ratio_lower'])
assert Kp==Q(c['non_tiny_positive_rate_including_huge'])
assert error==Q(c['non_tiny_count_error_constant'])
assert upper-lower==Q(c['remaining_analysis_only_window'])>0
# All-N tiny count bound uses only capacities, not BF chronology:
# e1+e2=0, |ei|<1 -> sum ki*ei <=1510, and n2>=beta*m-1.
constant=error+1510*beta/K+1
# Independently simulate arrivals, including incomplete prefixes, using exact
# scaled sizes and an all-container fit search. The input horizon is fixed,
# not generated from desired completed-container counts.
from math import lcm
scale=lcm(s.denominator,*(a.denominator for a in capacities))
unit=int(s*scale); caps=[int(a*scale) for a in capacities]
gaps=[]; counts=[0,0]; checked=0
for N in range(1,120001):
    eligible=[i for i,g in enumerate(gaps) if g>=unit]
    if eligible: dest=min(eligible,key=lambda i:gaps[i])
    else:
        m=len(gaps)
        typ=next(i for i,a in enumerate(proportions) if counts[i]<=a*m)
        counts[typ]+=1; gaps.append(caps[typ]); dest=m
    gaps[dest]-=unit
    m=len(gaps)
    assert all(abs(Q(counts[i])-proportions[i]*m)<1 for i in range(2))
    assert N<=slots[0]*counts[0]+slots[1]*counts[1]<=K*m+1510
    assert Kp*N+counts[1]-error>=lower*N-constant
    checked+=1
out={'status':'PASS','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
     'claim_sha256':hashlib.sha256(claim.read_bytes()).hexdigest(),
     'positive_rates':{str(k):str(v) for k,v in rates.items()},'Kp':str(Kp),'K':str(K),
     'lower':str(lower),'upper':str(upper),'gap':str(upper-lower),
     'sufficient_additive_constant':str(constant),'arbitrary_prefix_checks':checked,
     'scope':'Fixed capacities/proportions and positive-container architecture; not universal online lower bound.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
