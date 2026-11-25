#!/usr/bin/env python3
"""Exact eight-endpoint certificate for the entire convex step-charge family.
Analytic reduction is in TYPE_MIXTURE_THEOREM.md; no grid or optimizer proof.
"""
from fractions import Fraction as F
from pathlib import Path
import json
H=Path(__file__).resolve().parent;ROOT=H.parent.parent
J=json.loads((H/'type_mixture_certificate.json').read_text());R=F(J['target']);rows=J['critical_fixed_mixture_dual']
types={F(A):F(al) for A,al in J['parameters']['212']['containers']}
d=F(1,43);B=sum(A*al for A,al in types.items());b=types[F(1)]
a1=F(17,60)-d;a2=1-d;ql=1/a2;qh=1/a1
p=F(rows[0]['residual']);g=F(rows[1]['residual']);assert 0<p<g<d
assert sum(F(row['lambda_weight']) for row in rows)==1 and all(F(row['lambda_weight'])>0 for row in rows)
def item(c,q,s):
    kap=sum(al*max(F(0),1-q*(A-d)) for A,al in types.items());den=B-c-(d-c)*kap
    assert den>=B-d>0
    return b/den*s*(1+(d-c)*q*int(s>c))
tests=[]
for q in [ql,qh]:
    for c in [F(0),p,g,d]:
        v=sum(F(row['lambda_weight'])*(F(row['constant'])+item(c,q,F(row['residual']))) for row in rows)
        assert v>=R
        tests.append({'c':str(c),'q':str(q),'dual_value':str(v),'gap':str(v-R),'equality':v==R})
assert [(t['c'],t['q']) for t in tests if t['equality']]==[(str(p),str(ql)),(str(g),str(qh))]
oldBF=F(json.loads((ROOT/'phase2/best_fit/best_fit_certificate.json').read_text())['target'])
oldAH=F(json.loads((ROOT/'ah_three_parameter_full_certificate.json').read_text())['target'])
assert F(rows[0]['constant'])+b*p/(B-g)==oldBF
assert F(rows[1]['constant'])+b*g/(B-d)==oldAH>oldBF>R
# These identities control all q outside the undominated interval and give the
# entire single-charge floor, not just the tested endpoint sample.
assert sum(al*(A-d) for A,al in types.items())==B-d
assert types[F(17,60)]*(1-ql*a1)==1-ql*(B-d)
assert qh*a1==1 and ql*a2==1
out={'status':'PASS exact continuous-family dual certificate','target':str(R),
 'scope':'all finite convex mixtures of type-resolved step charges, with fixed algorithm parameters and non-tiny weights; not actual algorithm tightness',
 'single_charge_optimum':str(oldBF),'strict_mixture_improvement':str(oldBF-R),
 'undominated_q_interval':[str(ql),str(qh)],'critical_c_endpoints':[str(v) for v in [F(0),p,g,d]],
 'dual_weights':[row['lambda_weight'] for row in rows],'endpoint_checks':tests}
(H/'family_optimum_verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
