from utils import terminate
import pygame as pg
from pygame.locals import *
from Field import Field

WIDTH, HEIGHT = SIZE = 960, 720
FPS = 25  # Кадры в секунду

from pprint import pprint
import time
def start_game():
    points = 0  # Очки
    f = Field()
    f.board = [[2, 0] * 5] + [[0] * 10 for _ in range(14)]

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
        pg.display.flip()
        falling_left = False  # Двигается ли влево
        falling_right = False  # Двигается ли вправо
        pprint(f.board)
        f.update()
        time.sleep(1)
        pg.time.Clock().tick(FPS)


def main():
    pg.init()
    screen = pg.display.set_mode(SIZE)
    start_game()


if __name__ == '__main__':
    main()
