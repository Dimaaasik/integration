# Лабораторна робота 1 ,Branch Nochovca
import pygame
import math
from static import flatten , blit_rorate_center, blit_text_center
pygame.font.init()


GRASS = flatten(pygame.image.load("asets/grass.jpg"), 0.37)
TRACK = flatten(pygame.image.load("asets/track.png"), 0.9)

TRACK_BORDER = flatten(pygame.image.load("asets/track-border.png"), 0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
FINISH = pygame.image.load("asets/finish.png")
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (138, 240)



RED_CAR = flatten(pygame.image.load("asets/red-car.png"), 0.15)

HEIGHT = TRACK.get_height()
WIDTH = TRACK.get_width()   # Получение ширины и высоты из параметров трека т.к. они являются оптимальными для проекта и позволяют избегать искажений

MAIN_FONT = pygame.font.SysFont("comicsans", 41)



WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test Game")


FPS = 90


class GameBar:

    TIME = [3000, 1000, 950, 900, 870]
    SPEED = [4, 5 , 6 ,7, 8]
    ROTATION = [6, 7, 7, 7, 7]

    LEVELS = 5

    def __init__(self, level = 0):
        self.level = level
        self.speed = self.SPEED[level]
        self.rotation = self.ROTATION[level]
        self.statrted = False

    def next_level(self):
        self.level += 1
        self.statrted = False

    def select_level(self, level):
        self.level = level
        game_bar.start()

    def reset(self):
        self.level = 0
        self.statrted = False

    def game_finished(self):
        return self.level > self.LEVELS

    def start(self):
        self.statrted = True
        self.time = self.TIME[self.level]
        print(self.level)
        print(self.time)
        print(self.speed)
        print(self.rotation)



# Тут начинаются изменения , поскольку не планируются боты => класс не является абстрактным и будет использоваться для одной машины
class Car:


    IMG = RED_CAR # Поскольку задумка изменена и машина будет только одна я добавил передачу прямо в классе , !!!! Можно улучшить читабельность перед здачей если закинуть в инит
    START_POS = (160, 180) # так, же можно передать сразу, являются индивидуальными для класса
    def __init__(self, max_speed, rotation_speed):
        self.img = self.IMG
        self.max_speed = max_speed
        self.vel = 0
        self.rotation_speed = rotation_speed
        self.angle = 0
        self.x , self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self, left = False, right = False):
        if left:
            self.angle += self.rotation_speed
        elif right:
            self.angle -= self.rotation_speed

    def draw(self, win):
        blit_rorate_center(win, self.img, (self.x, self.y), self.angle)

    def move(self):
        self.vel = min(self.vel + self.acceleration, self.max_speed)
        self.vrum()

    def move_back(self):
        self.vel = max(self.vel - self.acceleration, -2)
        self.vrum()

    def vrum(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.x -= horizontal
        self.y -= vertical

    def reduce_speed(self):
        if self.vel >= 0:
            self.vel = max(self.vel - self.acceleration / 2, 0)
        else:
            self.vel = min(self.vel + self.acceleration / 2 , 0 )
        self.vrum()

    def collide(self, mask, x = 0, y = 0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = ( int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0

def pictures(imageges, win, player_car):
    for img, pos in imageges:
        win.blit(img, pos)

    player_car.draw(win)
    pygame.display.update()


run = True
clock = pygame.time.Clock()
img_disk = [(GRASS, (0, 0)), (TRACK, (0, 0)), (FINISH, (FINISH_POSITION)), (TRACK_BORDER, ( 0, 0))]


player_car = Car( 4 , 6) # Инициализация машинки , тут задаются основные параметры
game_bar = GameBar()

# counter = 3000

while run:
    # for e in pygame.event.get():
    #
    #     if e.type == pygame.QUIT:
    #         run = False

    # counter -= 1
    # if (counter % 10) == 0:
    #     print(counter)
    # if not counter:
    #     counter = 3000
    #     player_car.reset()
    keys = pygame.key.get_pressed()
    clock.tick(FPS)
    pictures(img_disk, WIN, player_car)

    while not game_bar.statrted:
        keys = pygame.key.get_pressed()
        blit_text_center(WIN, MAIN_FONT, "Press key from 1 - 5  to select level" )
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                break
            # if event.type == pygame.KEYDOWN:
            #     game_bar.start()

            if keys[pygame.K_1]:
                game_bar.select_level(0)
                player_car.max_speed = game_bar.SPEED[0]
            elif keys[pygame.K_2]:
                game_bar.select_level(1)
                player_car.max_speed = game_bar.SPEED[1]
            elif keys[pygame.K_3]:
                game_bar.select_level(2)
                player_car.max_speed = game_bar.SPEED[2]
            elif keys[pygame.K_4]:
                game_bar.select_level(3)
                player_car.max_speed = game_bar.SPEED[3]
            elif keys[pygame.K_5]:
                game_bar.select_level(4)
                player_car.max_speed = game_bar.SPEED[4]

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break



    moved = False
    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_back()

    if not moved:
        player_car.reduce_speed()

    if player_car.collide(TRACK_BORDER_MASK) is not None:
        player_car.reset()
        counter = 3000

    finish_poi_collide = player_car.collide(FINISH_MASK, *FINISH_POSITION)
    if finish_poi_collide is not None:
        if finish_poi_collide[1] == 0:
            player_car.reset()
            print('WRONG DIRRECTION')
            counter = 3000

        else:
            print('WIN!!')
            run = False
pygame.quit()