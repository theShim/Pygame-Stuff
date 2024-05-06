import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import contextlib
with contextlib.redirect_stdout(None):
    import pygame
    import pygame.gfxdraw
    from pygame.locals import *
    
import random
import sys
import math
import time
import numpy as np
from scipy.interpolate import interp1d

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

def get_curve(points):
    x_new = np.arange(points[0].x, points[-1].x, 1)
    x = np.array([i.x for i in points[:-1]])
    y = np.array([i.y for i in points[:-1]])
    f = interp1d(x, y, kind='cubic', fill_value='extrapolate')
    y_new = f(x_new)
    x1 = list(x_new)
    y1 = list(y_new)
    points = [vec(x1[i], y1[i]) for i in range(len(x1))]
    return points

class Spring(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = vec(pos)
        self.radius = 10
        self.target_height = HEIGHT//2 + 150

        self.dampening = 0.05 * 2
        self.tension = 0.01
        self.vel = 0
        self.held = False

        self.draw_flag = not False

    def move(self):
        dh = self.target_height - self.pos.y
        if abs(dh) < 0.01:
            self.pos.y = self.target_height
        
        self.vel += self.tension * dh - self.vel * self.dampening
        self.pos.y += self.vel

    def mouse_collide(self):
        mouse = pygame.mouse.get_pressed()
        mousePos = pygame.mouse.get_pos()

        if mouse[0]:
            if vec(mousePos).distance_to(self.pos) < self.radius:
                self.held = True
        else:
            self.held = False

        if self.held:
            self.pos.y = vec(mousePos).y


    def update(self, screen):
        self.mouse_collide()
        self.move()
        self.draw(screen)

    def draw(self, screen):
        if self.draw_flag:
            start, end = int(min(self.pos.y, self.target_height)), int(max(self.pos.y, self.target_height))
            for y in range(start, end, 20):
                pygame.draw.circle(screen, (255, 255, 255), (self.pos.x, y), self.radius/8)

            pygame.draw.circle(screen, (255, 255, 255), self.pos, self.radius)


class Wave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.springs = pygame.sprite.Group()

        self.dist = 80
        for i in range(-20, WIDTH+self.dist, self.dist):
            self.springs.add(Spring((i, 0*HEIGHT/2)))

    def spread_wave(self):
        spread = 0.02
        for i in range(len(self.springs)):
            springs = self.springs.sprites().copy()
            if i > 0:
                springs[i - 1].vel += spread * (springs[i].pos.y - springs[i - 1].pos.y)
            try:
                springs[i + 1].vel += spread * (springs[i].pos.y - springs[i + 1].pos.y)
            except IndexError:
                pass

    def update(self, screen):
        self.draw(screen)

        self.springs.update(screen)
        self.spread_wave()

    def draw(self, screen):
        springs = self.springs.sprites().copy()
        points = get_curve(list(map(lambda s: s.pos, springs)))

        surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        surf.fill((36, 80, 255, 124))
        pygame.draw.polygon(
            surf,
            (40, 40, 40),
            points + [(WIDTH, 0), (0, 0)]
        )
        screen.blit(surf, (0, 0))

        for i in range(2, len(points)):
            # pygame.gfxdraw.bezier(screen, [springs[i-2].pos, springs[i-1].pos, springs[i].pos], 2, (255, 255, 255))
            pygame.draw.line(screen, (255, 255, 255), points[i-1], points[i])


    ##############################################################################################

wave = Wave()

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

    screen.fill((40, 40, 40))
    wave.update(screen)

    #fps
    font = pygame.font.SysFont('monospace', 30)
    fps = font.render(f'FPS: {int(clock.get_fps())}', True, (215, 215, 215))
    screen.blit(fps, (0, 0))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()