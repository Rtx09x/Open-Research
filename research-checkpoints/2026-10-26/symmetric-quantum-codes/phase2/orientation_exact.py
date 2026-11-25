"""Exact rational checks of the orientation polynomial; no numerical rank tests."""
import json,random
from pathlib import Path
import sympy as s
I=s.I
pauli=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-I],[I,0]]),s.diag(1,-1)]
t,a,b,c=s.symbols('t a b c', real=True)
lhs=s.prod([t-a-b-c,t-a+b+c,t+a-b+c,t+a+b-c])/16
q=a*a+b*b+c*c
rhs=(t**4-2*t*t*q-8*t*a*b*c+2*(a**4+b**4+c**4)-q*q)/16
assert s.expand(lhs-rhs)==0
rng=random.Random(20261025);rows=[]
for d in [1,2,3,5]:
 X=s.Matrix(2*d,2,lambda i,j:s.Integer(rng.randrange(-3,4))+I*rng.randrange(-3,4));S=X*X.conjugate().T
 Bs=[s.kronecker_product(p,s.eye(d)) for p in pauli];tt=s.trace(S)
 H=s.Matrix(3,3,lambda i,j:2*s.trace(S*Bs[i]*S*Bs[j])-s.trace(S*Bs[i])*s.trace(S*Bs[j]))
 delta=2*I*s.trace(S*Bs[0]*S*Bs[1]*S*Bs[2]-S*Bs[0]*S*Bs[2]*S*Bs[1])
 inv=s.expand((tt**4-2*tt**2*s.trace(H)-8*tt*delta+2*s.trace(H*H)-s.trace(H)**2)/16)
 Zc=s.zeros(d,4)
 for k in range(d):
  M=s.Matrix([list(X[k,:]),list(X[d+k,:])]);Zc[k,0]=s.trace(M)
  for j in range(3):Zc[k,j+1]=I*s.trace(M*pauli[j])
 Z=Zc.applyfunc(s.re).col_join(Zc.applyfunc(s.im));actual=(Z.T*Z).det()
 assert s.expand(inv-actual)==0
 rows.append({'d':d,'determinant':str(actual),'matches':True})
Path(__file__).with_suffix('.json').write_text(json.dumps({'symbolic_signed_diagonal_identity':True,'exact_factor_tests':rows},indent=2));print(rows)
