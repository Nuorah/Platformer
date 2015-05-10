import pygame, sys, time, random, winsound
from pygame.locals import *

#initializing pygame and the clock and the mixer(?)
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
mainClock = pygame.time.Clock()

SIZE = 20
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
FPS = 60
G = 0.3
F = 0.9
J = 6
S = 5
MAXS = 9

keys = pygame.key.get_pressed()
