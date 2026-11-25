"""Reproduce AAB24's 19-qubit root as an exact rational-box certificate.
No decimal residual is accepted as exact. The code is defined by the unique
real root of nine rational quadratics inside the certified rational box.
"""
from pathlib import Path
import json, math
import sympy as s
ROOT=Path(__file__).parent

def pr_equations(n=19,t=2):
 q=s.symbols('q0:'+str((n+1)//2));qv=lambda j:q[j//2]
 end=(n-1)//2-t
 F=[]
 for a in range(0,2*t+1,2):
  for b in range(1,2*t+1,2):
   F.append(sum(s.binomial(n-2*t,2*k)*qv(2*k+a)*qv(n-2*k-b) for k in range(end+1)))
 for parity in (0,1):
  for a in range(parity,2*t+1,2):
   for b in range(a,2*t+1,2):
    if a+b>=2*t:continue
    if parity==0:
     f=sum(s.binomial(n-2*t,2*k)*(qv(2*k+a)*qv(2*k+b)-qv(2*k+2*t-a)*qv(2*k+2*t-b)) for k in range(end+1))
    else:
     f=sum(s.binomial(n-2*t,2*k)*(qv(n-2*k-a)*qv(n-2*k-b)-qv(n-2*k-2*t+a)*qv(n-2*k-2*t+b)) for k in range(end+1))
    F.append(f)
 return q,[s.expand(f) for f in F]

def certify():
 q,F=pr_equations();variables=q[1:];F=s.Matrix([f.subs(q[0],1) for f in F]);J=F.jacobian(variables)
 approx=[.0477572,-.0267249,-.00506367,.00332914,.00527235,-.000947223,.0152707,.00888631,.32678]
 root=s.nsolve(F,variables,approx,prec=90,tol=s.Rational(1,10**85),maxsteps=100)
 c=s.Matrix([s.Rational(str(v.evalf(65))) for v in root]);sub=dict(zip(variables,c));B=J.subs(sub).inv();fc=F.subs(sub)
 eta=max(abs(z) for z in B*fc)
 # J(x)=J(c)+sum_l Hessian_slice_l*(x_l-c_l), exactly, since quadratics.
 BH=[B*J.diff(v) for v in variables]
 L=max(sum(abs(T[i,j]) for T in BH for j in range(len(variables))) for i in range(len(variables)))
 rad=s.Rational(1,10**40)
 assert eta+L*rad**2<rad and L*rad<1
 # Krawczyk maps the box strictly into itself; nonsingular inverse and
 # contraction also certify unique root there.
 out={'n':19,'d':5,'q0':'1','variables':[str(v) for v in variables], 'equations':[str(f) for f in F], 'center':[str(z) for z in c], 'radius':str(rad), 'eta':str(eta),'L':str(L),'eta_float':str(eta.evalf(8)),'contraction_float':str((L*rad).evalf(8)),'existence_test':True,'uniqueness_test':True}
 (ROOT/'code19_root_certificate.json').write_text(json.dumps(out,indent=2))
 print('Root box certified:',out['eta_float'],out['contraction_float'],flush=True)
 return q,pr_equations()[1]

def exact_reduction_check(q,F):
 """Verify all four-qubit reduced Gram KL polynomials lie in PR equation span."""
 n=19;m=4
 coeff0=[q[w//2] if w%2==0 else 0 for w in range(n+1)]
 coeff1=list(reversed(coeff0))
 # Removing nonzero sqrt(C4i C4j), each equality is quadratic over Q.
 req=[]
 for i in range(m+1):
  for j in range(m+1):
   req.append(s.expand(sum(s.binomial(n-m,k)*(coeff0[k+i]*coeff0[k+j]-coeff1[k+i]*coeff1[k+j]) for k in range(n-m+1))))
   req.append(s.expand(sum(s.binomial(n-m,k)*coeff0[k+i]*coeff1[k+j] for k in range(n-m+1))))
 mon=[q[i]*q[j] for i in range(len(q)) for j in range(i,len(q))]
 mat=s.Matrix([[f.coeff(x) for x in mon] for f in F]).T
 certificates=[]
 for f in req:
  col=s.Matrix([f.coeff(x) for x in mon]);coef,params=mat.gauss_jordan_solve(col)
  assert params.rows==0
  assert s.expand(sum(a*b for a,b in zip(coef,F))-f)==0
  certificates.append([str(v) for v in coef])
 (ROOT/'code19_kl_reduction.json').write_text(json.dumps({'count':len(req),'all_exact':True,'coefficients':certificates},indent=2))
 print('All',len(req),'four-qubit reduced-Gram KL polynomials exactly in equation span.',flush=True)

if __name__=='__main__':
 q,F=certify();exact_reduction_check(q,F)
