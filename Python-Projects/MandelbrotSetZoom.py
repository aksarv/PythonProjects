# not very efficient, need to find a faster way of rendering these images than just the traditional method
# also will research algorithms used to colour the set, currently just doing it with a greyscale, where (0,0,0) is for 0 iterations and (255,255,255) is for 200 iterations, with colours evenly spaced for iterations in between
import pygame
import numpy as np
import math
import time
import copy

def f(c):
    start = copy.deepcopy(complex(0, 0))
    for i in range(200):
        if copy.deepcopy(start).real > 10**100 or copy.deepcopy(start).imag > 10**100:
            return i
        try:
            start = copy.deepcopy(copy.deepcopy(copy.deepcopy(start)**2) + c)
        except OverflowError:
            return i
    return 200

def g(a, b):
    start = complex(a, b)
    for i in range(200):
        if start.real > 10**100 or start.imag > 10**100:
            return i
        try:
            start = start**2 + complex(0, 0)
        except OverflowError:
            return i
    return 200

zoom_factor = 20
zoom_x, zoom_y = -1.74531988487885027713447498273476085896634305722105696742129661865282261999558047224370153648579017846314194740797991061518048259961406132688167278725824724293, -0.000000978082303916948363693792283633260105830911508489009694726857654368230055199423519164101807022830669865841816700774913494015650301430112809841020578001922

pygame.init()

scr = pygame.display.set_mode((750, 750))
pygame.display.set_caption('Fractals')

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    scr.fill((0, 0, 0))
    for zoom in range(0, 1000):
        for i in np.linspace(-1/zoom_factor**zoom, 1/zoom_factor**zoom, 750):
            for j in np.linspace(-1/zoom_factor**zoom, 1/zoom_factor**zoom, 750):
                print(i)
                ti = zoom_x+i
                tj = zoom_y+j
                m = copy.deepcopy(f(complex(ti, tj)))
                pygame.draw.rect(scr, (int(m/200*255), int(m/200*255), int(m/200*255)), [i*375*zoom_factor**zoom+375, -j*375*zoom_factor**zoom+375, 1, 1])
        pygame.display.update()
        pygame.image.save(scr, f'{time.time()}.jpg')
        scr.fill((0, 0, 0))
