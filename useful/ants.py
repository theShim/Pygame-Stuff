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
    return (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255), 128)

def euclidean_distance(point1, point2):
    return vec(point1).distance_to(vec(point2))

def clamp(n, smallest, largest): 
    return max(smallest, min(n, largest))

    ##############################################################################################

def calculate_pair_distances(pairs):
    total = 0
    for pair in pairs:
        total += vec(pair[0]).distance_to(vec(pair[1]))
    return total

class Town(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = vec(random.randint(400, WIDTH-200), random.randint(100, HEIGHT-100))

    def update(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), self.pos, 12)


class Ant(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = vec(random.randint(100, WIDTH-100), random.randint(100, HEIGHT-100))
        self.visited = []
        self.moving_to = None

        self.line_colour = gen_colour()
        self.dead = False


    def calculate(self, screen):
        if self.moving_to != None: return

        towns_ = []
        desirabilities = []

        for t in towns:
            if t in self.visited: 
                continue

            dst = self.pos.distance_to(t.pos)
            if dst == 0: continue
            desirability = pow(1 / dst, 2.5) * 10**7

            if len(self.visited) > 0:
                for pair in final_pairs:
                    if vec(pair[0]) == self.visited[-1].pos and t.pos == vec(pair[1]):
                        desirability *= 100
                        break

            desirabilities.append(desirability)

            towns_.append(t)

            # c = clamp(((desirability * 10**7) / 100) * 255, 0, 255)
            # c = (c, c, c)
            # pygame.draw.line(screen, c, self.pos, t.pos, 8)

    
        if len(towns_) > 0:
            chosen = random.choices(
                towns_, weights=desirabilities, k=1
            )[0]
            self.moving_to = chosen

        else:
            self.dead = True

    def move(self):
        if self.moving_to == None: return

        debug = True
        if not debug:
            vector = (self.moving_to.pos - self.pos).normalize() * 16
            self.pos += vector
        else:
            self.pos = self.moving_to.pos.copy()

        if -8 <= int(self.moving_to.pos.distance_to(self.pos)) <= 8:
            self.visited.append(self.moving_to)
            self.moving_to = None
        

    def update(self, screen):
        self.calculate(screen)
        self.move()

        self.draw(screen)

    def draw(self, screen):
        for i in range(len(self.visited)):
            pygame.draw.line(screen, self.line_colour, self.visited[i-1].pos, self.visited[i].pos, 4)

        pygame.draw.circle(screen, (0, 0, 0), self.pos, 8)
        pygame.draw.circle(screen, (255, 255, 255), self.pos, 8, 1)


towns = pygame.sprite.Group()
for i in range(40):
    towns.add(Town())

ants = pygame.sprite.Group()
ants.add([Ant() for i in range(50)])

final_pairs = []
generation = 1
flag = False
total_distance = 0

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

            elif event.key == pygame.K_r:
                for a in ants:
                    a.dead = False
                    a.visited = []
                    a.pos = vec(random.randint(100, WIDTH-100), random.randint(100, HEIGHT-100))
                generation += 1

            elif event.key == pygame.K_SPACE:
                flag = not flag

    screen.fill((30, 30, 30))
    towns.update(screen)

    ants.update(screen)
    for a in ants:
        if a.dead == False:
            break
    else:
        visitations = []
        x = {}

        for a in ants:
            visited = [(i.pos.x, i.pos.y) for i in a.visited]
            pairs = []
            for i in range(len(visited)):
                pairs.append((visited[i-1], visited[i]))
            visitations.append(pairs)

        for v_ in visitations:
            for v in v_:
                if v not in list(x.keys()):
                    x[v] = 1
                else:
                    x[v] += 1

        final_pairs_ = []
        for pair in list(x.keys()):
            if x[pair] > len(ants)//10:
                if pair not in final_pairs_:
                    final_pairs_.append(pair)

        if len(final_pairs) == 0:
            final_pairs = [i for i in final_pairs_]
        elif calculate_pair_distances(final_pairs_) < calculate_pair_distances(final_pairs):
            final_pairs = [i for i in final_pairs_]

        total_distance = calculate_pair_distances(final_pairs)

        if flag:
            for a in ants:
                a.dead = False
                a.visited = []
                a.pos = vec(random.randint(100, WIDTH-100), random.randint(100, HEIGHT-100))
            generation += 1


    for pair in final_pairs:
        pygame.draw.line(screen, (255, 0, 0), pair[0], pair[1], 5)

    #fps
    font = pygame.font.SysFont('monospace', 30)
    fps = font.render(f'Generation: {generation}', True, (215, 215, 215))
    screen.blit(fps, (0, 0))
    dst = font.render(f'Total Distance: {round(total_distance, 2)}', True, (215, 215, 215))
    screen.blit(dst, (0, fps.get_height()))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()