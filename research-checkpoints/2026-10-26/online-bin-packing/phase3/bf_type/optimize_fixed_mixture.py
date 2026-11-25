#!/usr/bin/env python3
"""Exact 1D row generation for two structurally chosen step certificates."""
from fractions import Fraction as Q
from pathlib import Path
from itertools import combinations
import sys,json,time
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent;ROOT=H.parent.parent;sys.path.insert(0,str(ROOT/'phase2'))
from verify_nonlinear_independent import reconstruct
from exact_nonlinear_pricing import tiny_parameters
from mix_pricing import price,envelope,D
J=json.loads((ROOT/'phase2/best_fit/best_fit_certificate.json').read_text())
P={int(j):{'lo':Q(r['lower']),'hi':Q(r['upper']),'a':{Q(i):Q(a) for i,a in r['containers']}} for j,r in J['parameters'].items()}
s=next(s for s in J['scenarios'] if(s['x'],s['y'])==('3/7','1/2'));normal,huge,*_=reconstruct(P,s);B,b=tiny_parameters(P,s)
items=[normal,huge];caps=[Q(1),Q(s['y'])]
c1,q1=Q(997,2100120),1/(1-D);c2,q2=Q(1,60),1/(Q(17,60)-D)
def mix(theta):return [(c1,q1,theta),(c2,q2,1-theta)]
rows=[];seen=set();start=time.time();history=[]
def add(h,pattern):
    key=(h,pattern)
    if key in seen:return False
    seen.add(key);look={j:(sz,w) for j,sz,w in items[h]}
    residual=caps[h]-sum(look[j][0]*n for j,n in pattern);K=h+sum(look[j][1]*n for j,n in pattern)
    v0=K+envelope(P,B,b,residual,mix(Q(0)));v1=K+envelope(P,B,b,residual,mix(Q(1)))
    rows.append({'huge':bool(h),'pattern':pattern,'residual':residual,'constant':K,'intercept':v0,'slope':v1-v0});return True
for theta in [Q(0),Q(1)]:
    for h in range(2):v,p,n=price(items[h],caps[h],P,B,b,mix(theta),h);add(h,p)
for iteration in range(30):
    choices={Q(0),Q(1)}
    for u,v in combinations(rows,2):
        if u['slope']!=v['slope']:
            x=(v['intercept']-u['intercept'])/(u['slope']-v['slope'])
            if 0<=x<=1:choices.add(x)
    theta=min(choices,key=lambda x:(max(row['intercept']+row['slope']*x for row in rows),x))
    lower=max(row['intercept']+row['slope']*theta for row in rows)
    out=[price(items[h],caps[h],P,B,b,mix(theta),h) for h in range(2)];upper=max(t[0] for t in out)
    history.append({'iteration':iteration,'rows':len(rows),'theta':theta,'lower':lower,'upper':upper});print(iteration,float(theta),float(lower),float(upper),flush=True)
    if lower==upper:
        active=[row for row in rows if row['intercept']+theta*row['slope']==lower]
        neg=next(row for row in active if row['slope']<0);pos=next(row for row in active if row['slope']>0)
        lam=pos['slope']/(pos['slope']-neg['slope']);assert 0<lam<1
        assert lam*neg['intercept']+(1-lam)*pos['intercept']==upper
        result={'status':'PASS exact fixed-two-charge mixture optimum; global scenarios not yet checked','x':s['x'],'y':s['y'],'target':upper,'theta':theta,'mixture':mix(theta),'dual_rows':[dict(neg,lambda_weight=lam),dict(pos,lambda_weight=1-lam)],'history':history,'seconds':time.time()-start}
        (H/'fixed_mixture_optimum.json').write_text(json.dumps(result,default=str,indent=2));print('PASS',str(upper),float(upper));break
    for h,(v,p,n) in enumerate(out):
        if v>lower:assert add(h,p)
else:raise RuntimeError('bounded30-round checkpoint reached')
