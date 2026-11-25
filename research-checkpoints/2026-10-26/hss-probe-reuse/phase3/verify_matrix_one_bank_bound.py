"""Exact k=2 covariance-invariant test with noncommuting transfers.

Independent stdlib implementation. Each stage averages the eight signed
permutations, which have exactly the centering/conjugation moments needed for
the LOCAL branch proof. The global theorem uses Haar complement orientations.
"""
from fractions import Fraction as F
from itertools import permutations, product
import json


def tr(a): return list(map(list, zip(*a)))
def mm(a, b): return [[sum(x*y for x,y in zip(r,c)) for c in zip(*b)] for r in a]
def add(a,b): return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def sub(a,b): return [[x-y for x,y in zip(r,s)] for r,s in zip(a,b)]
def scale(c,a): return [[c*x for x in r] for r in a]
def eye(n): return [[F(i==j) for j in range(n)] for i in range(n)]
def zero(n,m): return [[F(0) for _ in range(m)] for _ in range(n)]
def norm(a): return sum(x*x for r in a for x in r)


def house(v):
    v=list(map(F,v));s=sum(x*x for x in v)
    return [[F(i==j)-2*v[i]*v[j]/s for j in range(len(v))] for i in range(len(v))]


def blocks(o):
    assert mm(tr(o),o)==eye(4)
    return ([r[:2] for r in o[:2]],[r[2:] for r in o[:2]],
            [r[:2] for r in o[2:]],[r[2:] for r in o[2:]])


def step(state,row,col,h,o):
    x,y,z,w=state;r,t,rp,tp=row;a,b,ap,bp=col
    f=eye(4)[:2];g=eye(4)[2:];p=f;q=g
    fc=add(mm(a,f),mm(b,g));gc=mm(o,add(mm(ap,f),mm(bp,g)))
    pc=add(mm(r,p),mm(t,q));qc=mm(h,add(mm(rp,p),mm(tp,q)))
    yc=add(mm(x,fc),mm(y,gc));zc=add(mm(tr(z),pc),mm(tr(w),qc))
    ya,yd,za,zd=mm(tr(r),yc),mm(tr(t),yc),mm(tr(a),zc),mm(tr(b),zc)
    dad=mm(p,tr(zd));dda=mm(yd,tr(f))
    yn=sub(ya,mm(dad,g));zn=sub(za,mm(tr(dda),q))
    out=(mm(yn,tr(f)),mm(yn,tr(g)),mm(p,tr(zn)),mm(q,tr(zn)))
    # Independently verify the covariance-driving coordinate formula.
    pred_z=add(mm(mm(tr(r),z),a),mm(mm(mm(tr(rp),tr(h)),w),a))
    assert out[2]==pred_z
    return out


def main():
    group=[]
    for perm in permutations(range(2)):
        for signs in product((-1,1),repeat=2):
            h=zero(2,2)
            for i in range(2):h[i][perm[i]]=F(signs[i])
            group.append(h)
    w0=[[F(1,3),F(2,5)],[F(-3,7),F(4,11)]]
    c2=norm(w0);states=[(zero(2,2),zero(2,2),zero(2,2),w0)]
    result=[]
    for ell in range(3):
        row=blocks(mm(house([1,2+ell,3,4]),house([2,1,-1,3+ell])))
        col=blocks(mm(house([1,-2,2+ell,3]),house([3,1,1,2+ell])))
        o=[[F(3,5),F(-4,5)],[F(4,5),F(3,5)]]
        states=[step(s,row,col,h,o) for s in states for h in group]
        cov=zero(2,2);mean_s=F(0)
        for x,y,z,w in states:
            j=norm(sub(x,z))+norm(y)+norm(w)
            assert j<=c2
            cov=add(cov,mm(z,tr(z)))
            mean_s+=sum(map(norm,(x,y,z,w)))
        cov=scale(F(1,len(states)),cov);mean_s/=len(states)
        slack=sub(scale(c2/2,eye(2)),cov)
        assert slack==tr(slack)
        assert slack[0][0]>=0 and slack[1][1]>=0
        assert slack[0][0]*slack[1][1]-slack[0][1]**2>=0
        assert mean_s<=5*c2
        result.append(dict(step=ell+1,exact_orientation_histories=len(states),
                           covariance_cap_psd=True,pointwise_flux_cap=True,
                           expected_energy_ratio=float(mean_s/c2)))
    out=dict(status='PASS',arithmetic='fractions.Fraction',k=2,
             local_orientation_design='all 8 signed permutations',results=result)
    with open('matrix_one_bank_verification.json','w') as f:json.dump(out,f,indent=2)
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
