# Лабораторна робота 1 ,Branch Nochovca
import pygame
import math
import time
from static import flatten

GRASS = flatten(pygame.image.load("asets/grass.jpg"), 2.5)
TRACK = flatten(pygame.image.load("asets/track.png"), 0.9)

TRACK_BORDER = flatten(pygame.image.load("asets/track-border.png"), 0.9)
FINISH = flatten(pygame.image.load("asets/finish.png"), 0.82)

RED_CAR = flatten(pygame.image.load("asets/red-car.png"), 0.4)
WHITE_CAR = flatten(pygame.image.load("asets/white-car.png"), 0.4)

HEIGHT = TRACK.get_height()
WIDTH = TRACK.get_width()   # Получение ширины и высоты из параметров трека т.к. они являются оптимальными для проекта и позволяют избегать искажений

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test Game")
FPS = 90



run = True
clock = pygame.time.Clock()

while run:
    clock.tick(FPS)

    WIN.blit(GRASS, (0, 0))
    WIN.blit(TRACK, (0, 0))
    WIN.blit(FINISH, (138, 300))
    #WIN.blit(RED_CAR, (150, 300))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break


pygame.quit()