import pygame
import cv2
import numpy as np
import math

pygame.init()

scr_width, scr_height = 1280, 720
scr = pygame.display.set_mode((scr_width, scr_height))

texture = cv2.imread("sid.jpeg")
texture = cv2.cvtColor(texture, cv2.COLOR_BGR2RGB)
height, width, _ = texture.shape

tl = (100, 100)
tr = (400, 150)
bl = (70, 600)
br = (300, 400)
tl_x, tl_y = tl
bl_x, bl_y = bl
tr_x, tr_y = tr
br_x, br_y = br
points = [tl, tr, bl, br]

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    scr.fill((0, 0, 0))

    if pygame.mouse.get_pressed()[0]:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for i, x in enumerate(points):
            x1, y1 = x
            if math.sqrt((y1 - mouse_y) ** 2 + (x1 - mouse_x) ** 2) < 30:
                points[i] = (mouse_x, mouse_y)

    tl, tr, bl, br = points

    tl_x, tl_y = tl
    tr_x, tr_y = tr
    bl_x, bl_y = bl
    br_x, br_y = br

    for x in [tl, tr, bl, br]:
        x1, y1 = x
        pygame.draw.circle(scr, (255, 0, 0), (x1, y1), 10)

    for i, t in enumerate(np.linspace(0, 1, height)):
        l = ((1 - t) * tl_x + t * bl_x, (1 - t) * tl_y + t * bl_y)
        l_x, l_y = l
        r = ((1 - t) * tr_x + t * br_x, (1 - t) * tr_y + t * br_y)
        r_x, r_y = r
        for j, s in enumerate(np.linspace(0, 1, width)):
            p = ((1 - s) * l_x + s * r_x, (1 - s) * l_y + s * r_y)
            p_x, p_y = p
            col = texture[i][j]
            pygame.draw.rect(scr, col, [p_x, p_y, math.sqrt(((tl_y + bl_y) / 2 - (tr_y + br_y) / 2) ** 2 + ((tl_x + bl_x) / 2 - (tr_x + br_x) / 2) ** 2) / width, math.sqrt(((tl_y + bl_y) / 2 - (tr_y + br_y) / 2) ** 2 + ((tl_x + bl_x) / 2 - (tr_x + br_x) / 2) ** 2) / height])
    
    pygame.display.update()

pygame.quit()
