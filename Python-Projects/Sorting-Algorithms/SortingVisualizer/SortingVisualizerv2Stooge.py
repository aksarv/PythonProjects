# Stooge sort is known for making a LOT of redundant comparisons. Ever wondered just how many? Well, you're about to find out

import pygame, random

# Python program to implement stooge sort

stooge_frames = [] 
  
def stoogesort(arr, l, h): 
    if l >= h: 
        return
   
    # If first element is smaller 
    # than last, swap them 

    frame = [arr.copy(), l, h, arr[l], arr[h]]
    if arr[l]>arr[h]: 
        t = arr[l] 
        arr[l] = arr[h] 
        arr[h] = t 
        frame += [0]
    else:
        frame += [1]
    stooge_frames.append(frame)
   
    # If there are more than 2 elements in 
    # the array 
    if h-l + 1 > 2: 
        t = (int)((h-l + 1)/3) 
   
        # Recursively sort first 2 / 3 elements 
        stoogesort(arr, l, (h-t)) 
   
        # Recursively sort last 2 / 3 elements 
        stoogesort(arr, l + t, (h)) 
   
        # Recursively sort first 2 / 3 elements 
        # again to confirm 
        stoogesort(arr, l, (h-t)) 

def draw_text_with_outline(text, font, text_color, outline_color, position, outline_width=2):
    # Render the outline by drawing the text in black slightly offset in all directions
    text_surface = font.render(text, True, text_color)
    outline_surface = font.render(text, True, outline_color)
    
    x, y = position

    # Draw the outline
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                scr.blit(outline_surface, (x + dx, y + dy))

    # Draw the main text on top
    scr.blit(text_surface, position)

pygame.init()
scr_width, scr_height = 720, 480
scr = pygame.display.set_mode((scr_width, scr_height))

num_elements = 128

test_lst = list(range(1, num_elements + 1))
max_val = max(test_lst)
num_vals = len(test_lst)
random.shuffle(test_lst)

stoogesort(test_lst, 0, len(test_lst) - 1)

frames_quick = stooge_frames

"""get_frames_merge_sort(test_lst, 0, len(test_lst))
frames_merge = []
pointers_frames_merge = []
copy_test_lst = test_lst.copy()

for m in merges:
    change, start, end = m 
    for j,i in enumerate(range(start, end)):
        copy_test_lst[i] = change[j]
    val1 = copy_test_lst[start]
    val2 = copy_test_lst[end-1]
    frames_merge.append(copy_test_lst.copy())
    pointers_frames_merge.append([copy.copy(start), copy.copy(end), copy.copy(val1), copy.copy(val2)])"""

curr_frame = 0

clock=pygame.time.Clock()

rc_counter = 0

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    scr.fill((0, 0, 0))

    try:
        curr_radix_frame = frames_quick[curr_frame][0]
    except IndexError:
        pygame.quit()
        quit()
    for l,num in enumerate(curr_radix_frame):
        pygame.draw.rect(scr, (255, 255, 255), [int(l*(scr_width/num_vals))+1, int(scr_height-(scr_height/max_val)*num)+1, int(scr_width/num_vals-2)+1, int((scr_height/max_val)*num)+1])
    
    fp = frames_quick[curr_frame][1]
    rp = frames_quick[curr_frame][2]
    v1 = frames_quick[curr_frame][3]
    v2 = frames_quick[curr_frame][4]
    rc = frames_quick[curr_frame][5]

    rc_counter += rc

    draw_text_with_outline("Redundant Comparisons: " + str(rc_counter), pygame.font.SysFont("Pusab", 20), (255, 255, 255), (0, 0, 0), (20, 20))

    pygame.draw.rect(scr, (255, 0, 0), [int(fp*(scr_width/num_vals))+1, int(scr_height-(scr_height/max_val)*v1)+1, int(scr_width/num_vals-2)+1, int((scr_height/max_val)*v1)+1])
    pygame.draw.rect(scr, (255, 0, 0), [int(rp*(scr_width/num_vals))+1, int(scr_height-(scr_height/max_val)*v2)+1, int(scr_width/num_vals-2)+1, int((scr_height/max_val)*v2)+1])


    """curr_pointer_frame = pointers_frames_merge[curr_frame]
    s, e, v1, v2 = curr_pointer_frame
    pygame.draw.rect(scr, (255, 0, 0), [int(s*(scr_width/num_vals))+1, int(scr_height-(scr_height/max_val)*v1)+1, int(scr_width/num_vals-2)+1, int((scr_height/max_val)*v1)+1])
    pygame.draw.rect(scr, (255, 0, 0), [int(e*(scr_width/num_vals))+1, int(scr_height-(scr_height/max_val)*v2)+1, int(scr_width/num_vals-2)+1, int((scr_height/max_val)*v2)+1])
"""
    curr_frame += 1
    
    pygame.display.update()
    clock.tick(240)
