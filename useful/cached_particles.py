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
SIZE = WIDTH, HEIGHT = (1080, 720)
screen = pygame.display.set_mode(SIZE, flags, 16)
clock = pygame.time.Clock()

#renaming common functions
vec = pygame.math.Vector2

    ##############################################################################################

class Particle(pygame.sprite.Sprite):
    
    CACHED_IMAGES = {}

    @classmethod
    def vec_to_point(cls, vector):
        return (vector.x, vector.y)

    def __init__(self, pos, vel, size, col):
        super().__init__()
        self.pos = vec(pos)
        self.vel = vec(vel)

        self.size = size
        self.col = col

        self.image = self.get_image()
        self.rect = self.image.get_rect(topleft=self.pos)

    def update(self, dt):
        self.rect.topleft += self.vel * dt

        if self.rect.y < 0:
            self.rect.y = 0 
            self.vel.y *= -1
        if self.rect.y+self.rect.height > HEIGHT:
            self.rect.bottom = HEIGHT#-self.rect.y
            self.vel.y *= -1

        if self.rect.x < 0:
            self.rect.x = 0 
            self.vel.x *= -1
        if self.rect.x+self.rect.width > WIDTH:
            self.rect.right = WIDTH#-self.rect.y
            self.vel.x *= -1

        

    def get_image(self):
        cache_lookup = (self.vec_to_point(self.pos), self.col)
        
        if not (cached_image := self.CACHED_IMAGES.get(cache_lookup, None)):
            cached_image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            pygame.draw.circle(cached_image, self.col, (self.size/2, self.size/2), self.size/2)
            
            self.CACHED_IMAGES[cache_lookup] = cached_image
            
        return cached_image

particles = pygame.sprite.Group()

    ##############################################################################################

last_time = time.time()

running = True
while running:

    dt = (time.time() - last_time) * 60
    last_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False


    #if pygame.key.get_pressed()[pygame.K_SPACE]:
    if clock.get_fps() > 60:
        particles.add([Particle(
            (random.randint(0, WIDTH), 0),
            [random.randint(-100, 100)/10 , random.randint(50, 100)/10],
            10,
            (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        ) for i in range(20)])

    screen.fill((0, 0, 0))
    particles.update(dt)
    particles.draw(screen)

    #fps
    # font = pygame.font.SysFont('monospace', 30)
    # fps = font.render(f'FPS: {int(clock.get_fps())}', True, (215, 215, 215))
    # screen.blit(fps, (0, 0))
    pygame.display.set_caption(f"FPS: {int(clock.get_fps())} | Particles: {len(particles)}")

    pygame.display.update()
    clock.tick(2000)

pygame.quit()
sys.exit()