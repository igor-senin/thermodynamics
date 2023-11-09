from system import System
from particle import Particle

import numpy as np

from typing import List

def main_cycle_init(xmin: float, ymin: float, xmax: float, ymax: float, N:int):
    dr = 10.0 # shift from walls
    
    vmax = 1e1 # * 10**-10 metres per second

    xs  = np.random.uniform(xmin + dr, xmax - dr, N)
    ys  = np.random.uniform(ymin + dr, ymax - dr, N)
    vxs = np.random.uniform(-vmax, vmax, N)
    vys = np.random.uniform(-vmax, vmax, N)

    mass = 1.6735575e-27 # kg
    radius = 1.5 # * 10**-10 metres

    particles = []
    for i in range(N):
        particles.append(Particle(
            x=xs[i],
            y=ys[i],
            vx=vxs[i],
            vy=vys[i],
            mass=mass,
            radius=radius))

    lattice_dimension = 100

    global main_system 
    main_system = System(particles, xmin, xmax, ymin, ymax, lattice_dimension)
    print("cycle ready to work")

index = 0
def cycle_iteration():
    main_system.RecalculateSystem()
    ret = [main_system.GetParticles(), main_system.GetStatistics()]

    index += 1
    if index == 100:
        index = 0
        main_system.ClearStatistics()

    return ret

