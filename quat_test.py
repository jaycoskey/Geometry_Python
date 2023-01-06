#!/usr/bin/env python

import unittest

from quat import Quat, QRHAT, QIHAT, QJHAT, QKHAT
from quat import qexp, qlog, qpow, qslerp
from util import eq_approx


class QuatTest(unittest.TestCase):
    def test_add(self):
        expected = Quat(0.0, 1.0, 1.0, 0.0)
        actual = QIHAT + QJHAT
        self.assertTrue(eq_approx(expected, actual))

    def test_conjugation(self):
        pass

    def test_constructors(self):
        pass

    def test_exp_and_log(self):
        ii = qpow(QIHAT, 2.0)
        jj = qpow(QJHAT, 2.0)
        kk = qpow(QKHAT, 2.0)

        self.assertTrue(eq_approx(ii, -QRHAT))
        self.assertTrue(eq_approx(jj, -QRHAT))
        self.assertTrue(eq_approx(kk, -QRHAT))

        def assert_el_eq_le(q):
            el = qexp(qlog(q))
            le = qlog(qexp(q))
            self.assertTrue(eq_approx(el, le))

        assert_el_eq_le(QRHAT)
        assert_el_eq_le(QIHAT)
        assert_el_eq_le(QJHAT)
        assert_el_eq_le(QKHAT)

    def test_inverse(self):
        pass

    def test_mul(self):
        ii = QIHAT * QIHAT
        ij = QIHAT * QJHAT
        ik = QIHAT * QKHAT

        ji = QJHAT * QIHAT
        jj = QJHAT * QJHAT
        jk = QJHAT * QKHAT

        ki = QKHAT * QIHAT
        kj = QKHAT * QJHAT
        kk = QKHAT * QKHAT

        self.assertTrue(eq_approx(ii, -QRHAT))
        self.assertTrue(eq_approx(ij,  QKHAT))
        self.assertTrue(eq_approx(ik, -QJHAT))

        self.assertTrue(eq_approx(ji, -QKHAT))
        self.assertTrue(eq_approx(jj, -QRHAT))
        self.assertTrue(eq_approx(jk,  QIHAT))

        self.assertTrue(eq_approx(ki,  QJHAT))
        self.assertTrue(eq_approx(kj, -QIHAT))
        self.assertTrue(eq_approx(kk, -QRHAT))

    def test_sub(self):
        pass

    def test_slerp(self):
        pass

    def test_str(self):
        pass

    def test_sub(self):
        expected = Quat(0.0, 1.0, -1.0, 0.0)
        actual = QIHAT - QJHAT
        self.assertTrue(eq_approx(expected, actual))

    def test_truediv(self):
        expected = 0.5 * QIHAT
        actual = QIHAT / 2
        self.assertTrue(eq_approx(expected, actual))

    def test_as_vec3(self):
        pass


if __name__ == '__main__':
    unittest.main()
