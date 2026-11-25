"""Exact rational coherent-return obstruction to a UNIFORM conditional gate.
Pure scalar ad source; opposite-bank full-complement rotations fixed at I.
No claim against the unconditional scalar theorem or arbitrary algorithms.
"""
from fractions import Fraction as F
import json

def angles(m):
 points=[]
 for j in range(m+1):
  a,b=m-j,j;den=a*a+b*b;points.append((F(a*a-b*b,den),F(2*a*b,den)))
 out=[]
 for (c,s),(C,S) in zip(points,points[1:]):out.append((c*C+s*S,c*S-s*C))
 return out

def main():
 rows=[];d=2
 for m in [8,16,32,64,128]:
  rho=F(1);cc,ss=F(1),F(0)
  for r,t in angles(m):
   assert r*r+t*t==1 and r>0 and 1-r<=F(8,m*m)
   rho*=r;cc,ss=cc*r-ss*t,ss*r+cc*t
  assert (cc,ss)==(-1,0)
  assert rho>=1-F(8,m)
  q=rho*rho;U,A=F(1),F(0);cost=F(1)
  for cyc in range(m):
   cost+=(1+rho)**2*A
   Up=(1-F(1,d))*U+A;An=U/d
   cost+=(1-q)*An+(1-q)*Up/d
   U,A=q*Up,An
  inf=1+F(2,d)+(1+rho)/(d*(1-rho))
  assert cost<inf
  if m>8:assert inf>=1+F(2,d)+F(m-4,4*d)
  rows.append(dict(m=m,cycles=m,ancestor_steps=m*(m+1),rho=float(rho),finite_source_included_mean=float(cost),infinite_mean=float(inf),rho_fraction=str(rho),certified_finite_integer_lower_bound=cost.numerator//cost.denominator,finite_numerator_bits=cost.numerator.bit_length(),finite_denominator_bits=cost.denominator.bit_length()))
 report=dict(status='EXACT_FRACTION_PASS',d=d,width=3,conditioned_opposite_bank='H=I at every boundary',pi_rotation_exact=True,cycle_recurrence_exact=True,uniform_conditional_bound='REFUTED',scope='Uniform one-bank-conditioned pure-source claim only; not unconditional reconstruction risk',rows=rows)
 # Large exact certificates kept in JSON, not stdout.
 open('one_bank_conditional_obstruction_results.json','w').write(json.dumps(report,indent=2)+'\n')
 print(json.dumps({**report,'rows':[{k:v for k,v in row.items() if not k.endswith('_fraction')} for row in rows]},indent=2))
if __name__=='__main__':main()
