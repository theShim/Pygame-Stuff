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

class Spark(pygame.sprite.Sprite):
    def __init__(self, pos, scale, angle, speed=None, colour=(255, 255, 255), spin=False, grav=False):
        super().__init__()
        self.pos = vec(pos)
        self.scale = scale
        self.angle = angle
        self.speed = random.uniform(3, 6) if speed == None else speed
        self.colour = colour

        self.spin = spin
        self.grav = grav

        for i in range(int(self.scale*2)+1):
            self.move()


    def move(self):
        self.pos += vec(math.cos(self.angle), math.sin(self.angle)) * self.speed

    def apply_gravity(self, friction, force, terminal_velocity):
        movement = vec(math.cos(self.angle), math.sin(self.angle)) * self.speed
        movement[1] = min(terminal_velocity, movement[1] + force)
        movement[0] *= friction
        self.angle = math.atan2(movement[1], movement[0])


    def update(self, screen):
        self.speed -= 0.1
        if self.speed < 0:
            return sparks.remove(self)
        
        if self.spin:
            self.angle += 0.1
        if self.grav:
            self.apply_gravity(0.975, 0.2, 8)
        self.move()
        
        self.draw(screen)

    def draw(self, screen):
        points = [
            vec(math.cos(self.angle), math.sin(self.angle)) * self.scale * self.speed,
            vec(math.cos(self.angle - math.pi/2), math.sin(self.angle - math.pi/2)) * 0.3 * self.scale * self.speed,
            vec(math.cos(self.angle - math.pi), math.sin(self.angle - math.pi)) * 3 * self.scale * self.speed + vec(random.random(), random.random())*self.speed,
            vec(math.cos(self.angle + math.pi/2), math.sin(self.angle + math.pi/2))  * 0.3 * self.scale * self.speed,
        ]
        points = list(map(lambda x: x+self.pos, points))
        pygame.draw.polygon(screen, self.colour, points)
        pygame.draw.polygon(screen, (0, 0, 0), points, math.ceil(self.scale/4))

        # for pos in points:
        #     pos += vec(SIZE)/2
        #     pygame.draw.circle(screen, (255, 0, 0), pos, 5)

class RunSmoke(Spark):
    def __init__(self, pos, scale):
        c = random.uniform(100, 255)
        super().__init__(pos, scale, math.radians(random.randint(180, 225)), colour=(c, c, c), grav=True)

sparks = pygame.sprite.Group()
sparks.add(
    Spark(vec(SIZE)/2, 4, math.radians(random.randint(0, 360)))
)

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
    sparks.update(screen)

    c = random.uniform(100, 255)
    sparks.add(Spark(pygame.mouse.get_pos(), random.uniform(2, 4), math.radians(random.randint(0, 360)), colour=(c, c, c), grav=True))
    # if random.randint(0, 5) == 0:
    #     sparks.add(RunSmoke(pygame.mouse.get_pos(), random.uniform(4, 8)/2))


    #fps
    font = pygame.font.SysFont('monospace', 30)
    fps = font.render(f'FPS: {int(clock.get_fps())}', True, (215, 215, 215))
    screen.blit(fps, (0, 0))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()  