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

class Trail:
    def __init__(self, points):
        self.points = points

        self.move = vec(self.points[0])
        self.pointer = 0
        self.start = vec(self.points[self.pointer])
        self.end = vec(self.points[self.pointer+1])
        self.t = 0
        self.speed = 0.04

        self.after = pygame.sprite.Group()

    def walk(self):
        if self.t > 1:
            self.pointer = (self.pointer + 1) % len(self.points)
            self.t = 0
            self.start = vec(self.points[self.pointer])
            self.end = vec(self.points[self.pointer+1 if self.pointer+1 != len(self.points) else 0])

        self.move = self.start.lerp(self.end, self.t) + vec(random.uniform(-10, 10), random.uniform(-5, 10))
        x = 10
        for i in range(x):
            self.after.add(After_Trail(self.after, self.start.lerp(self.end, min(1, self.t + i*(self.speed/x))), 10))
        self.after.add(After_Trail(self.after, self.move.copy(), 10))

        self.t += self.speed

    def draw(self, screen):
        self.walk()

        for p in self.points:
            pygame.draw.circle(screen, (200, 0, 200), p, 8)

        self.after.update(screen)
        # pygame.draw.circle(screen, (0, 255, 0), self.move, 16)

class After_Trail(pygame.sprite.Sprite):
    def __init__(self, parent, pos, radius=16):
        super().__init__()
        self.parent = parent
        self.pos = pos
        self.alpha = 150
        self.decay = 10
        self.radius = radius

        self.surf = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.surf, (200, 200, 200), (radius, radius), radius)
        # self.surf.fill((0,))

    def update(self, screen):
        self.alpha -= self.decay
        if self.alpha <= 0:
            self.parent.remove(self)
        self.draw(screen)

    def draw(self, screen):
        self.surf.set_alpha(self.alpha)
        screen.blit(self.surf, self.pos)

d = 150
t = Trail([
    (d+100, d),
    (WIDTH-d, d+50),
    (WIDTH-d+70, HEIGHT-d-40),
    (d, HEIGHT-d),
])

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
    t.draw(screen)

    #fps
    font = pygame.font.SysFont('monospace', 30)
    fps = font.render(f'FPS: {int(clock.get_fps())}', True, (215, 215, 215))
    screen.blit(fps, (0, 0))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()