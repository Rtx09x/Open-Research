"""Independent source-derived complete AH algorithm-parameter audit; Fraction only.
No worker code imports. Reuses advisor's independently written source parser,
then separately constructs the full scenario partition and target-prices it.
"""
from pathlib import Path
from fractions import Fraction as F
import json,time,contextlib,io
start=time.time();ROOT=Path(__file__).resolve().parents[1]
# Replay the independent numerical transcription; full source text is deliberately excluded.
parser=Path(__file__).with_name('source_tables.py').read_text()
exec(parser)
d=json.loads((ROOT/'ah_three_parameter_full_certificate.json').read_text());R=F(d['target']);old=F(d['published_exact_target']);assert R<old
# Verify the entire modified algorithm against the source, not merely data self-consistency.
assert [(m['class'],m['from_type'],m['to_type'])for m in d['modifications']]==[(172,2,6),(179,10,2),(167,1,3)]
modified={j:{'min':p['min'],'max':p['max'],'types':dict(p['types'])}for j,p in classes.items()}
for m in d['modifications']:
 amount=F(m['mass']);assert 0<amount<F(1,500)
 modified[m['class']]['types'][F(m['from_type'])]-=amount
 modified[m['class']]['types'][F(m['to_type'])]+=amount
for j,p in modified.items():
 v=d['parameters'][str(j)];assert F(v['lower'])==p['min'] and F(v['upper'])==p['max']
 assert dict((F(i),F(a))for i,a in v['containers'])==p['types']
 assert all(a>0 for a in p['types'].values()) and sum(p['types'].values())==1
 assert j==2 or p['max']==modified[j-1]['min']
 assert all(0<(i if j==212 else i*p['max'])<=1 for i in p['types'])
# Closed breakpoints: all class boundaries, supported volumes, their complements.
V={F(0),F(1,2)}
for j,p in modified.items():
 V.update([p['min'],p['max']])
 for i in p['types']:
  vol=i if j==212 else i*p['max'];V.update([vol,1-vol])
V=sorted(v for v in V if 0<=v<=F(1,2));expected=list(zip(V,V[1:]));seen=[]

def prove(items,rho,capacity,target):
 # Net profit relative to infinitesimal sand. One-item dominance is safe.
 pairs=[]
 for size,weight,label in items:
  profit=weight-rho*size
  if size<capacity and profit>0:pairs.append((size,profit,label))
 front=[];top=F(-1)
 for size,profit,label in sorted(pairs,key=lambda z:(z[0],-z[1],str(z[2]))):
  if profit>top:front.append((size,profit,label));top=profit
 front.sort(key=lambda z:z[1]/z[0],reverse=True)
 ceiling=target-rho*capacity;assert ceiling>=0
 nodes=0;prunes=0
 def visit(i,remaining,gain):
  nonlocal nodes,prunes
  nodes+=1;assert gain<=ceiling,(target,gain+rho*capacity)
  if i==len(front):return
  size,profit,_=front[i]
  if gain+remaining*profit/size<=ceiling:prunes+=1;return
  m=(remaining.numerator*size.denominator-1)//(remaining.denominator*size.numerator)
  assert m*size<remaining<=(m+1)*size
  for q in range(m+1):visit(i+1,remaining-q*size,gain+q*profit)
 visit(0,capacity,F(0));return nodes,prunes

# Independently check that every analysis weight remains the published one.
def interval(s):
 vals=re.findall(r'\\frac\{(\d+)\}\{(\d+)\}',s);assert len(vals)==2
 return tuple(F(int(a),int(b))for a,b in vals)
small_rows=[(*interval(row[1]),number(row[2]))for row in table_rows('A2.T2.1')[1:]]
large_rows=[(*interval(row[0]),number(row[1]),number(row[2]),number(row[3]))for row in table_rows('A2.T3.1')[1:]]
assert F(facts['critical_w'])==F(413913,524288) and F(facts['smallest_w'])==0
for sc in d['scenarios']:
 x,y=F(sc['x']),F(sc['y'])
 if y<=F(1,6):assert F(sc['w'])==0
 elif x>=F(3,10) and y<=F(1,3):assert F(sc['w'])==F(413913,524288)
 elif y<=F(1,3):
  matches=[ww for lo,hi,ww in small_rows if lo<=x<y<=hi];assert matches==[F(sc['w'])]
 else:
  matches=[(uu,vv,ww)for lo,hi,uu,vv,ww in large_rows if lo<=x<y<=hi];assert matches==[(F(sc['u']),F(sc['v']),F(sc['w']))]

count=nodes=prunes=0;constraint_count=0
for sc in d['scenarios']:
 x,y,w=F(sc['x']),F(sc['y']),F(sc['w']);seen.append((x,y));assert 0<=w<=1
 k=next(j for j,p in modified.items()if p['min']<=x<y<=p['max']);large=k<=165
 if large:
  u,v=F(sc['u']),F(sc['v']);aa=modified[k]['types'].get(F(1),F(0));bb=modified[k]['types'].get(F(2),F(0))
  assert aa+bb==1 and 0<=u<=v<=1
  assert u*(aa+2*bb)+w*aa>=1 and u*bb+v>=1 and v*aa+2*u*bb+(1-w)*bb>=1
  constraint_count+=3
 normal=[(F(1,2),w,'huge< a')];heavy=[]
 for j,p in modified.items():
  if large and j==k:
   normal += [(p['min'],u,(j,'u')),(x,v,(j,'v'))];heavy.append((p['min'],u,j));continue
  num=den=F(0)
  for i,a in p['types'].items():
   vol=i if j==212 else i*p['max']
   if vol>F(1,2):
    if vol<=1-y:rw=w
    else:assert vol>=1-x;rw=F(1)
   else:
    if vol<=x:rw=1-w
    else:assert vol>=y;rw=F(1)
   num+=a*rw;den+=a*(i-F(1,43)if j==212 else i)
  weight=num/den
  if j==212:rho=weight
  else:
   normal.append((p['min'],weight,j))
   if j>=k:heavy.append((p['min'],weight,j))
 assert 0<=rho<=2
 for items,capacity,target in [(normal,F(1),R),(heavy,y,R-1)]:
  n,p=prove(items,rho,capacity,target);nodes+=n;prunes+=p
 count+=1
assert sorted(seen)==expected
out={'status':'PASS','exact':True,'source_parameters_from_independent_numeric_transcription':True,'all_modified_parameters_matched':True,'all_analysis_weights_match_primary_paper':True,'complete_partition_intervals':count,'large_validity_inequalities':constraint_count,'strict_knapsack_cases':2*count,'independent_pricing_nodes':nodes,'fractional_prunes':prunes,'bound':str(R),'bound_decimal':float(R),'gain_over_published_exact_bound':str(old-R),'seconds':time.time()-start,'scope':'new admissible parameter choice of existing AH framework; no reliance on printed old scenario upper bounds; novelty not established'}
Path(__file__).with_name('ah_three_parameter_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
