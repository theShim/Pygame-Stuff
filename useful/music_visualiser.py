import os

import contextlib
with contextlib.redirect_stdout(None):
    import pygame
    from pygame.locals import *

import wave
from scipy.fftpack import dct
    
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

BAR_NUMBER = 30
BAR_WIDTH = WIDTH / BAR_NUMBER
BAR_HEIGHT = HEIGHT

beats = 0
delay = 0

    ##############################################################################################

class Music_Visualiser:
    def __init__(self):
        self.player = Music_Player()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.player.start()

        if self.player.status == 'stopped':
            self.player.current_nframes = self.player.nframes

        elif self.player.status == 'playing':
            self.player.current_nframes -= (self.player.framerate / 60)

            if self.player.current_nframes > 0:
                self.draw(screen)

        global delay
        if delay > 0:
            delay -= 1


    def draw(self, screen):
        nframes = int(self.player.current_nframes)
        original = self.player.nframes
        h = abs(dct(self.player.wave_data[0][original - nframes:original - nframes + BAR_NUMBER]))
        h = [min(HEIGHT, int(i**(1 / 2.5) * HEIGHT / 100)) for i in h]

        global beats, delay
        if h[0] >= HEIGHT and delay == 0:
            global beats
            beats += 1
            delay = 15
        self.draw_bars(screen, h)

    def draw_bars(self, screen, heights):
        for i, height in enumerate(heights):
            pygame.draw.rect(screen, (255, 255, 255), [i*BAR_WIDTH, HEIGHT - height, BAR_WIDTH, height])
            pygame.draw.rect(screen, (0,   0,   0  ), [i*BAR_WIDTH, HEIGHT - height, BAR_WIDTH, height], 1)
        # print('#')


class Music_Player:
    def __init__(self):
        pygame.mixer.music.load("amogus_drip.wav")
        self.get_music_wave_data()

        self.status = 'stopped'

    def get_music_wave_data(self):
        f = wave.open("amogus_drip.wav", 'rb')
        params = f.getparams()
        self.nchannels, self.sampwidth, self.framerate, self.nframes = params[:4]
        self.current_nframes = self.nframes

        str_data = f.readframes(self.nframes)
        f.close()
        
        wave_data = np.frombuffer(str_data, dtype = np.short)
        wave_data.shape = -1, 2
        self.wave_data = wave_data.T

    def song_position(self):
        seconds = max(0, pygame.mixer.music.get_pos() / 1000)
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        hms = ("%02d:%02d:%02d" % (h, m, s))
        return hms

    def start(self):
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent()
        pygame.mixer.music.set_volume(0.2)
        self.status = "playing"
        self.get_music_wave_data()


m = Music_Visualiser()

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
    m.update()
    
    pygame.display.set_caption(f"Beats: {beats}")
    # info = font.render(m.player.song_position(), True, (255,255,255))
    # screen.blit(info,(0, 30))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()