import pygame
import copy
import time
import os
import datetime

pygame.init()

scr=pygame.display.set_mode((1000,600))
icon=pygame.transform.scale(pygame.image.load('Cube012.png'), (50,50))
spike=pygame.transform.scale(pygame.image.load('RegularSpike01.png'),(50,50))
bg=pygame.transform.scale(pygame.image.load('Background-GeometricBlue.png'),(1000,1000))
block=pygame.transform.scale(pygame.image.load('RegularBlock01.png'),(50,50))
jumppad=pygame.transform.scale(pygame.image.load('YellowJumpPad.png'),(50,8))
reversegravityportal=pygame.transform.scale(pygame.image.load('GravityPortalALabelled.png'),(50,80))
normalgravityportal=pygame.transform.scale(pygame.image.load('GravityPortalBLabelled.png'),(50,80))
jumpring=pygame.transform.scale(pygame.image.load('YellowJumpRing.png'),(50,50))
homescreen=pygame.transform.scale(pygame.image.load('HomeScreen.png'),(1000,600))
left_arrow=pygame.transform.scale(pygame.image.load('LeftArrow.png'),(71,150))
right_arrow=pygame.transform.scale(pygame.image.load('RightArrow.png'),(71,150))
clock=pygame.time.Clock()

class Cube(pygame.sprite.Sprite):
    def __init__(self,x,y,mode):
        super(Cube, self).__init__()
        self.x=x
        self.y=y
        self.x_copy=copy.deepcopy(x)
        self.y_copy=copy.deepcopy(y)
        self.camera_offset=0
        self.image=icon
        self.rot=0
        self.rect=self.image.get_rect()
        self.rect.center=(self.x+25, self.y+25)
        self.on_ground=False
        self.mode=mode
        self.reverse_gravity=False
        self.original_y_position=y
        if mode=='cube':
            self.y_vel=0
            self.gravity=0.35
            self.hitbox=pygame.Rect(x,y,50,50)
    def display(self):
        self.rect.center=(self.x+25, self.y+25)
        self.image=pygame.transform.rotozoom(icon,self.rot,1)
        self.rect=self.image.get_rect(center=self.rect.center)
        if not self.on_ground:
            if not self.reverse_gravity:
                self.rot-=3
            else:
                self.rot+=3
            self.rot%=360
    def display_hitbox(self):
        pygame.draw.rect(scr,(255,0,0),self.hitbox)
    def update(self):
        if not self.on_ground:
            self.y+=self.y_vel
            self.y_vel+=self.gravity

class Object:
    def __init__(self,x,y,obj):
        self.x=x
        self.y=y
        self.obj=obj
        if obj=='spike':
            self.hitbox=pygame.Rect(600+50*x+12.5,500-50*y+12.5,25,25)
        if obj=='block':
            self.hitbox=pygame.Rect(600+50*x,500-50*y,50,50)
        if obj=='jumppad':
            self.hitbox=pygame.Rect(600+50*x,500-50*y+30,50,20)
        if obj=='reversegravityportal':
            self.hitbox=pygame.Rect(600+50*x,500-50*y-30,50,80)
        if obj=='normalgravityportal':
            self.hitbox=pygame.Rect(600+50*x,500-50*y-30,50,80)
        if obj=='jumpring':
            self.hitbox=pygame.Rect(600+50*x,500-50*y,50,50)

