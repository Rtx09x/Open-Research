#!/usr/bin/env python3
"""Replay all adaptive-bias inequalities with ONLY standard-library integers.

Every interval endpoint is a dyadic rational. Rational powers use certified
integer nth roots; floating point is used ONLY to seed an integer iteration,
and exact integer assertions validate every returned root. Neither mpmath nor
the generating checker is imported. Partition coverage is independently checked.
"""
from fractions import Fraction
from pathlib import Path
import hashlib
import json
import math
import resource
import time

BITS = 80
SCALE = 1 << BITS
ROOT = Path(__file__).parent
POWER_CALLS = 0


def floor_nthroot(n,k):
    assert n >= 0 and k >= 1
    if n < 2 or k == 1:
        return n
    shift = max(0,n.bit_length()-53)
    estimate = int(2.0**((math.log2(n >> shift)+shift)/k))
    y = max(1,estimate+max(8,estimate >> 40))
    while y**k < n:
        y *= 2
    while True:
        z = ((k-1)*y+n//(y**(k-1)))//k
        if z >= y:
            break
        y = z
    assert y**k <= n < (y+1)**k
    return y


class Dyadic:
    def __init__(self,lo,hi=None):
        self.lo,self.hi = lo,lo if hi is None else hi
        assert self.lo <= self.hi
    @staticmethod
    def rational(x):
        f = Fraction(x)
        return Dyadic((f.numerator*SCALE)//f.denominator,
                      -((-f.numerator*SCALE)//f.denominator))
    def __add__(a,b):
        if not isinstance(b,Dyadic): b=Dyadic.rational(b)
        return Dyadic(a.lo+b.lo,a.hi+b.hi)
    __radd__ = __add__
    def __neg__(a): return Dyadic(-a.hi,-a.lo)
    def __sub__(a,b):
        if not isinstance(b,Dyadic): b=Dyadic.rational(b)
        return a+-b
    def __rsub__(a,b): return -a+b
    def __mul__(a,b):
        if not isinstance(b,Dyadic): b=Dyadic.rational(b)
        products=[a.lo*b.lo,a.lo*b.hi,a.hi*b.lo,a.hi*b.hi]
        return Dyadic(min(products)//SCALE,-((-max(products))//SCALE))
    __rmul__ = __mul__
    def __truediv__(a,b):
        if not isinstance(b,Dyadic): b=Dyadic.rational(b)
        assert b.lo > 0
        vals=[Fraction(a.lo*SCALE,b.lo),Fraction(a.lo*SCALE,b.hi),
              Fraction(a.hi*SCALE,b.lo),Fraction(a.hi*SCALE,b.hi)]
        lo,hi=min(vals),max(vals)
        return Dyadic(lo.numerator//lo.denominator,-((-hi.numerator)//hi.denominator))
    def __rtruediv__(a,b): return Dyadic.rational(b)/a
    def __pow__(a,exponent):
        global POWER_CALLS
        exponent=Fraction(exponent)
        if exponent < 0:
            return 1/(a**(-exponent))
        assert a.lo >= 0 and exponent > 0
        num,den=exponent.numerator,exponent.denominator
        def endpoint(x):
            global POWER_CALLS
            POWER_CALLS += 1
            scaled=x**num
            if den >= num:
                scaled <<= BITS*(den-num)
            else:
                scaled >>= BITS*(num-den)
            return floor_nthroot(scaled,den)
        return Dyadic(endpoint(a.lo),endpoint(a.hi)+1)
    def lower_text(a): return str(Fraction(a.lo,SCALE))
    def __repr__(a): return f'[{Fraction(a.lo,SCALE)},{Fraction(a.hi,SCALE)}]'


def pointmax(a,b): return Dyadic(max(a.lo,b.lo),max(a.hi,b.hi))
def pointmin(a,b): return Dyadic(min(a.lo,b.lo),min(a.hi,b.hi))


def main():
    start=time.perf_counter()
    path=ROOT/'results'/'adaptive_bias_certificate.json'
    raw=path.read_bytes()
    certificate=json.loads(raw)
    vals=certificate['parameters_exact_decimals']
    assert vals == dict(alpha='.0102', beta='.9475', rho='.0097', kappa='.6',
                        delta='14.8', kp='.856', kt='.902', P0='.85599',
                        Q0='.9019', qmax='.76', F='10000000000')
    A={k:Dyadic.rational(v) for k,v in vals.items()}
    beta,alpha=Fraction(vals['beta']),Fraction(vals['alpha'])
    rho,kappa,delta,kp,kt,P0,Q0,qmax,F=(A[k] for k in ['rho','kappa','delta','kp','kt','P0','Q0','qmax','F'])
    assert Fraction(vals['P0']) < Fraction(vals['Q0'])
    H=Dyadic.rational(2)**alpha
    U=H*kappa**beta
    p=1/(1-beta)
    def holder(x,y): return (x**p+y**p)**(1/p)
    x=pointmin(1/delta,kp**(-p))
    Mt=holder((kp+x**beta)/(1+x)**beta,Dyadic.rational(1))
    Mr=holder(kp,(1+rho**beta)/(1+rho)**beta)
    M=Dyadic(max(Mt.hi,Mr.hi))
    D0=holder(kt,Dyadic.rational(1))
    D1=holder(M,H*qmax)
    D=Dyadic(max(D0.hi,D1.hi))
    scalar={
        'persistent_rounding':kp-P0*(1+1/F)-F**(-beta),
        'total_rounding':kt-Q0*(1+1/F)-F**(-beta),
        'live_induction':H-D-F**(-beta),
        'minus_monotonicity':H/qmax-kp,
    }
    assert all(x.lo > 0 for x in scalar.values())
    leaves=certificate['partition']
    domains=[(1,Fraction(0),Fraction(vals['delta'])*Fraction(vals['rho'])),
             (2,Fraction(vals['rho']),Fraction(1))]
    for segment,left,right in domains:
        pairs=sorted((Fraction(b['lo']),Fraction(b['hi'])) for b in leaves if b['segment']==segment)
        assert pairs[0][0]==left and pairs[-1][1]==right
        assert all(a<b for a,b in pairs)
        assert all(a[1]==b[0] for a,b in zip(pairs,pairs[1:]))
    minima={key:None for key in ['denominator','q_upper','persistent_plus','total_plus']}
    for index,box in enumerate(leaves):
        lo,hi=Dyadic.rational(box['lo']),Dyadic.rational(box['hi'])
        x=Dyadic(lo.lo,hi.hi)
        z,r=(x,rho) if box['segment']==1 else (delta*x,x)
        zp,rp=z**beta,r**beta
        S=(z+1+r+kappa)**beta
        denominator=P0*S-kp*zp-rp
        assert denominator.lo>0,(index,'denominator')
        q=pointmax(Dyadic.rational(Fraction(1,2)),U/denominator)
        margins={'denominator':denominator,'q_upper':qmax-q,
                 'persistent_plus':P0*S-kp*zp-1-q*U,
                 'total_plus':Q0*S-kp*zp-1-rp-q*U}
        for name,value in margins.items():
            assert value.lo>0,(index,name,str(value))
            if minima[name] is None or value.lo<minima[name]: minima[name]=value.lo
    report={
        'backend':'stdlib integer dyadic arithmetic with exactly checked integer nth roots',
        'dyadic_precision_bits':BITS,'all_checks_passed':True,
        'covering_boxes_checked':len(leaves),'rational_power_endpoint_calls':POWER_CALLS,
        'scalar_margins_exact_lower':{k:v.lower_text() for k,v in scalar.items()},
        'box_margin_exact_min_lower':{k:str(Fraction(v,SCALE)) for k,v in minima.items()},
        'conditional_exponent_exact':str((2+1-alpha-beta)/(3+2*(1-alpha-beta))),
        'wall_seconds':time.perf_counter()-start,
        'maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'input_certificate_sha256':hashlib.sha256(raw).hexdigest(),
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    (ROOT/'results'/'rational_replay.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__': main()
