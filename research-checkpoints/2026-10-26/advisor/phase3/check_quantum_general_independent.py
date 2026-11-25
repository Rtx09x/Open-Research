"""Independent general-spin dual replay and low-rank KL eigenresidual check.
No worker/model imports. SymPy exact 6j sign/square -> Arb, not Racah factorial code.
"""
import json,sys,time,hashlib
from pathlib import Path
from fractions import Fraction as Q
from functools import lru_cache
import sympy as sp
from sympy.physics.wigner import wigner_6j
from flint import arb,arb_mat,fmpq,ctx
ctx.prec=256
n,t=map(int,sys.argv[1:3]);N=n+1;j=sp.Rational(n,2);cspin=Q(n*(n+2),4)
source=Path(__file__).resolve().parents[2]/'symmetric-quantum-codes'/'phase3'/f'general_dual_n{n}_t{t}.json';raw=source.read_bytes();data=json.loads(raw);scale=data['scale'];assert(data['n'],data['t'],data['K'],data['distance'])==(n,t,2,2*t+1)
st=time.time()
def ball(x):x=Q(x);return arb(fmpq(x.numerator,x.denominator))
def rat(x):assert type(x)==int;return Q(x,scale)
def eye(d):return arb_mat([[int(a==b)for b in range(d)]for a in range(d)])
def zmat(d):return arb_mat(d,d)
def matrix(x):return arb_mat([[ball(rat(v))for v in row]for row in x])
def symmetric(A):return(A+A.transpose())/2
@lru_cache(None)
def six(a,b,c,d,e,f):
 try:s=wigner_6j(a,b,c,d,e,f)
 except ValueError:return arb(0)
 if not s:return arb(0)
 sq=sp.cancel(s*s);assert sq.is_Rational and sq>0
 return (-1 if s<0 else 1)*ball(Q(int(sq.p),int(sq.q))).sqrt()
def sign(x):assert x==int(x);return (-1)**int(x)
blocks={}
for J2 in range(n%2,3*n+1,2):
 J=sp.Rational(J2,2);ls=[L for L in range(N)if abs(L-j)<=J<=L+j];d=len(ls);I=eye(d)
 swap23=arb_mat([[sign(n)*ball((2*L+1)*(2*K+1)).sqrt()*six(j,j,L,j,J,K)for K in ls]for L in ls])
 swap12=arb_mat([[sign(n-L)*int(a==b)for b in range(d)]for a,L in enumerate(ls)])
 swap13=swap12*swap23*swap12;G=[I,swap12,swap23,swap13,swap12*swap23,swap23*swap12]
 symproj=sum(G,zmat(d))/6;antiproj=(I-swap12-swap23-swap13+swap12*swap23+swap23*swap12)/6
 blocks[J2]={'J':J,'ls':ls,'I':I,'swap13':swap13,'G':G,'sym':symproj,'std':I-symproj-antiproj,'support':I-antiproj,'dual':zmat(d),'ppt':zmat(d)}
 for A in(swap12,swap23,swap13):
  err=A*A-I;assert all(abs(err[a,b])<ball(Q(1,10**55))for a in range(d)for b in range(d))
M=[[sign(n+r+k)*(2*r+1)*six(j,j,r,j,j,k)for k in range(N)]for r in range(N)]
H=[[2*M[r][k]-int(r==k)for k in range(N)]for r in range(N)]
shadow=[[sign(k)*M[r][k]for k in range(N)]for r in range(N)]
a=[arb(0)for _ in range(N)];pair=[arb(0)for _ in range(N)]
y=list(map(rat,data['equality_dual']));constant=y[0]+Q(N,2)*y[1]
for k in range(N):a[k]=-ball(y[0])*int(k==0)-ball(y[1])-sum((ball(y[r+1])*H[r][k]for r in range(1,2*t+1)),arb(0))
it=iter(y[2+2*t:])
for L in range(N):
 sectors=[('sym',Q(4,3)),('std',Q(2,3))]if sign(n-L)==1 else[('std',Q(2))]
 for sector,ratio in sectors:
  yy=ball(next(it));pair[L]+=yy*ball(ratio)
  for block in blocks.values():
   if L in block['ls']:
    ix=block['ls'].index(L);E=zmat(len(block['ls']));E[ix,ix]=1;block['dual']-=yy*symmetric(E*block[sector])
try:next(it);raise AssertionError('equality length')
except StopIteration:pass
zs=data['enumerator_inequality_dual'];assert all(type(x)==int and x>=0 for x in zs);zz=iter(map(rat,zs))
for k in range(N):a[k]+=ball(next(zz))
for r in range(2*t+1,N):
 z=ball(next(zz))
 for k in range(N):a[k]+=z*H[r][k]
for L in range(N):
 z=ball(next(zz))
 for k in range(N):a[k]+=z*shadow[L][k]
