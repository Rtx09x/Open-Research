"""Check interval overlap behind the noisy adaptive lower bound.
The analytic proof, not this finite audit, supplies the minimax lower bound.
"""
from fractions import Fraction as F
from itertools import combinations
import json
from explicit_gap import response

def check(m):
    assert m>=5
    bound=F(4,3*(m-1)**2);maxoutside=F(0);queries=0
    for q in combinations(range(m+2),2):
        untouched=[i for i in range(m) if i+2 not in q]
        vals=[response(m,q,i) for i in untouched]
        span=max(vals)-min(vals);assert span<=bound
        # The other orientation on an untouched branch has the same answer.
        assert all(response(m,q,m+i)==response(m,q,i) for i in untouched)
        maxoutside=max(maxoutside,span);queries+=1
    scan_margin=None
    for i in range(m):
        q=(0,i+2)
        high=response(m,q,i);low=response(m,q,m+i)
        outside=[response(m,q,j) for j in range(m) if j!=i]
        assert low==1 and high>2 and max(outside)<F(31,36)
        gap=min(1-max(outside),high-1)
        assert gap>F(1,8)
        scan_margin=gap if scan_margin is None else min(scan_margin,gap)
    return {'m':m,'queries_checked':queries,'max_outside_range':str(maxoutside),
            'proved_range_bound':str(bound),'lower_noise_threshold':str(bound/2),
            'adaptive_lower_above_threshold':(m+1)//2,
            'fixed_scan_upper_below_epsilon_1_over_16':m,
            'scan_minimum_margin':str(scan_margin)}
if __name__=='__main__':
    for m in [5,10,20]:print(json.dumps(check(m)),flush=True)
