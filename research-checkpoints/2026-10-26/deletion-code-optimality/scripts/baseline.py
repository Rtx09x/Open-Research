import json,collections,hashlib,sys
from pathlib import Path
from common import *
n=int(sys.argv[1]) if len(sys.argv)>1 else 12
code=vt(n); ds,A=incidence(n)
# First checker: packed integer deletion incidence.
owner={}
for x in code:
 for y in ds[x]:
  assert y not in owner
  owner[y]=x
# Second checker: direct string slicing, independently including checksum.
strings=[format(x,f'0{n}b') for x in code]
assert len(strings)==len(set(strings))
seen={}
for s in strings:
 assert sum(i for i,c in enumerate(s,1) if c=='1')%(n+1)==0
 for t in {s[:k]+s[k+1:] for k in range(n)}:
  assert t not in seen
  seen[t]=s
assert len(seen)==len(owner)
conflicts={x:sorted({owner[y] for y in ds[x]}) for x in range(1<<n) if x not in code}
report={'n':n,'size':len(code),'deletion_outputs_covered':len(owner),'total_outputs':1<<(n-1),'independent_string_check':True,'degree_counts':dict(sorted(collections.Counter(map(len,conflicts.values())).items())),'run_counts':dict(sorted(collections.Counter(len(ds[x]) for x in code).items()))}
out=Path('evidence');out.mkdir(exist_ok=True)
(out/f'vt0_n{n}.txt').write_text('\n'.join(strings)+'\n')
report['sha256']=hashlib.sha256((out/f'vt0_n{n}.txt').read_bytes()).hexdigest()
(out/f'baseline_n{n}.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
