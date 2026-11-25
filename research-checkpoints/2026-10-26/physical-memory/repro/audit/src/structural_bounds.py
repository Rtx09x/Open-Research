"""Graph-structural lower bounds and independent finite witness checks."""
from collections import Counter
from math import comb

def cohorts(f):
    parent=list(range(len(f)))
    def root(x):
        while parent[x]!=x:x=parent[x]
        return x
    for x,t in enumerate(f):
        if x!=t and f[t]!=t:parent[root(x)]=root(t)
    groups={}
    for x in range(len(f)):groups.setdefault(root(x),[]).append(x)
    return list(groups.values())

def weight_hall_bound(f,n):
    """Return a violated necessary cohort/Boolean-layer packing inequality."""
    indeg=Counter(f);groups=cohorts(f);allowed=[]
    for group in groups:
        weights=set(range(n+1))
        for x in group:
            weights &= {k for k in range(n+1) if indeg[x] <=
                        (1+k*(n-k+1) if f[x]==x else k*(n-k-1))}
        allowed.append(weights)
    # Exhaustive subsets make this a small-instance bound, not a claimed fast test.
    for mask in range(1,1<<len(groups)):
        selected=[j for j in range(len(groups)) if mask>>j&1]
        weights=set().union(*(allowed[j] for j in selected))
        demand=sum(len(groups[j]) for j in selected)
        supply=sum(comb(n,k) for k in weights)
        if demand>supply:return {'cohorts':[groups[j] for j in selected],
                                 'allowed_weights':sorted(weights),'demand':demand,'capacity':supply}
    return None

def nonnegative_onehot_bound(q):
    if q<3:raise ValueError('nontrivial allowed cycle required')
    return q*((q-1)//2)

if __name__=='__main__':
    import json
    from pathlib import Path
    from itertools import combinations
    checks=[]
    for vertices in range(1,13):
        edges=[{i,i+1} for i in range(vertices-1)]
        cost=next(k for k in range(vertices+1) if any(all(set(S)&e for e in edges)
                  for S in combinations(range(vertices),k)))
        assert cost==vertices//2;checks.append({'path_vertices':vertices,'cover':cost})
    f=[0,0,0,1,2];w=weight_hall_bound(f,3)
    assert w and w['demand']==4 and w['capacity']==3
    R=Path(__file__).resolve().parents[1]/'results'
    (R/'structural_bounds.json').write_text(json.dumps({'path_covers':checks,
        'packing_counterexample':{'f':f,'rejected_n':3,**w},
        'onehot_100_nonnegative_lower_bound':nonnegative_onehot_bound(100)},indent=2))
    print(w)
