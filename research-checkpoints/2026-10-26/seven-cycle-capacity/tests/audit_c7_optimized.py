"""Exact DAG and root audit using rational logarithm enclosures, not giant powers."""
import json,sys,time,hashlib,runpy
from pathlib import Path
from fractions import Fraction as F
sys.set_int_max_str_digits(0);start=time.time();HERE=Path(__file__).parent;ROOT=Path(__file__).resolve().parents[1]
# Recheck base axioms and S2a independently with our earlier implementation.
g=runpy.run_path(str(HERE/'audit_c7_recycled.py'));base=g['base'];rule=g['rule'];labels=g['labels'];raw=g['raw']
d=json.loads((ROOT/'optimized_recycle_certificate.json').read_text());assert hashlib.sha256(raw).hexdigest()==d['source_base_sha256']
values=[];dims=[];counts=[]
for i,node in enumerate(d['nodes']):
 if node['operation']=='base':
  v=base['vector'];dim=base['base_dimension'];cnt=1
 else:
  assert node['operation']=='S2a';a,b=node['children'];assert 0<=a<i and 0<=b<i
  wa=dict(zip(labels,values[a]));wb=dict(zip(labels,values[b]));v=[sum(wa[x]*wb[y]for x,y in rule[z])for z in labels];dim=dims[a]+dims[b];cnt=counts[a]+counts[b]
 assert cnt==node['leaves'];values.append(v);dims.append(dim);counts.append(cnt)
root=d['root'];v=values[root];dim=dims[root];assert dim==d['dimension']==500*d['leaf_count'];assert v==d['final_vector'];M=v[0]+v[4];assert M==d['M'];assert M>g['M']**6
# log(x)=2*sum z^(2j+1)/(2j+1), z=(x-1)/(x+1).
# For x in[1,2], every term positive, remainder <=2 z^(2n+1)/[(2n+1)(1-z²)].
def log_small(x,n=42):
 assert 1<=x<=2
 z=(x-1)/(x+1);power=z;total=F(0)
 for j in range(n):total+=power/F(2*j+1);power*=z*z
 return 2*total,2*total+2*power/F(2*n+1)/(1-z*z)
L2,U2=log_small(F(2))
def log_int(n,bits=128):
 assert n>0
 e=n.bit_length()-1
 if e<bits:
  lo=hi=F(n,1<<e)
 else:
  shift=e-bits+1;top=n>>shift;lo=F(top,1<<(bits-1));hi=F(top+1,1<<(bits-1))
 l,_=log_small(lo);_,u=log_small(hi)
 return e*L2+l,e*U2+u
ml,mu=log_int(M);r=d['root_numerator'];s=d['root_denominator'];rl,ru=log_int(r);pl,pu=log_int(r+1);sl,su=log_int(s)
assert d['certified_lower_bound']==str(r//s)+'.'+str(r%s).zfill(len(str(s))-1)
# Lower endpoint: d log(r/s) <= log M; upper endpoint: log M < d log((r+1)/s).
margin_lower=ml-dim*(ru-sl);margin_upper=dim*(pl-su)-mu
assert margin_lower>0 and margin_upper>0
out={'exact':True,'method':'independent seven-family/DAG recurrence; rational atanh logarithm bounds with explicit remainder','nodes':len(d['nodes']),'dimension':dim,'leaf_count':counts[root],'strict_improvement_over_128000':True,'certified_lower_bound':d['certified_lower_bound'],'root_log_lower_margin_positive':True,'root_log_upper_margin_positive':True,'root_log_lower_margin_float':float(margin_lower),'root_log_upper_margin_float':float(margin_upper),'seconds':time.time()-start,'scope':'exact finite-code lower bound, not full capacity; novelty unconfirmed'}
(HERE/'c7_optimized_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
