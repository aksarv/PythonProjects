import numpy as np
import math
import pygame
import time

epsilon = 1e-6

def do_two_line_segments_intersect(x1, y1, x2, y2, x3, y3, x4, y4, origin_x, origin_y):
    if x2-x1==0 and x4-x3==0:
        return False
    if x2-x1 == 0:
        xi = x1
        m2 = (y4-y3)/(x4-x3)
        yi = m2*x1-m2*x3+y3
        if (y1<=yi<=y2 or y2<=yi<=y1) and (x3<=xi<=x4 or x4<=xi<=x3) and (y3<=yi<=y4 or y4<=yi<=y3):
            return [math.sqrt((origin_x-xi) ** 2 + (origin_y-yi) ** 2), xi, yi]
        return False
    if x4-x3 == 0:
        return do_two_line_segments_intersect(x3, y3, x4, y4, x1, y1, x2, y2, origin_x, origin_y)
    m1 = (y2-y1)/(x2-x1)
    m2 = (y4-y3)/(x4-x3)
    if abs(m1-m2)<epsilon:
        return False
    xi = (m1*x1-y1-m2*x3+y3)/(m1-m2)
    yi = m1*(xi-x1)+y1
    if (x1<=xi<=x2 or x2<=xi<=x1) and (x3<=xi<=x4 or x4<=xi<=x3) and (y1<=yi<=y2 or y2<=yi<=y1) and (y3<=yi<=y4 or y4<=yi<=y3):
        return [math.sqrt((origin_x-xi) ** 2 + (origin_y-yi) ** 2), xi, yi]
    return False

grid = [[1, 1, 1, 1, 1],
        [1, 0, 1, 0, 1],
        [1, 1, 1, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1]]

grid_square_width = 50
grid_square_height = 50

grid_lines = []
for i, x in enumerate(grid):
    for j, y in enumerate(x):
        if y == 1:
                a, b, c, d = [[j * grid_square_width, i * grid_square_height], [(j + 1) * grid_square_width, i * grid_square_height]], [[j * grid_square_width, i * grid_square_height], [j * grid_square_width, (i + 1) * grid_square_height]], [[(j + 1) * grid_square_width, i * grid_square_height], [(j + 1) * grid_square_width, (i + 1) * grid_square_height]], [[j * grid_square_width, (i + 1) * grid_square_height], [(j + 1) * grid_square_width, (i + 1) * grid_square_height]]
                grid_lines.append(a) if a not in grid_lines else None
                grid_lines.append(b) if b not in grid_lines else None
                grid_lines.append(c) if c not in grid_lines else None
                grid_lines.append(d) if d not in grid_lines else None

pos_x = 0
pos_y = 0

pos_grid_x = (pos_x + 1) * 50 + 10
pos_grid_y = (pos_y + 1) * 50 + 10
negative_pos_grid_y = -pos_grid_y
init_angle = 315
fov = 50
ray_depth = 200
ray_length = 150

distances = []
closest_points = []
final_points = []

for i, ray_angle in enumerate(list(np.linspace(init_angle - fov // 2, init_angle + fov // 2, ray_depth))):
    x_new = ray_length * math.cos(math.radians(ray_angle)) + pos_grid_x
    y_new = ray_length * math.sin(math.radians(ray_angle)) + negative_pos_grid_y
    final_points.append([x_new, y_new])
    shortest_distance = float('inf')
    closest_point = None
    for line in grid_lines:
        line_start, line_end = line
        line_start_x, line_start_y = line_start
        line_end_x, line_end_y = line_end
        line_start_y, line_end_y = -line_start_y, -line_end_y
        intersection = do_two_line_segments_intersect(pos_grid_x, negative_pos_grid_y, x_new, y_new, line_start_x, line_start_y, line_end_x, line_end_y, pos_grid_x, negative_pos_grid_y)
        if intersection:
            distance, intersection_x, intersection_y = intersection
            if abs(distance - shortest_distance) < epsilon:
                continue
            if distance < shortest_distance:
                shortest_distance = distance
                closest_point = [intersection_x, intersection_y]
    distances.append([i, shortest_distance])
    closest_points.append(closest_point)

pygame.init()

scr_width, scr_height = 720, 480
scr = pygame.display.set_mode((scr_width, scr_height))

bar_width = scr_width / ray_depth



run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    scr.fill((0, 0, 0))
    
    for i, d in distances:
        if d != float('inf'):
            d = (150-d)*2
            pygame.draw.rect(scr, (255, 255, 255), [i * bar_width, scr_height / 2 - d / 2, bar_width, d])

    pygame.draw.rect(scr, (0, 0, 0), [scr_width-250, 0, 250, 250])

    for q in final_points:
        q_x, q_y = q
        pygame.draw.line(scr, (255, 128, 64), (scr_width-250+q_x, -q_y), (scr_width-250+pos_grid_x, pos_grid_y))
        pygame.draw.circle(scr, (0, 255, 255), (scr_width-250+q_x, -q_y), 3)

    for line in grid_lines:
        first_point, second_point = line
        first_point_x, first_point_y = first_point
        second_point_x, second_point_y = second_point
        pygame.draw.line(scr, (0, 0, 255), (scr_width-250+first_point_x, first_point_y), (scr_width-250+second_point_x, second_point_y))
    
    pygame.draw.circle(scr, (255, 0, 0), (scr_width-250+pos_grid_x, pos_grid_y), 3)

    pygame.draw.line(scr, (255, 0, 0), (scr_width-250+pos_grid_x, pos_grid_y), (scr_width-250+pos_grid_x + 50, pos_grid_y + 50 * math.tan(math.radians(init_angle))))
    
    for p in closest_points:
        if p is not None:
            p_x, p_y = p
            pygame.draw.circle(scr, (0, 255, 0), (scr_width-250+p_x, -p_y), 3)

    pygame.display.update()

pygame.quit()
