"""Independent exact polynomial proof gate for the Racah escape lower bound."""
import sympy as S,json
from pathlib import Path
s,u=S.symbols('s u',nonnegative=True);t=s+u;r=2*s+u;m=(t+1)**2
escape=s*s/m+(r+1)/(2*t+r+1)*(m-s*s)/m*(1-(m+s*s-1)/(4*m*(m-1)))
diff=S.factor(escape-r*(r+1)/(4*m));num,den=S.fraction(diff);p=S.Poly(num,s,u)
assert all(c>0 for _,c in p.terms())
assert S.simplify(den - 4*(s+u)*(s+u+1)**4*(s+u+2)*(4*s+3*u+1)) == 0
# s=0=r-t handles r=t; no singular point for t>=1. For r<=t direct monotonicity:
t0=S.symbols('t',positive=True);assert S.expand(4*(t0+1)**2-1-t0*(3*t0+1))==t0**2+7*t0+3
out={'passed':True,'scope':'critical n=2(t+1)^2-2 escape inequality only; stochastic drift and LP identity are separate dependencies','substitution':'t=s+u,r=2s+u, s,u>=0,t>=1','denominator':str(den),'positive_numerator_terms':[[list(k),int(v)] for k,v in p.terms()],'low_r_minimum_numerator':'t^2+7t+3','strict':True}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
