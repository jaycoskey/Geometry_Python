#!/usr/bin/env python

import unittest

from util import eq_approx
from vec3 import Vec3, XHAT, YHAT, ZHAT


class Vec3Test(unittest.TestCase):
    def test_add(self):
        expected = Vec3(1.0, 1.0, 0.0)
        actual = XHAT + YHAT
        self.assertTrue(eq_approx(expected, actual))

    def test_mul(self):
        expected = Vec3(5.0, 0.0, 0.0)
        actual = 5 * XHAT
        self.assertTrue(eq_approx(expected, actual))

    def test_sub(self):
        expected = Vec3(1.0, -1.0, 0.0)
        actual = XHAT - YHAT
        self.assertTrue(eq_approx(expected, actual))

    def test_truediv(self):
        expected = Vec3(0.5, 0.0, 0.0)
        actual = XHAT / 2
        self.assertTrue(eq_approx(expected, actual))

    def test_truediv_by_zero(self):
        pass

    def test_dot(self):
        expected = ZHAT
        actual = XHAT.cross(YHAT)
        self.assertTrue(eq_approx(expected, actual))

    def test_cross(self):
        expected = ZHAT
        actual = XHAT.cross(YHAT)
        self.assertTrue(eq_approx(expected, actual))


if __name__ == '__main__':
    unittest.main()
