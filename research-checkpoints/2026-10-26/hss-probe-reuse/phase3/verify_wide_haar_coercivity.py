"""Exact integer witness for failure of uniform wider-Haar coercivity.
No random simulation and no dense exponentially sized allocation.
"""
import json
from fractions import Fraction


def main():
 rows=[]
 for L in range(1,21):
  n=2**(L+1);path=[0]
  for bit in range(L,-1,-1):path.append(path[-1]+2**bit)
  product={i:[0,0] for i in path}
  for j,(u,v) in enumerate(zip(path,path[1:]),1):
   assert v&(v-1)==u
   assert u.bit_count()%2 != v.bit_count()%2
   val=(-1)**j
   product[u][v.bit_count()%2]+=val
   product[v][u.bit_count()%2]+=val
  assert all(product[v]==[0,0] for v in path[1:-1])
  onebank=sum(x*x for r in product.values() for x in r)
  assert onebank==2
  norm2=2*(L+1);quot=Fraction(2*onebank,norm2)
  assert quot==Fraction(2,L+1)
  rows.append(dict(L=L,N=n,edge_count=L+1,matrix_norm_squared=norm2,
                   two_bank_measurement_energy=2*onebank,exact_quotient=str(quot)))
 report=dict(status='PASS',arithmetic='integer and rational',
             scope='realization-uniform coercivity only',results=rows)
 with open('wide_haar_coercivity_results.json','w') as f:json.dump(report,f,indent=2)
 print(json.dumps(report,indent=2))


if __name__=='__main__':main()
