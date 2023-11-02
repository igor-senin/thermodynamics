import graphics
from graphics import DrawableParticle
from system import System

import numpy as np
import pygame

from typing import List


def do_main_cycle(particles: List[graphics.DrawableParticle],
                  scale_coeff=1.0,
                  metric_coeff=1.0,
                  xmin=0.0,
                  xmax=100.0,
                  ymin=0.0,
                  ymax=100.0, 
                  lattice_dimension=50):
    clock = pygame.time.Clock()
    run = True

    main_system = System(particles, xmin, xmax, ymin, ymax, lattice_dimension)

    colors = [(255, 0, 0),
              (255, 153, 51),
              (255, 255, 51),
              (153, 255, 51),
              (51, 255, 51),
              (255, 0, 127),
              (204, 0, 204),
              (0, 0, 255),
              (0, 0, 0)]

    while run:
        clock.tick(60)
        graphics.draw_surface()
        #for blocks_list in main_system.lattice.blocks:
        #    for block in blocks_list:
        #        graphics.draw_line(block.x_lower[0], block.x_lower[1],
        #                           block.x_higher[0], block.x_higher[1],
        #                           scale_coeff)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

            #  TODO

        main_system.RecalculateSystem()

        for b in main_system.GetParticles():
            #color_id = main_system.lattice.GetBlockID(b.coords[0], b.coords[1])
            #color_id %= len(colors)
            color = colors[0]#[color_id]
            b.Draw(scale_coeff, metric_coeff, color)

        graphics.display_update()

    pygame.quit()


def main_cycle():
    graphics.init()
    # 1 pixel <---> (scale_coeff / metric_coeff) metres
    # 400 * 225 particles on window
    scale_coeff = 400.0 / graphics.Width
    metric_coeff = 10**10 # = 1 / hydgrogenium diameter
    N = 1000 # total number of particles
    ymin = 0.0
    ymax = 225.0 # * 10**-10 metres

    x_total = 400.0
    xmin = (x_total - ymax) / 2.0 # * 10**-10 metres
    xmax = (x_total + ymax) / 2.0 # * 10**-10 metres

    dr = 15.0 # shift from walls
    
    vmax = 1e1 # * 10**-10 metres per second

    xs  = np.random.uniform(xmin + dr, xmax - dr, N)
    ys  = np.random.uniform(ymin + dr, ymax - dr, N)
    vxs = np.random.uniform(-vmax, vmax, N)
    vys = np.random.uniform(-vmax, vmax, N)

    mass = 1.6735575e-27 # kg
    radius = 2.0 # * 10**-10 metres

    particles = []
    for i in range(N):
        particles.append(DrawableParticle(
            x=xs[i],
            y=ys[i],
            vx=vxs[i],
            vy=vys[i],
            mass=mass,
            radius=radius,
            visible_radius=10,
            colour=graphics.Red))
    do_main_cycle(particles, scale_coeff, metric_coeff, xmin, xmax, ymin, ymax)

