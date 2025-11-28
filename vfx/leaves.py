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

wind = 0

    ##############################################################################################

class Leaf(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((8, 8), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=pos)

        self.speed = random.uniform(2, 4)
        self.timer = random.uniform(0, 30)#random.randint(0, 360)

    def move(self):
        self.rect.y += self.speed
        self.rect.x += math.sin(self.timer) * 2 + wind
        self.timer -= 0.05

    def draw(self):
        self.image = pygame.Surface((8, 8), pygame.SRCALPHA)
        pos = vec(random.randint(3, 5), random.randint(3, 5))
        while True:
            self.image.set_at([int(pos.x), int(pos.y)], (random.randint(50, 200), random.randint(150, 250), (random.randint(0, 20))))
            if random.randint(1, 20) > 5:
                pos.x += random.randint(-1, 1) if random.randint(1, 10) == 1 else 0
                pos.y += random.randint(-1, 1) if random.randint(1, 10) == 1 else 0
                continue
            else:
                break
        self.image = pygame.transform.scale(self.image, vec(24, 24))

    def update(self):
        self.move()
        self.draw()

        if self.rect.y > WIDTH:
            leaves.remove(self)

leaves = pygame.sprite.Group()

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

    leaves.update()
    leaves.draw(screen)

    if random.randint(1, 1) == 1:
        leaves.add(Leaf((random.randint(WIDTH/4, WIDTH*3/4), 0)))

    #fps
    # font = pygame.font.SysFont('monospace', 30)
    # fps = font.render(f'FPS: {int(clock.get_fps())}', True, (215, 215, 215))
    # screen.blit(fps, (0, 0))
    pygame.display.set_caption(f"No. Leaves: {len(leaves)}")

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()