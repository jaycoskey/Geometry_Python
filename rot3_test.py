#!/usr/bin/env python

import unittest

from math import pi

from quat import Quat
from rot3 import Rot3
from util import eq_approx, is_zero_approx
from vec3 import Vec3, XHAT, YHAT, ZHAT


class Rot3Test(unittest.TestCase):
    def test_constructors(self):
        pass

    def test_noncommutativity(self):
        axis1 = Vec3(1.0, -4.0, 9.0)
        angle1 = pi / 3
        r1 = Rot3(axis1, angle1)

        axis2 = Vec3(1.0, 4.0, 9.0)
        angle2 = pi / 6
        r2 = Rot3(axis2, angle2)

        vec = Vec3(1.0, 2.0, 3.0)
        a = r1(r2(vec))
        b = r2(r1(vec))
        self.assertFalse(is_zero_approx(a - b))

    def test_rot_x(self):
        rx = Rot3(XHAT, pi / 2)
        result = rx(YHAT)
        self.assertTrue(eq_approx(result, ZHAT))

    def test_rot_y(self):
        ry = Rot3(YHAT, pi / 2)
        result = ry(ZHAT)
        self.assertTrue(eq_approx(result, XHAT))

    def test_rot_z(self):
        rz = Rot3(ZHAT, pi / 2)
        result = rz(XHAT)
        self.assertTrue(eq_approx(result, YHAT))

    def test_rot_zero(self):
        rx0 = Rot3(XHAT, 0.0)
        ry0 = Rot3(YHAT, 0.0)
        rz0 = Rot3(ZHAT, 0.0)
        vec = Vec3(1.0, 2.0, 3.0)

        xvec = rx0(vec)
        yvec = ry0(vec)
        zvec = rz0(vec)

        self.assertTrue(eq_approx(vec, xvec))
        self.assertTrue(eq_approx(vec, yvec))
        self.assertTrue(eq_approx(vec, zvec))

    def test_rotate(self):
        pass


if __name__ == '__main__':
    unittest.main()
