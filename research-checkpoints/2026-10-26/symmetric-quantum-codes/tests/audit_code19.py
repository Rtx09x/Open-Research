"""Independent exact known19 replay: stdlib Fraction, AST polynomials, no SymPy."""
import ast,json,math,time
from fractions import Fraction as F
from pathlib import Path
start=time.time(); ROOT=Path(__file__).resolve().parents[1]
d=json.loads((ROOT/'code19_root_certificate.json').read_text()); reduction=json.loads((ROOT/'code19_kl_reduction.json').read_text())
def add(p,q):
 out=p.copy()
 for m,c in q.items():out[m]=out.get(m,F(0))+c
 return {m:c for m,c in out.items() if c}
def mul(p,q):
 out={}
 for m,c in p.items():
  for n,e in q.items():
   z=tuple(sorted(m+n));out[z]=out.get(z,F(0))+c*e
 return {m:c for m,c in out.items()if c}
def parse(a):
 if isinstance(a,ast.Expression):return parse(a.body)
 if isinstance(a,ast.Constant):return {():F(a.value)}
 if isinstance(a,ast.Name):return {(int(a.id[1:]),):F(1)}
 if isinstance(a,ast.UnaryOp) and isinstance(a.op,ast.USub):return {m:-c for m,c in parse(a.operand).items()}
 if isinstance(a,ast.BinOp):
  p=parse(a.left)
  if isinstance(a.op,ast.Pow):
   assert isinstance(a.right,ast.Constant) and a.right.value==2
   return mul(p,p)
  q=parse(a.right)
  if isinstance(a.op,ast.Add):return add(p,q)
  if isinstance(a.op,ast.Sub):return add(p,{m:-c for m,c in q.items()})
  if isinstance(a.op,ast.Mult):return mul(p,q)
 raise AssertionError(ast.dump(a))
polys=[]
for f in d['equations']:
 p=parse(ast.parse(f,mode='eval'));assert all(len(m)<=2 for m in p)
 polys.append({tuple(sorted((0,)*(2-len(m))+m)):c for m,c in p.items()})
c=[F(1)]+list(map(F,d['center']));r=F(d['radius']);dim=9
fc=[sum((a*c[i]*c[j]for (i,j),a in p.items()),F(0)) for p in polys]
J=[[F(0)]*dim for _ in polys];HH=[[[F(0)]*dim for _ in range(dim)]for _ in polys]
for row,p in enumerate(polys):
 for (i,j),a in p.items():
  if i:J[row][i-1]+=a*c[j]
  if j:J[row][j-1]+=a*c[i]
  if i and j:HH[row][i-1][j-1]+=a;HH[row][j-1][i-1]+=a
A=[row+[F(i==j) for j in range(dim)]for i,row in enumerate(J)]
for col in range(dim):
 pivot=next(i for i in range(col,dim)if A[i][col]);A[col],A[pivot]=A[pivot],A[col]
 den=A[col][col];A[col]=[v/den for v in A[col]]
 for i in range(dim):
  if i!=col:
   z=A[i][col];A[i]=[v-z*w for v,w in zip(A[i],A[col])]
B=[row[dim:]for row in A]
assert all(sum(B[i][k]*J[k][j]for k in range(dim))==int(i==j)for i in range(dim)for j in range(dim))
eta=max(abs(sum(B[i][j]*fc[j] for j in range(dim)))for i in range(dim))
L=max(sum(abs(sum(B[i][p]*HH[p][ell][j]for p in range(dim)))for ell in range(dim)for j in range(dim))for i in range(dim))
assert eta==F(d['eta']) and L==F(d['L'])
assert eta+L*r*r<r and L*r<1
# Rebuild all25 reduced-density differences and25 cross reductions.
def qindex(logical,w):
 if logical:w=19-w
 return w//2 if w%2==0 else None
req=[]
for i in range(5):
 for j in range(5):
  for cross in (False,True):
   p={}
   pairs=[(0,1,1)]if cross else[(0,0,1),(1,1,-1)]
   for left,right,sgn in pairs:
    for k in range(16):
     x=qindex(left,k+i);y=qindex(right,k+j)
     if x is not None and y is not None:p=add(p,{tuple(sorted((x,y))):F(sgn*math.comb(15,k))})
   req.append(p)
assert len(req)==reduction['count']==50
for p,co in zip(req,reduction['coefficients']):
 total={}
 for a,g in zip(map(F,co),polys):total=add(total,{m:a*v for m,v in g.items()})
 assert total==p
out={'exact':True,'method':'independent stdlib rational polynomial/Jacobian/Hessian and reduced-Gram reconstruction','root_contraction':True,'all_50_KL_reductions':True,'eta_matches':True,'L_matches':True,'eta_float':float(eta),'L_times_radius_float':float(L*r),'seconds':time.time()-start,'scope':'replication of known19 positive control, not new code'}
Path(__file__).with_name('code19_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
