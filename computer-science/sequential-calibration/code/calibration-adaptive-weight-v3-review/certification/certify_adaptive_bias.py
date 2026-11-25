#!/usr/bin/env python3
"""Independent interval certificate for a genuinely state-dependent bias rule.

Checks the FULL continuous trigger domain by a covering dyadic partition.
Does not infer uniform inequalities from sampled points. No optimization.
"""
from fractions import Fraction
from pathlib import Path
import hashlib
import json
import resource
import time
import mpmath
from mpmath import iv

iv.dps = 60
I = iv.mpf
VALUES = dict(alpha='.0102', beta='.9475', rho='.0097', kappa='.6',
              delta='14.8', kp='.856', kt='.902', P0='.85599',
              Q0='.9019', qmax='.76', F='10000000000')
alpha,beta,rho,kappa,delta,kp,kt,P0,Q0,qmax,F = (I(VALUES[k]) for k in VALUES)
v = 2**alpha
power = 1/(1-beta)
U = v*kappa**beta


def clamp(x,lo,hi):
    return I([min(hi.a,max(lo.a,x.a)),min(hi.b,max(lo.b,x.b))])


def pointwise_max(x,y):
    return I([max(x.a,y.a),max(x.b,y.b)])


def holder(x,y):
    return (x**power+y**power)**(1/power)


def fraction_interval(f):
    return I(f.numerator)/f.denominator


def interval_from_fractions(lo,hi):
    a,b = fraction_interval(lo),fraction_interval(hi)
    return I([a.a,b.b])


def test_box(segment,lo,hi):
    x = interval_from_fractions(lo,hi)
    if segment == 1:
        z,r = x,rho
    else:
        z,r = delta*x,x
    S = (z+1+r+kappa)**beta
    B = kp*z**beta+r**beta
    denom = P0*S-B
    if not denom > 0:
        return None
    q = pointwise_max(I('.5'),U/denom)
    margins = {
        'positive_denominator':denom,
        'q_upper':qmax-q,
        'persistent_plus':P0*S-kp*z**beta-1-q*U,
        'total_plus':Q0*S-kp*z**beta-1-r**beta-q*U,
    }
    if not all(m > 0 for m in margins.values()):
        return None
    return {k:str(m.a) for k,m in margins.items()}


start = time.perf_counter()
assert 0 < alpha < beta < 1 and alpha+beta < 1
assert 0 < rho <= 1 and 0 < kappa <= 1 and delta > 0
assert 0 < P0 < kp < kt and 0 < Q0 < kt and kp < 1
assert P0 < Q0
assert I('.5') <= qmax <= 1
x = clamp(kp**(-power),I(0),1/delta)
M_tau = holder((kp+x**beta)/(1+x)**beta,I(1))
M_rho = holder(kp,(1+rho**beta)/(1+rho)**beta)
M = max(M_tau.b,M_rho.b)
D0,D1 = holder(kt,I(1)),holder(M,v*qmax)
D = max(D0.b,D1.b)
global_margins = {
    'persistent_rounding':kp-P0*(1+1/F)-F**(-beta),
    'total_rounding':kt-Q0*(1+1/F)-F**(-beta),
    'live_induction':v-D-F**(-beta),
    'minus_monotonicity':v/qmax-kp,
}
assert all(m > 0 for m in global_margins.values())
assert kp <= M <= D
domains = [(1,Fraction(0),Fraction(VALUES['delta'])*Fraction(VALUES['rho'])),
           (2,Fraction(VALUES['rho']),Fraction(1))]
leaves = []
box_count = 0
max_depth = 0
for segment,lo,hi in domains:
    todo = [(lo,hi,0)]
    while todo:
        lo,hi,depth = todo.pop()
        box_count += 1
        max_depth = max(max_depth,depth)
        result = test_box(segment,lo,hi)
        if result is not None:
            leaves.append({'segment':segment,'lo':str(lo),'hi':str(hi),
                           'depth':depth,'strict_lower_bounds':result})
        else:
            assert depth < 24, ('Uncertified interval',segment,str(lo),str(hi))
            mid = (lo+hi)/2
            todo.extend([(mid,hi,depth+1),(lo,mid,depth+1)])

# Verify the accepted leaves cover both complete domains exactly, without gaps.
for segment,lo,hi in domains:
    part = sorted((Fraction(x['lo']),Fraction(x['hi'])) for x in leaves if x['segment']==segment)
    assert part[0][0] == lo and part[-1][1] == hi
    assert all(a[1] == b[0] for a,b in zip(part,part[1:]))
    assert all(a < b for a,b in part)
eps = 1-Fraction(VALUES['alpha'])-Fraction(VALUES['beta'])
theta = (2+eps)/(3+2*eps)
report = {
    'parameters_exact_decimals':VALUES,
    'q_rule':'max(1/2, U/(P0*S-B)); U=2^alpha*kappa^beta, S=(z+1+r+kappa)^beta, B=Kp*z^beta+r^beta',
    'domain':'segment1 r=rho,z in[0,delta*rho]; segment2 z=delta*r,r in[rho,1]',
    'interval_precision_decimal_digits':iv.dps,'mpmath_version':mpmath.__version__,
    'all_checks_passed':True,'covered_leaves':len(leaves),'evaluated_boxes':box_count,
    'max_subdivision_depth':max_depth,
    'global_margins':{k:str(x) for k,x in global_margins.items()},
    'witnesses':{k:str(x) for k,x in dict(M=M,D=D,D0=D0,D1=D1).items()},
    'epsilon_exact':str(eps),'conditional_calibration_exponent_exact':str(theta),
    'conditional_calibration_exponent_decimal':str(float(theta)),
    'wall_seconds':time.perf_counter()-start,
    'maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'scope':'Certifies numerical obligations for adaptive-bias induction; theorem requires separate algorithm/proof audit. No novelty or final theorem claim.',
    'partition':leaves,
}
out = Path(__file__).parent/'results'/'adaptive_bias_certificate.json'
out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='partition'},indent=2),flush=True)
