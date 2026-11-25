"""Independent full-space dual verification.
Uses candidate integer data only. No worker code, floating point solver,
eigensolver, S3 basis, rank selection, or primary factorial-6j implementation.
Symbolic SymPy 6j values are converted by exact rational sign/square to Arb.
Cone assembly uses a declarative primal-cone table and separate pair weights.
"""
import json,time,hashlib
from pathlib import Path
from fractions import Fraction as Q
from functools import lru_cache
import sympy as sp
from sympy.physics.wigner import wigner_6j
from flint import arb,arb_mat,fmpq,ctx
ctx.prec=256
ROOT=Path(__file__).parent;FILE=Path(__file__).resolve().parents[1]/'symmetric-quantum-codes'/'phase2'/'interval_dual_candidate.json';raw=FILE.read_bytes();cert=json.loads(raw);scale=cert['scale'];N=19;j=9

def ball(q):
 q=Q(q);return arb(fmpq(q.numerator,q.denominator))
def rr(v):return Q(int(v),scale)
def mat(values):return arb_mat([[ball(rr(v))for v in row]for row in values])
def zero(d):return arb_mat(d,d)
def ident(d):return arb_mat([[int(a==b)for b in range(d)]for a in range(d)])
def sym(A):return(A+A.transpose())/2
@lru_cache(None)
def six(a,b,c,d,e,f):
 z=wigner_6j(a,b,c,d,e,f)
 if not z:return arb(0)
 q=sp.cancel(z*z);assert q.is_Rational and q>0
 return (-1 if z<0 else 1)*ball(Q(int(q.p),int(q.q))).sqrt()

def gram(item):
 A=mat(item['factor']);return A*A.transpose()
def trace_exact(item):return sum((rr(v)**2 for row in item['factor']for v in row),Q(0))
start=time.time();B={}
for J in range(28):
 ls=[L for L in range(N) if abs(L-j)<=J<=L+j];d=len(ls);I=ident(d)
 S=arb_mat([[ball((2*L+1)*(2*K+1)).sqrt()*six(j,j,L,j,J,K)for K in ls]for L in ls]);T=arb_mat([[(-1)**L if a==b else 0 for b in range(d)]for a,L in enumerate(ls)]);V=T*S*T
 G=[I,T,S,V,T*S,S*T];Ps=sum(G,zero(d))/6;Pa=(I-T-S-V+T*S+S*T)/6
 B[J]=dict(ls=ls,d=d,I=I,S=S,T=T,V=V,G=G,Ps=Ps,Pt=I-Ps-Pa,Q=I-Pa,R=zero(d),PTdual=zero(d))
# Enumerators and pair-spin coefficients are collected separately.
M=[[(-1)**(r+k)*(2*r+1)*six(j,j,r,j,j,k)for k in range(N)]for r in range(N)]
H=[[2*M[r][k]-int(r==k)for k in range(N)]for r in range(N)]
shadow=[[ball(Q(4,N))*(-1)**k*M[L][k]for k in range(N)]for L in range(N)]
pair=[arb(0)for _ in range(N)];pairpt=[arb(0)for _ in range(N)];a=[arb(0)for _ in range(N)];constant=Q(0)
y=[rr(v)for v in cert['equality_dual']];constant=y[0]+Q(19,2)*y[1]
for k in range(N):a[k]-=ball(y[0])*int(k==0)+ball(y[1])+sum((ball(y[r+1])*H[r][k]for r in range(1,5)),arb(0))
it=iter(y[6:])
for L in range(N):
 for sector,ratio in ([('Ps',Q(4,3)),('Pt',Q(2,3))]if L%2==0 else [('Pt',Q(2))]):
  weight=ball(next(it));pair[L]+=weight*ball(ratio)
  for b in B.values():
   if L not in b['ls']:continue
   index=b['ls'].index(L);E=zero(b['d']);E[index,index]=1
   b['R']-=weight*sym(E*b[sector])
try:next(it);raise AssertionError('excess equality data')
except StopIteration:pass
z=cert['enumerator_inequality_dual'];assert len(z)==52 and all(v>=0 for v in z)
for k in range(N):a[k]+=ball(rr(z[k]))
for r in range(5,N):
 for k in range(N):a[k]+=ball(rr(z[N+r-5]))*H[r][k]
