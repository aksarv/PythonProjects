import cv2
import numpy as np
import pygame
import time
import random
import math

scr=pygame.display.set_mode((1000,1000))

with open('colour_data.txt','r') as file:
    data=[eval(line.strip()) for line in file.readlines()]
    rgbs=[item[0] for item in data]
    names=[item[1] for item in data]

def closest(colour):
    return names[sorted(enumerate([abs(colour[0]-x[0])+abs(colour[1]-x[1])+abs(colour[2]-x[2]) for x in rgbs]),key=lambda y:y[1])[0][0]]

is_random=input('Random faces or closest faces? Enter "y" for random and anything else for closest: ')=='y'

image=cv2.imread('Test1.jpeg')

setused=set()
for i,row in enumerate(image):
    for j,col in enumerate(row):       
        if f"{i} {j}" not in setused:
            k=0
            try:
                while image[i+k][j:j+k+1].size != 0 and np.array([l[j+k] for l in image[i:i+k+1]]).size != 0 and f"{i+k} {j+k}" not in setused and f"{i+k} {j}" not in setused and f"{i} {j+k}" not in setused and k<30:
                    if abs(sum([sum(m)/3 for m in np.vstack([image[i+k][j:j+k+1],np.array([l[j+k] for l in image[i:i+k+1]])])])/len([sum(m)/3 for m in np.vstack([image[i+k][j:j+k+1],np.array([l[j+k] for l in image[i:i+k+1]])])])-sum(col)/3)>10:
                        break
                    else:
                        k+=1
            except IndexError:
                pass
            img=pygame.image.load(closest(list(col))+'.png') if not is_random else pygame.image.load(random.choice(['Auto','Demon','Easy','EasyDemon','ExtremeDemon','Hard','Harder','Insane','InsaneDemon','MediumDemon','Normal','Unrated'])+'.png')
            scr.blit(pygame.transform.scale(img,(k,k)),(j,i))
            pygame.display.update()
            for n in range(i,i+k+1):
                for o in range(j,j+k+1):
                    if math.sqrt(((j+k/2)-(o))**2+((i+k/2)-(n))**2)<(k/2):
                        if f"{n} {o}" not in setused:
                            setused.add(f"{n} {o}")
    print(str(round(i/len(image)*100,1))+'%')

pygame.image.save(scr,f'{time.time()}.png')
