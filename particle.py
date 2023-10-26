import numpy as np


class Particle:
    def __init__(self, x, y, vx, vy, mass, radius):
        self.coords = np.array([x, y])
        self.velocity = np.array([vx, vy])
        self.mass = mass
        self.radius = radius

        # TODO: длина свободного пробега
        '''
            У частицы есть внутренний таймер, в течени
        '''

    def Dist(self, p):
        return np.linalg.norm(self.coords - p.coords)

    def CheckCollision(self, p):
        return self.Dist(p) <= self.radius + p.radius

    # Projection of velocity vector onto vector x
    def ProjectVelocityOn(self, x: np.ndarray) -> np.ndarray:
        return (np.dot(self.velocity, x) / np.dot(x, x)) * x

    def UpdatePosition(self):
        self.coords += self.velocity * 0.1


def dist(p1: Particle, p2: Particle):
    return p1.Dist(p2)

def check_collision(p1: Particle, p2: Particle):
    return p1.CheckCollision(p2)
