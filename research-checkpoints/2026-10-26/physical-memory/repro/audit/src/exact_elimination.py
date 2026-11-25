"""Standard-library exact Fourier--Motzkin oracle with proof provenance.

This is an established elimination algorithm, not a novelty claim. Without a
row cap it is a finite complete oracle; its worst-case resource growth can be
severe. With a cap, exhaustion is reported as unresolved. Primal and Farkas dual
outputs are checked against the original synthesis problem before acceptance.
"""
from fractions import Fraction as F
from math import gcd
from functools import reduce


def solve_exact(problem,max_rows=20000):
    D=problem.dimension
    rows=[]
    for i,(a,b) in enumerate(zip(problem.rows,problem.bounds)):
        rows.append((tuple(a.get(j,0) for j in range(D)),b,{i:F(1)}))
    history=[];variables=set(range(D));largest=len(rows)
    base={'spec':problem.spec,'fingerprint':problem.fingerprint,'variables':problem.variables,
          'rows':len(problem.rows),'dimension':D,'solver':'exact Fourier-Motzkin'}
    def simplify(raw):
        seen={}
        for a,b,y in raw:
            if not any(a):
                if b>0:return None,y
                continue
            divisor=reduce(gcd,[abs(x) for x in a]+[abs(b)]) or 1
            if divisor>1:
                a=tuple(v//divisor for v in a);b//=divisor;y={i:v/divisor for i,v in y.items()}
            if a not in seen or seen[a][1]<b:seen[a]=(a,b,y)
        return list(seen.values()),None
    def impossible(y):
        vector=[y.get(i,F(0)) for i in range(len(problem.rows))]
        assert problem.dual_ok(vector)
        return {**base,'status':'infeasible','dual':{str(i):str(v) for i,v in y.items() if v},
                'largest_intermediate_rows':largest}
    while variables:
        rows,bad=simplify(rows)
        if bad is not None:return impossible(bad)
        v=min(variables,key=lambda j:sum(a[j]>0 for a,_,_ in rows)*sum(a[j]<0 for a,_,_ in rows))
        positive=[r for r in rows if r[0][v]>0];negative=[r for r in rows if r[0][v]<0]
        zero=[r for r in rows if not r[0][v]]
        estimate=len(zero)+len(positive)*len(negative)
        if max_rows is not None and estimate>max_rows:
            return {**base,'status':'unresolved','reason':'exact elimination row cap',
                    'projected_rows':estimate,'largest_intermediate_rows':largest}
        history.append((v,rows));variables.remove(v);new=list(zero)
        for ap,bp,yp in positive:
            for an,bn,yn in negative:
                p=ap[v];q=-an[v]
                a=tuple(q*x+p*y for x,y in zip(ap,an));b=q*bp+p*bn
                y={i:q*z for i,z in yp.items()}
                for i,z in yn.items():y[i]=y.get(i,F(0))+p*z
                new.append((a,b,y))
        rows=new;largest=max(largest,len(rows))
    rows,bad=simplify(rows)
    if bad is not None:return impossible(bad)
    x=[F(0)]*D
    for v,old in reversed(history):
        low=high=None
        for a,b,_ in old:
            if not a[v]:continue
            bound=(F(b)-sum(F(c)*x[j] for j,c in enumerate(a) if j!=v))/a[v]
            if a[v]>0:low=bound if low is None else max(low,bound)
            else:high=bound if high is None else min(high,bound)
        assert low is None or high is None or low<=high
        x[v]=low if low is not None and low>0 else (high if high is not None and high<0 else F(0))
    assert problem.primal_ok(x)
    return {**base,'status':'feasible','primal':list(map(str,x)),
            'largest_intermediate_rows':largest}

if __name__=='__main__':
    from synthesis import Problem,verify_certificate
    from pathlib import Path
    import json
    cases=[Problem([1,2,4],[1,2,0],3,0),Problem([1,0],[0,0],1,0),
           Problem([1,0,3,2],[0,0,2,2],2,0),Problem([1,0,2],[0,0,0],2,1)]
    results=[]
    for p in cases:
        c=solve_exact(p,max_rows=50000);verify_certificate(c);results.append(c)
        print(p.spec['n'],p.spec['degree'],c['status'],c['largest_intermediate_rows'])
    (Path(__file__).resolve().parents[1]/'results'/'exact_oracle_smoke.json').write_text(json.dumps(results,indent=2))
