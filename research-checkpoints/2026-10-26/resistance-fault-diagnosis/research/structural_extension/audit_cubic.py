import networkx as nx,itertools,json
for k in [3,4,5,8]:
 H=nx.circular_ladder_graph(k);G=nx.Graph();G.add_nodes_from(H);pairs=[];shores=[]
 v=len(H)
 for u,w in H.edges():
  a,b,c,d=range(v,v+4);v+=4
  G.add_edges_from([(a,c),(a,d),(b,c),(b,d),(c,d),(u,a),(b,w)])
  pairs.append(frozenset([frozenset((u,a)),frozenset((b,w))]));shores.append(set([a,b,c,d]))
 assert nx.is_biconnected(G) and nx.check_planarity(G)[0] and set(dict(G.degree()).values())=={3}
 cutpairs=[]
 for e,f in itertools.combinations(G.edges(),2):
  J=G.copy();J.remove_edges_from([e,f])
  if not nx.is_connected(J):cutpairs.append(frozenset([frozenset(e),frozenset(f)]))
 assert set(cutpairs)==set(pairs)
 reps=[min(s) for s in shores];q=[(reps[i],reps[i+1]) for i in range(0,len(reps)-1,2)]
 if len(reps)%2:q.append((reps[-1],reps[0]))
 assert all(any((u in s)!=(w in s) for u,w in q) for s in shores)
 print(json.dumps({'prism_k':k,'vertices':len(G),'edges':G.number_of_edges(),'series_pairs':len(pairs),'A':2,'N':len(q),'simple_planar_cubic_biconnected':True,'all_cutpairs_verified':True}),flush=True)
