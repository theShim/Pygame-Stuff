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

class Lightning:
    def __init__(self):
        self.segments = []
        self.start = vec(100, HEIGHT/2)
        self.end = vec(WIDTH-100, HEIGHT/2)
        self.t = 45

    def update(self, screen):
        self.segments = []
        self.segments.append([self.start, self.end])
        offset = 8
        self.t += math.radians(random.uniform(8, 12))

        self.start = vec((WIDTH/2) + math.sin(self.t) * WIDTH/2.5, (HEIGHT/2))
        self.end = vec((WIDTH/2) + math.sin(self.t - math.radians(45)) * WIDTH/2.5, HEIGHT/2)

        length_scale = 0.7
        def rotate(vector, angle):
            x, y = vector
            x_rot = x * math.cos(angle) - y * math.sin(angle)
            y_rot = x * math.sin(angle) + y * math.cos(angle)
            return x_rot, y_rot

        for gen in range(3):
            for segment in list(self.segments):
                self.segments.remove(segment)

                midpoint = segment[0].lerp(segment[1], 0.5)
                normal = (segment[1]-segment[0]).normalize()
                offset_vec = vec(-normal.y, normal.x)
                offset_vec *= random.uniform(-offset, offset)
                midpoint += offset_vec

                self.segments.append([segment[0], midpoint])
                self.segments.append([midpoint, segment[1]])

                # branches
                # direction = midpoint - segment[0]
                # split_end = rotate(direction, random.uniform(-math.pi / 8, math.pi / 8))  # Random small angle rotation
                # split_end = (split_end[0] * length_scale + midpoint[0], split_end[1] * length_scale + midpoint[1])
                # self.segments.append([midpoint, split_end])
            offset //= 2

        self.draw(screen)

    def draw(self, screen):
        i = 0
        for segment in self.segments:
            pygame.draw.line(screen, (255-i, 255-i, 255-i), segment[0], segment[1], 2)
            i += 0.5 if i < 128 else 0

l = Lightning()
ls = [l for i in range(1)]

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
    for l in ls:
        l.update(screen)

    #fps
    font = pygame.font.SysFont('monospace', 30)
    fps = font.render(f'FPS: {int(clock.get_fps())}', True, (215, 215, 215))
    screen.blit(fps, (0, 0))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()