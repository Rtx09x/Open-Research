"""Conservative analytic lower bound on nonzero syndrome variance.
Uses the audited pure-complement dual separation plus HS norm perturbation.
"""
import json
from pathlib import Path
import sympy as s
from intrinsic_lp import transform
ROOT=Path(__file__).parent;N=19;M=transform(18)
c=[s.Rational(91,285),s.Rational(288199,1187025),s.Rational(33176,237405),s.Rational(10120,142443)]
cert=json.loads((ROOT/'pure_complement_short_certificate.json').read_text());y=[s.Rational(v)for v in cert['y']]
ylow=y[6:10];yc=y[10:12];rows=[1,3]
w=max(abs(sum(v*(M[r,k]-(1 if r==k else 0))for v,r in zip(yc,rows)))for k in range(N))
a=N*max([s.Integer(0)]+[v/cc for v,cc in zip(ylow,c)])
# If nu<=q^2, then delta<=sqrt(2) N q< (3/2)Nq.
# Needed: 1 <= a*nu + N*w*(2*sqrt(2)*N*sqrt(nu)+2*N^2*nu).
for den in [10**k for k in range(1,8)]:
 q=s.Rational(1,den);bound=a*q*q+N*w*(3*N*q+2*N*N*q*q)
 if bound<1:break
assert bound<1
out={'scope':'all hypothetical n18 codes, conditional on preceding exact reductions','variance_definition':'nu=||G-I9/19||F^2','necessary_lower_bound':str(q*q),'strict':True,'A':str(a),'w':str(w),'rational_upper_at_test':str(bound),'bound_float':str(bound.evalf()),'reason':'If nu<=q^2, exact dual plus ||Q0-Q||F^2=2*N^2*nu implies1<=bound<1.'}
(ROOT/'robust_pure_gap_certificate.json').write_text(json.dumps(out,indent=2));print(out)
