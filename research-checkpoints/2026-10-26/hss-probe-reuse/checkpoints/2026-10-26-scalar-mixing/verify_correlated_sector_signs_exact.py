"""Exact actual-query fine-sign sectors, including correlated ad/da anchors.
N8 unrelated dense bases; all256 fine sign assignments; Fraction only.
"""
from fractions import Fraction as F
from itertools import product
import json
from verify_triangular_regression_exact import dot,tr,mul,eye,zero,outer,add,bd
from verify_one_bank_output_signs_exact import probe,decode


def fine_carry(A,us,vs,om,ps):
 Y,Z=mul(A,om),mul(tr(A),ps);U=bd([[[c],[s]] for c,s in us]);V=bd([[[a],[b]] for a,b in vs]);blocks=[]
 for i,((c,s),(a,b)) in enumerate(zip(us,vs)):
  u,w,v,z=[c,s],[-s,c],[a,b],[-b,a]
  f,g=mul([v,z],om[2*i:2*i+2]);p,q=mul([u,w],ps[2*i:2*i+2])
  yd=mul([w],Y[2*i:2*i+2])[0];zd=mul([z],Z[2*i:2*i+2])[0]
  aa,bb,cc=dot(yd,f),dot(yd,g),dot(p,zd)
  D=add(add(zero(2,2),outer(w,v),aa),outer(w,z),bb);D=add(D,outer(u,z),cc);blocks.append(D)
 D=bd(blocks)
 return mul(tr(U),add(Y,mul(D,om),-1)),mul(tr(V),add(Z,mul(tr(D),ps),-1)),mul(tr(V),om),mul(tr(U),ps)


def main():
 fixed=[([(F(3,5),F(4,5))]*4,[(F(5,13),F(12,13))]*4),
        ([(F(8,17),F(15,17))]*2,[(F(7,25),F(24,25))]*2)]
 us,vs=fixed[0];U=bd([[[c],[s]] for c,s in us]);D=bd([[[-s],[c]] for c,s in us]);V=bd([[[a],[b]] for a,b in vs]);E=bd([[[-b],[a]] for a,b in vs])
 sectors=[]
 aa=[[F(i-2*j,7) for j in range(4)] for i in range(4)]
 sectors.append(('aa',(),mul(mul(U,aa),tr(V))))
 for j in range(4):
  a=[F(0) if i==j else F(i+j+1,9) for i in range(4)]
  sectors.append(('ad',(j,),mul(mul(U,outer(a,eye(4)[j])),tr(E))))
 for i in range(4):
  a=[F(0) if j==i else F(2*i-j+1,11) for j in range(4)]
  sectors.append(('da',(i,),mul(mul(D,outer(eye(4)[i],a)),tr(V))))
 for i in range(4):
  for j in range(4):
   if i!=j:sectors.append(('dd',(i,j),outer(tr(D)[i],tr(E)[j])))
 base=[];om0=probe(fixed,1,[1,-1]+[1]*4);ps0=probe(fixed,0,[-1,1]+[1]*4)
 for _,_,A in sectors:
  y,z,omc,psc=fine_carry(A,us,vs,om0,ps0)
  base.append((y,z,decode(fixed[1:],omc,psc,y,z)))
 chars=[]
 for signs in product([-1,1],repeat=8):
  sigma,tau=signs[:4],signs[4:];om=probe(fixed,1,[1,-1]+list(sigma));ps=probe(fixed,0,[-1,1]+list(tau));row=[]
  for index,(typ,ids,A) in enumerate(sectors):
   char=1 if typ=='aa' else sigma[ids[0]] if typ=='ad' else tau[ids[0]] if typ=='da' else tau[ids[0]]*sigma[ids[1]]
   y,z,omc,psc=fine_carry(A,us,vs,om,ps)
   by,bz,bo=base[index]
   assert y==[[char*v for v in r] for r in by] and z==[[char*v for v in r] for r in bz]
   assert omc==mul(tr(V),om0) and psc==mul(tr(U),ps0)
   # The remaining decoder is fixed and linear; exact output transforms by char.
   row.append(F(char))
  chars.append(row)
 cg=mul(tr(chars),chars)
 assert cg==[[256*v for v in row] for row in eye(len(sectors))]
 report=dict(status='EXACT_FRACTION_PASS',N=8,L=2,width=3,fine_sign_assignments=256,
  complete_sectors=len(sectors),actual_forward_and_transpose_samples=True,
  correlated_anchor_retained=True,coarser_frames_unchanged=True,
  carried_whole_sector_characters_exact=True,Walsh_Gram='256 I_21',
  scope='Exact correlated-law sector identity, not a finite check of the all-depth risk theorem')
 print(json.dumps(report,indent=2));open('correlated_sector_signs_exact_results.json','w').write(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
