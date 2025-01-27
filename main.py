from utils import terminate
import pygame as pg
from pygame.locals import *
from Field import Field
from pprint import pp
FALL_INTERVAL = 0.7  # Интервал между обновлением поля в секундах
WIDTH, HEIGHT = SIZE = 960, 720
FPS = 25  # Кадры в секунду

def start_game(screen):
    points = 0  # Очки
    f = Field()
    FALLEVENT = pg.USEREVENT + 1
    pg.time.set_timer(FALLEVENT, int(FALL_INTERVAL * 1000))
    f.board = [[2, 1] * 5] + [[0] * 10 for _ in range(7)] + [[1, 1] * 5] + [[0] * 10 for _ in range(6)]
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            if event.type == FALLEVENT:
                f.update()
                pp(f.board)
        pg.display.flip()
        pg.time.Clock().tick(FPS)


def main():
    pg.init()
    screen = pg.display.set_mode(SIZE)
    start_game(screen)


if __name__ == '__main__':
    main()
