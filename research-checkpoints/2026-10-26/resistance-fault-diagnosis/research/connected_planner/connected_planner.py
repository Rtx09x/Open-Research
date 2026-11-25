"""Exact generic connected-graph complete-edge-deletion research planner.

Polynomial cutpair/block preprocessing; adaptive optimization exponential in pieces.
Input resistances are exact positive rationals, never floating-point approximations.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
import json
from pathlib import Path
import sys
import networkx as nx
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from exact_search import responses, inverse
from research.planner.planner import Topology as BlockTopology, PlanningError, groups

HEALTHY = ('healthy',)
INFINITY = ('infinity',)


class Topology:
    """Structural planner. This alone does not certify supplied numerical weights."""
    def __init__(self, n, edges, accessible=None, max_pieces=18):
        if type(n) is not int or n < 2:
            raise PlanningError('Require at least two vertices and one fault edge.')
        self.n = n
        try: self.edges = [tuple(e) for e in edges]
        except TypeError as exc: raise PlanningError('Invalid edge list.') from exc
        if any(len(e) != 2 or any(type(v) is not int or not 0 <= v < n for v in e) or e[0] == e[1] for e in self.edges):
            raise PlanningError('Require loopless edges with vertices 0,...,n-1.')
        self.G = nx.Graph(); self.G.add_nodes_from(range(n)); self.G.add_edges_from(self.edges)
        self.m = len(self.edges)
        if self.G.number_of_edges() != self.m or not nx.is_connected(self.G):
            raise PlanningError('Require a simple connected graph with at least one edge.')
        if type(max_pieces) is not int or max_pieces < 1:
            raise PlanningError('max_pieces must be a positive integer.')
        raw_access = list(range(n)) if accessible is None else list(accessible)
        if any(type(v) is not int or not 0 <= v < n for v in raw_access):
            raise PlanningError('Invalid accessible vertex.')
        self.B = sorted(set(raw_access))
        index = {frozenset(e): i for i, e in enumerate(self.edges)}
        self.pieces = sorted([sorted(index[frozenset(e)] for e in es)
                             for es in nx.biconnected_component_edges(self.G)], key=lambda p: p[0])
        self.p = len(self.pieces)
        if self.p > max_pieces:
            raise PlanningError(f'{self.p} pieces exceeds max_pieces={max_pieces}; exact adaptive subset DP is exponential. Increase the explicit guard knowingly.')
        self.bridges = [p[0] for p in self.pieces if len(p) == 1]
        if self.bridges and self.B != list(range(n)) and self.m > 1:
            raise PlanningError('Restricted access with bridges is not implemented; use all vertices.')
        self.blocks = {}; self.local_vertices = {}; self.local_ids = {}
        # Include every physical vertex as an incidence node. Nonarticulations are
        # leaves, so the piece/vertex incidence graph remains a tree.
        self.incidence = nx.Graph(); self.incidence.add_nodes_from(('v', v) for v in range(n))
        for bi, piece in enumerate(self.pieces):
            vs = sorted({v for e in piece for v in self.edges[e]})
            self.local_vertices[bi] = vs
            self.local_ids[bi] = {v: i for i, v in enumerate(vs)}
            for v in vs: self.incidence.add_edge(('p', bi), ('v', v))
            if len(piece) > 1:
                ids = self.local_ids[bi]
                self.blocks[bi] = BlockTopology(len(vs), [(ids[self.edges[e][0]], ids[self.edges[e][1]]) for e in piece])
        assert nx.is_tree(self.incidence)
        self.demand_regions = []; self.leaf_order = []
        self.fixed_queries = None
        if not self.bridges: self.fixed_queries = self._fixed()
        elif self.m == 1: self.fixed_queries = []
        self.queries = list(combinations(self.B, 2))
        if self.m > 1 and not self.queries: raise PlanningError('No identifying accessible queries.')
        prepared = [self._partition(q) for q in self.queries]
        self.rows = [x[0] for x in prepared]; self.hits = [x[1] for x in prepared]
        self.changed_masks = []
        for row in self.rows:
            classes = defaultdict(int)
            for e, label in enumerate(row):
                if label != HEALTHY: classes[label] |= 1 << e
            self.changed_masks.append(list(classes.values()))
        if self.fixed_queries is not None:
            rows = [self.partition(q) for q in self.fixed_queries]
            assert len({tuple(row[e] for row in rows) for e in range(self.m)}) == self.m
        self.masks = [sum(1 << e for e in p) for p in self.pieces]
        self.choices = {}
        @lru_cache(None)
        def edge_mask(state):
            return sum(self.masks[i] for i in range(self.p) if state >> i & 1)
        self.edge_mask = edge_mask
        @lru_cache(None)
        def depth(state):
            mask = edge_mask(state)
            if mask.bit_count() <= 1: return 0
            best = self.m + 1
            for qi, row in enumerate(self.rows):
                nxt = state & ~self.hits[qi]
                if nxt == state: continue
                largest = max((mask & c).bit_count() for c in self.changed_masks[qi])
                tail = (largest - 1).bit_length()
                score = 1 + max(tail, depth(nxt))
                if score < best: best = score; self.choices[state] = qi
            return best
        self.depth = depth
        self.initial = (1 << self.p) - 1
        self.adaptive_count = depth(self.initial)
        self.dp_states = depth.cache_info().currsize

    def _partition(self, query):
        path = nx.shortest_path(self.incidence, ('v', query[0]), ('v', query[1]))
        labels = [HEALTHY] * self.m; hits = 0
        for j in range(1, len(path), 2):
            bi = path[j][1]; piece = self.pieces[bi]; hits |= 1 << bi
            if len(piece) == 1: labels[piece[0]] = INFINITY
            else:
                ids = self.local_ids[bi]
                local = self.blocks[bi].partition((ids[path[j-1][1]], ids[path[j+1][1]]))
                for e, label in zip(piece, local): labels[e] = ('block', bi, label)
        return labels, hits

    def partition(self, query): return self._partition(query)[0]

    def _fixed(self):
        arts = set(nx.articulation_points(self.G)); cycles = []; regions = {}
        K = nx.MultiGraph()
        for bi, block in self.blocks.items():
            vs = self.local_vertices[bi]
            for b, blob in enumerate(block.blobs):
                node = ('b', bi, b); K.add_node(node)
                physical = {vs[v] for v in blob}
                regions[node] = physical - arts if len(block.blobs) == 1 else physical
            for cyc in block.cycles:
                current = block.blob[block.edges[cyc['edges'][0]][0]]; order = []
                for e in cyc['edges']:
                    order.append(('b', bi, current))
                    u, v = block.edges[e]; x, y = block.blob[u], block.blob[v]
                    current = y if current == x else x
                cycles.append(order)
                for a, b in zip(order, order[1:] + order[:1]): K.add_edge(a, b)
            for a in sorted(arts.intersection(vs)):
                x = ('b', bi, block.blob[self.local_ids[bi][a]]); z = ('a', a)
                cycles.append([x, z]); K.add_edge(x, z); K.add_edge(x, z)
        self.auxiliary_cactus = K
        if len(K) == 1:
            if len(self.B) < 2: raise PlanningError('Single three-edge-connected block requires two accessible vertices.')
            self.access_exception = True
            return [tuple(self.B[:2])]
        self.access_exception = False
        leaves = {v for v, d in K.degree() if d == 2}
        self.demand_regions = [sorted(regions[v]) for v in sorted(leaves)]
        missing = [r for r in self.demand_regions if not set(r).intersection(self.B)]
        if missing: raise PlanningError('Accessible set misses mandatory physical regions: ' + str(missing))
        incident = defaultdict(list)
        for ci, cyc in enumerate(cycles):
            for v in cyc: incident[v].append(ci)
        order = []
        def visit(v, parent=None):
            if v in leaves: order.append(v)
            for ci in incident[v]:
                if ci == parent: continue
                cyc = cycles[ci]; i = cyc.index(v)
                for j in range(1, len(cyc)): visit(cyc[(i+j) % len(cyc)], ci)
        visit(next(iter(K)))
        assert set(order) == leaves and len(order) == len(leaves)
        reps = {v: min(regions[v].intersection(self.B)) for v in leaves}
        self.leaf_order = [reps[v] for v in order]
        if len(order) % 2: order.insert(1, order[0])
        h = len(order) // 2
        result = [tuple(sorted((reps[order[i]], reps[order[i+h]]))) for i in range(h)]
        assert all(u != v for u, v in result) and len(set(result)) == len(result)
        return result

    def tree(self, dictionary=None):
        def build(candidates, state=None):
            if len(candidates) == 1: return {'fault_edge_index': candidates[0]}
            def parts(qi):
                out = defaultdict(list)
                for e in candidates: out[self.rows[qi][e]].append(e)
                return out
            if state is not None: qi = self.choices[state]
            else:
                qi = min(range(len(self.queries)), key=lambda i: max(map(len, parts(i).values())))
                assert max(map(len, parts(qi).values())) <= (len(candidates)+1)//2
            bs = parts(qi); assert len(bs) > 1
            branches = []
            for label, S in bs.items():
                nxt = state & ~self.hits[qi] if state is not None and label == HEALTHY else None
                branch = {'candidate_edge_indices': S, 'next': build(S, nxt)}
                if dictionary is not None: branch['response'] = str(dictionary[self.queries[qi]][S[0]])
                branches.append(branch)
            return {'query': list(self.queries[qi]), 'branches': branches}
        return build(list(range(self.m)), self.initial)


def healthy_responses(n, edges, weights, queries):
    lap = [[Fraction(0) for _ in range(n-1)] for _ in range(n-1)]
    for (u, v), r in zip(edges, weights):
        c = 1/r
        if u < n-1: lap[u][u] += c
        if v < n-1: lap[v][v] += c
        if u < n-1 and v < n-1: lap[u][v] -= c; lap[v][u] -= c
    inv = inverse(lap)
    def entry(u, v): return inv[u][v] if u < n-1 and v < n-1 else Fraction(0)
    return [entry(u,u)+entry(v,v)-2*entry(u,v) for u,v in queries]


def plan(n, edges, resistances, accessible=None, max_pieces=18):
    topology = Topology(n, edges, accessible, max_pieces)
    if len(resistances) != len(edges) or any(isinstance(r, (float, bool)) for r in resistances):
        raise PlanningError('Supply one exact positive integer or rational string per edge; floats are rejected.')
    try: weights = [Fraction(r) for r in resistances]
    except (ValueError, ZeroDivisionError, TypeError) as exc: raise PlanningError('Invalid rational resistance.') from exc
    if any(r <= 0 for r in weights): raise PlanningError('All resistances must be positive.')
    Q, matrix = responses(n, edges, resistances=weights)
    baseline = healthy_responses(n, edges, weights, Q)
    for q, row, healthy in zip(Q, matrix, baseline):
        predicted = topology.partition(q)
        # Include the healthy reference even though it is not a fault hypothesis:
        # this catches zero-current accidental invisibility in fully active queries.
        actual = sorted(sorted(s) for s in groups(row + [healthy]))
        structural = sorted(sorted(s) for s in groups(predicted + [HEALTHY]))
        if actual != structural:
            raise PlanningError('Nongeneric input: exact electrical and structural partitions differ at query ' + str(q))
    dictionary = dict(zip(Q, matrix)); fixed = topology.fixed_queries
    if topology.m == 1: fixed = []
    result = {'model': 'exactly one complete edge deletion; positive exact rational resistances',
              'genericity_verified': True, 'n': n, 'edges': topology.edges,
              'resistances': list(map(str, weights)), 'accessible': topology.B,
              'pieces': topology.pieces, 'piece_count': topology.p,
              'adaptive_dp_piece_guard': max_pieces, 'adaptive_dp_states': topology.dp_states,
              'optimal_adaptive_count': topology.adaptive_count,
              'decision_tree': topology.tree(dictionary),
              'mandatory_physical_regions': topology.demand_regions,
              'cactus_leaf_representative_order': topology.leaf_order,
              'optimal_fixed_count': len(fixed) if fixed is not None else None,
              'fixed_status': 'optimal' if fixed is not None else 'unavailable: bridge-containing fixed optimization not implemented',
              'fixed_queries': fixed, 'verified_dictionary_entries': len(Q)*len(edges),
              'healthy_reference_checks': len(Q)}
    if not topology.bridges:
        result['minimum_access_count'] = 2 if topology.access_exception else len(topology.demand_regions)
        result['access_preserves_unrestricted_optima'] = True
    if fixed is not None:
        vectors = [tuple(dictionary[q][e] for q in fixed) for e in range(topology.m)]
        assert len(set(vectors)) == topology.m
        result['fixed_response_dictionary'] = [{'fault_edge_index': e, 'responses': list(map(str, vec))} for e, vec in enumerate(vectors)]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', help='JSON containing n, edges, resistances and optional accessible/max_pieces')
    parser.add_argument('--out'); parser.add_argument('--max-pieces', type=int)
    args = parser.parse_args()
    try:
        data = json.loads(Path(args.input).read_text())
        if args.max_pieces is not None: data['max_pieces'] = args.max_pieces
        result = plan(**data)
    except (PlanningError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({'error': str(exc)}), file=sys.stderr); return 2
    output = json.dumps(result, indent=2) + '\n'
    if args.out: Path(args.out).write_text(output)
    else: print(output, end='')
    return 0


if __name__ == '__main__': sys.exit(main())
