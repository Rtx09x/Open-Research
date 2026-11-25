"""Exact k2 two-step one-bank contraction, with a fixed arbitrary opposite bank.
The32-point orthogonal design has the needed first and second Haar moments.
"""
from fractions import Fraction as F
import json,time
from verify_triangular_regression_exact import mul,tr,eye,zero,add,bd,outer
from verify_matrix_branch_flux_exact import norm,cat,sub,orth,scale

def design():
 signs=[[1,1,1,1],[1,-1,1,-1],[1,1,-1,-1],[1,-1,-1,1]];out=[]
 for sh in range(4):
  for sig in signs:
   for z in [-1,1]:out.append([[F(z*sig[i] if j==(i+sh)%4 else 0) for j in range(4)] for i in range(4)])
 return out

def transfer(seed):
 c=[[F(3,5),F(0)],[F(0),F(4,5)]];s=[[F(4,5),F(0)],[F(0),F(3,5)]]
 core=cat(c,s)+cat(scale(s,-1),c)
 return mul(mul(bd([orth(2,seed),orth(2,seed+1)]),core),bd([orth(2,seed+2),orth(2,seed+3)]))

def parts(Q):return [sub(Q,i,j,2,2) for i,j in [(0,0),(0,2),(2,0),(2,2)]]
def flux(state):X,Z,Y,W=state;return norm(add(X,Z,-1))+norm(Y)+norm(W)
def step(state,ut,vt,O,H,physical=False):
 X,Z,Y,W=state;R,T,Rp,Tp=parts(ut);A,B,Ap,Bp=parts(vt);yo,hw=mul(Y,O),mul(tr(H),W);yb,yh=sub(yo,0,0,2,2),sub(yo,0,2,2,2);wb,wh=hw[:2],hw[2:];D=add(X,Z,-1)
 da=mul(tr(T),add(mul(X,A),mul(yb,Ap)));dd=mul(tr(T),add(mul(X,B),mul(yb,Bp)));ad=mul(add(mul(tr(R),Z),mul(tr(Rp),wb)),B)
 xn=add(mul(mul(tr(R),X),A),mul(mul(tr(R),yb),Ap));zn=add(mul(mul(tr(Rp),wb),A),mul(mul(tr(R),Z),A))
 yn=cat(add(add(mul(mul(tr(R),D),B),mul(mul(tr(R),yb),Bp)),mul(mul(tr(Rp),wb),B),-1),mul(tr(R),yh))
 wn=add(add(scale(mul(mul(tr(T),D),A),-1),mul(mul(tr(Tp),wb),A)),mul(mul(tr(T),yb),Ap),-1)+mul(wh,A)
 new=(xn,zn,yn,wn);loss=flux(state)-flux(new);assert loss>=0
 cost=norm(da)+norm(dd)+norm(ad);J=sum(norm(v) for v in state);assert cost<=J
 if physical:
  F0,G,K=eye(6)[:2],eye(6)[2:4],eye(6)[4:]
  fc=add(mul(A,F0),mul(B,G));pc=add(mul(R,F0),mul(T,G));cc=add(mul(Ap,F0),mul(Bp,G))+K;dc=add(mul(Rp,F0),mul(Tp,G))+K
  yc=add(mul(X,fc),mul(yo,cc));zc=add(mul(tr(Z),pc),mul(mul(tr(W),H),dc))
  assert da==mul(mul(tr(T),yc),tr(F0)) and dd==mul(mul(tr(T),yc),tr(G)) and ad==mul(mul(F0,tr(zc)),B)
  yraw=add(mul(tr(R),yc),mul(ad,G),-1);zraw=add(mul(tr(A),zc),mul(tr(da),G),-1)
  assert mul(yraw,tr(F0))==xn and tr(mul(zraw,tr(F0)))==zn
  assert cat(mul(yraw,tr(G)),mul(yraw,tr(K)))==yn
  assert tr(mul(zraw,tr(G)))+tr(mul(zraw,tr(K)))==wn
 return new,loss

def main():
 start=time.monotonic();group=design();n=len(group)
 assert all(sum(H[i][j] for H in group)==0 for i in range(4) for j in range(4))
 for a in range(4):
  for b in range(4):
   E=zero(4,4);E[a][b]=1;avg=zero(4,4)
   for H in group:avg=add(avg,mul(mul(tr(H),E),H))
   assert avg==scale(eye(4),F(n,4) if a==b else 0)
 U=[transfer(13),transfer(27)];V=[transfer(35),transfer(49)];fixed=[orth(4,161),orth(4,185)];delta=F(3,5);a=delta**2/2;c2=delta**4/2
 for Q in U+V:
  R,T,Rp,Tp=parts(Q)
  for M in [R,T]:
   P=add(mul(tr(M),M),scale(eye(2),delta**2),-1);assert P[0][0]>=0 and P[1][1]>=0 and P[0][0]*P[1][1]-P[0][1]*P[1][0]>=0
 state=([[F(1),F(2,3)],[F(-1,4),F(3,5)]],[[F(-1,3),F(4,7)],[F(2,5),F(1)]],[[F(i*4+j-2,7) for j in range(4)] for i in range(2)],[[F(i*3+j-4,9) for j in range(2)] for i in range(4)])
 H0=flux(state);reports=[]
 for direction in ['forward_fresh','transpose_fresh']:
  firstloss=twoloss=nextpassive=F(0)
  for i,O in enumerate(group):
   oo,hh=(O,fixed[0]) if direction=='forward_fresh' else (fixed[0],O)
   st,l1=step(state,U[0],V[0],oo,hh,physical=True);firstloss+=l1;nextpassive+=norm(st[2] if direction=='forward_fresh' else st[3])
   for O2 in group:
    oo2,hh2=(O2,fixed[1]) if direction=='forward_fresh' else (fixed[1],O2)
    _,l2=step(st,U[1],V[1],oo2,hh2);assert l2>=0;twoloss+=l1+l2
  firstloss/=n;twoloss/=n*n;nextpassive/=n
  assert twoloss>=c2*H0
  reports.append(dict(direction=direction,orientations=n*n,opposite_bank_fixed=True,initial_flux=str(H0),mean_first_loss=str(firstloss),mean_two_step_loss_ratio=float(twoloss/H0),proved_minimum_ratio=str(c2),exact_two_step_inequality=True,pointwise_cost_and_flux_checks=True))
 report=dict(status='EXACT_FRACTION_PASS',k=2,s=6,d=4,delta=str(delta),seconds=time.monotonic()-start,design_first_and_second_moments=True,results=reports,scope='Finite physical-model/algebra control; all-depth theorem is analytic')
 print(json.dumps(report,indent=2));open('uniform_mixing_two_step_exact_results.json','w').write(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
