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

class Timer:
    def __init__(self, duration: float, speed: float):
        self.t = 0
        self.end = duration
        self.speed = speed
        self.finished = False

        self.run = True

    #turn on/off
    def switch(self, flag:bool=None):
        if flag != None: 
            self.run = flag
        else: 
            self.run = not self.run

    def reset(self):
        self.t = 0
        self.finished = False

    def change_duration(self, duration: float|int):
        self.end = float(duration)

    def change_speed(self, speed: float|int):
        self.speed = float(speed)

    def update(self):
        if self.run:
            if self.t < self.end:
                self.t += self.speed
            else:
                self.finished = True

    ##############################################################################################

def gen_ellipse(r, a=1, b=0.5, n=100):
    t = np.linspace(0, 2 * math.pi, n)
    x = np.cos(t) * a * r
    y = np.sin(t) * b * r
    return np.vstack((x, y)).T

class Blackhole:
    def __init__(self, pos):
        self.children = pygame.sprite.LayeredUpdates()
        self.pos = pos

        self.circle = Blackhole_Circle(self, pos)
        self.children.add(self.circle)

        self.orb = Orb(self, pos - vec(0, HEIGHT * 0.2))
        self.children.add(self.orb)

        self.ring_timer = Timer(80, 1)
        self.ring_timer.switch(False)

    def update(self):
        self.ring_timer.update()
        if self.ring_timer.finished:
            self.ring_timer.reset()
            self.children.add(Blackhole_Ring(self, self.pos))

        self.children.update()

class Orb(pygame.sprite.Sprite):
    def __init__(self, parent, pos):
        self._layer = 2
        super().__init__()
        self.parent = parent
        self.pos = pos

        self.radius = 0
        self.max_radius = 160
        self.pause_timer = Timer(180, 1)
        self.increase_radius_timer = Timer(60, 0.5)

        self.child_orb_radius = 75
        self.child_orb_dist_timer = Timer(100, 1)
        self.child_rot_angle = 0
        self.child_rot_angle_mod = 1
        self.child_orb_poss = [vec(pos), vec(pos), vec(pos), vec(pos)]

    def update(self):
        self.pause_timer.update()
        if not self.pause_timer.finished: return

        self.increase_radius_timer.update()

        if self.increase_radius_timer.finished:
            self.child_orb_dist_timer.update()

            self.child_rot_angle += math.radians(self.child_rot_angle_mod)
            self.child_rot_angle_mod *= 1.0075
            self.child_rot_angle %= 2 * math.pi

            a = self.child_orb_dist_timer.t
            t = self.child_rot_angle

            self.child_orb_poss[0].xy = ((-a) * math.cos(t) - (-a) * math.sin(t), 0.5 * ((-a) * math.sin(t) + (-a) * math.cos(t))) + self.pos
            self.child_orb_poss[1].xy = ((-a) * math.cos(t + math.pi/2) - (-a) * math.sin(t + math.pi/2), 0.5 * ((-a) * math.sin(t + math.pi/2) + (-a) * math.cos(t + math.pi/2))) + self.pos
            self.child_orb_poss[2].xy = ((-a) * math.cos(t + math.pi) - (-a) * math.sin(t + math.pi), 0.5 * ((-a) * math.sin(t + math.pi) + (-a) * math.cos(t + math.pi))) + self.pos
            self.child_orb_poss[3].xy = ((-a) * math.cos(t - math.pi/2) - (-a) * math.sin(t - math.pi/2), 0.5 * ((-a) * math.sin(t - math.pi/2) + (-a) * math.cos(t - math.pi/2))) + self.pos
        
        else:
            self.radius = self.max_radius * (self.increase_radius_timer.t / self.increase_radius_timer.end)

        self.draw()

    def draw(self):
        # if self.child_orb_dist_timer.t <= 175:
        pygame.draw.circle(screen, (255, 255, 255), self.pos, self.radius)
        if self.child_orb_dist_timer.t:
            for pos in self.child_orb_poss:
                pygame.draw.circle(screen, (255, 255, 255), pos, self.child_orb_radius)

        pygame.draw.circle(screen, (0, 0, 0), self.pos, self.radius * 0.95)
        if self.child_orb_dist_timer.t:
            for pos in self.child_orb_poss:
                pygame.draw.circle(screen, (0, 0, 0), pos, self.child_orb_radius * 0.95)

        # else:
        #     for pos in sorted(self.child_orb_poss + [self.pos], key=lambda pos: pos.y):
        #         pygame.draw.circle(screen, (255, 255, 255), pos, (self.child_orb_radius if pos != self.pos else self.radius))
        #         pygame.draw.circle(screen, (0, 0, 0), pos, (self.child_orb_radius if pos != self.pos else self.radius) * 0.95)