class Level:
    def __init__(self,objects):
        self.objects=objects
        self.copy=copy.deepcopy(objects)
        self.attempts=1
        self.attempt_x=300
    def display(self):
        for object in self.objects:
            if object.obj=='spike':
                scr.blit(spike,(600+50*object.x,500-50*object.y))
            if object.obj=='block':
                scr.blit(block,(600+50*object.x,500-50*object.y))
            if object.obj=='jumppad':
                scr.blit(jumppad,(600+50*object.x,500-50*object.y+42))
            if object.obj=='reversegravityportal':
                scr.blit(reversegravityportal,(600+50*object.x,500-50*object.y-30))
            if object.obj=='normalgravityportal':
                scr.blit(normalgravityportal,(600+50*object.x,500-50*object.y-30))
            if object.obj=='jumpring':
                scr.blit(jumpring,(600+50*object.x,500-50*object.y))
    def move(self):
        for object in self.objects:
            object.x-=0.08
            if object.obj=='spike':
                object.hitbox=pygame.Rect(600+50*object.x+20,500-50*object.y+20,10,30)
            if object.obj=='block':
                object.hitbox=pygame.Rect(600+50*object.x,500-50*object.y,50,50)
            if object.obj=='jumppad':
                object.hitbox=pygame.Rect(600+50*object.x,500-50*object.y+30,50,20)
            if object.obj=='reversegravityportal':
                object.hitbox=pygame.Rect(600+50*object.x,500-50*object.y-30,50,80)
            if object.obj=='normalgravityportal':
                object.hitbox=pygame.Rect(600+50*object.x,500-50*object.y-30,50,80)
            if object.obj=='jumpring':
                object.hitbox=pygame.Rect(600+50*object.x,500-50*object.y,50,50)
    def reset(self):
        self.objects=self.copy
        self.copy=copy.deepcopy(self.objects)
        self.attempt_x=300
    def display_hitboxes(self):
        for object in self.objects:
            if object.obj=='spike':
                pygame.draw.rect(scr,(255,0,0),object.hitbox,3)
            else:
                pygame.draw.rect(scr,(0,0,255),object.hitbox,3)
    def display_attempts(self):
        scr.blit(pygame.font.SysFont('Pusab',32).render('Attempt '+str(self.attempts),True,(255,255,255)),(self.attempt_x,200))
        self.attempt_x-=0.08*50

class Queue:
    def __init__(self, elements):
        self.elements=elements
        self.selected_position=0

def closest(lst,n):
    return lst[sorted([[x[0],abs(n-x[1])] for x in enumerate(lst)],key=lambda l:l[1])[0][0]]

def point_inside_rectangle(x,y,width,height,point_x,point_y):
    return x<point_x<x+width and y<point_y<y+height

