#!/usr/bin/env python3
"""Finite exact refinement of the two observed active patterns; full oracle check."""
from explore import *

def row(pattern):
    look={j:(sz,w) for j,sz,w in normal}
    return Q(1)-sum(look[j][0] for j in pattern),sum(look[j][1] for j in pattern)
rP,kP=row([1,165,179,205,208,211]);rQ,kQ=row([1,165,179,187])
assert rP==p and rQ==Q(29,1254)
def values(g):
    mix=[(p,g,1/(1-g),Q(1))]
    return [K+envelope(P,B,b,r,mix) for r,K in [(rP,kP),(rQ,kQ)]]
lo=Q(163,7740);hi=Q(223,10320)
assert values(lo)[0]<values(lo)[1] and values(hi)[0]>values(hi)[1]
for _ in range(100):
    mid=(lo+hi)/2;u,v=values(mid)
    if u<v:lo=mid
    else:hi=mid
den=10**12;n=int(lo*den)
choices=[Q(n,den),Q(n+1,den)]
g=min(choices,key=lambda z:max(values(z)))
mix=[(p,g,1/(1-g),Q(1))]
out=[price(items[h],caps[h],P,B,b,mix,h) for h in range(2)]
R=max(t[0] for t in out);assert R==max(values(g))<Q(J['target'])
result={'status':'PASS exact critical-scenario pricing; global/all-input certificate pending','g':g,'c':p,'mixture':mix,'target':R,'target_decimal':float(R),'active_face_rows':[{'pattern':[1,165,179,205,208,211],'constant':kP,'residual':rP,'value':values(g)[0]},{'pattern':[1,165,179,187],'constant':kQ,'residual':rQ,'value':values(g)[1]}],'intersection_bracket':[lo,hi],'decimal_grid_denominator':den,'oracle':[{'maximum':v,'pattern':pat,'nodes':n} for v,pat,n in out]}
(H/'refined_candidate.json').write_text(json.dumps(result,default=str,indent=2)+'\n')
print('g',str(g),'R',str(R),float(R),'P/Q',[float(x) for x in values(g)],'nodes',sum(z[2] for z in out))
