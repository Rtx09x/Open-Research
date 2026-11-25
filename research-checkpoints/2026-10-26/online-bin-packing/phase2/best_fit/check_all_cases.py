#!/usr/bin/env python3
"""Exact all-case pricing for fixed simple BF thresholds; no optimization."""
from fractions import Fraction as Q
from pathlib import Path
import sys,json,time,hashlib
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parent))
from verify_nonlinear_independent import reconstruct
from exact_nonlinear_pricing import tiny_parameters
from step_pricing import price,D

J=json.loads((H.parent/'single_threshold_certificate.json').read_text())
P={int(j):{'lo':Q(r['lower']),'hi':Q(r['upper']),'a':{Q(i):Q(a) for i,a in r['containers']}} for j,r in J['parameters'].items()}
cs={('49/320','1/6'):Q(3,200),('533/1600','1/3'):Q(1,60),('3/7','1/2'):Q(1,60)}
start=time.time();rows=[]
for s in J['scenarios']:
    normal,huge,*_=reconstruct(P,s);B,b=tiny_parameters(P,s);c=cs.get((s['x'],s['y']),D)
    out=[price(normal,Q(1),B,b,c,0),price(huge,Q(s['y']),B,b,c,1)]
    row={k:s[k] for k in ['x','y','u','v','w'] if k in s}
    row.update(c=str(c),maximum=str(max(v for v,p,n in out)),cases=[{'maximum':str(v),'pattern':p,'nodes':n} for v,p,n in out])
    rows.append(row)
R=max(Q(s['maximum']) for s in rows)
out={'status':'all402 exact pricing cases PASS; algorithm applicability separately audited',
     'target':str(R),'target_decimal':float(R),'previous_one_open_target':J['target'],
     'algorithm':'tiny Best Fit across all advertised tiny containers; create only if none fits; same quota and non-tiny rules',
     'charge':'b/(B-c) * s * (1 + (d-c)/(Amin-d) * indicator(s>c))',
     'parameters':J['parameters'],'scenarios':rows,
     'source_certificate_sha256':hashlib.sha256((H.parent/'single_threshold_certificate.json').read_bytes()).hexdigest()}
assert R<Q(J['target']) and len(rows)==402
(H/'best_fit_certificate.json').write_text(json.dumps(out,indent=2))
print('PASS',str(R),float(R),'seconds',time.time()-start,'nodes',sum(z['nodes'] for s in rows for z in s['cases']))
print('bottlenecks',[(s['x'],s['y'],s['c']) for s in rows if Q(s['maximum'])==R])
