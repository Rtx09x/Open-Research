"""Exact finite unary minimization for unrestricted threshold functions.

The search can be exponential. It is not a fixed-degree/pairwise optimizer.
An exhausted dimension certifies nonexistence; an interrupted run does not.
"""
from math import comb
from memory import validate_map,has_two_cycle,code_certificate


def capacity(n):
    return comb(n,(n-1)//2) if n>=1 else 1


def cycle_lengths(f):
    finished=set(); result=[]
    for v in range(len(f)):
        order={}; x=v
        while x not in finished and x not in order:
            order[x]=len(order); x=f[x]
        if x in order:result.append(len(order)-order[x])
        finished.update(order)
    return result


def partial_ok(c,f):
    peaks={}; descending=set(); chosen={a for a in c if a is not None}
    for i,j in enumerate(f):
        if i==j or c[i] is None or c[j] is None:continue
        A,T=c[i],c[j]; add,rem=T & ~A,A & ~T
        if add.bit_count()!=1 or rem.bit_count()>1:return False
        P=A|T
        if not rem and f[j]!=j:return False
        if rem:descending.add(P)
        if P in peaks and peaks[P]!=T:return False
        peaks[P]=T
    return not chosen & descending


def find_encoding(f,n):
    validate_map(f); m=len(f)
    if m>1<<n or has_two_cycle(f):return None,0
    if any(q>1 and q>capacity(n) for q in cycle_lengths(f)):return None,0
    for i in range(m):
        bound=1+(n+1)**2//4 if f[i]==i else (n-1)**2//4
        if f.count(i)>bound:return None,0
    c=[None]*m; nodes=0
    def visit(index,used):
        nonlocal nodes
        if index==m:
            code_certificate(c,f,n);return list(c)
        # Coordinate permutations put the first code in initial-segment form.
        candidates=[(1<<k)-1 for k in range(n+1)] if index==0 else range(1<<n)
        for x in candidates:
            if x in used:continue
            c[index]=x;nodes+=1
            if partial_ok(c,f):
                answer=visit(index+1,used|{x})
                if answer is not None:return answer
        c[index]=None
        return None
    return visit(0,set()),nodes


def minimize(f):
    validate_map(f)
    if has_two_cycle(f):return {'f':f,'minimum':None,'impossible':'contains a two-cycle'}
    if len(f)==1:return {'f':f,'minimum':0,'codes':[0],'exhausted':[]}
    exhausted=[]
    for n in range((len(f)-1).bit_length(),len(f)+1):
        codes,nodes=find_encoding(f,n)
        if codes is not None:
            return {'f':f,'minimum':n,'codes':codes,'exhausted':exhausted,
                    'search_nodes_at_witness':nodes}
        exhausted.append({'n':n,'search_nodes':nodes})
    raise AssertionError('Contradicts the one-hot existence theorem')
