import sqlite3
from pprint import pp

import pygame as pg
import pygame.display
import pygame_menu

from Tetris import Tetris
from database import *
from utils import terminate, load_image, COLOR_TEXT, COLOR_BACKGROUND

FONT_NAME = pygame_menu.font.FONT_MUNRO
# Параметры экрана
WIDTH, HEIGHT = SIZE = 960, 720
B_WIDTH, B_HEIGHT = B_SIZE = 10, 15
FPS = 30  # Кадры в секунду
TIME_FALL = 1.4  # Интервал между обновлением таблицы в секундах
TIME_SHIFT = 0.8  # Интервал между сдвигами фигуры в сторону
WHITE = (255, 255, 255)

# Тема для меню
game_theme = pygame_menu.themes.THEME_DARK.copy()
game_theme.background_color = COLOR_BACKGROUND

# холст для таблицы
width_ts = int(min(WIDTH, HEIGHT) * 0.6)
height_ts = int(min(WIDTH, HEIGHT) * 0.9)

# глобальные переменные
player_nickname = ''  # Переменная для хранения введённого ника
score = 0  # Переменная для очков
screen = None  # Переменная для основного окна
difficulty = 1  # Сложность
EVENT_FALL = pg.USEREVENT + 1  # Создание событий и
EVENT_SHIFT = pg.USEREVENT + 2


def start_game():
    global score
    t = Tetris((B_WIDTH, B_HEIGHT))
    pg.time.set_timer(EVENT_FALL, int(TIME_FALL * 1000 / difficulty))  # Установка таймера вызова искусственных событий
    pg.time.set_timer(EVENT_SHIFT, int(TIME_SHIFT * 1000 / difficulty))

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
                elif event.key in [pg.K_DOWN, pg.K_s]:
                    pg.time.set_timer(EVENT_FALL, int(TIME_FALL * 1000 / difficulty / 2))
            if event.type == pg.KEYUP:  # Отпускание
                if event.key in [pg.K_LEFT, pg.K_a]:
                    t.field.shift_side += 1
                elif event.key in [pg.K_RIGHT, pg.K_d]:
                    t.field.shift_side -= 1
                elif event.key in [pg.K_DOWN, pg.K_s]:
                    pg.time.set_timer(EVENT_FALL, int(TIME_FALL * 1000 / difficulty))
            if event.type == EVENT_SHIFT:
                t.field.figure_shift()
            if event.type == EVENT_FALL:  # Периодическое падение блоков
                t.field.update()
                score = t.field.score * difficulty
                if t.field.over:
                    break

        if not t.field.over:
            screen.blit(static_surface, (0, 0))
            render_score()
            t.render(surface_game)
            surface_flipped_game = pg.transform.flip(surface_game, False, True)
            screen.blit(surface_flipped_game, (WIDTH * 0.1, HEIGHT * 0.05))
            pg.display.flip()
            pg.time.Clock().tick(FPS)
        else: # при поражении
            pg.time.set_timer(EVENT_FALL, 0)  # Остановка воспроизводства событий
            pg.time.set_timer(EVENT_SHIFT, 0)
            out = 0
            render_text_gameover()
            pg.display.flip()
            while True:
                for event in pg.event.get():
                    if event.type == pg.QUIT:  # Выход
                        terminate()
                    if event.type == pg.KEYDOWN:
                        out = 1
                        break
                if out:
                    break
                pg.time.Clock().tick(FPS)
            score_screen()
            break





def render_static_surface():
    surf = load_image('background.jpg')
    surf = pg.transform.scale(surf, (WIDTH, HEIGHT))
    render_game_name(surf)
    return surf

def render_text_gameover():
    surf = pg.Surface((WIDTH, HEIGHT // 4))
    surf.fill(COLOR_BACKGROUND)

    font = pg.font.Font(FONT_NAME, int(min(WIDTH, HEIGHT) * 0.2))
    text = font.render('GAME OVER', True, COLOR_TEXT)
    surf.blit(text, (WIDTH * 0.2, HEIGHT // 25))

    font = pg.font.Font(FONT_NAME, int(min(WIDTH, HEIGHT) * 0.05))
    text = font.render('Press any button', True, COLOR_TEXT)
    surf.blit(text, (WIDTH * 0.35, HEIGHT // 64 * 13))

    screen.blit(surf, (0, HEIGHT // 5 * 2))


def render_score():  # Отрисовка количества очков
    font = pg.font.Font(FONT_NAME, 140)
    text = font.render(str(score), True, COLOR_TEXT)
    screen.blit(text, (WIDTH * 0.6, HEIGHT * 0.08))


def render_game_name(surface):  # Название Игры
    font = pg.font.Font(FONT_NAME, 140)
    text = font.render('SIRTET', True, COLOR_TEXT)
    surface.blit(text, (WIDTH * 0.6, HEIGHT * 0.8))


def score_screen():  # Меню для запроса ника игрока
    menu = pygame_menu.Menu("Введите Ник", WIDTH, HEIGHT, theme=game_theme)
    menu = pygame_menu.Menu("Введите Ник", WIDTH, HEIGHT, theme=game_theme)
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
                                        theme=game_theme)
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


def set_difficulty(value, difclty):
    global difficulty
    difficulty = difclty
    pass


def start_menu():
    menu = pygame_menu.Menu('Sirtet', WIDTH, HEIGHT,
                            theme=game_theme)

    menu.add.button('Играть', start_game)
    menu.add.selector('Сложность :', [('Easy', 1), ('Normal', 2), ('Hard', 3), ('Extra', 4)], onchange=set_difficulty)
    menu.add.button('Таблица лидеров', view_scoreboard)
    menu.add.button('Выход', pygame_menu.events.EXIT)
    menu.mainloop(screen)


def set_icon():
    icon = load_image('icon.png')
    pygame.display.set_icon(icon)


def main():
    global screen
    global score
    score = 0
    pg.init()
    screen = pg.display.set_mode(SIZE)
    pg.display.set_caption('Sirtet')
    set_icon()
    start_menu()
    score_screen()


if __name__ == '__main__':
    main()
