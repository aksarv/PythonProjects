import pygame, random, copy

pygame.init()

scr_width = 1500
scr_height = 1000
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
                yield [int(a) for a in lst.copy()]
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

num_elements = 400

test_lst = list(range(1, num_elements + 1))
max_val = max(test_lst)
num_vals = len(test_lst)
random.shuffle(test_lst)

get_frames_merge_sort(test_lst, 0, len(test_lst))
frames_merge = []
pointers_frames_merge = []
copy_test_lst = test_lst.copy()

for m in merges:
    change, start, end = m
    val1 = copy_test_lst[start]
    val2 = copy_test_lst[end-1]
    for j,i in enumerate(range(start, end)):
        copy_test_lst[i] = change[j]
    frames_merge.append(copy_test_lst.copy())
    pointers_frames_merge.append([copy.copy(start), copy.copy(end), copy.copy(val1), copy.copy(val2)])

curr_frame = 0

clock=pygame.time.Clock()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    scr.fill((0, 0, 0))

    try:
        curr_radix_frame = frames_merge[curr_frame]
    except IndexError:
        pygame.quit()
        quit()
    for l,num in enumerate(curr_radix_frame):
        pygame.draw.rect(scr, (255, 255, 255), [l*(scr_width/num_vals), scr_height-(scr_height/max_val)*num, scr_width/num_vals-2, (scr_height/max_val)*num])
    
    curr_pointer_frame = pointers_frames_merge[curr_frame]
    s, e, v1, v2 = curr_pointer_frame
    pygame.draw.rect(scr, (255, 0, 0), [s*(scr_width/num_vals), scr_height-(scr_height/max_val)*v1, scr_width/num_vals-2, (scr_height/max_val)*v1])
    pygame.draw.rect(scr, (255, 0, 0), [e*(scr_width/num_vals), scr_height-(scr_height/max_val)*v2, scr_width/num_vals-2, (scr_height/max_val)*v2])

    curr_frame += 1
    
    pygame.display.update()
    clock.tick(20)
