#!/usr/bin/env python3
"""Corrupt only disposable copies and require the mathematical checker to reject."""
from pathlib import Path
import json,shutil,sys,tempfile,subprocess,time,os,argparse
ROOT=Path(__file__).resolve().parent
from run_phase3_checks import limits

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',default='integration/phase3/negative_controls_local.json');a=ap.parse_args()
 if not __debug__:raise SystemExit('Assertions required.')
 cases=[('packing_false_target','online-bin-packing/phase3/successor_mixture/successor_mixture_certificate.json','online-bin-packing/phase3/successor_mixture','verify_independent.py'),('quantum_negative_multiplier','symmetric-quantum-codes/phase3/general_dual_n34_t3.json','symmetric-quantum-codes/phase3','check_general_dual_tight.py 34 3'),('c7_duplicate_word','seven-cycle-capacity/phase3/physical_iteration/new_367_core_escape.json','seven-cycle-capacity/phase3/independent_advisor','check_c7_escape_independent.py'),('deletion_corrupted_part','deletion-code-optimality/phase2/certificate_bundle_k6/parts/part-000.bin','deletion-code-optimality/phase2','replay_k6.py')];out={'all_rejected':True,'checks':[]}
 env=os.environ.copy();env.update(PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1');env.pop('PYTHONOPTIMIZE',None)
 for name,target,cwd,cmd in cases:
  with tempfile.TemporaryDirectory(prefix='research-p3-corrupt-') as td:
   r=Path(td);start=time.monotonic()
   for folder in ['online-bin-packing','symmetric-quantum-codes','seven-cycle-capacity','deletion-code-optimality','advisor']:shutil.copytree(ROOT/folder,r/folder)
   for p in r.rglob('*'):
    if p.is_file():p.chmod(0o644)
   p=r/target
   if name=='deletion_corrupted_part':b=bytearray(p.read_bytes());b[0]^=1;p.write_bytes(b)
   else:
    d=json.loads(p.read_text())
    if name=='packing_false_target':d['target']='1'
    elif name=='quantum_negative_multiplier':d['enumerator_inequality_dual'][0]=-1
    else:d['code'][1]=d['code'][0]
    p.write_text(json.dumps(d))
   result=subprocess.run([sys.executable,*cmd.split()],cwd=r/cwd,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=400,preexec_fn=limits)
   passed=result.returncode!=0 and ('AssertionError' in result.stdout or 'hash' in result.stdout.lower())
   out['checks'].append({'name':name,'rejected':passed,'returncode':result.returncode,'seconds':time.monotonic()-start,'output':result.stdout});out['all_rejected'] &= passed
   print(name,'PASS' if passed else 'FAIL',flush=True)
 p=ROOT/a.output;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2)+'\n');return 0 if out['all_rejected'] else 1
if __name__=='__main__':raise SystemExit(main())
