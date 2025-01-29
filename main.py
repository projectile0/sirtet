from pprint import pp

import pygame as pg
import pygame
from Field import Field
from utils import terminate

WIDTH, HEIGHT = SIZE = 960, 720
FPS = 25  # Кадры в секунду
TIME_FALL = 0.7  # Интервал между обновлением таблицы в секундах
WHITE = (255, 255, 255)

# холст для таблицы
width_ts = 400
height_ts = 500
test_table = pygame.Surface((width_ts, height_ts))
test_table.fill('White')


def start_game(screen):
    points = 0  # Очки
    f = Field()
    b = Board(10, 17)
    b.set_view(10, 10, 20)
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
                pp(f.board)  # Отображение таблицы в консоли(ТЕСТ)
        screen.blit(test_table, (300, 150))
        b.render(screen)
        pg.display.flip()
        pg.time.Clock().tick(FPS)


class Board:    # Таблица
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, WHITE,
                                 (self.left + self.cell_size * x,
                                  self.top + self.cell_size * y,
                                  self.cell_size, self.cell_size), 1)


def main():
    pg.init()
    screen = pg.display.set_mode(SIZE)
    start_game(screen)


if __name__ == '__main__':
    main()
