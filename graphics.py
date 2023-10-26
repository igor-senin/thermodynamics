from particle import Particle
from system import System

import pygame


# colors
White = (255, 255, 255)
Blue  = (30, 144, 255)
Black = (0, 0, 0)
Red   = (255, 0, 0)
Green = (0, 200, 0)
Yellow= (255, 255, 0)

def init():
    pygame.init()

    global Width, Height, Window
    Width, Height = pygame.display.Info().current_w, pygame.display.Info().current_h
    Window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    
    global Surface
    Surface = pygame.Surface((Width, Height), pygame.SRCALPHA)

    pygame.display.set_caption("Thermodynamics")

def display_update():
    pygame.display.update()

def draw_surface():
    Window.fill(White)
    Window.blit(Surface, (0,0))

"""
    Drawable class
"""
class DrawableParticle(Particle):
    def __init__(self,
                 x,
                 y,
                 vx,
                 vy,
                 mass,
                 radius,
                 colour=None,
                 visible_radius=None):
        super(DrawableParticle, self).__init__(x, y, vx, vy, mass, radius)
        self.colour = Red if colour is None else colour
        self.visible_radius = radius if visible_radius is None else visible_radius

    def Draw(self, scale_coeff: float, metric_coeff: float):
        pygame.draw.circle(Window, # TODO
                           self.colour,
                          (float(self.coords[0]) / scale_coeff,
                           float(self.coords[1]) / scale_coeff),
                           self.visible_radius)

