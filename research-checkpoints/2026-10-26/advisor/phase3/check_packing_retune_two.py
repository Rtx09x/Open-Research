"""Independent source-derived exact audit of all-container tiny Best Fit ordered-suffix bound.
Uses only advisor's frozen source-derived factual-table/parameter audit; no worker imports.
Pricing is reduced-profit density order rather than worker's raw-weight size order.
"""
from pathlib import Path
from fractions import Fraction as F
import json,time,hashlib
start=time.time();A=Path(__file__).resolve().parents[2]/'online-bin-packing'/'tests'
# Reuse the independently authored, frozen source parser and parameter checks,
# stopping before its old pricing run or any output writes.
p=A/'audit_ah_three_parameter.py';env={'__file__':str(p)}
exec(p.read_text().split('count=nodes=prunes=0;constraint_count=0')[0],env)
P=env['modified'];old=env['d'];expected=env['expected'];D=F(1,43)
path=Path(__file__).resolve().parents[2]/'online-bin-packing/phase4/retune_two/retuned_certificate.json'
raw=path.read_bytes();C=json.loads(raw);R=F(C['target']);assert R<F(C['previous_bound'])<F(old['target'])
anchor_path=path.parents[1]/'ordered_suffix'/'ordered_suffix_certificate.json'
anchor_raw=anchor_path.read_bytes();anchor=json.loads(anchor_raw)
assert C['source_certificate_sha256']==hashlib.sha256(anchor_raw).hexdigest()
assert sorted(C['changed_classes'])==[167,179]
changed=[]
for j,p in P.items():
 row=C['parameters'][str(j)]
 newtypes={F(i):F(a) for i,a in row['containers']}
 assert set(newtypes)==set(p['types']) and sum(newtypes.values())==1 and min(newtypes.values())>0
 if newtypes!=p['types']:
  assert j in (167,179);changed.append(j);p['types']=newtypes
assert sorted(changed)==[167,179]
anchor_refs={(s['x'],s['y']):s for s in anchor['scenarios']}

for j,p in P.items():
 row=C['parameters'][str(j)];assert F(row['lower'])==p['min'] and F(row['upper'])==p['max'] and {F(i):F(a)for i,a in row['containers']}==p['types']
refs={(s['x'],s['y']):s for s in old['scenarios']}
def component(b,B,c,g):
 assert 0<=c<=g<=D and B>g
 rho=b/(B-c)
 return rho,rho*(g-c)/(B-g),b/(B-g)
def hinge(room,g):
 n=room//D;rem=room-n*D
 return n*(D-g)+max(F(0),rem-g)

def bonus(room,c):
 if c==0:return room
 if c==D:return F(0)
 n=(room.numerator*c.denominator-1)//(room.denominator*c.numerator)
 assert n*c<room<=(n+1)*c
 return min(room,n*D)

def prove(items,cap,b,B,mix,bound):
 assert sum(w for c,g,w in mix)==1 and min(w for c,g,w in mix)>=0
 comps=[(c,g,weight,*component(b,B,c,g)) for c,g,weight in mix]
 rho=sum(w*base for c,g,w,base,extra,he in comps)
 extra_density=sum(w*(extra+he*(D-g)/D) for c,g,w,base,extra,he in comps)
 def excess(room):return sum(w*(extra*bonus(room,c)+he*hinge(room,g)) for c,g,w,base,extra,he in comps)
 front=[];best=F(-1)
 rows=[(size,weight-rho*size,j) for j,size,weight in items if size<cap and weight>rho*size]
 for size,profit,j in sorted(rows,key=lambda r:(r[0],-r[1],r[2])):
  if profit>best:front.append((size,profit,j));best=profit
 front.sort(key=lambda r:r[1]/r[0],reverse=True)
 base=rho*cap;nodes=prunes=0
 def rec(i,room,gain):
  nonlocal nodes,prunes
  nodes+=1
  assert base+gain+excess(room)<=bound
  density=max(extra_density,front[i][1]/front[i][0] if i<len(front) else F(0))
  if base+gain+room*density<=bound:prunes+=1;return
  if i==len(front):return
  size,profit,j=front[i];m=(room.numerator*size.denominator-1)//(room.denominator*size.numerator)
  assert m*size<room<=(m+1)*size
  for count in range(m+1):rec(i+1,room-count*size,gain+count*profit)
 rec(0,cap,F(0));return nodes,prunes
