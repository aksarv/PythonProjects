import pygame
import math
import copy

pygame.init()
scr=pygame.display.set_mode((500,500))

def fractal(angle,init_branch_length,reduction_factor,max_depth,x=250,y=500,path=[]):
    if len(path)>max_depth:
        raise BaseException
    branch_length=init_branch_length*reduction_factor**len(path)
    final_angle=90
    for p in path:
        if p=='L':
            final_angle+=angle
        elif p=='R':
            final_angle-=angle
    left_angle=final_angle+angle
    right_angle=final_angle-angle
    x_step_left=math.cos(math.radians(left_angle))*branch_length
    y_step_left=math.sin(math.radians(left_angle))*branch_length
    x_step_right=math.cos(math.radians(right_angle))*branch_length
    y_step_right=math.sin(math.radians(right_angle))*branch_length
    pygame.draw.line(scr,(255,255,255),(x,y),(x+x_step_left,y-y_step_left),max_depth-len(path))
    pygame.draw.line(scr,(255,255,255),(x,y),(x+x_step_right,y-y_step_right),max_depth-len(path))
    copy_path_left=copy.deepcopy(path)
    copy_path_left.append('L')
    copy_path_right=copy.deepcopy(path)
    copy_path_right.append('R')
    try:
        fractal(angle,init_branch_length,reduction_factor,max_depth,x=x+x_step_left,y=y-y_step_left,path=copy_path_left)
        fractal(angle,init_branch_length,reduction_factor,max_depth,x=x+x_step_right,y=y-y_step_right,path=copy_path_right)
    except BaseException:
        return

angle=25
init_branch_length=100
reduction_factor=0.7
max_depth=10

run=True
while run:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    scr.fill((0,0,0))
    mouse_x,mouse_y=pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0]:
        if 400<=mouse_x<=500 and 0<=mouse_y<=10:
            angle=(mouse_x-400)/100*90
        if 400<=mouse_x<=500 and 15<=mouse_y<=25:
            init_branch_length=(mouse_x-400)/100*250
        if 400<=mouse_x<=500 and 30<=mouse_y<=40:
            reduction_factor=(mouse_x-400)/100
        if 400<=mouse_x<=500 and 45<=mouse_y<=55:
            max_depth=int((mouse_x-400)/100*20)
    fractal(angle,init_branch_length,reduction_factor,max_depth)
    pygame.draw.rect(scr,(255,255,255),[400,0,100,10],2)
    pygame.draw.rect(scr,(255,255,255),[400,15,100,10],2)
    pygame.draw.rect(scr,(255,255,255),[400,30,100,10],2)
    pygame.draw.rect(scr,(255,255,255),[400,45,100,10],2)
    pygame.draw.circle(scr,(255,0,0),(angle/90*100+400,5),5)
    pygame.draw.circle(scr,(255,0,0),(init_branch_length/250*100+400,20),5)
    pygame.draw.circle(scr,(255,0,0),(reduction_factor*100+400,35),5)
    pygame.draw.circle(scr,(255,0,0),(max_depth/20*100+400,50),5)
    scr.blit(pygame.font.SysFont(None,15).render('angle',True,(255,255,255)),(368,0))
    scr.blit(pygame.font.SysFont(None,15).render('init_branch_length',True,(255,255,255)),(302,15))
    scr.blit(pygame.font.SysFont(None,15).render('reduction_factor',True,(255,255,255)),(314,30))
    scr.blit(pygame.font.SysFont(None,15).render('max_depth',True,(255,255,255)),(340,45))
    pygame.display.update()
pygame.quit()
