import graphics
from graphics import DrawableParticle
from system import System

import numpy as np
import pygame

from typing import List


def do_main_cycle(particles: List[graphics.DrawableParticle],
                  scale_coeff=1.0,
                  metric_coeff=1.0,
                  xmax=100.0,
                  ymax=100.0):
    clock = pygame.time.Clock()
    run = True

    main_system = System(particles, xmax, ymax)

    while run:
        clock.tick(60)
        graphics.draw_surface()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

            #  TODO

        main_system.RecalculateSystem()

        for b in main_system.GetParticles():
            b.Draw(scale_coeff, metric_coeff)

        graphics.display_update()

    pygame.quit()


def main_cycle():
    graphics.init()
    # 1 pixel <---> (scale_coeff / metric_coeff) metres
    # 400 * 225 particles on window
    scale_coeff = 0.2083333 # for Width = 1920
    metric_coeff = 10**10 # = 1 / hydgrogenium diameter
    N = 100 # total number of particles
    xmax = 400.0 # * 10**-10 metres
    ymax = 225.0 # * 10**-10 metres
    vmax = 1e1 # * 10**-10 metres per second
    xs  = np.random.uniform(15.0, xmax - 15.0, N)
    ys  = np.random.uniform(15.0, ymax - 15.0, N)
    vxs = np.random.uniform(-vmax, vmax, N)
    vys = np.random.uniform(-vmax, vmax, N)

    mass = 1.6735575e-27 # kg
    radius = 1.0 # * 10**-10 metres

    particles = []
    for i in range(N):
        particles.append(DrawableParticle(
            x=xs[i],
            y=ys[i],
            vx=vxs[i],
            vy=vxs[i],
            mass=mass,
            radius=radius,
            visible_radius=30,
            colour=graphics.Red))
    do_main_cycle(particles, scale_coeff, metric_coeff, xmax, ymax)

