# Demonstrating conduction through a simulation. Could extend this by adding matplotlib to see average temperature over time, through threading to prevent matplotlib from blocking pygame when showing the graph. I could also develop my own graphing library that isn't blocking, which I might do later on.

import pygame
import random
import math
import time

pygame.init()
scr_width,scr_height=1024,576
scr=pygame.display.set_mode((1024,576))

fire=pygame.transform.scale(pygame.image.load('fire.png'),(1024,576))

class Particle:
    def __init__(self,x,y,x_vel,y_vel,width):
        self.id=random.uniform(0,10000000000)
        self.x=x
        self.y=y
        self.x_vel=x_vel
        self.y_vel=y_vel
        self.gravity=0
        self.width=width
        #self.momentum=math.sqrt(self.x_vel**2+self.y_vel**2)*self.width

num_particles=200
particles=[]
for _ in range(num_particles):
    rand_angle=random.uniform(0,359.999999999)
    particles.append(Particle(random.randint(0,1024),random.randint(0,1024),math.cos(math.radians(rand_angle))*100,math.sin(math.radians(rand_angle))*100,5))
#particles=[Particle(50,50,1.7777*50,1*50,20),Particle(1024-50,576-50,-1.8*50,-1*50,20)]
#print([vars(thing) for thing in particles])
energy_lost_coefficient=0.95
right_wall_energy=1.15
start=time.time()
clock=pygame.time.Clock()
run=True
while run:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    scr.fill((255,128,128))
    scr.blit(fire,(0,0))
    end=time.time()
    delta_time=end-start
    for p in particles:
        p.x_vel=min(p.x_vel,5000)
        p.y_vel=min(p.y_vel,5000)
        p.x+=p.x_vel*delta_time
        p.y+=p.y_vel*delta_time
        p.y_vel+=p.gravity*delta_time
    for p1 in particles:
        for p2 in particles:
            if p1.id!=p2.id:
                delta_y=p2.y-p1.y   
                delta_x=p2.x-p1.x
                if math.sqrt((delta_y)**2+(delta_x)**2)<p1.width+p2.width:
                    difference=(p1.width+p2.width)-math.sqrt((delta_y)**2+(delta_x)**2)
                    difference_1=math.sqrt((delta_y)**2+(delta_x)**2)
                    ratio=difference_1/difference
                    try:
                        delta_y_1=delta_y/ratio
                        delta_x_1=delta_x/ratio
                    except ZeroDivisionError:
                        pass
                    p2.y+=delta_y_1
                    p2.x+=delta_x_1
                    new_p1_x_vel=((p1.width-p2.width)*p1.x_vel+2*p2.width*p2.x_vel)/(p1.width+p2.width)
                    new_p1_y_vel=((p1.width-p2.width)*p1.y_vel+2*p2.width*p2.y_vel)/(p1.width+p2.width)
                    new_p2_x_vel=((p2.width-p1.width)*p2.x_vel+2*p1.width*p1.x_vel)/(p1.width+p2.width)
                    new_p2_y_vel=((p2.width-p1.width)*p2.y_vel+2*p1.width*p1.y_vel)/(p1.width+p2.width)
                    p1.x_vel=new_p1_x_vel*0.999
                    p1.y_vel=new_p1_y_vel*0.999
                    p2.x_vel=new_p2_x_vel*0.999
                    p2.y_vel=new_p2_y_vel*0.999
        if p1.x<p1.width:
            p1.x+=p1.width-p1.x
            p1.x_vel*=-1
            p1.x_vel*=right_wall_energy
            p1.y_vel*=right_wall_energy
        if p1.x>scr_width-p1.width:
            p1.x-=p1.x-(scr_width-p1.width)
            p1.x_vel*=-1
        if p1.y<p1.width:
            p1.y+=p1.width-p1.y
            p1.y_vel*=-1
        if p1.y>scr_height-p1.width:
            p1.y-=p1.y-(scr_height-p1.width)
            p1.y_vel*=-1
    for p in particles:
        pygame.draw.circle(scr,(min((math.sqrt(p.x_vel**2+p.y_vel**2)-100 if math.sqrt(p.x_vel**2+p.y_vel**2)-100>0 else 0)/300*255,255),0,255-min(math.sqrt(p.x_vel**2+p.y_vel**2)/300*255,255)),(p.x,p.y),p.width)
    scr.blit(pygame.font.SysFont(None,32).render('Average Temperature: '+str(round((sum(math.sqrt(p.x_vel**2+p.y_vel**2) for p in particles)/len(particles))/100*20,2))+' °C',True,(255,255,255)),(680,30))
    start=time.time()
    pygame.display.update()
    clock.tick(240)
pygame.quit()
