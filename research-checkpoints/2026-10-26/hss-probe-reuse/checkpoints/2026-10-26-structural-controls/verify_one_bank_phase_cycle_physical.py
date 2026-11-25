"""Fraction full (x,z,w0,w1) moment system vs claimed two-state phase cycle.
Independently retains covariance and all output terms, not just U,A update.
"""
from fractions import Fraction as F
import json
from verify_triangular_regression_exact import mul,tr,add,outer,zero
from verify_one_bank_conditional_obstruction import angles

def step(C,U,r,t,a,b):
 B=[[r*a,F(0),F(0),F(0)],[F(0),r*a,-a*t,F(0)],[-a*t,a*t,a*r,F(0)],[F(0),F(0),F(0),a]]
 h=[-r*b,F(0),t*b,F(0)];ell=[r,-r,t,F(0)];ad=[F(0),r,-t,F(0)]
 def quad(v):return mul(mul([v],C),tr([v]))[0][0]
 cost=t*t*C[0][0]+t*t*U/2+b*b*quad(ad)
 Cp=add(mul(mul(B,C),tr(B)),[[U*x/2 for x in row] for row in outer(h,h)])
 Up=r*r*(1-b*b/2)*U+b*b*quad(ell)
 return Cp,Up,cost

def main():
 results=[]
 for m in [4,8,16,32]:
  seq=angles(m);rho=F(1)
  for r,t in seq:rho*=r
  q=rho*rho;U,A=F(3,5),F(2,7);v=[-rho,-rho-1,F(0),F(0)];C=[[A*x for x in row] for row in outer(v,v)]
  cost=F(0)
  for r,t,a,b in [(F(1),F(0),F(0),F(1))]+[(r,t,F(1),F(0)) for r,t in seq]:C,U,c=step(C,U,r,t,a,b);cost+=c
  Up=(1-F(1,2))*F(3,5)+F(2,7);An=F(3,10)
  expected_C=[[An*x for x in row] for row in outer(v,v)]
  expected_cost=(1+rho)**2*F(2,7)+(1-q)*An+(1-q)*Up/2
  assert C==expected_C and U==q*Up and cost==expected_cost
  results.append(dict(m=m,full_covariance_and_unused_passive=True,exact_cycle=True,cost=float(cost)))
 report=dict(status='EXACT_FRACTION_PASS',width=3,checks=results,scope='Full conditional moment cycle identity, not an unconditional algorithm lower bound')
 print(json.dumps(report,indent=2));open('one_bank_phase_cycle_physical_results.json','w').write(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
