"""Independent source-derived exact audit of all-container tiny Best Fit step bound.
Uses advisor-authored source-derived factual tables/parameter audit; no worker imports.
Pricing is reduced-profit density order rather than worker's raw-weight size order.
"""
from pathlib import Path
from fractions import Fraction as F
import json,time,hashlib
start=time.time();A=Path(__file__).resolve().parents[2]/'online-bin-packing'/'tests'
# Replay the independently authored numerical source transcription and parameter checks,
# stopping before its old pricing run or any output writes.
p=A/'audit_ah_three_parameter.py';env={'__file__':str(p)}
exec(p.read_text().split('count=nodes=prunes=0;constraint_count=0')[0],env)
P=env['modified'];old=env['d'];expected=env['expected'];D=F(1,43)
path=Path(__file__).resolve().parents[2]/'online-bin-packing'/'phase2'/'best_fit/best_fit_certificate.json'
raw=path.read_bytes();C=json.loads(raw);R=F(C['target']);assert R<F(C['previous_one_open_target'])<F(old['target'])
for j,p in P.items():
 row=C['parameters'][str(j)];assert F(row['lower'])==p['min'] and F(row['upper'])==p['max'] and {F(i):F(a)for i,a in row['containers']}==p['types']
refs={(s['x'],s['y']):s for s in old['scenarios']}
def tiny(room,c):
 assert 0<c<=D and room>0
 n=(room.numerator*c.denominator-1)//(room.denominator*c.numerator)
 assert n*c<room<=(n+1)*c
 return room+(D-c)/(F(17,60)-D)*min(room,n*D)
def prove(items,cap,b,B,c,bound):
 rho=b/(B-c);front=[];best=F(-1)
 rows=[(s,w-rho*s,j)for j,s,w in items if s<cap and w>rho*s]
 for s,p,j in sorted(rows,key=lambda r:(r[0],-r[1],r[2])):
  if p>best:front.append((s,p,j));best=p
 front.sort(key=lambda r:r[1]/r[0],reverse=True)
 extra_density=rho*(D-c)/(F(17,60)-D);base=rho*cap;nodes=0;prunes=0
 def rec(i,room,gain):
  nonlocal nodes,prunes
  nodes+=1
  assert base+gain+rho*(tiny(room,c)-room)<=bound
  density=max(extra_density,front[i][1]/front[i][0] if i<len(front) else F(0))
  if base+gain+room*density<=bound:prunes+=1;return
  if i==len(front):return
  s,p,j=front[i];m=(room.numerator*s.denominator-1)//(room.denominator*s.numerator)
  assert m*s<room<=(m+1)*s
  for n in range(m+1):rec(i+1,room-n*s,gain+n*p)
 rec(0,cap,F(0));return nodes,prunes
seen=[];logs=[];dual_logs=[]
for sc in C['scenarios']:
 x,y,w,c=map(F,(sc['x'],sc['y'],sc['w'],sc['c']));assert 0<=c<=D
 ref=refs[sc['x'],sc['y']];assert all(sc.get(k)==ref.get(k)for k in ('u','v','w'));seen.append((x,y))
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
 bound=F(sc.get('target',C['target']));assert bound<=R
 counts=[prove(normal,F(1),tiny_b,tiny_B,c,bound),prove(heavy,y,tiny_b,tiny_B,c,bound-1)]
 logs.append({'interval':[str(x),str(y)],'c':str(c),'nodes':sum(z[0]for z in counts),'prunes':sum(z[1]for z in counts)})
assert sorted(seen)==expected and len(seen)==402
out={'status':'PASS','source_derived_factual_tables_and_parameters_replayed':True,'all_published_analysis_weights_preserved':True,'exact_bound':str(R),'decimal_bound':float(R),'certificate_sha256':hashlib.sha256(raw).hexdigest(),'scenarios':402,'strict_knapsacks':804,'pricing_nodes':sum(x['nodes']for x in logs),'seconds':time.time()-start,'scope':'all-container tiny Best Fit AH variant; step-charge upper bound, not tightness','checks':logs}
Path(__file__).with_name('packing_best_fit_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k!='checks'},indent=2))
