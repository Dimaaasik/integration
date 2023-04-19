# Лабораторна робота 1 ,Branch Nochovca
import pygame
import math
import time
from static import flatten , blit_rorate_center

GRASS = flatten(pygame.image.load("asets/grass.jpg"), 2.5)
TRACK = flatten(pygame.image.load("asets/track.png"), 0.9)

TRACK_BORDER = flatten(pygame.image.load("asets/track-border.png"), 0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

FINISH = flatten(pygame.image.load("asets/finish.png"), 0.82)

RED_CAR = flatten(pygame.image.load("asets/red-car.png"), 0.4)
WHITE_CAR = flatten(pygame.image.load("asets/white-car.png"), 0.4)

HEIGHT = TRACK.get_height()
WIDTH = TRACK.get_width()   # Получение ширины и высоты из параметров трека т.к. они являются оптимальными для проекта и позволяют избегать искажений

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test Game")



FPS = 90

# Тут начинаются изменения , поскольку не планируются боты => класс не является абстрактным и будет использоваться для одной машины
class Car:

    IMG = RED_CAR # Поскольку задумка изменена и машина будет только одна я добавил передачу прямо в классе , !!!! Можно улучшить читабельность перед здачей если закинуть в инит
    START_POS = (180, 200) # так, же можно передать сразу, являются индивидуальными для класса
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
img_disk = [(GRASS, (0, 0)), (TRACK, (0, 0)), (FINISH, (138, 240))]
player_car = Car( 4 , 6)


while run:
    clock.tick(FPS)
    pictures(img_disk, WIN, player_car)

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    keys = pygame.key.get_pressed()

    moved = False
    if keys[pygame.K_a]:
        player_car.rotate(left= True)
    if keys[pygame.K_d]:
        player_car.rotate(right= True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_back()

    if not moved:
        player_car.reduce_speed()

    if player_car.collide(TRACK_BORDER_MASK) != None:
        print("Car.START_POS[0]")
        player_car.reset()
pygame.quit()