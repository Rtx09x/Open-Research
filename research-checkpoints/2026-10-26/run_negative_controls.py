#!/usr/bin/env python3
"""Require exact checkers to reject deliberately corrupted disposable inputs."""
from pathlib import Path
import argparse,json,os,shutil,subprocess,sys,tempfile,time
from run_checks import limits
ROOT=Path(__file__).resolve().parent

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',default='integration/negative_controls_local.json');args=p.parse_args()
    if not __debug__:raise SystemExit('Assertions must remain enabled.')
    cases=[('quantum Farkas coefficient','symmetric-quantum-codes','lp_exact_certificates.json','tests/check_quantum_farkas.py','farkas'),('HSS claimed rational mean','hss-probe-reuse','rational_potential_certificate.json','verify_rational_potential.py','hss'),('C7 inherited input vector','seven-cycle-capacity','terminal_recycled_base.json','verify_recycled_certificate.py','c7'),('AH invalid target','online-bin-packing','ah_three_parameter_full_certificate.json','verify_ah_full.py ah_three_parameter_full_certificate.json mutated_output.json','ah')]
    out=[]
    for name,track,filename,command,kind in cases:
        with tempfile.TemporaryDirectory(prefix='research-negative-') as temp:
            work=Path(temp)/track;shutil.copytree(ROOT/track,work);path=work/filename;data=json.loads(path.read_text())
            if kind=='farkas':data[0]['y'][0]='999999999'
            elif kind=='hss':data['expected_energy_increase_exact']='0'
            elif kind=='c7':data['input_vector'][0]+=1
            else:data['target']='1'
            path.write_text(json.dumps(data));start=time.monotonic()
            env=os.environ.copy();env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None)
            result=subprocess.run([sys.executable,*command.split()],cwd=work,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=320,preexec_fn=limits)
            rejected=result.returncode!=0 and 'AssertionError' in result.stdout
            out.append({'case':name,'rejected_by_assertion':rejected,'returncode':result.returncode,'wall_seconds':round(time.monotonic()-start,3),'output':result.stdout})
            print('PASS'if rejected else'FAIL',name,flush=True)
    result={'all_rejected':all(x['rejected_by_assertion']for x in out),'controls':out,'scope':'Four deliberate corruptions rejected; not exhaustive adversarial verifier testing.'}
    p=ROOT/args.output;p.parent.mkdir(exist_ok=True);p.write_text(json.dumps(result,indent=2)+'\n')
    return 0 if result['all_rejected'] else 1
if __name__=='__main__':raise SystemExit(main())
