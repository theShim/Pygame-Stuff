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
import colorsys

    ##############################################################################################

#initialising pygame stuff
pygame.init()  #general pygame
pygame.font.init() #font stuff
pygame.mixer.pre_init(44100, 16, 2, 4096) #music stuff
pygame.mixer.init()
pygame.event.set_blocked(None) #setting allowed events to reduce lag
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
pygame.display.set_caption("Colour Picker")

#initalising pygame window
flags = pygame.DOUBLEBUF #| pygame.FULLSCREEN
SIZE = WIDTH, HEIGHT = (1400, 768)
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

lerp = lambda a, b, t: a + (b-a) * t

    ##############################################################################################
    
    # screen.fill((30, 31, 34))
    # pygame.draw.rect(screen, (43, 45, 49), [1140, 0, 20, HEIGHT])
    # pygame.draw.rect(screen, (49, 51, 56), [0, 0, 1140, HEIGHT])

class ColourPicker:
    font = pygame.font.SysFont("monospace", 12, bold=True)

    def __init__(self, pos=(WIDTH/2, HEIGHT/2)):
        self.surf = pygame.Surface((376, 200), pygame.SRCALPHA)
        self.shadow = self.surf.copy()
        pygame.draw.rect(self.surf, (49, 51, 56), self.surf.get_rect(), 0, 10)
        pygame.draw.rect(self.surf, (0, 0, 0), [16, 16, self.surf.get_height()-32, self.surf.get_height()-32], 0, 10)
        pygame.draw.rect(self.surf, (43, 45, 49), [0, 0, self.surf.get_height(), self.surf.get_height()], 16, border_bottom_left_radius=10, border_top_left_radius=10)
        pygame.draw.rect(self.surf, (49+20, 51+20, 56+20), self.surf.get_rect(), 2, 10)
        pygame.draw.rect(self.shadow, (20, 21, 24), self.surf.get_rect(), 0, 10)
        self.rect = self.surf.get_rect(center=pos)
        
        self.red_slider = self.Slider(self, "Red", (208, (c:=40)-8))
        self.blue_slider = self.Slider(self, "Green", (208, c*2-8))
        self.green_slider = self.Slider(self, "Blue", (208, c*3-8))

    def update(self, screen):
        self.draw(screen)

    def draw(self, screen):

        col = [s.value for s in [self.red_slider, self.blue_slider, self.green_slider]]
        pygame.draw.rect(self.surf, col, [16, 16, self.surf.get_height()-32, self.surf.get_height()-32])

        screen.blit(self.shadow, vec(self.rect.topleft) + vec(5, 5))
        screen.blit(self.surf, self.rect)

        self.red_slider.update(screen)
        self.green_slider.update(screen)
        self.blue_slider.update(screen)

        col = (int(self.red_slider.value), int(self.green_slider.value), int(self.blue_slider.value))
        hsv = [round(c, 2) for c in colorsys.rgb_to_hsv(*(c/255.0 for c in col))]
        hls = [round(c, 2) for c in colorsys.rgb_to_hls(*(c/255.0 for c in col))]
        screen.blit(
            self.font.render(
                f"RGB: ({col[0]:>3}, {col[1]:>3}, {col[2]:>3})", 
                True, 
                (19, 20, 20)
            ), 
            vec(self.rect.topleft) + vec(206+1, 180-36+1-4)
        )
        screen.blit(
            self.font.render(
                f"HSL: ({hls[0]:>3}, {hls[2]:>3}, {hls[1]:>3})", 
                True, 
                (19, 20, 20)
            ), 
            vec(self.rect.topleft) + vec(206+1, 180-18+1-4)
        )
        screen.blit(
            self.font.render(
                f"HSV: ({hsv[0]:>3}, {hsv[1]:>3}, {hsv[2]:>3})", 
                True, 
                (19, 20, 20)
            ), 
            vec(self.rect.topleft) + vec(206+1, 180+1-4)
        )

        screen.blit(
            self.font.render(
                f"RGB: ({col[0]:>3}, {col[1]:>3}, {col[2]:>3})", 
                True, 
                (199, 201, 204)
            ), 
            vec(self.rect.topleft) + vec(206, 180-36-4)
        )
        screen.blit(
            self.font.render(
                f"HSL: ({hls[0]:>3}, {hls[2]:>3}, {hls[1]:>3})", 
                True, 
                (199, 201, 204)
            ), 
            vec(self.rect.topleft) + vec(206, 180-18-4)
        )
        screen.blit(
            self.font.render(
                f"HSV: ({hsv[0]:>3}, {hsv[1]:>3}, {hsv[2]:>3})", 
                True, 
                (199, 201, 204)
            ), 
            vec(self.rect.topleft) + vec(206, 180-4)
        )


    class Slider:
        font = pygame.font.SysFont("monospace", 18, bold=True)

        def __init__(self, parent, name, pos, min_=0, max_=255):
            self.name = name
            self.parent = parent

            self.bounds = [min_, max_]
            self.knob_x = 0
            self.surf_width = 160
            self.value = 0
            self.held = False
            
            self.surf = pygame.Surface((self.surf_width, 12), pygame.SRCALPHA)
            self.shadow = self.surf.copy()
            pygame.draw.rect(self.surf, (49+15, 51+15, 56+15), self.surf.get_rect(), 0, 5)
            pygame.draw.rect(self.surf, (49+25, 51+25, 56+25), self.surf.get_rect(), 2, 5)
            pygame.draw.rect(self.shadow, (10, 11, 14), self.surf.get_rect(), 0, 5)
            self.rect = self.surf.get_rect(topleft=vec(pos) + vec(parent.rect.topleft))

            self.label = self.font.render(self.name, True, (49+150, 51+150, 56+150))
            self.label_shadow = self.font.render(self.name, True, (20, 21, 24))

            self.knob = pygame.Surface((8, 16), pygame.SRCALPHA)
            pygame.draw.rect(self.knob, (49+15-20, 51+15-20, 56+15-20), self.knob.get_rect(), 0, 1)
            pygame.draw.rect(self.knob, (49+25-20, 51+25-20, 56+25-20), self.knob.get_rect(), 2, 1)
            self.knob_rect = self.knob.get_rect(topleft=vec(pos) + vec(parent.rect.topleft) - vec(0, 2))

        def mouse_collide(self):
            for s in [self.parent.red_slider, self.parent.blue_slider, self.parent.green_slider]:
                if s != self:
                    if s.held:
                        return
                    
            mousePos = vec(pygame.mouse.get_pos())
            mouse = pygame.mouse.get_pressed()

            if self.held == False:
                if self.knob_rect.collidepoint(mousePos) and mouse[0]:
                    self.knob_rect.x = mousePos.x
                    self.held = True
            else:
                if mouse[0]:
                    self.knob_rect.x = mousePos.x
                else:
                    self.held = False

            if self.knob_rect.x < self.rect.x:
                self.knob_rect.x = self.rect.x
            if self.knob_rect.x > self.rect.x + self.surf_width - 8:
                self.knob_rect.x = self.rect.x + self.surf_width - 8

        def update(self, screen):
            self.value = sorted([0, 255, ((self.knob_rect.x - self.rect.x) / (self.surf_width - 8)) * 255])[1]
            self.mouse_collide()

            v = int(self.value)
            self.label = self.font.render(f"{self.name}: {' ' * (8-len(str(v) + self.name)) + str(v)}", True, (49+150, 51+150, 56+150))
            self.label_shadow = self.font.render(f"{self.name}: {' ' * (8-len(str(v) + self.name)) + str(v)}", True, (20, 21, 24))

            self.draw(screen)

        def draw(self, screen):
            screen.blit(self.shadow, vec(self.rect.topleft) + vec(2, 2))
            screen.blit(self.surf, self.rect)

            x = ((self.knob_x - self.bounds[0]) / self.bounds[1]) * (self.bounds[1] - self.bounds[0])
            screen.blit(self.knob, vec(self.knob_rect.topleft) + vec(x, 0))

            screen.blit(self.label_shadow, vec(self.rect.topleft) - vec(-2, self.label.get_height()-2))
            screen.blit(self.label, vec(self.rect.topleft) - vec(0, self.label.get_height()))

c = ColourPicker()

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
    c.update(screen)

    #fps
    font = pygame.font.SysFont('monospace', 30)
    fps = font.render(f'FPS: {int(clock.get_fps())}', True, (215, 215, 215))
    screen.blit(fps, (0, 0))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()