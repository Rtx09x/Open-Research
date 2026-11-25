"""Independent certificate checker. Does NOT import exact_search or certify.

Electrical responses use the matrix-tree determinant ratio in SymPy, not
Gauss-Jordan inversion. Optimality uses supplied upper tree and lower DAG only.
"""
import json,sys
from fractions import Fraction

def electrical_matrix(n,edges,queries,resistances=None):
    import sympy as sp
    rows=[[] for _ in queries]
    for failed in range(len(edges)):
        adj=[set() for _ in range(n)]
        weights={}
        for i,(u,v) in enumerate(edges):
            if i!=failed:
                adj[u].add(v);adj[v].add(u)
                conductance = sp.Rational(1,resistances[i]) if resistances else sp.Integer(1)
                total = weights.get((u,v),sp.Integer(0)) + conductance
                weights[u,v] = weights[v,u] = total
        for k,(s,t) in enumerate(queries):
            comp={s};front=[s]
            while front:
                u=front.pop()
                for v in adj[u]-comp:comp.add(v);front.append(v)
            if t not in comp:rows[k].append('inf');continue
            vertices=sorted(comp);ix={v:i for i,v in enumerate(vertices)}
            lap=sp.zeros(len(vertices))
            for u in vertices:
                lap[ix[u],ix[u]]=sum(weights[u,v] for v in adj[u])
                for v in adj[u]:lap[ix[u],ix[v]]=-weights[u,v]
            one=[ix[v] for v in vertices if v!=s]
            two=[ix[v] for v in vertices if v not in (s,t)]
            den=lap.extract(one,one).det(method='domain-ge')
            num=lap.extract(two,two).det(method='domain-ge')
            rows[k].append(str(num/den))
    return rows

def check(data,electrical=True):
    if not __debug__:
        raise RuntimeError('Certificate verification requires assertions; do not run Python with -O.')
    matrix=data['matrix'];m=len(data['edges']);queries=data['queries'];visited=0
    fixed_lower=None
    assert type(data['adaptive_depth']) is int and data['adaptive_depth'] >= 0, 'adaptive depth must be a nonnegative integer'
    assert m >= 1 and len(matrix) == len(queries) and matrix
    assert all(len(row) == m for row in matrix), 'response dictionary shape mismatch'
    if electrical:assert electrical_matrix(data['n'],data['edges'],queries,data.get('resistances'))==matrix,'electrical response mismatch'
    for e in range(m):
        node=data['tree'];depth=0
        while 'query' in node:
            q=node['query'];assert 0<=q<len(queries)
            node=node['children'][matrix[q][e]];depth+=1
            assert depth<=data['adaptive_depth']
        assert node.get('edge')==e,('wrong leaf',e,node)
    if 'nonadaptive_queries' in data:
        selected=data['nonadaptive_queries']
        assert all(type(q) is int and 0 <= q < len(queries) for q in selected), 'invalid fixed query index'
        assert len({tuple(matrix[q][e] for q in selected) for e in range(m)})==m
        if 'nonadaptive_depth' in data:assert len(selected)==data['nonadaptive_depth']
    if 'nonadaptive_dual' in data:
        dual=data['nonadaptive_dual']
        for a,b,w in dual:
            assert type(a) is int and type(b) is int and 0 <= a < b < m, 'invalid dual fault pair'
            assert Fraction(w) >= 0, 'dual weights must be nonnegative'
        for row in matrix:
            assert sum(Fraction(w) for a,b,w in dual if row[a]!=row[b])<=1
        total=sum(Fraction(w) for a,b,w in dual)
        fixed_lower=(total.numerator+total.denominator-1)//total.denominator
        assert fixed_lower==data.get('nonadaptive_lower',data.get('nonadaptive_depth'))
    if 'theta_lower' in data:
        paths=data['theta_lower']['paths']; k=data['adaptive_depth']-1
        assert paths and k >= 1
        for path in paths:
            assert path and len(set(path)) == len(path), 'lower-bound subsets must contain distinct faults'
            assert all(type(e) is int and 0 <= e < m for e in path), 'invalid lower-bound fault index'
        assert all(max(len({row[e] for e in path}) for row in matrix)<=2 for path in paths)
        for row in matrix:
            assert any(len(path)>2**(k-1) and len({row[e] for e in path})==1 for path in paths)
        return {'file_family':data['family'],'sizes':data['sizes'],'depth':data['adaptive_depth'],
                'electrical_entries':len(matrix)*m if electrical else 0,'fault_paths_checked':m,
                'theta_lower_queries_checked':len(matrix),'static_lower':fixed_lower}
    cert=data['lower_certificate'];arity=max(len(set(r)) for r in matrix)
    assert cert['arity']==arity
    seen=set()
    def lower(key):
        nonlocal visited
        if key in seen:return
        node=cert['nodes'][key];S=set(node['candidates']);b=node['budget']
        assert len(S)>1 and b>=0
        if node['reason']=='zero_budget':assert b==0
        elif node['reason']=='capacity':assert len(S)>arity**b
        else:
            assert node['reason']=='all_queries' and b>0
            assert len(node['hard_children'])==len(matrix)
            for q,child in enumerate(node['hard_children']):
                cn=cert['nodes'][child];T=set(cn['candidates'])
                assert cn['budget']==b-1 and T and T<=S
                val=matrix[q][next(iter(T))]
                assert T=={e for e in S if matrix[q][e]==val}
                lower(child)
        seen.add(key);visited+=1
    root=cert['nodes'][cert['root']]
    assert set(root['candidates'])==set(range(m)) and root['budget']==data['adaptive_depth']-1
    lower(cert['root'])
    return {'file_family':data['family'],'sizes':data['sizes'],'depth':data['adaptive_depth'],'electrical_entries':len(matrix)*m if electrical else 0,'fault_paths_checked':m,'lower_nodes_checked':visited,'static_lower':fixed_lower,'static_upper':len(data['nonadaptive_queries']) if 'nonadaptive_queries' in data else None}

if __name__=='__main__':
    args=sys.argv[1:];electrical='--certificate-only' not in args
    for p in [a for a in args if a!='--certificate-only']:
        with open(p) as f: data=json.load(f)
        print(json.dumps(check(data,electrical=electrical)),flush=True)
