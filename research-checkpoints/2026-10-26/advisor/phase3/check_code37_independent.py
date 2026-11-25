"""Independent Fraction-only contraction and all 98 six-qubit KL identities.
No worker code imports; consumes declarative certificate data only.
"""
import ast,json,math,hashlib,time,sys
from fractions import Fraction as Q
from pathlib import Path
sys.set_int_max_str_digits(0)
st=time.time();src=Path(__file__).resolve().parents[2]/'symmetric-quantum-codes'/'phase3'
r=json.loads((src/'code37_root_certificate.json').read_text());kl=json.loads((src/'code37_kl_reduction.json').read_text())
N=18;assert r['n']==37 and r['t']==3 and r['distance']==7 and r['q0']=='1'
assert r['variables']==['q'+str(i)for i in range(1,19)]
def clean(p):return {k:v for k,v in p.items()if v}
def add(p,q,sgn=1):
 d=p.copy()
 for k,v in q.items():d[k]=d.get(k,Q(0))+sgn*v
 return clean(d)
def mul(p,q):
 d={}
 for a,x in p.items():
  for b,y in q.items():
   k=tuple(sorted(a+b));assert len(k)<=2;d[k]=d.get(k,Q(0))+x*y
 return clean(d)
def parse(e):
 if isinstance(e,ast.Constant):assert isinstance(e.value,int);return {():Q(e.value)}
 if isinstance(e,ast.Name):assert e.id in r['variables'];return {(int(e.id[1:]),):Q(1)}
 if isinstance(e,ast.UnaryOp)and isinstance(e.op,ast.USub):return {k:-v for k,v in parse(e.operand).items()}
 if isinstance(e,ast.BinOp):
  a=parse(e.left)
  if isinstance(e.op,ast.Pow):assert isinstance(e.right,ast.Constant)and e.right.value==2;return mul(a,a)
  b=parse(e.right)
  if isinstance(e.op,ast.Add):return add(a,b)
  if isinstance(e.op,ast.Sub):return add(a,b,-1)
  if isinstance(e.op,ast.Mult):return mul(a,b)
  if isinstance(e.op,ast.Div):assert list(b)==[()];return {k:v/b[()]for k,v in a.items()}
 raise ValueError(ast.dump(e))
F=[parse(ast.parse(s,mode='eval').body)for s in r['equations']];assert len(F)==18
c=[Q(1)]+list(map(Q,r['center']));rad=Q(r['radius'])
f=[sum(v*math.prod(c[i]for i in k)for k,v in p.items())for p in F]
J=[[Q(0)for _ in range(N)]for _ in F];Hs=[[[Q(0)for _ in range(N)]for _ in range(N)]for _ in F]
for a,p in enumerate(F):
 for k,v in p.items():
  for pos,j in enumerate(k):J[a][j-1]+=v*math.prod(c[i]for q,i in enumerate(k)if q!=pos)
  if len(k)==2:
   i,j=k;Hs[a][i-1][j-1]+=v;Hs[a][j-1][i-1]+=v
# independent exact inverse
aug=[row[:]+[Q(i==j)for j in range(N)]for i,row in enumerate(J)]
for j in range(N):
 pivot=next(i for i in range(j,N)if aug[i][j]);aug[j],aug[pivot]=aug[pivot],aug[j]
 d=aug[j][j];aug[j]=[v/d for v in aug[j]]
 for i in range(N):
  if i==j:continue
  d=aug[i][j]
  if d:aug[i]=[a-d*b for a,b in zip(aug[i],aug[j])]
B=[row[N:]for row in aug]
assert all(sum(B[i][a]*J[a][j]for a in range(N))==int(i==j)for i in range(N)for j in range(N))
eta=max(abs(sum(B[i][a]*f[a]for a in range(N)))for i in range(N))
L=max(sum(abs(sum(B[i][a]*Hs[a][ell][j]for a in range(N)))for ell in range(N)for j in range(N))for i in range(N))
assert eta==Q(r['eta'])and L==Q(r['L']);assert eta+L*rad**2<rad and L*rad<1
print('Contraction PASS',float(eta),float(L*rad),flush=True)
# Homogenize q0=1 equations; reconstruct reduced density matrices combinatorially.
FH=[{tuple(sorted((0,)*(2-len(k))+k)):v for k,v in p.items()}for p in F]
def v0(w):return w//2 if w%2==0 else None
def v1(w):return v0(37-w)
def pair(d,i,j,v):
 if i is not None and j is not None:
  k=tuple(sorted((i,j)));d[k]=d.get(k,Q(0))+v
req=[]
for a in range(7):
 for b in range(7):
  diff={};cross={}
  for k in range(32):
   v=math.comb(31,k);pair(diff,v0(k+a),v0(k+b),v);pair(diff,v1(k+a),v1(k+b),-v);pair(cross,v0(k+a),v1(k+b),v)
  req += [clean(diff),clean(cross)]
assert kl['n']==37 and kl['t']==3 and kl['count']==len(req)==98 and kl['equation_count']==18
for num,(p,cs)in enumerate(zip(req,kl['coefficients'])):
 assert len(cs)==18
 d={}
 for f0,z in zip(FH,map(Q,cs)):
  for k,v in f0.items():d[k]=d.get(k,Q(0))+z*v
 assert clean(d)==p,num
out={'passed':True,'n':37,'t':3,'distance':7,'root_sha256':hashlib.sha256((src/'code37_root_certificate.json').read_bytes()).hexdigest(),'kl_sha256':hashlib.sha256((src/'code37_kl_reduction.json').read_bytes()).hexdigest(),'variables':18,'exact_KL_polynomials':98,'eta':str(eta),'L':str(L),'radius':str(rad),'eta_float':float(eta),'Lr_float':float(L*rad),'existence':True,'contraction':True,'seconds':time.time()-st,'method':'stdlib ast sparse polynomials + Fraction Gauss-Jordan; no worker imports, no floating proof arithmetic','scope':'Existence of real fully symmetric two-dimensional n37 code correcting arbitrary three-qubit errors; not minimality or novelty.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items()if k not in('eta','L')})
