#!/usr/bin/env python3
"""Network-free, isolated checkpoint replay. Assertions must remain enabled."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,platform,resource,shutil,subprocess,sys,tempfile,time
ROOT=Path(__file__).resolve().parent

def limits():
    resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
    resource.setrlimit(resource.RLIMIT_CPU,(300,305))
    if hasattr(os,'sched_setaffinity'):
        available=os.sched_getaffinity(0)
        os.sched_setaffinity(0,{min(available)})

def tasks(full):
    out=[]
    def add(track,cmd,kind='exact certificate',inspect=None):out.append((track,cmd.split(),kind,inspect))
    t='deletion-code-optimality'
    add(t,'scripts/baseline.py 12','baseline reconstruction')
    add(t,'scripts/small_exact_control.py --n 6','small exact positive control',('evidence/small_exact_control_n6.json','small'))
    add(t,'scripts/trades.py --n 6 --k 2 --seconds 30','known neutral-switch positive control',('evidence/trades_n6_k2.json','neutral'))
    t='symmetric-quantum-codes'
    for f in ['check_quantum_farkas.py','check_quantum_gram_bound.py','audit_code19.py','audit_pure_complement.py','audit_time_reversal.py','audit_robust_pure_gap.py','audit_optimized_robust_gap.py','audit_gram_map_exact.py']:add(t,'tests/'+f)
    t='hss-probe-reuse'
    add(t,'verify_rational_potential.py','exact 4096-sign proof-route counterexample')
    add(t,'verify_results.py','stored-result consistency, not independent regeneration')
    add(t,'exact_tree_test.py','finite exhaustive integer-valued NumPy controls')
    t='seven-cycle-capacity'
    for f in ['verify_base.py','replay_wrapper.py','verify_weighted_terminal_independent.py','verify_recycled_certificate.py','tests/audit_c7_optimized.py']:add(t,f)
    if full:add(t,'verify_recycled_certificate.py optimized_recycle_certificate.json','exact giant-integer-power root bracket')
    t='online-bin-packing'
    for f in ['verify_ah_source_delta.py','verify_ah_full.py ah_three_parameter_full_certificate.json ah_three_parameter_full_verification.json','verify_ah_three_parameter_algebra.py','tests/audit_ah_three_parameter.py','tests/audit_ah_two_scenario_floor.py','verify_ah_full.py ah_two_parameter_published_weights_certificate.json ah_two_parameter_published_weights_verification.json','verify_ah_three_face_algebra.py','verify_ah_full.py ah_variant_full_certificate.json ah_variant_full_verification.json']:add(t,f)
    if full:
        t='deletion-code-optimality'
        add(t,'scripts/trades.py --n 12 --k 9 --seconds 280','exhaustive local barrier',('evidence/trades_n12_k9.json','original'))
        add(t,'scripts/verify_trades_independent.py --n 12 --k 9 --seconds 280','independently implemented exhaustive local barrier',('evidence/independent_trades_n12_k9.json','independent'))
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--full',action='store_true');ap.add_argument('--output',default='integration/verification_local.json');a=ap.parse_args()
    if not __debug__:raise SystemExit('Refusing optimized Python: assertions must be enabled.')
    env=os.environ.copy();env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',PYTHONHASHSEED='0',PYTHONDONTWRITEBYTECODE='1')
    env.pop('PYTHONOPTIMIZE',None)
    output={'utc_started':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,'platform':platform.platform(),'mode':'full'if a.full else'core','network_used':False,'limits':{'address_space_bytes':2*1024**3,'cpu_seconds_per_check':300,'blas_threads':1,'concurrent_checks':1},'checks':[]}
    support_records={};all_ok=True
    for track,cmd,kind,inspect in tasks(a.full):
        start=time.monotonic();entry={'track':track,'command':'python '+' '.join(cmd),'scope':kind}
        with tempfile.TemporaryDirectory(prefix='research-check-') as tmp:
            work=Path(tmp)/track;shutil.copytree(ROOT/track,work,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
            try:
                result=subprocess.run([sys.executable,*cmd],cwd=work,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=320,preexec_fn=limits)
                entry.update(returncode=result.returncode,output=result.stdout,passed=result.returncode==0)
                if inspect and entry['passed']:
                    name,mode=inspect;data=json.loads((work/name).read_text());assert data['complete'],'incomplete enumeration'
                    if mode=='small':assert data['maximum_code_size']==10
                    elif mode=='neutral':assert data['neutral_examples'],'known neutral switch not detected'
                    elif mode=='original':
                        assert data['checked']==2733456 and not data['positive'] and not data['neutral_examples']
                        support_records[mode]=data['connected_supports']
                    elif mode=='independent':
                        assert data['no_neutral_or_improving_trade'] and not data['uncovered_cases'] and data['hard_cover_tests']==416412
                        assert sum(r['connected_supports']for r in data['support_records'])==2733456
                        support_records[mode]=data['support_records'];assert support_records['original']==support_records[mode],'independent hashes/counts differ'
                    entry['structured_result_checked']=True
            except Exception as exc:
                entry.update(passed=False,error=repr(exc))
            entry['wall_seconds']=round(time.monotonic()-start,3);all_ok&=entry['passed'];output['checks'].append(entry)
            print(('PASS'if entry['passed']else'FAIL'),track,' '.join(cmd),entry['wall_seconds'],flush=True)
            path=ROOT/a.output;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(output,indent=2)+'\n')
    output.update(all_passed=all_ok,utc_finished=datetime.datetime.now(datetime.timezone.utc).isoformat(),independent_radius9_hashes_match=bool(support_records)and support_records.get('original')==support_records.get('independent'))
    path.write_text(json.dumps(output,indent=2)+'\n');return 0 if all_ok else 1
if __name__=='__main__':raise SystemExit(main())
