#!/usr/bin/env python3
"""Replay curated phase-2 checks in isolated temporary copies; no downloads."""
from pathlib import Path
import argparse,datetime,json,os,platform,resource,shutil,subprocess,sys,tempfile,time
ROOT=Path(__file__).resolve().parent

def limits():
    resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
    resource.setrlimit(resource.RLIMIT_CPU,(300,305))
    if hasattr(os,'sched_setaffinity'):
        os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})

def tasks(quantum=False):
    result=[]
    def add(cwd,script,scope):result.append((cwd,script,scope))
    t='online-bin-packing'
    for script in ['phase2/exact_threshold_search.py','phase2/verify_single_thresholds.py','phase2/coupled/check_saturation.py','phase2/best_fit/check_all_cases.py','phase2/best_fit/verify_step_independent.py']:
        add(t,script,'exact rational finite certificate; analytic applicability remains in theorem/audit notes')
    add(t,'phase2/best_fit/stress_gap_lemma.py','finite falsification controls, not universal proof')
    for script in ['check_packing_single_thresholds.py','check_packing_best_fit.py']:
        add('advisor/phase2',script,'independent exact pricing using integrated source-derived factual tables')
    t='hss-probe-reuse/phase2'
    for script in ['verify_one_bank_counterexample.py','verify_matrix_one_bank_bound.py','verify_one_bank_sharpness.py','wavelet_support_obstruction.py']:
        add(t,script,'exact rational controls supporting separately audited analytic fixed-basis theorem')
    add(t,'verify_three_color_forest.py','finite exhaustive integer-valued controls; NumPy int64 values remain within range')
    for script in ['test_fixed_basis_algorithm.py','test_finite_orientation_variant.py']:
        add(t,script,'supplemental numerical callback/query-count and model-recovery checks, not proof')
    if quantum:
        add('symmetric-quantum-codes','phase2/check_interval_dual.py','rigorous interval dual arithmetic; necessity requires theorem/applicability audit')
        add('quantum-independent-audit','run_exact_verification.py','separate interval implementation with fresh KL-stability replay; all shorter lengths and exact known19 existence')
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--quantum',action='store_true');ap.add_argument('--quantum-only',action='store_true');ap.add_argument('--output',default='integration/phase2/verification_local.json');args=ap.parse_args();args.quantum=args.quantum or args.quantum_only
    if not __debug__:raise SystemExit('Assertions must remain enabled; do not use Python -O.')
    env=os.environ.copy();env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',PYTHONHASHSEED='0',PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None)
    output={'utc_started':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,'platform':platform.platform(),'network_used':False,'quantum_included':args.quantum,'limits':{'address_space_bytes':2*1024**3,'cpu_seconds_per_check':300,'blas_threads':1,'concurrent_checks':1},'checks':[]}
    ok=True
    for cwd,script,scope in tasks(args.quantum):
        if args.quantum_only and not cwd.startswith(('symmetric-quantum-codes','quantum-independent-audit')):continue
        start=time.monotonic();entry={'cwd':cwd,'command':'python '+script,'scope':scope}
        with tempfile.TemporaryDirectory(prefix='phase2-check-') as temp:
            work=Path(temp)/'research';work.mkdir()
            groups=['online-bin-packing','hss-probe-reuse','advisor']
            if args.quantum:groups+=['symmetric-quantum-codes','quantum-independent-audit']
            for group in groups:shutil.copytree(ROOT/group,work/group,ignore=shutil.ignore_patterns('.venv','__pycache__','*.pyc','*.npz'))
            try:
                r=subprocess.run([sys.executable,script],cwd=work/cwd,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=320,preexec_fn=limits)
                entry.update(returncode=r.returncode,output=r.stdout,passed=r.returncode==0)
            except Exception as exc:entry.update(passed=False,error=repr(exc))
        entry['wall_seconds']=round(time.monotonic()-start,3);ok &= entry['passed'];output['checks'].append(entry)
        print('PASS' if entry['passed'] else 'FAIL',cwd,script,entry['wall_seconds'],flush=True)
        path=ROOT/args.output;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(output,indent=2)+'\n')
    output.update(all_passed=ok,utc_finished=datetime.datetime.now(datetime.timezone.utc).isoformat());path.write_text(json.dumps(output,indent=2)+'\n');return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
