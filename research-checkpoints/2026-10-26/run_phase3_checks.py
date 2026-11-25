#!/usr/bin/env python3
"""Isolated cloud-checkpoint replay; no discovery solvers or network requests."""
from pathlib import Path
import argparse,datetime,json,os,resource,shutil,subprocess,sys,tempfile,time,shlex,hashlib
ROOT=Path(__file__).resolve().parent

def limits(cpu=300):
 resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3));resource.setrlimit(resource.RLIMIT_CPU,(cpu,cpu+5))
 if hasattr(os,'sched_setaffinity'):os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})

def tasks(slow=False):
 out=[]
 def add(group,cwd,command,scope,cpu=300):out.append((group,cwd,command,scope,cpu))
 for f in ['lower_shared/verify_shared_fork.py','successor_mixture/check_all.py','successor_mixture/verify_independent.py','successor_mixture/verify_family.py','successor_mixture/check_chronology.py','successor_mixture/check_mixed_chronology.py']:
  add('packing','online-bin-packing','phase3/'+f,'exact certificate or finite chronology control; universal applicability is analytic')
 add('packing','advisor/phase3','check_packing_successor_mixture.py','independent all402/804 exact pricing, integrated source-derived facts')
 add('deletion','deletion-code-optimality/phase2','replay_k6.py --independent','complete868 duals/1716 supports; two implementations')
 add('deletion','deletion-code-optimality/phase2','replay_k6.py --negative','deliberately omitted canonical support must be rejected')
 base='deletion-code-optimality/continuation/release_20261025'
 for f in ['scripts/verify_cg_hierarchy.py evidence/best_dual.json','scripts/verify_fractional_root.py','scripts/negative_controls.py']:
  add('deletion',base,f,'exact global upper/fractional relaxation and deliberate corruptions; integer interval remains316–320')
 add('deletion','advisor/phase3','check_deletion_cg_independent.py ../../'+base+'/evidence/best_dual.json','independent4096-word transport and exact CG dual')
 for f in ['verify.py','negative_controls.py']:add('deletion','deletion-code-optimality/continuation/barrier26_release_20261025',f,'exact fractional selected-integrality obstruction and four corruptions; not a code')
 add('deletion','advisor/phase3','check_deletion_branch26_barrier_independent.py','independent literal-deletion geometry,155496 cliques and783CG nodes; fractional obstruction only')
 c='seven-cycle-capacity/phase3'
 for f in ['verify_core_boundary_covers.py','classify_second_boundary_maxima.py']:add('c7',c+'/physical_iteration',f,'exact restricted alphabet cover/classification; no capacity improvement')
 for f in ['check_c7_component_independent.py','check_c7_escape_independent.py','check_c7_second_boundary_independent.py']:add('c7',c+'/independent_advisor',f,'independent physical component/367-code/classification checks')
 h='hss-probe-reuse/phase3'
 for f in ['verify_triangular_regression_exact.py','verify_path_ls_gauge_exact.py','verify_dense_envelope_clique.py','verify_matrix_one_bank_bound.py','verify_wide_haar_coercivity.py','verify_greedy_coefficient_identity.py','verify_greedy_bridge_independent.py']:
  add('hss',h,f,'exact controls of restricted analytic reductions; not full RE02')
 for f in ['coordinate_observation_forest.py','coordinate_star_probing.py','verify_three_color_forest.py']:add('hss',h,f,'finite integer/block controls; not all-depth proof')
 for f in ['test_fixed_basis_algorithm.py','test_finite_orientation_variant.py','test_path_global_ls_inverse.py','test_path_global_ls_robustness.py']:add('hss',h,f,'supplemental numerical implementation/robustness controls')
 q='symmetric-quantum-codes/phase3'
 for f in ['check_reduced_t2.py','check_general_dual.py 33 3','check_general_dual_tight.py 34 3','check_non_anticoherence37.py']:add('quantum',q,f,'rigorous finite certificate arithmetic; scope/necessity in separate theorem and audits')
 for f in ['check_code37_independent.py','check_t3_scalar_hypergeom.py']:add('quantum','advisor/phase3',f,'independent exact37 root/all98KL or scalar exclusions')
 add('quantum',q,'test_logical_face_inverse.py','small-spin complex numerical algebra control, not proof')
 if slow:
  add('quantum','advisor/phase3','check_quantum_general_independent.py 33 3','independent SymPy/Arb full-spin and516KL checks; observed~15min',1800)
  add('quantum','advisor/phase3','check_quantum_general_tight_independent.py 34 3','independent SymPy/Arb full-spin and535KL checks; observed~15min',1800)
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--only',choices=['packing','deletion','c7','hss','quantum']);ap.add_argument('--slow',action='store_true');ap.add_argument('--output',default='integration/phase3/verification_local.json');a=ap.parse_args()
 if not __debug__:raise SystemExit('Assertions must remain enabled.')
 env=os.environ.copy();env.update(PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1');env.pop('PYTHONOPTIMIZE',None)
 report={'host_utc_started':datetime.datetime.now(datetime.timezone.utc).isoformat(),'network_used':False,'slow_included':a.slow,'checks':[]};ok=True
 for group,cwd,command,scope,cpu in tasks(a.slow):
  if a.only and group!=a.only:continue
  start=time.monotonic();row={'group':group,'cwd':cwd,'command':'python '+command,'scope':scope,'cpu_limit_seconds':cpu}
  with tempfile.TemporaryDirectory(prefix='research-p3-check-') as temp:
   work=Path(temp)/'research';work.mkdir()
   for folder in ['online-bin-packing','deletion-code-optimality','seven-cycle-capacity','hss-probe-reuse','symmetric-quantum-codes','advisor']:
    shutil.copytree(ROOT/folder,work/folder,ignore=shutil.ignore_patterns('__pycache__','*.pyc','.venv','*.npz'))
   for p in work.rglob('*'):
    if p.is_file():p.chmod(0o644)
   try:
    r=subprocess.run([sys.executable,*shlex.split(command)],cwd=work/cwd,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=cpu+100,preexec_fn=lambda:limits(cpu))
    row.update(passed=r.returncode==0,returncode=r.returncode,output=r.stdout)
   except Exception as e:row.update(passed=False,error=repr(e))
  row['seconds']=round(time.monotonic()-start,3);ok &= row['passed'];report['checks'].append(row)
  print('PASS' if row['passed'] else 'FAIL',group,command,row['seconds'],flush=True)
  p=ROOT/a.output;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(report,indent=2)+'\n')
 report.update(all_passed=ok,host_utc_finished=datetime.datetime.now(datetime.timezone.utc).isoformat());p.write_text(json.dumps(report,indent=2)+'\n');return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
