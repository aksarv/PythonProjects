"""
Not complete
"""
import pygame
import random
import time

pygame.init()

rows, cols = 16, 16
probability = 0.1
grid = [[1 if random.random() < probability else 0 for _ in range(cols)] for _ in range(rows)]
searched = [[0 for _ in range(cols)] for _ in range(rows)]
marked = [[0 for _ in range(cols)] for _ in range(rows)]
font = pygame.font.SysFont("Comic Sans MS", 24, bold=True)


def get_numbers(grid):
    numbers = []
    for i in range(len(grid)):
        number_row = []
        for j in range(len(grid[0])):
            if grid[i][j] != 1:
                number = 0
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        try:
                            if (not dx == 0 or not dy == 0) and grid[i + dx][j + dy] == 1:
                                number += 1
                        except IndexError:
                            pass
            else:
                number = -1
            number_row.append(number)
        numbers.append(number_row)

    return numbers


def expand(grid, x, y):
    frontier = set()
    visited = set()
    frontier.add((x, y))
    while True:
        print("Running...")
        new = set()
        for node in frontier:
            node_x, node_y = node
            if get_numbers(grid)[node_x][node_y] == 0:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if not dx == 0 or not dy == 0:
                            if 0 <= node_x + dx < rows and 0 <= node_y + dy < cols and get_numbers(grid)[node_x + dx][node_y + dy] != -1 and (node_x + dx, node_y + dy) not in visited:
                                new.add((node_x + dx, node_y + dy))
                                visited.add((node_x + dx, node_y + dy))
        if not new:
            break
        frontier = new

    for node in visited:
        node_x, node_y = node
        searched[node_x][node_y] = 1

    print("Done!")


grid_size = 50
scr_width, scr_height = cols * grid_size, rows * grid_size
first = False
start = time.time()

scr = pygame.display.set_mode((scr_width, scr_height))

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pressed()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x, grid_y = mouse_y // grid_size, mouse_x // grid_size
            if mouse[0]:
                if not first:
                    grid[grid_x][grid_y] = 0
                    first = True
                if grid[grid_x][grid_y] == 0:
                    expand(grid, grid_x, grid_y)
                elif get_numbers(grid)[grid_x][grid_y] > 0:
                    searched[grid_x][grid_y] = 1
                elif grid[grid_x][grid_y] == 1:
                    scr.fill((0, 0, 0))
                    scr.blit(font.render("Your ded", True, (255, 255, 255)), (0, 0))
                    time.sleep(1)
                    run = False
                else:
                    print("If your seeing this the program didnt work so yeah")
            elif mouse[2]:
                marked[grid_x][grid_y] = 1 - marked[grid_x][grid_y]

    end = time.time()
    difference = end - start
    start = time.time()

    scr.fill((0, 0, 0))

    for i in range(len(grid)):
        pygame.draw.line(scr, (255, 255, 255), (0, i * grid_size), (scr_width, i * grid_size))
    for i in range(len(grid[0])):
        pygame.draw.line(scr, (255, 255, 255), (i * grid_size, 0), (i * grid_size, scr_height))

    numbers = get_numbers(grid)
    for i in range(len(numbers)):
        for j in range(len(grid[0])):
            if numbers[i][j] not in [-1, 0]:
                scr.blit(font.render(str(numbers[i][j]), True, (255, 255, 255) if searched[i][j] == 1 else (255, 0, 0)), (j * grid_size + grid_size // 2 - 3, i * grid_size + grid_size // 2 - 3))
            elif numbers[i][j] == 0 and searched[i][j] == 1:
                pygame.draw.rect(scr, (0, 255, 0), [j * grid_size, i * grid_size, grid_size, grid_size])
            if marked[i][j] == 1:
                pygame.draw.circle(scr, (255, 0, 0), (j * grid_size + grid_size // 2, i * grid_size + grid_size // 2), 8)

    pygame.display.update()

pygame.quit()
