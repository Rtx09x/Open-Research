"""Independent stdlib-only Q(i) replay of quantum export and endpoint syzygies."""
from fractions import Fraction as F
from pathlib import Path
from math import comb
from collections import Counter
import json,hashlib,time
start=time.time();Z=(F(0),F(0));ONE=(F(1),F(0));I=(F(0),F(1))
def add(x,y):return(x[0]+y[0],x[1]+y[1])
def neg(x):return(-x[0],-x[1])
def mul(x,y):return(x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def cj(x):return(x[0],-x[1])
def div(x,y):
 d=y[0]*y[0]+y[1]*y[1];v=mul(x,cj(y));return(v[0]/d,v[1]/d)
def smul(A,c):return{k:mul(v,c)for k,v in A.items()if mul(v,c)!=Z}
def madd(*As):
 C={}
 for A in As:
  for k,v in A.items():C[k]=add(C.get(k,Z),v)
 return{k:v for k,v in C.items()if v!=Z}
def mm(A,B):
 rows={}
 for(k,j),v in B.items():rows.setdefault(k,[]).append((j,v))
 C={}
 for(i,k),v in A.items():
  for j,w in rows.get(k,[]):C[i,j]=add(C.get((i,j),Z),mul(v,w))
 return{k:v for k,v in C.items()if v!=Z}
def comm(A,B):return madd(mm(A,B),smul(mm(B,A),(-1,0)))
def trace(A,n=19):
 r=Z
 for i in range(n):r=add(r,A.get((i,i),Z))
 return r
def weighted_adjoint(A,weights):return{(j,i):mul(cj(v),(weights[i]/weights[j],0))for(i,j),v in A.items()}
source=Path(__file__).resolve().parents[2]/'symmetric-quantum-codes'/'phase2'/'exact_moment_coefficients.json'
raw=source.read_bytes();D=json.loads(raw);assert D['n']==18 and D['dimension']==19
B=[{(i,j):(F(r),F(im))for i,j,r,im in a['entries']}for a in D['basis']]
assert len(B)==36 and Counter(a['rank']for a in D['basis'])=={r:2*r+1 for r in range(6)}
Jp={(w+1,w):(F(18-w),F(0))for w in range(18)};Jm={(w,w+1):(F(w+1),F(0))for w in range(18)}
Jz={(w,w):(F(w-9),F(0))for w in range(19)if w!=9}
Js=[smul(madd(Jp,Jm),(F(1,2),0)),smul(madd(Jp,smul(Jm,(-1,0))),(0,F(-1,2))),Jz]
weights=[F(1,comb(18,w))for w in range(19)]
assert weighted_adjoint(Jp,weights)==Jm
assert comm(Js[0],Js[1])==smul(Js[2],I)
assert madd(*(mm(J,J)for J in Js))=={(w,w):(F(90),F(0))for w in range(19)}
# Rebuild the harmonic matrices independently from ladder powers/commutators.
rebuilt={(0,0,'scalar'):{(w,w):ONE for w in range(19)}}
for r in range(1,6):
 T={(w,w):ONE for w in range(19)}
 for _ in range(r):T=mm(T,Jp)
 for q in range(r,-1,-1):
  if q:
   U=weighted_adjoint(T,weights)
   rebuilt[r,q,'real']=smul(madd(T,U),(F(1,2),0))
   rebuilt[r,q,'imag']=smul(madd(T,smul(U,(-1,0))),(0,F(-1,2)))
  else:rebuilt[r,q,'real']=T
  T=comm(Jm,T)
for k,(A,meta)in enumerate(zip(B,D['basis'])):
 assert A==rebuilt[meta['rank'],meta['q'],meta['part']]
 assert A==weighted_adjoint(A,weights)
 norm=trace(mm(A,A));assert norm==(F(meta['HS_norm_squared']),F(0)) and norm[0]>0
 for j in range(k):assert trace(mm(A,B[j]))==Z
checks=0
for records,middle in [(D['gram'],None)]+list(zip(D['K_xyz'],Js)):
 assert {(r['a'],r['b'])for r in records}=={(a,b)for a in range(9)for b in range(9)}
 for row in records:
  actual=mm(B[row['a']],B[row['b']])if middle is None else mm(mm(B[row['a']],middle),B[row['b']])
  expected=madd(*(smul(B[k],(F(r),F(im)))for k,r,im in row['coefficients']))
  assert actual==expected;checks+=1
  if middle is None:assert all(D['basis'][k]['rank']<=4 for k,r,im in row['coefficients'])
# Integer derivative and multiplication operators: common sector normalization
# does not change their coefficient syzygies.
a={(w-1,w):(F(w),F(0))for w in range(1,19)}
b={(w,w):(F(18-w),F(0))for w in range(18)}
ac={(w+1,w):ONE for w in range(19)};bc={(w,w):ONE for w in range(19)}
R0=[mm(op,E)for op in (b,a)for E in B[:9]]
R19=[mm(op,E)for op in (ac,smul(bc,(-1,0)))for E in B[:9]]
def kernels(rows):
 pivots={};ker=[]
 for i,row in enumerate(rows):
  v=dict(row);coef={i:ONE}
  while v:
   k=min(v);f=v[k]
   if k not in pivots:
    v={h:div(x,f)for h,x in v.items()};coef={h:div(x,f)for h,x in coef.items()};pivots[k]=(v,coef);break
   old,c=pivots[k]
   for h,x in old.items():
    v[h]=add(v.get(h,Z),neg(mul(f,x)))
    if v[h]==Z:del v[h]
   for h,x in c.items():
    coef[h]=add(coef.get(h,Z),neg(mul(f,x)))
    if coef[h]==Z:del coef[h]
  else:ker.append(coef)
 return len(pivots),ker
rank0,U=kernels(R0);rank19,V=kernels(R19);assert rank0==rank19==12 and len(U)==len(V)==6
for rows,K in ((R0,U),(R19,V)):
 for u in K:assert not madd(*(smul(rows[i],v)for i,v in u.items()))
# Universal G-metric orthogonality as a physical operator identity.
G={(a,b):mm(B[a],B[b])for a in range(9)for b in range(9)}
for u in U:
 for v in V:
  ans=madd(*(smul(G[a%9,b%9],mul(cj(x),y))for a,x in u.items()for b,y in v.items()if a//9==b//9))
  assert not ans
# Disjointness follows already by metric positivity, check rank directly too.
combined=[{(0,k):v for k,v in u.items()}for u in U+V];assert kernels(combined)[0]==12
encode=lambda K:[[[k,str(v[0]),str(v[1])]for k,v in sorted(u.items())]for u in K]
out={'status':'PASS','source_sha256':hashlib.sha256(raw).hexdigest(),'basis_count':36,'exact_product_expansions':checks,'annihilation_span_rank':rank0,'creation_span_rank':rank19,'coefficient_kernel_dimensions':[len(U),len(V)],'combined_kernel_rank':12,'operator_metric_orthogonality_checks':36,'annihilation_kernel':encode(U),'creation_kernel':encode(V),'seconds':time.time()-start,'scope':'exact export and universal syzygies; no code feasibility claim'}
Path(__file__).with_name('rational_moment_export_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items()if not k.endswith('_kernel')},indent=2))
