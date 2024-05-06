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

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = vec(pos)
        self.radius = 4
        
        self.vel = vec(random.uniform(-1, 1), random.uniform(-1, 1))
        self.acc = vec(0, 0)
        self.speed = 200

        self.colour = gen_colour()


    def move(self, dt):
        self.vel += self.acc * dt 
        self.pos += self.vel * dt * self.speed

        self.collide()

    def collide(self):
        if self.pos.x - self.radius < 0:
            self.pos.x = self.radius
            self.vel.x *= -1
        if self.pos.x + self.radius > WIDTH:
            self.pos.x = WIDTH - self.radius
            self.vel.x *= -1
            
        if self.pos.y - self.radius < 0:
            self.pos.y = self.radius
            self.vel.y *= -1
        if self.pos.y + self.radius > HEIGHT:
            self.pos.y = HEIGHT - self.radius
            self.vel.y *= -1

    def collide_particle(self, p):
        x = self.pos.x - p.pos.x
        y = self.pos.y - p.pos.y

        if x==0:x=-1
        if y==0:y=-1

        if abs(x) >= abs(y):
            self.vel = pygame.math.Vector2(x/abs(x), y/abs(x))
        else:
            self.vel = pygame.math.Vector2(x/abs(y), y/abs(y))

        # for p in particles:
        #     if p != self and euclidean_distance(p.pos, self.pos) < self.radius*2:
        #         collision(self, p)


    def update(self, screen, dt):
        self.move(dt)
        self.draw(screen)

    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, self.pos, self.radius)

particles = pygame.sprite.Group()
for i in range(50):
    particles.add(Particle((random.randint(0, WIDTH), random.randint(0, HEIGHT))))

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
    particles.update(screen, dt)

    #sweep and prune algorithm
    sorted_particles = sorted(particles, key=lambda p:p.pos.x)
    active = [sorted_particles.pop(0)]

    for i in range(len(sorted_particles)):
        p = sorted_particles.pop(0)
        for a in active:
            if euclidean_distance(p.pos, a.pos) < p.radius + a.radius:
                p.collide_particle(a)
                a.collide_particle(p)
            else:
                active = [p]
                break
                

    if clock.get_fps() >= 59.5:
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            [particles.add(Particle((random.randint(0, WIDTH), random.randint(0, HEIGHT)))) for i in range(5)]

    #fps
    # font = pygame.font.SysFont('monospace', 30)
    pygame.display.set_caption(f"FPS: {int(clock.get_fps())} | Particle No: {len(particles)}")

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()