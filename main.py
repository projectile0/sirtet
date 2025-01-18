from utils import terminate
import pygame as pg

WIDTH, HEIGHT = SIZE = 960, 720


def start_game():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
        pg.display.flip()


def main():
    pg.init()
    screen = pg.display.set_mode(SIZE)
    start_game()


if __name__ == '__main__':
    main()
