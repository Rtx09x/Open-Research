#!/usr/bin/env python3
"""Dependency-free exact checker of algebraic squeezed-state Chernoff ordering.
Total Pauli error is p=91/500 (not per-Pauli error).
It checks a bivariate polynomial identity on a sufficient exact interpolation
mesh, then a 1-variable integer-polynomial positivity certificate.
The quantum Chernoff theorem, Gaussian square-root covariance formula, and
binary cq entropy inequalities are analytical imports, not proved by this script.
"""
from fractions import Fraction as Q
from math import comb

p=Q(91,500); eta=1-Q(4,3)*p
T=2*eta*eta/(1+eta); G=eta/T
E=1-T; F=T*(G-1); H=(G-1)*E+G
assert eta==Q(284,375)
assert (T,G,E,F)==(Q(161312,247125),Q(659,568),Q(85813,247125),Q(25844,247125))

def add(A,B): return [[A[i][j]+B[i][j] for j in range(2)] for i in range(2)]
def sub(A,B): return [[A[i][j]-B[i][j] for j in range(2)] for i in range(2)]
def mul(A,B): return [[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def scale(A,k): return [[k*A[i][j] for j in range(2)] for i in range(2)]
def det(A): return A[0][0]*A[1][1]-A[0][1]*A[1][0]
def quadratic_adjugate(A): return A[0][0]+A[1][1]+A[0][1]+A[1][0]

a=415065438346832
b=866854719009461
d=412335642318000
e=105757630339125
s=59969;t=80656;v=20687

# Identity polynomial P_ID(x,c) of deg_x <= 10, deg_c <= 3.
# Ux entries are degree <=1 in x; Up entries Laurent exponents -1..0;
# P=x*(nu2-1/4) has degree<=2; Wtilde=P*Ux+c*x*C degree<=3 in x
# and degree<=1 in c. 2x2 determinants/adjugates give the bounds.
# A polynomial with these degree bounds vanishing on an 11x4 grid
# vanishes identically. No floating-point calculations used.
checks=0
for xi in range(1,12):
  x=Q(xi)
  bx=eta*x/2+(1-eta*eta)/(2*eta)
  bp=eta/(2*x)+(1-eta*eta)/(2*eta)
  nu2=bx*bp
  P=x*(nu2-Q(1,4))
  Ux=[[(E*x+T)/(2*E),(1-x)/2],[(1-x)/2,(F*x+H)/(2*F)]]
  Up=[[(E/x+T)/(2*E),(1/x-1)/2],[(1/x-1)/2,(F/x+H)/(2*F)]]
  D=[[E,Q(0)],[Q(0),F]]
  C=sub(mul(mul(mul(mul(Ux,D),Up),D),Ux),scale(Ux,Q(1,4)))
  den=187156*(s*x+t)*(t*x*x-v*x+t)
  for ci in range(4):
    c=Q(ci)
    Wtilde=add(scale(Ux,P),scale(C,c*x))
    q=quadratic_adjugate(Wtilde)
    determinant=det(Wtilde)
    N=c*(a*x*x+b*x+a)-d*x*x+e*x-d
    left=den*(bx*(1+c)*P*q-eta*determinant)
    right=N*determinant
    assert left==right,(x,c,left-right)
    checks+=1

# c(x)^2 = s*(t*z-v)/(s*t*z+s*s+t*t) for z=x+1/x>=2.
# N/x = c*(a*z+b)-(d*z-e).  A>0, B>0 for all z>=2;
# (c*A)^2-B^2 = polynomial F(z)/positive denominator.
assert 2*d>e
assert 2*t>v

def pmul(A,B):
  out=[0]*(len(A)+len(B)-1)
  for i,ai in enumerate(A):
    for j,bj in enumerate(B):out[i+j]+=ai*bj
  return out

def psub(A,B):
  n=max(len(A),len(B));return [(A[i] if i<len(A) else 0)-(B[i] if i<len(B) else 0) for i in range(n)]
A=[b,a];B=[-e,d]
Fpoly=psub(pmul([-s*v,s*t],pmul(A,A)),pmul([s*s+t*t,s*t],pmul(B,B)))
assert len(Fpoly)==4
# Change variable z=y+2. y>=0.
shift=[sum(Fpoly[j]*comb(j,k)*2**(j-k) for j in range(k,4)) for k in range(4)]
assert all(k>0 for k in shift)
assert shift==[
 14064771544407206520438194274902343750000,
 11584877946750014267313386718750000000000,
 2036795301781986156290666183238336000000,
 10924706255250488847234229442270068736]
print('PASS:',checks,'interpolation identities (deg_x<=10, deg_c<=3)')
print('PASS: all 4 F(z=y+2) integer coefficients strictly positive')
print('PROVED BY ALGEBRA: gamma_E(v)>gamma_B(v) for every nonzero')
print('displacement v, every pure one-mode squeezing parameter and orientation')
print('at total Pauli noise p=91/500; quantum Chernoff/entropy results imported.')
