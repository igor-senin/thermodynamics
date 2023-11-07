from particle import Particle
from system import System
import graphics

import numpy as np
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

def get_box_bounds():
    ymin = 0.0
    ymax = (graphics.Height / graphics.Width) * 400.0 # * 10**-10 metres
    x_total = 400.0
    xmin = (x_total - ymax) / 2.0 # * 10**-10 metres
    xmax = (x_total + ymax) / 2.0 # * 10**-10 metres
    return xmin, ymin, xmax, ymax

def display_update():
    pygame.display.update()

def draw_squeare(x1, y1, x2, y2, scale_coeff):
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
class DrawableParticle():
    def __init__(self, x=0.0, y=0.0, vx=0.0, vy=0.0, colour=None, visible_radius=None):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.colour = Red if colour is None else colour
        self.visible_radius = 10.0 if visible_radius is None else visible_radius

    def Draw(self, scale_coeff: float, metric_coeff: float, color=None):
        v = np.linalg.norm([self.vx, self.vy])
        v *= 20
        print(v)
        int_v = min(int(v), 255)
        v_color = (255, 255 - int_v, 0)

        pygame.draw.circle(Window,
                           v_color,
                           #self.colour if color is None else color,
                          (float(self.x) / scale_coeff,
                           float(self.y) / scale_coeff),
                           self.visible_radius)