def run_level(level):
    cube=Cube(300,500,'cube')
    #level=Level([Object(x,-1,'block') for x in range(-20,300)])
    last_visited=[]
    path=False
    frames=0
    flag=False
    buffer_jump_ring=False
    transition_camera=False
    camera_transition_smoothness=20
    difference=0
    transition_frames=0
    run=True
    while run:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.MOUSEBUTTONDOWN:
                left_pressed,_,_=pygame.mouse.get_pressed()
                if left_pressed:
                    for object in level.objects:
                        if object.obj=='jumpring':
                            if object.hitbox.colliderect(cube.hitbox):
                                path=False
                                if not cube.reverse_gravity:
                                    cube.y_vel=-9
                                else:
                                    cube.y_vel=9
                            else:
                                if path:
                                    buffer_jump_ring=True
        scr.fill((0,0,0))
        scr.blit(bg,(0,0))
        frames+=1
        if frames%5==0:
            if len(last_visited)<5:
                last_visited.append([cube.x,cube.y])
            else:
                last_visited.append([cube.x,cube.y])
                del last_visited[0]
        if len(last_visited)>1 and path:
            for x in range(len(last_visited)-1):
                pygame.draw.line(scr,(255,255,255),(last_visited[x][0]+25,last_visited[x][1]+25),(last_visited[x+1][0]+25,last_visited[x+1][1]+25),x+1)
        for x in range(len(last_visited)):
            last_visited[x][0]-=0.08*50
        mouse=pygame.mouse.get_pressed()
        if mouse[0] and cube.on_ground:
            if not cube.reverse_gravity:
                cube.y_vel=-9
            else:
                cube.y_vel=9
            cube.on_ground=False
        keys=pygame.key.get_pressed()
        cube.display()
        #cube.display_hitboxes()
        cube.update()
        level.display()
        level.move()
        #level.display_hitboxes()
        level.display_attempts()
        for object in level.objects:
            if object.obj=='jumppad':
                if object.hitbox.colliderect(cube.hitbox):
                    if cube.reverse_gravity:
                        cube.y_vel=13
                    else:
                        cube.y_vel=-13
                    cube.on_ground=False
                    path=True
            elif object.obj=='spike':
                if object.hitbox.colliderect(cube.hitbox):
                    time.sleep(0.5)
                    level.reset()
                    frames=0
                    level.attempts+=1
            elif object.obj=='block':
                if object.hitbox.colliderect(cube.hitbox):
                    left=max(object.hitbox.left,cube.hitbox.left)
                    right=max(object.hitbox.top,cube.hitbox.top)
                    width=min(object.hitbox.right,cube.hitbox.right)-max(object.hitbox.left,cube.hitbox.left)
                    height=min(object.hitbox.bottom,cube.hitbox.bottom)-max(object.hitbox.top,cube.hitbox.top)
                    if width>height or (width<10 and height<10):
                        cube.rot=closest([0,90,180,270],cube.rot)
                        cube.on_ground=True
                        path=False
                        if cube.reverse_gravity:
                            if cube.hitbox.top>object.hitbox.top:
                                cube.y=object.hitbox.bottom 
                        else:
                            if cube.hitbox.top<object.hitbox.top:
                                cube.y=object.hitbox.top-50
                        cube.y_vel=0
                        cube.hitbox=pygame.Rect(600+50*object.x,500-50*object.y,50,50)
                    elif height>width and width>10 and height>10:
                        level.reset()
                        cube.x=cube.x_copy
                        cube.y=cube.y_copy
                        cube.reverse_gravity=False
                        frames=0
                        level.attempts+=1
            elif object.obj=='reversegravityportal':
                if object.hitbox.colliderect(cube.hitbox):
                    cube.reverse_gravity=True
            elif object.obj=='normalgravityportal':
                if object.hitbox.colliderect(cube.hitbox):
                    cube.reverse_gravity=False
            elif object.obj=='jumpring':
                if object.hitbox.colliderect(cube.hitbox):
                    if buffer_jump_ring:
                        if not cube.reverse_gravity:
                            cube.y_vel=-9
                        else:
                            cube.y_vel=9
                        buffer_jump_ring=False
        if cube.mode=='cube':
            difference=copy.deepcopy(cube.y-cube.original_y_position)
            if difference<-200 or difference>200 or cube.y>500 or cube.y<0:
                transition_camera=True
            if transition_camera:
                if transition_frames>camera_transition_smoothness:
                    transition_camera=False
                for object in level.objects:
                    object.y+=(difference/50)/camera_transition_smoothness
                cube.y-=difference/camera_transition_smoothness
                transition_frames+=1
            if cube.reverse_gravity:
                cube.gravity=-abs(cube.gravity)
            else:
                cube.gravity=abs(cube.gravity)
            cube.hitbox=pygame.Rect(cube.x,cube.y,50,50)
            if cube.on_ground:
                for object in level.objects:
                    if object.obj=='block':
                        if cube.reverse_gravity:
                            if object.hitbox.collidepoint(cube.x,cube.y-2):
                                break
                        else:
                            if object.hitbox.collidepoint(cube.x,cube.y+52):
                                break
                else:
                    cube.on_ground=False
            scr.blit(cube.image,cube.rect)
        for object in level.objects:
            if object.obj=='block':
                if object.hitbox.colliderect(cube.hitbox):
                    if cube.reverse_gravity:
                        if object.hitbox.y>cube.hitbox.y:
                            level.reset()
                            cube.x=cube.x_copy
                            cube.y=cube.y_copy
                            cube.reverse_gravity=False
                            cube.original_y_position=cube.y
                            frames=0
                            level.attempts+=1
                    else:
                        if object.hitbox.y<cube.hitbox.y:
                            level.reset()
                            cube.x=cube.x_copy
                            cube.y=cube.y_copy
                            cube.reverse_gravity=False
                            cube.original_y_position=cube.y
                            frames=0
                            level.attempts+=1
        pygame.display.update()
        clock.tick(120)

