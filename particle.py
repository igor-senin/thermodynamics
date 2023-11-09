import numpy as np


class Particle:
    def __init__(self, x, y, vx, vy, mass, radius):
        self.coords = np.array([x, y])
        self.velocity = np.array([vx, vy])
        self.mass = mass
        self.radius = radius
        self.past_collision = None

        self.dt = 0.1

        # TODO: длина свободного пробега

    def Dist(self, p):
        return np.linalg.norm(self.coords - p.coords)

    def CheckCollision(self, p):
        return self.Dist(p) <= self.radius + p.radius

    def EdgesCollisions(self, system):
        # system of type system.System
        xmin = system.xmin
        xmax = system.xmax
        ymin = system.ymin
        ymax = system.ymax

        has_collision = False

        if self.coords[0] <= self.radius + xmin:
            print("left pressure", system.left_wall_pressure)
            system.left_wall_pressure += self.mass * (self.velocity[0])**2
            self.velocity[0] *= -1.0
            has_collision = True

        if self.coords[0] + self.radius >= xmax:
            print("right pressure", system.right_wall_pressure)
            system.right_wall_pressure += self.mass * (self.velocity[0])**2
            self.velocity[0] *= -1.0
            has_collision = True

        if self.coords[1] <= self.radius + ymin:
            print("top pressure", system.top_wall_pressure)
            system.top_wall_pressure += self.mass * (self.velocity[1])**2
            self.velocity[1] *= -1.0
            has_collision = True

        if self.coords[1] + self.radius >= ymax:
            print("bottom pressure", system.bottom_wall_pressure)
            system.bottom_wall_pressure += self.mass * (self.velocity[1])**2
            self.velocity[1] *= -1.0
            has_collision = True

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

        return has_collision

    # Projection of velocity vector onto vector x
    def ProjectVelocityOn(self, x: np.ndarray) -> np.ndarray:
        return (np.dot(self.velocity, x) / np.dot(x, x)) * x

    def UpdatePosition(self):
        self.coords += self.velocity * self.dt


def dist(p1: Particle, p2: Particle):
    return p1.Dist(p2)

def check_collision(p1: Particle, p2: Particle):
    return p1.CheckCollision(p2)
