import random
import pygame

print("Imports done")

N = 350
mst = set()
visited = set()
start = (0, 0)
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
                candidates.append((v, new_v, 1))
    min_weight = min(candidates, key=lambda l: l[2])[2]
    min_edge = random.choice([x for x in candidates if x[2] == min_weight])
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

scr_dim = 800
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
