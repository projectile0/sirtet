from pprint import pp

import pygame as pg
from Field import Field
from utils import terminate
from utils import load_image

# Параметры экрана
WIDTH, HEIGHT = SIZE = 960, 720
FPS = 25  # Кадры в секунду
TIME_FALL = 0.7  # Интервал между обновлением таблицы в секундах
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# холст для таблицы
width_ts = 300
height_ts = 510
test_table = pg.Surface((width_ts, height_ts))
test_table.fill('Black')


def start_game(screen):
    points = 0  # Очки
    f = Field()
    b = Board(10, 17)
    b.set_view(30)
    FALLEVENT = pg.USEREVENT + 1
    pg.time.set_timer(FALLEVENT, int(TIME_FALL * 1000))
    im = load_image('background.jpg')
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
        screen.blit(im, (-25, 0))
        Name_game(screen)
        screen.blit(test_table, (346, 150))
        b.render(test_table)
        pg.display.flip()
        pg.time.Clock().tick(FPS)


class Board:    # Таблица
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.cell_size = 30

    # Параметры
    def set_view(self, cell_size):
        self.cell_size = cell_size

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pg.draw.rect(screen, WHITE,
                                 (self.cell_size * x,
                                  self.cell_size * y,
                                  self.cell_size, self.cell_size), 1)


def Name_game(screen):    # Название Игры
    font = pg.font.Font(None, 50)
    text = font.render("Tetris", True, ('Green'))
    text_x = 490 - text.get_width() // 2
    text_y = 100 - text.get_height() // 2
    screen.blit(text, (text_x, text_y))


def main():
    global screen
    pg.init()
    screen = pg.display.set_mode(SIZE)
    start_game(screen)


if __name__ == '__main__':
    main()
