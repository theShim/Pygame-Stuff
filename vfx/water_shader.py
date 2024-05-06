import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import contextlib
with contextlib.redirect_stdout(None):
    import pygame
    from pygame.locals import *
    
import random
import sys
import math
import time
import numpy as np

from perlin_numpy import generate_fractal_noise_2d

    ##############################################################################################

#initialising pygame stuff
pygame.init()  #general pygame
pygame.font.init() #font stuff
pygame.mixer.pre_init(44100, 16, 2, 4096) #music stuff
pygame.mixer.init()
pygame.event.set_blocked(None) #setting allowed events to reduce lag
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
pygame.display.set_caption("")

#initalising pygame window
flags = pygame.DOUBLEBUF #| pygame.FULLSCREEN
SIZE = WIDTH, HEIGHT = (720, 720)
screen = pygame.display.set_mode(SIZE, flags, 16)
clock = pygame.time.Clock()

#renaming common functions
vec = pygame.math.Vector2

#useful functions
def gen_colour():
    return (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

def euclidean_distance(point1, point2):
    return vec(point1).distance_to(vec(point2))

def rotate(origin, point, angle):
    ox, oy = origin
    px, py = point
    angle = math.radians(angle)

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return vec(qx, qy)

    ##############################################################################################

class Water:
    NOISE = generate_fractal_noise_2d(
        (160, 160),
        (8, 8),
        3,
    )
    NOISE = NOISE[:120, :120]

    CACHE = {}

    @classmethod
    def add_colour(cls, noise: np.ndarray):
        color_world = np.zeros(noise.shape+(3,))
        
        noise = noise.copy() * 4
        color_world[:] = [2,150,215]
    
        # shifted_noise = np.roll(noise, (-1, -1), axis=(0, 1)) 
        # shifted_condition = (2 < shifted_noise % 4) & (shifted_noise % 4 < 3)
        # color_world[shifted_condition] = [214, 214, 214]
        shifted_noise = np.roll(noise, (1, 1), axis=(0, 1)) 
        shifted_condition = (1.5 < shifted_noise % 4) & (shifted_noise % 4 < 2)
        color_world[shifted_condition] = [220, 220, 220]

        condition = (0 < noise % 4) & (noise % 4 < 2)
        color_world[condition] = [44,232,248]

        # condition = (noise % 4 < 4.1)
        # color_world[condition] = [9, 10, 27]
        # condition = (noise % 4 < 3.5)
        # color_world[condition] = [4, 3, 6]
        # condition = (noise % 4 < 2.6)
        # color_world[condition] = [14, 19, 32]
        # condition = (noise % 4 < 1.9)
        # color_world[condition] = [17, 25, 37]

        return color_world
    
    def __init__(self):
        self.screen = pygame.display.get_surface()
    
    def update(self):
        self.NOISE -= 0.01

        # try:
        #     surf = self.CACHE[(round(self.game.offset.x, 1), round(self.game.offset.y, 1))]
        # except:
        surf = pygame.surfarray.make_surface(self.add_colour(self.NOISE))
        surf = pygame.transform.scale(surf, SIZE)
        # self.CACHE[(round(self.game.offset.x, 1), round(self.game.offset.y, 1))] = surf
        self.screen.blit(surf, (0, 0))

w = Water()

    ##############################################################################################

last_time = time.time()

running = True
while running:

    dt = time.time() - last_time
    last_time = time.time()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

    screen.fill((30, 30, 30))
    w.update()

    #fps
    font = pygame.font.SysFont('monospace', 30)
    fps = font.render(f'FPS: {int(clock.get_fps())}', True, (215, 215, 215))
    screen.blit(fps, (0, 0))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()