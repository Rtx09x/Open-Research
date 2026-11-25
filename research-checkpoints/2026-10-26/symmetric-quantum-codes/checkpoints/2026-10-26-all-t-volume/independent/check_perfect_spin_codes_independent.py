"""Independent finite all-t equality exclusion, no worker imports.
Derive a Newton-coefficient obstruction symbolically, then exhaust divisors.
"""
from fractions import Fraction as F
from pathlib import Path
import json,time,math
import sympy as S
start=time.monotonic();t=S.symbols('t',integer=True,positive=True);n=2*(t+1)**2-1
# A_h/A_(h+1) follows directly from terminating4F3 coefficient ratios.
ratio=lambda h: -(h+1)*(h+2)*(n-h)*(n+h+2)/((t-h)*(t+h+2))
third=S.factor(-ratio(t-1)*ratio(t-2)*ratio(t-3))
P=t**2*(t-2)*(t-1)**2*(t+1)*(t+2)*(2*t+5)*(2*t*t+3*t+2)*(2*t*t+3*t+3)*(2*t*t+3*t+4)*(2*t*t+5*t+1)
assert S.cancel(third-P/(12*(2*t-1)))==0
assert S.Poly(P,t).degree()==16 and P.subs(t,S.Rational(1,2))==-S.Rational(2025,2)
# If D=2t-1 divides integer P(t), then 2^16 P(t)==-2025*2^15 modD.
# D is odd, so D|2025. This does not assume a rational polynomial quotient
# is integer-valued without clearing powers of2.
divisors=sorted(3**a*5**b for a in range(5) for b in range(3))
assert len(divisors)==15 and all(2025%d==0 for d in divisors)
candidates=[(d+1)//2 for d in divisors if d>=5]
assert candidates==[3,5,8,13,14,23,38,41,68,113,203,338,1013]

def newton_coeffs(T):
    N=2*(T+1)**2-1;out={T:F(1)}
    for h in range(T-1,-1,-1):
        out[h]=out[h+1]*F(-(h+1)*(h+2)*(N-h)*(N+h+2),(T-h)*(T+h+2))
        if out[h].denominator!=1:return out,h
    return out,None

def standard_mod(coeff,T,p):
    # B_0=1;B_(h+1)=(x-h(h+1))B_h. Coefficients low-first.
    basis=[1];ret=[0]*(T+1)
    for h in range(T+1):
        for i,v in enumerate(basis):ret[i]=(ret[i]+int(coeff[h])*v)%p
        nxt=[0]*(len(basis)+1)
        for i,v in enumerate(basis):nxt[i]=(nxt[i]-h*(h+1)*v)%p;nxt[i+1]=(nxt[i+1]+v)%p
        basis=nxt
    assert ret[-1]==1
    return ret

def strip_roots(poly,p):
    # Independent synthetic division in descending order, retaining repeats.
    desc=poly[::-1]
    for root in range(p):
        while len(desc)>1:
            q=[desc[0]]
            for v in desc[1:]:q.append((v+root*q[-1])%p)
            if q[-1]!=0:break
            desc=q[:-1]
    return desc[::-1]

primes={3:19,5:23,8:23,14:3};rows=[]
for T in candidates:
    coeff,obstruction=newton_coeffs(T)
    if obstruction is not None:
        c=coeff[obstruction];rows.append({'t':T,'reason':'noninteger_monic_Newton_coefficient','index':obstruction,'coefficient':str(c),'distance_from_top':T-obstruction})
    else:
        p=primes[T];poly=standard_mod(coeff,T,p);rem=strip_roots(poly,p)
        assert len(rem)>1 and all(sum(v*pow(r,i,p) for i,v in enumerate(rem))%p for r in range(p))
        rows.append({'t':T,'reason':'monic_polynomial_not_completely_split_mod_prime','prime':p,'polynomial_mod_p':poly,'remaining_root_free_factor':rem})
assert {r['t']for r in rows if r['reason'].startswith('monic_')}==set(primes)
# Explicit t2 monic polynomial, derive by integer Newton expansion.
c,_=newton_coeffs(2);assert c=={2:F(1),1:F(-384),0:F(31008)}
# B2=x(x-2), so x²−386x+31008=(x−114)(x−272).
assert 114+272==386 and 114*272==31008
assert math.isqrt(1+4*114)**2!=1+4*114
assert 272==16*17
c,_=newton_coeffs(1);assert c=={1:F(1),0:F(-42)} and 42==6*7
out={'PASS':True,'scope':'No K2 code saturates n+1=2(t+1)^2 for any integer t>=2, conditional only on separately audited all-t volume/equality-quadrature theorem; not full3t²+3t+1 conjecture','symbolic_third_Newton_coefficient':str(third),'P_degree':16,'P_at_half':'-2025/2','congruence':'2^16 P(t) = -2025*2^15 mod(2t-1); odd divisor permits cancellation','all_positive_divisors_2025':divisors,'remaining_t_ge3':candidates,'finite_cases':rows,'t2':'114 is not r(r+1), while272=16*17','t1_positive_control':'root42=6*7 remains possible','resulting_integer_length_bound':'n>=2t^2+4t+2 for K2,t>=2','seconds':time.monotonic()-start}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
