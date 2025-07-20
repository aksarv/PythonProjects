import pygame, math, random, time

pygame.init()

pygame.mixer.init()

pygame.mixer.music.load("bgmusic.mp3")

boom = pygame.mixer.Sound("boom.mp3")

pygame.mixer.music.play(loops=-1)

scr_width, scr_height = 1080, 720
scr = pygame.display.set_mode((scr_width, scr_height))

pygame.display.set_caption("READING SCHOOL TANKS")

tank_size = 30
vertical_offset = 5

total_score = 0

GRAVITY = 0.5

tank = pygame.transform.scale(pygame.image.load("tank.png"), (tank_size, tank_size))
bg = pygame.transform.scale(pygame.image.load("logo.png"), (1080, 720))
reading_school_thingy = pygame.transform.scale(pygame.image.load("readingschool.png"), (1080, 205))

class Circle:
    def __init__(self, center_x, center_y, radius):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius

class Tank:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.prev_x = None
        self.prev_y = None
        self.y_vel = 0
        self.gravity = GRAVITY
        self.img = tank
        self.x_speed = 3
        self.collide_circle = Circle(x + 15, y + 15, 15)
        self.angle = -math.pi / 2

    def draw_collide_circle(self):
        pygame.draw.circle(scr, (255, 255, 255), (self.collide_circle.center_x, self.collide_circle.center_y), self.collide_circle.radius)
    
    def update_hitbox(self):
        self.collide_circle = Circle(self.x + 15, self.y + 15, 15)

    def draw_angle(self):
        pygame.draw.circle(scr, (0, 0, 255), (self.x + math.cos(self.angle) * 25 + 15, self.y + math.sin(self.angle) * 25 + 15), 3)

    def update(self):
        self.prev_x = self.x
        self.prev_y = self.y
        self.y += self.y_vel
        self.y_vel += self.gravity

class Player1(Tank):
    def __init__(self, x, y):
        super().__init__(x, y)

class Player2(Tank):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.img = pygame.transform.flip(self.img, True, False)

class Terrain:
    def __init__(self):
        self.points = [[x, 520 - vertical_offset] for x in range(0, 1082, 2)]

class Bullet:
    def __init__(self, x, y, x_vel, y_vel, sent_from):
        self.x = x
        self.y = y
        self.prev_x = None
        self.prev_y = None
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.gravity = GRAVITY
        self.sent_from = sent_from
        self.id = time.time()
    
    def update(self):
        self.prev_x = self.x
        self.prev_y = self.y
        self.x += self.x_vel
        self.y += self.y_vel
        self.y_vel += self.gravity

player_1 = Player1(0, 440)
player_2 = Player2(1080 - tank_size, 440)
terrain = Terrain()

bullets = []

show_hitbox = True

clock = pygame.time.Clock()

