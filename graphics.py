from particle import Particle
from system import System
import graphics

import pygame


# colors
White = (255, 255, 255)
Blue  = (30, 144, 255)
Black = (0, 0, 0)
Red   = (255, 0, 0)
Green = (0, 200, 0)
Yellow= (255, 255, 0)
Grey  = (192, 192, 192)

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

def draw_line(x1, y1, x2, y2, scale_coeff):
    x1 = x1 / scale_coeff
    x2 = x2 / scale_coeff
    y1 = y1 / scale_coeff
    y2 = y2 / scale_coeff
    pygame.draw.line(Window, graphics.Black, [x1, y1], [x1, y2], 3)
    pygame.draw.line(Window, graphics.Black, [x2, y1], [x2, y2], 3)
    pygame.draw.line(Window, graphics.Black, [x1, y1], [x2, y1], 3)
    pygame.draw.line(Window, graphics.Black, [x1, y2], [x2, y2], 3)

def draw_surface():
    Window.fill(Grey)
    x = (Width - Height) / 2
    pygame.draw.rect(Surface, White, pygame.Rect(x, 0, Height, Height))
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

    def Draw(self, scale_coeff: float, metric_coeff: float, color=None):
        pygame.draw.circle(Window, # TODO
                           self.colour if color is None else color,
                          (float(self.coords[0]) / scale_coeff,
                           float(self.coords[1]) / scale_coeff),
                           self.visible_radius)

