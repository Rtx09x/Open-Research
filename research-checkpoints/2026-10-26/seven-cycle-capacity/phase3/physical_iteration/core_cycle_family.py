"""Extract conflict-free unicyclic core trades from two-neighbor boundary.

An outside word with exactly two core neighbors is an edge on those neighbors.
Replacing all vertices of a cycle by its edge-words preserves cardinality;
physical independence and cross-block separation are checked, not assumed.
"""
from physical_graph import *
from auxiliary_orbit_milp import nh
from collections import defaultdict,Counter
import time
def run():
 start=time.monotonic();cl=json.loads((HERE/'private_component_closure.json').read_text());core=set(cl['core']);ep=set(sum(cl['components'],[]));owners=[[] for _ in range(16807)]
 for a in core:
  for q in nh([a]):owners[q].append(a)
 qs=[q for q,r in enumerate(owners) if len(r)==2 and all(not confusable(q,e) for e in ep)];edges={q:tuple(owners[q]) for q in qs};inc=defaultdict(set)
 for q,(a,b) in edges.items():inc[a].add(q);inc[b].add(q)
 todo=[a for a in inc if len(inc[a])==1]
 while todo:
  a=todo.pop()
  if len(inc[a])!=1:continue
  q=next(iter(inc[a]));x,y=edges[q];b=y if a==x else x;inc[a].remove(q);inc[b].remove(q)
  if len(inc[b])==1:todo.append(b)
 active={a for a in inc if inc[a]};cycles=[];rejected=[]
 while active:
  startv=min(active);r={startv};qset=set();todo=[startv];active.remove(startv)
  while todo:
   a=todo.pop();assert len(inc[a])==2
   for q in inc[a]:
    qset.add(q)
    for b in edges[q]:
     if b not in r:r.add(b);active.remove(b);todo.append(b)
  assert len(r)==len(qset) and independent(r)
  bad=[[a,b] for a,b in itertools.combinations(sorted(qset),2) if confusable(a,b)]
  rec={'remove':sorted(r),'add':sorted(qset),'size':len(r),'outside_conflicts':bad}
  (rejected if bad else cycles).append(rec)
 cycles.sort(key=lambda c:(-c['size'],c['remove']));fixed=core-set(sum((c['remove'] for c in cycles),[]));blocks=[[c['remove'],c['add']] for c in cycles]+cl['component_choices']
 allblocks=[set(sum(ch,[])) for ch in blocks]
 separated=all(not confusable(a,b) for i,c in enumerate(allblocks) for d in allblocks[:i] for a in c for b in d)
 fixedsep=all(not confusable(a,b) for a in fixed for b in set().union(*allblocks))
 assert separated and fixedsep and independent(fixed)
 assert len(fixed)+sum(len(ch[0]) for ch in blocks)==367
 out={'source_core':sorted(core),'two_core_words_separated_from_ports':len(qs),'fixed':sorted(fixed),'cycles':cycles,'rejected_cycles':rejected,'blocks':blocks,'universal_cross_block_separation':separated,'fixed_separation':fixedsep,'code_count':2**len(cycles)*3**5,'size_each':367,'alphabet_size':len(fixed|set().union(*allblocks)),'seconds':time.monotonic()-start}
 (HERE/'core_cycle_family.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['source_core','fixed','cycles','blocks']},indent=2));print('cycle_sizes',[c['size'] for c in cycles])
if __name__=='__main__':run()
