#!/usr/bin/env python3
"""Small regression and negative-control suite for the exact verifier."""
from __future__ import annotations
import copy
from fractions import Fraction as F
from math import comb
import unittest
import verify


class ExactVerifierTests(unittest.TestCase):
    def test_main_constructions(self):
        for make, n, delta in [(verify.six_model, 6, F(247, 50)),
                               (verify.five_model, 5, F(19, 20))]:
            d = verify.model_check(make())
            self.assertEqual(d['period'], 10)
            self.assertEqual(d['n'], n)
            self.assertEqual(F(d['minimum_trace_margin']), delta)

    def test_matching_and_dual_proofs(self):
        self.assertEqual(verify.matching_check()['total_matchings'], 60)
        self.assertEqual(verify.dual_check()['exact_dual_certificates'], 16)

    def test_wrong_peak_is_rejected(self):
        d = verify.six_model(); d['high'] = '1'
        with self.assertRaises(AssertionError):
            verify.model_check(d)

    def test_modified_parameter_is_rejected(self):
        d = verify.six_model(); d['a'][0] = '1000'
        with self.assertRaises(AssertionError):
            verify.model_check(d)

    def test_repeated_vertex_is_rejected(self):
        d = verify.five_model(); d['path'][2] = d['path'][0]
        with self.assertRaises(AssertionError):
            verify.model_check(d)

    def test_tied_candidate_is_rejected(self):
        d = verify.five_model()
        # At initial low {1,2}, intended add is 3. Make 4 tie with its field.
        initial = d['path'][0]
        t3 = verify.threshold(d, 2, initial, True)
        t4 = verify.threshold(d, 3, initial, True)
        d['a'][3] = str(F(d['a'][3]) + t3 - t4)
        with self.assertRaises(AssertionError):
            verify.leg(d, initial, F(0), F(13))

    def test_high_n_offsets_remain_bounded(self):
        n = 25; path = []
        for i in range(n):
            path += [1 << i, (1 << i) | (1 << ((i+1) % n))]
        d = verify.compile_cycle(n, path, 'offset_regression')
        offsets = [F(b) + 2 for b in d['b']]
        self.assertTrue(all(F(0) < e < F(1,4) for e in offsets))
        self.assertEqual(len(set(offsets)), n)
        # Do not enumerate the 2^25 global states for this offset-only test.

    def test_capacity_closed_form(self):
        for n in range(3, 51):
            direct = max(min(comb(n,k), comb(n,k+1)) for k in range(n))
            self.assertEqual(direct, comb(n, (n-1)//2))

    def test_invalid_compiler_input(self):
        with self.assertRaises(AssertionError):
            verify.compile_cycle(3, [1, 3, 2, 6, 4, 9], 'invalid')

if __name__ == '__main__':
    unittest.main(verbosity=2)