run1 = True
while run1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run1 = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                run1 = False

    scr.fill((255, 255, 0))

    scr.blit(pygame.font.SysFont(None, 32).render("Player 1 Controls:", True, (0, 0, 0)), (20, 20))
    scr.blit(pygame.font.SysFont(None, 32).render("A - Move Left", True, (0, 0, 0)), (20, 50))
    scr.blit(pygame.font.SysFont(None, 32).render("D - Move Right:", True, (0, 0, 0)), (20, 80))
    scr.blit(pygame.font.SysFont(None, 32).render("Q - Rotate Anticlockwise", True, (0, 0, 0)), (20, 110))
    scr.blit(pygame.font.SysFont(None, 32).render("E - Rotate Clockwise", True, (0, 0, 0)), (20, 140))
    scr.blit(pygame.font.SysFont(None, 32).render("X - Shoot", True, (0, 0, 0)), (20, 170))
    scr.blit(pygame.font.SysFont(None, 32).render("Player 2 Controls:", True, (0, 0, 0)), (20, 200))
    scr.blit(pygame.font.SysFont(None, 32).render("Left Arrow - Move Left", True, (0, 0, 0)), (20, 230))
    scr.blit(pygame.font.SysFont(None, 32).render("Right Arrow - Move Right", True, (0, 0, 0)), (20, 260))
    scr.blit(pygame.font.SysFont(None, 32).render("B - Rotate Anticlockwise", True, (0, 0, 0)), (20, 290))
    scr.blit(pygame.font.SysFont(None, 32).render("M - Rotate Clockwise", True, (0, 0, 0)), (20, 320))
    scr.blit(pygame.font.SysFont(None, 32).render("N - Shoot", True, (0, 0, 0)), (20, 350))
    scr.blit(pygame.font.SysFont(None, 32).render("Press ENTER to play", True, (0, 0, 0)), (20, 450))

    pygame.display.update()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                boom.play()
                bullets.append(Bullet(player_2.x, player_2.y, math.cos(-player_2.angle) * 20, -math.sin(-player_2.angle) * 20, 2))
            if event.key == pygame.K_x:
                boom.play()
                bullets.append(Bullet(player_1.x, player_1.y, math.cos(-player_1.angle) * 20, -math.sin(-player_1.angle) * 20, 1))

    scr.fill((255, 255, 0))

    scr.blit(bg, (0, 0))

    scr.blit(reading_school_thingy, (0, 515))

    # for point in terrain.points:
    #     pygame.draw.circle(scr, (0, 255, 0), (point[0], point[1]), 5)

    pygame.draw.polygon(scr, (128, 0, 0), [[0, 720]] + terrain.points + [[1080, 720]])

    keys = pygame.key.get_pressed()

    if keys[pygame.K_d]:
        player_1.x = player_1.x + player_1.x_speed
    if keys[pygame.K_a]:
        player_1.x = player_1.x - player_1.x_speed
    if keys[pygame.K_RIGHT]:
        player_2.x = player_2.x + player_2.x_speed
    if keys[pygame.K_LEFT]:
        player_2.x = player_2.x - player_2.x_speed
    if keys[pygame.K_b]:
        player_2.angle -= math.radians(2)
    if keys[pygame.K_m]:
        player_2.angle += math.radians(2)
    if keys[pygame.K_q]:
        player_1.angle -= math.radians(2)
    if keys[pygame.K_e]:
        player_1.angle += math.radians(2)

    player_1.x = max(0, min(1050, player_1.x))
    player_2.x = max(0, min(1050, player_2.x))

    player_1.update()
    player_2.update()

    player_1.y = min(player_1.y, terrain.points[[y[0] for y in terrain.points].index(player_1.x // 2 * 2)][1] - 30)
    player_2.y = min(player_2.y, terrain.points[[y[0] for y in terrain.points].index(player_2.x // 2 * 2)][1] - 30)

    player_1.angle = max(-math.pi, min(0, player_1.angle))
    player_2.angle = max(-math.pi, min(0, player_2.angle))

    player_1.update_hitbox()
    player_2.update_hitbox()

    if show_hitbox:
        player_1.draw_collide_circle()
        player_2.draw_collide_circle()

    player_1.draw_angle()
    player_2.draw_angle()

    scr.blit(player_1.img, (player_1.x, player_1.y))
    scr.blit(player_2.img, (player_2.x, player_2.y))

    for bullet in bullets:
        bullet.update()
        pygame.draw.circle(scr, (0, 0, 0), (bullet.x + 15, bullet.y + 15), 5)

    collisions = {bullet.id: 0 for bullet in bullets}
    for point in terrain.points:
        point_x, point_y = point
        for bullet in bullets:
            played = False
            if math.sqrt((point_x - bullet.x) ** 2 + (point_y - bullet.y) ** 2) <= 15:
                if not played:
                    boom.play()
                    played = True
                for i, point_1 in enumerate(terrain.points):
                    point_x_1, point_y_1 = point_1
                    if math.sqrt((point_x - point_x_1) ** 2 + (point_y - point_y_1) ** 2) <= 30:
                        terrain.points[i][1] += abs(math.atan2(point_y - bullet.y, point_x - bullet.x))
                        collisions[bullet.id] += 1
                        total_score += abs(math.atan2(point_y - bullet.y, point_x - bullet.x))

    new_bullets = []
    for bullet in bullets:
        if collisions[bullet.id] < 100:
            new_bullets.append(bullet)

    bullets = new_bullets

    for bullet in bullets:
        if math.sqrt((player_1.x - bullet.x) ** 2 + (player_1.y - bullet.y) ** 2) <= 30 and bullet.sent_from == 2:
            scr.fill((0, 0, 0))
            scr.blit(pygame.font.SysFont(None, 100).render("player 1 lost", True, (255, 255, 255)), (0, 0))
            pygame.display.update()
            time.sleep(3)
            quit()
        if math.sqrt((player_2.x - bullet.x) ** 2 + (player_2.y - bullet.y) ** 2) <= 30 and bullet.sent_from == 1:
            scr.fill((0, 0, 0))
            scr.blit(pygame.font.SysFont(None, 100).render("player 2 lost", True, (255, 255, 255)), (0, 0))
            pygame.display.update()
            time.sleep(3)
            quit()

    scr.blit(pygame.font.SysFont(None, 32).render("Score: " + str(round(total_score / 10)), True, (0, 0, 0)), (20, 20))

    pygame.display.update()
    clock.tick(60)

total_score = round(total_score / 10)

# The variable "total_score" is what has the score, it should be returned at the end to add to their XP
