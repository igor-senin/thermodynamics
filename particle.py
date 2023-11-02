import numpy as np
from numba import njit
from numba.experimental import jitclass

class Particle:
    def __init__(self, x, y, vx, vy, mass, radius):
        self.coords = np.array([x, y])
        self.velocity = np.array([vx, vy])
        self.mass = mass
        self.radius = radius

        # TODO: длина свободного пробега

    def Dist(self, p):
        return np.linalg.norm(self.coords - p.coords)

    def CheckCollision(self, p):
        return self.Dist(p) <= self.radius + p.radius

    def EdgesCollisions(self, xmin: float, xmax: float, ymin: float, ymax: float):
        if self.coords[0] <= self.radius + xmin or self.coords[0] + self.radius >= xmax:
            self.velocity[0] *= -1.0

        if self.coords[1] <= self.radius + ymin or self.coords[1] + self.radius >= ymax:
            self.velocity[1] *= -1.0

        # fix effect when ball changing velocity very fast
        # after this need recalculate lattice
        eps = 0.000001
        if self.coords[0] <= self.radius + xmin:
            self.coords[0] = self.radius + xmin + eps

        if self.coords[0] + self.radius >= xmax:
            self.coords[0] = xmax - self.radius - eps


        if self.coords[1] <= self.radius + ymin:
            self.coords[1] = self.radius + ymin + eps

        if self.coords[1] + self.radius > ymax:
            self.coords[1] = ymax - self.radius - eps

    # Projection of velocity vector onto vector x
    def ProjectVelocityOn(self, x: np.ndarray) -> np.ndarray:
        return (np.dot(self.velocity, x) / np.dot(x, x)) * x

    def UpdatePosition(self):
        self.coords += self.velocity * 0.1


def dist(p1: Particle, p2: Particle):
    return p1.Dist(p2)

def check_collision(p1: Particle, p2: Particle):
    return p1.CheckCollision(p2)
