import pygame
import math
import time
import noise

pygame.init()

pixels_per_unit = 50


class Node:
    id = 0

    def __init__(self, x, y):
        self.id = Node.id
        Node.id += 1
        self.grid_x = x
        self.grid_y = y
        self.x = x
        self.y = y
        self.x_vel = 0
        self.y_vel = 0
        self.acc_x = 0
        self.acc_y = 0


def coords(x, y):
    return 640 + x * pixels_per_unit, 360 + y * pixels_per_unit


def angle_between_points(origin, point):
    return math.degrees(math.atan2(point[1] - origin[1], point[0] - origin[0])) % 360


def wind(t):
    base = noise.pnoise1(t * 0.1)
    gust = noise.pnoise1(t * 0.5) * 0.5
    return (base + gust) * 7


N = 2
STIFFNESS = 30.0
MASS = 0.5
GRAVITY = 10.0
LOSS = 0.985
TIMEWARP = 1.5

nodes = [Node(i, j) for j in range(-N // 2, N // 2 + 1) for i in range(-N // 2, N // 2 + 1)]
nodes_dict = {}
for node in nodes:
    nodes_dict[(node.x, node.y)] = node

scr = pygame.display.set_mode((1280, 720))

prev_time = time.time()
first_time = time.time()

clock = pygame.time.Clock()

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    scr.fill((0, 0, 0))

    curr_time = time.time()
    dt = (curr_time - prev_time) * TIMEWARP
    prev_time = curr_time

    for node in nodes:
        x_coord, y_coord = coords(node.x, node.y)
        x_force = 0
        y_force = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if not (dx == 0 and dy == 0):
                    try:
                        adj_node = nodes_dict[(node.grid_x + dx, node.grid_y + dy)]
                        adj_x_coord, adj_y_coord = coords(adj_node.x, adj_node.y)
                        pygame.draw.line(scr, (255, 255, 255), (x_coord, y_coord), (adj_x_coord, adj_y_coord), 3)
                        force = (math.hypot(adj_node.x - node.x, adj_node.y - node.y) - 1) * STIFFNESS
                        angle = angle_between_points([node.x, node.y], [adj_node.x, adj_node.y])
                        x_force += force * math.cos(math.radians(angle))
                        y_force += force * math.sin(math.radians(angle))
                    except KeyError:
                        pass
        """if (node.grid_x == -N // 2 and node.grid_y == -N // 2) or (node.grid_x == N // 2 and node.grid_y == -N // 2):
            continue"""
        if node.grid_y == -N // 2:
            continue
        node.acc_x = x_force * MASS + wind(time.time() - first_time)
        node.acc_y = y_force * MASS + GRAVITY
        node.x_vel += node.acc_x * dt
        node.y_vel += node.acc_y * dt
        node.x_vel *= LOSS
        node.y_vel *= LOSS
        node.x += node.x_vel * dt
        node.y += node.y_vel * dt

    for node in nodes:
        node_x, node_y = coords(node.x, node.y)
        pygame.draw.circle(scr, (255, 0, 0), (node_x, node_y), 5)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
