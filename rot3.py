#!/usr/bin/env python

from math import cos, pi, sin

from quat import Quat
from vec3 import Vec3, XHAT, YHAT, ZHAT


# TODO: JMC: Support conversion to and from matrices
# TODO: JMC: Support representation via Euler angles
# TODO: JMC: Support angular velocity (vector Quaternion class)
# TODO: JMC: Support distinguishing between body & space coordinates
# TODO: JMC: Add abs, add, floordiv, matmul, mul, neg, pow, sub, radd, rfloordiv,
#                rmatmul, rmul, rpow, rsub, rtruediv, truediv
class Rot3:
    @staticmethod
    def degrees_to_radians(degs):
        return degs * pi / 180

    @staticmethod
    def radians_to_degrees(rads):
        return rads * 180 / pi

    @staticmethod
    def x_rotatation(angle):
        return Rot3(XHAT, angle)

    @staticmethod
    def y_rotatation(angle):
        return Rot3(YHAT, angle)

    @staticmethod
    def z_rotatation(angle):
        return Rot3(ZHAT, angle)

    def __init__(self, *args):
        if len(args) == 0:
            self.quat = Quat()
        elif len(args) == 1:
            if isinstance(args[0], float):
                self.quat = Quat(args[0], 0.0, 0.0, 0.0)
            elif isinstance(args[0], list):
                coords = args[0]
                self.quat = Quat(coords[0], coords[1], coords[2], coords[3])
            else:
                assert(False)
        elif len(args) == 2:
            def axis_angle_to_quat(axis, angle):
                cs = cos(angle/2)
                sn = sin(angle/2)
                return Quat(cs, sn * axis.x, sn * axis.y, sn * axis.z)

            if (type(args[0]) == Vec3):
                axis = args[0].normalized()
                angle = args[1]
                self.quat = axis_angle_to_quat(axis, angle)
            elif (type(args[1]) == Vec3):
                axis = args[1].normalized()
                angle = args[0]
                self.quat = axis_angle_to_quat(axis, angle)
            else:
                assert(False)

    def __call__(self, vec):
        return self.rotate(vec)

    def __str__(self):
        return "Rot3-" + _quat.__str__()

    def rotate(self, vec: Vec3) -> Vec3:
        """The result of rotating a vector using a quaternion is
            q * v * q^(-1),
        where R^3 is identified with the imaginary subspace of H (the quaternions)."""
        qv = Quat(vec)
        qinv = self.quat.inverse()
        assert(isinstance(self.quat, Quat))
        assert(isinstance(qv, Quat))
        assert(isinstance(qinv, Quat))
        result = self.quat * qv * qinv
        return result.as_vec3()


XROT90 = Rot3.x_rotatation(Rot3.degrees_to_radians(90))
YROT90 = Rot3.y_rotatation(Rot3.degrees_to_radians(90))
ZROT90 = Rot3.z_rotatation(Rot3.degrees_to_radians(90))
