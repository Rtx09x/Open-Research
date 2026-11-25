"""Exact generic single-edge-deletion planner for simple biconnected graphs.

Resistances, not conductances, are the input weights. No numerical tolerances.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path
import sys
import networkx as nx
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from exact_search import responses


class PlanningError(ValueError):
    pass


def groups(labels):
    out = defaultdict(list)
    for e, label in enumerate(labels):
        out[label].append(e)
    return list(out.values())


class Topology:
    def __init__(self, n, edges, accessible=None):
        self.n = n
        self.edges = [tuple(e) for e in edges]
        self.m = len(edges)
        if n < 3 or any(len(e) != 2 or any(type(v) is not int or not 0 <= v < n for v in e) or e[0] == e[1] for e in self.edges):
            raise PlanningError('Require at least three vertices labeled 0,...,n-1 and loopless edges.')
        self.G = nx.Graph()
        self.G.add_nodes_from(range(n)); self.G.add_edges_from(self.edges)
        if self.G.number_of_edges() != self.m or not nx.is_biconnected(self.G):
            raise PlanningError('Require a simple vertex-biconnected graph.')
        self.B = list(range(n)) if accessible is None else sorted(set(accessible))
        if any(type(v) is not int or not 0 <= v < n for v in self.B):
            raise PlanningError('Invalid accessible vertex.')
        self.cuts = {}
        edge_dsu = nx.utils.UnionFind(range(self.m))
        for a, b in combinations(range(self.m), 2):
            H = self.G.copy(); H.remove_edges_from([self.edges[a], self.edges[b]])
            comps = list(nx.connected_components(H))
            if len(comps) > 1:
                assert len(comps) == 2
                self.cuts[a, b] = frozenset(comps[0]); edge_dsu.union(a, b)
        self.classes = groups([edge_dsu[e] for e in range(self.m)])
        # Vertices are in the same 3-edge-connected blob iff no two-cut separates them.
        signatures = {v: tuple(v in S for S in self.cuts.values()) for v in range(n)}
        sig_ids = {}; self.blob = {}
        for v in range(n):
            self.blob[v] = sig_ids.setdefault(signatures[v], len(sig_ids))
        self.blobs = groups([self.blob[v] for v in range(n)])
        self.cactus = nx.MultiGraph(); self.cactus.add_nodes_from(range(len(self.blobs)))
        for e, (u, v) in enumerate(self.edges):
            a, b = self.blob[u], self.blob[v]
            if a != b: self.cactus.add_edge(a, b, key=e)
        self.leaves = [v for v, d in self.cactus.degree() if d == 2]
        if len(self.blobs) > 1:
            missing = [b for b in self.leaves if not set(self.blobs[b]) & set(self.B)]
            if missing: raise PlanningError('Accessible set is not identifying; missing degree-two blobs: ' + str([self.blobs[b] for b in missing]))
        elif len(self.B) < 2:
            raise PlanningError('Accessible set must contain two distinct vertices.')
        self.cycles = []
        for C in self.classes:
            if len(C) == 1: continue
            H = self.G.copy(); H.remove_edges_from(self.edges[e] for e in C)
            comps = list(nx.connected_components(H)); comp = {v: i for i, S in enumerate(comps) for v in S}
            adj = defaultdict(list)
            for e in C:
                u, v = self.edges[e]; a, b = comp[u], comp[v]
                adj[a].append((e, b)); adj[b].append((e, a))
            current = comp[self.edges[C[0]][0]]; start = current; used = set(); order = []; nodes = []
            while len(used) < len(C):
                nodes.append(current)
                e, nxt = next((e, x) for e, x in sorted(adj[current]) if e not in used)
                order.append(e); used.add(e); current = nxt
            assert current == start
            pos = {c: i for i, c in enumerate(nodes)}
            self.cycles.append({'edges': order, 'positions': {v: pos[comp[v]] for v in range(n)}})
        self.queries = list(combinations(self.B, 2))
        scores = [self.imbalance(q) for q in self.queries]
        self.kappa = min(scores)
        self.first = scores.index(self.kappa)
        self.rows = [self.partition(q) for q in self.queries]
        self.adaptive_count = 1 + (self.kappa - 1).bit_length()
        self.fixed_queries = self._fixed()
        assert len(self.fixed_queries) == max(1, (len(self.leaves) + 1) // 2)
        assert all(any((u in S) != (v in S) for u, v in self.fixed_queries) for S in self.cuts.values())

    def imbalance(self, query):
        """Largest first-response block in O(number of nonsingleton classes)."""
        s, t = query; worst = 1
        for cyc in self.cycles:
            k = len(cyc['edges'])
            a = (cyc['positions'][t] - cyc['positions'][s]) % k
            worst = max(worst, a, k-a)
        return worst

    def partition(self, query):
        s, t = query; labels = list(range(self.m))
        for cyc in self.cycles:
            order = cyc['edges']; k = len(order); a = cyc['positions'][s]; b = cyc['positions'][t]
            arc = [order[(a + j) % k] for j in range((b - a) % k)]
            arc_set = set(arc)
            other = [e for e in order if e not in arc_set]
            for block in (arc, other):
                if block:
                    representative = min(block)
                    for e in block: labels[e] = representative
        return labels

    def _fixed(self):
        if len(self.blobs) == 1:
            self.leaf_order = []; return [tuple(self.B[:2])]
        # Cycle-node incidence tree, respecting each cycle's circular order.
        cycles = []; incident = defaultdict(list)
        for c in self.cycles:
            e0 = c['edges'][0]; a, b = self.edges[e0]; current = self.blob[a]; order = []
            for e in c['edges']:
                order.append(current); u, v = self.edges[e]; x, y = self.blob[u], self.blob[v]
                current = y if current == x else x
            ci = len(cycles); cycles.append(order)
            for v in order: incident[v].append(ci)
        order = []
        def visit(v, parent_cycle=None):
            if v in self.leaves: order.append(v)
            for ci in incident[v]:
                if ci == parent_cycle: continue
                cyc = cycles[ci]; i = cyc.index(v)
                for j in range(1, len(cyc)): visit(cyc[(i+j) % len(cyc)], ci)
        visit(0)
        assert sorted(order) == sorted(self.leaves)
        self.leaf_order = order[:]
        if len(order) % 2: order.insert(1, order[0])
        half = len(order) // 2
        reps = {b: min(set(self.blobs[b]) & set(self.B)) for b in self.leaves}
        result = [tuple(sorted((reps[order[i]], reps[order[i+half]]))) for i in range(half)]
        assert all(u != v for u, v in result) and len(set(result)) == len(result)
        return result

    def tree(self, dictionary=None):
        """Balanced structural refinement, no exponential minimax recurrence."""
        def build(state, first=False):
            if len(state) == 1: return {'fault_edge_index': state[0]}
            def blocks(i):
                out = defaultdict(list)
                for e in state: out[self.rows[i][e]].append(e)
                return list(out.values())
            i = self.first if first else min(range(len(self.queries)), key=lambda j: max(map(len, blocks(j))))
            bs = blocks(i)
            assert len(bs) > 1
            if not first: assert max(map(len, bs)) <= (len(state)+1)//2
            children = []
            for S in bs:
                branch = {'candidate_edge_indices': S, 'next': build(S)}
                if dictionary is not None: branch['response'] = str(dictionary[self.queries[i]][S[0]])
                children.append(branch)
            return {'query': list(self.queries[i]), 'branches': children}
        return build(list(range(self.m)), True)


def plan(n, edges, resistances, accessible=None):
    topology = Topology(n, edges, accessible)
    if len(resistances) != len(edges) or any(isinstance(r, (float, bool)) for r in resistances):
        raise PlanningError('Supply one exact integer or rational string resistance per edge; floats are rejected.')
    try: weights = [Fraction(r) for r in resistances]
    except (ValueError, ZeroDivisionError, TypeError) as exc: raise PlanningError('Invalid rational resistance.') from exc
    if any(r <= 0 for r in weights): raise PlanningError('All resistances must be positive.')
    # Check ALL vertex queries, even with restricted access, to certify the global generic theorem.
    Q, matrix = responses(n, edges, resistances=weights)
    for q, row in zip(Q, matrix):
        predicted = topology.partition(q)
        actual_blocks = sorted(sorted(S) for S in groups(row))
        predicted_blocks = sorted(sorted(S) for S in groups(predicted))
        if actual_blocks != predicted_blocks:
            raise PlanningError('Nongeneric input: exact electrical and structural partitions differ at query ' + str(q))
    dictionary = dict(zip(Q, matrix))
    fixed = topology.fixed_queries
    vectors = [tuple(dictionary[q][e] for q in fixed) for e in range(len(edges))]
    assert len(set(vectors)) == len(edges)
    return {'model': 'one complete edge deletion; exact known positive rational resistances',
            'genericity_verified': True, 'n': n, 'edges': edges,
            'resistances': list(map(str, weights)), 'accessible': topology.B,
            'series_classes': topology.classes, 'blobs': topology.blobs,
            'cactus_leaf_order': topology.leaf_order, 'kappa': topology.kappa,
            'optimal_adaptive_count': topology.adaptive_count,
            'optimal_first_query': topology.queries[topology.first],
            'decision_tree': topology.tree(dictionary),
            'optimal_fixed_count': len(fixed), 'fixed_queries': fixed,
            'fixed_response_dictionary': [{'fault_edge_index': e, 'responses': list(map(str, vectors[e]))} for e in range(len(edges))],
            'verified_dictionary_entries': len(Q)*len(edges)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', help='JSON: n, edges, resistances, optional accessible')
    parser.add_argument('--out')
    args = parser.parse_args()
    try:
        data = json.loads(Path(args.input).read_text()); result = plan(**data)
    except (PlanningError, TypeError, KeyError, json.JSONDecodeError) as exc:
        print(json.dumps({'error': str(exc)}), file=sys.stderr); return 2
    text = json.dumps(result, indent=2) + '\n'
    if args.out: Path(args.out).write_text(text)
    else: print(text, end='')
    return 0

if __name__ == '__main__': sys.exit(main())
