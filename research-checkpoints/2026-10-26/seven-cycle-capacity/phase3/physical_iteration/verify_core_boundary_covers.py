"""Standalone stdlib auditor of the437/842 original-channel clique covers."""
import json,itertools,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
def conf(a,b):return all(((a//7**j)-(b//7**j))%7 in (0,1,6) for j in range(5))
first=json.loads((HERE/'first_core_boundary_certificate.json').read_text());core=set(first['core']);old=set(first['original_alphabet']);u=set(first['alphabet']);parts=first['clique_partition'];lower=set(first['lower_code'])
assert len(core)==357 and len(old)==377 and len(u)==437 and len(parts)==367
assert len(lower)==367 and lower<=u and all(not conf(a,b) for a,b in itertools.combinations(lower,2))
assert len(sum(parts,[]))==len(u) and set(sum(parts,[]))==u
assert all(conf(a,b) for c in parts for a,b in itertools.combinations(c,2))
bd={q for q in range(16807) if q not in old and sum(conf(q,a) for a in core)==1};assert bd==u-old
second=json.loads((HERE/'second_core_boundary_capacity_cover.json').read_text());u2=set(second['alphabet']);assert len(u2)==842 and lower<=u2
assert u2=={q for q in range(16807) if sum(conf(q,a) for a in core)<=2}
cov={q:0 for q in u2};den=second['denominator'];total=0
for term in second['terms']:
 c=term['vertices'];w=term['weight'];assert w>0 and len(c)==len(set(c)) and set(c)<=u2
 assert all(conf(a,b) for a,b in itertools.combinations(c,2))
 for q in c:cov[q]+=w
 total+=w
assert min(cov.values())>=den and total==367*den==second['total_numerator']
out={'first_boundary_vertices':437,'second_boundary_vertices':842,'first_partition_cliques':367,'second_cover_terms':len(second['terms']),'second_denominator':den,'both_restricted_capacities_exactly':367,'checks':'full-space core-neighborhood membership, direct-coordinate cliques, integer coverage, independent367 lower code','source_sha256':hashlib.sha256((HERE/'second_core_boundary_capacity_cover.json').read_bytes()).hexdigest()}
(HERE/'core_boundary_cover_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
