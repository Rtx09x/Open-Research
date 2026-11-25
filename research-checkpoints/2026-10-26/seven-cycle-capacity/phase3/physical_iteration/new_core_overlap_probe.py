"""Cheap exact C1 probe after the15-cycle main-code flip.

Does not reuse any old overlap certificate. Builds the actual134753-word
two-block code and checks all eight published exchange neighborhoods exactly.
This is a gate for whether a full heterogeneous-certificate replay is worthwhile.
"""
from physical_graph import *
from auxiliary_orbit_milp import nh
from collections import defaultdict
import time,resource
def run():
 start=time.monotonic();d=json.loads(BASE.read_text());fam=json.loads((HERE/'core_cycle_family.json').read_text());cy=fam['cycles'][0];X=set(d['X']);PH=set(d['PH']);PV=set(d['PV']);R={r for r,q in d['private_pairs']};hh,vv=nh(PH),nh(PV);X0=X-(hh|vv);XH=X&hh;XV=X&vv;XR=X-X0;n0,nr=nh(X0),nh(XR);records=[]
 for label,main in [('original',set(d['I0'])),('cycle_flip',(set(d['I0'])-set(cy['remove']))|set(cy['add']))]:
  assert len(main)==367 and independent(main)
  assert all({a for a in main if confusable(a,q)}=={r} for r,q in d['private_pairs'])
  B=main-R;blocks=[(B,B),(R,X0),(PH,XH),(PV,XV),(X0,R),(XH,PV),(XV,PH)]
  I2=set().union(*(set(itertools.product(a,b)) for a,b in blocks));assert len(I2)==sum(len(a)*len(b) for a,b in blocks)==134753
  raw={(transform(a),transform(b)) for a,b in I2};assert len(raw)==134753
  def outside(p):return not ((p[0] in n0 and p[1] in n0) or (p[0] in nr and p[1] in nr))
  pre=sum(map(outside,raw));byfirst=defaultdict(set)
  for a,b in raw:byfirst[a].add(b)
  ex=[]
  for rem,ins in d['exchanges']['pairs']:
   rem,ins=tuple(rem),tuple(ins);nb2=nh([ins[1]]);neighbors={(a,b) for a in nh([ins[0]]) for b in byfirst[a]&nb2};ok=rem in raw and ins not in raw and neighbors=={rem} and not outside(rem) and outside(ins);ex.append({'removed':rem,'inserted':ins,'neighbors':sorted(neighbors),'valid':ok})
  valid=all(e['valid'] for e in ex)
  rec={'main':label,'C1_pre_exchange':pre,'all_original_exchanges_valid':valid,'exchange_checks':ex}
  if valid:
   ins={tuple(e[1]) for e in d['exchanges']['pairs']};assert all(not(confusable(a[0],b[0]) and confusable(a[1],b[1])) for a,b in itertools.combinations(ins,2));J=(raw-{tuple(e[0]) for e in d['exchanges']['pairs']})|ins;rec['C1_after_exchange']=sum(map(outside,J));assert rec['C1_after_exchange']==pre+8
  records.append(rec);print(label,pre,valid,rec.get('C1_after_exchange'),flush=True)
 out={'records':records,'seconds':time.monotonic()-start,'maxRSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'scope':'C1 only; no C2-C4 or q15 certificate reused'}
 (HERE/'new_core_overlap_probe.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='records'},indent=2))
if __name__=='__main__':run()
