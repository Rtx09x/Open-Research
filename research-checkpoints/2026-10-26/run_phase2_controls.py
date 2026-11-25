#!/usr/bin/env python3
"""Optional isolated supplementary controls; none replaces the analytic proofs."""
from pathlib import Path
import datetime,json,os,shutil,subprocess,sys,tempfile,time
from run_phase2_checks import limits
ROOT=Path(__file__).resolve().parent
if not __debug__:raise SystemExit('Assertions must remain enabled.')
env=os.environ.copy();env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None)
jobs=[['advisor/phase2/'+x] for x in ('check_local_casimir.py','check_three_copy_pair_map.py','check_spinor_compression.py','check_quaternion_invariant.py','check_rational_moment_export.py')]
jobs += [['symmetric-quantum-codes/phase2/'+x] for x in ('check_ppt_recoupling.py','orientation_exact.py','spinor_exact_controls.py')]
jobs += [['quantum-independent-audit/complex_projector_controls.py'],['quantum-independent-audit/generic_n18_control.py'],['symmetric-quantum-codes/phase2/three_copy_known19_direct.py','quantum-independent-audit/replay_all_cones.py']]
rows=[];ok=True
for scripts in jobs:
    start=time.monotonic();row={'scripts':scripts,'scope':'supplemental exact algebra or numerical model controls; not an exclusion proof','executions':[]}
    with tempfile.TemporaryDirectory(prefix='phase2-control-') as tmp:
        work=Path(tmp)/'research';work.mkdir()
        for group in ('symmetric-quantum-codes','quantum-independent-audit','advisor'):
            shutil.copytree(ROOT/group,work/group,ignore=shutil.ignore_patterns('.venv','__pycache__','*.npz','*.pyc'))
        for script in scripts:
            p=work/script
            try:
                r=subprocess.run([sys.executable,str(p)],cwd=p.parent,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=320,preexec_fn=limits)
                passed=r.returncode==0;row['executions'].append({'script':script,'returncode':r.returncode,'output':r.stdout,'passed':passed})
            except Exception as exc:passed=False;row['executions'].append({'script':script,'error':repr(exc),'passed':False})
            if not passed:break
    row['passed']=all(x['passed'] for x in row['executions']) and len(row['executions'])==len(scripts);ok &= row['passed'];row['seconds']=round(time.monotonic()-start,3);rows.append(row)
    print('PASS' if row['passed'] else 'FAIL','; '.join(scripts),row['seconds'],flush=True)
    out={'all_passed':ok,'controls':rows,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'network_used':False,'scope':'supplemental original-model controls, distinct from the standalone rigorous verifiers'}
    (ROOT/'integration/phase2/supplemental_controls.json').write_text(json.dumps(out,indent=2)+'\n')
raise SystemExit(0 if ok else 1)
