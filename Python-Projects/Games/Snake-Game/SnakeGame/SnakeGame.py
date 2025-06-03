# Snake game in about 10 minutes
import pygame, sys
from pygame.locals import QUIT
import random

pygame.init()
scr = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Snake Game')
snake = [[200,150]]
clock = pygame.time.Clock()
appleX, appleY = random.choice(range(0,400,10)),random.choice(range(0,300,10))
direction = None
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_UP:
            direction='U'
          if event.key == pygame.K_DOWN:
            direction='D'
          if event.key == pygame.K_LEFT:
            direction='L'
          if event.key == pygame.K_RIGHT:
            direction='R'
    scr.fill((255,255,255))
    if direction == 'L':
      snake.append([snake[-1][0]-10,snake[-1][1]])
      del snake[0]
    if direction == 'R':
      snake.append([snake[-1][0]+10,snake[-1][1]])
      del snake[0]
    if direction == 'U':
      snake.append([snake[-1][0],snake[-1][1]-10])
      del snake[0]
    if direction == 'D':
      snake.append([snake[-1][0],snake[-1][1]+10])
      del snake[0]
    pygame.draw.rect(scr,(255,0,0),[appleX,appleY,10,10])
    if snake[-1][0]==appleX and snake[-1][1]==appleY:
      if direction == 'L':
        snake.append([snake[-1][0]-10,snake[-1][1]])
      if direction == 'R':
        snake.append([snake[-1][0]+10,snake[-1][1]])
      if direction == 'U':
        snake.append([snake[-1][0],snake[-1][1]-10])
      if direction == 'D':
        snake.append([snake[-1][0],snake[-1][1]+10])
      appleX, appleY = random.choice(range(0,400,10)),random.choice(range(0,300,10))
    if not 0<snake[-1][0]<400 or not 0<snake[-1][1]<300:
      break
    for sq in snake:
      pygame.draw.rect(scr,(0,0,0),[sq[0],sq[1],10,10])
    pygame.display.update()
    clock.tick(20)
