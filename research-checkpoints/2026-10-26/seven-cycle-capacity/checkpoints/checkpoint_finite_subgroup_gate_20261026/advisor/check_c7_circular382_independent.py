"""Independent exhaustive n=382 rank-one circular classification, no worker imports."""
from itertools import combinations_with_replacement,product
from math import gcd
from pathlib import Path
import json,time
start=time.monotonic();n=382;k=107

def enumerate_case(first,allowed):
 bad=[t for t in range(1,192) if min(first*t%n,(-first*t)%n)<k]
 full=(1<<len(bad))-1
 masks={a:sum(1<<i for i,t in enumerate(bad) if min(a*t%n,(-a*t)%n)>=k) for a in allowed}
 grouped={}
 for a,b in combinations_with_replacement(allowed,2):grouped.setdefault(masks[a]|masks[b],[]).append((a,b))
 unions=list(grouped);indexed=[0]*len(bad)
 for j,mask in enumerate(unions):
  for i in range(len(bad)):
   if (mask>>i)&1:indexed[i]|=1<<j
 solutions=set()
 for u in unions:
  required=full^u;possible=(1<<len(unions))-1
  while required and possible:
   bit=required&-required;required-=bit;possible&=indexed[bit.bit_length()-1]
  while possible:
   bit=possible&-possible;possible-=bit;v=unions[bit.bit_length()-1]
   for p,q in product(grouped[u],grouped[v]):solutions.add(tuple(sorted((first,*p,*q))))
 return sorted(solutions)
units=[u for u in range(1,n) if gcd(u,n)==1]
nonunits=[a for a in range(1,192) if gcd(a,n)>1]
assert all(any(a*u%n==gcd(a,n) for u in units) for a in range(1,n))
sol=enumerate_case(1,list(range(1,192)))
assert sol==[(1,7,39,49,109)]
assert all(not enumerate_case(g,nonunits) for g in (2,191))
minimum=min(max(min(a*t%n,(-a*t)%n)for a in sol[0])for t in range(1,n))
assert minimum==108
# All k108 solutions are among k107 solutions; the unique k107 solution meets108.
out={'PASS':True,'n':n,'thresholds':[107,108],'unit_normalized_solutions':sol,'no_unit_gcd_cases':[2,191],'minimum_of_unique_template':minimum,'seconds':time.monotonic()-start,'zero_coordinate_case':'A zero can be replaced by a repeated nonzero multiplier without harming coverage; the unique resulting feasible template has five distinct nonzero coordinates, so no omitted zero-coordinate solution exists.','scope':'Complete rank-one circular classification at n382 only, modulo unit reparameterization, coordinate signs and permutations. No nonlinear-code exclusion.'}
Path(__file__).with_name('c7_circular382_independent_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
