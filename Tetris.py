from random import choice, randint

import pygame as pg

from utils import COLOR_FIGURE, COLOR_FIGURE_BORDERS, COLOR_FIELD_BORDERS, COLOR_FIELD_BACKGROUND
from utils import get_frames


class Tetris:
    def __init__(self, f_size=(10, 15)):
        self.field = Field(f_size)  # Создание поля
        # значения по умолчанию
        self.cell_size = 30
        self.all_sprites = pg.sprite.Group()
        self.frames_flames = get_frames('flame_frames')
        self.flames = []
        for i in range(4):
            self.flames.append(Flame(self.cell_size, (0, 0), self.frames_flames,
                  self.all_sprites))

    # Параметры
    def set_view(self, cell_size):
        self.cell_size = cell_size

    def render(self, screen):
        screen.fill(COLOR_FIELD_BACKGROUND)
        f_x, f_y = self.field.figure_center  # Центр фигуры
        for y in range(self.field.height):  # Отрисовка статичного поля
            for x in range(self.field.width):
                cell_value = self.field.board_fixed[y][x]
                if cell_value == 0:
                    pg.draw.rect(screen, COLOR_FIELD_BORDERS,
                                 (self.cell_size * x, self.cell_size * y, self.cell_size, self.cell_size), 1)
                elif cell_value == 1:
                    pg.draw.rect(screen, COLOR_FIGURE,
                                 (self.cell_size * x, self.cell_size * y, self.cell_size, self.cell_size))
        self.all_sprites.update()
        self.all_sprites.draw(screen)
        num = 0
        for x, y in self.field.all_turns[self.field.cur_figure_turn]:  # Отрисовка падающей фигуры
            self.flames[num].rect.x = (x + f_x - 0.5) * self.cell_size
            self.flames[num].rect.y = (y + f_y - 1.5) * self.cell_size
            num += 1
            pg.draw.rect(screen, COLOR_FIGURE,
                         (self.cell_size * (x + f_x), self.cell_size * (y + f_y), self.cell_size, self.cell_size))
            pg.draw.rect(screen, COLOR_FIGURE_BORDERS, (
                self.cell_size * (x + f_x) - 1, self.cell_size * (y + f_y) - 1, self.cell_size + 2, self.cell_size + 2),
                         2)


class Field:  # Класс поля
    shapes = list({
                      'I': [((0, -1), (0, 0), (0, 1), (0, 2)), ((-1, 0), (0, 0), (1, 0), (2, 0))],
                      'J': [((0, -1), (1, -1), (0, 0), (0, 1)), ((-1, 0), (0, 0), (1, 0), (1, 1)),
                            ((0, -1), (0, 0), (-1, 1), (0, 1)), ((-1, -1), (0, 0), (-1, 0), (1, 0))],
                      'L': [((-1, -1), (0, -1), (0, 0), (0, 1)), ((1, 1), (0, 0), (-1, 0), (1, 0)),
                            ((0, -1), (0, 0), (0, 1), (1, 1)), ((-1, 0), (0, 0), (1, 0), (1, -1))],
                      'O': [((0, 0), (1, 0), (0, 1), (1, 1))],
                      'S': [((0, -1), (0, 0), (1, 0), (1, 1)), ((0, 0), (1, 0), (-1, 1), (0, 1))],
                      'T': [((0, -1), (-1, 0), (0, 0), (1, 0)), ((0, -1), (0, 0), (1, 0), (0, 1)),
                            ((-1, 0), (0, 0), (1, 0), (0, 1)), ((0, -1), (-1, 0), (0, 0), (0, 1))],
                      'Z': [((1, -1), (0, 0), (1, 0), (0, 1)), ((-1, -1), (0, -1), (0, 0), (1, 0))]
                  }.items())  # Координаты относительно центра: (x, y)

    # Названия всех вариантов фигур со всеми вариантами расположения,
    # первым считать вертикальное положение "головой" вверх

    def __init__(self, size):
        self.score = 0
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
        self.figure_fall()  # Падение фигуры
        self.check_line()  # Проверяет на составление линии

    def figure_rotate(self):  # Поворот фигуры
        blocks = self.all_turns[(self.cur_figure_turn + 1) % len(self.all_turns)]
        cells_empty = all(set(map(self.empty_block, blocks)))
        if cells_empty:
            self.cur_figure_turn = (self.cur_figure_turn + 1) % len(self.all_turns)

    def figure_shift(self):  # Сдвиг фигуры
        blocks = self.all_turns[self.cur_figure_turn]
        x, y = self.figure_center
        cells_empty = all(set(map(lambda cc: self.empty_block((cc[0] + self.shift_side, cc[1])), blocks)))
        if cells_empty:
            self.figure_center = (x + self.shift_side, y)

    def figure_fall(self):  # Падение фигуры
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

    def check_line(self):  # Проверка заполненна ли линия
        for y in self.board_fixed:
            if all(y):
                self.board_fixed.remove(y)
                self.board_fixed.insert(0, [0] * self.width)
                self.score += 100

    # empty_block:
    # (0: Клетка не пустая/вне таблицы по координате Y; 1: В таблице, пустая без сдвига; 2: В таблице, пустая клетка)
    # Вход координат относительно центра фигуры

    def new_figure(self):  # Появление новой фигуры
        self.all_turns = choice(self.shapes)[1]  # Выбор новой фигуры, запись положений всех блоков относительно центра
        self.cur_figure_turn = randint(0, len(self.all_turns) - 1)  # Поворот созданной фигуры
        self.figure_center = (self.width // 2 - 1, 1)
        x, y = self.figure_center
        self.over = any(list(self.board_fixed[y + b_y][x + b_x] for b_x, b_y in self.all_turns[self.cur_figure_turn]))  # ...

    def fix_board(self):  # Фиксация текущей фигуры
        c_x, c_y = self.figure_center  # центр фигуры
        for x, y in self.all_turns[self.cur_figure_turn]:
            self.board_fixed[y + c_y][x + c_x] = 1  # Если фигура устаялась на месте: 1

    def board_clear(self):  # Возвращает пустую таблицу
        return [[0] * self.width for _ in range(self.height)]  # опустошение фигуры


class Flame(pg.sprite.Sprite):  # Класс спрайтов огня
    def __init__(self, size, coords, frames, *group):
        super().__init__(*group)
        self.flame_frames = frames
        self.cur_frame = 0
        self.image = self.flame_frames[self.cur_frame]
        self.image = pg.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(coords[0], coords[1])

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.flame_frames)
        self.image = self.flame_frames[self.cur_frame]


class OverlayError(Exception):
    pass
