"""Adversarial regression tests for the audit extension (standard library only)."""
from pathlib import Path
import unittest,json,copy
from fractions import Fraction as F
from itertools import product
from independent import Device,from_legacy,verify_device,sweep,geometry,InvalidDynamics
from validate_model import validate,UnverifiedModel
from resources import independent_minimum,independent_machine,reset_frontier,reset_construct,explicit_device,required_terms,dp_terms
from sparse import sparse_unary
from structural_bounds import weight_hall_bound,nonnegative_onehot_bound
from synthesis import Problem,verify_certificate,phase_options
from exact_elimination import solve_exact
from encoding_search import encodings,unrestricted_minimum,SearchLimit
from complete_bands import finish
R=Path(__file__).resolve().parents[1]/'results'

class AuditTests(unittest.TestCase):
    def test_seven_state_quadratic(self):
        from seven_state_separation import quadratic_model
        m=quadratic_model();self.assertEqual(validate(m)['trials'],7)
        self.assertEqual(sum(t['mask']!=0 for row in m['up'] for t in row),7)
    def test_seven_state_two_term(self):
        from seven_state_separation import five_bit_two_term_model
        m=five_bit_two_term_model();self.assertGreater(validate(m)['band_gap'],0)
        self.assertEqual(sum(t['mask']!=0 for row in m['up'] for t in row),2)
    def test_seven_state_forced_geometry(self):
        from seven_state_separation import check_forced_geometry
        self.assertEqual(check_forced_geometry()['geometrically_valid'],36)
    def test_seven_state_remove_xor_term(self):
        from seven_state_separation import quadratic_model
        m=quadratic_model()
        for b in ('up','down'):m[b][0]=[t for t in m[b][0] if t['mask']!=6]
        with self.assertRaises(ValueError):validate(m)
    def test_reset_weighted_incidence_minimum(self):
        from resources import reset_incidence_minimum
        self.assertEqual(reset_incidence_minimum(37,11),30)
        for d in (1,2,3,6):
            m=reset_construct(37,11,d)
            self.assertEqual(sum(t['mask'].bit_count() for row in m['down'] for t in row),30)
        self.assertEqual(reset_incidence_minimum(37,36),0)
    def test_negative_span_is_rejected(self):
        m=json.loads((R/'negative_span_counterexample.json').read_text())
        verify_device(from_legacy(m))
        with self.assertRaisesRegex(InvalidDynamics,'nonpositive span'):validate(m)
    def test_good_reset(self):self.assertTrue(validate(reset_construct(37,11,2))['global_model_valid'])
    def test_zero_dimension_identity(self):self.assertEqual(validate(independent_machine([0]))['trials'],1)
    def test_duplicate_codes(self):
        m=independent_machine([0,1]);m['codes']=[0,0]
        with self.assertRaises(ValueError):validate(m)
    def test_invalid_target(self):
        m=independent_machine([0,0]);m['f'][1]=99
        with self.assertRaises(ValueError):validate(m)
    def test_float_threshold_rejected(self):
        m=independent_machine([0,0]);m['a'][0]=2.0
        with self.assertRaises(ValueError):validate(m)
    def test_boolean_dimension_rejected(self):
        m=independent_machine([0,0]);m['n']=True
        with self.assertRaises(ValueError):validate(m)
    def test_invalid_scale(self):
        m=independent_machine([0,0]);m['scale']=0
        with self.assertRaises(ValueError):validate(m)
    def test_reversed_endpoints(self):
        m=independent_machine([0,0]);m['highs']=[-1]
        with self.assertRaises(ValueError):validate(m)
    def test_self_coupling_rejected(self):
        m=sparse_unary([1,2,0]);m['J'][0][0]=1
        with self.assertRaises(ValueError):validate(m)
    def test_self_polynomial_rejected(self):
        m=reset_construct(5,3,2);m['up'][0].append({'mask':1,'coefficient':1})
        with self.assertRaises(ValueError):validate(m)
    def test_duplicate_term_rejected(self):
        m=reset_construct(5,3,2);m['up'][0].append(copy.deepcopy(m['up'][0][0]))
        with self.assertRaises(ValueError):validate(m)
    def test_wrong_successor_rejected(self):
        m=sparse_unary([1,2,0]);m['f']=[2,0,1]
        with self.assertRaises(ValueError):validate(m)
    def test_endpoint_tie_rejected(self):
        m=independent_machine([0,0]);m['highs']=[2*m['scale']+1]
        with self.assertRaisesRegex(InvalidDynamics,'endpoint'):validate(m)
    def test_tied_winner_rejected(self):
        d=Device(2,0,[10],1,lambda i,s,u:5 if u else -2,[0],[0])
        with self.assertRaisesRegex(InvalidDynamics,'tie'):verify_device(d)
    def test_second_flip_budget(self):
        d=Device(2,0,[10],1,lambda i,s,u:(4+i if u else -2-i),[0],[0])
        with self.assertRaisesRegex(InvalidDynamics,'budget'):verify_device(d)
    def test_fixed_excursion_is_allowed(self):
        d=Device(1,0,[4],1,lambda i,s,u:3 if u else 1,[0],[0])
        self.assertEqual(len(sweep(d,0)['events']),2);verify_device(d,full=True)
    def test_fixed_phase_enumeration(self):self.assertEqual(len(list(phase_options([0],[0],2))),3)
    def test_two_cycle_geometry_rejected(self):self.assertFalse(geometry([1,2],[1,0],2))
    def test_two_cycle_sparse_rejected(self):
        with self.assertRaises(ValueError):sparse_unary([1,0])
    def test_zero_coupling_nonidempotent(self):self.assertIsNone(independent_minimum([0,0,1]))
    def test_zero_coupling_formula(self):self.assertEqual(independent_minimum([0,0,0,3,3,5]),4)
    def test_reset_zero_coupling_limit(self):
        self.assertIsNone(reset_frontier(37,35,0));self.assertEqual(reset_frontier(37,36,0)['terms'],0)
    def test_reset_minimum_bits(self):self.assertIsNone(reset_frontier(37,10,6))
    def test_reset_frontier_values(self):
        self.assertEqual([reset_frontier(37,11,d)['terms'] for d in (1,2,3,6)],[30,15,10,5])
    def test_coverage_dp(self):
        for k in range(1,5):
            for e in range(4):
                for d in range(1,5):
                    for q in range(k*e+1):self.assertEqual(required_terms(q,k,e,d),dp_terms(q,k,e,d))
    def test_sparse_support_bound(self):
        for f in product(range(4),repeat=4):
            if any(i!=t and f[t]==i for i,t in enumerate(f)):continue
            m=sparse_unary(list(f));validate(m)
            self.assertLessEqual(m['nonzero_directed_influences'],3*m['nonfixed_edges'])
    def test_large_symbolic_span(self):
        self.assertIn('symbolic',validate(sparse_unary(list(range(1,100))+[0]))['global_validation_method'])
    def test_unknown_large_span_not_silently_accepted(self):
        n=14;m={'kind':'explicit_polynomial','n':n,'scale':1,'low':0,'highs':[1],
                'codes':[0],'f':[0],'up':[[{'mask':0,'coefficient':4}]+([{'mask':2,'coefficient':1}] if i==0 else []) for i in range(n)],
                'down':[[{'mask':0,'coefficient':-2}] for _ in range(n)]}
        with self.assertRaises(UnverifiedModel):validate(m)
    def test_packing_obstruction(self):
        r=weight_hall_bound([0,0,0,1,2],3);self.assertEqual((r['demand'],r['capacity']),(4,3))
    def test_four_bit_packing_example(self):self.assertEqual(unrestricted_minimum([0,0,0,1,2])['minimum'],4)
    def test_inhibitory_onehot_bound(self):self.assertEqual(nonnegative_onehot_bound(100),4900)
    def test_fresh_decimal_duals(self):
        for c in json.loads((R/'fresh_decimal_duals.json').read_text())['certificates']:verify_certificate(c)
    def test_corrupted_dual_rejected(self):
        c=json.loads((R/'fresh_decimal_duals.json').read_text())['certificates'][0]
        c['dual']={}
        with self.assertRaisesRegex(ValueError,'dual'):verify_certificate(c)
    def test_negative_dual_rejected(self):
        c=json.loads((R/'fresh_decimal_duals.json').read_text())['certificates'][0]
        k=next(iter(c['dual']));c['dual'][k]='-1'
        with self.assertRaises(ValueError):verify_certificate(c)
    def test_corrupted_primal_rejected(self):
        c=json.loads((R/'cycle_n6_q15_d1_c0_u0_p1.json').read_text());c['primal']=['0']*len(c['primal'])
        with self.assertRaisesRegex(ValueError,'primal'):verify_certificate(c)
    def test_fingerprint_rejected(self):
        c=json.loads((R/'cycle_n6_q15_d1_c0_u0_p1.json').read_text());c['fingerprint']='changed'
        with self.assertRaisesRegex(ValueError,'fingerprint'):verify_certificate(c)
    def test_unresolved_not_certificate(self):
        c=json.loads((R/'cycle_n6_q15_d1_c0_u0_p1.json').read_text());c['status']='unresolved'
        with self.assertRaisesRegex(ValueError,'Unresolved'):verify_certificate(c)
    def test_exact_elimination_feasible(self):
        p=Problem([1,0],[0,0],1,0);c=solve_exact(p);self.assertEqual(c['status'],'feasible');verify_certificate(c)
    def test_exact_elimination_infeasible(self):
        p=Problem([1,2,4],[1,2,0],3,0);c=solve_exact(p);self.assertEqual(c['status'],'infeasible');verify_certificate(c)
    def test_elimination_cap_not_impossibility(self):
        p=Problem([1,0,2],[0,0,0],2,1);c=solve_exact(p,max_rows=0)
        self.assertEqual(c['status'],'unresolved')
    def test_geometry_cap_not_impossibility(self):
        r=unrestricted_minimum([1,2,0],limit=0);self.assertEqual(r['status'],'unresolved')
    def test_band_completed_cycles(self):
        for r in json.loads((R/'improved_cycle_constructions.json').read_text()):
            c=validate(json.loads((R/r['file']).read_text()));self.assertGreater(c['band_gap'],0)
    def test_support_mask_restriction(self):
        p=Problem([1,2,4],[1,2,0],3,1,support=[]);c=solve_exact(p)
        self.assertEqual(c['status'],'infeasible');verify_certificate(c)

if __name__=='__main__':unittest.main(verbosity=2)
