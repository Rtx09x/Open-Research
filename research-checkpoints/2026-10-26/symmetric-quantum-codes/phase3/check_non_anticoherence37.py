"""Exact root-box counterexample to KL=>anticoherence; stdlib only.
Independent interval evaluation of the diagonal rank2 spin moment.
Root existence/all KL identities are verified in the separate code37 suite.
"""
from fractions import Fraction as Q
from math import comb
from pathlib import Path
import json
root=Path(__file__).parent;c=json.loads((root/'code37_root_certificate.json').read_text());center=[Q(1)]+list(map(Q,c['center']));rad=Q(c['radius']);p=[Q(0),Q(0)];norm=[Q(0),Q(0)]
for i,x in enumerate(center):
 r=0 if i==0 else rad;lo,hi=x-r,x+r;sqlo=0 if lo<=0<=hi else min(lo*lo,hi*hi);sqhi=max(lo*lo,hi*hi);w=comb(37,2*i);g=w*(3*(37-4*i)**2-37*39)
 norm[0]+=w*sqlo;norm[1]+=w*sqhi
 a,b=g*sqlo,g*sqhi;p[0]+=min(a,b);p[1]+=max(a,b)
assert norm[0]>0 and p[1]<0
out={'exact_interval_excludes_zero':True,'polynomial_interval':list(map(str,p)),'norm_interval':list(map(str,norm)),'normalized_difference_interval':[str(p[0]/(12*norm[0])),str(p[1]/(12*norm[1]))],'approx_difference':float(sum(comb(37,2*i)*(3*(37-4*i)**2-37*39)*x*x for i,x in enumerate(center))/(12*sum(comb(37,2*i)*x*x for i,x in enumerate(center)))),'meaning':'Exact distance7 code37 is not2-anticoherent. KL scalar compressions are not forced zero.'}
(root/'non_anticoherence37.json').write_text(json.dumps(out,indent=2));print({k:v for k,v in out.items()if not k.endswith('interval')})
