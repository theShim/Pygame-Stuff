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

class Fire(pygame.sprite.Sprite):
    def __init__(self, pos=vec((WIDTH/2, HEIGHT/2)), flame_intensity=2, angle=0):
        super().__init__()
        self.pos = vec(pos)
        self.oPos = self.pos.copy()

        self.flame_intensity = flame_intensity
        self.particles = pygame.sprite.Group()
        for i in range(self.flame_intensity * 25):
            self.particles.add(FireParticle((self.pos + vec(random.uniform(-5, 5), random.uniform(-5, 5))), random.randint(1, 5), self))

        self.angle = angle

    def update(self, screen):
        self.pos = rotate((WIDTH/2, HEIGHT/2), self.oPos, self.angle)
        self.angle += 1

        self.particles.update(screen)


class FireParticle(pygame.sprite.Sprite):
    alpha_layer_qty = 2
    alpha_glow_constant = 2

    def __init__(self, pos, radius, parent):
        super().__init__()
        self.parent = parent

        self.pos = vec(pos)
        self.radius = radius
        self.yellow = 0

        self.alpha_layers = FireParticle.alpha_layer_qty
        self.alpha_glow = FireParticle.alpha_glow_constant
        self.burn_rate = 0.1 * random.uniform(1, 4)

        max_size = 2 * self.radius * self.alpha_glow * self.alpha_layers ** 2
        self.surf = pygame.Surface((max_size, max_size), pygame.SRCALPHA)

    def burn(self):
        self.radius -= self.burn_rate
        if self.radius < 0:
            self.parent.particles.remove(self)
            self.parent.particles.add(FireParticle((self.parent.pos + vec(random.uniform(-5, 5), random.uniform(-5, 5))), random.randint(1, 5), self.parent))
            return True
        
        self.pos.x += random.uniform(-self.radius, self.radius)
        self.pos.y -= random.uniform(5, 8) - self.radius

        self.yellow += 8
        if self.yellow > 255:
            self.yellow = 255


    def update(self, screen):
        dead = self.burn()
        if dead: return
         
        self.draw(screen)

    def draw(self, screen):
        max_size = 2 * self.radius * self.alpha_glow * self.alpha_layers ** 2
        self.surf = pygame.Surface((max_size, max_size), pygame.SRCALPHA)

        for i in range(self.alpha_layers, -1, -1):
            alpha = 255 - i * (255 // self.alpha_layers - 5)
            if alpha < 0: alpha = 0

            radius = self.radius * self.alpha_glow * i**2
            pygame.draw.circle(self.surf, (255, self.yellow, 0, alpha), list(map(lambda x: x/2, self.surf.get_size())), radius)
        screen.blit(self.surf, self.surf.get_rect(center=self.pos))

    ##############################################################################################

fire = pygame.sprite.Group()
for angle in range(0, 360, 45):
    fire.add(Fire((WIDTH/2, HEIGHT/5), flame_intensity=2, angle=angle)) #pygame.sprite.Group()
# for i in range(10):
#     fire.add(FireParticle((WIDTH/2, HEIGHT/2), 4))

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
    fire.update(screen)

    #fps
    font = pygame.font.SysFont('monospace', 30)
    fps = font.render(f'FPS: {int(clock.get_fps())}', True, (215, 215, 215))
    screen.blit(fps, (0, 0))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()