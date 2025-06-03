import pygame
import time
import random
i = input(
  "To visualise Dijkstra's algorithm, enter D, to visualise A*, enter anything else: "
)
pygame.init()
clock = pygame.time.Clock()
def h_cost(x1, y1, x2, y2):
  return ((y2-y1)**2+(x2-x1)**2)**0.5
def a_star(x1, y1, x2, y2, no, s, square_size):
  scr = pygame.display.set_mode((square_size * s, square_size * s))
  pygame.display.set_caption("Dijkstra's and A*")
  f_cost = {}
  for x in range(s):
    for y in range(s):
      f_cost[f'{x},{y}'] = float('inf')
  g_cost = {}
  for x in range(s):
    for y in range(s):
      g_cost[f'{x},{y}'] = float('inf')
  g_cost[f'{x1},{y1}'] = 0
  f_cost[f'{x1},{y1}'] = h_cost(x1, y1, x2, y2)
  came_from = {}
  valid = [[x1, y1]]
  visited = []
  while valid:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()
    for x in range(s):
      for y in range(s):
        pygame.draw.rect(
          scr, (128, 128, 128),
          [y * square_size, x * square_size, square_size - s//25, square_size - s//25])
    for v in visited:
      pygame.draw.rect(scr, (0, 255, 0), [
        v[1] * square_size, v[0] * square_size, square_size - 2,
        square_size - 2
      ])
    if i == 'D':
      curr_x, curr_y = sorted([[v, g_cost[f'{v[0]},{v[1]}']] for v in valid],
                              key=lambda l: l[1])[0][0]
    else:
      curr_x, curr_y = sorted([[v, f_cost[f'{v[0]},{v[1]}']] for v in valid],
                              key=lambda l: l[1])[0][0]
    for v in valid:
      pygame.draw.rect(scr, (128, 0, 255), [
        v[1] * square_size, v[0] * square_size, square_size - 2,
        square_size - 2
      ])
    pygame.draw.rect(
      scr, (255, 0, 0),
      [y1 * square_size, x1 * square_size, square_size - 2, square_size - 2])
    pygame.draw.rect(scr, (0, 255, 255), [
      curr_y * square_size, curr_x * square_size, square_size - 2,
      square_size - 2
    ])
    pygame.draw.rect(
      scr, (255, 0, 0),
      [y2 * square_size, x2 * square_size, square_size - 2, square_size - 2])
    for n in no:
      pygame.draw.rect(scr, (255, 255, 255), [
        n[1] * square_size, n[0] * square_size, square_size - 2,
        square_size - 2
      ])
    neighbours = [
      x for x in [[curr_x + 1, curr_y], [curr_x -
                                          1, curr_y], [curr_x, curr_y +
                                                      1], [curr_x, curr_y - 1],
                  [curr_x + 1, curr_y + 1], [curr_x + 1, curr_y -
                                              1], [curr_x - 1, curr_y +
                                                  1], [curr_x - 1, curr_y - 1]]
      if x not in no and -1 < x[0] < s and -1 < x[1] < s
      ]
    for n in neighbours:
      if n not in visited:
        visited.append(n)
    if [curr_x, curr_y] == [x2, y2]:
      looking_at = [x2, y2]
      final = [[x2, y2]]
      while True:
        looking_at = came_from[f'{looking_at[0]},{looking_at[1]}']
        if looking_at == [x1, y1]:
          break
        final.append(looking_at)
      for f in final:
        pygame.draw.rect(scr, (0, 0, 255), [
          f[1] * square_size, f[0] * square_size, square_size - 2,
          square_size - 2
        ])
      pygame.display.update()
      time.sleep(5)
      return final
    valid.remove([curr_x, curr_y])
    for neighbour in neighbours:
      if neighbour[0] == curr_x or neighbour[1] == curr_y:
        tentative_g_cost = g_cost[f'{curr_x},{curr_y}'] + 1
      else:
        tentative_g_cost = g_cost[f'{curr_x},{curr_y}'] + 1.4
      if tentative_g_cost < g_cost[f'{neighbour[0]},{neighbour[1]}']:
        g_cost[f'{neighbour[0]},{neighbour[1]}'] = tentative_g_cost
        f_cost[f'{neighbour[0]},{neighbour[1]}'] = tentative_g_cost + h_cost(
          neighbour[0], neighbour[1], x2, y2)
        came_from[f'{neighbour[0]},{neighbour[1]}'] = [curr_x, curr_y]
        if [neighbour[0], neighbour[1]] not in valid:
          valid.append([neighbour[0], neighbour[1]])
    pygame.display.update()
    clock.tick(int(s*1.2))
  


size = 100
a, b = random.randint(0, size - 1), random.randint(0, size - 1)
c, d = random.randint(0, size - 1), random.randint(0, size - 1)
while [a, b] == [c, d]:
  c, d = random.randint(0, size - 1), random.randint(0, size - 1)
no = []
for _ in range(int((size**2) / 3)):
  pair = [random.randint(0, size - 1), random.randint(0, size - 1)]
  if pair != [0, 0] and pair != [a, b] and pair != [c, d]:
    no.append(pair)
a_star(c, d, a, b, no, size, 5)
