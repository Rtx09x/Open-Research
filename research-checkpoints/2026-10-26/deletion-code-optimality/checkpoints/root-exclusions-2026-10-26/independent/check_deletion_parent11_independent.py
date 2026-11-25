"""Own recursive, exact deletion-geometry audit of the frozen parent5 exclusion.
No worker code imports. Earlier independently audited receiver/face proofs
are bound by exact file hashes, rather than inferred from their discovery logs.
"""
from pathlib import Path
from collections import Counter
from itertools import combinations
import json,hashlib,time
if not __debug__:raise RuntimeError('Assertions required')
start=time.monotonic();H=Path(__file__).resolve().parent
F=Path('/workspace/shared/research-active/deletion-code-optimality/continuation/evidence/parent11_exclusion_frozen')
E=F/'evidence';root=E/'case'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=read(F/'MANIFEST.json');assert sha(F/'MANIFEST.json')=='75dfbeb05aa15b14a3e6f26b33b7ef94d7ca67c5339216246cc9fddb34c162e1'
for f in manifest['files']:
 p=F/f['path'];assert p.is_relative_to(F) and p.stat().st_size==f['bytes'] and sha(p)==f['sha256']
req=read(E/'required_receivers320/certificate.json');prior=read(H/'check_deletion_forced_receivers_independent.json')
assert prior['PASS'] and prior['certificate_sha256']==sha(E/'required_receivers320/certificate.json')
assert sha(E/'required_receivers320/global_dual.json')==req['global_dual_sha256']
D=[];R=[set() for _ in range(2048)]
for x in range(4096):
 s=f'{x:012b}';D.append({int(s[:i]+s[i+1:],2) for i in range(12)})
 for y in D[-1]:R[y].add(x)
def tr(x,g):return (int(f'{x:012b}'[::-1],2) if g&2 else x)^(4095 if g&1 else 0)
ccache={};cgcache={};normalization=read(root/'model.json')['normalization']
def clique(xs):
 key=tuple(sorted(xs));assert len(key)==len(set(key)) and all(type(x)==int and 0<=x<4096 for x in key)
 if key not in ccache:
  assert all(D[x]&D[y] for x,y in combinations(key,2));ccache[key]=({x:1 for x in key},1)
 return ccache[key]
