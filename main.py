from pprint import pp

import sqlite3

import pygame as pg
import pygame_menu

from Tetris import Tetris
from utils import terminate, load_image

# Параметры экрана
WIDTH, HEIGHT = SIZE = 960, 720
B_WIDTH, B_HEIGHT = B_SIZE = 10, 15
FPS = 25  # Кадры в секунду
TIME_FALL = 0.7  # Интервал между обновлением таблицы в секундах
TIME_SHIFT = 0.4  # Интервал между сдвигами фигуры в сторону
SCORE = 999


# холст для таблицы
width_ts = int(min(WIDTH, HEIGHT) * 0.6)
height_ts = int(min(WIDTH, HEIGHT) * 0.9)
surface_game = pg.Surface((width_ts, height_ts))
surface_game.fill('Black')

def start_game():
    points = 0  # Очки
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
    text = font.render("Tetris", True, ('Green'))
    text_x = 490 - text.get_width() // 2
    text_y = 100 - text.get_height() // 2
    screen.blit(text, (text_x, text_y))

def score_screen(screen):  # Окно с выводом ников и очков игроков'
    # Инициализация базы данных внутри функции
    conn = sqlite3.connect("sirtet_score.db")
    cursor = conn.cursor()
    conn.commit()

    # Функция для вставки нового результата в базу данных
    def insert_score(nickname, score):
        cur = conn.cursor()
        cur.execute("INSERT INTO scores (nickname, score) VALUES (?, ?)", (nickname, score))
        conn.commit()

    # Функция для получения топ-10 результатов
    def get_top_scores():
        cur = conn.cursor()
        cur.execute("SELECT nickname, score FROM scores ORDER BY score DESC LIMIT 10")
        return cur.fetchall()

    # Переменная для хранения введённого ника
    player_nickname = ""

    # Callback для обновления ника при вводе
    def set_nickname(value):
        nonlocal player_nickname
        player_nickname = value.strip()

    # Функция, которая запускается после ввода ника
    def start_game():
        nonlocal player_nickname
        if player_nickname == "":
            return  # Если ник не введён, ничего не делаем

        # Генерируем случайное количество очков
        insert_score(player_nickname, SCORE)

        # Получаем топ-10 результатов
        top_scores = get_top_scores()

        # Меню для отображения таблицы лидеров
        leaderboard_menu = pygame_menu.Menu("Таблица лидеров", screen.get_width(), screen.get_height(),
                                            theme=pygame_menu.themes.THEME_DARK)
        leaderboard_menu.add.label("ТОП 10", font_size=40)
        leaderboard_menu.add.vertical_margin(20)

        for index, (nickname, score_val) in enumerate(top_scores, start=1):
            leaderboard_menu.add.label(f"{index}. {nickname} - {score_val}", font_size=30)

        leaderboard_menu.add.vertical_margin(30)
        leaderboard_menu.add.button("Выход", pygame_menu.events.EXIT)
        leaderboard_menu.mainloop(screen)

    # Главное меню для запроса ника игрока
    menu = pygame_menu.Menu("Введите Ник", screen.get_width(), screen.get_height(), theme=pygame_menu.themes.THEME_DARK)
    menu.add.text_input("Ник: ", default="", onchange=set_nickname)
    menu.add.button("Отправить", start_game)
    menu.add.button("Выход", pygame_menu.events.EXIT)
    menu.mainloop(screen)

    conn.close()

def main():
    global screen
    pg.init()
    screen = pg.display.set_mode(SIZE)
    start_game()
    score_screen(screen)

if __name__ == '__main__':
    main()