import pygame
import numpy as np


def intersection_points_sphere(line_origin, distance_vector, sphere_centre, sphere_radius):
    distance_vector = distance_vector / np.linalg.norm(distance_vector)
    a = np.dot(distance_vector, distance_vector)
    b = 2 * np.dot(line_origin - sphere_centre, distance_vector)
    c = np.dot(line_origin - sphere_centre, line_origin - sphere_centre) - sphere_radius ** 2
    discriminant = b ** 2 - 4 * a * c
    if discriminant < 0:
        return False
    elif discriminant == 0:
        t = -b / (2 * a)
        return line_origin + t * distance_vector
    t1 = (-b + np.sqrt(discriminant)) / (2 * a)
    t2 = (-b - np.sqrt(discriminant)) / (2 * a)
    point1 = line_origin + t1 * distance_vector
    point2 = line_origin + t2 * distance_vector
    if np.linalg.norm(point1 - line_origin) < np.linalg.norm(point2 - line_origin):
        return point1
    return point2


environment = [np.array([-1, 4, -1, 1, 100, 60, 0, 0]), np.array([0, 5, 0, 1, 2000, 0, 0, 60])]
camera = np.array([0, 0, 0])
light_sources = [np.array([0, 0, 1, 100])]
ambient_light = 1

# Camera grid is in the xz-plane

tl = np.array([-2, 2, 2])
tr = np.array([2, 2, 2])
bl = np.array([-2, 2, -2])
br = np.array([2, 2, -2])

resolution_x, resolution_y = 240, 240

coordinates = []

for i, x in enumerate(np.linspace(tl[2], bl[2], resolution_y)):
    for j, y in enumerate(np.linspace(tl[0], tr[0], resolution_x)):
        ray_origin = camera
        direction_without_normalisation = np.array([y, tl[1], x]) - ray_origin
        line_direction = direction_without_normalisation / np.linalg.norm(direction_without_normalisation)
        for obj in environment:
            o_x, o_y, o_z, sphere_radius, specular_exponent, red, green, blue = obj
            sphere_centre = np.array([o_x, o_y, o_z])
            ip = intersection_points_sphere(ray_origin, line_direction, sphere_centre, sphere_radius)
            if not isinstance(ip, bool):
                normal_vector = (ip - sphere_centre) / sphere_radius
                total_light = ambient_light
                for l in light_sources:
                    # Diffuse reflection
                    l_x, l_y, l_z, l_intensity = l
                    light_vector = (np.array([l_x, l_y, l_z]) - ip) / np.linalg.norm((np.array([l_x, l_y, l_z]) - ip))
                    dot_product = max(0, np.dot(normal_vector, light_vector))
                    distance_to_light = np.linalg.norm(np.array([l_x, l_y, l_z]) - ip)
                    attenuated_intensity = l_intensity / (distance_to_light ** 2)
                    total_light += attenuated_intensity * dot_product
                    # Specular reflection
                    view_vector = (camera - ip) / np.linalg.norm(camera - ip)
                    reflection_vector = 2 * normal_vector * np.dot(normal_vector, light_vector) - light_vector
                    reflection_vector = reflection_vector / np.linalg.norm(reflection_vector)
                    reflection_dot_vector = max(np.dot(reflection_vector, view_vector), 0)
                    total_light += l_intensity * pow(reflection_dot_vector, specular_exponent)
                total_light = max(total_light, 0)
                coordinates.append([j, i, red / 255, green / 255, blue / 255, total_light])

pygame.init()

scr_width, scr_height = resolution_x, resolution_y
scr = pygame.display.set_mode((scr_width, scr_height))

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    scr.fill((0, 0, 0))

    for coord_x, coord_y, red, green, blue, intensity in coordinates:
        scaled_red = int(max(0, min(255, red * intensity * 255)))
        scaled_green = int(max(0, min(255, green * intensity * 255)))
        scaled_blue = int(max(0, min(255, blue * intensity * 255)))

        pygame.draw.rect(scr, (scaled_red, scaled_green, scaled_blue), [coord_x, coord_y, 1, 1])

    pygame.display.update()
