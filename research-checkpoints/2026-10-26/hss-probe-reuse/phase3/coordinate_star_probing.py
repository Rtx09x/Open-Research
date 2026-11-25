"""Known coordinate-HSS support: treewidth certificate and direct signed probing.
Small star-coloring search is for reproducible controls, not a complexity claim.
"""
import itertools,json
import numpy as np
from coordinate_observation_forest import structure


def certificate(bases):
 n,levels,rr,cc,rc,vc,entries,w=structure(bases)
 bags=[{rr[0],rr[1],n+cc[0]},{rr[0],rr[1],n+cc[1]}];parents=[None,0]
 introduced=set.union(*bags)
 for nodes in reversed(levels):
  for rows,cols,u,v in nodes:
   r,c=rows[u],n+cols[v];rd,cd=rows[1-u],n+cols[1-v]
   assert r in introduced and c in introduced and rd not in introduced and cd not in introduced
   anchor=next(i for i,b in enumerate(bags) if {r,c}<=b)
   i=len(bags);bags.extend([{r,c,rd},{r,rd,cd}]);parents.extend([anchor,i]);introduced.update([rd,cd])
 edges={(i,n+j) for i,j,_ in entries};adj=[set() for _ in range(2*n)]
 for a,b in edges:adj[a].add(b);adj[b].add(a)
 assert all(any({a,b}<=bag for bag in bags) for a,b in edges)
 badj=[set() for _ in bags]
 for i,p in enumerate(parents):
  if p is not None:badj[i].add(p);badj[p].add(i)
 for v in range(2*n):
  target={i for i,b in enumerate(bags) if v in b};seen={next(iter(target))};stack=list(seen)
  while stack:
   i=stack.pop()
   for j in badj[i]&target-seen:seen.add(j);stack.append(j)
  assert seen==target
 return n,entries,adj,bags,parents


def star_coloring(adj,limit=6):
 n=len(adj);paths=set()
 for a in range(n):
  for b in adj[a]:
   for c in adj[b]-{a}:
    for d in adj[c]-{a,b}:paths.add(min((a,b,c,d),(d,c,b,a)))
 at=[[] for _ in range(n)]
 for p in paths:
  for v in p:at[v].append(p)
 colors=[-1]*n;calls=0
 def visit(done):
  nonlocal calls
  calls+=1
  if calls>100000:raise RuntimeError('Small-test coloring search cap reached; no theorem conclusion')
  if done==n:return True
  v=max((v for v in range(n) if colors[v]<0),key=lambda v:(len({colors[w] for w in adj[v] if colors[w]>=0}),len(adj[v])))
  used=max(colors)+1
  for col in range(min(limit,used+1)):
   if any(colors[w]==col for w in adj[v]):continue
   colors[v]=col
   if any(all(colors[x]>=0 for x in p) and colors[p[0]]==colors[p[2]] and colors[p[1]]==colors[p[3]] for p in at[v]):continue
   if visit(done+1):return True
  colors[v]=-1;return False
 assert visit(0)
 assert all(colors[a]!=colors[b] for a in range(n) for b in adj[a])
 assert all(not(colors[a]==colors[c] and colors[b]==colors[d]) for a,b,c,d in paths)
 return colors,calls


def selected_equations(n,entries,colors):
 support={(i,j) for i,j,_ in entries};selected={};channels=set()
 for i,j in support:
  forward=[l for h,l in support if h==i and colors[n+l]==colors[n+j]]
  reverse=[h for h,l in support if l==j and colors[h]==colors[i]]
  if len(forward)==1:channel=('F',i,colors[n+j])
  else:
   assert len(reverse)==1;channel=('T',j,colors[i])
  assert channel not in channels;channels.add(channel);selected[i,j]=channel
 weights=np.zeros((n,n),dtype=np.int64)
 for i in range(n):
  for j in range(n):
   if (i,j) not in support:
    weights[i,j]=int(('F',i,colors[n+j]) in channels)+int(('T',j,colors[i]) in channels)
 assert weights.max()<=2
 return support,selected,weights


def decode(a,n,k,colors,selected,tau,sigma):
 q=max(colors)+1;om=np.zeros((n*k,q*k),dtype=np.int64);ps=om.copy()
 for i in range(n):
  om[i*k:(i+1)*k,colors[n+i]*k:(colors[n+i]+1)*k]=sigma[i]*np.eye(k,dtype=np.int64)
  ps[i*k:(i+1)*k,colors[i]*k:(colors[i]+1)*k]=tau[i]*np.eye(k,dtype=np.int64)
 y=a@om;z=a.T@ps;b=np.zeros_like(a)
 for (i,j),(direction,vertex,color) in selected.items():
  ri=slice(i*k,(i+1)*k);cj=slice(j*k,(j+1)*k);ch=slice(color*k,(color+1)*k)
  b[ri,cj]=sigma[j]*y[ri,ch] if direction=='F' else tau[i]*z[cj,ch].T
 return b


def main():
 rng=np.random.default_rng(71091);out=[]
 # All coordinate basis pairs at n4; all256 physical sign gauges, k1 andk2.
 for bits in itertools.product([0,1],repeat=4):
  bas=[(bits[:2],bits[2:])];n,entries,adj,bags,par=certificate(bas);colors,calls=star_coloring(adj)
  support,sel,weights=selected_equations(n,entries,colors)
  for k in [1,2]:
   a=rng.integers(-3,4,size=(n*k,n*k),dtype=np.int64);e=a.copy()
   for i,j in support:e[i*k:(i+1)*k,j*k:(j+1)*k]=0
   expected=sum((1+int(weights[i,j]))*int(np.sum(e[i*k:(i+1)*k,j*k:(j+1)*k]**2)) for i in range(n) for j in range(n))
   total=0
   for signs in itertools.product([-1,1],repeat=2*n):
    b=decode(a,n,k,colors,sel,signs[:n],signs[n:]);total+=int(np.sum((a-b)**2))
   assert total==expected*2**(2*n);assert expected<=3*int(np.sum(e*e))
  out.append(dict(n=n,basis_bits=list(bits),colors=max(colors)+1,search_calls=calls,exact_sign_cases=512))
 # Larger random hierarchy treewidth, coloring and unit-leakage controls.
 larger=[]
 for L in [2,3]:
  for trial in range(12):
   bas=[(rng.integers(0,2,size=2**ell).tolist(),rng.integers(0,2,size=2**ell).tolist()) for ell in range(L,0,-1)]
   n,entries,adj,bags,par=certificate(bas);colors,calls=star_coloring(adj);support,sel,weights=selected_equations(n,entries,colors)
   larger.append(dict(L=L,n=n,colors=max(colors)+1,search_calls=calls,bag_count=len(bags),max_offsupport_leakage=int(weights.max())))
 decomp=[]
 for L in [4,5,6]:
  for trial in range(5):
   bas=[(rng.integers(0,2,size=2**ell).tolist(),rng.integers(0,2,size=2**ell).tolist()) for ell in range(L,0,-1)]
   n,entries,adj,bags,par=certificate(bas);decomp.append(dict(L=L,n=n,bags=len(bags),width=2))
 report=dict(status='EXACT_INTEGER_PASS',n4_exhaustive=out,larger=larger,decomposition_only_larger=decomp,total_n4_decoder_executions=8192)
 print(json.dumps(report,indent=2));open('coordinate_star_probing_results.json','w').write(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
