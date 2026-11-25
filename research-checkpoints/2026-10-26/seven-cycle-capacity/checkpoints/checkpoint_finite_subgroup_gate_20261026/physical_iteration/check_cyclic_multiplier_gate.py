"""Independent exact transposed-bitset audit and extension of circular gate.

No C++ output is used to decide feasibility. A circular rank-one code is
{t(a1,...,a5) mod n:t in Z_n}. Distance ≥ceil(2n/7) maps directly to C7^5.
Unit case normalizes one coordinate to1. In the no-unit case, enumerate its
gcd g with n and normalize it to g by multiplying t by a unit; only nonunit
remaining multipliers are allowed. This normalization is exhaustively checked
for the finite n range. Signs identify a and n-a. Four residual choices reduce
to two pair unions; every pair's possible partners are intersected as bitsets.
"""
import json,math,time,resource,os
from pathlib import Path
P=Path(__file__).resolve().parent
def cover(n,k,first,cands):
 ts=[t for t in range(1,n//2+1) if min((first*t)%n,n-(first*t)%n)<k]
 masks={a:sum(1<<i for i,t in enumerate(ts) if min((a*t)%n,n-(a*t)%n)>=k) for a in cands};pairs={}
 for i,a in enumerate(cands):
  for b in cands[i:]:pairs.setdefault(masks[a]|masks[b],(a,b))
 values=list(pairs);N=len(values);columns=[0]*len(ts)
 for j,m in enumerate(values):
  v=1<<j
  while m:
   b=m&-m;m-=b;columns[b.bit_length()-1]|=v
 full=(1<<len(ts))-1;allpartners=(1<<N)-1;checks=0
 for m in values:
  remaining=full^m;possible=allpartners
  while remaining and possible:
   b=remaining&-remaining;remaining-=b;possible&=columns[b.bit_length()-1];checks+=1
  if possible:
   j=(possible&-possible).bit_length()-1;ans=[first,*pairs[m],*pairs[values[j]]]
   assert all(max(min((a*t)%n,n-(a*t)%n) for a in ans)>=k for t in range(1,n))
   return {'first':first,'residual_residues':len(ts),'candidate_multipliers':len(cands),'unique_pair_unions':N,'bitset_intersections':checks,'multipliers':ans}
 return {'first':first,'residual_residues':len(ts),'candidate_multipliers':len(cands),'unique_pair_unions':N,'bitset_intersections':checks,'multipliers':None}
def run():
 resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3));resource.setrlimit(resource.RLIMIT_CPU,(270,270));os.sched_setaffinity(0,{min(os.sched_getaffinity(0))});start=time.monotonic();rows=[]
 control=cover(382,108,1,list(range(1,192)));assert control['multipliers'] is not None;print('POSITIVE_CONTROL',json.dumps(control),flush=True)
 for n in range(368,402):
  k=(2*n+6)//7;units=[a for a in range(1,n) if math.gcd(a,n)==1];nonunits=[a for a in range(1,n//2+1) if math.gcd(a,n)>1];divisors=sorted({math.gcd(a,n) for a in nonunits})
  assert all(any(a*u%n==math.gcd(a,n) for u in units) for a in nonunits)
  r={'n':n,'k':k,'unit':cover(n,k,1,list(range(1,n//2+1))),'no_unit_cases':[cover(n,k,g,nonunits) for g in divisors]};rows.append(r)
  hits=[q for q in [r['unit']]+r['no_unit_cases'] if q['multipliers']]
  print(json.dumps({'n':n,'unit_none':r['unit']['multipliers'] is None,'no_unit_divisors':divisors,'hits':hits,'elapsed':time.monotonic()-start}),flush=True)
  out={'positive_control_n382_k108':control,'records':rows,'complete_range':len(rows)==34,'all_target_cases_infeasible':not any(q['multipliers'] for r in rows for q in [r['unit']]+r['no_unit_cases']),'seconds':time.monotonic()-start,'maxRSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'scope':'Rank-one circular cyclic codes of size368..401 with direct distance-preserving rounding only; nonlinear/translated-deletion-and-completion constructions remain outside.'};(P/'cyclic_multiplier_bitset_audit.json').write_text(json.dumps(out,indent=2)+'\n')
  if hits or time.monotonic()-start>250:break
if __name__=='__main__':run()
