from pprint import pp

import pygame as pg

from Tetris import Tetris
from utils import terminate, load_image

# Параметры экрана
WIDTH, HEIGHT = SIZE = 960, 720
B_WIDTH, B_HEIGHT = B_SIZE = 10, 15
FPS = 25  # Кадры в секунду
TIME_FALL = 0.7  # Интервал между обновлением таблицы в секундах
TIME_SHIFT = 0.4  # Интервал между сдвигами фигуры в сторону



# холст для таблицы
width_ts = int(min(WIDTH, HEIGHT) * 0.6)
height_ts = int(min(WIDTH, HEIGHT) * 0.9)
surface_game = pg.Surface((width_ts, height_ts))
surface_game.fill('Black')

def start_game():
    t = Tetris((B_WIDTH, B_HEIGHT))
    EVENT_FALL = pg.USEREVENT + 1  # Создание событий и постановка таймера их обновления
    pg.time.set_timer(EVENT_FALL, int(TIME_FALL * 1000))
    EVENT_SHIFT = pg.USEREVENT + 2
    pg.time.set_timer(EVENT_SHIFT, int(TIME_SHIFT * 1000))

    t.set_view(min(width_ts // B_WIDTH, height_ts // B_HEIGHT))
    im_background = load_image('background.jpg')
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:  # Выход
                terminate()
            if event.type == pg.KEYDOWN:  # Нажатие
                if event.key in [pg.K_LEFT, pg.K_a]:
                    t.field.shift_side -= 1
                elif event.key in [pg.K_RIGHT, pg.K_d]:
                    t.field.shift_side += 1
                elif event.key in [pg.K_UP, pg.K_w]:
                    t.field.figure_rotate()
            if event.type == pg.KEYUP:  # Отпускание
                if event.key in [pg.K_LEFT, pg.K_a]:
                    t.field.shift_side += 1
                elif event.key in [pg.K_RIGHT, pg.K_d]:
                    t.field.shift_side -= 1
            if event.type == EVENT_SHIFT:
                t.field.figure_shift()
            if event.type == EVENT_FALL:  # Периодическое падение блоков
                t.field.update()
                if t.field.over:
                    break

                print(t.field.figure_center, t.field.cur_figure_turn, t.field.points)
                pp(t.field.board_fixed)  # Отображение таблицы в консоли(ТЕСТ) TODO Убрать тест

            screen.blit(im_background, (-25, 0))
            render_game_name()
            screen.blit(surface_game, (0, 0))
            t.render(surface_game)
            pg.display.flip()
            pg.time.Clock().tick(FPS)




def render_game_name():    # Название Игры
    font = pg.font.Font(None, 50)
    text = font.render("Tetris", True, 'Green')
    text_x = 490 - text.get_width() // 2
    text_y = 100 - text.get_height() // 2
    screen.blit(text, (text_x, text_y))


def main():
    global screen
    global points
    points = 0
    pg.init()
    screen = pg.display.set_mode(SIZE)
    start_game()


if __name__ == '__main__':
    main()
