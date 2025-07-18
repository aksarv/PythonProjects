import pygame
import math

pygame.init()
scr = pygame.display.set_mode((500, 500))


def fractal(
    init_triangle_length, max_depth, x=250, y=0, inverted=False, current_depth=0
):
    if current_depth == 0:
        x_step = init_triangle_length / 2
        y_step = math.sqrt(3 * x_step**2)
        pygame.draw.line(scr, (255, 255, 255), (x, y), (x + x_step, y + y_step), 1)
        pygame.draw.line(
            scr,
            (255, 255, 255),
            (x + x_step, y + y_step),
            (x + x_step - init_triangle_length, y + y_step),
            1,
        )
        pygame.draw.line(
            scr,
            (255, 255, 255),
            (x + x_step - init_triangle_length, y + y_step),
            (x, y),
            1,
        )
    if current_depth > max_depth:
        raise BaseException
    if not inverted:
        triangle_length = init_triangle_length / 2**current_depth
        x_step_half = triangle_length / 4
        y_step_half = math.sqrt(12 * x_step_half**2) / 2
        pygame.draw.line(
            scr,
            (255, 255, 255),
            (x + x_step_half, y + y_step_half),
            (x - x_step_half, y + y_step_half),
            1,
        )
        pygame.draw.line(
            scr,
            (255, 255, 255),
            (x - x_step_half, y + y_step_half),
            (x, y + y_step_half * 2),
            1,
        )
        pygame.draw.line(
            scr,
            (255, 255, 255),
            (x, y + y_step_half * 2),
            (x + x_step_half, y + y_step_half),
            1,
        )
        try:
            fractal(
                init_triangle_length,
                max_depth,
                x=x,
                y=y,
                inverted=False,
                current_depth=current_depth + 1,
            )
            fractal(
                init_triangle_length,
                max_depth,
                x=x + x_step_half,
                y=y + y_step_half,
                inverted=False,
                current_depth=current_depth + 1,
            )
            fractal(
                init_triangle_length,
                max_depth,
                x=x - x_step_half,
                y=y + y_step_half,
                inverted=False,
                current_depth=current_depth + 1,
            )
        except BaseException:
            return
    """else:
        triangle_length=init_triangle_length/2**current_depth
        x_step_half=triangle_length/4
        y_step_half=math.sqrt(12*x_step_half**2)/2
        pygame.draw.line(scr,(255,255,255),(x+x_step_half*2,y),(x+x_step_half,y+y_step_half),5)
        pygame.draw.line(scr,(255,255,255),(x+x_step_half,y+y_step_half),(x+x_step_half*3,y+y_step_half),5)
        pygame.draw.line(scr,(255,255,255),(x+x_step_half*3,y+y_step_half),(x+x_step_half*2,y),5)"""


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    scr.fill((0, 0, 0))
    fractal(300, 10)
    pygame.display.update()
