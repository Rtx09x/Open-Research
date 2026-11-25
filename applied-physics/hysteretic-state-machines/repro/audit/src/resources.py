"""Exact resource laws developed in the audit extension.

Interaction cost means distinct nonconstant directed multilinear monomials,
counted once when the two branches share the same shift. It is not gate area.
"""
from __future__ import annotations
from independent import Device,verify_device
from math import ceil


def independent_minimum(f:list[int]) -> int | None:
    """Exact minimum with no inter-element interactions; None means impossible."""
    m=len(f)
    if not m or any(type(t)!=int or not 0<=t<m for t in f):raise ValueError('map')
    if any(f[t]!=t for t in f):return None
    p=len(set(f));D=max(f.count(t) for t in set(f))
    return D-1+(p-1).bit_length()


def independent_machine(f:list[int])->dict:
    n=independent_minimum(f)
    if n is None:raise ValueError('Not idempotent')
    roots=sorted(set(f));r=max(f.count(t) for t in roots)-1
    activated=(1<<r)-1;codes=[0]*len(f)
    for label,t in enumerate(roots):
        root=activated|(label<<r);codes[t]=root
        leaves=[x for x in range(len(f)) if x!=t and f[x]==t]
        for j,x in enumerate(leaves):codes[x]=root^(1<<j)
    D=8*(n+1)
    return {'kind':'affine','n':n,'scale':D,'low':0,'highs':[3*D],
            'a':[2 if i<r else 4 for i in range(n)],'b':[-4 if i<r else -2 for i in range(n)],
            'J':[[0]*n for _ in range(n)],'codes':codes,'f':f,
            'activated_bits':r,'exact_no_interaction_minimum':n}


def coverage(k:int,e:int,d:int,c:int)->int:
    """Largest number of missing-bit incidences covered by c degree-d terms."""
    if min(k,e,c)<0 or d<1:raise ValueError('domain')
    a,r=divmod(k,d)
    return d*min(c,e*a)+r*min(e,max(0,c-e*a))


def required_terms(q:int,k:int,e:int,d:int)->int|None:
    if q<0 or k<0 or e<0 or d<1:raise ValueError('domain')
    if q==0:return 0
    if q>k*e:return None
    a,r=divmod(k,d);full=e*a*d
    if q<=full:return (q+d-1)//d
    assert r>0
    return e*a+(q-full+r-1)//r


