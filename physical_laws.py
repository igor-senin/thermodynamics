import numpy as np
from numba import njit

from particle import Particle


class PhysicalLaws:

    @staticmethod
    def Collision(p1: Particle, p2: Particle):
        if not p1.CheckCollision(p2):
            return

        x_axis = p2.coords - p1.coords
        x_axis = x_axis / np.linalg.norm(x_axis)
        y_axis = np.array([-x_axis[1], x_axis[0]])

        div = 0 if x_axis[0] != 0.0 else 1

        v1x = p1.ProjectVelocityOn(x_axis)[div] / x_axis[div]
        v2x = p2.ProjectVelocityOn(x_axis)[div] / x_axis[div]

        m1, m2 = p1.mass, p2.mass
        v1x_new = (2 * m2 * v2x + v1x * (m1 - m2)) / (m1 + m2)
        v2x_new = (2 * m1 * v1x + v2x * (m2 - m1)) / (m1 + m2)

        v1y = p1.ProjectVelocityOn(y_axis)
        v2y = p2.ProjectVelocityOn(y_axis)

        p1.velocity = v1x_new * x_axis + v1y
        p2.velocity = v2x_new * x_axis + v2y

