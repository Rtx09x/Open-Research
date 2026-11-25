#!/usr/bin/env python3
"""Two-point obstruction to constant q for THIS new certificate's budgets.
Not a lower bound against every fixed-bias strategy or all parameter choices.
"""
from mpmath import iv
import json
from pathlib import Path
iv.dps=60
I=iv.mpf
a,b,rho,k,d,p,p0=map(I,['.0102','.9475','.0097','.6','14.8','.856','.85599'])
U=2**a*k**b
# At initial-epoch trigger z=0,r=rho, persistent plus needs q<=upper.
upper=(p0*(1+rho+k)**b-1)/U
# At tau/h=delta and equal half counts, completed minus needs q>=lower.
S=(d+2+k)**b;B=p*d**b+1
lower=U/(p0*S-B)
assert upper < I('.56') and lower > I('.75')
assert lower>upper
out={'scope':'No constant q satisfies both endpoint inventory budgets for these fixed constants; not a universal fixed-bias lower bound.', 'upper_at_z0_rrho':str(upper),'lower_at_zdelta_r1':str(lower),'gap_lower':str((lower-upper).a),'checks_passed':True}
Path(__file__).with_name('fixed_q_obstruction.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
