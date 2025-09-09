"""Incomplete"""

import random
import pygame
import time

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


PIXELS_PER_UNIT = 30
N = 20

recursiveBacktracking(N, 0, 0)

maze = [[["L", "R", "U", "D"] for _ in range(N)] for __ in range(N)]
pellets = [[1 for _ in range(N)] for __ in range(N)]


def coordinates(x, y):
    return x // PIXELS_PER_UNIT * PIXELS_PER_UNIT + PIXELS_PER_UNIT // 2, y // PIXELS_PER_UNIT * PIXELS_PER_UNIT + PIXELS_PER_UNIT // 2


def square(x, y):
    return int(x // PIXELS_PER_UNIT), int(y // PIXELS_PER_UNIT)


class Player:
    def __init__(self):
        self.x = PIXELS_PER_UNIT // 2
        self.y = PIXELS_PER_UNIT // 2
        self.direction = None


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

scr_width, scr_height = N * PIXELS_PER_UNIT, N * PIXELS_PER_UNIT
scr = pygame.display.set_mode((scr_width, scr_height))


class Enemy:
    def __init__(self):
        self.x, self.y = coordinates(random.randint(0, scr_width), random.randint(0, scr_height))
        self.direction = random.choice(["L", "R", "U", "D"])
        s_x, s_y = square(self.x, self.y)
        while self.direction in maze[s_x][s_y]:
            self.direction = random.choice(["L", "R", "U", "D"])


player = Player()
enemies = [Enemy() for _ in range(4)]
pellet_colour = (0, 0, 0)
frames = 0

add = True

start = time.time()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            player.x, player.y = coordinates(player.x, player.y)
            if event.key == pygame.K_LEFT:
                player.direction = "L"
            if event.key == pygame.K_RIGHT:
                player.direction = "R"
            if event.key == pygame.K_UP:
                player.direction = "U"
            if event.key == pygame.K_DOWN:
                player.direction = "D"

    scr.fill((0, 0, 0))

    end = time.time()
    dt = end - start
    start = time.time()

    for i, mx in enumerate(maze):
        for j, my in enumerate(mx):
            for di in my:
                if di == "L":
                    pygame.draw.line(scr, (255, 255, 255), (i * PIXELS_PER_UNIT, j * PIXELS_PER_UNIT),
                                     (i * PIXELS_PER_UNIT, (j + 1) * PIXELS_PER_UNIT), 2)
                elif di == "R":
                    pygame.draw.line(scr, (255, 255, 255), ((i + 1) * PIXELS_PER_UNIT, j * PIXELS_PER_UNIT),
                                     ((i + 1) * PIXELS_PER_UNIT, (j + 1) * PIXELS_PER_UNIT), 2)
                elif di == "U":
                    pygame.draw.line(scr, (255, 255, 255), (i * PIXELS_PER_UNIT, j * PIXELS_PER_UNIT),
                                     ((i + 1) * PIXELS_PER_UNIT, j * PIXELS_PER_UNIT), 2)
                elif di == "D":
                    pygame.draw.line(scr, (255, 255, 255), (i * PIXELS_PER_UNIT, (j + 1) * PIXELS_PER_UNIT),
                                     ((i + 1) * PIXELS_PER_UNIT, (j + 1) * PIXELS_PER_UNIT), 2)
            if pellets[i][j] == 1:
                pygame.draw.circle(scr, pellet_colour, (i * PIXELS_PER_UNIT + PIXELS_PER_UNIT // 2, j * PIXELS_PER_UNIT + PIXELS_PER_UNIT // 2), 3)

    c_x, c_y = coordinates(player.x, player.y)
    s_y, s_x = square(player.x, player.y)
    pellets[s_y][s_x] = 0

    if all([not any(x) for x in pellets]):
        scr.fill((0, 0, 0))
        scr.blit(pygame.font.SysFont(None, 50).render("You win!", True, (255, 255, 255)), (10, 10))
        time.sleep(2)
        run = False

    if player.direction == "L":
        player.x -= 40 * dt
        if player.x < c_x and "L" in maze[s_y][s_x]:
            player.direction = None
            player.x, player.y = coordinates(player.x, player.y)
    if player.direction == "R":
        player.x += 40 * dt
        if player.x > c_x and "R" in maze[s_y][s_x]:
            player.direction = None
            player.x, player.y = coordinates(player.x, player.y)
    if player.direction == "U":
        player.y -= 40 * dt
        if player.y < c_y and "U" in maze[s_y][s_x]:
            player.direction = None
            player.x, player.y = coordinates(player.x, player.y)
    if player.direction == "D":
        player.y += 40 * dt
        if player.y > c_y and "D" in maze[s_y][s_x]:
            player.direction = None
            player.x, player.y = coordinates(player.x, player.y)

    for enemy in enemies:
        s_x, s_y = square(enemy.x, enemy.y)
        if enemy.direction == "L":
            enemy.x -= 40 * dt
            if enemy.x < c_x and "L" in maze[s_y][s_x]:
                enemy.x, enemy.y = coordinates(enemy.x, enemy.y)
                enemy.direction = random.choice(["L", "R", "U", "D"])
                while enemy.direction in maze[s_y][s_x]:
                    enemy.direction = random.choice(["L", "R", "U", "D"])
        elif enemy.direction == "R":
            enemy.x += 40 * dt
            if enemy.x > c_x and "R" in maze[s_y][s_x]:
                enemy.x, enemy.y = coordinates(enemy.x, enemy.y)
                enemy.direction = random.choice(["L", "R", "U", "D"])
                while enemy.direction in maze[s_y][s_x]:
                    enemy.direction = random.choice(["L", "R", "U", "D"])
        elif enemy.direction == "U":
            enemy.y -= 40 * dt
            if enemy.y < c_y and "U" in maze[s_y][s_x]:
                enemy.x, enemy.y = coordinates(enemy.x, enemy.y)
                enemy.direction = random.choice(["L", "R", "U", "D"])
                while enemy.direction in maze[s_y][s_x]:
                    enemy.direction = random.choice(["L", "R", "U", "D"])
        elif enemy.direction == "D":
            enemy.y += 40 * dt
            if enemy.y > c_y and "D" in maze[s_y][s_x]:
                enemy.x, enemy.y = coordinates(enemy.x, enemy.y)
                enemy.direction = random.choice(["L", "R", "U", "D"])
                while enemy.direction in maze[s_y][s_x]:
                    enemy.direction = random.choice(["L", "R", "U", "D"])

        pygame.draw.circle(scr, (255, 0, 0), (enemy.x, enemy.y), 10)

        if coordinates(player.x, player.y) == coordinates(enemy.x, enemy.y):
            scr.fill((0, 0, 0))
            scr.blit(pygame.font.SysFont(None, 50).render("You lose!", True, (255, 255, 255)), (10, 10))
            time.sleep(2)
            run = False

    pygame.draw.circle(scr, (0, 255, 0), (player.x, player.y), 10)

    if add:
        frames += 1
    else:
        frames -= 1

    if frames > 900:
        add = False
    if frames < 1:
        add = True

    pellet_colour = (frames / 2 ** 2 % 255, abs(128 - (frames / 2 ** 2 % 255)), frames / 2 ** 3 % 255)

    pygame.display.update()

pygame.quit()
