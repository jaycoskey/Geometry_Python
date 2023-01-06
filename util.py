#!/usr/bin/env python

from math import fabs


EPSILON = 10E-6


def eq_approx(x, y, eps=EPSILON):
    return is_zero_approx(x - y, eps)

def is_zero_approx(x, eps=EPSILON):
    t = type(x).__name__
    if t == 'Quat' or t == 'Vec3':
        return is_zero_approx(x.norm())
    else:
        return fabs(x) < eps
