"""Exact physical ad-sector anchor versus strict-ancestor inverse column."""
from fractions import Fraction as F
import json
from verify_triangular_regression_exact import dot,tr,mul,eye,zero,outer,add,bd
from verify_wide_inverse_branch_exact import atoms
from verify_one_bank_output_signs_exact import probe,decode


def main():
 fixed=[([(F(3,5),F(4,5))]*4,[(F(5,13),F(12,13))]*4),
        ([(F(8,17),F(15,17))]*2,[(F(7,25),F(24,25))]*2)]
 le,ri,typ=atoms(fixed);us,vs=fixed[0]
 U=bd([[[c],[s]] for c,s in us]);V=bd([[[a],[b]] for a,b in vs]);Wv=bd([[[-b],[a]] for a,b in vs])
 count=0
 for signrow,signcol in [([1,-1,-1,1,1,-1],[-1,1,1,1,-1,1]),([-1]*6,[1]*6)]:
  om,ps=probe(fixed,1,signcol),probe(fixed,0,signrow);omc,psc=mul(tr(V),om),mul(tr(U),ps)
  ro,lp=mul(ri,om),mul(le,ps)
  T=[[dot(le[i],le[j])*dot(ro[i],ro[j]) if typ[i]=='F' else dot(ri[i],ri[j])*dot(lp[i],lp[j]) for j in range(22)] for i in range(22)]
  for j in range(4):
   x=[];source=3*j+2
   for i in range(22):x.append((F(i==source)-sum(T[i][h]*x[h] for h in range(i)))/T[i][i])
   gj=mul([tr(Wv)[j]],om)[0]
   pure=decode(fixed[1:],omc,psc,outer(eye(4)[j],[-v for v in gj]),zero(4,3))
   assert x[12:]==pure and x[:12]==[F(i==source) for i in range(12)]
   a=[F(0) if i==j else F(i+j+1,7) for i in range(4)];Bj=dot(psc[j],mul([a],psc)[0])
   A=mul(mul(U,outer(a,eye(4)[j])),tr(Wv))
   actual=decode(fixed,om,ps,mul(A,om),mul(tr(A),ps))
   first=decode(fixed[1:],omc,psc,outer(a,gj),zero(4,3))
   expected=[Bj*F(i==source) for i in range(12)]+[f+Bj*v for f,v in zip(first,pure)]
   assert actual==expected;count+=1
 report=dict(status='EXACT_FRACTION_PASS',N=8,L=2,width=3,complete_ad_columns=count,
  original_sample_inverse_column_equals_pure_anchor=True,
  whole_physical_sector_equals_first_source_plus_correlated_anchor=True,
  scope='Finite identity controls; no independence between anchor amplitude and inverse column assumed')
 print(json.dumps(report,indent=2));open('anchor_inverse_identity_exact_results.json','w').write(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
