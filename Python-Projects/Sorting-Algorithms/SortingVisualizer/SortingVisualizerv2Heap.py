import pygame, random

heap_sort_frames = []

def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left

    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def build_max_heap(arr):
    n = len(arr)
    
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
        heap_sort_frames.append([arr.copy(), n, i, arr[0], arr[i]])

def heap_sort(arr):
    n = len(arr)
    
    build_max_heap(arr)
    
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heap_sort_frames.append([arr.copy(), 0, i, arr[0], arr[i]])
        heapify(arr, i, 0)

pygame.init()
scr_width, scr_height = 720, 480
scr = pygame.display.set_mode((scr_width, scr_height))

num_vals = 512
test_lst = list(range(1, num_vals + 1))
max_val = max(test_lst)
random.shuffle(test_lst)

heap_sort(test_lst)

clock = pygame.time.Clock()

frame_no = 0

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    scr.fill((0, 0, 0))

    try:
        curr_heap_frame = heap_sort_frames[frame_no][0]
        
    except IndexError:
        pygame.quit()
        quit()

    for l,num in enumerate(curr_heap_frame):
        pygame.draw.rect(scr, (255, 255, 255), [int(l*(scr_width/num_vals))+1, int(scr_height-(scr_height/max_val)*num)+1, int(scr_width/num_vals-2)+1, int((scr_height/max_val)*num)+1])

    fp = heap_sort_frames[frame_no][1]
    rp = heap_sort_frames[frame_no][2]
    v1 = heap_sort_frames[frame_no][3]
    v2 = heap_sort_frames[frame_no][4]

    pygame.draw.rect(scr, (255, 0, 0), [int(fp*(scr_width/num_vals))+1, int(scr_height-(scr_height/max_val)*v1)+1, int(scr_width/num_vals-2)+1, int((scr_height/max_val)*v1)+1])
    pygame.draw.rect(scr, (255, 0, 0), [int(rp*(scr_width/num_vals))+1, int(scr_height-(scr_height/max_val)*v2)+1, int(scr_width/num_vals-2)+1, int((scr_height/max_val)*v2)+1])

    frame_no += 1
    pygame.display.update()
    clock.tick(60)
