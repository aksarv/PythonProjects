import pygame
import math
import copy

pygame.init()

scr_width = 720
scr_height = 450
scr = pygame.display.set_mode((scr_width, scr_height))
pygame.display.set_caption('Kinematics')

class Circle:
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width

# For testing purposes
def average(lst):
    if len(lst) == 0:
        return 0
    return sum(lst) / len(lst)

def within_range(value1, value2, percentage):
    if value2 - value2 * (percentage / 100) <= value1 <= value2 + value2 * (percentage / 100):
        return True
    return False

circle = Circle(scr_width//2, scr_height//2, 30)

clock = pygame.time.Clock()

move_circle = False

how_many_values = 100

fps = 60

last_8_displacement_values = []
last_8_velocity_values = []

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            move_circle = False

    scr.fill((0, 0, 0))

    mouse_x, mouse_y = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0] and math.sqrt((mouse_x - circle.x)**2 + (mouse_y - circle.y)**2) <= circle.width:
        move_circle = True

    old_circle_x = copy.copy(circle.x)
    old_circle_y = copy.copy(circle.y)
    
    if move_circle:
        circle.x = mouse_x
        circle.y = mouse_y

    displacement = math.sqrt((circle.x - old_circle_x)**2 + (circle.y - old_circle_y)**2)
    delta_time = clock.tick(fps) / 1000
    expected_delta_time = 1 / fps

    if within_range(delta_time, expected_delta_time, 5):
        if len(last_8_displacement_values) < how_many_values + 1:
            last_8_displacement_values.append(displacement)
            if len(last_8_displacement_values) >= 2:
                first_velocity = last_8_displacement_values[-1]
                second_velocity = last_8_displacement_values[-2]
                last_8_velocity_values.append((first_velocity - second_velocity) / delta_time)
            else:
                last_8_velocity_values.append(0)
        else:
            last_8_displacement_values.append(displacement)
            last_8_displacement_values.pop(0)
            if len(last_8_displacement_values) >= 2:
                first_velocity = last_8_displacement_values[-1]
                second_velocity = last_8_displacement_values[-2]
                last_8_velocity_values.append((first_velocity - second_velocity) / delta_time)
                last_8_velocity_values.pop(0)
            else:
                last_8_velocity_values.append(0)

    pygame.draw.circle(scr, (255, 255, 255), (circle.x, circle.y), circle.width)  

    start_disp_x = (4/5) * scr_width
    start_disp_y = (1/5) * scr_height
    disp_width = (1/5) * scr_width
    disp_height = (1/5) * scr_height

    disp_points = []
    accel_points = []
    
    for i, disp_val in enumerate(last_8_displacement_values):
        disp_points.append([start_disp_x + ((i+1) / how_many_values) * disp_width, disp_height - (start_disp_y + (disp_val / 75) * disp_height) + disp_height])
        accel_points.append([start_disp_x + ((i+1) / how_many_values) * disp_width, disp_height - (start_disp_y + (last_8_velocity_values[i] / 10000) * disp_height) + disp_height])

    for i in range(len(disp_points)-1):
        current_point_x, current_point_y = disp_points[i]
        next_point_x, next_point_y = disp_points[i+1]
        current_point_x_1, current_point_y_1 = accel_points[i]
        next_point_x_1, next_point_y_1 = accel_points[i+1]
        pygame.draw.line(scr, (255, 255, 0), (current_point_x, current_point_y), (next_point_x, next_point_y), 2)
        pygame.draw.line(scr, (0, 255, 0), (current_point_x_1, current_point_y_1), (next_point_x_1, next_point_y_1), 2)
    
    pygame.draw.line(scr, (255, 255, 255), (start_disp_x, 0), (start_disp_x, disp_height), 2)
    pygame.draw.line(scr, (255, 255, 255), (start_disp_x, disp_height+2), (scr_width, disp_height+2), 2)
    
    scr.blit(pygame.font.SysFont('Arial', 15).render("Yellow is velocity", True, (255, 255, 0)), (start_disp_x, disp_height + 20))
    scr.blit(pygame.font.SysFont('Arial', 15).render("Green is acceleration", True, (0, 255, 0)), (start_disp_x, disp_height + 45))
    scr.blit(pygame.font.SysFont('Arial', 15).render("Axes not to scale", True, (255, 255, 255)), (start_disp_x, disp_height + 70))
    scr.blit(pygame.font.SysFont('Arial', 15).render("Drag the circle with your mouse.", True, (255, 255, 255)), (20, 20))

    pygame.display.update()
    clock.tick(fps)


pygame.quit()
