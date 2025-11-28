import os

os.makedirs("assets", exist_ok=True)
os.makedirs("scripts", exist_ok=True)
os.makedirs("scripts/config", exist_ok=True)
os.makedirs("scripts/utils", exist_ok=True)

    ######################################################################

settings_code = """import pygame

DEBUG = False

SIZE = WIDTH, HEIGHT = (640, 400)
WINDOW_TITLE = "WINDOW TITLE"
FPS = 60
CAMERA_FOLLOW_SPEED = 12
TILE_SIZE = 32

Z_LAYERS = {
    "player" : 5
}

#   PHYSICS
FRIC = 0.9
GRAV = 0.4

CONTROLS = {
    "up"        : pygame.K_w,
    "down"      : pygame.K_s,
    "left"      : pygame.K_a,
    "right"     : pygame.K_d,
    "jump"      : pygame.K_SPACE,
}"""

with open("scripts/config/SETTINGS.py", "w") as f:
    f.write(settings_code)

    ######################################################################

corefuncs_code = r"""import pygame
import math
import random
import json

    ##############################################################################################

#   RENAMING COMMON FUNCTIONS
vec = pygame.math.Vector2
vec3 = pygame.math.Vector3

    ##############################################################################################

#   GENERAL STUFF
def gen_rand_colour() -> tuple[float]:
    return (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

def euclidean_distance(point1: list[float], point2: list[float]) -> float:
    return (((point1[0] - point2[0]) ** 2) + ((point1[1] - point2[1]) ** 2) ** 0.5)

def rotate(origin: list, point: list, angle: float) -> list[float]:
    ox, oy = origin
    px, py = point
    angle = math.radians(angle)

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return [qx, qy]

def lerp(a: float, b: float, lerp_factor: float) -> float:
    return a + (b - a) * lerp_factor

def normalize(val, amt, target):
    if val > target + amt:
        val -= amt
    elif val < target - amt:
        val += amt
    else:
        val = target
    return val

#bezier stuff
def ptOnCurve(b, t):
    q = b.copy()
    for k in range(1, len(b)):
        for i in range(len(b) - k):
            q[i] = (1-t) * q[i][0] + t * q[i+1][0], (1-t) * q[i][1] + t * q[i+1][1]
    return round(q[0][0]), round(q[0][1])

def bezierfy(points, samples): #no idea how this works just does, i think it's just recursive lerping though
    pts = [ptOnCurve(points, i/samples) for i in range(samples+1)]
    return pts

    ##############################################################################################

#   FILE STUFF
def read_file(path):
    file = open(path)
    data = file.readlines()
    file.close()
    return data

def write_file(path, data):
    file = open(path)
    file.write(data + '\n')
    file.close()


def read_json(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data

def write_json(path, dict):
    with open(path, 'w') as json_file:
        json.dump(dict, json_file)

    ##############################################################################################
    
class QuitWindow(BaseException):
    def __init__(self):
        super().__init__()

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

    def change_speed(self, speed: float|int):
        self.speed = speed

    def update(self):
        if self.run:
            if self.t < self.end:
                self.t += self.speed
            else:
                self.finished = True

    ##############################################################################################

#counting total number of lines written in the directory
import os                
def countLinesIn(directory):
    total_lines = 0
    uncommented_total = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                    total_lines += len(lines)
                    uncommented_total += len(list(filter(lambda l:l[0] != "#", filter(lambda l: len(l), map(lambda l: l.strip(), lines)))))
    print(f"Total Lines: {total_lines} | Uncommented: {uncommented_total}")"""

with open("scripts/utils/CORE_FUNCS.py", "w") as f:
    f.write(corefuncs_code)

    ######################################################################

boilerplate_code = """import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.environ['SDL_VIDEO_CENTERED'] = '1'

import contextlib
with contextlib.redirect_stdout(None):
    import pygame
    from pygame.locals import *
    
import random
import sys
import math
import time
import numpy as np

from scripts.config.SETTINGS import *
from scripts.utils.CORE_FUNCS import *

if DEBUG:
    #code profiling for performance optimisations
    import pstats
    import cProfile
    import io

    ##############################################################################################

class Game:
    def __init__(self):
        #intiaising pygame stuff
        self.initialise()

        #initalising pygame window
        flags = pygame.RESIZABLE | pygame.SCALED
        self.screen = pygame.display.set_mode(SIZE, flags)
        self.clock = pygame.time.Clock()

        #groups
        self.all_sprites = pygame.sprite.Group()

    def initialise(self):
        pygame.init()  #general pygame
        pygame.font.init() #font stuff
        pygame.display.set_caption(WINDOW_TITLE) #Window Title 

        pygame.mixer.pre_init(44100, 16, 2, 4096) #music stuff
        pygame.mixer.init()

        pygame.event.set_blocked(None) #setting allowed events to reduce lag
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEWHEEL])

    def calculate_offset(self):
        pass


    def run(self):
        if DEBUG:
            PROFILER = cProfile.Profile()
            PROFILER.enable()

        last_time = pygame.time.get_ticks()
        running = True
        while running:
            #deltatime
            self.dt = (current_time := pygame.time.get_ticks()) - last_time
            self.dt /= 1000
            last_time = current_time
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                    
            self.screen.fill((0, 0, 0))


            if DEBUG or not DEBUG:
                debug_info = f"FPS: {int(self.clock.get_fps())}"
                pygame.display.set_caption(f"{WINDOW_TITLE} | {debug_info}")

            pygame.display.update()
            self.clock.tick(FPS)

        if DEBUG:
            PROFILER.disable()
            PROFILER.dump_stats("test.stats")
            pstats.Stats("test.stats", stream=(s:=io.StringIO())).sort_stats((sortby:=pstats.SortKey.CUMULATIVE)).print_stats()
            print(s.getvalue())

        pygame.quit()
        sys.exit()
    

    ##############################################################################################

if __name__ == "__main__":
    game = Game()
    game.run()"""

with open(__file__, "w") as f:
    f.write(boilerplate_code)