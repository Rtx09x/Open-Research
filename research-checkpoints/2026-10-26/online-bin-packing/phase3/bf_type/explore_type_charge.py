#!/usr/bin/env python3
from fractions import Fraction as Q
from pathlib import Path
import sys,json,time
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent;ROOT=H.parent.parent;sys.path.insert(0,str(ROOT/'phase2'))
from verify_nonlinear_independent import reconstruct
from exact_nonlinear_pricing import tiny_parameters
from type_pricing import price,D
J=json.loads((ROOT/'phase2/best_fit/best_fit_certificate.json').read_text())
P={int(j):{'lo':Q(r['lower']),'hi':Q(r['upper']),'a':{Q(i):Q(a) for i,a in r['containers']}} for j,r in J['parameters'].items()}
targets={('49/320','1/6'),('533/1600','1/3'),('3/7','1/2')}
cs=[Q(1,100),Q(3,250),Q(3,200),Q(1,60),Q(1,50)]
q=1/(Q(1)-D);start=time.time();rows=[]
for s in J['scenarios']:
    if (s['x'],s['y']) not in targets:continue
    normal,huge,*_=reconstruct(P,s);B,b=tiny_parameters(P,s)
    for c in cs:
        out=[price(normal,Q(1),P,B,b,c,q,0),price(huge,Q(s['y']),P,B,b,c,q,1)]
        h=max(range(2),key=lambda h:out[h][0]);v,p,n=out[h]
        row={'x':s['x'],'y':s['y'],'c':str(c),'q':str(q),'bound':str(v),'decimal':float(v),'huge':bool(h),'pattern':p,'nodes':sum(t[2] for t in out)}
        rows.append(row);print(row,flush=True)
(H/'type_charge_exploration.json').write_text(json.dumps({'scope':'bounded endpoint-q exploration, not all-input certificate','rows':rows,'seconds':time.time()-start},indent=2))
