#!/usr/bin/env python3
"""Solver-free exact continuous-family dual endpoint certificate.

The analytic q/c/g reductions are proved in SUCCESSOR_MIXTURE_THEOREM.md.
This program recomputes all physical rows, positive duals and endpoint values.
"""
from fractions import Fraction as F
from pathlib import Path
import json,sys,hashlib
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent;ROOT=H.parent.parent;sys.path.insert(0,str(ROOT/'phase2'))
from verify_single_thresholds import weights
J=json.loads((H/'successor_mixture_certificate.json').read_text());M=json.loads((H/'refined_candidate.json').read_text())
P={int(j):{'lo':F(r['lower']),'hi':F(r['upper']),'alpha':{F(i):F(a) for i,a in r['containers']}} for j,r in J['parameters'].items()}
s=next(s for s in J['scenarios'] if(s['x'],s['y'])==('3/7','1/2'));N,HUGE,B,b,c,y=weights(P,s)
R=F(J['target']);assert R==F(M['target']);d=F(1,43);a=F(17,60)
rows=M['dual'];assert sum(F(z['lambda_weight']) for z in rows)==1
for row in rows:
    h=int(row['huge']);lookup={j:(size,w) for j,size,w in (HUGE if h else N)}
    residual=(y if h else F(1))-sum(lookup[j][0]*n for j,n in row['pattern'])
    K=h+sum(lookup[j][1]*n for j,n in row['pattern'])
    assert K==F(row['constant']) and residual==F(row['residual']) and 0<residual<d and F(row['lambda_weight'])>0
def f(size,c,g,q):
    k=sum(al*max(F(0),1-q*(A-g)) for A,al in P[212]['alpha'].items());den=B-c-(g-c)*k
    assert den>=B-g>0
    return b/den*(size+(g-c)*q*size*int(size>c)+(1+(g-c)*q)*max(F(0),size-g))
cuts=sorted({F(0),d,*[F(row['residual']) for row in rows]})
columns=sorted(set((c,g,1/(A-g)) for g in cuts for c in cuts if c<=g for A in [F(1),a]))
checks=[]
for c,g,q in columns:
    value=sum(F(row['lambda_weight'])*(F(row['constant'])+f(F(row['residual']),c,g,q)) for row in rows)
    assert value>=R
    checks.append({'c':str(c),'g':str(g),'q':str(q),'value':str(value),'gap':str(value-R),'equality':value==R})
mix=[tuple(map(F,z)) for z in M['mixture']];assert sum(t for c,g,q,t in mix)==1 and all(t>0 for c,g,q,t in mix)
assert [[str(v) for v in z] for z in mix]==s['analysis_mixture']
for row in rows:
    r=F(row['residual']);value=F(row['constant'])+sum(t*f(r,c,g,q) for c,g,q,t in mix)
    assert value==R
    # A single tiny item tending upward to r realizes every component's
    # separate step/hinge envelope simultaneously, including r=c or r=g.
    for c,g,q,t in mix:
        count=(r/c).numerator//(r/c).denominator if c and (r/c).denominator!=1 else ((r/c).numerator-1 if c else 0)
        if c:assert min(r,count*d)==(r if r>c else 0)
        assert r//d==0
for c,g,q,t in mix:
    assert any(z['equality'] and tuple(map(F,[z['c'],z['g'],z['q']]))==(c,g,q) for z in checks)
# Exact formulas used in the analytic g reduction, checked on all endpoint
# combinations and physical residuals (identities also derived in prose).
for c,g,q in columns:
    for row in rows:
        r=F(row['residual'])
        if q==1/(1-g):
            simple=b*r*(1-g)/((1-c)*(B-g)) if r<=c else b*(r+max(F(0),r-g))/(B-g)
        else:
            simple=b*r/(B-c) if r<=c else b*(a-c)*(r+max(F(0),r-g))/((B-c)*(a-g))
        assert f(r,c,g,q)==simple
out={'status':'PASS exact entire continuous-family mixture floor','target':str(R),'target_decimal':float(R),'scope':'finite convex mixtures of disjoint-successor two-cutoff charges with fixed algorithm/non-tiny weights; not true algorithm ratio or unrestricted analysis optimum','physical_dual':rows,'endpoint_count':len(checks),'checks':checks,'certificate_sha256':hashlib.sha256((H/'successor_mixture_certificate.json').read_bytes()).hexdigest()}
(H/'family_verification.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS physical positive dual; all',len(checks),'endpoint columns; R',str(R))