try:next(zz);raise AssertionError('inequality length')
except StopIteration:pass
for k in range(N):a[k]+=sum((pair[L]*ball(Q(4,N))*shadow[L][k]for L in range(N)),arb(0))
for item in data['ordinary_PSD']:
 b=blocks[item['J2']];assert item['Ls']==b['ls'];A=matrix(item['basis_U'])*matrix(item['factor']);b['dual']+=A*A.transpose()
for item in data['PPT']:
 b=blocks[item['J2']];F=matrix(item['factor']);D=F*F.transpose();ix=[b['ls'].index(L)for L in item['Ls']]
 for p,pp in enumerate(ix):
  for q,qq in enumerate(ix):b['ppt'][pp,qq]+=D[p,q]
for J2,b in blocks.items():
 for p,L in enumerate(b['ls']):
  for q,Lp in enumerate(b['ls']):
   b['dual'][p,q]+=sum((sign(n)*six(L,j,b['J'],Lp,j,c['J'])*c['ppt'][c['ls'].index(L),c['ls'].index(Lp)]for c in blocks.values()if L in c['ls']and Lp in c['ls']),arb(0))
print('Independent cone coefficients ready',time.time()-st,flush=True)
# Cache exact local-Casimir matrices; independently check intended low-rank vectors.
@lru_cache(None)
def casimir(L,Lp):
 bs=[(J2,b)for J2,b in blocks.items()if L in b['ls']and Lp in b['ls']];js=[b['J']for _,b in bs]
 C=arb_mat([[ball(2*cspin)*(int(K==J)-N*sign(L+Lp)*ball((2*K+1)*(2*J+1)).sqrt()*six(j,K,L,J,j,1)*six(j,K,Lp,J,j,1))for J in js]for K in js])
 return bs,C
maxkl=0.;budgetkl=Q(0);seen=set()
for item in data['KL']:
 L,Lp,r=item['L'],item['Lp'],item['r'];assert abs(L-Lp)<=r<=min(L+Lp,n,2*t);yy=rat(item['multiplier']);bs,C=casimir(L,Lp)
 v=[sign(L+j+b['J'])*ball((2*b['J']+1)*(2*r+1)).sqrt()*six(L,j,b['J'],j,Lp,r)for _,b in bs]
 key=(L,Lp,r)
 if key not in seen:
  seen.add(key);lam=r*(r+1)
  assert abs(sum((x*x for x in v),arb(0))-1)<ball(Q(1,10**50))
  for p in range(len(bs)):
   defect=sum((C[p,q]*v[q]for q in range(len(bs))),arb(0))-lam*v[p]
   assert abs(defect)<ball(Q(1,10**50)),('KL eigenvector',key,p,str(defect));maxkl=max(maxkl,float(abs(defect).upper()))
 # Gap to rank 2t+1 at least (2t+1)(2t+2)-r(r+1).
 # Coarse sqrt dimension<=N, ||(2Swap-I)Z||<=3TrZ=24.
 budgetkl+=abs(yy)*Q(24*N,10**50*((2*t+1)*(2*t+2)-r*(r+1)))
 for (_,b),vv in zip(bs,v):
  d=len(b['ls']);p=b['ls'].index(L);q=b['ls'].index(Lp);E=zmat(d);E[q,p]=1
  b['dual']-=ball(yy)*vv/ball(2*b['J']+1).sqrt()*symmetric(E*(2*b['swap13']-b['I']))
eps=Q(1,10**8);maxres=0.
for J2,b in blocks.items():
 D=symmetric(b['dual']);D=sum((g*D*g.transpose()for g in b['G']),zmat(len(b['ls'])))/6;D=b['support']*D*b['support']
 for p in range(D.nrows()):
  for q in range(D.ncols()):assert abs(D[p,q])<ball(eps),('dual moment residual',J2,p,q,str(D[p,q]));maxres=max(maxres,float(abs(D[p,q]).upper()))
for k,v in enumerate(a):assert abs(v)<ball(eps),('enumerator residual',k,str(v))
budget=(Q(N,2)+8*N)*eps;assert budgetkl<Q(1,10**35)and constant+budget+budgetkl<0
out={'passed':True,'n':n,'t':t,'certificate_sha256':hashlib.sha256(raw).hexdigest(),'constant_exact':str(constant),'main_residual_budget':str(budget),'extra_KL_defect_bound':str(budgetkl),'extra_KL_defect_less_than':'1e-35','strict_upper_using_coarse_KL_bound':str(constant+budget+Q(1,10**35)),'KL_vectors_checked':len(seen),'diagnostic_max_KL_eigenresidual':maxkl,'diagnostic_max_moment_residual':maxres,'diagnostic_max_enum_residual':max(float(abs(v).upper())for v in a),'seconds':time.time()-st,'arithmetic':'Independent SymPy exact6j to256bit Arb; declarative full-space collection; no worker imports','scope':'Finite necessary relaxation exclusion, conditional only on audited representation-theoretic identities, not novelty.'}
Path(__file__).with_name(f'quantum_general_n{n}_t{t}_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
