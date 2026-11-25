"""Exact nonzero chain-overlap certificate; no full dense atom allocation."""
from fractions import Fraction as F
import json


def dot(x,y):return sum(a*b for a,b in zip(x,y))
def chain(L,c,s):
 n=2**(L+1);active=[[F(i==j) for j in range(n)] for i in range(n)];detail=[];bases=[]
 for ell in range(L):
  nxt=[];ds=[]
  for i in range(len(active)//2):
   x,y=active[2*i:2*i+2];nxt.append([c*a+s*b for a,b in zip(x,y)]);ds.append([-s*a+c*b for a,b in zip(x,y)])
  detail.append(ds[0]);bases.append(nxt[0]);active=nxt
 waves=detail+[active[0]]
 assert all(dot(x,y)==F(i==j) for i,x in enumerate(waves) for j,y in enumerate(waves))
 nonzeros=[]
 for i in range(L):
  for j in range(i+1,L+1):
   val=dot(bases[i],waves[j]);assert val!=0;nonzeros.append(str(val))
 return nonzeros


def main():
 rows=[]
 for L in range(1,7):
  left=chain(L,F(3,5),F(4,5));right=chain(L,F(5,13),F(12,13))
  rows.append(dict(L=L,biclique_part_size=L+1,envelope_positions=(L+1)**2,required_star_colors_at_least=L+2,left_overlaps=left,right_overlaps=right))
 r=dict(status='EXACT_FRACTION_PASS',results=rows);print(json.dumps(r,indent=2));open('dense_envelope_clique_results.json','w').write(json.dumps(r,indent=2)+'\n')

if __name__=='__main__':main()
