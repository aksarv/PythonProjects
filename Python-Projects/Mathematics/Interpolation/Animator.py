"""
An animator that uses Lagrange and Bezier to animate a red circle
"""

import numpy as np
import pygame
import time
import matplotlib.pyplot as plt

def lagrange(x_points, y_points):
    final_formula = []
    for i, yp in enumerate(y_points):
        factor = yp / float(np.prod([x_points[i]-x_points[j] for j in range(len(x_points)) if j != i]))
        final_formula.append([factor, [-x_points[j] for j in range(len(x_points)) if j != i]])
    return final_formula

def get_point(x1, y1, x2, y2, t):
    delta_y = y2-y1
    delta_x = x2-x1
    return [x1 + delta_x * t, y1 + delta_y * t]

def bezier(cx, cy, num_samples):
    # Quadratic
    if len(cx) == 3:
        points = []
        for t in np.linspace(0, 1, num_samples):
            t = float(t)
            point_1 = get_point(cx[0], cy[0], cx[1], cy[1], t)
            point_2 = get_point(cx[1], cy[1], cx[2], cy[2], t)
            point_3 = get_point(point_1[0], point_1[1], point_2[0], point_2[1], t)
            points.append(point_3)
        return points
    # Cubic
    elif len(cx) == 4:
        points = []
        for t in np.linspace(0, 1, num_samples):
            t = float(t)
            points_1 = []
            for l in range(0, len(cx)-1):
                points_1.append(get_point(cx[l], cy[l], cx[l+1], cy[l+1], t))
            points_1_x = [m[0] for m in points_1]
            points_1_y = [m[1] for m in points_1]
            points_2 = []
            for n in range(0, len(points_1_x)-1):
                points_2.append(get_point(points_1_x[n], points_1_y[n], points_1_x[n+1], points_1_y[n+1], t))
            point_2_1, point_2_2 = points_2
            point_3 = get_point(point_2_1[0], point_2_1[1], point_2_2[0], point_2_2[1], t)
            points.append(point_3)
        return points
    
pygame.init()

scr_width, scr_height = 720, 480
scr = pygame.display.set_mode((scr_width, scr_height))

selected_lagrange = None
selected_quadratic = None
cubic_start_next = False
quadratic_start_next = False
lagrange_start_next = False

