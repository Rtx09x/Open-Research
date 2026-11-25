"""Bounded full new-base replay; only run after parent resource clearance.

Uses unchanged inspected/attributed Tandon verifier, with an explicitly changed
physical base file. Every C1--C4/q15 overlap is recomputed before any bound claim.
"""
import resource,sys,json,time,traceback,hashlib,os
from pathlib import Path
HERE=Path(__file__).resolve().parent
resource.setrlimit(resource.RLIMIT_AS,(1536*1024*1024,1536*1024*1024))
resource.setrlimit(resource.RLIMIT_CPU,(270,275))
os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
sys.path.insert(0,str(HERE.parent/'published'))
start=time.monotonic();result={}
try:
 from shannon.certificates import compute_all
 from shannon.construction import load_certificates,theorem2,nth_root_digits
 derived=compute_all(HERE/'cycle_flip_base_c7.json',verbose=True)
 assert all(derived['base_axioms'].values())
 assert derived['C1']==25352
 ledger=load_certificates();ledger['base_gadget']['profile']=list(derived['base_profile'])
 for key in ['C1','C2','C3','C4','q15']:ledger['certificates'][key]['value']=derived[key]
 ledger['certificates']['C1']['pre_exchange_value']=derived['C1_pre_exchange']
 ledger['certificates']['C4']['component_decomposition']=derived['C4_components']
 ledger['certificates']['C4']['size_I30pp']=derived['I30pp'];ledger['certificates']['C4']['size_X30_0L']=derived['X30_0L']
 construction=theorem2(ledger);M=construction['M']
 result={'derived':derived,'M500':M,'rate':nth_root_digits(M,500,50),'target_exceeded':M*10**3000>3258841**500,'base_sha256':hashlib.sha256((HERE/'cycle_flip_base_c7.json').read_bytes()).hexdigest(),'upstream_attribution':'../published/NOTICE; pinned inspected source, unchanged','status':'full recomputation completed'}
 (HERE/'cycle_flip_recomputed_ledger.json').write_text(json.dumps(ledger,indent=2)+'\n');(HERE/'cycle_flip_recomputed_result.json').write_text(json.dumps(result,indent=2)+'\n');print('RESULT',result['rate'],'TARGET_EXCEEDED',result['target_exceeded'],flush=True)
except Exception as e:
 result={'status':'failed','exception':repr(e)};traceback.print_exc();raise
finally:
 resources={'seconds':time.monotonic()-start,'maxRSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'status':result.get('status','interrupted')};(HERE/'cycle_flip_replay_resources.json').write_text(json.dumps(resources,indent=2)+'\n');print('RESOURCES',resources,flush=True)
