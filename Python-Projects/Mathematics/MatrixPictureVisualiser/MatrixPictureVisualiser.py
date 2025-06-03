import numpy as np
import math
import cv2
import pygame
import time

image_data = cv2.imread("ENTERPICTUREFILENAMEHERE.png")
image_data = cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB)
image_height, image_width = image_data.shape[:2]

class Point:
    def __init__(self, x, y, rgb):
        self.x = x
        self.y = y
        self.rgb = rgb

    @staticmethod
    def shear(point, factor, with_y_axis=False):
        transform = np.array([[1, factor], [0, 1]]) if not with_y_axis else np.array([[1, 0], [factor, 1]])
        return transform @ point

    @staticmethod
    def enlarge(point, factor, with_y=False):
        transform = np.array([[factor, 0], [0, 1]]) if not with_y else np.array([[1, 0], [0, factor]])
        return transform @ point

    @staticmethod
    def reflect_in_x(point):
        return np.array([[-1, 0], [0, 1]]) @ point

    @staticmethod
    def reflect_in_y(point):
        return np.array([[1, 0], [0, -1]]) @ point

    @staticmethod
    def rotate(point, angle, radians=True, acw=True):
        angle = math.radians(angle) if not radians else angle
        angle = 2 * math.pi - angle if not acw else angle
        return np.array([[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]]) @ point

    @staticmethod
    def apply_matrix(point, transform):
        return transform @ point
    
points = []

for row in range(0, image_height):
    for col in range(0, image_width):
        colour = image_data[row][col]
        new_x, new_y = col, image_height - row
        point_array = np.array([new_x, new_y])

        # Apply your transformation here
        new_x, new_y = Point.apply_matrix(point_array, np.array([[1, 3], [2, 4]]))
        
        points.append(Point(new_x, -new_y, colour))
    
pygame.init()

scr_width, scr_height = 720, 720
scr = pygame.display.set_mode((scr_width, scr_height))

scroll_sensitivity = 0.2

pixels_per_unit = 1
x_offset = 0
y_offset = 0

previous_x = None
previous_y = None

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                pixels_per_unit += 0.1
                delta_x = mouse_x - (scr_width // 2 + x_offset)
                delta_y = mouse_y - (scr_width // 2 + y_offset)
                x_offset += delta_x * scroll_sensitivity
                y_offset += delta_y * scroll_sensitivity
            elif event.y < 0:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                pixels_per_unit -= 0.1
                delta_x = mouse_x - (scr_width // 2 + x_offset)
                delta_y = mouse_y - (scr_width // 2 + y_offset)
                x_offset -= delta_x * scroll_sensitivity
                y_offset -= delta_y * scroll_sensitivity
        if event.type == pygame.MOUSEBUTTONUP:
            previous_x, previous_y = None, None

    scr.fill((0, 0, 0))

    mouse = pygame.mouse.get_pressed()
    if mouse[0]:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if previous_x == previous_y == None:
            previous_x, previous_y = mouse_x, mouse_y
        x_offset += mouse_x - previous_x
        y_offset += mouse_y - previous_y
        previous_x, previous_y = mouse_x, mouse_y

    pygame.draw.line(scr, (255, 255, 255), (scr_width // 2 + x_offset, 0), (scr_width // 2 + x_offset, scr_height))
    pygame.draw.line(scr, (255, 255, 255), (0, scr_height // 2 + y_offset), (scr_width, scr_height // 2 + y_offset))

    for point in points:
        x, y, rgb = point.x, point.y, point.rgb
        pygame.draw.rect(scr, tuple(rgb), [scr_width // 2 + x_offset + x * pixels_per_unit, scr_width // 2 + y_offset + y * pixels_per_unit, max(pixels_per_unit, 1), max(pixels_per_unit, 1)])

    pygame.draw.circle(scr, (255, 0, 0), (scr_width // 2 + x_offset, scr_height // 2 + y_offset), 3)

    pygame.display.update()