def rebuild(model):
 assert model['normalization']==normalization and model['fixed_constants']==[0,4095] and model['selected_words']==[]
 key=json.dumps(model['nodes'],sort_keys=True)
 if key not in cgcache:
  cg=[]
  for i,node in enumerate(model['nodes']):
   a=Counter();b=0
   for p in node['parents']:
    m=p.get('m',1);assert type(m)==int and m>0
    if 'receiver' in p:aa={x:1 for x in R[p['receiver']]};bb=1
    elif 'clique' in p:aa,bb=clique(p['clique'])
    else:assert 0<=p['cut']<i;aa,bb=cg[p['cut']]
    for x,v in aa.items():a[x]+=m*v
    b+=m*bb
   q=node['divisor'];assert type(q)==int and q>=2
   cg.append(({x:v//q for x,v in a.items() if v>=q},b//q))
  cgcache[key]=cg
 cg=cgcache[key];rows=[];required=[];canon=[]
 assert len(model['rows'])==len(model['rhs'])
 for i,r in enumerate(model['rows']):
  if 'clique' in r:a,b=clique(r['clique'])
  elif 'required_receiver' in r:
   y=r['required_receiver'];assert y in req['required_receivers'];required.append(y);a={x:-1 for x in R[y]};b=-1
  elif 'canonical_prefix' in r:
   pf=r['canonical_prefix'];g=r['transform'];assert 1<=len(pf)<=10 and len(pf)==len(set(pf)) and pf==normalization['prefix'][:len(pf)] and g in(1,2,3)
   a=Counter();b=0;canon.append((len(pf),g))
   for j,x in enumerate(pf):a[tr(x,g)]+=2**(len(pf)-j-1);a[x]-=2**(len(pf)-j-1)
   a={x:v for x,v in a.items() if v}
  else:
   assert set(r)=={'cut','transform'} and r['transform'] in range(4)
   aa,b=cg[r['cut']];a={tr(x,r['transform']):v for x,v in aa.items()}
  assert b==model['rhs'][i];rows.append((a,b))
 assert sorted(required)==sorted(req['required_receivers']) and sorted(canon)==[(i,g) for i in range(1,11) for g in(1,2,3)]
 return rows
logs=[];partitions=[];face_logs=[]
def visit(path,y,extras):
 model=read(path/'model.json');scope=model['conditional_target320'];ones=[0,4095,11]+extras
 assert scope['fixed_ones']==ones and scope.get('extra_fixed_ones',[])==extras
 assert scope.get('cover_path',[[3,11]])==[[3,11]] and scope['branch_receiver']==3 and scope['fixed_parent']==11
 assert scope['required_receivers']==req['required_receivers'] and scope['required_certificate_sha256']==prior['certificate_sha256'] and scope['all58_zero_restriction'] is False
 assert 11 in R[3] and all(not D[x]&D[z] for x,z in combinations(ones,2))
 zeros={x for x in range(4096) if x not in ones and any(D[x]&D[z] for z in ones)}
 rows=rebuild(model);c=read(path/'dual.json');M=c['scale'];assert type(M)==int and M>0 and c['fixed_ones']==ones and set(c['conflict_zero_words'])==zeros
 cov=[0]*4096;cost=0
 for label in('lambda','upper','lower'):assert len(dict(c[label]))==len(c[label]) and all(type(v)==int and v>0 for _,v in c[label])
 for i,v in c['lambda']:
  assert 0<=i<len(rows);a,b=rows[i];cost+=v*b
  for x,z in a.items():cov[x]+=v*z
 for x,v in c['upper']:assert 0<=x<4096;cov[x]+=v;cost+=v*(x not in zeros)
 for x,v in c['lower']:assert 0<=x<4096;cov[x]-=v;cost-=v*(x in ones)
 assert min(cov)>=M and cost==c['numerator']
 logs.append({'path':str(path.relative_to(F)),'numerator':cost,'scale':M,'direct_prune':cost<320*M})
 if cost<320*M:return
 face=path/'slack_face_proof.json'
 if face.exists():
  link=read(face);fp=E/link['folder'];assert sha(fp/'MANIFEST.json')==link['manifest_sha256']
  afile='check_deletion_forced_face_independent.json' if y==519 and not extras else 'check_deletion_forced_face263_771_independent.json'
  audit=read(H/afile);assert audit['PASS'] and audit['conditional_path']==scope['cover_path'] and audit.get('extra_fixed_ones',[])==extras
  for name,h in audit['files_sha256'].items():assert sha(fp/name)==h
  for name in('model.json','dual.json'):assert sha(path/name)==sha(fp/name)
  assert audit['minimum']>audit['rhs'];face_logs.append({'path':str(path.relative_to(F)),'audit':afile,'margin':audit['minimum']-audit['rhs']});return
 ps=list(path.glob('forced_clique*/partition.json'));assert len(ps)==1
 pfile=ps[0];part=read(pfile);assert part['source_model_sha256']==sha(path/'model.json') and part['source_dual_sha256']==sha(path/'dual.json')
 idx=part['source_row'];assert model['rows'][idx]=={'clique':part['clique']};a,b=rows[idx]
 assert b==1 and all(v==1 for v in a.values()) and not set(a)&set(ones)
 gap=cost-320*M;lam=dict(c['lambda'])[idx];assert lam>gap==part['gap_numerator'] and lam==part['multiplier']
 xs=sorted(set(a)-zeros);assert xs==part['compatible_parents'] and sorted(set(a)&zeros)==part['discarded_conflicting_parents']
 if 'scope' in part:assert part['scope']==scope
 partitions.append({'path':str(pfile.relative_to(F)),'children':xs,'gap':gap,'multiplier':lam})
 for x in xs:visit(pfile.parent/f'parent_{x}',y,extras+[x])
visit(root,11,[])
assert len(logs)==61 and sum(x['direct_prune'] for x in logs)==49 and len(face_logs)==0 and len(partitions)==12
out={'PASS':True,'method':'Own literal deletion, CG/fixed-prefix rebuild, exact dual costs and recursive forced-clique partition; no worker code imports','manifest_sha256':sha(F/'MANIFEST.json'),'nodes':len(logs),'direct_exact_leaves':49,'independently_bound_Farkas_leaves':face_logs,'forced_partitions':partitions,'root_receiver3_parent':11,'claim':'Normalized target320 code with constants cannot contain word11','global_upper319':False,'seconds':time.monotonic()-start,'node_checks':logs}
(H/'check_deletion_parent11_independent.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in('node_checks','forced_partitions')},indent=2))
