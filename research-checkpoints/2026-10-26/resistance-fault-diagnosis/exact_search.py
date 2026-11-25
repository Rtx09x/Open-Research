"""Exact research calculations for one open-circuit edge; Python standard library.

All vertex pairs are permitted unless an explicit query list is passed.
Response matrices are exact rationals. Decision trees minimize worst-case depth.
No floating point tolerances, sampling, or model calls are used.
"""
from fractions import Fraction as F
from itertools import combinations
from functools import lru_cache
import json, time
from math import inf

def inverse(a):
    n=len(a)
    x=[[F(v) for v in row]+[F(i==j) for j in range(n)] for i,row in enumerate(a)]
    for k in range(n):
        pivot=next(i for i in range(k,n) if x[i][k])
        x[k],x[pivot]=x[pivot],x[k]
        v=x[k][k]; x[k]=[z/v for z in x[k]]
        for i in range(n):
            if i!=k:
                v=x[i][k]
                if v: x[i]=[z-v*w for z,w in zip(x[i],x[k])]
    return [row[n:] for row in x]

def responses(n, edges, queries=None, resistances=None):
    edges=[tuple(e) for e in edges]
    conductances=[F(1,r) for r in resistances] if resistances is not None else [F(1)]*len(edges)
    queries=list(combinations(range(n),2)) if queries is None else list(queries)
    matrix=[[] for q in queries]
    for failed in range(len(edges)):
        adj=[set() for _ in range(n)]
        weighted={}
        for i,(u,v) in enumerate(edges):
            if i!=failed:
                adj[u].add(v); adj[v].add(u)
                total = weighted.get((u,v), F(0)) + conductances[i]
                weighted[u,v] = weighted[v,u] = total
        components=[]; seen=set()
        for u in range(n):
            if u in seen: continue
            comp=[]; todo=[u]; seen.add(u)
            while todo:
                v=todo.pop(); comp.append(v)
                for w in adj[v]:
                    if w not in seen: seen.add(w); todo.append(w)
            components.append(comp)
        comp_id={v:i for i,c in enumerate(components) for v in c}
        invs={}; maps={}
        for i,comp in enumerate(components):
            ix={v:j for j,v in enumerate(comp)}; maps[i]=ix
            lap=[[0]*(len(comp)-1) for _ in comp[:-1]]
            for v in comp[:-1]:
                j=ix[v]; lap[j][j]=sum(weighted[v,w] for w in adj[v])
                for w in adj[v]:
                    if ix[w]<len(comp)-1: lap[j][ix[w]]-=weighted[v,w]
            invs[i]=inverse(lap)
        for k,(u,v) in enumerate(queries):
            if comp_id[u]!=comp_id[v]: value='inf'
            else:
                c=comp_id[u]; ix=maps[c]; inv=invs[c]
                def entry(a,b):
                    return inv[ix[a]][ix[b]] if ix[a]<len(inv) and ix[b]<len(inv) else F(0)
                value=entry(u,u)+entry(v,v)-2*entry(u,v)
            matrix[k].append(value)
    return queries,matrix

def partitions(matrix):
    result=[]
    for row in matrix:
        groups={}
        for i,value in enumerate(row): groups[value]=groups.get(value,0)|(1<<i)
        result.append(tuple(groups.values()))
    return result

def adaptive(matrix, hypothesis_count=None):
    """Return exact minimax depth, certificate, and memoized-state count.

    Depth is None when the available queries cannot identify every hypothesis.
    Empty query families require an explicit positive hypothesis_count.
    """
    m = _hypothesis_count(matrix, hypothesis_count)
    parts=partitions(matrix); choices={}
    @lru_cache(None)
    def depth(s):
        if s.bit_count()<=1: return 0
        best=inf; bestq=None
        candidates=[]; distinct=set()
        for q,p in enumerate(parts):
            blocks=tuple(sorted(x&s for x in p if x&s))
            if len(blocks)<2 or blocks in distinct: continue
            distinct.add(blocks)
            candidates.append((max(x.bit_count() for x in blocks),q,blocks))
        for _,q,blocks in sorted(candidates):
            worst=0
            for x in sorted(blocks,key=int.bit_count,reverse=True):
                worst=max(worst,depth(x))
                if 1+worst>=best: break
            if 1+worst<best: best=1+worst; bestq=q
        choices[s]=bestq
        return best
    initial=(1<<m)-1; d=depth(initial)
    def certificate(s):
        if s.bit_count()<=1: return {'edge':s.bit_length()-1}
        q=choices[s]
        if q is None:
            # Supply a real pair/class with identical complete response columns,
            # not the whole state (which may also contain distinguishable faults).
            columns = {}
            for e in range(m):
                if s >> e & 1:
                    key = tuple(row[e] for row in matrix)
                    columns[key] = columns.get(key, 0) | (1 << e)
            witness = next(mask for mask in columns.values() if mask.bit_count() > 1)
            return {'unidentifiable_state': s, 'indistinguishable': witness}
        children={}
        for i in range(m):
            if s>>i&1:
                value=str(matrix[q][i]); children[value]=children.get(value,0)|(1<<i)
        return {'query':q,'children':{v:certificate(t) for v,t in children.items()}}
    return (None if d == inf else d),certificate(initial),depth.cache_info().currsize

def _hypothesis_count(matrix, hypothesis_count):
    if hypothesis_count is None:
        if not matrix:
            raise ValueError('Empty query families require hypothesis_count.')
        hypothesis_count = len(matrix[0])
    if type(hypothesis_count) is not int or hypothesis_count < 1:
        raise ValueError('Require a positive integer hypothesis_count.')
    if any(len(row) != hypothesis_count for row in matrix):
        raise ValueError('Response rows must match hypothesis_count.')
    return hypothesis_count


def nonadaptive(matrix, hypothesis_count=None):
    """Return (None, None) if no identifying fixed family exists."""
    m=_hypothesis_count(matrix, hypothesis_count); pairs=list(combinations(range(m),2)); full=(1<<len(pairs))-1
    covers=[sum(1<<i for i,(a,b) in enumerate(pairs) if row[a]!=row[b]) for row in matrix]
    for k in range(len(matrix)+1):
        for subset in combinations(range(len(matrix)),k):
            union=0
            for q in subset: union|=covers[q]
            if union==full: return k,subset
    return None,None

def complete(n): return list(combinations(range(n),2))
def bipartite(a,b): return [(u,a+v) for u in range(a) for v in range(b)]

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(); p.add_argument('family',choices=['complete','bipartite']);p.add_argument('sizes',nargs='+',type=int);p.add_argument('--fixed',action='store_true');p.add_argument('--out')
    args=p.parse_args(); n=sum(args.sizes) if args.family=='bipartite' else args.sizes[0]
    edges=bipartite(*args.sizes) if args.family=='bipartite' else complete(n)
    start=time.time(); queries,matrix=responses(n,edges)
    d,tree,states=adaptive(matrix)
    result={'family':args.family,'sizes':args.sizes,'n':n,'edges':edges,'queries':queries,'matrix':[[str(x) for x in row] for row in matrix],'adaptive_depth':d,'tree':tree,'states':states,'seconds':time.time()-start}
    if args.fixed: result['nonadaptive_depth'],result['nonadaptive_queries']=nonadaptive(matrix)
    if args.out:
        with open(args.out,'w') as f: json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k not in ['matrix','tree','edges','queries']}),flush=True)
