import networkx as nx,itertools,json,sys,random,time
from pathlib import Path
from fractions import Fraction as F
sys.path.insert(0,str(Path(__file__).resolve().parents[2]));from exact_search import responses
H=nx.complete_graph(4);G=nx.Graph();G.add_nodes_from(H);pairs=[];shores=[];v=4
for u,w in H.edges():
 a,b,c,d=range(v,v+4);v+=4
 G.add_edges_from([(a,c),(a,d),(b,c),(b,d),(c,d),(u,a),(b,w)])
 pairs.append(frozenset([frozenset((u,a)),frozenset((b,w))]));shores.append(set([a,b,c,d]))
E=list(G.edges());n=len(G);m=len(E);Q=list(itertools.combinations(range(n),2));L=len(Q)*m*(m-1)//2;S=2*(2*n-3)*L;rng=random.Random(20261008);weights=[F(2*S,S+rng.randint(1,S)) for _ in E]
t=time.time();_,M=responses(n,E,resistances=weights);minimum=None;equalities=0
ps={frozenset((E.index(tuple(e)) if tuple(e) in E else E.index(tuple(e)[::-1])) for e in p):s for p,s in zip(pairs,shores)}
for q,row in zip(Q,M):
 for a,b in itertools.combinations(range(m),2):
  shore=ps.get(frozenset((a,b)));expected=shore is not None and ((q[0] in shore)==(q[1] in shore))
  assert (row[a]==row[b])==expected
  if row[a]!=row[b]:
   gap=abs(row[a]-row[b]);minimum=gap if minimum is None else min(minimum,gap)
  else:equalities+=1
reps=[min(s) for s in shores];fixed=[(reps[i],reps[i+1]) for i in range(0,len(reps),2)];indices=[Q.index(tuple(sorted(q))) for q in fixed]
assert len(set(tuple(M[q][e] for q in indices) for e in range(m)))==m
out={'vertices':n,'edges':m,'response_entries':len(Q)*m,'comparisons':L,'structural_equalities':equalities,'S':S,'maximum_resistor_bit_length':max(max(r.numerator.bit_length(),r.denominator.bit_length()) for r in weights),'min_nonzero_response_gap':str(minimum),'min_gap_float':float(minimum),'fixed_queries':fixed,'N':3,'A':2,'seconds':time.time()-t,'all_generic_partitions_verified':True,'weights':[str(w) for w in weights],'edges_list':E}
print(json.dumps(out),flush=True)
