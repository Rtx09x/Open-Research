#!/usr/bin/env python3
"""Ensure selected corruptions are rejected, in temporary copies only."""
from pathlib import Path
import datetime,json,os,shutil,subprocess,sys,tempfile
from run_phase2_checks import limits
ROOT=Path(__file__).resolve().parent
if not __debug__:raise SystemExit('Assertions must remain enabled.')
env=os.environ.copy();env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None)
cases=[('packing_false_upper','online-bin-packing','phase2/best_fit/best_fit_certificate.json','phase2/best_fit/verify_step_independent.py'),('packing_source_binding','online-bin-packing','phase2/single_threshold_certificate.json','phase2/best_fit/verify_step_independent.py'),('quantum_negative_multiplier','symmetric-quantum-codes','phase2/interval_dual_candidate.json','phase2/check_interval_dual.py'),('quantum_wrong_gram_factor','symmetric-quantum-codes','phase2/interval_dual_candidate.json','phase2/check_interval_dual.py')]
rows=[]
for name,track,artifact,checker in cases:
    with tempfile.TemporaryDirectory(prefix='phase2-negative-') as tmp:
        work=Path(tmp)/track;shutil.copytree(ROOT/track,work,ignore=shutil.ignore_patterns('.venv','__pycache__','*.npz','*.pyc'))
        path=work/artifact;data=json.loads(path.read_text())
        if name=='packing_false_upper':data['target']='1'
        elif name=='packing_source_binding':data['target']='0'
        elif name=='quantum_negative_multiplier':data['enumerator_inequality_dual'][0]=-1
        else:data['ordinary_PSD'][0]['factor'][0][0]+=100*data['scale']
        path.write_text(json.dumps(data))
        r=subprocess.run([sys.executable,checker],cwd=work,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=320,preexec_fn=limits)
        rejected=r.returncode!=0 and 'AssertionError' in r.stdout and 'ModuleNotFoundError' not in r.stdout and 'FileNotFoundError' not in r.stdout
        row={'case':name,'checker':track+'/'+checker,'rejected_by_assertion':rejected,'returncode':r.returncode,'output_tail':r.stdout[-1500:]};rows.append(row)
        print('PASS' if rejected else 'FAIL',name,flush=True)
        assert rejected,row
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_rejected':True,'scope':'four selected negative controls; not exhaustive correctness or security testing','cases':rows}
p=ROOT/'integration/phase2/negative_controls.json';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2)+'\n')