home_screen=True
while home_screen:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            home_screen=False
        if event.type==pygame.MOUSEBUTTONDOWN:
            mouse=pygame.mouse.get_pressed()
            if mouse[0]:
                mouse_x,mouse_y=pygame.mouse.get_pos()
                if point_inside_rectangle(251,225,106,114,mouse_x,mouse_y):
                    pass
                elif point_inside_rectangle(411,192,176,181,mouse_x,mouse_y):
                    level_1_x=0
                    easy=pygame.transform.scale(pygame.image.load('Easy.png'),(50,50))
                    normal=pygame.transform.scale(pygame.image.load('Normal.png'),(50,50))
                    hard=pygame.transform.scale(pygame.image.load('Hard.png'),(50,50))
                    main_levels=True
                    while main_levels:
                        for event in pygame.event.get():
                            if event.type==pygame.QUIT:
                                main_levels=False
                            if event.type==pygame.MOUSEBUTTONDOWN:
                                if pygame.mouse.get_pressed()[0]:
                                    mouse_x,mouse_y=pygame.mouse.get_pos()
                                    if level_1_x==0:
                                        if point_inside_rectangle(909,225,71,150,mouse_x,mouse_y):
                                            level_1_x-=1000
                                    elif level_1_x==-1000:
                                        if point_inside_rectangle(909,225,71,150,mouse_x,mouse_y):
                                            level_1_x-=1000
                                        if point_inside_rectangle(20,225,71,150,mouse_x,mouse_y):
                                            level_1_x+=1000
                                    elif level_1_x==-2000:
                                        if point_inside_rectangle(20,225,71,150,mouse_x,mouse_y):
                                            level_1_x+=1000
                                    if point_inside_rectangle(125,150,750,300,mouse_x,mouse_y):
                                        if level_1_x==0:
                                            file=[x.replace('\n','').split(',') for x in open('ThunderstormToucans_gdlevel.txt','r').readlines()]
                                            thunderstorm_toucans_objects=[]
                                            for line in file:
                                                x,y,object_type=line
                                                thunderstorm_toucans_objects.append(Object(int(x),int(y),object_type))
                                            run_level(Level(thunderstorm_toucans_objects))
                                        elif level_1_x==-1000:
                                            file=[x.replace('\n','').split(',') for x in open('BurgerchipExploration_gdlevel.txt','r').readlines()]
                                            burgerchip_exploration_objects=[]
                                            for line in file:
                                                x,y,object_type=line
                                                burgerchip_exploration_objects.append(Object(int(x),int(y),object_type))
                                            run_level(Level(burgerchip_exploration_objects))
                                        elif level_1_x==-2000:
                                            file=[x.replace('\n','').split(',') for x in open('StoichiometrySaviour_gdlevel.txt','r').readlines()]
                                            stoichiometry_saviour_objects=[]
                                            for line in file:
                                                x,y,object_type=line
                                                stoichiometry_saviour_objects.append(Object(int(x),int(y),object_type))
                                            run_level(Level(stoichiometry_saviour_objects))
                        scr.fill((0,0,0))
                        pygame.draw.rect(scr,(47,71,255),[level_1_x,0,1000,600])
                        pygame.draw.rect(scr,(50,193,1),[level_1_x+1000,0,1000,600])
                        pygame.draw.rect(scr,(255,226,95),[level_1_x+2000,0,1000,600])
                        pygame.draw.rect(scr,(23,35,127),[level_1_x+125,150,750,300],0,50)
                        pygame.draw.rect(scr,(25,96,0),[level_1_x+1125,150,750,300],0,50)
                        pygame.draw.rect(scr,(127,113,47),[level_1_x+2125,150,750,300],0,50)
                        scr.blit(easy,(145,275))
                        scr.blit(normal,(level_1_x+1145,275))
                        scr.blit(hard,(level_1_x+2145,275))
                        scr.blit(pygame.font.SysFont('Pusab',50).render('Thunderstorm Toucans',True,(255,255,255)),(level_1_x+215,285))
                        scr.blit(pygame.font.SysFont('Pusab',50).render('Burgerchip Exploration',True,(255,255,255)),(level_1_x+1215,285))
                        scr.blit(pygame.font.SysFont('Pusab',50).render('Stoichiometry Saviour',True,(255,255,255)),(level_1_x+2215,285))
                        if level_1_x==0:
                            scr.blit(right_arrow,(909,225))
                        elif level_1_x==-2000:
                            scr.blit(left_arrow,(20,225))
                        elif level_1_x==-1000:
                            scr.blit(left_arrow,(20,225))
                            scr.blit(right_arrow,(909,225))
                        pygame.display.update()
                elif point_inside_rectangle(637,225,106,114,mouse_x,mouse_y):
                    run_editor=True
                    editor_zoom=50
                    editor_x_offset=0
                    editor_y_offset=0
                    build=True
                    edit=False
                    delete=False
                    build_active=pygame.transform.scale(pygame.image.load('BuildActive.png'),(83,28))
                    build_inactive=pygame.transform.scale(pygame.image.load('BuildInactive.png'),(83,28))
                    edit_active=pygame.transform.scale(pygame.image.load('EditActive.png'),(83,28))
                    edit_inactive=pygame.transform.scale(pygame.image.load('EditInactive.png'),(83,28))
                    delete_active=pygame.transform.scale(pygame.image.load('DeleteActive.png'),(83,28))
                    delete_inactive=pygame.transform.scale(pygame.image.load('DeleteInactive.png'),(83,28))
                    save_button=pygame.transform.scale(pygame.image.load('SaveButton.png'),(198,28))
                    search_button=pygame.transform.scale(pygame.image.load('SearchButton.png'),(75,40))
                    levels_found_overlay=pygame.transform.scale(pygame.image.load('LevelsFoundOverlay.png'),(1000,600))
                    search_levels_text=pygame.transform.scale(pygame.image.load('SearchLevelsText.png'),(431,60))
                    page_index=0
                    levels_found_offset=0
                    show_levels=False
                    display_help=False
                    display_save_message=False
                    display_save_frame_count=0
                    selected_object=None
                    previous_mouse_pos=(None,None)
                    level=Level([Object(x,-1,'block') for x in range(-20,300)])
                    queues=[]
                    while run_editor:
                        for event in pygame.event.get():
                            if event.type==pygame.QUIT:
                                run_editor=False
                                run=False
                            if event.type==pygame.KEYDOWN:
                                if event.key==pygame.K_w:
                                    editor_y_offset-=1
                                elif event.key==pygame.K_a:
                                    editor_x_offset-=1
                                elif event.key==pygame.K_s:
                                    editor_y_offset+=1
                                elif event.key==pygame.K_d:
                                    editor_x_offset+=1
                                elif event.key==pygame.K_UP and edit:
                                    selected_object.y+=1
                                elif event.key==pygame.K_DOWN and edit:
                                    selected_object.y-=1
                                elif event.key==pygame.K_LEFT and edit:
                                    selected_object.x-=1
                                elif event.key==pygame.K_RIGHT and edit:
                                    selected_object.x+=1
                                keys=pygame.key.get_pressed()
                                mouse_x,mouse_y=pygame.mouse.get_pos()
                                obj_x,obj_y=mouse_x//editor_zoom+editor_x_offset,(600-mouse_y)//editor_zoom+editor_y_offset+1
                                if build:
                                    if keys[pygame.K_1]:
                                        level.objects.append(Object(obj_x,obj_y,'spike'))
                                    if keys[pygame.K_2]:
                                        level.objects.append(Object(obj_x,obj_y,'block'))
                                    if keys[pygame.K_3]:
                                        level.objects.append(Object(obj_x,obj_y,'jumppad'))
                                    if keys[pygame.K_4]:
                                        level.objects.append(Object(obj_x,obj_y,'reversegravityportal'))
                                    if keys[pygame.K_5]:
                                        level.objects.append(Object(obj_x,obj_y,'normalgravityportal'))
                                    if keys[pygame.K_6]:
                                        level.objects.append(Object(obj_x,obj_y,'jumpring'))
                            if event.type==pygame.MOUSEBUTTONDOWN:
                                mouse=pygame.mouse.get_pressed()
                                if event.button==4:
                                    editor_zoom-=1
                                elif event.button==5:
                                    editor_zoom+=1
                                if mouse[0]:
                                    mouse_x,mouse_y=pygame.mouse.get_pos()
                                    if 0<mouse_x<83 and 516<mouse_y<544:
                                        build,edit,delete=True,False,False
                                    if 0<mouse_x<83 and 544<mouse_y<572:
                                        build,edit,delete=False,True,False
                                    if 0<mouse_x<83 and 572<mouse_y<600:
                                        build,edit,delete=False,False,True
                                if edit:
                                    if mouse[0]:
                                        mouse_x,mouse_y=pygame.mouse.get_pos()
                                        objects_on_point=[]
                                        for object in level.objects:
                                            if object.obj=='spike':
                                                if point_inside_rectangle((object.x-editor_x_offset)*editor_zoom,600-(object.y-editor_y_offset)*editor_zoom,editor_zoom,editor_zoom,mouse_x,mouse_y):
                                                    objects_on_point.append(object)
                                            if object.obj=='block':
                                                if point_inside_rectangle((object.x-editor_x_offset)*editor_zoom,600-(object.y-editor_y_offset)*editor_zoom,editor_zoom,editor_zoom,mouse_x,mouse_y):
                                                    objects_on_point.append(object)
                                            if object.obj=='jumppad':
                                                if point_inside_rectangle((object.x-editor_x_offset)*editor_zoom,600-(object.y-editor_y_offset)*editor_zoom+42,editor_zoom,editor_zoom//6.25,mouse_x,mouse_y):
                                                    objects_on_point.append(object)
                                            if object.obj=='reversegravityportal':
                                                if point_inside_rectangle((object.x-editor_x_offset)*editor_zoom,600-(object.y-editor_y_offset)*editor_zoom-30,editor_zoom,int(editor_zoom*1.6),mouse_x,mouse_y):
                                                    objects_on_point.append(object)
                                            if object.obj=='normalgravityportal':
                                                if point_inside_rectangle((object.x-editor_x_offset)*editor_zoom,600-(object.y-editor_y_offset)*editor_zoom-30,editor_zoom,int(editor_zoom*1.6),mouse_x,mouse_y):
                                                    objects_on_point.append(object)
                                            if object.obj=='jumpring':
                                                if point_inside_rectangle((object.x-editor_x_offset)*editor_zoom,600-(object.y-editor_y_offset)*editor_zoom,editor_zoom,editor_zoom,mouse_x,mouse_y):
                                                    objects_on_point.append(object)
                                        if len(objects_on_point)==1:
                                            selected_object=objects_on_point[0]
                                        elif len(objects_on_point)>1:
                                            for queue in queues:
                                                if queue.elements==objects_on_point:
                                                    selected_object=queue.elements[queue.selected_position]
                                                    queue.selected_position+=1
                                                    queue.selected_position%=len(queue.elements)
                                                    break
                                            else:
                                                queues.append(Queue(objects_on_point))
                                                selected_object=queues[-1].elements[queues[-1].selected_position]
                                                queues[-1].selected_position+=1
                                                queues[-1].selected_position%=len(queues[-1].elements)
                                if point_inside_rectangle(802,572,198,28,mouse_x,mouse_y):
                                    file=open(str(datetime.datetime.now()).replace(' ','_')+'_gdlevel.txt','w+')
                                    for object in level.objects:
                                        file.write(f'{object.x},{object.y},{object.obj}\n')
                                    display_save_message=True
                                    file.close()
                                if point_inside_rectangle(925,532,75,40,mouse_x,mouse_y):
                                    show_levels=True
                            if event.type==pygame.MOUSEBUTTONUP:
                                if show_levels:
                                    previous_mouse_pos=(None,None)
                        scr.fill((0,0,0))
                        if not show_levels:
                            scr.blit(bg,(0,0))
                            start_grid_x=(editor_x_offset-int(editor_x_offset))/50
                            start_grid_y=(editor_y_offset-int(editor_y_offset))/50
                            for grid_x in range(0,1000,50):
                                pygame.draw.line(scr,(128,128,128),(grid_x+start_grid_x,0),(grid_x+start_grid_x,600))
                            for grid_y in range(0,600,50):
                                pygame.draw.line(scr,(128,128,128),(0,grid_y+start_grid_y),(1000,grid_y+start_grid_y))
                            scr.blit(save_button,(802,572))
                            scr.blit(search_button,(925,532))
                            if build:
                                scr.blit(build_active,(0,516))
                            else:
                                scr.blit(build_inactive,(0,516))
                            if edit:
                                scr.blit(edit_active,(0,544))
                            else:
                                scr.blit(edit_inactive,(0,544))
                            if delete:
                                scr.blit(delete_active,(0,572))
                            else:
                                scr.blit(delete_inactive,(0,572))
                            for object in level.objects:
                                if object.obj=='spike':
                                    scr.blit(pygame.transform.scale(spike,(editor_zoom,editor_zoom)),((object.x-editor_x_offset)*editor_zoom,600-(object.y-editor_y_offset)*editor_zoom))
                                if object.obj=='block':
                                    scr.blit(pygame.transform.scale(block,(editor_zoom,editor_zoom)),((object.x-editor_x_offset)*editor_zoom,600-(object.y-editor_y_offset)*editor_zoom))
                                if object.obj=='jumppad':
                                    scr.blit(pygame.transform.scale(jumppad,(editor_zoom,editor_zoom//6.25)),((object.x-editor_x_offset)*editor_zoom,600-(object.y-editor_y_offset)*editor_zoom+42))
                                if object.obj=='reversegravityportal':
                                    scr.blit(pygame.transform.scale(reversegravityportal,(editor_zoom,int(editor_zoom*1.6))),((object.x-editor_x_offset)*editor_zoom,600-(object.y-editor_y_offset)*editor_zoom-30))
                                if object.obj=='normalgravityportal':
                                    scr.blit(pygame.transform.scale(normalgravityportal,(editor_zoom,int(editor_zoom*1.6))),((object.x-editor_x_offset)*editor_zoom,600-(object.y-editor_y_offset)*editor_zoom-30))
                                if object.obj=='jumpring':
                                    scr.blit(pygame.transform.scale(jumpring,(editor_zoom,editor_zoom)),((object.x-editor_x_offset)*editor_zoom,600-(object.y-editor_y_offset)*editor_zoom))
                            if display_save_message:
                                scr.blit(pygame.font.SysFont('Pusab',100).render('Saved!',True,(255,255,255)),(325,270))
                                display_save_frame_count+=1
                                if display_save_frame_count==120:
                                    display_save_frame_count=0
                                    display_save_message=False
                        else:
                            scr.fill((0,0,0))
                            levels_found=[x for x in os.listdir() if x.endswith('_gdlevel.txt')]
                            page=[levels_found[y:y+10] for y in range(0,len(levels_found),10)][page_index] if len(levels_found)>10 else [levels_found][page_index]
                            for i,level_found in enumerate(page):
                                pygame.draw.rect(scr,(230,126,77),[195,107+i*200+levels_found_offset+i*10,613,200])
                                scr.blit(pygame.font.SysFont('Pusab',25).render(level_found,True,(255,255,255)),(205,117+i*200+levels_found_offset+i*10))
                            pygame.draw.rect(scr,(0,121,239),[0,0,999,105])
                            pygame.draw.rect(scr,(0,121,239),[0,0,188,599])
                            pygame.draw.rect(scr,(0,121,239),[1,511,999,89])
                            pygame.draw.rect(scr,(0,121,239),[812,0,188,600])
                            scr.blit(levels_found_overlay,(0,0))
                            scr.blit(search_levels_text,(285,40))
                            scr.blit(pygame.font.SysFont('Pusab',20).render(f'{page_index*10+1} to {page_index*10+len(page)} of {len(levels_found)} in current directory',True,(255,255,255)),(20,20))
                            if pygame.mouse.get_pressed()[0]:
                                mouse_x,mouse_y=pygame.mouse.get_pos()
                                if point_inside_rectangle(195,107,613,400,mouse_x,mouse_y):
                                    if previous_mouse_pos!=(None,None):
                                        difference=previous_mouse_pos[1]-mouse_y
                                        levels_found_offset-=difference
                                        previous_mouse_pos=(mouse_x,mouse_y)
                                    else:
                                        previous_mouse_pos=(mouse_x,mouse_y)
                            if pygame.mouse.get_pressed()[2]:
                                mouse_x,mouse_y=pygame.mouse.get_pos()
                                for i,l in enumerate(page):
                                    if point_inside_rectangle(195,107+i*200+levels_found_offset+i*10,613,200,mouse_x,mouse_y):
                                        file=[x.replace('\n','').split(',') for x in open(l,'r').readlines()]
                                        level_objects=[]
                                        for line in file:
                                            x,y,object_type=line
                                            level_objects.append(Object(int(x),int(y),object_type))
                                        level=Level(level_objects)
                                        show_levels=False
                            keys=pygame.key.get_pressed()
                            if keys[pygame.K_LEFT]:
                                page_index-=1
                                page_index%=len(levels_found)//10+1
                            if keys[pygame.K_RIGHT]:
                                page_index+=1
                                page_index%=len(levels_found)//10+1
                            print(page_index)
                        pygame.display.update()
                        clock.tick(120)
    scr.fill((0,0,0))
    scr.blit(bg,(0,0))
    scr.blit(homescreen,(0,0))
    pygame.display.update()
pygame.quit()