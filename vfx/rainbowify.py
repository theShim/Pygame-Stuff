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

def apply_rainbow(surf: pygame.Surface, offset=0, strength=0.7, bands=2):
    x = np.linspace(0, 1, surf.get_width())
    y = np.linspace(0, 1, surf.get_height())
    gradient = np.outer(x, y) * bands

    red_mult = np.sin(math.pi * 2 * (gradient + offset)) * 0.5 + 0.5
    green_mult = np.sin(math.pi * 2 * (gradient + offset + 0.25)) * 0.5 + 0.5
    blue_mult = np.sin(math.pi * 2 * (gradient + offset + 0.5)) * 0.5 + 0.5
    red_mult =green_mult = 0

    res = surf.copy()

    red_pixels = pygame.surfarray.pixels_red(res)
    red_pixels[:] = (red_pixels * (1 - strength) + red_pixels * red_mult * strength).astype(dtype='uint16')

    green_pixels = pygame.surfarray.pixels_green(res)
    green_pixels[:] = (green_pixels * (1 - strength) + green_pixels * green_mult * strength).astype(dtype='uint16')

    blue_pixels = pygame.surfarray.pixels_blue(res)
    blue_pixels[:] = (blue_pixels * (1 - strength) + blue_pixels * blue_mult * strength).astype(dtype='uint16')

    return res

    ##############################################################################################

frog = pygame.image.load('frog.png').convert_alpha()
frog = pygame.transform.scale(frog, (frog.get_width() * 10,
                                     frog.get_height() * 10))

    ##############################################################################################

last_time = time.time()
start = False
x = 0

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
            if event.key == pygame.K_SPACE:
                start = True

    screen.fill((30, 30, 30))

    x += 20
    surf = apply_rainbow(frog, round(x/600, 2), 0.7)
    screen.blit(surf, (0, 0))

    #fps
    font = pygame.font.SysFont('monospace', 30)
    fps = font.render(f'FPS: {int(clock.get_fps())}', True, (215, 215, 215))
    screen.blit(fps, (0, 0))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()