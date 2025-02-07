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
WHITE = (255, 255, 255)

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
            score(im_background, points)
            next_tetromino(im_background, None)  # Вместо None, вставляем переменную, в которой хранится фигура
            screen.blit(surface_game, (0, 0))
            t.render(surface_game)
            pg.display.flip()
            pg.time.Clock().tick(FPS)


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_cell(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        cell_x = (mouse_x - self.left) // self.cell_size
        cell_y = (mouse_y - self.top) // self.cell_size
        if 0 <= cell_x < self.width and 0 <= cell_y < self.height:
            return cell_x, cell_y
        return None

    def on_click(self, cell_coords):
        x, y = cell_coords
        self.board[y][x] = not self.board[y][x]

    def get_click(self, mouse_pos):
        if self.get_cell(mouse_pos):
            self.on_click(self.get_cell(mouse_pos))


    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 0:
                    pygame.draw.rect(screen, WHITE,
                                     (self.left + self.cell_size * x,
                                      self.top + self.cell_size * y,
                                      self.cell_size, self.cell_size), 1)
                elif self.board[y][x] == 1:
                    pygame.draw.rect(screen, WHITE,
                                     (self.left + self.cell_size * x,
                                      self.top + self.cell_size * y,
                                      self.cell_size, self.cell_size))


def render_game_name():    # Название Игры
    font = pg.font.Font(None, 50)
    text = font.render("Tetris", True, ('Green'))
    text_x = 490 - text.get_width() // 2
    text_y = 50 - text.get_height() // 2
    screen.blit(text, (text_x, text_y))


def score(surface_static, points):    # Счет игры
    font = pg.font.Font(None, 35)
    text = font.render(f"Score: ", True, ('White'))
    text_x = 857 - text.get_width() // 2
    text_y = 50 - text.get_height() // 2
    surface_static.blit(text, (text_x, text_y))


def next_tetromino(surface_static, name_picture_tetromino):    # Следующая фигура
    font = pg.font.Font(None, 35)
    text = font.render(f"Next: {name_picture_tetromino}", True, ('White'))
    text_x = 857 - text.get_width() // 2
    text_y = 650 - text.get_height() // 2
    surface_static.blit(text, (text_x, text_y))


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


def start_menu():
    menu = pygame_menu.Menu('Сыграй в нашу игру!', WIDTH, HEIGHT,
                            theme=pygame_menu.themes.THEME_DARK)

    menu.add.button('Играть', start_game)
    menu.add.button('Выход', pygame_menu.events.EXIT)
    menu.mainloop(screen)


def main():
    global screen
    pg.init()
    screen = pg.display.set_mode(SIZE)
    start_menu()
    score_screen(screen)


if __name__ == '__main__':
    main()