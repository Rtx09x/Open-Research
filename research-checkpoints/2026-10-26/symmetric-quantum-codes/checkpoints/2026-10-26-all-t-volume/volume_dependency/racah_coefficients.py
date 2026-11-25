"""Exact factorial Racah coefficient; extracted without solver dependencies."""
from fractions import Fraction as Q
from functools import lru_cache
from math import factorial as f
@lru_cache(None)
def racah(n,r,k):
 pref=Q(f(n-r)*f(r)**2,f(n+r+1))*Q(f(n-k)*f(k)**2,f(n+k+1))
 return pref*sum((Q((-1)**z*f(z+1),f(z-n-r)**2*f(z-n-k)**2*f(2*n-z)*f(n+r+k-z)**2)for z in range(max(n+r,n+k),min(2*n,n+r+k)+1)),Q(0))
