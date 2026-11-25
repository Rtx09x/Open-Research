"""Exact integer observation-forest representation of scalar coordinate LM."""
import itertools,json
import numpy as np


def structure(bases):
 n=2*len(bases[0][0]);rr=list(range(n));cc=list(range(n));levels=[]
 for us,vs in bases:
  nodes=[]
  for h,(u,v) in enumerate(zip(us,vs)):
   rows=rr[2*h:2*h+2];cols=cc[2*h:2*h+2]
   nodes.append((rows,cols,u,v))
  levels.append(nodes);rr=[rows[u] for rows,cols,u,v in nodes];cc=[cols[v] for rows,cols,u,v in nodes]
 rc={rr[0]:0,rr[1]:1};vc={cc[0]:0,cc[1]:1}
 for nodes in reversed(levels):
  for rows,cols,u,v in nodes:rc[rows[1-u]]=1-rc[rows[u]];vc[cols[1-v]]=1-vc[cols[v]]
 edges=[]
 for nodes in levels:
  for rows,cols,u,v in nodes:
   edges.extend([(rows[1-u],cols[v],'F'),(rows[1-u],cols[1-v],'F'),(rows[u],cols[1-v],'T')])
 edges.extend((i,j,'F') for i in rr for j in cc)
 def f(i,j):return 2*i+vc[j]
 def t(i,j):return 2*n+2*j+rc[i]
 parent={};edge_parent={};adj=[[] for _ in range(4*n)]
 for a,(i,j,choice) in enumerate(edges):
  u,v=f(i,j),t(i,j);child,par=(u,v) if choice=='F' else (v,u)
  assert child not in parent;parent[child]=par;edge_parent[child]=a;adj[u].append(v);adj[v].append(u)
 def path(v):
  out=[];seen=set()
  while v in parent:
   assert v not in seen;seen.add(v);out.append(edge_parent[v]);v=parent[v]
  return v,set(out)
 paths=[path(v) for v in range(4*n)]
 assert len(set(r for r,p in paths))==n+2
 weights=np.zeros((n,n),dtype=np.int64)
 for i in range(n):
  for j in range(n):
   ru,pu=paths[f(i,j)];rv,pv=paths[t(i,j)]
   weights[i,j]=len(pu.symmetric_difference(pv)) if ru==rv else len(pu)+len(pv)
 return n,levels,rr,cc,rc,vc,edges,weights


def all_unit_decoder(bases):
 n,levels,rr,cc,rc,vc,edges,weights=structure(bases);om=np.eye(2,dtype=np.int64)[[vc[i] for i in range(n)]];ps=np.eye(2,dtype=np.int64)[[rc[i] for i in range(n)]]
 y=np.zeros((n,2,n*n),dtype=np.int64);z=y.copy()
 for i in range(n):
  for j in range(n):y[i,:,i*n+j]=om[j];z[j,:,i*n+j]=ps[i]
 maps=[]
 for us,vs in bases:
  ny=[];nz=[];no=[];np_=[]
  for h,(u,v) in enumerate(zip(us,vs)):
   yy,zz=y[2*h:2*h+2],z[2*h:2*h+2];oo,pp=om[2*h:2*h+2],ps[2*h:2*h+2]
   d=np.zeros((2,2,n*n),dtype=np.int64)
   for i,j in [(1-u,v),(1-u,1-v),(u,1-v)]:
    d[i,j]=oo[j]@yy[i] if i!=u else pp[i]@zz[j]
    maps.append(d[i,j].copy())
   ny.append(yy[u]-np.einsum('ct,cs->st',d[u],oo));nz.append(zz[v]-np.einsum('rt,rs->st',d[:,v],pp));no.append(oo[v]);np_.append(pp[u])
  y,z,om,ps=map(np.array,(ny,nz,no,np_))
 for i in range(2):
  for j in range(2):maps.append(om[j]@y[i])
 maps=np.array(maps)
 assert np.array_equal(np.sum(maps*maps,axis=0).reshape(n,n),weights)
 positions=[(i,j) for i,j,_ in edges]
 assert np.array_equal(maps[:,[i*n+j for i,j in positions]],np.eye(len(edges),dtype=np.int64))
 return weights


def main():
 results=[]
 for L in [1,2]:
  n=2**(L+1);count=0;mx=0
  for bits in itertools.product([0,1],repeat=2*(n-2)):
   pos=0;bas=[]
   for ell in range(L,0,-1):
    m=2**ell;u=bits[pos:pos+m];pos+=m;v=bits[pos:pos+m];pos+=m;bas.append((u,v))
   w=all_unit_decoder(bas);count+=1;mx=max(mx,int(w.max()))
  results.append(dict(L=L,n=n,basis_pairs=count,all_matrix_units_per_pair=n*n,max_coefficient_weight=mx))
 # Independently generated exact greedy hierarchy from the previous control.
 from verify_greedy_coefficient_identity import basis
 family=[]
 for L in range(3,9):
  bas=basis(L);n,_,_,_,_,_,_,w=structure(bas)
  got=[int(w[2**j,2**L]) for j in range(L)];assert got==[3]*L
  family.append(dict(L=L,signal_coefficient_weights=got,actual_expected_total_error=4*L))
 report=dict(status='EXACT_INTEGER_PASS',exhaustive=results,greedy_family=family)
 print(json.dumps(report,indent=2));open('coordinate_observation_forest_results.json','w').write(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
