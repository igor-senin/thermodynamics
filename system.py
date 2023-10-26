from particle import Particle
from physical_laws import PhysicalLaws

from typing import List


class System:
    def __init__(self, particles: List[Particle]):
        self.particles = particles # no copy

    def RecalculateSystem(self):
        size = len(self.particles)

        for i in range(size):
            self.particles[i].EdgesCollisions()

            for j in range(i + 1, size):
                PhysicalLaws.Collision(self.particles[i], self.particles[j])

            self.particles[i].UpdatePosition()

    def GetParticles(self):
        return self.particles
