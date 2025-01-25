from utils import terminate
import pygame as pg
from pygame.locals import *
from Field import Field

FALL_INTERVAL = 0.4  # Интервал между обновлением поля в секундах
WIDTH, HEIGHT = SIZE = 960, 720
FPS = 25  # Кадры в секунду


def start_game():
    points = 0  # Очки
    f = Field()
    FALLEVENT = pg.USEREVENT + 1
    pg.time.set_timer(FALLEVENT, int(FALL_INTERVAL * 1000))
    f.board = [[2, 0] * 5] + [[0] * 10 for _ in range(14)]
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            if event.type == FALLEVENT:
                f.update()
        pg.display.flip()
        falling_left = False  # Двигается ли влево
        falling_right = False  # Двигается ли вправо
        pg.time.Clock().tick(FPS)


def main():
    pg.init()
    screen = pg.display.set_mode(SIZE)
    start_game()


if __name__ == '__main__':
    main()
