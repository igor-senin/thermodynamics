import graphics
from graphics import DrawableParticle
from system import System

import pygame

from typing import List


def do_main_cycle(particles: List[graphics.DrawableParticle]):
    clock = pygame.time.Clock()
    run = True

    main_system = System(particles)

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
            b.Draw(1.0)

        graphics.display_update()

    pygame.quit()


def main_cycle():
    graphics.init()
    particles = []
    for i in range(5):
        particles.append(DrawableParticle(i * 200., i * 250., 10., 10., 2.5, 100))
    do_main_cycle(particles) # TODO

