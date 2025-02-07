import sqlite3
from pprint import pp

import pygame as pg
import pygame_menu

from Tetris import Tetris
from database import *
from utils import terminate, COLOR_BACKGROUND

# Параметры экрана
WIDTH, HEIGHT = SIZE = 960, 720
B_WIDTH, B_HEIGHT = B_SIZE = 10, 15
FPS = 30  # Кадры в секунду
TIME_FALL = 0.7  # Интервал между обновлением таблицы в секундах
TIME_SHIFT = 0.4  # Интервал между сдвигами фигуры в сторону
WHITE = (255, 255, 255)

# холст для таблицы
width_ts = int(min(WIDTH, HEIGHT) * 0.6)
height_ts = int(min(WIDTH, HEIGHT) * 0.9)

player_nickname = ''  # Переменная для хранения введённого ника
score = 0  # Переменная для очков
screen = None  # Переменная для основного окна


def start_game():
    global score
    t = Tetris((B_WIDTH, B_HEIGHT))
    EVENT_FALL = pg.USEREVENT + 1  # Создание событий и постановка таймера их обновления
    pg.time.set_timer(EVENT_FALL, int(TIME_FALL * 1000))
    EVENT_SHIFT = pg.USEREVENT + 2
    pg.time.set_timer(EVENT_SHIFT, int(TIME_SHIFT * 1000))

    t.set_view(min(width_ts // B_WIDTH, height_ts // B_HEIGHT))
    static_surface = render_static_surface()
    surface_game = pg.Surface((width_ts, height_ts))  # surface таблицы тетриса
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
                print(t.field.figure_center, t.field.cur_figure_turn)
                pp(t.field.board_fixed)  # Отображение таблицы в консоли(ТЕСТ) TODO Убрать тест

        if t.field.over:
            score_screen()
            break
        screen.blit(static_surface, (0, 0))
        t.render(surface_game)
        surface_flipped_game = pg.transform.flip(surface_game, False, True)
        screen.blit(surface_flipped_game, (WIDTH * 0.1, HEIGHT * 0.05))
        pg.display.flip()
        pg.time.Clock().tick(FPS)


def render_static_surface():
    surf = pg.Surface((WIDTH, HEIGHT))
    surf.fill(COLOR_BACKGROUND)
    render_game_name(surf)
    render_game_name(surf)
    render_score(surf, score)
    render_next_tetromino(surf, None)  # Вместо None, вставляем переменную, в которой хранится фигура
    return surf


def render_game_name(surface):  # Название Игры
    font = pg.font.Font(None, 50)
    text = font.render("Tetris", True, 'Green')
    text_x = 490 - text.get_width() // 2
    text_y = 50 - text.get_height() // 2
    surface.blit(text, (text_x, text_y))


def render_score(surface, score):  # Счет игры
    font = pg.font.Font(None, 35)
    text = font.render(f"Score: ", True, 'White')
    text_x = 857 - text.get_width() // 2
    text_y = 50 - text.get_height() // 2
    surface.blit(text, (text_x, text_y))


def render_next_tetromino(surface, name_picture_tetromino):  # Следующая фигура
    font = pg.font.Font(None, 35)
    text = font.render(f"Next: {name_picture_tetromino}", True, 'White')
    text_x = 857 - text.get_width() // 2
    text_y = 650 - text.get_height() // 2
    surface.blit(text, (text_x, text_y))


def score_screen():  # Окно с выводом ников и очков игроков
    global conn

    # Меню для запроса ника игрока
    menu = pygame_menu.Menu("Введите Ник", screen.get_width(), screen.get_height(), theme=pygame_menu.themes.THEME_DARK)
    menu.add.text_input("Ник: ", default="", onchange=set_nickname)
    menu.add.button("Отправить", view_scoreboard)
    menu.add.button("Выход", pygame_menu.events.EXIT)
    menu.mainloop(screen)


# Запускается при обновлении ника
def set_nickname(value):
    global player_nickname
    player_nickname = value.strip()


# Функция, которая запускается после ввода ника
def view_scoreboard():
    # Инициализация базы данных внутри функции
    conn = sqlite3.connect('sirtet_score.db')
    cursor = conn.cursor()
    conn.commit()

    if player_nickname:
        # Добавляем набранное количество очков в таблицу
        insert_score(conn, player_nickname, score)

    # Получаем топ-10 результатов
    top_scores = get_top_scores(conn)

    # Меню для отображения таблицы лидеров
    leaderboard_menu = pygame_menu.Menu("Таблица лидеров", WIDTH, HEIGHT,
                                        theme=pygame_menu.themes.THEME_DARK)
    leaderboard_menu.add.label("ТОП 10", font_size=40)
    leaderboard_menu.add.vertical_margin(20)

    for index, (nickname, score_val) in enumerate(top_scores, start=1):
        leaderboard_menu.add.label(f"{index}. {nickname} - {score_val}", font_size=30)

    leaderboard_menu.add.vertical_margin(20)
    leaderboard_menu.add.button("Меню", start_menu)
    leaderboard_menu.add.vertical_margin(30)
    leaderboard_menu.add.button("Выход", pygame_menu.events.EXIT)

    leaderboard_menu.mainloop(screen)

    conn.close()


def start_menu():
    menu = pygame_menu.Menu('Tetris', WIDTH, HEIGHT,
                            theme=pygame_menu.themes.THEME_DARK)

    menu.add.button('Играть', start_game)
    menu.add.button('Таблица лидеров', view_scoreboard)
    menu.add.button('Выход', pygame_menu.events.EXIT)
    menu.mainloop(screen)


def main():
    global screen
    global score
    score = 0
    pg.init()
    screen = pg.display.set_mode(SIZE)
    pg.display.set_caption('Tetris')
    start_menu()
    score_screen()


if __name__ == '__main__':
    main()
