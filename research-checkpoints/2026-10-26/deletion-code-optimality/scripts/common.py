"""Exact binary one-deletion incidence; big-endian positions in checksum."""
import numpy as np
from scipy.sparse import coo_matrix

def checksum(x,n):
 return sum(i*((x>>(n-i))&1) for i in range(1,n+1))
def vt(n,a=0): return [x for x in range(1<<n) if checksum(x,n)%(n+1)==a]
def descendants(x,n):
 return sorted({((x>>(k+1))<<k)|(x&((1<<k)-1)) for k in range(n)})
def incidence(n):
 ds=[descendants(x,n) for x in range(1<<n)]
 rows=[]; cols=[]
 for x,d in enumerate(ds): rows+=d; cols += [x]*len(d)
 A=coo_matrix((np.ones(len(rows)),(rows,cols)),shape=(1<<(n-1),1<<n)).tocsc()
 return ds,A
