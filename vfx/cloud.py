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
SIZE = WIDTH, HEIGHT = (1200, 800)
screen = pygame.display.set_mode(SIZE, flags)
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

class Cloud(pygame.sprite.Sprite):
    def __init__(self, pos=(WIDTH/2, HEIGHT/2)):
        self.image = pygame.Surface((500, 300))
        
        start_radius = 20
        stack = [[(self.image.width/2, self.image.height - 1), start_radius]]
        col = (200, 200, 200)

        while stack:
            current, radius = stack.pop()
            pygame.draw.circle(self.image, col, current, radius)

            radius -= 2
            if radius > 0:
                for i in range(-1, 2):
                    for j in range(-1, 0):
                        if not(i == j == 0):
                            if random.randint(0, 1): 
                                stack.append([vec(current) + vec(i, j) * radius, radius])
        
        self.pos = pos

    def update(self):
        screen.blit(self.image, self.image.get_rect(center=self.pos))

c = Cloud()

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
    c.update()

    #fps
    font = pygame.font.SysFont('monospace', 30)
    fps = font.render(f'FPS: {int(clock.get_fps())}', True, (215, 215, 215))
    screen.blit(fps, (0, 0))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()