#!/usr/bin/env python

from math import acos, cos, exp, sin, cos, log, sqrt

from util import is_zero_approx
from vec3 import Vec3


class Quat:
    def __init__(self, *args):
        if len(args) == 0:
            self.qr = self.qi = self.qj = self.qk = 0.0
        elif len(args) == 1:
            arg0 = args[0]
            if type(arg0) == type(self):  # arg0 = a quaternion
                self.qr = other.qr
                self.qi = other.qi
                self.qj = other.qj
                self.qk = other.qk
            elif isinstance(arg0, Vec3):
                self.qr = 0.0
                self.qi = arg0.x
                self.qj = arg0.y
                self.qk = arg0.z
            elif isinstance(arg0, float):
                self.qr = arg0
                self.qi = self.qj = self.qk = 0.0
            else:
                assert(False)
        elif len(args) == 2:  # Axis & angle
            if type(args[1]).__name__ == 'Quat':
                self.qr = args[0]
                self.qi = args[1].qi
                self.qj = args[1].qj
                self.qk = args[1].qk
            elif type(args[1]).__name__ == 'Vec3':
                angle = args[0]
                axis = args[1]

                cs = cos(angle / 2)
                sn = sin(angle / 2)

                self.qr = cs
                self.qi = sn * axis.x
                self.qj = sn * axis.y
                self.qk = sn * axis.z
            else:
                assert(False)
        elif len(args) == 4:
            self.qr = args[0]
            self.qi = args[1]
            self.qj = args[2]
            self.qk = args[3]
        else:
            raise ValueError('Constructor takes 0, 1, 2, or 4 arguments.')
        assert(isinstance(self.qr, float))
        assert(isinstance(self.qi, float))
        assert(isinstance(self.qj, float))
        assert(isinstance(self.qk, float))

    def __add__(self, other):
        if type(other) == type(self):
            return Quat(self.qr + other.qr, self.qi + other.qi, self.qj + other.qj, self.qk + other.qk)
        else:
            return Quat(self.qr + other, self.qi, self.qj, self.qk)

    def __rmul__(self, other):
        return self * other

    def __mul__(self, other):
        if type(other) == type(self):
            return Quat(
                self.qr * other.qr - self.qi * other.qi - self.qj * other.qj - self.qk * other.qk,
                self.qr * other.qi + self.qi * other.qr + self.qj * other.qk - self.qk * other.qj,
                self.qr * other.qj + self.qj * other.qr + self.qk * other.qi - self.qi * other.qk,
                self.qr * other.qk + self.qk * other.qr + self.qi * other.qj - self.qj * other.qi)
        else:
            return Quat(other * self.qr, other * self.qi, other * self.qj, other * self.qk)

    def __pos__(self):
            return Quat(self.qr, self.qi, self.qj, self.qk)

    def __neg__(self):
        return Quat(-self.qr, -self.qi, -self.qj, -self.qk)

    def __str__():
        return '{0:.2f} + {1:.2f}i + {2:.2f}j + {3:.2f}k'.format(self.qr, self.qi, self.qj, self.qk)

    def __sub__(self, other):
        if type(other) == type(self):
            return Quat(self.qr - other.qr, self.qi - other.qi, self.qj - other.qj, self.qk - other.qk)
        else:
            return Quat(self.qr - other, self.qi, self.qj, self.qk)

    def __truediv__(self, other):
        if type(other) == type(self):
            return Quat(self * other.inverse())
        else:
            return Quat(self.qr / other, self.qi / other, self.qj / other, self.qk / other)

    def as_vec3(self):
        '''Return a 3D vector representing the non-real components of the argument.
        Note: This should only be called on vector quaternion.'''
        return Vec3(self.qi, self.qj, self.qk)

    def conjugate(self):
        return Quat(self.qr, -self.qi, -self.qj, -self.qk)

    def diffnorm(self, other):
        return (self - other).length()

    def imag(self):
        return Quat(0.0, self.qi, self.qj, self.qk)

    def inverse(self):
        return self.conjugate() / self.norm2()

    def norm(self):
        norm2 = self.norm2()
        return sqrt(norm2)

    def norm2(self):
        norm2 = self.qr**2 + self.qi**2 + self.qj**2 + self.qk**2
        return norm2

    def normalize(self):
        n = self.norm()
        assert(not is_zero_approx(n))
        # return Quat(self.qr / n, self.qi / n, self.qj / n, self.qk / n)
        return (1/self.norm()) * self

# ----------------------------------------

QZERO = Quat(0.0, 0.0, 0.0, 0.0)
QRHAT = Quat(1.0, 0.0, 0.0, 0.0)
QIHAT = Quat(0.0, 1.0, 0.0, 0.0)
QJHAT = Quat(0.0, 0.0, 1.0, 0.0)
QKHAT = Quat(0.0, 0.0, 0.0, 1.0)

# ----------------------------------------

def qexp(q):
    """Just as e ** (i * pi) == -1, it's also true that e ** (v * PI) == -1 for any unit vector Quaternion, v."""
    qimag = q.imag()
    qimagnorm = qimag.norm()
    if is_zero_approx(qimagnorm):
        return exp(q.qr) * QRHAT
    else:
        qimaghat = qimag.normalize()
        theta = qimag.norm()
        cos_theta = cos(theta) * QRHAT
        sin_theta_vhat = sin(theta) * qimaghat
        return cos_theta + sin_theta_vhat

def qlog(q):
    """Given a non-zero quaternion q, q = |q| * qhat, where qhat is a unit quaternion.
    qhat = (cos theta) + (sin theta) * qijkhat = exp(qijkhat * theta),
        where qijkhat is a pure imaginary unit quaternion.
    log(qhat) = qijkhat * theta
    So log(q) = log(|q|) + qijkhat * theta
    """
    """TODO: Document the cut point for the complex log function.
    If q = r (cos A + v * sin A), then Log(q) = r + v * A,
    where r is the norm of q, and v is a vector quaternion---one with zero real component."""
    qnorm = q.norm()
    assert(not is_zero_approx(qnorm))
    qhat = (1/qnorm) * q
    theta = acos(qhat.qr)
    qijk = qhat.imag()
    qijknorm = qijk.norm()
    if is_zero_approx(qijk):
        def sgn(x):
            return 1 if x > 0 else (-1 if x < 0 else 0)
        sgn_r = sgn(qijknorm)
        qijkhat = sgn_r * QRHAT
    else:
        qijkhat = qhat.imag().normalize()
    return Quat(log(qnorm), theta * qijkhat)


def qpow(q1, q2):
    """Note: Since quaternions are non-commutative,
    it is NOT always the case that log(x**y) = y * log(x) = log(x) * y.
    To make the definition of pow(q1, q2) well-defined, the second argument should be real.
    This is a sufficient, but not necessary condition."""
    return qexp(q2 * qlog(q1))


def qslerp(a, b, t):
    """Spherical Linear Interpolation ("Slerp") of quaternions yeilds natural transitions from one rotation to another.
    x = Starting quaternion
    y = Ending quaternion
    z = Time, which goes from 0 to 1"""
    return qpow(a, 1-t) * qpow(b, t)
