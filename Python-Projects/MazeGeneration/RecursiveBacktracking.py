import random
import pygame

visited = set()
connections = set()


def recursiveBacktracking(N, x, y):
    global visited, connections
    n = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    random.shuffle(n)
    visited.add((x, y))
    for dx, dy in n:
        if (x + dx, y + dy) not in visited and 0 <= x + dx < N and 0 <= y + dy < N:
            connections.add(tuple(sorted([(x, y), (x + dx, y + dy)], key=lambda l: (l[0], l[1]))))
            recursiveBacktracking(N, x + dx, y + dy)


PIXELS_PER_UNIT = 10
N = 20

recursiveBacktracking(N, 0, 0)

maze = [[["L", "R", "U", "D"] for _ in range(N)] for __ in range(N)]

for c in connections:
    (cx, cy), (nx, ny) = c
    if cx - nx == 1:
        maze[cx][cy].remove("L")
        maze[nx][ny].remove("R")
    elif nx - cx == 1:
        maze[cx][cy].remove("R")
        maze[nx][ny].remove("L")
    elif cy - ny == 1:
        maze[cx][cy].remove("U")
        maze[nx][ny].remove("D")
    elif ny - cy == 1:
        maze[cx][cy].remove("D")
        maze[nx][ny].remove("U")

pygame.init()

scr = pygame.display.set_mode((N * PIXELS_PER_UNIT, N * PIXELS_PER_UNIT))

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                print("Generating new maze...")
                visited = set()
                connections = set()
                recursiveBacktracking(N, 0, 0)
                print("...done")
                maze = [[["L", "R", "U", "D"] for _ in range(N)] for __ in range(N)]
                for c in connections:
                    (cx, cy), (nx, ny) = c
                    if cx - nx == 1:
                        maze[cx][cy].remove("L")
                        maze[nx][ny].remove("R")
                    elif nx - cx == 1:
                        maze[cx][cy].remove("R")
                        maze[nx][ny].remove("L")
                    elif cy - ny == 1:
                        maze[cx][cy].remove("U")
                        maze[nx][ny].remove("D")
                    elif ny - cy == 1:
                        maze[cx][cy].remove("D")
                        maze[nx][ny].remove("U")

    scr.fill((0, 0, 0))

    for i, mx in enumerate(maze):
        for j, my in enumerate(mx):
            for di in my:
                if di == "L":
                    pygame.draw.line(scr, (255, 255, 255), (i * PIXELS_PER_UNIT, j * PIXELS_PER_UNIT), (i * PIXELS_PER_UNIT, (j + 1) * PIXELS_PER_UNIT))
                elif di == "R":
                    pygame.draw.line(scr, (255, 255, 255), ((i + 1) * PIXELS_PER_UNIT, j * PIXELS_PER_UNIT), ((i + 1) * PIXELS_PER_UNIT, (j + 1) * PIXELS_PER_UNIT))
                elif di == "U":
                    pygame.draw.line(scr, (255, 255, 255), (i * PIXELS_PER_UNIT, j * PIXELS_PER_UNIT), ((i + 1) * PIXELS_PER_UNIT, j * PIXELS_PER_UNIT))
                elif di == "D":
                    pygame.draw.line(scr, (255, 255, 255), (i * PIXELS_PER_UNIT, (j + 1) * PIXELS_PER_UNIT), ((i + 1) * PIXELS_PER_UNIT, (j + 1) * PIXELS_PER_UNIT))

    pygame.display.update()

pygame.quit()
