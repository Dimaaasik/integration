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


WIN_IMG = flatten(pygame.image.load("asets/win.png"), 0.85)



RED_CAR = flatten(pygame.image.load("asets/red-car.png"), 0.15)

print(RED_CAR)
print(TRACK.get_height())

HEIGHT = TRACK.get_height()
WIDTH = TRACK.get_width()


MAIN_FONT = pygame.font.SysFont("comicsans", 41)



WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test Game")


FPS = 90


class GameBar:

    TIME = [3000, 1500, 1200, 1000, 950]
    SPEED = [4, 5 , 6 ,7, 8]
    ROTATION = [6, 7, 7, 7, 7]

    LEVELS = 4

    def __init__(self, level = 0):
        self.level = level
        self.speed = self.SPEED[level]
        self.rotation = self.ROTATION[level]
        self.statrted = False
        self.counter = self.TIME[level]
    def next_level(self):
        '''
        Change level, when car cross finish line.
        '''
        self.level += 1
        if self.level > self.LEVELS:
            game_bar.game_finished()
        else:
            self.statrted = True
            self.counter = self.TIME[self.level]
            player_car.configuration(self.level)
            player_car.start_position()
    def select_level(self, level:int):
        '''
        Give opportunity player select level in menu.
        :param level: int
        '''
        self.level = level
        player_car.configuration(level)
        game_bar.start()

    def reset(self):
        '''
        Reset levels.
        '''
        self.level = 0
        self.statrted = False

    def reset_level(self):
        '''
        Reset counter, used when car collide track border.
        '''
        self.counter = self.TIME[self.level]

    def game_finished(self):
        '''
        End game when car passed all levels.
        '''
        WIN.blit(WIN_IMG, (0, 0))
        pygame.display.update()
        pygame.quit()
        return self.level > self.LEVELS

    def start(self):
        '''
        Start current level.
        '''
        self.statrted = True
        self.counter = self.TIME[self.level]





class Car:


    IMG = RED_CAR

    START_POS = (160, 180)
    #START_POS = (160, 300) # Cheat ^^
    def __init__(self, max_speed:float, rotation_speed:float):
        self.img = self.IMG
        self.max_speed = max_speed
        self.vel = 0
        self.rotation_speed = rotation_speed
        self.angle = 0
        self.x , self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self, left: bool =False, right: bool =False):
        '''
        Rotate car rectangle.
        :param left: Bool parameter which give direction on which car will be rotatating
        :param right: Bool parameter which give direction on which car will be rotatating
        '''
        if left:
            self.angle += self.rotation_speed
        elif right:
            self.angle -= self.rotation_speed

    def draw(self, win):
        '''
        Draw car image.
        :param win: Surface of game area
        :param win: Surface of game area
        :return:
        '''
        blit_rorate_center(win, self.img, (self.x, self.y), self.angle)

    def move(self):
        '''
        Car moving.
        '''
        self.vel = min(self.vel + self.acceleration, self.max_speed)
        self.vrum()

    def move_back(self):
        '''
        Car moving back.
        '''
        self.vel = max(self.vel - self.acceleration, -2)
        self.vrum()

    def vrum(self):
        '''
        Car rotating while moving.
        '''
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.x -= horizontal
        self.y -= vertical

    def reduce_speed(self):
        '''
        Reduce speed when player don't push W.
        '''
        if self.vel >= 0:
            self.vel = max(self.vel - self.acceleration / 2, 0)
        else:
            self.vel = min(self.vel + self.acceleration / 2 , 0 )
        self.vrum()

    def collide(self, mask, x = 0, y = 0):
        '''
        Handle colliding player's car and track.
        :param mask: mask of the track
        :return: colliding result
        '''
        car_mask = pygame.mask.from_surface(self.img)
        offset = ( int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        '''
        Change  car speed, angle, level, position on start value.
        '''
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0
        game_bar.reset_level()

    def start_position(self):
        '''
        Change  car speed, angle, position on start value.
        '''
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0
    def configuration(self, level:int):
        '''
        Changing car speed, car rotation speed, counter on current level values.
        '''
        self.max_speed = game_bar.SPEED[level]
        self.rotation_speed = game_bar.ROTATION[level]
        self.counter = game_bar.TIME[level]

def pictures(imageges, win, player_car):
    '''
    Display images array.
    :param imageges: Array of background images.
    :param win: Surface of game area
    :param player_car:
    :return:
    '''
    for img, pos in imageges:
        win.blit(img, pos)

    level_text = MAIN_FONT.render(f"Level {game_bar.level + 1}", 1, (230, 230, 230))
    win.blit(level_text, (10, HEIGHT - level_text.get_height() - 80))

    time_text = MAIN_FONT.render(f"Time {game_bar.counter}", 1, (230, 230, 230))
    win.blit(time_text, (10, HEIGHT - level_text.get_height() - 40))

    speed_text = MAIN_FONT.render(f"Speed {round(player_car.vel, 1)} p/x", 1, (230, 230, 230))
    win.blit(speed_text, (10, HEIGHT - level_text.get_height()))

    player_car.draw(win)
    pygame.display.update()


run = True
clock = pygame.time.Clock()
img_disk = [(GRASS, (0, 0)), (TRACK, (0, 0)), (FINISH, (FINISH_POSITION)), (TRACK_BORDER, ( 0, 0))]


player_car = Car( 4 , 6) # Car initialization
game_bar = GameBar()


while run:

    keys = pygame.key.get_pressed()
    clock.tick(FPS)

    while not game_bar.statrted:
        keys = pygame.key.get_pressed()
        blit_text_center(WIN, MAIN_FONT, "Press key from 1 - 5  to select level" )
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                break

            if keys[pygame.K_1]:
                game_bar.select_level(0)
            elif keys[pygame.K_2]:
                game_bar.select_level(1)
            elif keys[pygame.K_3]:
                game_bar.select_level(2)
            elif keys[pygame.K_4]:
                game_bar.select_level(3)
            elif keys[pygame.K_5]:
                game_bar.select_level(4)

        # realization background changing and skin car changing
    game_bar.counter -= 1

    if not game_bar.counter:
        game_bar.counter = 3000
        player_car.reset()

    pictures(img_disk, WIN, player_car)
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

    finish_poi_collide = player_car.collide(FINISH_MASK, *FINISH_POSITION)
    if finish_poi_collide is not None:
        if finish_poi_collide[1] == 0:

            player_car.reset()
            print('WRONG DIRRECTION')

        else:
            if  (game_bar.level < game_bar.LEVELS):
                game_bar.next_level()
            else:
                game_bar.game_finished()


pygame.quit()