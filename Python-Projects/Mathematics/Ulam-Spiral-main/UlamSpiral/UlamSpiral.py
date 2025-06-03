import pygame
pygame.init()
def is_Prime(num):
    if num == 1:
        return False
    if num == 2:
        return True
    if num % 2 == 0:
        return False
    for x in range(3, int(num**0.5)+1, 2):
        if num % x == 0:
            return False
    return True
scr = pygame.display.set_mode((500, 500))
ulam = []
incriment = 1
minus = True
print('Calculating Ulam Spiral...')
for _ in range(1000):
    for x in range(incriment):
        if minus:
            ulam.append('-1x')
        else:
            ulam.append('+1x')
    for x in range(incriment):
        if minus:
            ulam.append('-1y')
        else:
            ulam.append('+1y')
    minus = not minus
    incriment += 1
number = 1
start = [250, 250]
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if is_Prime(number):
        pygame.draw.rect(scr, (255, 255, 255), [start[0], start[1], 1, 1])
        pygame.display.update()
    try:
        if ulam[number-1] == '-1x':
            start[0] -= 1
        if ulam[number-1] == '-1y':
            start[1] -= 1
        if ulam[number-1] == '+1x':
            start[0] += 1
        if ulam[number-1] == '+1y':
            start[1] += 1
    except IndexError:
        break
    number += 1
    pygame.display.update()
