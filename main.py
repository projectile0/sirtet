from pprint import pp

import sqlite3

import pygame as pg
import pygame_menu

from Field import Field
from utils import terminate

WIDTH, HEIGHT = SIZE = 960, 720
FPS = 25  # Кадры в секунду
FALL_INTERVAL = 0.7  # Интервал между обновлением поля в секундах
score = 999

def start_game(screen):
    points = 0  # Очки
    f = Field()
    FALLEVENT = pg.USEREVENT + 1
    pg.time.set_timer(FALLEVENT, int(FALL_INTERVAL * 1000))
    screen.fill((255, 255, 255))
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            if event.type == FALLEVENT:
                f.update()

                pp(f.board)  # Отображение таблицы в консоли(ТЕСТ)

        pg.display.flip()
        pg.time.Clock().tick(FPS)

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
        insert_score(player_nickname, score)

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
    pg.init()
    screen = pg.display.set_mode(SIZE)
    start_game(screen)
    score_screen(screen)

if __name__ == '__main__':
    main()
