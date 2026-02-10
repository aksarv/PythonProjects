# Not complete, just trying implementing optimisation for N Body Sim using Barnes Hut

import pygame
from random import uniform, gauss
from math import cos, sin, pi, hypot
from time import time
from dumper import dump

pygame.init()

MAX_DEPTH = 20
THRESHOLD = 0.1


def next(a, b):
    t = abs(gauss(0, 0.6))
    while t > 1:
        t = abs(gauss(0, 0.6))
    t = 1 - t
    return (b - a) * t + a


class Planet:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass
        self.x_vel = 0
        self.y_vel = 0


class Node:
    def __init__(self, tl, br):
        self.tl = tl
        self.br = br
        self.planets = []
        self.children = []

    def centre_of_mass(self):
        c_x, c_y = 0, 0
        for planet in self.planets:
            c_x += planet.mass * planet.x
            c_y += planet.mass * planet.y
        c_x, c_y = 1 / len(self.planets) * c_x, 1 / len(self.planets) * c_y
        return c_x, c_y

    def total_mass(self):
        return sum(p.mass for p in self.planets)


def construct(curr, depth=0):
    if len(curr.planets) == 0 or len(curr.planets) == 1 or depth >= MAX_DEPTH:
        return
    tl_x, tl_y = curr.tl
    br_x, br_y = curr.br
    curr.children = [Node((tl_x, tl_y), (tl_x + (br_x - tl_x) / 2, tl_y + (br_y - tl_y) / 2)),
                     Node((tl_x + (br_x - tl_x) / 2, tl_y), (br_x, tl_y + (br_y - tl_y) / 2)),
                     Node((tl_x, tl_y + (br_y - tl_y) / 2), (tl_x + (br_x - tl_x) / 2, br_y)),
                     Node((tl_x + (br_x - tl_x) / 2, tl_y + (br_y - tl_y) / 2), (br_x, br_y))]
    for planet in curr.planets:
        p_x, p_y = planet.x, planet.y
        for square in curr.children:
            tl_x, tl_y = square.tl
            br_x, br_y = square.br
            if tl_x <= p_x <= br_x and tl_y <= p_y <= br_y:
                square.planets.append(planet)
                break
    for child in curr.children:
        construct(child, depth=depth + 1)


scr_width, scr_height = 1280, 720
scr = pygame.display.set_mode((scr_width, scr_height))

planets = []
for _ in range(200):
    # Prevent favouring generating planets near the centre
    r = next(0, 300)
    t = uniform(0, 2 * pi)
    planets.append(Planet(r * cos(t) + 350, r * sin(t) + 350, uniform(10, 100)))

for _ in range(100):
    # Prevent favouring generating planets near the centre
    r = next(0, 200)
    t = uniform(0, 2 * pi)
    planets.append(Planet(r * cos(t) + scr_width - 250, r * sin(t) + scr_height - 250, uniform(10, 100)))


def build_new_tree():
    tree = Node((0, 0), (scr_width, scr_height))
    tree.planets = planets
    construct(tree)
    return tree


NET_FORCE_X = 0
NET_FORCE_Y = 0


def get_net_force(planet, curr):
    global NET_FORCE_X, NET_FORCE_Y
    centre_x, centre_y = curr.centre_of_mass()
    total_mass = curr.total_mass()
    region_width = curr.br[0] - curr.tl[0]
    dist = hypot(planet.x - centre_x, planet.y - centre_y)
    ratio = region_width / dist
    vec_norm = ((centre_x - planet.x) / dist, (centre_y - planet.y) / dist)
    if ratio < THRESHOLD or len(curr.planets) == 0 or len(curr.planets) == 1:
        NET_FORCE_X += total_mass / (dist ** 2) * vec_norm[0]
        NET_FORCE_Y += total_mass / (dist ** 2) * vec_norm[1]
        return
    for child in curr.children:
        get_net_force(planet, child)


start = time()
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    scr.fill((0, 0, 0))

    tree = build_new_tree()
    end = time()
    dt = end - start
    start = time()
    for planet in planets:
        pygame.draw.circle(scr, (255, 255, 255), (planet.x, planet.y), planet.mass / 10)
        get_net_force(planet, tree)
        quit()
        f_x, f_y = NET_FORCE_X * 1000, NET_FORCE_Y * 1000
        planet.x_vel += f_x / planet.mass
        planet.y_vel += f_y / planet.mass
        planet.x += planet.x_vel
        planet.y += planet.y_vel
        NET_FORCE_X, NET_FORCE_Y = 0, 0

    pygame.display.update()

pygame.quit()
