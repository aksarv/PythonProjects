import cv2
import numpy as np
import pygame

img=pygame.image.load('Normal.png')

scr=pygame.display.set_mode((1000,1000))

image=cv2.imread('Normal.png')
setused=set()
for i,row in enumerate(image):
    for j,col in enumerate(row):
        #if sum(col)/3>127:
            if f"{i} {j}" not in setused:
                k=1
                try:
                    while image[i-k][j-k:j+k+1].size != 0 and image[i+k][j-k:j+k+1].size != 0 and np.array([l[j-k] for l in image[i-k+1:i+k]]).size != 0 and np.array([l[j+k] for l in image[i-k+1:i+k]]).size != 0:
                        if abs(sum([sum(m)/3 for m in np.vstack([image[i-k][j-k:j+k+1],image[i+k][j-k:j+k+1],np.array([l[j-k] for l in image[i-k+1:i+k]]),np.array([l[j+k] for l in image[i-k+1:i+k]])])])/3-sum(col)/3)>10:
                            break
                        else:
                            k+=1
                except IndexError:
                    pass
                #print(k)
                scr.blit(pygame.transform.scale(img,(k*2,k*2)),(j-k,i-k))
                pygame.display.update()
                for n in range(i-k,i+k+1):
                    for o in range(j-k,j+k+1):
                        if f"{n} {o}" not in setused:
                            setused.add(f"{n} {o}")

pygame.image.save(scr,'lobotomylolwhatevenisthislol.jpeg')