cubic_clicks = []
quadratic_clicks = []
lagrange_clicks = []

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if selected_lagrange is None:
                    if mouse_x < scr_width // 2:
                        selected_lagrange = True
                    else:
                        selected_lagrange = False
                elif selected_lagrange == False:
                    if selected_quadratic is None:
                        if mouse_x < scr_width // 2:
                            selected_quadratic = True
                        else:
                            selected_quadratic = False
                    elif selected_quadratic == False:
                        if len(cubic_clicks) < 4:
                            cubic_clicks.append([mouse_x, mouse_y])
                        else:
                            cubic_start_next = True
                    else:
                        if len(quadratic_clicks) < 3:
                            quadratic_clicks.append([mouse_x, mouse_y])
                        else:
                            quadratic_start_next = True
                else:
                    lagrange_clicks.append([mouse_x, mouse_y])
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and selected_lagrange == True:
                lagrange_start_next = True

    scr.fill((0, 0, 0))

    if selected_lagrange is None:
        pygame.draw.rect(scr, (255, 0, 0), [0, 0, scr_width // 2, scr_height])
        pygame.draw.rect(scr, (0, 0, 255), [scr_width // 2, 0, scr_width // 2, scr_height])
        font = pygame.font.Font("/Users/akshith/Library/Fonts/Montserrat-ExtraBoldItalic.ttf", 40)
        text = font.render("Lagrange", True, (255, 255, 255))
        text_rect = text.get_rect(center=(scr_width // 4, scr_height // 2))
        scr.blit(text, text_rect)
        text1 = font.render("Bezier", True, (255, 255, 255))
        text_rect1 = text1.get_rect(center=(scr_width // 4 * 3, scr_height // 2))
        scr.blit(text1, text_rect1)
    elif selected_lagrange == False:
        if selected_quadratic is None:
            pygame.draw.rect(scr, (255, 0, 0), [0, 0, scr_width // 2, scr_height])
            pygame.draw.rect(scr, (0, 0, 255), [scr_width // 2, 0, scr_width // 2, scr_height])
            font = pygame.font.Font("/Users/akshith/Library/Fonts/Montserrat-ExtraBoldItalic.ttf", 40)
            text = font.render("Quadratic", True, (255, 255, 255))
            text_rect = text.get_rect(center=(scr_width // 4, scr_height // 2))
            scr.blit(text, text_rect)
            text1 = font.render("Cubic", True, (255, 255, 255))
            text_rect1 = text1.get_rect(center=(scr_width // 4 * 3, scr_height // 2))
            scr.blit(text1, text_rect1)
        elif selected_quadratic == False:
            if not cubic_start_next:
                for pos_x, pos_y in cubic_clicks:
                    pygame.draw.circle(scr, (255, 255, 255), (pos_x, pos_y), 20)
            else:
                cubic_clicks_1 = [[p, -q] for p, q in cubic_clicks]
                cubic_clicks_1_x = [cubic_click[0] for cubic_click in cubic_clicks_1]
                cubic_clicks_1_y = [cubic_click[1] for cubic_click in cubic_clicks_1]
                bezier_points = bezier(cubic_clicks_1_x, cubic_clicks_1_y, 100)
                bezier_points_1 = [[p, -q] for p, q in bezier_points]

                pos_in_points = 0

                clock = pygame.time.Clock()

                run1 = True
                while run1:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                    
                    scr.fill((0, 0, 0))

                    """for pos_x, pos_y in cubic_clicks:
                        pygame.draw.circle(scr, (255, 255, 255), (pos_x, pos_y), 5)"""

                    curr_pos_x, curr_pos_y = bezier_points_1[pos_in_points]
                    pygame.draw.circle(scr, (255, 0, 0), (curr_pos_x, curr_pos_y), 20)

                    pos_in_points += 1
                    if pos_in_points >= len(bezier_points_1):
                        time.sleep(10)
                        pygame.quit()
                        quit()

                    pygame.display.update()
                    clock.tick(60)
        else:
            if not quadratic_start_next:
                for pos_x, pos_y in quadratic_clicks:
                    pygame.draw.circle(scr, (255, 255, 255), (pos_x, pos_y), 20)
            else:
                quadratic_clicks_1 = [[p, -q] for p, q in quadratic_clicks]
                quadratic_clicks_1_x = [quadratic_click[0] for quadratic_click in quadratic_clicks_1]
                quadratic_clicks_1_y = [quadratic_click[1] for quadratic_click in quadratic_clicks_1]
                bezier_points = bezier(quadratic_clicks_1_x, quadratic_clicks_1_y, 100)
                bezier_points_1 = [[p, -q] for p, q in bezier_points]

                pos_in_points = 0

                clock = pygame.time.Clock()

                run1 = True
                while run1:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                    
                    scr.fill((0, 0, 0))

                    """for pos_x, pos_y in cubic_clicks:
                        pygame.draw.circle(scr, (255, 255, 255), (pos_x, pos_y), 5)"""

                    curr_pos_x, curr_pos_y = bezier_points_1[pos_in_points]
                    pygame.draw.circle(scr, (255, 0, 0), (curr_pos_x, curr_pos_y), 20)

                    pos_in_points += 1
                    if pos_in_points >= len(bezier_points_1):
                        time.sleep(10)
                        pygame.quit()
                        quit()

                    pygame.display.update()
                    clock.tick(60)
    else:
        if not lagrange_start_next:
            for pos_x, pos_y in lagrange_clicks:
                pygame.draw.circle(scr, (255, 255, 255), (pos_x, pos_y), 20)
        else:
            x_points = [point[0] for point in lagrange_clicks]
            y_points = [-point[1] for point in lagrange_clicks]
            lagrange_function = lagrange(x_points, y_points)
            transformed_points = []
            for t in np.linspace(min(x_points), max(x_points), 100):
                t = float(t)
                lagrange_sum = 0
                for exp in lagrange_function:
                    coefficient, bracket_terms = exp
                    prod = coefficient
                    for b in bracket_terms:
                        prod *= (t+b)
                    lagrange_sum += prod
                transformed_points.append([t, -lagrange_sum])
                
            pos_in_points = 0

            clock = pygame.time.Clock()

            run1 = True
            while run1:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                
                scr.fill((0, 0, 0))

                """for pos_x, pos_y in cubic_clicks:
                    pygame.draw.circle(scr, (255, 255, 255), (pos_x, pos_y), 5)"""

                curr_pos_x, curr_pos_y = transformed_points[pos_in_points]
                pygame.draw.circle(scr, (255, 0, 0), (curr_pos_x, curr_pos_y), 20)

                pos_in_points += 1
                if pos_in_points >= len(transformed_points):
                    time.sleep(10)
                    pygame.quit()
                    quit()

                pygame.display.update()
                clock.tick(60)

    pygame.display.update()

pygame.quit()
