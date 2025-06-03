import pygame, numpy as np, math, seconds_to_ywdhms

pygame.init()

scr_width, scr_height = 720, 480
scr = pygame.display.set_mode((scr_width, scr_height))

G = 6.674e-11

t = 0
dt = 10000

m1 = 1000
m2 = 5
x1 = scr_width // 2
y1 = scr_height // 2
x2 = scr_width // 4
y2 = scr_height // 4
v2x, v2y = 0.00002, 0
v1x, v1y = 0, 0

last_100_positions = []

clock = pygame.time.Clock()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    scr.fill((0, 0, 0))

    scr.blit(pygame.font.Font("/Users/akshith/Library/Fonts/Montserrat-ExtraBoldItalic.ttf", 20).render(seconds_to_ywdhms.seconds_to_ywdhms(t), True, (255, 255, 255)), (25, 25))

    r = math.sqrt((y2-y1)**2+(x2-x1)**2)
    fx = -((G*m1*m2)/(r**3))*(x2-x1)
    fy = -((G*m1*m2)/(r**3))*(y2-y1)
    # Newton's 2nd Law
    a2x = fx/m2
    a2y = fy/m2
    a1x = -fx/m1
    a1y = -fy/m1
    v2x += a2x * dt
    v2y += a2y * dt
    v1x += a1x * dt
    v1y += a1y * dt
    x2 += v2x * dt
    x1 += v1x * dt
    y2 += v2y * dt
    y1 += v1y * dt

    pygame.draw.circle(scr, (255, 0, 0), (x1, y1), 81)
    pygame.draw.circle(scr, (0, 0, 255), (x2, y2), 10)

    if len(last_100_positions) < 1000:
        last_100_positions.append([x2, y2])
    else:
        last_100_positions.append([x2, y2])
        del last_100_positions[0]

    for i in range(len(last_100_positions) - 1):
        pygame.draw.line(scr, (255, 255, 255), (last_100_positions[i][0], last_100_positions[i][1]), (last_100_positions[i+1][0], last_100_positions[i+1][1]))

    t += dt

    pygame.display.update()

pygame.quit()
