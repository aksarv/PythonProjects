# Best First Search

import pygame
def path(start, end, x, y, walls):
    pathsofar = [start]
    while True:
        deletes = []
        neighbor1 = [[pathsofar[-1][0], pathsofar[-1][1]+1]]
        neighbor2 = [[pathsofar[-1][0], pathsofar[-1][1]-1]]
        neighbor3 = [[pathsofar[-1][0]+1, pathsofar[-1][1]]]
        neighbor4 = [[pathsofar[-1][0]-1, pathsofar[-1][1]]]
        combined = neighbor1+neighbor2+neighbor3+neighbor4
        for n in combined:
            if n[0] < 1 or n[0] > x or n[1] < 1 or n[1] > y:
                combined.remove(n)
            for o in walls:
                if o[0] == n[0] and o[1] == n[1]:
                    deletes.append(n)
        combined = [x for x in combined if x not in deletes and x not in pathsofar]
        if len(combined) == 0:
            walls.append(pathsofar[-1])
            pathsofar = pathsofar[:-1]
        else:
            distances = []
            for item in combined:
                if item == end:
                    pathsofar.append(item)
                    return pathsofar
                distance = ((end[1]-item[1])**2+(end[0]-item[0])**2)**0.5
                distances.append([item, distance])
            minimum = sorted(distances, key=lambda l: l[1])[0][0]
            pathsofar.append(minimum)
start = eval(input('Enter start coord '))
end = eval(input('Enter end coord '))
x = eval(input('Enter x size '))
y = eval(input('Enter y size '))
display_walls = []
walls = []
way = None
square_size = 15
pygame.init()
scr = pygame.display.set_mode((x*square_size, y*square_size))
pygame.display.set_caption('Press F To Reveal Path, Click To Add Wall')
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousex, mousey = pygame.mouse.get_pos()
            display_walls.append([mousex // square_size * square_size, mousey // square_size * square_size])
            walls.append([mousex // square_size, mousey // square_size])
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                way = path(start, end, x, y, walls)
    scr.fill((0, 0, 0))
    pygame.draw.rect(scr, (255, 0, 0), [start[0] * square_size, start[1] * square_size, square_size, square_size])
    pygame.draw.rect(scr, (0, 0, 255), [end[0] * square_size, end[1] * square_size, square_size, square_size])
    for linex in range(0, x*square_size, square_size):
        pygame.draw.line(scr, (255, 255, 255), (linex, 0), (linex, x*square_size))
    for liney in range(0, y*square_size, square_size):
        pygame.draw.line(scr, (255, 255, 255), (0, liney), (y*square_size, liney))
    if display_walls != []:
        for wall in display_walls:
            pygame.draw.rect(scr, (255, 255, 255), [wall[0], wall[1], square_size, square_size])
    if way is not None:
        for square in way:
            pygame.draw.rect(scr, (0, 255, 0),  [square[0] * square_size, square[1] * square_size, square_size, square_size])
    pygame.display.update()
pygame.quit()
