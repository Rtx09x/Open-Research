"""Reproducible independent tests. Run with NetworkX installed."""
from itertools import combinations
import json
import random
import time
from pathlib import Path
import networkx as nx
from planner import Topology, PlanningError, plan
from exact_search import adaptive, nonadaptive

rng = random.Random(20261008)
stats = {'atlas_graphs': 0, 'exact_optimizer_comparisons': 0, 'restricted_sets': 0, 'rational_graphs': 0, 'cactus_lifts': 0, 'cubic_gadgets': 0, 'prisms': 0, 'cycles': 0}
start = time.time()


def depth(tree):
    if 'fault_edge_index' in tree: return 0
    return 1 + max(depth(x['next']) for x in tree['branches'])


def check(t):
    assert depth(t.tree()) == t.adaptive_count
    # Independent cut-pair equivalence, not cycle projection.
    for q, row in zip(t.queries, t.rows):
        for a, b in combinations(range(t.m), 2):
            S = t.cuts.get((a,b))
            expected = S is not None and ((q[0] in S) == (q[1] in S))
            assert (row[a] == row[b]) == expected
    # Circular shore interval certificate and direct augmentation certificate.
    for S in t.cuts.values():
        bits = [bool(set(t.blobs[b]) & S) for b in t.leaf_order]
        assert any(bits) and not all(bits)
        assert sum(bits[i] != bits[(i+1)%len(bits)] for i in range(len(bits))) == 2
        assert any((u in S) != (v in S) for u,v in t.fixed_queries)


for G in nx.graph_atlas_g():
    if len(G) < 3 or not nx.is_biconnected(G): continue
    n = len(G); E = list(G.edges()); t = Topology(n,E); check(t)
    a, _, _ = adaptive(t.rows); f, _ = nonadaptive(t.rows)
    assert a == t.adaptive_count and f == len(t.fixed_queries)
    stats['exact_optimizer_comparisons'] += 1
    B = [min(t.blobs[b]) for b in t.leaves] if t.leaves else [0,1]
    restricted = Topology(n,E,B); check(restricted)
    assert restricted.kappa == t.kappa and len(restricted.fixed_queries) == f
    stats['restricted_sets'] += 1
    if n <= 6:
        weights = [str(rng.randrange(1,10**7)) for _ in E]
        result = plan(n,E,weights,B)
        assert depth(result['decision_tree']) == a
        stats['rational_graphs'] += 1
    stats['atlas_graphs'] += 1


def lift(C):
    G = nx.Graph(); ports = {}; k = 0
    for v in C:
        incident = list(C.edges(v, keys=True)); d = len(incident)
        if d == 2:
            nodes = [k]; k += 1; G.add_node(nodes[0])
        else:
            nodes = list(range(k,k+d)); k += d; G.add_edges_from(combinations(nodes,2))
        for i,(a,b,key) in enumerate(incident): ports[v,key] = nodes[0] if d == 2 else nodes[i]
    for u,v,key in C.edges(keys=True): G.add_edge(ports[u,key],ports[v,key])
    assert nx.is_biconnected(G)
    return G


for n in range(3, 16):
    G = nx.cycle_graph(n); check(Topology(n,list(G.edges())))
    stats['cycles'] += 1

for trial in range(15):
    C = nx.MultiGraph(); C.add_node(0); v = 1; edge = 0
    for block in range(1 + trial % 5):
        root = rng.choice(list(C)); size = rng.randrange(2,6)
        cyc = [root] + list(range(v,v+size-1)); v += size-1
        for i in range(size):
            C.add_edge(cyc[i],cyc[(i+1)%size],key=edge); edge += 1
    G = lift(C); E = list(G.edges()); t = Topology(len(G),E); check(t)
    assert len(t.leaves) == sum(d == 2 for _,d in C.degree())
    stats['cactus_lifts'] += 1

for k in [3,4,5,8]:
    H = nx.circular_ladder_graph(k); check(Topology(len(H),list(H.edges())))
    stats['prisms'] += 1
    G = nx.Graph(); G.add_nodes_from(H); v = len(H)
    for u,w in H.edges():
        a,b,c,d = range(v,v+4); v += 4
        G.add_edges_from([(a,c),(a,d),(b,c),(b,d),(c,d),(u,a),(b,w)])
    t = Topology(len(G),list(G.edges())); check(t)
    assert t.adaptive_count == 2 and len(t.fixed_queries) == (3*k+1)//2
    stats['cubic_gadgets'] += 1

for bad in [dict(n=4,edges=list(nx.cycle_graph(4).edges()),resistances=[1]*4),
            dict(n=3,edges=list(nx.path_graph(3).edges()),resistances=[1]*2),
            dict(n=3,edges=list(nx.cycle_graph(3).edges()),resistances=[1.0]*3),
            dict(n=3,edges=list(nx.cycle_graph(3).edges()),resistances=[-1,2,3]),
            dict(n=4,edges=list(nx.cycle_graph(4).edges()),resistances=[1,2,4,8],accessible=[0,1])]:
    try: plan(**bad)
    except PlanningError: pass
    else: raise AssertionError('Expected rejection: ' + str(bad))

example = dict(n=5,edges=list(nx.cycle_graph(5).edges()),resistances=['2/3','3/4','5/7','11/13','17/19'])
Path(__file__).with_name('example_cycle.json').write_text(json.dumps(example,indent=2)+'\n')
Path(__file__).with_name('example_plan.json').write_text(json.dumps(plan(**example),indent=2)+'\n')
stats['seconds'] = time.time()-start
Path(__file__).with_name('test_results.json').write_text(json.dumps(stats,indent=2)+'\n')
print(json.dumps(stats,indent=2))
