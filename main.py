from pprint import pp

import pygame as pg
from Field import Field
from utils import terminate
from utils import load_image

# Параметры экрана
WIDTH, HEIGHT = SIZE = 960, 720
B_WIDTH, B_HEIGHT = B_SIZE = 10, 15
FPS = 25  # Кадры в секунду
TIME_FALL = 0.7  # Интервал между обновлением таблицы в секундах
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# холст для таблицы
width_ts = int(min(WIDTH, HEIGHT) * 0.6)
height_ts = int(min(WIDTH, HEIGHT) * 0.9)
print(width_ts, height_ts)
surface_game = pg.Surface((width_ts, height_ts))
surface_game.fill('Black')


def start_game():
    points = 0  # Очки
    f = Field()
    b = Board(B_WIDTH, B_HEIGHT)
    b.set_view(min(width_ts // B_WIDTH, height_ts // B_HEIGHT))
    print(WIDTH // B_WIDTH)
    FALLEVENT = pg.USEREVENT + 1
    pg.time.set_timer(FALLEVENT, int(TIME_FALL * 1000))
    im_background = load_image('background.jpg')
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
        screen.blit(im_background, (-25, 0))
        render_game_name(screen)
        screen.blit(surface_game, (0, 0))
        b.render(surface_game)
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


def render_game_name(screen):    # Название Игры
    font = pg.font.Font(None, 50)
    text = font.render("Tetris", True, ('Green'))
    text_x = 490 - text.get_width() // 2
    text_y = 100 - text.get_height() // 2
    screen.blit(text, (text_x, text_y))


def main():
    global screen
    pg.init()
    screen = pg.display.set_mode(SIZE)
    start_game()


if __name__ == '__main__':
    main()
