#!/usr/bin/env python3
"""Bounded rational candidate tests, not an algorithm theorem by themselves."""
from fractions import Fraction as Q
from pathlib import Path
import sys,json,time
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parent))
from verify_nonlinear_independent import reconstruct
from exact_nonlinear_pricing import tiny_parameters
from step_pricing import price,D

J=json.loads((H.parent/'single_threshold_certificate.json').read_text())
P={int(j):{'lo':Q(r['lower']),'hi':Q(r['upper']),'a':{Q(i):Q(a) for i,a in r['containers']}} for j,r in J['parameters'].items()}
targets={('49/320','1/6'),('533/1600','1/3'),('3/7','1/2')}
cs=[Q(1,100),Q(3,200),Q(1,50),Q(21,1000),Q(11,500),Q(23,1000),D]
start=time.time();rows=[]
for s in J['scenarios']:
    if (s['x'],s['y']) not in targets:continue
    normal,huge,*_=reconstruct(P,s);B,b=tiny_parameters(P,s)
    for c in cs:
        out=[price(normal,Q(1),B,b,c,0),price(huge,Q(s['y']),B,b,c,1)]
        h=max(range(2),key=lambda h:out[h][0]);v,p,n=out[h]
        row={'x':s['x'],'y':s['y'],'c':str(c),'bound':str(v),'decimal':float(v),'huge':bool(h),'pattern':p,'nodes':sum(t[2] for t in out)}
        rows.append(row);print(row,flush=True)
(H/'step_charge_exploration.json').write_text(json.dumps({'scope':'hypothesis pricing only','rows':rows,'seconds':time.time()-start},indent=2))
