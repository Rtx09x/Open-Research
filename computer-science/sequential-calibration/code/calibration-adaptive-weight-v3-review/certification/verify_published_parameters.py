#!/usr/bin/env python3
"""Recompute DF v2 Appendix A inequalities with outward intervals.

This is a source-control/reproduction check, NOT a new exponent or proof.
Analytic extrema are derived in Appendix A; this file checks their numerical
obligations using exact-decimal interval inputs and exact rational reduction.
"""
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import time
import mpmath
from mpmath import iv

iv.dps = 80
I = iv.mpf
alpha,beta,lam,rho,kappa,kp,kt,delta = map(I,[
    '0.0082540892','0.9574603467','1.9444858156','0.0164237243',
    '0.4148723339','0.8812155678','0.9208553424','9.4880928733'])
F = I('10000000000')
v = 2**alpha
q = 1/(1-beta)


def clamped(x, lo, hi):
    return I([min(hi.a,max(lo.a,x.a)),min(hi.b,max(lo.b,x.b))])


def holder(a,b):
    return (a**q+b**q)**(1/q)


def trigger_maxima(a,b):
    # Boundary 1: r=rho, 0 <= z <= delta*rho.
    z = clamped((kp*(1+rho+kappa)/(a*rho**beta+b))**q,I(0),delta*rho)
    first = (kp*z**beta+a*rho**beta+b)/(z+1+rho+kappa)**beta
    # Boundary 2: z=delta*r, rho <= r <= 1.
    r = clamped(((kp*delta**beta+a)*(1+kappa)/((1+delta)*b))**q,rho,I(1))
    second = ((kp*delta**beta+a)*r**beta+b)/((1+delta)*r+1+kappa)**beta
    return max(first.b,second.b), {'z':str(z),'r':str(r),'first':str(first),'second':str(second)}


start = time.perf_counter()
x = clamped(kp**(-q),I(0),1/delta)
m1 = holder((kp+x**beta)/(1+x)**beta,I(1))
m2 = holder(kp,(1+rho**beta)/(1+rho)**beta)
M = max(m1.b,m2.b)  # exact binary endpoint used as the auxiliary witness
d1,d2 = holder(kt,I(1)),holder(M,v/lam)
D = max(d1.b,d2.b)
Pplus,plus_detail = trigger_maxima(I(0),1+v*kappa**beta/lam)
Pminus,minus_detail = trigger_maxima(I(1),lam*v*kappa**beta)
Q,total_detail = trigger_maxima(I(1),1+v*kappa**beta/lam)
P = max(Pplus,Pminus)
rounding,inflation = F**(-beta),1+1/F
margins = {
    'persistent_terminal':kp-(P*inflation+rounding),
    'total_terminal':kt-(Q*inflation+rounding),
    'unfinished_epoch':v-(D+rounding),
    'terminal_minus':kp-(Pminus*inflation+rounding),
    'terminal_plus':kp-(Pplus*inflation+rounding),
    'intermediate_deficit_condition':lam*v-kp,
}
assert 0 < alpha < 1 and 0 < beta < 1
assert 1 < lam <= 2 and 0 < rho <= 1 and 0 < kappa <= 1 and delta > 0
assert F >= 1 and 0 < kp < 1 and kt > kp and kp <= M <= D and P > 0 and Q > 0
assert m1.b <= M and m2.b <= M and d1.b <= D and d2.b <= D
assert Pplus <= P and Pminus <= P
for key,margin in margins.items():
    assert margin > 0, (key,margin)
eps = 1-Fraction('0.0082540892')-Fraction('0.9574603467')
exponent = (2+eps)/(3+2*eps)
assert eps == Fraction('0.0342855641')
assert exponent == Fraction(20342855641,30685711282)
assert Fraction('0.662942288')-exponent == Fraction(162390413,958928477562500000)
report = {
    'source':'https://arxiv.org/html/2610.07623v2#A1',
    'scope':'Numerical Appendix A sufficient inequalities; not independent verification of full inductive or minimax proof',
    'mpmath_version':mpmath.__version__, 'interval_decimal_precision':iv.dps,
    'all_checks_passed':True, 'margins':{k:str(v) for k,v in margins.items()},
    'auxiliary_witnesses':{'M':str(M),'D':str(D),'P':str(P),'Q':str(Q)},
    'endpoint_details':{'plus':plus_detail,'minus':minus_detail,'total':total_detail},
    'epsilon_exact':str(eps),'exponent_exact':str(exponent),
    'printed_exponent_slack_exact':str(Fraction('0.662942288')-exponent),
    'seconds':time.perf_counter()-start,
    'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
out = Path(__file__).parent/'results'/'published_parameter_certificate.json'
out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
