"""Standalone exact classification of all maximum codes in the842 alphabet.

A367-clique cover forces every367-code to hit each clique exactly once and
exclude multiply covered vertices. Arc consistency reduces the remaining
independent-transversal CSP to small components, exhaustively enumerated here.
Only standard library and direct physical coordinate tests are used.
"""
import json,itertools,hashlib,time
from pathlib import Path
from collections import Counter,defaultdict
HERE=Path(__file__).resolve().parent
def conf(a,b):return all(((a//7**j)-(b//7**j))%7 in (0,1,6) for j in range(5))
def run():
 start=time.monotonic();path=HERE/'second_core_boundary_capacity_cover.json';data=json.loads(path.read_text());assert data['denominator']==1 and data['total_numerator']==367 and all(t['weight']==1 for t in data['terms'])
 cs=[set(t['vertices']) for t in data['terms']];universe=set(data['alphabet']);assert len(cs)==367 and set.union(*cs)==universe and len(universe)==842
 assert all(conf(a,b) for c in cs for a,b in itertools.combinations(c,2))
 multiplicity=Counter(a for c in cs for a in c);removed={a for a in universe if multiplicity[a]>1};allowed=universe-removed;dom=[c&allowed for c in cs];edges={a:{b for b in allowed if a!=b and conf(a,b)} for a in allowed};trace=[]
 while True:
  bad={}
  for j,d in enumerate(dom):
   assert d
   for a in d:
    witness=next((k for k,e in enumerate(dom) if k!=j and e<=edges[a]),None)
    if witness is not None:bad[a]=witness
  if not bad:break
  trace.append([{'word':a,'incompatible_entire_clique':k} for a,k in sorted(bad.items())])
  for d in dom:d.difference_update(bad)
 forced={next(iter(d)) for d in dom if len(d)==1};assert all(not conf(a,b) for a,b in itertools.combinations(forced,2))
 idx={a:j for j,d in enumerate(dom) for a in d};ng=defaultdict(set)
 for a,j in idx.items():
  for b in edges[a]&set(idx):
   k=idx[b]
   if j!=k:ng[j].add(k);ng[k].add(j)
 components=[];seen=set()
 for j,d in enumerate(dom):
  if len(d)==1 or j in seen:continue
  q=[j];seen.add(j);comp=[]
  while q:
   k=q.pop();comp.append(k)
   for b in ng[k]-seen:seen.add(b);q.append(b)
  components.append(sorted(comp))
 solved=[];nodes=0
 def solve(ds):
  nonlocal nodes
  nodes+=1;ds=[set(d) for d in ds]
  while True:
   if any(not d for d in ds):return []
   changes=False
   for i,d in enumerate(ds):
    if len(d)!=1:continue
    a=next(iter(d))
    for j,e in enumerate(ds):
     if j!=i:
      bad=e&edges[a]
      if bad:e.difference_update(bad);changes=True
   if not changes:break
  if all(len(d)==1 for d in ds):return [sorted(next(iter(d)) for d in ds)]
  j=min((i for i,d in enumerate(ds) if len(d)>1),key=lambda i:len(ds[i]));out=[]
  for a in sorted(ds[j]):
   child=[set(d) for d in ds];child[j]={a};out.extend(solve(child))
  return out
 for comp in components:
  sols=solve([dom[j] for j in comp]);assert sols and len({tuple(s) for s in sols})==len(sols)
  for s in sols:assert all(not conf(a,b) for a,b in itertools.combinations(s,2))
  solved.append({'clique_indices':comp,'domains':[sorted(dom[j]) for j in comp],'solutions':sols})
 totals=1;support=set(forced)
 for c in solved:totals*=len(c['solutions']);support.update(sum(c['solutions'],[]))
 # Cross-component/fixed separation makes the Cartesian product exact.
 groups=[set(sum(c['solutions'],[])) for c in solved]+[forced]
 assert all(not conf(a,b) for i,g in enumerate(groups) for h in groups[:i] for a in g for b in h)
 adj={a:{b for b in support if b!=a and conf(a,b)} for a in support};seen=set();shapes=[]
 for a in support:
  if a in seen:continue
  comp={a};todo=[a];seen.add(a)
  while todo:
   z=todo.pop()
   for b in adj[z]-seen:seen.add(b);comp.add(b);todo.append(b)
  shapes.append({'vertices':sorted(comp),'degree_sequence':sorted(len(adj[z]) for z in comp)})
 assert totals==486 and len(support)==392
 assert Counter(len(c['vertices']) for c in shapes)=={1:342,4:5,30:1}
 assert all(c['degree_sequence']==([0] if len(c['vertices'])==1 else [1,1,2,2] if len(c['vertices'])==4 else [2]*30) for c in shapes)
 out={'cover_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'initial_alphabet_size':842,'multi_covered_forbidden':sorted(removed),'arc_consistency_trace':trace,'arc_consistency_rounds':len(trace),'forced_after_arc_consistency':sorted(forced),'components':solved,'enumeration_nodes':nodes,'maximum_code_size':367,'maximum_code_count':totals,'support_of_all_maximum_codes':sorted(support),'support_graph_components':shapes,'seconds':time.monotonic()-start,'scope':'All maximum independent sets in this842-word physical alphabet only'}
 (HERE/'second_boundary_maxima_classification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['multi_covered_forbidden','arc_consistency_trace','forced_after_arc_consistency','components','support_of_all_maximum_codes','support_graph_components']},indent=2));print('component_solution_counts',[len(c['solutions']) for c in solved]);print('support_components',dict(Counter(len(c['vertices']) for c in shapes)))
if __name__=='__main__':run()
