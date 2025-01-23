from utils import terminate
import pygame as pg
import time
from pygame.locals import *
from Field import Field

WIDTH, HEIGHT = SIZE = 960, 720
FPS = 25  # Кадры в секунду
block, zone_h, zone_w = 20, 20, 10  # к block привязываются остальные параметры игрового поля(zone_h, zone_w)
side_freq, down_freq = 0.15, 0.1  # скорость с которой поворачиваются и падает фигура
side_margin = int((WIDTH - zone_w * block) / 2)  # Константа. Определяет дистанцию между правой и левой сторонами окна
top_margin = WIDTH - (zone_h * block) - 5  # Другая константа. Определяет дистанцию между верхом и низом сторонами окна


def start_game():
    points = 0  # Очки
    f = Field()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
        pg.display.flip()
        last_move_down = time.time()  # Последнее движение вниз
        last_side_move = time.time()  # Последнее движение в сторону
        last_one = time.time()  # Последняя падавшая фигура
        falling_down = False  # Падает ли сейчас
        falling_left = False  # Двигается ли влево
        falling_right = False  # Двигается ли вправо
        pg.time.Clock().tick(FPS)


def main():
    pg.init()
    screen = pg.display.set_mode(SIZE)
    start_game()


if __name__ == '__main__':
    main()
