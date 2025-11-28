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

from scipy.spatial import Delaunay

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

weight = 0
R = 255
G = 0
B = 0

    ##############################################################################################
    
def point_on_triangle(pt1, pt2, pt3):
    """
    Random point on the triangle with vertices pt1, pt2 and pt3.
    """
    x, y = sorted([random.random(), random.random()])
    s, t, u = x, y - x, 1 - y
    return (s * pt1[0] + t * pt2[0] + u * pt3[0],
            s * pt1[1] + t * pt2[1] + u * pt3[1])


class Del:
    def __init__(self, point_num=100):

        # self.super_triangle = [
        #     vec(WIDTH/2, 50),
        #     vec(50, HEIGHT-50),
        #     vec(WIDTH-50, HEIGHT-50)
        # ]

        self.points = np.array([
            vec(random.uniform(-50, WIDTH+50), random.uniform(-50, HEIGHT+50)) for i in range(point_num)
        ] + [
            vec(-50, -50),
            vec(-50, HEIGHT+50),
            vec(WIDTH+50, -50),
            vec(WIDTH+50, HEIGHT+50)
        ])
        self.vectors = np.array([
            vec([random.uniform(-1, 1), random.uniform(-1, 1)]) * 0.9 for i in range(point_num)
        ] + [
            vec(0, 0),
            vec(0, 0),
            vec(0, 0),
            vec(0, 0),
        ])

    def update(self, screen):
        self.points += self.vectors

        condition1 = self.points[:, 0] < -50
        condition2 = self.points[:, 1] < -50
        condition3 = self.points[:, 0] > WIDTH + 50
        condition4 = self.points[:, 1] > HEIGHT + 50

        self.vectors[condition1, 0] *= -1
        self.vectors[condition2, 1] *= -1
        self.vectors[condition3, 0] *= -1
        self.vectors[condition4, 1] *= -1

        self.triangles = Delaunay(self.points)
        self.draw(screen)

    def draw(self, screen):
        global weight, R, G, B
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            weight += 20
        elif keys[pygame.K_DOWN]:
            weight -= 20
            
        if keys[pygame.K_r] and keys[pygame.K_i]:
            R += 2
        if keys[pygame.K_r] and keys[pygame.K_k]:
            R -= 2
        if keys[pygame.K_g] and keys[pygame.K_i]:
            G += 2
        if keys[pygame.K_g] and keys[pygame.K_k]:
            G -= 2
        if keys[pygame.K_b] and keys[pygame.K_i]:
            B += 2
        if keys[pygame.K_b] and keys[pygame.K_k]:
            B -= 2


        for polygon in self.triangles.simplices:
            polygon = self.points[polygon]

            height = polygon[polygon[:, 1].argsort()][-1][1]
            ratio = 1 - ((height + weight) / HEIGHT)

            r = np.clip((R * ratio), 0, 255)
            g = np.clip((G * ratio), 0, 255)
            b = np.clip((B * ratio), 0, 255)

            pygame.draw.polygon(screen, (r, g, b), polygon, 0)
            # pygame.draw.polygon(screen, (10, 200, c), polygon, 1)
            
        # for p in self.points:
        #     pygame.draw.circle(screen, (255 - 255, 255 - 255, 255 - 255), p, 3)

d = Del()

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

    screen.fill((30, 30, 30), [0, 0, 125, 30])
    d.update(screen)

    #fps
    # font = pygame.font.SysFont('monospace', 30)
    # fps = font.render(f'FPS: {int(clock.get_fps())}', True, (215, 215, 215))
    # screen.blit(fps, (0, 0))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()