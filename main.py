from pprint import pp

import sqlite3

import pygame as pg
import pygame_menu

from Field import Field
from utils import terminate

WIDTH, HEIGHT = SIZE = 960, 720
FPS = 25  # Кадры в секунду
FALL_INTERVAL = 0.7  # Интервал между обновлением поля в секундах


def start_game(screen):
    points = 0  # Очки
    f = Field()
    FALLEVENT = pg.USEREVENT + 1
    pg.time.set_timer(FALLEVENT, int(FALL_INTERVAL * 1000))
    screen.fill((255, 255, 255))
    score_displayed = False  # Расположен ли экран с очками или нет
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            if event.type == FALLEVENT:
                f.update()
                pp(f.board)  # Отображение таблицы в консоли(ТЕСТ)
            if event.type == pg.MOUSEBUTTONUP:
                score_screen(screen)

        pg.display.flip()
        pg.time.Clock().tick(FPS)


def score_screen(screen):  # Окно с выводом ников и очков игроков
    conn = sqlite3.connect('sirtet_score.db')  # Подключение бд
    cursor = conn.cursor()  # Создание курсора
    cursor.execute("SELECT name, score FROM data ORDER BY score DESC")  # Запрос
    scores = cursor.fetchall()  # возвращение записей
    font = pg.font.Font(None, 36)  # шрифт
    for index, (nick, score) in enumerate(scores):  # цикл для вывода
        text = f"{nick}: {score}"  # Форма текста и сам текст
        text_surface = font.render(text, True, (0, 0, 0))  # Вид текста
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + index * 40))  # Позиция текста(центр)
        screen.blit(text_surface, text_rect)  # Вывод текста на экран
    conn.close()  # Закрытие связи
    pg.display.flip()
    waiting = True
    while waiting:  # Цикл в ожидании нажатия
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            if event.type == pg.KEYDOWN:
                waiting = False


def main():
    pg.init()
    screen = pg.display.set_mode(SIZE)
    start_game(screen)
    score_screen(screen)


if __name__ == '__main__':
    main()
