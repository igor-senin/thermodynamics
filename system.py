from particle import Particle
from physical_laws import PhysicalLaws

from typing import List


class System:
    def __init__(self, particles: List[Particle], xmax: float, ymax: float):
        self.particles = particles # no copy
        self.xmax = xmax
        self.ymax = ymax

    def RecalculateSystem(self):
        size = len(self.particles)

        for i in range(size):
            self.particles[i].EdgesCollisions(self.xmax, self.ymax)

            for j in range(i + 1, size):
                PhysicalLaws.Collision(self.particles[i], self.particles[j])

            self.particles[i].UpdatePosition()

    def GetParticles(self):
        return self.particles
