"""Exact total-coefficient wavelet-birth sign cancellation, N8 dense bases.
Does not use a conditional deterministic-RHS norm claim.
"""
from fractions import Fraction as F
from itertools import product
import json
from verify_triangular_regression_exact import dot,tr,mul,eye,zero,outer,add,lin,bd
from verify_wide_inverse_branch_exact import atoms


def probe(fixed,side,signs):
 e=eye(3);inc=[(e[0],[e[1],e[2]]),(e[1],[e[0],e[2]])];at=0
 for pair in reversed(fixed):
  nxt=[]
  for node,(c,s) in enumerate(pair[side]):
   f,base=inc[node];h=[[F(3,5),F(-4,5)],[F(4,5),F(3,5)]]
   comp=mul(h,base);comp=[[signs[at]*v for v in row] for row in comp];at+=1
   g=comp[0];f0,f1=lin(c,-s,f,g),lin(s,c,f,g)
   nxt +=[(f0,[f1,comp[1]]),(f1,[f0,comp[1]])]
  inc=nxt
 return [x[0] for x in inc]


def decode(fixed,om,ps,Y,Z):
 coeff=[]
 for us,vs in fixed:
  U=bd([[[c],[s]] for c,s in us]);V=bd([[[a],[b]] for a,b in vs]);blocks=[]
  for i,((c,s),(a,b)) in enumerate(zip(us,vs)):
   u,w,v,z=[c,s],[-s,c],[a,b],[-b,a]
   f,g=mul([v,z],om[2*i:2*i+2]);p,q=mul([u,w],ps[2*i:2*i+2])
   yd=mul([w],Y[2*i:2*i+2])[0];zd=mul([z],Z[2*i:2*i+2])[0]
   aa,bb,cc=dot(yd,f),dot(yd,g),dot(p,zd);coeff +=[aa,bb,cc]
   D=add(add(zero(2,2),outer(w,v),aa),outer(w,z),bb);D=add(D,outer(u,z),cc);blocks.append(D)
  D=bd(blocks)
  Y,Z=mul(tr(U),add(Y,mul(D,om),-1)),mul(tr(V),add(Z,mul(tr(D),ps),-1))
  om,ps=mul(tr(V),om),mul(tr(U),ps)
 coeff+=sum(mul(Y,tr(om)),[])
 return coeff


def main():
 fixed=[([(F(3,5),F(4,5))]*4,[(F(5,13),F(12,13))]*4),
        ([(F(8,17),F(15,17))]*2,[(F(7,25),F(24,25))]*2)]
 le,ri,_=atoms(fixed);waves=le[:18:3]+[le[18],le[20]]
 assert mul(waves,tr(waves))==eye(8)
 om=probe(fixed,1,[1,-1,1,-1,-1,1]);q=om[0];assert dot(q,q)==1
 gram=zero(8,8)
 for signs in product([-1,1],repeat=6):
  ps=probe(fixed,0,signs)
  outputs=[decode(fixed,om,ps,outer(w,q),zero(8,3)) for w in waves]
  gram=add(gram,mul(outputs,tr(outputs)))
 assert all(gram[i][j]==0 for i in range(8) for j in range(8) if i!=j)
 report=dict(status='EXACT_FRACTION_PASS',N=8,L=2,width=3,row_sign_assignments=64,
  deterministic_wavelet_inputs=8,forward_dependent_unit_q=True,
  expected_total_output_cross_birth_Gram_offdiagonal='exactly zero',
  scope='Sign cancellation only; norm estimate uses unconditional full-Haar inverse-column theorem')
 print(json.dumps(report,indent=2));open('one_bank_output_signs_exact_results.json','w').write(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
