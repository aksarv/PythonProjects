import random
import pygame
import cv2
import numpy as np

img = cv2.imread("sm.png")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

height, width, _ = img.shape

print("Imports done")

N = 100
mst = set()
visited = set()
start = (random.randint(0, N - 1), random.randint(0, N - 1))
visited.add(start)


def get_dir(s_x, s_y, e_x, e_y):
    if s_x == e_x:
        if s_y - e_y == 1:
            return "L"
        elif e_y - s_y == 1:
            return "R"
    else:
        if s_x - e_x == 1:
            return "U"
        elif e_x - s_x == 1:
            return "D"


print("Generating MST...")

while len(visited) < N ** 2:
    print(round(len(visited) / N ** 2 * 100, 2), "% complete")
    candidates = []
    for v in visited:
        for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            new_v = (v[0] + dx, v[1] + dy)
            new_x, new_y = new_v
            if 0 <= new_x < N and 0 <= new_y < N and new_v not in visited:
                cell_x = int((new_x + 0.5) / N * height)
                cell_y = int((new_y + 0.5) / N * width)
                cell_x = min(height - 1, max(0, cell_x))
                cell_y = min(width - 1, max(0, cell_y))
                pixel = img[cell_x, cell_y]
                is_black = np.all(pixel < 60)
                candidates.append((v, new_v, (10 if is_black else 1)))
    min_weight = min(candidates, key=lambda l: l[2])[2]
    best_candidates = [x for x in candidates if x[2] == min_weight]
    if min_weight == 1:
        min_edge = random.choice(best_candidates)
    else:
        min_edge = next(x for x in best_candidates if get_dir(x[0][0], x[0][1], x[1][0], x[1][1]) == "R")
    mst.add(min_edge)
    visited.add(min_edge[1])

print("...done")

print("Generating maze...")

maze = [[["L", "R", "U", "D"] for __ in range(N)] for _ in range(N)]

for s, e, _ in mst:
    d = get_dir(s[0], s[1], e[0], e[1])
    opp_d = "L" if d == "R" else "R" if d == "L" else "U" if d == "D" else "D" if d == "U" else None
    maze[s[0]][s[1]].remove(d)
    maze[e[0]][e[1]].remove(opp_d)

print("...done")

pygame.init()

scr_dim = 720
scr = pygame.display.set_mode((scr_dim, scr_dim))

block_size = scr_dim / N

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    scr.fill((0, 0, 0))

    for i, row in enumerate(maze):
        for j, col in enumerate(row):
            for d in col:
                if d == "L":
                    pygame.draw.line(scr, (255, 255, 255), (j * block_size, i * block_size), (j * block_size, (i + 1) * block_size))
                elif d == "R":
                    pygame.draw.line(scr, (255, 255, 255), ((j + 1) * block_size, i * block_size), ((j + 1) * block_size, (i + 1) * block_size))
                elif d == "U":
                    pygame.draw.line(scr, (255, 255, 255), (j * block_size, i * block_size), ((j + 1) * block_size, i * block_size))
                elif d == "D":
                    pygame.draw.line(scr, (255, 255, 255), (j * block_size, (i + 1) * block_size), ((j + 1) * block_size, (i + 1) * block_size))

    pygame.display.update()
