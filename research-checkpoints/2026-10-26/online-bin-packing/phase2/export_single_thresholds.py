#!/usr/bin/env python3
"""Convert exact mixture solutions to pointwise-better single thresholds."""
from fractions import Fraction as Q
from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent;source=H.parent/'ah_three_parameter_full_certificate.json'
F=json.loads(source.read_text());M=json.loads((H/'continuous_mixture_search.json').read_text())
P=F['parameters'];B=sum(Q(i)*Q(a) for i,a in P['212']['containers']);selected={}
for r in M['results']:
 z=sum(Q(t)/(B-Q(c)) for c,t in r['mixture']);c=B-1/z;assert 0<=c<=Q(1,43)
 rows=[]
 for i,l in zip(r['dual']['rows'],r['dual']['lambda']):rows.append(dict(r['rows'][i],lambda_weight=l))
 selected[(r['x'],r['y'])]={'c':str(c),'target':r['target'],'dual_patterns':rows,'dominated_mixture':r['mixture']}
for s in F['scenarios']:
 s.update(selected.get((s['x'],s['y']),{'c':'1/43'}))
F.update({'status':'new exact single-threshold certificate; independent full verification pending','algorithm_change':'delay tiny-container closure until next tiny item fails nominal capacity; all other rules unchanged','target':M['target'],'pro_target':'87931323061219230147063794829048504459349/55715094120735551199336133222286481162240','frozen_parameter_certificate_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'structural_claim':'f_c is convex in1/(B-c), so one effective threshold pointwise dominates every convex mixture'})
(H/'single_threshold_certificate.json').write_text(json.dumps(F,indent=2))
for key,v in selected.items():print(key,'c=',v['c'],'~',float(Q(v['c'])),'R=',float(Q(v['target'])))
