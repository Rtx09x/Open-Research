#!/usr/bin/env python3
"""Bounded exact two-cutoff exploration; no global theorem asserted here."""
from fractions import Fraction as Q
from pathlib import Path
from itertools import combinations
import sys,json,time
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent;ROOT=H.parent.parent;sys.path.insert(0,str(ROOT/'phase2'))
from verify_nonlinear_independent import reconstruct
from exact_nonlinear_pricing import tiny_parameters
from pricing import price,envelope,D
J=json.loads((ROOT/'phase3/bf_type/type_mixture_certificate.json').read_text())
P={int(j):{'lo':Q(r['lower']),'hi':Q(r['upper']),'a':{Q(i):Q(a) for i,a in r['containers']}} for j,r in J['parameters'].items()}
s=next(s for s in J['scenarios'] if(s['x'],s['y'])==('3/7','1/2'));normal,huge,*_=reconstruct(P,s);B,b=tiny_parameters(P,s)
items=[normal,huge];caps=[Q(1),Q(s['y'])]
p=Q(997,2100120);g0=Q(1,60);q2=1/(Q(17,60)-D)

def optimize(g):
    def mix(theta):return [(p,g,1/(1-g),theta),(g0,D,q2,1-theta)]
    rows=[];seen=set();history=[]
    def add(h,pattern):
        key=(h,pattern)
        if key in seen:return False
        seen.add(key);look={j:(sz,w) for j,sz,w in items[h]}
        residual=caps[h]-sum(look[j][0]*n for j,n in pattern);K=h+sum(look[j][1]*n for j,n in pattern)
        v0=K+envelope(P,B,b,residual,mix(Q(0)));v1=K+envelope(P,B,b,residual,mix(Q(1)))
        rows.append({'huge':bool(h),'pattern':pattern,'residual':residual,'constant':K,'intercept':v0,'slope':v1-v0});return True
    for theta in [Q(0),Q(1)]:
        for h in range(2):v,pat,n=price(items[h],caps[h],P,B,b,mix(theta),h);add(h,pat)
    for iteration in range(20):
        choices={Q(0),Q(1)}
        for u,v in combinations(rows,2):
            if u['slope']!=v['slope']:
                x=(v['intercept']-u['intercept'])/(u['slope']-v['slope'])
                if 0<=x<=1:choices.add(x)
        theta=min(choices,key=lambda x:(max(row['intercept']+row['slope']*x for row in rows),x))
        lower=max(row['intercept']+row['slope']*theta for row in rows)
        out=[price(items[h],caps[h],P,B,b,mix(theta),h) for h in range(2)];upper=max(t[0] for t in out)
        history.append({'iteration':iteration,'rows':len(rows),'theta':theta,'lower':lower,'upper':upper})
        if lower==upper:
            return {'status':'exact conservative envelope optimum for fixed two components only','g':g,'target':upper,'theta':theta,'mixture':mix(theta),'active':[row for row in rows if row['intercept']+theta*row['slope']==lower],'history':history}
        for h,(v,pat,n) in enumerate(out):
            if v>lower:assert add(h,pat)
    raise RuntimeError('bounded20-round checkpoint reached')

if __name__=='__main__':
    start=time.time();results=[]
    grid=sorted({D,g0,Q(29,1254),*[g0+(D-g0)*Q(i,12) for i in range(13)]},reverse=True)
    for g in grid:
        r=optimize(g);results.append(r);print('g',str(g),'R',float(r['target']),'theta',float(r['theta']),'active',[(a['residual'],a['pattern']) for a in r['active']],flush=True)
        (H/'exploration.json').write_text(json.dumps({'status':'checkpoint; global cases not checked','results':results,'best':min(results,key=lambda z:z['target']),'seconds':time.time()-start},default=str,indent=2))
    assert results[0]['target']==Q(J['target'])
    print('PASS old-family control g=d; bounded sweep complete',time.time()-start)
