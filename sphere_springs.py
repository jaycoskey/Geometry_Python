#!/usr/bin/env python

from math import acos, cos, pi, sin

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numpy.random import normal

from rot3 import Rot3
from vec3 import Vec3


VERBOSE = False


def clamp(minval, maxval, val):
    return minval if val < minval else (maxval if val > maxval else val)


def new_point_location(alpha, point, net_force):
    angle = alpha * net_force.norm()
    axis = net_force.cross(point).normalized()
    rot3 = Rot3(axis, angle)
    result = rot3.rotate(point)
    if VERBOSE:
        print(f'    Moved point from {point} to {result}. Delta={result - point}')
    return result


class SphereSprings:
    alpha = 0.25
    force_threshold = 10e-4
    movement_threshold = 10e-6
    radius = 1.0
    max_iter_count = 100

    def __init__(self, points):
        self.points = points

    def by_coords(self):
        length = len(self.points)
        return ([self.points[k].x for k in range(length)],
                [self.points[k].y for k in range(length)],
                [self.points[k].z for k in range(length)])

    def stabilize(self):
        iter_count = 0
        points_count = len(self.points)
        radius = SphereSprings.radius
        while True:
            if VERBOSE:
                print(f'stabilize loop iter count=({iter_count}): Sum of points = {Vec3.sum(self.points)}')
            if iter_count >= SphereSprings.max_iter_count:
                if VERBOSE:
                    exit_expr = f'iter_count={iter_count} >= {SphereSprings.max_iter_count}'
                    print(f'stabilize: Exit condition 1: {exit_expr}')
                return  # Stopping condition #1

            # Compute forces: key (i, j) references the force exerted by point i on point j
            forces: Map[Pair[Int], Vec3] = { (i, j) : Vec3() for i in range(points_count) for j in range(points_count) }
            for i in range(points_count):
                pi = self.points[i]
                for j in range(i + 1, points_count):
                    pj = self.points[j]
                    cos_angle_ij = clamp(-1, 1, pi.dot(pj) / (pi.norm() * pj.norm()))
                    angle_ij = acos(cos_angle_ij)
                    perp = pi.cross(pj)
                    dir_i = pi.cross(perp)
                    dir_j = perp.cross(pj)
                    forces[(i, j)] += SphereSprings.alpha * angle_ij * dir_i.normalized()
                    forces[(j, i)] += SphereSprings.alpha * angle_ij * dir_j.normalized()

            def net_force(fs):
                return Vec3.sum(fs)

            def forces_on_nth_point(n):
                return [forces[(i, n)] for i in range(points_count) if i != n]

            # Compute net forces, then remove component perpendicular to sphere, leaving only tangential component
            net_forces = [net_force(forces_on_nth_point(n)) for n in range(points_count)]
            net_forces = [net_forces[k] - (net_forces[k].dot(self.points[k]) * self.points[k]) for k in range(points_count)]

            if VERBOSE:
                print(f'\tNet forces: ', end='')
                for k in range(points_count):
                    print(f'{net_forces[k]} ', end='')
                print()

            max_force = max([net_forces[k].norm() for k in range(points_count)])
            if max_force < SphereSprings.force_threshold:
                if VERBOSE:
                    exit_expr = f'max_force={max_force} >= {SphereSprings.force_threshold}'
                    print(f'stabilize: Exit condition 2: {exit_expr}')
                return  # Stopping condition #2

            new_points = [new_point_location(SphereSprings.alpha, points[k], net_forces[k]) for k in range(len(self.points))]
            movement_norms = [(self.points[k] - new_points[k]).norm() for k in range(points_count)]
            sum_movement_norms = sum(movement_norms)
            if sum_movement_norms < SphereSprings.movement_threshold:
                if VERBOSE:
                    exit_expr = f'sum_movement_norms={sum_movement_norms} < {SphereSprings.movement_threshold}'
                    print(f'stabilize: Exit condition 3: {exit_expr}')
                return  # Stopping condition #3

            self.points = new_points
            iter_count += 1


if __name__ == '__main__':
    points_count = 50
    xs = normal(0, 1, points_count)
    ys = normal(0, 1, points_count)
    zs = normal(0, 1, points_count)
    points = [Vec3(xs[k], ys[k], zs[k]) for k in range(points_count)]
    springs = SphereSprings(points)
    springs.stabilize()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(*springs.by_coords(), color='k')
    plt.show()
