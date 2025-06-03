"""
Uses 80% rule to play snake
"""

import pygame, random, math

pygame.init()

scr_width, scr_height = 300, 300
scr = pygame.display.set_mode((scr_width - 1, scr_height - 1))

snake = [[150, 150]]
direction = "R"

apple_x, apple_y = random.randint(0, 29) * 10, random.randint(0, 29) * 10

def accessible_squares(snake_start, rest_of_snake):
    squares = [snake_start]
    visited = []
    while squares:
        new_squares = []
        for square in squares:
            square_x, square_y = square
            for dx, dy in [(0, 10), (10, 0), (-10, 0), (0, -10)]:
                new_square = [square_x + dx, square_y + dy]
                if 0 <= new_square[0] < 300 and 0 <= new_square[1] < 300 \
                        and new_square not in visited and new_square not in rest_of_snake:
                    new_squares.append(new_square)
                    visited.append(new_square)
        squares = new_squares
    return visited

clock = pygame.time.Clock()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    scr.fill((0, 0, 0))

    best_directions = []
    for possible_direction in ["L", "R", "U", "D"]:
        tentative_snake = snake[:]
        if possible_direction == "R":
            next_position = [snake[-1][0] + 10, snake[-1][1]]
        elif possible_direction == "L":
            next_position = [snake[-1][0] - 10, snake[-1][1]]
        elif possible_direction == "U":
            next_position = [snake[-1][0], snake[-1][1] - 10]
        elif possible_direction == "D":
            next_position = [snake[-1][0], snake[-1][1] + 10]
        
        if not (0 <= next_position[0] < 300 and 0 <= next_position[1] < 300) or next_position in snake:
            continue
        
        tentative_snake.append(next_position)
        del tentative_snake[0]

        num_accessible_squares = len(accessible_squares(tentative_snake[-1], tentative_snake[:-1]))
        ratio = num_accessible_squares / (30 * 30)
        if ratio > 0.8:
            best_directions.append([possible_direction, abs(next_position[0] - apple_x) + abs(next_position[1] - apple_y)])

    if best_directions:
        best_directions.sort(key=lambda x: x[1])
        best_direction = best_directions[0][0]
        if (direction == "R" and best_direction == "L") or (direction == "U" and best_direction == "D") \
                or (direction == "D" and best_direction == "U") or (direction == "L" and best_direction == "R"):
            if len(best_directions) > 1:
                direction = best_directions[1][0]
        else:
            direction = best_direction

    if direction == "R":
        snake.append([snake[-1][0] + 10, snake[-1][1]])
    elif direction == "L":
        snake.append([snake[-1][0] - 10, snake[-1][1]])
    elif direction == "U":
        snake.append([snake[-1][0], snake[-1][1] - 10])
    elif direction == "D":
        snake.append([snake[-1][0], snake[-1][1] + 10])
    del snake[0]

    if not (0 <= snake[-1][0] < 300 and 0 <= snake[-1][1] < 300) or snake[-1] in snake[:-1]:
        run = False

    if snake[-1] == [apple_x, apple_y]:
        while [apple_x, apple_y] in snake:
            apple_x, apple_y = random.randint(0, 29) * 10, random.randint(0, 29) * 10
        snake.insert(0, snake[0][:])

    for square_x, square_y in snake:
        pygame.draw.rect(scr, (255, 255, 255), [square_x, square_y, 9, 9])
    pygame.draw.rect(scr, (255, 0, 0), [apple_x, apple_y, 9, 9])

    pygame.display.update()
    clock.tick(10)
