#!/usr/bin/env python3
"""Check precise stated changes against numerical source snapshot (no discovery imports).
The snapshot's primary-source transcription is separately audited; this routine
proves the final artifact only changes the three stated algorithm proportions.
"""
from fractions import Fraction as Q
import json
S=json.load(open('ah_published_numeric_snapshot.json'));D=json.load(open('ah_three_parameter_full_certificate.json'))
def parameters(data):
 return {int(j):{'lower':Q(r['lower']),'upper':Q(r['upper']),'containers':{Q(i):Q(a) for i,a in r['containers']}} for j,r in data.items()}
P=parameters(S['parameters']);F=parameters(D['parameters']);expected={167:(1,3),172:(2,6),179:(10,2)}
assert set(P)==set(F)==set(range(2,213))
assert {q['class'] for q in D['modifications']}==set(expected)
for change in D['modifications']:
 j=change['class'];i,k=change['from_type'],change['to_type'];a=Q(change['mass'])
 assert (i,k)==expected[j] and a>0
 P[j]['containers'][Q(i)]-=a;P[j]['containers'][Q(k)]+=a
assert P==F
for j,p in F.items():assert sum(p['containers'].values())==1 and all(v>0 for v in p['containers'].values())
def scenario_map(data):
 return {(Q(s['x']),Q(s['y'])):{k:Q(s[k]) for k in ['w','u','v'] if k in s} for s in data}
assert scenario_map(S['scenarios'])==scenario_map(D['scenarios'])
print(json.dumps({'status':'PASS','changed_classes':sorted(expected),'unchanged_published_analysis_scenarios':len(S['scenarios']),'source':S['source']},indent=2))
