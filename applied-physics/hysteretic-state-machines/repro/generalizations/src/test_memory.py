"""Regression tests include intentionally broken inputs and designs."""
import copy,json,unittest
from pathlib import Path
from memory import *
from minimize import minimize
from cycle_operations import *
R=Path(__file__).resolve().parents[1]/'results'


def raw(m):
    r={'kind':'raw','n':m['n'],'scale':m['scale'],'low':m['low'],'highs':list(m['highs'])}
    for name,up in [('plus',True),('minus',False)]:
        r[name]=[[threshold(m,i,s,up) for s in range(1<<m['n'])] for i in range(m['n'])]
    return r


class MemoryTests(unittest.TestCase):
    def test_two_cycle_rejected(self):
        for f in ([1,0],[1,2,1],[0,2,1,0]):
            with self.assertRaises(ValueError):one_hot(f)
            self.assertIsNone(minimize(f)['minimum'])
    def test_ambiguous_peak_rejected(self):
        with self.assertRaises(ValueError):code_certificate([1,2],[1,0],2)
    def test_add_only_nonfixed_rejected(self):
        with self.assertRaises(ValueError):code_certificate([0,1,3],[1,2,2],2)
    def test_descending_peak_cannot_be_code(self):
        with self.assertRaises(ValueError):code_certificate([1,2,3],[1,1,2],2)
    def test_zero_switch_identity(self):
        info=minimize([0]);self.assertEqual(info['minimum'],0)
        self.assertEqual(check_machine(table_compile([0],[0],0))['trials'],1)
    def test_wrong_expected_transition(self):
        m=one_hot([1,2,0]);m['f'][0]=0
        with self.assertRaises(ValueError):check_machine(m)
    def test_wrong_coupling(self):
        m=one_hot([1,2,0]);m['J'][1][0]=1000
        with self.assertRaises(ValueError):check_machine(m)
    def test_endpoint_tie(self):
        m=one_hot([1,2,0]);m['highs'][0]=threshold(m,1,1,True)
        with self.assertRaises(ValueError):pulse(m,1)
    def test_candidate_tie(self):
        m=raw(one_hot([1,2,0]));m['plus'][2][1]=m['plus'][1][1]
        with self.assertRaises(ValueError):pulse(m,1)
    def test_second_up_flip_rejected(self):
        m=raw(one_hot([1,2,0]));m['plus'][2][3]=m['highs'][0]-1
        with self.assertRaises(ValueError):pulse(m,1)
    def test_input_branching_rejected(self):
        with self.assertRaises(ValueError):amplitude_compile([[1,2],[1,1],[2,2]])
    def test_nonmonotone_gate_rejected(self):
        with self.assertRaises(ValueError):amplitude_compile([[1,0],[1,1]])
    def test_counter_lift_boundary(self):
        p=one_hot_cycle(3)
        for q in range(3,8):check_machine(model(5,lift(3,p,q)))
        for q in (2,8):
            with self.assertRaises(ValueError):lift(3,p,q)
    def test_repeated_cycle_vertex(self):
        p=one_hot_cycle(3);p[-1]=p[1]
        with self.assertRaises(ValueError):validate_cycle(3,p)
    def test_bad_join_layers(self):
        with self.assertRaises(ValueError):join(3,one_hot_cycle(3),one_hot_cycle(3))
    def test_saturating_margin_and_span(self):
        m=cycle_model(31);r=check_machine(m)
        self.assertGreater(8*r['minimum_slack_numerator'],7*m['scale'])
        for i in range(m['n']):self.assertEqual(threshold(m,i,0,True)-threshold(m,i,0,False),6*m['scale'])
    def test_polynomial_local_band_option(self):
        m=cycle_model(15,False,False);check_machine(m)
        self.assertFalse(m['global_band_guarantee']);self.assertEqual(m['a'][0],4)
    def test_distinct_task_minima(self):
        self.assertEqual(minimize([0,0,0])['minimum'],2)
        self.assertEqual(minimize([1,2,2])['minimum'],3)
        self.assertEqual(minimize([0,0,1,1])['minimum'],4)
    def test_thousand_counter(self):
        m=json.loads((R/'counter_1000_13_saturated.json').read_text())
        self.assertEqual(m['n'],13);self.assertEqual(check_machine(m)['trials'],1000)
    def test_fsm_family_sizes(self):
        for d in (1,2,33):check_machine(broom_machine(d))
        for n in (1,5,11):
            m=reset_machine(n);self.assertEqual(len(m['codes']),1+(n+1)**2//4)

if __name__=='__main__':unittest.main(verbosity=2)
