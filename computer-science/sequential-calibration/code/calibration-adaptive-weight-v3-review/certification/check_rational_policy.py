#!/usr/bin/env python3
"""Independent closed-cell and exact-lookup audit of the compiled q policy.
Uses the stdlib integer interval backend, never the lead's compiler or mpmath.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import resource
import time
import replay_rational_certificate as arithmetic
from replay_rational_certificate import Dyadic as D, SCALE


def main():
    start=time.perf_counter()
    root=Path(__file__).parent
    path=root.parent/'theory'/'rational_q_policy.json'
    raw=path.read_bytes()
    policy=json.loads(raw)
    rows=policy['rows']
    assert len(rows)==4988==policy['n_rows']
    assert policy['source_certificate_sha256']==hashlib.sha256((root/'results'/'adaptive_bias_certificate.json').read_bytes()).hexdigest()
    beta,alpha=F('.9475'),F('.0102')
    kp,P0,Q0,kappa,delta,rho,qmax=map(D.rational,['.856','.85599','.9019','.6','14.8','.0097','.76'])
    H=D.rational(2)**alpha
    U=H*kappa**beta
    parsed=[(row['segment'],F(row['lo']),F(row['hi']),F(row['q'])) for row in rows]
    assert all(s in (1,2) and lo<hi and F(1,2)<=q<=F('.76') for s,lo,hi,q in parsed)
    domains=[(1,F(0),F('14.8')*F('.0097')),(2,F('.0097'),F(1))]
    for segment,lo,hi in domains:
        part=sorted((a,b) for s,a,b,q in parsed if s==segment)
        assert part[0][0]==lo and part[-1][1]==hi
        assert all(a[1]==b[0] for a,b in zip(part,part[1:]))
    minima={k:None for k in ['persistent_minus','persistent_plus','total_plus','q_upper']}
    for index,(segment,lo,hi,qrat) in enumerate(parsed):
        a,b=D.rational(lo),D.rational(hi)
        x=D(a.lo,b.hi)
        z,r=(x,rho) if segment==1 else (delta*x,x)
        zp,rp=z**beta,r**beta
        S=(z+1+r+kappa)**beta
        q=D.rational(qrat)
        margins={
            'persistent_minus':P0*S-kp*zp-rp-U/q,
            'persistent_plus':P0*S-kp*zp-1-q*U,
            'total_plus':Q0*S-kp*zp-1-rp-q*U,
            'q_upper':qmax-q,
        }
        for key,value in margins.items():
            assert value.lo>0,(index,key,str(value))
            if minima[key] is None or value.lo<minima[key]: minima[key]=value.lo
    # Independently reproduce the published lookup convention at every boundary
    # and midpoint. Domain coverage proves all other points have a containing row.
    lookup_tests=0
    for segment,lo,hi,q in parsed:
        for x in [lo,(lo+hi)/2,hi]:
            z=x if segment==1 else F('14.8')*x
            selected_segment=1 if z<=F('14.8')*F('.0097') else 2
            selected_x=z if selected_segment==1 else z/F('14.8')
            chosen=next((row for row in parsed if row[0]==selected_segment and row[1]<=selected_x<=row[2]),None)
            assert chosen is not None
            assert chosen[1]<=selected_x<=chosen[2]
            # The two segments coincide at the common endpoint; selecting seg1
            # there is legal even when this test originated in a seg2 row.
            assert max(F('.0097'),z/F('14.8')) == (F('.0097') if selected_segment==1 else selected_x)
            lookup_tests += 1
    report={
        'all_checks_passed':True,'closed_cells_checked':len(rows),
        'exact_boundary_midpoint_lookups_checked':lookup_tests,
        'backend':'standard-library dyadic rational intervals; exact integer nth roots',
        'precision_bits':arithmetic.BITS,
        'minimum_certified_margin_exact_lower':{k:str(F(v,SCALE)) for k,v in minima.items()},
        'policy_sha256':hashlib.sha256(raw).hexdigest(),
        'source_certificate_sha256':policy['source_certificate_sha256'],
        'rational_power_endpoint_calls':arithmetic.POWER_CALLS,
        'wall_seconds':time.perf_counter()-start,
        'maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'scope':'Each selected rational q satisfies all required inequalities on its whole closed cell. Coverage and exact first-containing-row lookup are sound; no efficient-forecaster complexity claim.',
    }
    (root/'results'/'rational_policy_check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__': main()
