"""Independent exact rational interval minimax verification; no stochastic model."""
from fractions import Fraction as F
from itertools import combinations
from functools import lru_cache
from pathlib import Path
import json, sys, time
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from exact_search import responses

def interval_masks(row, eta):
    intervals=[(x*(1-eta),x*(1+eta)) for x in row]
    endpoints=sorted({x for pair in intervals for x in pair})
    masks={sum(1<<i for i,(a,b) in enumerate(intervals) if a<=x<=b) for x in endpoints}
    # Only maximal compatible sets are relevant to worst-case diagnosis.
    return tuple(sorted(s for s in masks if s and not any(s!=t and s&t==s for t in masks)))

def adaptive(parts,m):
    infinity=m+1
    @lru_cache(None)
    def depth(s):
        if s.bit_count()<2:return 0
        best=infinity
        distinct=set()
        for p in parts:
            children=tuple(sorted({s&t for t in p if s&t}))
            if s in children or children in distinct:continue
            distinct.add(children)
            worst=0
            for child in sorted(children,key=int.bit_count,reverse=True):
                worst=max(worst,depth(child))
                if worst+1>=best:break
            best=min(best,worst+1)
        return best
    d=depth((1<<m)-1)
    return (None if d>=infinity else d),depth.cache_info().currsize

def fixed(parts,m):
    pairs=list(combinations(range(m),2));full=(1<<len(pairs))-1
    covers=[sum(1<<i for i,(a,b) in enumerate(pairs) if not any((s>>a&1) and (s>>b&1) for s in p)) for p in parts]
    allcover=0
    for c in covers:allcover|=c
    if allcover!=full:return None,None
    for k in range(len(parts)+1):
        for subset in combinations(range(len(parts)),k):
            union=0
            for q in subset:union|=covers[q]
            if union==full:return k,subset

out=[]
for n in range(4,8):
    edges=list(combinations(range(n),2));m=len(edges)
    matrix=[[F(2,n)+F(len(set(q)&set(e))**2,n*(n-2)) for e in edges] for q in edges]
    if n<=6:
        _,electrical=responses(n,edges)
        assert matrix==electrical
    alpha=F(1,4*n-7);beta=F(3,4*n-3);gamma=F(1,n-1)
    settings=[('zero',F(0)),('below_alpha',alpha/2),('at_alpha',alpha),('middle',(alpha+beta)/2),('at_beta',beta),('above_beta',(beta+gamma)/2),('at_gamma',gamma)]
    if n==7: settings=[settings[0],settings[1],settings[4]]
    for label,eta in settings:
        start=time.time();parts=[interval_masks(row,eta) for row in matrix]
        # Full exact noisy recursion at n<=6; pairwise impossibility also certified for n=7.
        if n==7 and eta>=beta:
            assert all(any(s&3==3 for s in p) for p in parts)
            a=None;states=0
        else:a,states=adaptive(parts,m)
        f,subset=fixed(parts,m)
        expected_a=n//2+1 if eta<alpha else m-1 if eta<beta else None
        expected_f=(2*n+2)//3 if eta<alpha else m-1 if eta<beta else None
        if n==5 and eta<alpha:expected_f=3
        assert a==expected_a,(n,label,a,expected_a)
        assert f==expected_f,(n,label,f,expected_f)
        rec=dict(n=n,eta=str(eta),regime=label,adaptive=a,fixed=f,fixed_queries=subset,states=states,seconds=time.time()-start)
        out.append(rec);print(json.dumps(rec),flush=True)
Path(__file__).with_name('results.json').write_text(json.dumps(out,indent=2)+'\n')
