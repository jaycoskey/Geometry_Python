#!/usr/bin/env python

import unittest

from math import sqrt


class Vec3:
    @staticmethod
    def cross_product(a, b):
        result = Vec3(
            a.y * b.z - a.z * b.y,
            a.z * b.x - a.x * b.z,
            a.x * b.y - a.y * b.x )
        return result

    @staticmethod
    def dot_product(a, b):
        return(a.x * b.x + a.y * b.y + a.z * b.z)

    @staticmethod
    def sum(vs):
        result = Vec3()
        for v in vs:
            result += v
        return result

    def __init__(self, *args):
        if len(args) == 0:
            self.x = self.y = self.z = 0.0
        elif len(args) == 1:
            self.x = args[0].x
            self.y = args[0].y
            self.z = args[0].z
        elif len(args) == 3:
            self.x = args[0]
            self.y = args[1]
            self.z = args[2]
        else:
            raise ValueError('Vec3() requires 0, 1, or 3 arguments')

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, other):
        return Vec3(other * self.x, other * self.y, other * self.z)

    def __rmul__(self, other):
        return Vec3(other * self.x, other * self.y, other * self.z)

    def __rep__(self):
        return self.__str__()

    def __str__(self):
        return '({0:f}, {1:f}, {2:f})'.format(self.x, self.y, self.z)

    def __sub__(self, other):
        assert(isinstance(other, Vec3))
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __truediv__(self, other):
        return Vec3(self.x / other, self.y / other, self.z / other)

    def cross(self, b):
        return Vec3.cross_product(self, b)

    def dot(self, b):
        return Vec3.dot_product(self, b)

    def interpolate(a, b, t):
        return (1 - t) * a + t * b

    def norm(self):
        return sqrt(self.norm2())

    def norm2(self):
        return self.x ** 2 + self.y ** 2 +  self.z ** 2

    def normalized(self):
        n = self.norm()
        return Vec3((1/n) * self.x, (1/n) * self.y, (1/n) * self.z)

ZERO = Vec3(0.0, 0.0, 0.0)
XHAT = Vec3(1.0, 0.0, 0.0)
YHAT = Vec3(0.0, 1.0, 0.0)
ZHAT = Vec3(0.0, 0.0, 1.0)
