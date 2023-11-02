import graphics
from graphics import DrawableParticle
from system import System

from plot_missings import main_plot

import numpy as np
import pygame

from typing import List

def do_main_cycle(particles: List[graphics.DrawableParticle],
                  scale_coeff=1.0,
                  metric_coeff=1.0,
                  xmax=100.0,
                  ymax=100.0, 
                  lattice_dimension=100):
    clock = pygame.time.Clock()
    run = True

    main_system = System(particles, xmax, ymax, lattice_dimension)

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
        global collision
        collision = main_system.GetBallCollisionValues()
        

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
    scale_coeff = 0.2083333 # for Width = 1920
    metric_coeff = 10**10 # = 1 / hydgrogenium diameter
    N = 10 # total number of particles
    xmax = 400.0 # * 10**-10 metres
    ymax = 225.0 # * 10**-10 metres
    vmax = 1e1 # * 10**-10 metres per second

    dimension = 2

    x  = np.random.uniform(15.0, xmax - 15.0, N * dimension).reshape(N, dimension)
    # TODO may be normal, not uniform
    vx = np.random.uniform(-vmax, vmax, N * dimension).reshape(N, dimension)

    mass = 1.6735575e-27 # kg
    radius = 1.0 # * 10**-10 metres

    particles = []
    for i in range(N):
        particles.append(DrawableParticle(
            x=x[i],
            vx=vx[i],
            mass=mass,
            radius=radius,
            visible_radius=7,
            colour=graphics.Red))
    do_main_cycle(particles, scale_coeff, metric_coeff, xmax, ymax)

