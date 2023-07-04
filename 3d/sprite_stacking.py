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
import copy

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
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point
    angle = math.radians(-angle)

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

    ##############################################################################################

class Car(pygame.sprite.Sprite):

    images = [pygame.image.load('car/' + img) for img in os.listdir('car')]
    images = [pygame.transform.scale(img, (14*4, 20*4)) for img in images]

    IMAGES = {}
    for angle in range(360):
        sprite = pygame.Surface((122, 122), pygame.SRCALPHA)
        for i, img in enumerate(images):
            rotated_img = pygame.transform.rotate(img, angle)
            sprite.blit(rotated_img, (sprite.get_width()//2 - rotated_img.get_width()//2, sprite.get_height()//2 + 8 - rotated_img.get_height()//2 - i*3))
            IMAGES[angle] = sprite


    def __init__(self, pos=vec(WIDTH//2, HEIGHT//2)):
        self.images = Car.IMAGES.copy()

        self.pos = vec(pos)
        self.width, self.height = self.images[0].get_size()

        self.vel = vec()
        self.acc = vec(.1, .1)
        self.max_vel = 2

        self.tyres = [
            vec(self.pos.x + self.width/2, self.pos.y + self.height/2),
            vec(self.pos.x + self.width/3, self.pos.y + self.height - 40),
            vec(self.pos.x + 2*self.width/3, self.pos.y + self.height - 40)
        ]
        
        self.rotation = 0
        self.turnSpeed = 2


    def move(self, keys):
        max_vel = self.max_vel# if not keys[pygame.K_LSHIFT] else self.max_vel * 1.5
        
        # #accelerating
        if keys[pygame.K_DOWN]:
            self.vel.x = min(self.vel.x + self.acc.x, max_vel)
            self.vel.y = min(self.vel.y + self.acc.y, max_vel)
        elif keys[pygame.K_UP]:
            self.vel.x = max(self.vel.x - self.acc.x, -max_vel)
            self.vel.y = max(self.vel.y - self.acc.y, -max_vel)

        #slowing down
        else:
            if self.vel.x >= 0: self.vel.x = max(self.vel.x - self.acc.x, 0)
            else:              self.vel.x = min(self.vel.x + self.acc.x, max_vel)

            if self.vel.y >= 0: self.vel.y = max(self.vel.y - self.acc.y, 0)
            else:              self.vel.y = min(self.vel.y + self.acc.y, max_vel)

        radians = math.radians(self.rotation)
        vel = self.vel.copy()
        if vel.x != 0.0 and vel.y != 0.0:
            vel *= 1/math.sqrt(2)

        x = math.sin(radians) * vel.x * 10
        y = math.cos(radians) * vel.y * 10

        self.pos.x += x
        self.pos.y += y

    def rotate(self, keys):
        if keys[pygame.K_LEFT]:
            self.rotation += self.turnSpeed
        if keys[pygame.K_RIGHT]:
            self.rotation -= self.turnSpeed

    def update(self, screen):
        keys = pygame.key.get_pressed()
        self.rotate(keys)
        self.move(keys)

        self.tyres = [
            vec(self.pos.x + self.width/2, self.pos.y + self.height/2),
            vec(self.pos.x + self.width/3, self.pos.y + self.height - 40),
            vec(self.pos.x + 2*self.width/3, self.pos.y + self.height - 40)
        ]
        self.render(screen)


    def render(self, screen):
        screen.blit(self.images[int(self.rotation%360)].copy(), self.pos)

        #tyre
        for tyre in self.tyres[1:]:
            p = vec(rotate(self.tyres[0], tyre, self.rotation))
            # pygame.draw.circle(screen, (255, 0, 255), p, 5)

            if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                particles.add(Trail(p))
                radians = math.radians(self.rotation)

                x = math.sin(radians) * self.vel.x
                y = math.cos(radians) * self.vel.y

                p.x += x * 1.5
                p.y += y * 1.5
                particles.add(Trail(p))

class Wheel:
    def __init__(self, pos):
        self.pos = vec(pos)
        self.angle = 0


class Trail(pygame.sprite.Sprite):
    def __init__(self, pos, col=(0, 0, 0)):
        super().__init__()
        self.pos = vec(pos)
        self.col = col
        self.timer = -50

    def update(self, screen):
        self.timer += 2
        if self.timer > 100:
            return particles.remove(self)
        self.draw(screen)

    def draw(self, screen):
        c = (pygame.math.Vector3(30, 30, 30) - pygame.math.Vector3(self.col)) * (self.timer/100)
        c = [max(i, 0) for i in c]
        pygame.draw.circle(screen, c, self.pos, 5)
        
car = Car((WIDTH//2, HEIGHT//2))
particles = pygame.sprite.Group()

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
    particles.update(screen)
    car.update(screen)

    pygame.display.set_caption(f"{car.pos}")
    #fps
    font = pygame.font.SysFont('monospace', 30)
    fps = font.render(f'FPS: {int(clock.get_fps())}', True, (215, 215, 215))
    screen.blit(fps, (0, 0))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()