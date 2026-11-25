"""Artifact consistency checks; these do not replace the mathematical proofs."""
import json,math,pathlib
p=pathlib.Path(__file__).resolve().parent
read=lambda name:json.loads((p/name).read_text())
x=read('exact_tree_results.json')
assert x[0]['sign_assignments']==256 and x[1]['sign_assignments']==65536
for a in x[:2]:assert a['identity_pass'] and a['total_integer_squared_error']==a['sign_assignments']*a['exact_expected_error']
for a in x[2:]:assert a['sharp_error']==2*a['L']+2 and a['full_HSS_optimal_error']==0
for a in read('baseline_results.json'):
 assert a['queries']==12*a['k']
 assert a['rank_tail']<1e-8
 if a['noise']==0:assert a['mean_relerr']<1e-10
for a in read('tree_flow_results.json'):
 assert a['rank_tail']<1e-8 and a['exact_error']<1e-10
 assert a['predicted']<=a['bound']+1e-8
for a in read('dependency_results.json'):
 assert a['covariance']>0 and abs(a['X_variance']-.125)<.002
 assert abs(a['covariance']-a['theory_from_gap'])<.02
z=read('exact_conditional_operator_results.json')[-1]
assert z['difference_extrema'][1]>.1
assert z['cross_extrema'][0]<-.07
assert abs(z['max_after']-2)<1e-9
print('PASS: query counts, exact finite-sign identities, HSS rank checks, dependence controls, and failed-potential-route flags are consistent.')
print('NOT CLAIMED: full RE-02; dense fixed-basis variance theorem; exact arithmetic certification of floating-point spectra; novelty.')
