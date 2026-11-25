#!/usr/bin/env python3
"""Exact P/Q intersection for the disjoint-successor cutoff certificate."""
from fractions import Fraction as Q
from pathlib import Path
import sys,json
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent;ROOT=H.parent.parent;sys.path.insert(0,str(ROOT/'phase2'))
from verify_nonlinear_independent import reconstruct
from exact_nonlinear_pricing import tiny_parameters
from pricing import price,envelope,D
J=json.loads((ROOT/'phase3/bf_type/type_mixture_certificate.json').read_text())
P={int(j):{'lo':Q(r['lower']),'hi':Q(r['upper']),'a':{Q(i):Q(a) for i,a in r['containers']}} for j,r in J['parameters'].items()}
s=next(s for s in J['scenarios'] if(s['x'],s['y'])==('3/7','1/2'));normal,huge,*_=reconstruct(P,s);B,b=tiny_parameters(P,s)
def row(pattern):
    look={j:(sz,w) for j,sz,w in normal}
    return Q(1)-sum(look[j][0] for j in pattern),sum(look[j][1] for j in pattern)
p,kP=row([1,165,179,205,208,211]);rQ,kQ=row([1,165,179,187])
assert p==Q(997,2100120) and rQ==Q(29,1254)
delta=kP-kQ;constant=delta*B+b*p/(1-p)-2*b*rQ;linear=-delta-b*p/(1-p)+b
g=-constant/linear;assert Q(1,60)<g<rQ<D
mix=[(p,g,1/(1-g),Q(1))]
vP=kP+envelope(P,B,b,p,mix);vQ=kQ+envelope(P,B,b,rQ,mix)
assert vP==vQ
out=[price(normal,Q(1),P,B,b,mix,0),price(huge,Q(s['y']),P,B,b,mix,1)]
R=max(z[0] for z in out);assert R==vP<Q(J['target'])
result={'status':'PASS exact critical-scenario pricing and rational P/Q intersection; full cases pending','g':g,'c':p,'mixture':mix,'target':R,'target_decimal':float(R),'active_face_rows':[{'pattern':[1,165,179,205,208,211],'constant':kP,'residual':p,'value':vP},{'pattern':[1,165,179,187],'constant':kQ,'residual':rQ,'value':vQ}],'intersection_equation':{'constant':constant,'linear':linear},'oracle':[{'maximum':v,'pattern':pat,'nodes':n} for v,pat,n in out]}
(H/'refined_candidate.json').write_text(json.dumps(result,default=str,indent=2)+'\n')
print('g',str(g),float(g),'R',str(R),float(R),'nodes',sum(z[2] for z in out))