class Blackhole_Ring(pygame.sprite.Sprite):
    def __init__(self, parent, pos):
        self._layer = 1
        super().__init__()
        self.parent = parent
        self.pos = pos
        self.ellipse = gen_ellipse(1)
        self.t = 1

    def update(self):
        self.t += 2
        self.draw()

    def draw(self):
        col = pygame.Color(255, 255, 255)
        ellipse = self.ellipse * self.t + self.pos
        pygame.draw.polygon(screen, col, ellipse, 6)

class Blackhole_Circle(pygame.sprite.Sprite):
    def __init__(self, parent, pos):
        super().__init__()
        self.parent = parent
        self.pos = pos

        self.radius = 0
        self.max_radius = 160
        self.angle = 0
        self.angle_mod = math.radians(3)
        self.ellipse = gen_ellipse(self.max_radius) + self.pos

        self.increase_radius_timer = Timer(60, 1)
        self.pause_before_end = Timer(40, 1)
        self.end_circle = Timer(1, 0.025)
        
    def update(self):
        self.angle += self.angle_mod
        # self.angle %= (2 * math.pi)

        self.increase_radius_timer.update()
        self.radius = self.max_radius * (self.increase_radius_timer.t / self.increase_radius_timer.end)

        if self.increase_radius_timer.finished:
            self.pause_before_end.update()
            if self.pause_before_end.finished:
                if self.end_circle.finished:
                    self.parent.ring_timer.switch(True)
                    return self.kill()
                self.end_circle.update()


        self.draw()

    def draw(self):
        ellipse = self.ellipse
        if not self.increase_radius_timer.finished:
            ellipse = gen_ellipse(self.radius) + self.pos
            
        col = pygame.Color(255, 255, 255).lerp(pygame.Color(30, 30, 30), self.end_circle.t ** 4)
        pygame.draw.polygon(screen, col, ellipse, 6)

        pygame.draw.polygon(screen, col, self.end_circle.t * (ellipse - self.pos) + self.pos, 6)
        
        pygame.draw.line(screen, col, (self.end_circle.t * (ellipse - self.pos) + self.pos)[int(len(ellipse) * (((self.angle) % (2 * math.pi))             / (2 * math.pi)))], ellipse[int(len(ellipse) * (((self.angle) % (2 * math.pi))             / (2 * math.pi)))], 6)
        pygame.draw.line(screen, col, (self.end_circle.t * (ellipse - self.pos) + self.pos)[int(len(ellipse) * (((self.angle + math.pi/2) % (2 * math.pi)) / (2 * math.pi)))], ellipse[int(len(ellipse) * (((self.angle + math.pi/2) % (2 * math.pi)) / (2 * math.pi)))], 6)
        pygame.draw.line(screen, col, (self.end_circle.t * (ellipse - self.pos) + self.pos)[int(len(ellipse) * (((self.angle + math.pi) % (2 * math.pi))   / (2 * math.pi)))], ellipse[int(len(ellipse) * (((self.angle + math.pi) % (2 * math.pi))   / (2 * math.pi)))], 6)
        pygame.draw.line(screen, col, (self.end_circle.t * (ellipse - self.pos) + self.pos)[int(len(ellipse) * (((self.angle - math.pi/2) % (2 * math.pi)) / (2 * math.pi)))], ellipse[int(len(ellipse) * (((self.angle - math.pi/2) % (2 * math.pi)) / (2 * math.pi)))], 6)

b = Blackhole(vec(WIDTH/2, 0.65 * HEIGHT))

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
    b.update()

    #fps
    font = pygame.font.SysFont('monospace', 30)
    fps = font.render(f'FPS: {int(clock.get_fps())}', True, (215, 215, 215))
    screen.blit(fps, (0, 0))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()