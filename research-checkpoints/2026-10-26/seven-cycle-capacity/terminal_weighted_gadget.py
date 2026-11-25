#!/usr/bin/env python3
"""Weighted private-block Gao construction above the published terminal code.
This is a finite label-code construction; endpoints denote blocks, not vertices.
"""
import os
os.environ.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1')
import sys,json,itertools,time
import numpy as np
sys.path.insert(0,'published')
from shannon import bpz
from shannon.construction import theorem2,nth_root_digits
T=theorem2();labels=[l for l in bpz.LABELS if T['n25'][bpz.INDEX[l]]];words=list(itertools.product(labels,repeat=4));index={w:i for i,w in enumerate(words)};A=np.array([[labels.index(x) for x in w] for w in words]);n=len(words);L=np.array([[not bpz.perp(a,b) for b in labels] for a in labels]);adj=np.ones((n,n),dtype=bool)
for k in range(4):adj&=L[A[:,None,k],A[None,:,k]]
R=[index[w] for w in bpz.K4a];rset=set(R);W=[bpz._word_value(w,[T['n25']]*4) for w in words];main=sum(W[x] for x in R);assert main==T['M'];neighbors=adj[:,R].sum(axis=1);pairs=[(R[int(np.flatnonzero(adj[q,R])[0])],q) for q in range(n) if q not in rset and neighbors[q]==1]
print('private_alternatives',len(pairs),'equal_weight',sum(W[r]==W[q] for r,q in pairs),flush=True)
reflect={'B':'B','N':'N','A':'D','D':'A','H':'V','V':'H'};Xs={}
for perm in itertools.permutations(range(4)):
 for flags in itertools.product((0,1),repeat=4):
  X=tuple(sorted(index[tuple(reflect[w[perm[k]]] if flags[k] else w[perm[k]] for k in range(4))] for w in bpz.K4a));Xs.setdefault(X,{'perm':perm,'reflect':flags})
best=main**2;bestcand=None;valid=0;start=time.monotonic()
for X,transform in Xs.items():
 s=sum(W[x] for x in X)
 for r,q in pairs:
  nr=adj[r,list(X)];nq=adj[q,list(X)]
  if np.any(nr&nq):continue
  valid+=1;x0=sum(W[x] for x,a,b in zip(X,nr,nq) if not(a or b));side=s-x0
  M=(main-W[r])**2+2*W[r]*x0+(W[r]+W[q])*side
  if M>best:
   best=M;B=[x for x in R if x!=r];X0=[x for x,a,b in zip(X,nr,nq) if not(a or b)];XH=[x for x,a in zip(X,nr) if a];XV=[x for x,a in zip(X,nq) if a]
   # Literal finite Cartesian recipe, independently rechecked before export.
   code=set(tuple(words[a]+words[b]) for S,U in ((B,B),([r],X0),([r],XH),([q],XV),(X0,[r]),(XH,[q]),(XV,[r])) for a in S for b in U)
   exact=bpz.apply_code(list(code),[T['n25']]*8);assert exact==M
   # Factor-wise separation of rectangles proves pairwise independence without quadratic materialization.
   blocks=[(B,B),([r],X0),([r],XH),([q],XV),(X0,[r]),(XH,[q]),(XV,[r])]
   for S,U in blocks:
    assert not np.any(adj[np.ix_(S,S)]&~np.eye(len(S),dtype=bool));assert not np.any(adj[np.ix_(U,U)]&~np.eye(len(U),dtype=bool))
   for (S,U),(V,Z) in itertools.combinations(blocks,2):assert not np.any(adj[np.ix_(S,V)]) or not np.any(adj[np.ix_(U,Z)])
   bestcand={'pair_words':[words[r],words[q]],'auxiliary_automorphism':transform,'auxiliary_words':[words[x] for x in X],'main_weight':main,'new_M':M,'dimension':1000,'bound':nth_root_digits(M,1000,70),'gain_over_square':M-main**2,'label_codeword_count':len(code),'code':sorted(code),'blocks':[[[words[x] for x in S],[words[x] for x in U]] for S,U in blocks],'input_vector':T['n25']}
   open('weighted_terminal_improvement.json','w').write(json.dumps(bestcand,indent=2)+'\n');print('IMPROVEMENT',bestcand['bound'],'codewords',len(code),flush=True)
out={'private_alternatives':len(pairs),'auxiliary_automorphism_codes':len(Xs),'admissible_single_pair_gadgets':valid,'improved':best>main**2,'best_bound':nth_root_digits(best,1000,70),'elapsed_seconds':time.monotonic()-start};open('weighted_terminal_results.json','w').write(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
