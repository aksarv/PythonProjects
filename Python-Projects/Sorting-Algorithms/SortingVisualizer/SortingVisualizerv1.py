#Bad

import pygame, random, time, heapq, itertools
pygame.init()
sizing = 600
scr = pygame.display.set_mode((sizing, sizing))
pygame.display.set_caption('Visualize Sorting Algorithms')
font = pygame.font.SysFont(None, 24)
run = True
_list = random.sample(range(sizing), sizing)
start = time.time()
#Functions
def swap(_list, index1, index2):
    one = _list[index1]
    two = _list[index2]
    _list[index1] = two
    _list[index2] = one
def is_sorted(_list):
    for x in range(len(_list)-1):
        if _list[x] > _list[x+1]:
            return False
    return True
def bubble_sort(_list):
    while not is_sorted(_list):
        for x in range(len(_list)-1):
            if _list[x] > _list[x+1]:
                swap(_list, x, x+1)
    return _list
def chunks(_list, n):
    return [_list[i * n:(i + 1) * n] for i in range((len(_list) + n - 1) // n )] 
#Bubble Sort
while run and not is_sorted(_list):
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
  scr.fill((255, 255, 255))
  for z in range(len(_list)-1):
      if _list[z] > _list[z+1]:
          swap(_list, z, z+1)
  for y in range(len(_list)):
      pygame.draw.rect(scr, (round(sizing/3000*_list[y]), round(sizing/3000*_list[y]), round(sizing/3000*_list[y])), [y, sizing-_list[y], 1, _list[y]])
  text = font.render('Time: '+str(round(time.time()-start, 1)), True, (0, 0, 0))
  scr.blit(text, (32, 32))
  bubblesort = font.render('Bubble Sort / Delay: 0.01s', True, (0, 0, 0))
  scr.blit(bubblesort, (sizing/2, 32))
  time.sleep(.01)
  pygame.display.flip()
#Selection Sort
time.sleep(3)
random.shuffle(_list)
start1 = time.time()
minimumcounter = 1
while run and not is_sorted(_list):
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
  scr.fill((255, 255, 255))
  minimum = heapq.nsmallest(minimumcounter, _list)[-1]
  _list.remove(minimum)
  _list.insert(0, minimum)
  if minimumcounter > 600:
        _list = _list[::-1]
  for y in range(len(_list)):
      pygame.draw.rect(scr, (round(sizing/3000*_list[y]), round(sizing/3000*_list[y]), round(sizing/3000*_list[y])), [y, sizing-_list[y], 1, _list[y]])
  text = font.render('Time: '+str(round(time.time()-start1, 1)), True, (0, 0, 0))
  scr.blit(text, (32, 32))
  selecsort = font.render('Selection Sort / Delay: 0.01s', True, (0, 0, 0))
  scr.blit(selecsort, (sizing/2, 32))
  time.sleep(.01)
  pygame.display.flip()
  minimumcounter += 1
#Insertion Sort
time.sleep(3)
random.shuffle(_list)
start1 = time.time()
marker = 1
while run and not is_sorted(_list):
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
  scr.fill((255, 255, 255))
  if marker == 1:
      if _list[0] > _list[1]:
          swap(_list, 0, 1)
  else:
      for a in range(len(_list[:marker])):
          if _list[a] <= _list[marker]:
              swap(_list, a, marker)
  if marker == 599:
      _list = _list[::-1]
  for y in range(len(_list)):
      pygame.draw.rect(scr, (round(sizing/3000*_list[y]), round(sizing/3000*_list[y]), round(sizing/3000*_list[y])), [y, sizing-_list[y], 1, _list[y]])
  text = font.render('Time: '+str(round(time.time()-start1, 1)), True, (0, 0, 0))
  scr.blit(text, (32, 32))
  insertionsort = font.render('Insertion Sort / Delay: 0.01s', True, (0, 0, 0))
  scr.blit(insertionsort, (sizing/2, 32))
  time.sleep(.01)
  pygame.display.flip()
  marker += 1
#Bounce Sort
time.sleep(3)
random.shuffle(_list)
start1 = time.time()
marker = 1
backwards = False
while run and not is_sorted(_list):
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
  scr.fill((255, 255, 255))
  if not backwards:
      for x in range(len(_list)-1):
          if _list[x] > _list[x+1]:
              swap(_list, x, x+1)
      backwards = True
  elif backwards:
      start = len(_list)-1
      while start != 1:
          if _list[start] < _list[start-1]:
              swap(_list, start, start-1)
          start -= 1
      backwards = False
  for y in range(len(_list)):
      pygame.draw.rect(scr, (round(sizing/3000*_list[y]), round(sizing/3000*_list[y]), round(sizing/3000*_list[y])), [y, sizing-_list[y], 1, _list[y]])
  text = font.render('Time: '+str(round(time.time()-start1, 1)), True, (0, 0, 0))
  scr.blit(text, (32, 32))
  bouncesort = font.render('Bounce Sort / Delay: 0.01s', True, (0, 0, 0))
  scr.blit(bouncesort, (sizing/2, 32))
  time.sleep(.01)
  pygame.display.flip()
  marker += 1
#Iterative Merge Sort
time.sleep(3)
random.shuffle(_list)
start1 = time.time()
block = 2
backwards = False
while run and not is_sorted(_list):
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
  scr.fill((255, 255, 255))
  if block > len(_list):
      for z in range(len(_list)-1):
          if _list[z] > _list[z+1]:
              swap(_list, z, z+1)
  chunk = chunks(_list, block)
  for x in range(len(chunk)):
      chunk[x] = bubble_sort(chunk[x])
  _list = list(itertools.chain.from_iterable(chunk))
  for y in range(len(_list)):
      pygame.draw.rect(scr, (round(sizing/3000*_list[y]), round(sizing/3000*_list[y]), round(sizing/3000*_list[y])), [y, sizing-_list[y], 1, _list[y]])
  text = font.render('Time: '+str(round(time.time()-start1, 1)), True, (0, 0, 0))
  scr.blit(text, (32, 32))
  mergesort = font.render('Iterative Merge Sort / Delay: 0.01s', True, (0, 0, 0))
  scr.blit(mergesort, (sizing/2, 32))
  time.sleep(.01)
  pygame.display.flip()
  block *= 2
#Bogo Sort
_list = [100, 200, 300, 400, 500, 600]
time.sleep(3)
random.shuffle(_list)
start1 = time.time()
block = 2
backwards = False
while run and not is_sorted(_list):
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
  scr.fill((255, 255, 255))
  random.shuffle(_list)
  for y in range(len(_list)):
      pygame.draw.rect(scr, (round(sizing/3000*_list[y]), round(sizing/3000*_list[y]), round(sizing/3000*_list[y])), [y*100, sizing-_list[y], 100, _list[y]])
  text = font.render('Time: '+str(round(time.time()-start1, 1)), True, (0, 0, 0))
  scr.blit(text, (32, 32))
  bogosort = font.render('Bogo Sort / Delay: 0.01s', True, (0, 0, 0))
  scr.blit(bogosort, (sizing/2, 32))
  time.sleep(.01)
  pygame.display.flip()
  block *= 2  
time.sleep(3)
pygame.quit()
quit()