seen=[];logs=[];dual_logs=[]
for sc in C['scenarios']:
 x,y,w,c=map(F,(sc['x'],sc['y'],sc['w'],sc['c']));assert 0<=c<=D
 ref=refs[sc['x'],sc['y']];assert all(sc.get(k)==ref.get(k)for k in ('u','v','w'));seen.append((x,y));assert sc['analysis_mixture']==anchor_refs[sc['x'],sc['y']]['analysis_mixture']
 k=next(j for j,p in P.items()if p['min']<=x<y<=p['max']);large=k<=165
 normal=[(1,F(1,2),w)];heavy=[]
 if large:
  u,v=F(sc['u']),F(sc['v']);alpha=P[k]['types'].get(F(1),F(0));beta=P[k]['types'][F(2)]
  assert u*(alpha+2*beta)+w*alpha>=1 and u*beta+v>=1 and v*alpha+2*u*beta+(1-w)*beta>=1
 for j,p in P.items():
  if large and j==k:
   normal.extend([(j,p['min'],u),(1000+j,x,v)]);heavy.append((j,p['min'],u));continue
  b=mean=F(0)
  for typ,alpha in p['types'].items():
   vol=typ if j==212 else typ*p['max']
   if vol>F(1,2):
    if vol<=1-y:charge=w
    else:assert vol>=1-x;charge=F(1)
   else:
    if vol<=x:charge=1-w
    else:assert vol>=y;charge=F(1)
   b+=alpha*charge;mean+=alpha*typ
  if j==212:tiny_b,tiny_B=b,mean
  else:
   normal.append((j,p['min'],b/mean))
   if j>=k:heavy.append((j,p['min'],b/mean))
 bound=F(sc['maximum']);assert bound<=R
 mix=[tuple(map(F,row)) for row in sc['analysis_mixture']]
 if (x,y)!=(F(3,7),F(1,2)):assert mix==[(c,D,F(1))]
 counts=[prove(normal,F(1),tiny_b,tiny_B,mix,bound),prove(heavy,y,tiny_b,tiny_B,mix,bound-1)]
 logs.append({'interval':[str(x),str(y)],'c':str(c),'nodes':sum(z[0]for z in counts),'prunes':sum(z[1]for z in counts)})
assert sorted(seen)==expected and len(seen)==402
assert (x,y)==(F(3,7),F(1,2))

# The unchanged physical G row yields a constant fixed-charge two-coordinate floor.
itemmap={j:(size,weight)for j,size,weight in normal}
pattern=[(1,1),(165,1),(172,1)]
rem=1-sum(itemmap[j][0]*cnt for j,cnt in pattern)
const=sum(itemmap[j][1]*cnt for j,cnt in pattern)
assert rem==F(1,60) and all(j not in (167,179) for j,cnt in pattern)
assert len(mix)==1
c,g,weight=mix[0];assert c<rem<g and rem<D
floor=const+tiny_b*rem/(tiny_B-g)
assert floor==R
# For every class167/179 choice preserving their supports, this same pattern and
# fixed tiny charge have the same limiting weight. Perturb non-tiny sizes above
# their infima and reduce tiny size by the total perturbation: still c<tiny<g.
out={'status':'PASS','source_parameters_independently_reparsed':True,'all_published_analysis_weights_preserved':True,'exact_bound':str(R),'decimal_bound':float(R),'certificate_sha256':hashlib.sha256(raw).hexdigest(),'scenarios':402,'strict_knapsacks':804,'pricing_nodes':sum(x['nodes']for x in logs),'seconds':time.time()-start,'scope':'Revised class167/179 proportions of all-container tiny Best Fit AH; fixed ordered-suffix charges. Exact upper and fixed-two-coordinate analysis floor, not algorithm tightness or full parameter optimum','changed_classes':changed,'physical_floor':str(floor),'checks':logs}
Path(__file__).with_name('packing_retune_two_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k!='checks'},indent=2))
