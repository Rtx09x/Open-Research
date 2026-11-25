"""New constraint-based search for injective unary encodings.

All prunings are necessities of the geometric characterization. No timeout is
interpreted as nonexistence. Coordinate normalization is used only because this
search allows arbitrary wiring and is invariant under coordinate permutations.
"""
from __future__ import annotations
from itertools import product
from math import comb
from collections import Counter
from independent import geometry

class SearchLimit(RuntimeError):pass


def isotype(f):
    """Exact canonical functional-digraph type, using rooted trees and cycles."""
    m=len(f);indeg=[0]*m;pred=[[] for _ in f]
    for x,t in enumerate(f):indeg[t]+=1;pred[t].append(x)
    queue=[i for i,d in enumerate(indeg) if d==0]
    for x in queue:
        indeg[f[x]]-=1
        if indeg[f[x]]==0:queue.append(f[x])
    cyclic={i for i,d in enumerate(indeg) if d}
    def tree(x):return '('+''.join(sorted(tree(y) for y in pred[x] if y not in cyclic))+')'
    used=set();components=[]
    for x in cyclic:
        if x in used:continue
        cycle=[];u=x
        while u not in used:used.add(u);cycle.append(tree(u));u=f[u]
        components.append(min(tuple(cycle[i:]+cycle[:i]) for i in range(len(cycle))))
    return tuple(sorted(components))


def encodings(f,n,limit=None):
    m=len(f)
    if n<0 or m>1<<n or any(t!=i and f[t]==i for i,t in enumerate(f)):return
    indeg=Counter(f);codes=[None]*m;steps=0
    domains=[]
    for i,t in enumerate(f):
        domain=[]
        for s in range(1<<n):
            k=s.bit_count()
            bound=1+k*(n-k+1) if i==t else k*(n-k-1)
            if indeg[i]>bound:continue
            if i!=t and f[t]!=t and k in (0,n):continue
            domain.append(s)
        if not domain:return
        domains.append(set(domain))
    # Choose a distinguished vertex before imposing coordinate symmetry.
    anchor=max(range(m),key=lambda i:(indeg[i],f[i]!=i,-i))
    domains[anchor]&={(1<<k)-1 for k in range(n+1)}
    edges=[(i,t) for i,t in enumerate(f) if i!=t]
    incoming=[[] for _ in f]
    for x,t in edges:incoming[t].append(x)
    def pair(A,T,t):
        ad=T&~A;rm=A&~T
        return ad.bit_count()==1 and rm.bit_count()<=1 and (bool(rm) or f[t]==t)
    def visit(current):
        nonlocal steps
        steps+=1
        if limit is not None and steps>limit:raise SearchLimit('node limit')
        assigned={s for s in codes if s is not None}
        peak={};forbidden=set()
        for i,t in edges:
            A,T=codes[i],codes[t]
            if A is None or T is None:continue
            if not pair(A,T,t):return
            P=A|T
            if A&~T:forbidden.add(P)
            if P in peak and peak[P]!=T:return
            peak[P]=T
        if assigned&forbidden:return
        if len(assigned)==m:
            assert geometry(codes,f,n)
            yield list(codes);return
        new=[]
        for i in range(m):
            if codes[i] is not None:new.append({codes[i]});continue
            d=current[i]-assigned-forbidden
            t=f[i]
            if i!=t and codes[t] is not None:d={s for s in d if pair(s,codes[t],t)}
            for x in incoming[i]:
                if codes[x] is not None:d={s for s in d if pair(codes[x],s,i)}
            if not d:return
            new.append(d)
        # Arc consistency on unassigned edges.
        changed=True
        while changed:
            changed=False
            for i,t in edges:
                a={s for s in new[i] if any(s!=v and pair(s,v,t) for v in new[t])}
                b={v for v in new[t] if any(s!=v and pair(s,v,t) for s in a)}
                if not a or not b:return
                if a!=new[i] or b!=new[t]:changed=True;new[i]=a;new[t]=b
        x=min((i for i in range(m) if codes[i] is None),key=lambda i:(len(new[i]),-indeg[i],-len(incoming[i])))
        for s in sorted(new[x]):
            codes[x]=s
            yield from visit(new)
        codes[x]=None
    yield from visit(domains)


def unrestricted_minimum(f,limit=None):
    if any(t!=i and f[t]==i for i,t in enumerate(f)):return {'minimum':None,'reason':'two-cycle'}
    for n in range((len(f)-1).bit_length(),len(f)+1):
        try:code=next(encodings(f,n,limit=limit),None)
        except SearchLimit:return {'minimum':None,'status':'unresolved','dimension_interrupted':n}
        if code is not None:return {'minimum':n,'codes':code,'status':'exact'}
    raise AssertionError('one-hot upper bound contradicted')


def minimize_degree(f,degree=1,common=False,uniform=False,nonnegative=False,limit=None):
    """Minimize over all encodings and fixed-state phases with checked LP witnesses.

    An unresolved LP or capped geometry search prevents an exact-minimum claim.
    Returns the full lower-dimension dual ledger (potentially large).
    """
    from synthesis import Problem,phase_options
    if any(t!=i and f[t]==i for i,t in enumerate(f)):
        return {'status':'impossible','reason':'two-cycle','minimum':None}
    if degree==0:
        from resources import independent_minimum,independent_machine
        n=independent_minimum(f)
        return {'status':'exact' if n is not None else 'impossible','minimum':n,
                'method':'interaction-free theorem','model':None if n is None else independent_machine(f)}
    rejected=[];unresolved=[];attempts=0
    for n in range((len(f)-1).bit_length(),len(f)+1):
        try:
            for codes in encodings(f,n,limit=limit):
                for phases in phase_options(codes,f,n):
                    cert=Problem(codes,f,n,min(degree,max(0,n-1)),common,uniform,nonnegative,phases).solve()
                    attempts+=1
                    if cert['status']=='feasible':
                        return {'status':'exact' if not unresolved else 'upper_bound_only','minimum':n if not unresolved else None,
                                'upper_bound':n,'witness':cert,'rejected':rejected,'unresolved':unresolved,'lp_attempts':attempts}
                    if cert['status']=='infeasible':rejected.append(cert)
                    else:unresolved.append(cert)
        except SearchLimit:
            unresolved.append({'dimension':n,'reason':'geometry node cap'})
            return {'status':'unresolved','minimum':None,'rejected':rejected,'unresolved':unresolved}
    raise AssertionError('pairwise unary upper bound contradicted')

if __name__=='__main__':
    import json,time
    from pathlib import Path
    start=time.monotonic();records=[]
    for m in range(1,7):
        types={}
        for f in product(range(m),repeat=m):types.setdefault(isotype(f),list(f))
        hist=Counter();noreal=0
        for f in types.values():
            info=unrestricted_minimum(f,limit=300000)
            records.append({'f':f,**info});hist[str(info.get('minimum'))]+=1
        print(m,len(types),dict(hist),flush=True)
    R=Path(__file__).resolve().parents[1]/'results'
    (R/'unary_types_through6.json').write_text(json.dumps({'records':records,'seconds':time.monotonic()-start},indent=2))
