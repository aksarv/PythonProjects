# Visualise distortion of mercator projection.

import pygame
import math
import numpy as np
import geopandas as gpd

# Load the shapefile or GeoJSON file
#countries = gpd.read_file("ne_10m_admin_0_countries.shp")

#print(countries)
#quit()
def convert_lat_long_to_x_y(latitude, longitude):

    mapWidth = 200    # Width of the map in pixels
    mapHeight = 200   # Height of the map in pixels

    # Convert longitude to x coordinate
    x = (longitude + 180) * (mapWidth / 360)

    # Convert latitude to radians
    latRad = latitude * math.pi / 180

    # Mercator projection formula for y
    # Mercator projection becomes undefined for latitude >= 90
    if latitude == 90:
        y = 0  # North pole should be the top of the map
    else:
        mercN = math.log(math.tan((math.pi / 4) + (latRad / 2)))
        y = (mapHeight / 2) - (mapHeight * mercN / (2 * math.pi))

    return x, y


pygame.init()

scr=pygame.display.set_mode((200,200))
pygame.display.set_caption("Mercator")

clock=pygame.time.Clock()


points=[[10*math.cos(x), 10*math.sin(x)] for x in np.linspace(0, 2*math.pi, 20)]

goDown=False

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    scr.fill((0,0,0))
    scr.blit(pygame.transform.scale(pygame.image.load("mercator.JPG"),(200,200)), (0,0))
    for i,point in enumerate(points[:-1]):
        pointX,pointY=point
        nextPointX,nextPointY=points[i+1]
        try:
            pygame.draw.line(scr, (255, 0, 0), convert_lat_long_to_x_y(pointY,pointX), convert_lat_long_to_x_y(nextPointY,nextPointX), 2)
        except ValueError:
            goDown=not goDown
        if goDown:
            points[i][1]-=0.1
        else:
            points[i][1]+=0.1
    clock.tick(60)
    pygame.display.update()

