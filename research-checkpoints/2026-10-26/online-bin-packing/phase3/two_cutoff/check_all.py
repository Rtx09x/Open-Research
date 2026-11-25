#!/usr/bin/env python3
"""Exact all-scenario two-cutoff pricing, preserving previous certificates."""
from fractions import Fraction as Q
from pathlib import Path
import sys,json,hashlib,time
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent;ROOT=H.parent.parent;sys.path.insert(0,str(ROOT/'phase2'))
from verify_nonlinear_independent import reconstruct
from exact_nonlinear_pricing import tiny_parameters
from pricing import price,D
source=ROOT/'phase3/bf_type/type_mixture_certificate.json';J=json.loads(source.read_text());M=json.loads((H/'refined_candidate.json').read_text())
P={int(j):{'lo':Q(r['lower']),'hi':Q(r['upper']),'a':{Q(i):Q(a) for i,a in r['containers']}} for j,r in J['parameters'].items()}
start=time.time();rows=[]
for s in J['scenarios']:
    normal,huge,*_=reconstruct(P,s);B,b=tiny_parameters(P,s)
    mix=[tuple(map(Q,z)) for z in M['mixture']] if(s['x'],s['y'])==('3/7','1/2') else [(Q(c),D,Q(q),Q(weight)) for c,q,weight in s['analysis_mixture']]
    out=[price(normal,Q(1),P,B,b,mix,0),price(huge,Q(s['y']),P,B,b,mix,1)]
    row={k:s[k] for k in ['x','y','u','v','w','c'] if k in s}
    row.update(analysis_mixture=[[str(v) for v in z] for z in mix],maximum=str(max(v for v,pat,n in out)),cases=[{'maximum':str(v),'pattern':pat,'nodes':n} for v,pat,n in out]);rows.append(row)
R=max(Q(s['maximum']) for s in rows);assert R==Q(M['target'])<Q(J['target'])
out={'status':'PASS exact all402/804 conservative two-cutoff-envelope pricing; independent audit pending','target':str(R),'target_decimal':float(R),'algorithm':'unchanged phase2 tiny Best Fit AH variant','source_certificate_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'parameters':J['parameters'],'scenarios':rows,'previous_bound':J['target'],'critical_g':M['g']}
(H/'two_cutoff_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS',str(R),float(R),'nodes',sum(z['nodes'] for s in rows for z in s['cases']),'seconds',time.time()-start)
