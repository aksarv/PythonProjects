from sklearn.neighbors import KNeighborsClassifier
import os
import cv2
import pygame
import numpy
import itertools
import time

dirs = os.listdir('[PATH_TO_IMAGES]/Images')[1:]
data = []
labels = []
for x in dirs:
    for y in os.listdir('[PATH_TO_IMAGES]/Images/' + x):
        if y != '.DS_Store':
            img = cv2.imread('[PATH_TO_IMAGES]Images/' + x + '/' + y, cv2.IMREAD_GRAYSCALE).tolist()
            for z in range(64):
                for a in range(64):
                    rgb = img[z][a]
                    if rgb > 128:
                        img[z][a] = 1
                    else:
                        img[z][a] = 0
            data.append(list(itertools.chain.from_iterable(img)))
            labels.append(y.split(' ')[0])
knc = KNeighborsClassifier(n_neighbors=3)
knc.fit(data, labels)
pygame.init()
scr = pygame.display.set_mode((500, 500))
pygame.display.set_caption('Draw: Smiley, Water Glass, Bike or Umbrella (Hit P for Prediction)')
def text(size, message, colour, x, y):
    scr.blit(pygame.font.SysFont('SF Pro', size).render(message, True, colour), (x, y))
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                filename = str(time.time()) + '.png'
                pygame.image.save(scr, filename)
                drawing = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
                drawing = cv2.resize(drawing, (64, 64), interpolation = cv2.INTER_AREA)
                copy = drawing
                for b in range(64):
                    for c in range(64):
                        rgb = drawing[b][c]
                        if rgb > 128:
                            drawing[b][c] = 1
                        else:
                            drawing[b][c] = 0
                drawing = list(itertools.chain.from_iterable(drawing))
                prediction = knc.predict([drawing])[0]
                result = True
                while result:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False
                    scr.fill((0, 0, 0))
                    text(30, 'Computer predicts this is a ' + prediction + '.', (255, 255, 255), 10, 10)
                    pygame.display.update()
    if pygame.mouse.get_pressed()[0]:
        x, y = pygame.mouse.get_pos()
        pygame.draw.rect(scr, (255, 255, 255), [x, y, 31, 31])
    pygame.display.update()
pygame.quit()