for L in range(N):pair[L]+=ball(rr(z[33+L]))
for item in cert['ordinary_PSD']:
 b=B[item['J2']//2];assert item['Ls']==b['ls'];U=mat(item['basis_U']);F=mat(item['factor']);A=U*F;b['R']+=A*A.transpose()
# Entries: constant multiplier; coefficients of D12,Y13,Y23,Z,PT13,PT23,PTZ.
table={
 'PPQ':(Q(0),1,0,0,-1,0,0,0),
 'PQQ':(Q(2,N),-1,-1,0,1,0,0,0),
 'QQQ':(1-Q(6,N),1,1,1,-1,0,0,0),
 'PPT_Z':(Q(0),0,0,0,0,0,0,1),
 'PPT_PPQ':(Q(0),1,0,0,0,0,0,-1),
 'PPT_PQP':(Q(0),0,0,0,0,1,0,-1),
 'PPT_PQQ':(Q(2,N),-1,0,0,0,-1,0,1),
 'PPT_QQP':(Q(2,N),0,0,0,0,-1,-1,1),
 'PPT_QQQ':(1-Q(6,N),1,0,0,0,1,1,-1),
}
for item in cert['cones']:
 J=item['J2']//2;b=B[J];D=zero(b['d']);small=gram(item)
 ix=[b['ls'].index(L)for L in item['Ls']]
 for p,aidx in enumerate(ix):
  for q,bidx in enumerate(ix):D[aidx,bidx]=small[p,q]
 cc,dc,y13c,y23c,zc,p13c,p23c,ptzc=table[item['kind']]
 constant+=cc*trace_exact(item)
 D13=b['S']*D*b['S'];D23=b['V']*D*b['V']
 for t,L in enumerate(b['ls']):
  pair[L]+=(dc*D[t,t]+y13c*D13[t,t]+y23c*D23[t,t])/(2*L+1)
  pairpt[L]+=p13c*D13[t,t]+p23c*D23[t,t]
 b['R']+=zc*D/(2*J+1);b['PTdual']+=ptzc*D
for L in range(N):
 pair[L]+=sum((pairpt[K]*six(j,j,K,j,j,L)for K in range(N)),arb(0))
for k in range(N):a[k]+=sum((pair[L]*shadow[L][k]for L in range(N)),arb(0))
for J,b in B.items():
 for p,L in enumerate(b['ls']):
  for q,Lp in enumerate(b['ls']):
   b['R'][p,q]+=sum((six(L,j,J,Lp,j,K)*c['PTdual'][c['ls'].index(L),c['ls'].index(Lp)]for K,c in B.items()if L in c['ls']and Lp in c['ls']),arb(0))
# The mathematical necessity of these approximate rows is independently
# certified by check_kl_stability.py; a 1e-40 error budget is allowed below.
for item in cert['KL_projected_h']:
 L,Lp=item['L'],item['Lp'];Js=[J2//2 for J2 in item['Js']];h=[ball(rr(v))for v in item['h']];hp=[arb(0)for _ in Js]
 for r in range(abs(L-Lp),min(L+Lp,18,4)+1):
  v=[(-1)**(L+j+J)*ball((2*J+1)*(2*r+1)).sqrt()*six(L,j,J,j,Lp,r)for J in Js]
  alpha=sum((u*w for u,w in zip(v,h)),arb(0))
  for i in range(len(Js)):hp[i]+=v[i]*alpha
 for J,weight in zip(Js,hp):
  b=B[J];p=b['ls'].index(L);q=b['ls'].index(Lp);E=zero(b['d']);E[q,p]=1
  b['R']-=weight/ball(2*J+1).sqrt()*sym(E*(2*b['V']-b['I']))
maxentry=arb(0)
for J,b in B.items():
 R=sum((g*sym(b['R'])*g.transpose()for g in b['G']),zero(b['d']))/6
 R=b['Q']*R*b['Q']
 for p in range(b['d']):
  for q in range(b['d']):assert abs(R[p,q])<ball(Q(1,10**8)),('moment residual',J,p,q,str(R[p,q]))
for k,v in enumerate(a):assert abs(v)<ball(Q(1,10**8)),('enumerator residual',k,str(v))
kl=json.loads((ROOT/'check_kl_stability.json').read_text());assert kl['PASS'] and kl['candidate_sha256']==hashlib.sha256(raw).hexdigest()
residual=Q(19,2*10**8)+Q(8*19,10**8)+Q(1,10**40)
assert constant< -Q(1,10000) and constant+residual<0
out={'PASS':True,'candidate_sha256':hashlib.sha256(raw).hexdigest(),'constant_exact':str(constant),'rigorous_residual_bound_exact':str(residual),'strict_negative_upper_exact':str(-Q(1,10000)+residual),'KL_strategy':'A posteriori exact-Casimir eigenresidual bound, not assumed exact Racah projector','arithmetic':'SymPy exact sign/square 6j + outward Arb 256-bit balls; exact rational PSD Gram factors','worker_code_imports':False,'seconds':time.time()-start,'scope':'Arithmetic certificate plus stated physically necessary model; does not establish literature novelty.'}
(ROOT/'verify_full_certificate_independent.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
