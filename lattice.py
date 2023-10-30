import numpy as np
from numba import njit
from numba.experimental import jitclass

class Block:
    def __init__(self, x_lower, x_higher):
        self.x_lower = x_lower
        self.x_higher = x_higher
        self.visitors = []
        pass

class Lattice:
    def __init__(self, xmax, ymax, lattince_dimension, particles):
        self.xmax = xmax
        self.ymax = ymax
        self.lattince_dimension = lattince_dimension
        self.particles = particles
        # block indexes for every particle in particles
        self.particles_indexes = []
        # blocks in latttince, contains particles
        self.blocks = [[] for i in range(lattince_dimension)]
        for i in range(lattince_dimension):
            for j in range(lattince_dimension):
                x_min = i / lattince_dimension * xmax
                y_min = j / lattince_dimension * ymax
                x_max = (i+1) /lattince_dimension * xmax
                y_max = (j+1) /lattince_dimension * ymax
                self.blocks[i].append(Block([x_min, y_min], [x_max, y_max]))

        for i, p in enumerate(particles):
            indexes = self.GetBlockIndex(p.coords[0], p.coords[1])
            self.blocks[indexes[0]][indexes[1]].visitors.append(i)
            self.particles_indexes.append(indexes)


    # get index of block which contains coordinates [x, y]
    def GetBlockIndex(self, x, y):
        x_index = int((x / self.xmax)  * self.lattince_dimension)

        if x_index < 0:
            x_index = 0
        if x_index > self.lattince_dimension - 1:
            x_index = self.lattince_dimension - 1

        y_index = int((y / self.ymax)  * self.lattince_dimension)
        if y_index < 0:
            y_index = 0
        if y_index > self.lattince_dimension - 1:
            y_index = self.lattince_dimension - 1

        return [x_index, y_index]

    # particle index is is index in list of particles
    def RecalculateParticle(self, particle_index):
        prev_index = self.particles_indexes[particle_index]

        new_index = self.GetBlockIndex(self.particles[particle_index].coords[0], 
                                       self.particles[particle_index].coords[1])
        if prev_index != new_index:
            self.blocks[prev_index[0]][prev_index[1]].visitors.remove(particle_index)
            self.blocks[new_index[0]][new_index[1]].visitors.append(particle_index)
            self.particles_indexes[particle_index] = new_index

    # get particle visitors by particle index in particles
    def GetVisitorsByParticleIndex(self, index):
        x = self.particles[index].coords[0]
        y = self.particles[index].coords[1]

        return self.GetVisitorsByParticleCoordinates(x, y)


    def GetVisitorsByParticleCoordinates(self, x, y):
        indexes = self.GetBlockIndex(x, y)
        return self.blocks[indexes[0]][indexes[1]].visitors


    def GetBlockLen(self):
        return self.xmax / self.lattince_dimension

    # get block unique identifier by point in this block
    def GetBlockID(self, x, y):
        indexes = self.GetBlockIndex(x, y)
        return indexes[0] * self.lattince_dimension + indexes[1]
