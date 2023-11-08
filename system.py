import numpy as np
from sys import float_info
from particle import Particle
from physical_laws import PhysicalLaws

from lattice import Lattice

from typing import List

class System:
    def __init__(self, particles: List[Particle],
                 xmin: float, xmax: float,
                 ymin: float, ymax: float,
                 lattice_dimension : int):
        self.particles = particles # no copy
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

        # lattice example for dimension 2
        # -----
        # | | |
        # |-|-|
        # | | |
        # -----
        self.lattice = Lattice(xmin, xmax, ymin, ymax, lattice_dimension, self.particles)
        self.max_velocity = 0.0
        self.min_velocity = float_info.max
        self.mean_velocity = 0.0
        self.hits_on_the_walls = 0.0

    def SetBallCollisionValues(self, current_collision, true_collision):
        self.current_collision = current_collision
        self.true_collision = true_collision 

    def GetBallCollisionValues(self):
        return [self.current_collision, self.true_collision]


    def RecalculateSystem(self):
        size = len(self.particles)
        self.max_velocity = np.float64(float_info.min)
        self.min_velocity = np.float64(float_info.max)
        self.mean_velocity = np.float64(0.0)
        self.hits_on_the_walls = np.float64(0.0) 
        
        for i in range(size):
            velocity_norm = np.linalg.norm(self.particles[i].velocity)
            self.max_velocity = np.max([self.max_velocity, velocity_norm])
            self.min_velocity = np.min([self.min_velocity, velocity_norm])
            self.mean_velocity += velocity_norm

            has_collision = self.particles[i].EdgesCollisions(self.xmin, self.xmax, self.ymin, self.ymax)
            self.hits_on_the_walls += 1.0 if has_collision else 0.0

            self.lattice.RecalculateParticle(i)

            # here and below it is written that we recalculate collision only in particle block
            # and right lower and diag(right and lower) 
            # it is correct because left and higher and etc will be recalculated 
            # when we consider particle in left(or higher, diag...) block 
            def recalculateWithVisitors(visitors, start_index):
                for j in range(start_index, len(visitors)):
                    PhysicalLaws.Collision(self.particles[i], self.particles[visitors[j]])

            visitors_current = self.lattice.GetVisitorsByParticleIndex(i)
            start_index = visitors_current.index(i) + 1

            recalculateWithVisitors(visitors_current, start_index)

            border_len = self.lattice.GetBlockLen()
            visitors_right = self.lattice.GetVisitorsByParticleCoordinates(self.particles[i].coords[0], 
                                                                           self.particles[i].coords[1] + border_len)

            visitors_lower = self.lattice.GetVisitorsByParticleCoordinates(self.particles[i].coords[0] + border_len, 
                                                                           self.particles[i].coords[1])

            visitors_diag = self.lattice.GetVisitorsByParticleCoordinates(self.particles[i].coords[0] + border_len, 
                                                                          self.particles[i].coords[1] + border_len)

            start_index = 0

            # this check for case when particle doesn't have diag, right or lower neighbour blocks
            if visitors_diag != visitors_current:
                recalculateWithVisitors(visitors_diag, start_index)

            if visitors_right != visitors_diag and visitors_right != visitors_current:
                recalculateWithVisitors(visitors_right, start_index)

            if visitors_lower != visitors_diag and visitors_lower != visitors_current:
                recalculateWithVisitors(visitors_lower, start_index)

            self.particles[i].UpdatePosition()
            self.lattice.RecalculateParticle(i)

        self.mean_velocity /= size

    def GetParticles(self):
        return self.particles

    def GetStatistics(self):
        print(self.max_velocity, self.min_velocity, self.mean_velocity, self.hits_on_the_walls)

        return [self.max_velocity, 
                self.min_velocity, 
                self.mean_velocity,
                self.hits_on_the_walls]

