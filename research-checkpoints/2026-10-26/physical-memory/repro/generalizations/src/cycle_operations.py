"""Exact combinatorial cycle operations; no numerical solver is needed.

An alternating path lists low, high, low, high, ... masks and closes to its
first low vertex. Every operation validates both its inputs and its output.
"""
from __future__ import annotations
from memory import require, layer_compile


def validate_cycle(n: int, path: list[int]) -> tuple[int,int]:
    require(type(n) is int and n>=3, 'Invalid dimension')
    require(len(path)>=6 and len(path)%2==0, 'Need a nontrivial alternating cycle')
    require(all(type(s) is int and 0<=s<1<<n for s in path), 'Invalid cycle mask')
    require(len(set(path))==len(path), 'Repeated vertex')
    k=path[0].bit_count()
    require(1<=k<=n-2, 'Invalid adjacent layers')
    require(all(s.bit_count()==k+t%2 for t,s in enumerate(path)), 'Ranks do not alternate')
    require(all((path[t]^path[(t+1)%len(path)]).bit_count()==1 for t in range(len(path))),
            'A path step is not a cube edge')
    return k,len(path)//2


def from_codes(n: int, codes: list[int]) -> list[int]:
    path=[]
    for t,a in enumerate(codes):
        b=codes[(t+1)%len(codes)]
        path.extend([a,a|b])
    validate_cycle(n,path)
    return path


def one_hot_cycle(q: int) -> list[int]:
    return from_codes(q,[1<<i for i in range(q)])


def complement(n: int, path: list[int]) -> list[int]:
    validate_cycle(n,path)
    c=[((1<<n)-1)^s for s in path]
    result=c[1:]+c[:1]
    validate_cycle(n,result)
    return result


def embed(n: int, path: list[int], on: int=0, off: int=0) -> tuple[int,list[int]]:
    validate_cycle(n,path)
    require(on>=0 and off>=0,'Negative number of fixed bits')
    result=[s|(((1<<on)-1)<<n) for s in path]
    dimension=n+on+off
    validate_cycle(dimension,result)
    return dimension,result


def join(n: int, upper: list[int], lower: list[int]) -> list[int]:
    """Join B(n,k) and B(n,k-1), yielding period q_upper+q_lower-1 on n+1 bits."""
    k,qu=validate_cycle(n,upper); ell,ql=validate_cycle(n,lower)
    require(ell==k-1,'The two cycles have incompatible layers')
    a,b=upper[0],upper[2]
    u,v=lower[1],lower[-1]
    def indices(mask):return [i for i in range(n) if mask>>i&1]
    source_groups=[indices(u&v),indices(u&~v),indices(v&~u),indices(((1<<n)-1)&~(u|v))]
    target_groups=[indices(a&b),indices(a&~b),indices(b&~a),indices(((1<<n)-1)&~(a|b))]
    permutation={}
    for src,dst in zip(source_groups,target_groups):
        require(len(src)==len(dst),'Wedges are not isomorphic')
        permutation.update(zip(src,dst))
    def permute(s):return sum(1<<permutation[i] for i in range(n) if s>>i&1)
    require(permute(u)==a and permute(v)==b,'Permutation endpoint mismatch')
    result=upper[2:]+upper[:1]+[permute(s)|(1<<n) for s in lower[1:]]
    rk,q=validate_cycle(n+1,result)
    require(rk==k and q==qu+ql-1,'Joining cardinality mismatch')
    return result


def lift(n: int, path: list[int], q: int) -> list[int]:
    """Realize any period 3..2Q+1 on n+2 bits from a Q-cycle on n bits."""
    k,Q=validate_cycle(n,path)
    require(type(q) is int and 3<=q<=2*Q+1,'Requested lifted period is outside the theorem')
    t=q//2; lows=path[::2];x=1<<n;y=1<<(n+1)
    codes=[a|x for a in lows[:t]]+[a|y for a in reversed(lows[:t])]
    if q%2:codes.append(path[-1])
    result=from_codes(n+2,codes)
    rk,actual=validate_cycle(n+2,result)
    require(rk==k+1 and actual==q,'Lift cardinality mismatch')
    return result


def model(n: int, path: list[int], saturating: bool=True, global_bands: bool=True) -> dict:
    _,q=validate_cycle(n,path)
    return layer_compile(path[::2],list(range(1,q))+[0],n,saturating,global_bands)