def reset_frontier(m:int,n:int,d:int)->dict|None:
    """Exact least interaction-term cost among reset devices with <=n bits.

    The formula covers arbitrary real signs, branch-dependent thresholds, and
    degree<=d. A common nonnegative-shift construction attains it. d=0 uses the
    separate interaction-free theorem. Memory counts include unused bits when
    the budget n exceeds what the selected construction uses.
    """
    if type(m)!=int or m<2 or type(n)!=int or n<1 or type(d)!=int or d<0:
        raise ValueError('domain')
    if d==0:
        return {'m':m,'n':n,'degree':0,'terms':0,'k':m-1,'row_sizes':[]} if n>=m-1 else None
    candidates=[]
    for k in range(1,n+1):
        q=max(0,m-1-k);e=n-k;c=required_terms(q,k,e,d)
        if c is not None:candidates.append((c,k,q))
    if not candidates:return None
    c,k,q=min(candidates,key=lambda t:(t[0],-t[1]))
    if q==0:k=min(k,m-1)
    # Allocate full d-bit blocks before partial final blocks in each row.
    e=n-k;a,r=divmod(k,d);row_sizes=[0]*e;remaining=q
    for i in range(e):
        take=min(remaining,a*d);row_sizes[i]+=take;remaining-=take
    for i in range(e):
        take=min(remaining,r);row_sizes[i]+=take;remaining-=take
    assert not remaining
    assert sum((v+d-1)//d for v in row_sizes)==c
    return {'m':m,'n':n,'degree':d,'terms':c,'k':k,'row_sizes':row_sizes}


def reset_incidence_minimum(m:int,n:int)->int|None:
    """Exact sum of monomial arities (source incidences), for any degree >=1.

    This counts occurrences in directed monomials, not fabricated wire lengths
    or shared mechanical components. Higher arity cannot lower this minimum.
    """
    if m<2 or n<1:raise ValueError('domain')
    feasible=[k for k in range(1,n+1) if m-1<=k*(n-k+1)]
    if not feasible:return None
    return max(0,m-1-max(feasible))


def reset_construct(m:int,n:int,d:int)->dict:
    info=reset_frontier(m,n,d)
    if info is None:raise ValueError('Infeasible resource request')
    if d==0:
        out=independent_machine([0]*m);out['resource_certificate']=info;return out
    k=info['k'];T=(1<<k)-1;codes=[T]
    codes.extend(T^(1<<j) for j in range(min(k,m-1)))
    groups=[]
    for v in info['row_sizes']:
        groups.append([sum(1<<j for j in range(a,min(a+d,v))) for a in range(0,v,d)])
    for r,v in enumerate(info['row_sizes'],k):
        codes.extend((T^(1<<j))|(1<<r) for j in range(v))
    assert len(codes)==m and len(set(codes))==m
    W=2*max((len(row) for row in groups),default=0)+4
    D=8*(n+1);up=[];down=[]
    for i in range(n):
        g=[] if i<k else groups[i-k]
        base=2 if i<k else W+1-2*len(g)
        shift=[{'mask':s,'coefficient':2*D} for s in g]
        up.append([{'mask':0,'coefficient':base*D+i+1}]+shift)
        down.append([{'mask':0,'coefficient':(base-W)*D+i+1}]+shift)
    return {'kind':'explicit_polynomial','n':n,'scale':D,'low':0,'highs':[3*D],
            'up':up,'down':down,'codes':codes,'f':[0]*m,'resource_certificate':info,
            'uniform_span_scaled':W*D,'global_band_guarantee':True,
            'global_avalanche_free_guarantee':True}


def explicit_device(m:dict)->Device:
    if m.get('kind')!='explicit_polynomial':
        from independent import from_legacy
        return from_legacy(m)
    def T(i,s,u):
        return sum(t['coefficient'] for t in m['up' if u else 'down'][i]
                   if s&t['mask']==t['mask'])
    return Device(m['n'],m['low'],m['highs'],m['scale'],T,m['codes'],m['f'])


def dp_terms(q,k,e,d):
    """Independent dynamic-programming check of the closed coverage formula."""
    large=10**9;cost=[0]+[large]*q
    for _ in range(e):
        nxt=[large]*(q+1)
        for old in range(q+1):
            for count in range(min(k,q-old)+1):
                nxt[old+count]=min(nxt[old+count],cost[old]+(count+d-1)//d)
        cost=nxt
    return None if cost[q]>=large else cost[q]

if __name__=='__main__':
    import json,time
    from pathlib import Path
    from itertools import product
    from independent import from_legacy
    start=time.monotonic();cases=trials=0
    for n in range(1,13):
        for m in range(2,2+(n+1)**2//4):
            for d in range(1,n+1):
                z=reset_construct(m,n,d);r=verify_device(explicit_device(z))
                assert r['margin']*8>7*z['scale']
                assert sum(t['mask']!=0 for row in z['down'] for t in row)==z['resource_certificate']['terms']
                if n<=5:verify_device(explicit_device(z),full=True)
                cases+=1;trials+=r['trials']
    dp_count=0
    for k in range(1,9):
        for e in range(5):
            for d in range(1,10):
                for q in range(k*e+1):
                    assert required_terms(q,k,e,d)==dp_terms(q,k,e,d)
                    dp_count+=1
    independent_counts=[]
    for m in range(1,7):
        count=0
        for f in product(range(m),repeat=m):
            if independent_minimum(list(f)) is not None:
                verify_device(from_legacy(independent_machine(list(f))))
                count+=1
        independent_counts.append({'m':m,'idempotent_maps':count})
    report={'reset_frontier_constructions':cases,'reset_transitions':trials,
            'allocation_dp_comparisons':dp_count,'independent_maps':independent_counts,
            'reset37_n11':[reset_frontier(37,11,d) for d in range(1,7)],
            'reset37_minimum_source_incidence_count':reset_incidence_minimum(37,11),
            'reset35_pairwise':[reset_frontier(35,n,1) for n in range(11,35)],
            'seconds':time.monotonic()-start}
    R=Path(__file__).resolve().parents[1]/'results'
    (R/'resource_laws_verification.json').write_text(json.dumps(report,indent=2))
    for d in (1,2,3,6):
        (R/f'reset37_11bits_degree{d}.json').write_text(json.dumps(reset_construct(37,11,d),indent=2))
    print(json.dumps(report,indent=2))
