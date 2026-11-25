#!/usr/bin/env python3
"""Isolated replay of frozen Oct26 extensions; analytic scopes remain in theorem docs."""
from pathlib import Path
import argparse,json,shutil,tempfile,subprocess,time,os,sys,shlex
from materialize_replay_assets import materialize
from run_phase3_checks import limits
ROOT=Path(__file__).resolve().parent

def tasks():
 out=[]
 def add(group,base,cmd):out.append((group,base,cmd))
 q='symmetric-quantum-codes/checkpoints/2026-10-26-all-t-volume'
 for cmd in ['check_no_perfect_rank_two.py','independent/check_perfect_spin_codes_independent.py']:add('quantum',q,cmd)
 for cmd in ['check_spin_hamming.py','independent/check_racah_kernel_moments.py','independent/check_quantum_critical_escape_polynomial.py','independent/check_quantum_lp_length_monotonicity.py']:add('quantum',q+'/volume_dependency',cmd)
 h='hss-probe-reuse/checkpoints/2026-10-26-scalar-mixing'
 for cmd in ['verify_uniform_mixing_two_step_exact.py','verify_branch_doob_exact.py','verify_one_bank_output_signs_exact.py','verify_correlated_sector_signs_exact.py','verify_anchor_inverse_identity_exact.py','test_uniform_mixing_fixed_basis.py','test_complex_scalar_gauge.py']:add('hss',h,cmd)
 h='hss-probe-reuse/checkpoints/2026-10-26-structural-controls'
 for cmd in ['verify_matrix_branch_flux_exact.py','verify_one_bank_phase_cycle_physical.py','verify_one_bank_conditional_obstruction.py','advisor/check_hss_matrix_flux_independent.py','advisor/check_hss_one_bank_obstruction_independent.py']:add('hss',h,cmd)
 c='seven-cycle-capacity/checkpoints/'
 add('c7',c+'checkpoint_fiber_gate_20261026/physical_iteration','verify_c30_fiber_pair_gate.py');add('c7',c+'checkpoint_fiber_gate_20261026/independent_advisor','check_relocated.py')
 add('c7',c+'checkpoint_reservoir_gates_20261026/physical_iteration','verify_reservoir_matching_gate.py --compact');add('c7',c+'checkpoint_reservoir_gates_20261026/independent_advisor','check_relocated.py')
 for cmd in ['physical_iteration/verify_multireservoir_final.py','advisor/check_c7_multireservoir_portable.py']:add('c7',c+'checkpoint_multireservoir_gate_20261026',cmd)
 # Last two checks deliberately share one isolated packet because the advisor seed check consumes the Hall check output.
 for cmd in ['physical_iteration/verify_hall_shadow_seed.py','advisor/check_c7_attachment_hall_independent.py','advisor/check_c7_hall_seed_independent.py','physical_iteration/reservoir_escape_gate.py --output diagnostic_control.json.gz']:add('c7',c+'checkpoint_multireservoir_diagnosis_20261026',cmd)
 for cmd in ['advisor/check_c7_circular_range_independent.py','advisor/check_c7_abelian_subgroups_independent.py']:add('c7',c+'checkpoint_finite_subgroup_gate_20261026',cmd)
 add('deletion','deletion-code-optimality/checkpoints/root-exclusions-2026-10-26','replay.py')
 for cmd in ['check_phase_twisted_gnu.py','independent/check_quantum_phase_gnu_independent.py']:add('quantum','symmetric-quantum-codes/checkpoints/2026-10-26-phase-twisted-gnu',cmd)
 for cmd in ['phase7/actual_floor/verify_actual_floor.py','phase4/retune_two/verify_independent.py','phase4/retune_two/verify_active_face.py']:add('packing','online-bin-packing',cmd)
 for cmd in ['check_packing_actual_floor_independent.py','check_packing_retune_two.py']:add('packing','advisor/phase3',cmd)
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--only',choices=['quantum','hss','c7','packing','deletion']);ap.add_argument('--output',default='integration/2026-10-26/replay_local.json');a=ap.parse_args()
 if not __debug__:raise SystemExit('Assertions required.')
 env=os.environ.copy();env.update(PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1');env.pop('PYTHONOPTIMIZE',None)
 out={'all_passed':True,'network_used':False,'checks':[]}
 with tempfile.TemporaryDirectory(prefix='research-oct26-') as td:
  r=Path(td)/'research';shutil.copytree(ROOT,r,ignore=shutil.ignore_patterns('__pycache__','*.pyc','.venv'));materialize(r)
  for p in r.rglob('*'):
   if p.is_file():p.chmod(0o644)
  for group,cwd,cmd in tasks():
   if a.only and group!=a.only:continue
   start=time.monotonic()
   try:
    p=subprocess.run([sys.executable,*shlex.split(cmd)],cwd=r/cwd,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=400,preexec_fn=limits);row={'group':group,'cwd':cwd,'command':'python '+cmd,'passed':p.returncode==0,'returncode':p.returncode,'output':p.stdout}
   except Exception as e:row={'group':group,'cwd':cwd,'command':cmd,'passed':False,'error':repr(e)}
   row['seconds']=time.monotonic()-start;out['checks'].append(row);out['all_passed'] &= row['passed'];print('PASS' if row['passed'] else 'FAIL',group,cmd,round(row['seconds'],2),flush=True)
   dest=ROOT/a.output;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(out,indent=2)+'\n')
 return 0 if out['all_passed'] else 1
if __name__=='__main__':raise SystemExit(main())
