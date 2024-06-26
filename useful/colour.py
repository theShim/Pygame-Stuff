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
SIZE = WIDTH, HEIGHT = (1200, 720)
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

colours = [
    (0, 0, 255),
    (0, 0, 0),
    (0, 0, 0),
    (255, 0, 0)
][::-1]
colour_positions = [
    (0, 0),
    (WIDTH, 0),
    (0, HEIGHT),
    (WIDTH, HEIGHT)
]

highest = 0
used = []
for y in range(HEIGHT):
    for x in range(WIDTH):
        colour = pygame.math.Vector3()
        
        distances = [[i, euclidean_distance(vec(pos), vec(x, y))] for i, pos in enumerate(colour_positions)]
        for dist in distances:
            i = dist[0]
            d = dist[1]
            multiplier = (d / sum([d[1] for d in distances]))
            colour += pygame.math.Vector3(colours[i]) * multiplier
            
        # for c in colour:
        #     c = abs(255 - c)
        screen.set_at((x, y), colour)
            
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

    # screen.fill((0, 0, 0))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()