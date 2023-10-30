from particle import Particle
from physical_laws import PhysicalLaws

from lattince import Lattince

from typing import List


class System:
    def __init__(self, particles: List[Particle], xmax: float, ymax: float, lattice_dimension : int):
        self.particles = particles # no copy
        self.xmax = xmax
        self.ymax = ymax

        # lattice example for dimension 2
        # -----
        # | | |
        # |-|-|
        # | | |
        # -----
        self.lattice = Lattince(xmax, ymax, lattice_dimension, self.particles)
        print("xmax ", self.lattice.xmax)


    def RecalculateSystem(self):
        size = len(self.particles)

        for i in range(size):
            self.particles[i].EdgesCollisions(self.xmax, self.ymax)

            visitors = self.lattice.GetVisitorsByParticleIndex(i)
            start_index = visitors.index(i) + 1
            for j in range(start_index, len(visitors)):
                PhysicalLaws.Collision(self.particles[i], self.particles[visitors[j]])

            self.particles[i].UpdatePosition()
            self.lattice.RecalculateParticle(i)

    def GetParticles(self):
        return self.particles
