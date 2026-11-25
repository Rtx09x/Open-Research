"""Exact cluster and separated-cover checks for the query/precision theorem."""
from fractions import Fraction as F
from itertools import combinations
import json

def run(m,eps_values):
    assert m>=5
    g=[1/(3+F(i+1,m+1)) for i in range(m)];C=sum(g);H=[1/(C-x) for x in g]
    radius=m//2;qs=[(i,i+radius) for i in range(radius)]
    if m%2:qs.append((0,m-1))
    assert len(qs)==(m+1)//2 and set(sum(([i,j] for i,j in qs),[]))==set(range(m))
    bound=F(27,4096);margin=None
    for p,q in qs:
        x,y=g[p],g[q];h=C-x-y;D=(C-x)*(C-y)
        assert abs(x-y)>F(1,48)
        low=[2-y+y*y/(C-x),2-x+x*x/(C-y)]
        high=[1/x-y+(1-y)**2/(C-x),1/y-x+(1-x)**2/(C-y)]
        outside=[2-x-y+(x-y)**2*H[i] for i in range(m) if i not in (p,q)]
        inside=low+high
        local=min([abs(a-b) for a,b in combinations(inside,2)]+
                  [abs(a-b) for a in inside for b in outside])
        assert local>bound
        margin=local if margin is None else min(local,margin)
    hs=sorted(H);delta=F(9,16*(m+1)*(m-1)**2);U=F(16,9*(m+1)*(m-1)**2)
    assert all(delta<b-a<U for a,b in zip(hs,hs[1:]))
    rows=[]
    for eps in eps_values:
        K=max(sum(x<=y<=x+2*eps for y in hs) for x in hs)
        kl=min(m,1+(2*eps//U));ku=min(m,1+(2*eps//delta))
        assert kl<=K<=ku
        lo=max(2,(K+1)//2);hi=min(m//2+1,K//2+2)
        fixed_lo=(m+1)//2;fixed_hi=m
        if eps<F(27,8192):
            hi=min(hi,(m+1)//2);fixed_hi=fixed_lo
        assert lo<=hi
        rows.append({'epsilon':str(eps),'K':K,'adaptive_lower':lo,'adaptive_upper':hi,
                     'fixed_lower':fixed_lo,'fixed_upper':fixed_hi})
    return {'m':m,'cover':qs,'minimum_local_margin':str(margin),
            'proved_cover_margin':'27/4096','results':rows}
if __name__=='__main__':
    es=list(map(F,['0','0.00000001','0.0000001','0.000001','0.00001','0.0001','0.001','0.003','0.01','0.06']))
    for m in [5,6,10,30,100]:print(json.dumps(run(m,es)),flush=True)
