"""Independent small-graph certificates; simple-path enumeration is TEST ONLY."""
import json
from pathlib import Path
import random
import sys
import time
from collections import Counter
import networkx as nx
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from exact_search import adaptive, nonadaptive, responses
from research.connected_extension.audit_connected import oracle
from research.connected_planner.connected_planner import Topology, plan, PlanningError, groups


def canonical(row): return sorted(sorted(x) for x in groups(row))


def verify_tree(t, tree, dictionary=None):
    depths = []
    def walk(node, candidates, depth):
        if 'fault_edge_index' in node:
            assert candidates == [node['fault_edge_index']]
            depths.append(depth); return
        q = tuple(node['query']); row = t.partition(q)
        bs = groups([row[e] for e in candidates])
        expected = sorted(sorted(candidates[i] for i in b) for b in bs)
        assert sorted(sorted(b['candidate_edge_indices']) for b in node['branches']) == expected
        for b in node['branches']:
            walk(b['next'], b['candidate_edge_indices'], depth+1)
    walk(tree, list(range(t.m)), 0)
    assert max(depths) == t.adaptive_count


def glue(graphs, chain=False):
    G = nx.Graph(); anchor = None
    for H in graphs:
        if not G:
            G = H.copy(); anchor = max(G); continue
        next_id = len(G); nodes = list(H); mapping = {nodes[0]: anchor}
        for v in nodes[1:]: mapping[v] = next_id; next_id += 1
        G.add_edges_from((mapping[u], mapping[v]) for u,v in H.edges())
        if chain: anchor = max(G)
    return G


def rejects(fn):
    try: fn()
    except PlanningError: return
    raise AssertionError('Expected PlanningError')


def main():
    started = time.time(); stats = Counter(); rng = random.Random(8102206)
    for G in nx.graph_atlas_g():
        if len(G) < 2 or not nx.is_connected(G): continue
        E = list(G.edges()); t = Topology(len(G), E)
        O = oracle(G, E, t.queries)
        assert all(canonical(a) == canonical(b) for a,b in zip(t.rows,O))
        a, _, _ = adaptive(O); assert a == t.adaptive_count
        verify_tree(t, t.tree()); stats['atlas_graphs'] += 1
        stats['independent_minimax_checks'] += 1
        if not t.bridges:
            count, _ = nonadaptive(O); assert count == len(t.fixed_queries)
            stats['independent_fixed_optima'] += 1
            S = [min(r) for r in t.demand_regions] if t.demand_regions else [0,1]
            restricted = Topology(len(G), E, accessible=S)
            assert restricted.adaptive_count == t.adaptive_count
            assert len(restricted.fixed_queries) == len(t.fixed_queries)
            verify_tree(restricted, restricted.tree()); stats['restricted_access_checks'] += 1
        if len(G) <= 5:
            result = plan(len(G), E, [rng.randrange(1, 10**9) for _ in E])
            assert result['optimal_adaptive_count'] == a
            Q, R = responses(len(G), E, resistances=list(map(__import__('fractions').Fraction, result['resistances'])))
            dictionary = dict(zip(Q,R))
            for e in range(len(E)):
                node = result['decision_tree']
                while 'query' in node:
                    response = str(dictionary[tuple(node['query'])][e])
                    matches = [b for b in node['branches'] if b['response'] == response]
                    assert len(matches) == 1 and e in matches[0]['candidate_edge_indices']
                    node = matches[0]['next']
                assert node['fault_edge_index'] == e
            stats['exact_weight_plans'] += 1
            stats['exact_response_entries'] += result['verified_dictionary_entries']
        if stats['atlas_graphs'] % 100 == 0: print(json.dumps(dict(stats)), flush=True)
    cases = {
        'triangle_chain_12': glue([nx.cycle_graph(3)]*12, True),
        'k4_bouquet_12': glue([nx.complete_graph(4)]*12),
        'mixed_chain': glue([nx.complete_graph(4),nx.cycle_graph(5),nx.diamond_graph(),nx.cycle_graph(4),nx.complete_graph(5)], True),
        'bridge_cycle_chain': glue([nx.path_graph(2),nx.cycle_graph(4),nx.path_graph(3),nx.complete_graph(4)], True),
        'path_17': nx.path_graph(18),
    }
    examples = []
    for name, G in cases.items():
        E = list(G.edges()); t = Topology(len(G), E); verify_tree(t,t.tree())
        if name == 'triangle_chain_12': assert t.adaptive_count == 2 and len(t.fixed_queries) == 7
        if name == 'k4_bouquet_12':
            assert t.adaptive_count == 6 and len(t.fixed_queries) == 6
            art = set(nx.articulation_points(G))
            assert all(not (set(r)&art) for r in t.demand_regions)
        if not t.bridges:
            S = [max(r) for r in t.demand_regions] if t.demand_regions else [0,1]
            restricted = Topology(len(G),E,S); verify_tree(restricted,restricted.tree())
            assert restricted.adaptive_count == t.adaptive_count
        if len(G) <= 18:
            result = plan(len(G),E,[rng.randrange(1,10**9) for _ in E])
            assert result['optimal_adaptive_count'] == t.adaptive_count
        print(json.dumps({'larger_case_passed':name}), flush=True)
        examples.append({'name':name,'n':len(G),'m':len(E),'pieces':t.p,'adaptive':t.adaptive_count,
                         'fixed':len(t.fixed_queries) if t.fixed_queries else None,'dp_states':t.dp_states})
    singleton = plan(2,[(0,1)],['7/3'], accessible=[])
    assert singleton['optimal_adaptive_count'] == singleton['optimal_fixed_count'] == 0
    treeplan = plan(4,[(0,1),(1,2),(2,3)],[2,3,5])
    assert treeplan['optimal_fixed_count'] is None and 'inf' in json.dumps(treeplan['decision_tree'])
    rejects(lambda: plan(4,[(0,1),(1,2),(2,3),(3,0)],[1,1,1,1]))
    rejects(lambda: plan(2,[(0,1)],[1.0]))
    rejects(lambda: plan(2,[(0,1)],[-1]))
    rejects(lambda: Topology(20,list(nx.path_graph(20).edges())))
    rejects(lambda: Topology(3,[(0,1),(1,2)],accessible=[0,2]))
    rejects(lambda: Topology(2,[(0,1)],accessible=[0,False]))
    rejects(lambda: Topology(2,[(0,1)],accessible=[0,0.0]))
    # Trivial local cactus leaf regions exclude the articulation itself.
    G=glue([nx.complete_graph(4)]*3); t=Topology(len(G),list(G.edges()))
    rejects(lambda: Topology(len(G),list(G.edges()),accessible=list(nx.articulation_points(G))))
    assert all(len(r)==3 for r in t.demand_regions)
    result={'status':'passed','seed':8102206,'counts':dict(stats),'larger_examples':examples,
            'seconds':time.time()-started,'networkx':nx.__version__,
            'oracle_note':'Original-simple-path enumeration is used only by the independent small-graph test oracle, never production preprocessing.'}
    Path(__file__).with_name('test_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__': main()
