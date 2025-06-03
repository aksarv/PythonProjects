"""
Draws a fascinating fractal pattern derived from the x-position of a bouncing ball in a circle after a set period of time
"""

import pygame, time, math, colorsys

pygame.init()

scr_width, scr_height = 480, 360
scr = pygame.display.set_mode((scr_width, scr_height))

GRAVITY = 1000000

class Ball:
    def __init__(self, x, y, x_vel, y_vel):
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel

def convert_colour(hue):
    r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
    return tuple([int(r * 255), int(g * 255), int(b * 255)])

starting_y = 0

starting_x = 0
while math.sqrt((starting_x - scr_width // 2) ** 2 + (starting_y - (scr_height // 2 - 200)) ** 2) >= scr_height // 2:
    starting_x += 2

ball = Ball(starting_x, starting_y, 0, 0)

clock = pygame.time.Clock()

prev_time = time.time()

inside = True

points = [[ball.x, ball.y]]

rects = []

elapsed = time.time()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    current_time = time.time()
    dt = current_time - prev_time
    prev_time = current_time

    scr.fill((0, 0, 0))

    pygame.draw.circle(scr, (255, 255, 255), (scr_width // 2, scr_height // 2 - 200), scr_height // 2, 5)

    ball.y += ball.y_vel * dt
    ball.x += ball.x_vel * dt

    ball.y_vel += GRAVITY * dt

    points.append([ball.x, ball.y])

    for i in range(len(points) - 1):
        point_1 = points[i]
        point_2 = points[i + 1]
        pygame.draw.line(scr, (255, 0, 0), tuple(point_1), tuple(point_2))

    distance_to_center = math.sqrt((ball.y - (scr_height // 2 - 200)) ** 2 + (ball.x - scr_width // 2) ** 2)
    if distance_to_center >= scr_height // 2 and inside:
        inside = False

    if not inside:
        delta_x = ball.x - scr_width // 2
        delta_y = ball.y - (scr_height // 2 - 200)
        ratio = (scr_height // 2) / distance_to_center
        delta_x *= ratio
        delta_y *= ratio

        ball.x = scr_width // 2 + delta_x
        ball.y = (scr_height // 2 - 200) + delta_y

        ball_pos = pygame.Vector2(ball.x, ball.y)
        centre_pos = pygame.Vector2(scr_width // 2, (scr_height // 2 - 200))
        normal = (ball_pos - centre_pos) / (ball_pos - centre_pos).length()

        ball_vel = pygame.Vector2(ball.x_vel, ball.y_vel)

        new_ball_vel = ball_vel - 2 * ball_vel.dot(normal) * normal

        ball.x_vel, ball.y_vel = new_ball_vel.x, new_ball_vel.y

        inside = True

    pygame.draw.circle(scr, (255, 255, 255), (ball.x, ball.y), 5, 1)

    scr.blit(pygame.font.SysFont(None, 20).render("Starting X: " + str(starting_x), True, (255, 255, 255)), (20, 20))
    scr.blit(pygame.font.SysFont(None, 20).render("Starting Y: " + str(starting_y), True, (255, 255, 255)), (20, 35))

    for rect_colour in rects:
        colour, rect = rect_colour
        pygame.draw.rect(scr, colour, rect)

    if time.time() - elapsed >= 0.1:
        elapsed = time.time()

        r = (ball.x - (scr_width // 2 - scr_height // 2)) / ((scr_width // 2 + scr_height // 2) - (scr_width // 2 - scr_height // 2))
        rects.append([convert_colour(r), pygame.Rect(starting_x - 1, starting_y - 1, 2, 2)])

        starting_x += 2
        ball.x = starting_x
        ball.y = starting_y
        ball.x_vel = 0
        ball.y_vel = 0
        points = []

        if math.sqrt((starting_x - scr_width // 2) ** 2 + (starting_y - (scr_height // 2 - 200)) ** 2) >= scr_height // 2:
            starting_y += 2
            if starting_y > scr_height - 200:
                run = False
            starting_x = 0
            while math.sqrt((starting_x - scr_width // 2) ** 2 + (starting_y - (scr_height // 2 - 200)) ** 2) >= scr_height // 2:
                starting_x += 2

    pygame.display.update()
    # clock.tick(60)

pygame.quit()
