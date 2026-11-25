"""Exact rational one-bank gains >2 and approaching the proved bound5."""
from fractions import Fraction as F
import json


def run(q,m):
    a,b=F(q*q-1,q*q+1),F(2*q,q*q+1)
    x=y=F(0);z=F(1)  # attained from pure detail by row swap / column identity
    co,si=F(1),F(0)
    for _ in range(m):
        x,y,z=a*x-b*y,b*(x-z)+a*y,a*z
        co,si=a*co-b*si,b*co+a*si
    actual=x*x+y*y+z*z
    predicted=1+2*a**(2*m)-2*a**m*co
    assert actual==predicted and actual<5
    return actual


def main():
    rows=[]
    for q,m in [(4,6),(8,13),(32,50),(128,201),(512,804)]:
        gain=run(q,m)
        assert gain>2
        rows.append(dict(rotation_half_angle_tangent=f'1/{q}',ancestors=m+1,
                         exact_gain=str(gain) if q==4 else None,
                         gain_float=float(gain),exact_gain_below5=True))
    assert rows[-1]['gain_float']>4.96
    out=dict(status='PASS',arithmetic='fractions.Fraction',sharp_limit=5,results=rows)
    with open('one_bank_sharpness_results.json','w') as f:json.dump(out,f,indent=2)
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
