# Breadth First Search

import pygame
def path(start, end, x, y, walls):
    paths = [[start]]
    discovered = []
    while True:
        for path in paths:
            copy = path.copy()
            last = path[-1]
            if last == end:
                return path
            neighbours = [[last[0]+1,last[1]],[last[0]-1,last[1]],[last[0],last[1]+1],[last[0],last[1]-1]]
            for neighbour in neighbours:
                if 0 < neighbour[0] < x and 0 < neighbour[1] < y and neighbour not in discovered and neighbour not in walls:
                    paths.append(copy+[neighbour])
            for neighbour in neighbours:
                if 0 < neighbour[0] < x and 0 < neighbour[1] < y:
                    discovered.append(neighbour)
start = [1,1]
end = [50,50]
x = 65
y = 65
display_walls = []
walls = []
way = None
square_size = 15
pygame.init()
scr = pygame.display.set_mode((x*square_size, y*square_size))
pygame.display.set_caption('Press S To Show Path, Click To Add Wall')
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
            if event.key == pygame.K_s:
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
