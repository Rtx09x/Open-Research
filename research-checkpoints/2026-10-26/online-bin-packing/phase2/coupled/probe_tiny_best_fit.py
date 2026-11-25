#!/usr/bin/env python3
"""Exact, bounded structural falsification probe, NOT a new ratio certificate.

Replay the saturation tiny prefix under Best Fit across all previously created
tiny containers, retaining their advertised capacities and original quotas.
No non-tiny AH simulation is performed. Counts show whether the particular
one-open overflow obstruction survives this genuinely different insertion rule.
"""
from bisect import bisect_left, insort
from fractions import Fraction as Q
from pathlib import Path
import json, math, time

H=Path(__file__).resolve().parent
J=json.loads((H.parent/'single_threshold_certificate.json').read_text())
Aalpha=[(Q(a),Q(v)) for a,v in J['parameters']['212']['containers']]
Aalpha.sort()
tau=Q(1,100000000);p=Q(997,2100120)-6*tau;q=Q(29,1254)-4*tau
scale=math.lcm(p.denominator,q.denominator,tau.denominator,*[a.denominator for a,v in Aalpha])
A=[int(a*scale) for a,v in Aalpha];alpha=[v for a,v in Aalpha]
pp,qq,tt=[int(v*scale) for v in [p,q,tau]]

def choose(n):
    return next(i for i,a in enumerate(alpha) if n[i]*a.denominator<=a.numerator*sum(n))

def run(m):
    plan=[];n=[0]*len(A)
    for _ in range(m):
        i=choose(n);n[i]+=1;plan.append(i)
    fills=[A[i]-2*qq+tt for i in plan]
    F=sum(fills);np=(F+pp-1)//pp
    bf=[0]*len(A);gaps=[];items=0;mass=0;created=0
    def put(s):
        nonlocal items,mass,created
        items+=1;mass+=s
        k=bisect_left(gaps,(s,-1))
        if k==len(gaps):
            i=choose(bf);bf[i]+=1;gap=A[i];idx=created;created+=1
        else:
            gap,idx=gaps.pop(k)
        assert gap>=s
        if gap>s:insort(gaps,(gap-s,idx))
    remaining=pp
    for f in fills:
        put(qq)
        while f:
            s=min(f,remaining);put(s);f-=s;remaining-=s
            if not remaining:remaining=pp
    assert mass==F+m*qq
    assert sum(g for g,i in gaps)==sum(A[i]*bf[i] for i in range(len(A)))-mass
    pos=lambda ns:sum(ns[i] for i,a in enumerate(A) if 2*a>scale)
    return {'source_tiny_containers':m,'offline_OPT':np+m,'source_type_counts':n,
            'best_fit_type_counts':bf,'best_fit_tiny_containers':created,'items':items,
            'source_positive_tiny_containers':pos(n),'best_fit_positive_tiny_containers':pos(bf),
            'positive_count_reduction':pos(n)-pos(bf),'remaining_gaps':len(gaps),
            'max_final_gap':str(Q(max(g for g,i in gaps),scale)),
            'tiny_volume':str(Q(mass,scale))}

start=time.time();results=[run(m) for m in [10,100,1000]]
out={'status':'PASS exact structural probe; no new all-input bound claimed',
     'tau':str(tau),'results':results,'seconds':time.time()-start,
     'scope':'only tiny insertions, same source saturation inputs; matching and full AH not simulated'}
(H/'tiny_best_fit_probe.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
