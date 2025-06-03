import pygame, random, copy, time

pygame.init()

scr_width = 720
scr_height = 480
scr = pygame.display.set_mode((scr_width, scr_height))

def get_frames_radix_sort(lst):
    max_size = -float("inf")
    for l in lst:
        if len(str(l)) > max_size:
            max_size = len(str(l))
    for i in range(len(lst)):
        lst[i] = str(lst[i]).zfill(max_size)
    for d in range(max_size-1, -1, -1):
        buckets = [[] for _ in range(10)]
        for j in range(len(lst)):
            buckets[int(lst[j][d])].append(lst[j])
            buckets_copy = []
            for bx in buckets:
                for by in bx:
                    buckets_copy.append(by)
            new_lst = lst[j+1:]
            yield [int(z) for z in buckets_copy+new_lst]
        lst = []
        for x in buckets:
            for y in x:
                lst.append(y)

def get_frames_bubble_sort(lst):
    for i in range(len(lst)-1, -1, -1):
        flag = False
        for j in range(i):
            if lst[j] > lst[j+1]:
                lst[j], lst[j+1] = lst[j+1], lst[j]
                yield [[int(a) for a in lst.copy()], j, j+1, lst[j], lst[j+1]]
                flag = True
        if not flag:
            break

def merge(sorted_a, sorted_b):
    merged = []
    pointer_a = 0
    pointer_b = 0
    while True:
        if pointer_a == len(sorted_a):
            merged.extend(sorted_b[pointer_b:])
            break
        if pointer_b == len(sorted_b):
            merged.extend(sorted_a[pointer_a:])
            break

        val_a = sorted_a[pointer_a]
        val_b = sorted_b[pointer_b]

        if val_a < val_b:
            merged.append(val_a)
            pointer_a += 1
        elif val_b < val_a:
            merged.append(val_b)
            pointer_b += 1
        else:
            merged.append(val_a)
            merged.append(val_b)
            pointer_a += 1
            pointer_b += 1
    return merged


merges = []

def get_frames_merge_sort(lst, a, b):
    if len(lst) == 1:
        return lst
    left = get_frames_merge_sort(lst[:len(lst)//2], a, a+len(lst)//2-1)
    right = get_frames_merge_sort(lst[len(lst)//2:], a+len(lst)//2, b)
    m = merge(left, right)
    merges.append([m.copy(), a, b])
    return m

quick_sort_changes = []

def partition(lst, l, h):
    i = l-1
    j = l
    while True:
        if j == h:
            i += 1
            lst[i], lst[h] = lst[h], lst[i]
            quick_sort_changes.append([lst.copy(), i, h, lst[i], lst[h]])
            break
        if lst[j] > lst[h]:
            j += 1
        else:
            i += 1
            lst[i], lst[j] = lst[j], lst[i]
            quick_sort_changes.append([lst.copy(), i, j, lst[i], lst[j]])
            j += 1
    return lst, i

def get_frames_quick_sort(lst, low, high):
    if low >= high:
        return lst
    lst, ind = partition(lst, low, high)
    lst = get_frames_quick_sort(lst, ind+1, high)
    lst = get_frames_quick_sort(lst, low, ind-1)
    return lst

num_elements = 128

test_lst = list(range(1, num_elements + 1))
max_val = max(test_lst)
num_vals = len(test_lst)
random.shuffle(test_lst)

frames_bubble = list(get_frames_bubble_sort(test_lst))

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

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    scr.fill((0, 0, 0))

    try:
        curr_radix_frame = frames_bubble[curr_frame][0]
    except IndexError:
        pygame.quit()
        quit()
    for l,num in enumerate(curr_radix_frame):
        pygame.draw.rect(scr, (255, 255, 255), [int(l*(scr_width/num_vals))+1, int(scr_height-(scr_height/max_val)*num)+1, int(scr_width/num_vals-2)+1, int((scr_height/max_val)*num)+1])
    
    fp = frames_bubble[curr_frame][1]
    rp = frames_bubble[curr_frame][2]
    v1 = frames_bubble[curr_frame][3]
    v2 = frames_bubble[curr_frame][4]

    pygame.draw.rect(scr, (255, 0, 0), [int(fp*(scr_width/num_vals))+1, int(scr_height-(scr_height/max_val)*v1)+1, int(scr_width/num_vals-2)+1, int((scr_height/max_val)*v1)+1])
    pygame.draw.rect(scr, (255, 0, 0), [int(rp*(scr_width/num_vals))+1, int(scr_height-(scr_height/max_val)*v2)+1, int(scr_width/num_vals-2)+1, int((scr_height/max_val)*v2)+1])

    """curr_pointer_frame = pointers_frames_merge[curr_frame]
    s, e, v1, v2 = curr_pointer_frame
    pygame.draw.rect(scr, (255, 0, 0), [int(s*(scr_width/num_vals))+1, int(scr_height-(scr_height/max_val)*v1)+1, int(scr_width/num_vals-2)+1, int((scr_height/max_val)*v1)+1])
    pygame.draw.rect(scr, (255, 0, 0), [int(e*(scr_width/num_vals))+1, int(scr_height-(scr_height/max_val)*v2)+1, int(scr_width/num_vals-2)+1, int((scr_height/max_val)*v2)+1])
"""
    curr_frame += 1
    
    pygame.display.update()
    clock.tick(60)
