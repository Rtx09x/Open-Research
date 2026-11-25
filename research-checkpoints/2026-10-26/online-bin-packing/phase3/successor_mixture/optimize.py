#!/usr/bin/env python3
"""Finite endpoint LP discovery, exact primal/dual and full pricing certification.

SciPy discovers a basis only. Every decision is certified with Fractions.
Analytic endpoint reduction, not the numerical solver, covers the continuum.
"""
from fractions import Fraction as Q
from pathlib import Path
import sys,json,time,os
if hasattr(os,"sched_getaffinity"):
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent;ROOT=H.parent.parent
sys.path.insert(0,str(ROOT/'phase2'));sys.path.insert(0,str(ROOT/'phase3/successor_cutoff'))
from verify_nonlinear_independent import reconstruct
from exact_nonlinear_pricing import tiny_parameters
from pricing import price,envelope,D
from scipy.optimize import linprog
J=json.loads((ROOT/'phase3/bf_type/type_mixture_certificate.json').read_text())
P={int(j):{'lo':Q(r['lower']),'hi':Q(r['upper']),'a':{Q(i):Q(a) for i,a in r['containers']}} for j,r in J['parameters'].items()}
s=next(s for s in J['scenarios'] if(s['x'],s['y'])==('3/7','1/2'));normal,huge,*_=reconstruct(P,s);B,b=tiny_parameters(P,s)
items=[normal,huge];caps=[Q(1),Q(s['y'])];rows=[];seen=set();history=[];start=time.time()
def add(h,pattern):
    look={j:(sz,w) for j,sz,w in items[h]};r=caps[h]-sum(look[j][0]*n for j,n in pattern);K=h+sum(look[j][1]*n for j,n in pattern)
    if(r,K) in seen:return False
    seen.add((r,K));assert 0<r<=D
    rows.append({'huge':bool(h),'pattern':pattern,'residual':r,'constant':K});return True
for pat in [[1,165,179,205,208,211],[1,165,172],[1,165,179,187]]:add(0,tuple((j,1) for j in pat))

def solve(A,y):
    A=[list(map(Q,row))+[Q(v)] for row,v in zip(A,y)];n=len(y);assert all(len(row)==n+1 for row in A)
    for i in range(n):
        pivot=next(j for j in range(i,n) if A[j][i]);A[i],A[pivot]=A[pivot],A[i]
        z=A[i][i];A[i]=[v/z for v in A[i]]
        for j in range(n):
            if j!=i:
                z=A[j][i];A[j]=[u-z*v for u,v in zip(A[j],A[i])]
    return [row[-1] for row in A]

for iteration in range(12):
    cuts=sorted({Q(0),D,*[row['residual'] for row in rows]})
    columns=sorted(set((c,g,1/(A-g)) for g in cuts for c in cuts if c<=g for A in [Q(1),Q(17,60)]))
    M=[[row['constant']+envelope(P,B,b,row['residual'],[(*col,Q(1))]) for col in columns] for row in rows]
    # Rescale near-equal physical weights for stable discovery only.
    base=Q(1578,1000);scale=10**6
    L=linprog([0.0]*len(columns)+[1.0],A_ub=[[float((v-base)*scale) for v in row]+[-1.0] for row in M],b_ub=[0.0]*len(rows),A_eq=[[1.0]*len(columns)+[0.0]],b_eq=[1.0],bounds=[(0,None)]*len(columns)+[(None,None)],method='highs')
    if not L.success:raise RuntimeError('discovery failed; no exact claim')
    support=[j for j,x in enumerate(L.x[:-1]) if x>1e-8];active=[i for i,x in enumerate(L.ineqlin.marginals) if -x>1e-8];assert len(support)==len(active)
    n=len(support)
    sol=solve([[Q(1)]*n+[Q(0)]]+[[M[i][j] for j in support]+[-Q(1)] for i in active],[Q(1)]+[Q(0)]*n)
    theta,R=sol[:-1],sol[-1];assert all(x>0 for x in theta)
    dual=solve([[Q(1)]*n+[Q(0)]]+[[M[i][j] for i in active]+[-Q(1)] for j in support],[Q(1)]+[Q(0)]*n)
    lam,Rdual=dual[:-1],dual[-1];assert R==Rdual and all(x>0 for x in lam)
    assert all(sum(row[j]*x for j,x in zip(support,theta))<=R for row in M)
    assert all(sum(M[i][j]*x for i,x in zip(active,lam))>=R for j in range(len(columns)))
    mix=[(*columns[j],t) for j,t in zip(support,theta)]
    out=[price(items[h],caps[h],P,B,b,mix,h) for h in range(2)];upper=max(z[0] for z in out)
    history.append({'iteration':iteration,'rows':len(rows),'columns':len(columns),'support':len(support),'lower':R,'upper':upper})
    print(iteration,'rows/cols',len(rows),len(columns),'support',len(support),'R',float(R),'upper',float(upper),flush=True)
    if upper==R:
        result={'status':'PASS exact endpoint LP primal/dual and all-pattern critical pricing; analytic continuum reduction separate','target':R,'target_decimal':float(R),'mixture':mix,'dual':[dict(rows[i],lambda_weight=t) for i,t in zip(active,lam)],'endpoint_checks':[{'c':c,'g':g,'q':q,'value':sum(M[i][j]*t for i,t in zip(active,lam))} for j,(c,g,q) in enumerate(columns)],'history':history}
        (H/'refined_candidate.json').write_text(json.dumps(result,default=str,indent=2)+'\n')
        print('PASS',str(R),'mix',mix,'seconds',time.time()-start);break
    for h,(v,pat,nodes) in enumerate(out):
        if v>R:assert add(h,pat)
else:raise RuntimeError('bounded12-iteration checkpoint')
