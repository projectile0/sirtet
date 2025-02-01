from pprint import pp

import pygame as pg

from Field import Field
from utils import terminate

WIDTH, HEIGHT = SIZE = 960, 720
FPS = 25  # Кадры в секунду
TIME_FALL = 0.7  # Интервал между обновлением таблицы в секундах


def start_game(screen):
    points = 0  # Очки
    f = Field()
    FALLEVENT = pg.USEREVENT + 1
    pg.time.set_timer(FALLEVENT, int(TIME_FALL * 1000))
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:  # Выход
                terminate()
            if event.type == pg.KEYDOWN:  # Нажатие
                if event.key in [pg.K_LEFT, pg.K_a]:
                    f.shift_side -= 1
                elif event.key in [pg.K_RIGHT, pg.K_d]:
                    f.shift_side += 1
            if event.type == pg.KEYUP:  # Отпускание
                if event.key in [pg.K_LEFT, pg.K_a]:
                    f.shift_side += 1
                elif event.key in [pg.K_RIGHT, pg.K_d]:
                    f.shift_side -= 1
            if event.type == FALLEVENT:  # Периодическое падение блоков
                f.update()
                print(f.figure_center)
                pp(f.board_fixed)  # Отображение таблицы в консоли(ТЕСТ) TODO Убрать тест

        pg.display.flip()
        pg.time.Clock().tick(FPS)


def main():
    pg.init()
    screen = pg.display.set_mode(SIZE)
    start_game(screen)


if __name__ == '__main__':
    main()
