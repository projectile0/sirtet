from random import choice, randint

import pygame as pg

from utils import WHITE


class Tetris:
    def __init__(self, f_size=(10, 15)):
        self.field = Field(f_size) # Создание поля

        # значения по умолчанию
        self.cell_size = 30

    # Параметры
    def set_view(self, cell_size):
        self.cell_size = cell_size

    def render(self, screen):
        for y in range(self.field.height):
            for x in range(self.field.width):
                pg.draw.rect(screen, WHITE,
                             (self.cell_size * x,
                              self.cell_size * y,
                              self.cell_size, self.cell_size), 1)


class Field:  # Класс поля
    shapes = list({
                      'I': [((0, -1), (0, 0), (0, 1), (0, 2)), ((-1, 0), (0, 0), (1, 0), (2, 0))],
                      'J': [((0, -1), (1, -1), (0, 0), (0, 1)), ((-1, 0), (0, 0), (1, 0), (1, 1)),
                            ((0, -1), (0, 0), (-1, 1), (0, 1)), ((-1, -1), (0, 0), (-1, 0), (1, 0))],
                      'L': [((-1, -1), (0, -1), (0, 0), (0, 1)), ((1, 1), (0, 0), (-1, 0), (1, 0)),
                            ((0, -1), (0, 0), (0, 1), (1, 1)), ((-1, 0), (0, 0), (1, 0), (-1, 1))],
                      'O': [((0, 0), (1, 0), (0, 1), (1, 1))],
                      'S': [((0, -1), (0, 0), (1, 0), (1, 1)), ((0, 0), (1, 0), (-1, 1), (0, 1))],
                      'T': [((0, -1), (-1, 0), (0, 0), (1, 0)), ((0, -1), (0, 0), (1, 0), (0, 1)),
                            ((-1, 0), (0, 0), (1, 0), (0, 1)), ((0, -1), (-1, 0), (0, 0), (0, 1))],
                      'Z': [((1, -1), (0, 0), (1, 0), (0, 1)), ((-1, -1), (0, -1), (0, 0), (1, 0))]
                  }.items())  # Координаты относительно центра: (x, y)

    # Названия всех вариантов фигур со всеми вариантами расположения,
    # первым считать вертикальное положение "головой" вверх

    def __init__(self, size):
        self.points = 0  # очки
        self.size = self.width, self.height = size  # размеры
        if self.width < 4 or self.height < 5:  # проверка на слишком маленькие параметры поля
            self.size = self.width, self.height = (10, 15)
        self.board_fixed = self.board_clear()  # Таблица фиксированных блоков
        self.board_show = []  # Таблица для отображения
        self.shift_side = 0  # Сдвиг фигуры на x клеток("-" - влево, "+" - вправо)
        self.figure_center = (0, 0)  # Переменная для сохранения центра фигуры
        self.cur_figure_turn = 0  # Номер варианта поворота фигуры
        self.all_turns = ()  # Запись всех вариантов положения фигуры в виде координат блоков относительно центра

        self.new_figure()  # Появление первой фигуры

    def update(self):  # Следующий кадр
        self.figure_fall()
        return self.check_line()  # Возврат points

    def figure_rotate(self):
        blocks = self.all_turns[(self.cur_figure_turn + 1) % len(self.all_turns)]
        cells_empty = all(set(map(self.empty_block, blocks)))
        if cells_empty:
            self.cur_figure_turn = (self.cur_figure_turn + 1) % len(self.all_turns)

    def figure_shift(self):
        blocks = self.all_turns[self.cur_figure_turn]
        x, y = self.figure_center
        cells_empty = all(set(map(lambda cc: self.empty_block((cc[0] + self.shift_side, cc[1])), blocks)))
        if cells_empty:
            self.figure_center = (x + self.shift_side, y)

    def figure_fall(self):
        blocks = self.all_turns[self.cur_figure_turn]
        x, y = self.figure_center
        cells_empty = all(set(map(lambda cc: self.empty_block((cc[0], cc[1] + 1)), blocks)))
        if cells_empty:  # Проверка на пустоту под блоком
            self.figure_center = (x, y + 1)
            return
        self.fix_board()
        self.new_figure()

    def empty_block(self, coords):  # Проверка на нахождение в таблице и пустоту клетки
        x = coords[0] + self.figure_center[0]
        y = coords[1] + self.figure_center[1]
        if 0 <= y < self.height:
            if 0 <= x < self.width:
                if self.board_fixed[y][x] == 0:
                    return True
        return False

    def check_line(self):
        for y in self.board_fixed:
            if all(y):
                self.board_fixed.remove(y)
                self.board_fixed.insert(0, [0] * self.width)
                self.points += 100

    # empty_block:
    # (0: Клетка не пустая/вне таблицы по координате Y; 1: В таблице, пустая без сдвига; 2: В таблице, пустая клетка)
    # Вход координат относительно центра фигуры

    def new_figure(self):  # Появление новой фигуры
        self.all_turns = choice(self.shapes)[1]  # Выбор новой фигуры, запись положений всех блоков относительно центра
        self.cur_figure_turn = randint(0, len(self.all_turns) - 1)
        self.figure_center = (self.width // 2 - 1, 1)
        x, y = self.figure_center
        self.over = any(self.board_fixed[y + b_y][x + b_x] for b_x, b_y in self.all_turns[self.cur_figure_turn])

    def fix_board(self):  # Фиксация текущей фигуры
        c_x, c_y = self.figure_center  # центр фигуры
        for x, y in self.all_turns[self.cur_figure_turn]:
            self.board_fixed[y + c_y][x + c_x] = 1

    def board_clear(self):  # Возвращает пустую таблицу
        return [[0] * self.width for _ in range(self.height)]


class OverlayError(Exception):
    pass
