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
pygame.display.set_caption("")

#initalising pygame window
flags = pygame.DOUBLEBUF #| pygame.FULLSCREEN
SIZE = WIDTH, HEIGHT = (720, 720)
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

joysticks = {}
point1 = vec(WIDTH/2, HEIGHT/2)
point2 = vec(WIDTH/2, HEIGHT/2)
speed = 1000000

    ##############################################################################################

last_time = time.time()
prev = [0, 0, 0, 0, 0, 0]

running = True
while running:

    dt = (time.time() - last_time) / 1000
    last_time = time.time()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            if event.key == pygame.K_r:
                point1 = vec(WIDTH/2, HEIGHT/2)
                point2 = vec(WIDTH/2, HEIGHT/2)

        elif event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
            if event.button == 0:
                joystick = joysticks[event.instance_id]
                print(joysticks)
                if joystick.rumble(0.5, 1, 1000):
                    print(f"Rumble effect played on joystick {event.instance_id}")

        if event.type == pygame.JOYDEVICEADDED:
            # This event will be generated when the program starts for every
            # joystick, filling up the list without needing to create them manually.
            joy = pygame.joystick.Joystick(event.device_index)
            joysticks[joy.get_instance_id()] = joy
            print(f"Joystick {joy.get_instance_id()} connected")

        if event.type == pygame.JOYDEVICEREMOVED:
            if event.instance_id in joysticks:
                del joysticks[event.instance_id]
                print(f"Joystick {event.instance_id} disconnected")
            else:
                print(
                    f"Tried to disconnect Joystick {event.instance_id}, "
                    "but couldn't find it in the joystick list"
                )

    screen.fill((30, 30, 30))

    point1.x += prev[0] * speed * dt
    point1.y += prev[1] * speed * dt
    pygame.draw.circle(screen, (255, 0, 0), point1, 16)

    point2.x += prev[2] * speed * dt
    point2.y += prev[3] * speed * dt
    pygame.draw.circle(screen, (0, 0, 255), point2, 16)

    
    for joystick in joysticks.values():
        axes = joystick.get_numaxes()
        axis = list(map(lambda v: 0 if abs(v) < 0.1 else v, [round(joystick.get_axis(i), 2) for i in range(axes)]))
        
        check = [abs(axis[i] - prev[i]) > 0.02 for i in range(axes)]
        if any(check):
            prev = axis
            print(axis)

    #fps
    font = pygame.font.SysFont('monospace', 30)
    fps = font.render(f'FPS: {int(clock.get_fps())}', True, (215, 215, 215))
    screen.blit(fps, (0, 0))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()