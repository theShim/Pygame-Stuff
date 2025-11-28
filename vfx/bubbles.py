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
flags = pygame.DOUBLEBUF | pygame.SCALED#| pygame.FULLSCREEN
SIZE = WIDTH, HEIGHT = (400 * 2, 400 * 2)
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

class Black_Fire(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.children = pygame.sprite.Group()
        self.col = pygame.Color(47, 203, 200)
        self.col2 = (47, 203, 200)
        
        self.base = self.col
        self.t = 0

    def update(self):
        self.t += math.radians(1)
        interp = (math.sin(self.t) ** 2)
        self.col = self.base.lerp(self.col2, interp)

        mousePos = pygame.mouse.get_pos()
        for i in range(5):
            Black_Particle(self.children, mousePos, self.col, random.randint(20, 50))

        self.draw()

    def draw(self):
        self.children.update(None)
        self.children.update(False)
        self.children.update(True)

class Black_Particle(pygame.sprite.Sprite):
    def __init__(self, groups, pos, col, radius = 20):
        super().__init__(groups)
        self.pos = vec(pos)
        self.radius = radius
        self.decay = max(0.5, random.random())
        self.vel = vec(0, -1)

        self.t = random.uniform(0, math.pi)
        self.col = col

    def update(self, draw_flag):
        if draw_flag != None:
            return self.draw(draw_flag)
        
        self.t += math.radians(random.uniform(4, 10))
        

        self.radius -= self.decay
        self.vel = vec(0, -self.radius / 4)
        if self.radius <= 1:
            return self.kill()
        
        self.pos += self.vel
        self.vel = vec(random.uniform(-self.radius / 10, self.radius / 10) * 2, random.uniform(-self.radius / 10, self.radius / 10) * 2)#-random.uniform(3, 4))

    def draw(self, draw_flag):
        pos = [self.pos.x + math.sin(self.t) * 50, self.pos.y]
        if draw_flag in ["bg", False]:
            pygame.draw.circle(screen, (255, 255, 255), pos, self.radius)
        elif draw_flag in ["fg", True]:
            pygame.draw.circle(screen, self.col, pos, self.radius * 0.9)

    ##############################################################################################

fire = Black_Fire()

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

    screen.fill((47, 203, 200))
    fire.update()

    #fps
    font = pygame.font.SysFont('monospace', 30)
    fps = font.render(f'FPS: {int(clock.get_fps())}\n{len(fire.children)}', True, (215, 215, 215))
    screen.blit(fps, (0, 0))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()